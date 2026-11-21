"""Refresh the release-date column in lists/*.md.

The date is normally a static shields.io badge. Looking up every repository
individually costs one GitHub request per project, so this script queries them
through GraphQL in batches by default and only falls back to per-repository
REST calls for entries GraphQL cannot resolve.

Usage:
    python scripts/refresh_dates.py                 # GraphQL batches, static badges
    python scripts/refresh_dates.py --dry-run       # show what would change
    python scripts/refresh_dates.py --mode rest     # one REST call per repository
    python scripts/refresh_dates.py --style dynamic # restore auto-updating badges

Both badge styles are understood on input, so a file may mix them.
Repositories without a release keep the version and date columns empty.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
LISTS = sorted((ROOT / "lists").glob("*.md"))

STATIC_DATE = re.compile(
    r"!\[(?:Date|GitHub Release Date)\]\(https://img\.shields\.io/badge/\d{4}--\d{2}--\d{2}-[0-9a-fA-F]{6}\)"
)
DYNAMIC_DATE = re.compile(
    r"!\[GitHub Release Date\]\(https://img\.shields\.io/github/release-date/([^?)]+)\?[^)]*\)"
)
REPO = re.compile(r"github\.com/([^/\s)|]+/[^/\s)|]+)")


def badge_static(day: str) -> str:
    return f"![Date](https://img.shields.io/badge/{day.replace('-', '--')}-1a7f37)"


def badge_dynamic(repo: str) -> str:
    return (
        f"![GitHub Release Date](https://img.shields.io/github/release-date/{repo}"
        "?label=&display_date=published_at&style=flat)"
    )


def read_lists() -> dict[Path, list[str]]:
    return {path: path.read_text(encoding="utf-8").splitlines() for path in LISTS}


def rows_with_repos(files: dict[Path, list[str]]) -> dict[str, list[tuple[Path, int]]]:
    """Map repository -> [(file, line index)] for table rows linking to GitHub."""
    found: dict[str, list[tuple[Path, int]]] = {}
    for path, lines in files.items():
        for index, line in enumerate(lines):
            if not line.startswith("| ["):
                continue
            first_cell = line.split("|")[1]
            match = REPO.search(first_cell)
            if match:
                found.setdefault(match.group(1), []).append((path, index))
    return found


def gh(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["gh", *args], capture_output=True, text=True, encoding="utf-8", timeout=120
    )


def latest_dates_graphql(repos: list[str], batch_size: int) -> tuple[dict[str, str], list[str]]:
    dates: dict[str, str] = {}
    unresolved: list[str] = []
    for start in range(0, len(repos), batch_size):
        batch = repos[start : start + batch_size]
        aliases = []
        for number, repo in enumerate(batch):
            owner, name = repo.split("/", 1)
            aliases.append(
                f'r{number}: repository(owner: "{owner}", name: "{name}") '
                "{ latestRelease { publishedAt } }"
            )
        query = "query { " + " ".join(aliases) + " }"
        result = gh("api", "graphql", "-f", f"query={query}")
        try:
            payload = json.loads(result.stdout) if result.stdout.strip() else {}
        except json.JSONDecodeError:
            payload = {}
        data = payload.get("data") or {}
        if result.returncode != 0 and not data:
            print(f"GraphQL batch failed: {result.stderr.strip()}", file=sys.stderr)
            unresolved.extend(batch)
            continue
        # One unknown repository makes gh exit non-zero while the rest of the
        # batch still resolves, so trust the aliases that came back.
        for number, repo in enumerate(batch):
            node = data.get(f"r{number}")
            if not node:
                unresolved.append(repo)
                continue
            release = node.get("latestRelease") or {}
            published = release.get("publishedAt")
            if published:
                dates[repo] = published[:10]
            else:
                unresolved.append(repo)
    return dates, unresolved


def latest_dates_rest(repos: list[str]) -> tuple[dict[str, str], list[str]]:
    """Return known dates and repositories whose lookup failed (not a 404)."""

    def one(repo: str) -> tuple[str, str | None, bool]:
        for attempt in range(3):
            result = gh("api", f"repos/{repo}/releases/latest", "--jq", ".published_at")
            if result.returncode == 0:
                value = result.stdout.strip()
                day = value[:10] if re.fullmatch(r"\d{4}-\d{2}-\d{2}.*", value) else None
                return repo, day, False
            if "not found" in result.stderr.lower():
                return repo, None, False
            time.sleep(1 + attempt)
        return repo, None, True

    dates: dict[str, str] = {}
    failed: list[str] = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        for repo, day, failed_call in pool.map(one, repos):
            if day:
                dates[repo] = day
            elif failed_call:
                failed.append(repo)
    return dates, failed


def collect_dates(repos: list[str], mode: str, batch_size: int) -> tuple[dict[str, str], set[str]]:
    """Return known dates and repositories that must be left untouched."""
    if mode == "rest":
        dates, failed = latest_dates_rest(repos)
        return dates, set(failed)
    dates, unresolved = latest_dates_graphql(repos, batch_size)
    if mode == "graphql":
        return dates, set(unresolved)
    if unresolved:
        print(f"Falling back to REST for {len(unresolved)} repositories")
        rest_dates, failed = latest_dates_rest(unresolved)
        dates.update(rest_dates)
        return dates, set(failed)
    return dates, set()


def rewrite(
    style: str,
    dates: dict[str, str],
    files: dict[Path, list[str]],
    dry_run: bool,
    failed: set[str],
) -> tuple[int, int]:
    changed = 0
    without_date = 0
    for repo, occurrences in rows_with_repos(files).items():
        if repo in failed:
            continue
        day = dates.get(repo)
        for path, index in occurrences:
            line = files[path][index]
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) != 5:
                print(f"Skipping malformed row in {path.name}:{index + 1}")
                continue
            if day is None:
                # No release: the version and date columns stay empty.
                if not cells[2] and not cells[3]:
                    continue
                cells[2] = cells[3] = ""
                without_date += 1
            else:
                cells[3] = badge_static(day) if style == "static" else badge_dynamic(repo)
            new_line = "| " + " | ".join(cells) + " |"
            if new_line == line:
                continue
            files[path][index] = new_line
            changed += 1
    if not dry_run and changed:
        for path, lines in files.items():
            path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return changed, without_date


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=("auto", "graphql", "rest"),
        default="auto",
        help="GraphQL batches by default; auto falls back to REST per repository",
    )
    parser.add_argument(
        "--style",
        choices=("static", "dynamic"),
        default="static",
        help="static writes a colored YYYY-MM-DD badge; dynamic restores the shields date badge",
    )
    parser.add_argument("--batch-size", type=int, default=50)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    files = read_lists()
    repos = sorted(rows_with_repos(files))
    print(f"{len(repos)} repositories in {len(files)} list files")
    dates, failed = collect_dates(repos, args.mode, args.batch_size)
    missing = [repo for repo in repos if repo not in dates and repo not in failed]
    changed, without_date = rewrite(args.style, dates, files, args.dry_run, failed)
    verb = "would change" if args.dry_run else "changed"
    print(f"{verb} {changed} rows")
    if args.style == "static":
        print(f"{without_date} rows have no release and keep the version/date columns empty")
    if missing:
        print(f"{len(missing)} repositories returned no release, e.g. {', '.join(missing[:5])}")
    if failed:
        print(f"{len(failed)} repositories could not be queried and were left untouched")


if __name__ == "__main__":
    main()
