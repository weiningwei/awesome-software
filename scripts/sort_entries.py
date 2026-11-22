"""Sort every list table by GitHub stars (descending).

Star counts only exist inside shields.io badge images, so ordering cannot be
derived from the Markdown alone. This script queries stargazerCount through
GraphQL in batches, then rewrites each subcategory table as stars descending.
Rows without a GitHub repository (official-site links or the invalid badge)
keep their original order and move to the bottom of the table.

Usage:
    python scripts/sort_entries.py            # rewrite lists in place
    python scripts/sort_entries.py --check    # exit 1 when a table is out of order
    python scripts/sort_entries.py --dry-run  # report without writing

The daily refresh workflow runs this after refreshing release dates and
regenerates README.md so the index follows the new order.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
LISTS = sorted((ROOT / "lists").glob("*.md"))
SKIP = {"fonts.md"}
STARS = re.compile(r"img\.shields\.io/github/stars/([^?)\s]+)\?")


def read_lists() -> dict[Path, list[str]]:
    return {path: path.read_text(encoding="utf-8").splitlines() for path in LISTS}


def row_repo(line: str) -> str | None:
    """Return owner/repo from the stars badge of a table row."""
    match = STARS.search(line)
    return match.group(1) if match else None


def repos_in(files: dict[Path, list[str]]) -> list[str]:
    found: set[str] = set()
    for path, lines in files.items():
        if path.name in SKIP:
            continue
        for line in lines:
            if not line.startswith("| ["):
                continue
            repo = row_repo(line)
            if repo:
                found.add(repo)
    return sorted(found)


def gh(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["gh", *args], capture_output=True, text=True, encoding="utf-8", timeout=120
    )


def fetch_stars(repos: list[str], batch_size: int) -> dict[str, int]:
    """Return owner/repo -> stars, retrying a batch before giving up."""
    stars: dict[str, int] = {}
    unresolved: list[str] = []
    for start in range(0, len(repos), batch_size):
        batch = repos[start : start + batch_size]
        aliases = []
        for number, repo in enumerate(batch):
            owner, name = repo.split("/", 1)
            aliases.append(
                f'r{number}: repository(owner: "{owner}", name: "{name}") '
                "{ stargazerCount }"
            )
        query = "query { " + " ".join(aliases) + " }"
        data: dict = {}
        for attempt in range(3):
            result = gh("api", "graphql", "-f", f"query={query}")
            try:
                data = (json.loads(result.stdout) if result.stdout.strip() else {}).get(
                    "data"
                ) or {}
            except json.JSONDecodeError:
                data = {}
            if data:
                break
            print(f"GraphQL batch failed: {result.stderr.strip()}", file=sys.stderr)
            time.sleep(1 + attempt)
        for number, repo in enumerate(batch):
            node = data.get(f"r{number}")
            if not node:
                unresolved.append(repo)
                continue
            stars[repo] = int(node.get("stargazerCount") or 0)
    if unresolved:
        raise RuntimeError(
            f"{len(unresolved)} repositories could not be queried: "
            + ", ".join(unresolved[:5])
        )
    return stars


def sort_key(line: str, stars: dict[str, int]) -> tuple[int, int]:
    repo = row_repo(line)
    if repo is None or repo not in stars:
        return (0, 0)
    return (1, stars[repo])


def reorder(
    files: dict[Path, list[str]], stars: dict[str, int], check: bool
) -> tuple[int, list[str], set[Path]]:
    """Rewrite table blocks in place; return changed rows, messages, dirty files."""
    changed = 0
    messages: list[str] = []
    dirty: set[Path] = set()
    for path, lines in files.items():
        if path.name in SKIP:
            continue
        section = ""
        index = 0
        while index < len(lines):
            line = lines[index]
            if line.startswith("## "):
                section = line[3:].strip()
            if not line.startswith("|"):
                index += 1
                continue
            start = index
            while index < len(lines) and lines[index].startswith("|"):
                index += 1
            block = lines[start:index]
            head, rows = block[:2], block[2:]
            order = sorted(
                range(len(rows)), key=lambda number: sort_key(rows[number], stars), reverse=True
            )
            ordered = [rows[number] for number in order]
            if ordered == rows:
                continue
            moved = sum(1 for old, new in zip(rows, ordered) if old != new)
            changed += moved
            messages.append(
                f"- {path.name} / {section or path.stem}: {moved} rows reordered"
            )
            if not check:
                lines[start:index] = head + ordered
                dirty.add(path)
    return changed, messages, dirty


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail instead of writing")
    parser.add_argument("--dry-run", action="store_true", help="report without writing")
    parser.add_argument("--batch-size", type=int, default=50)
    parser.add_argument(
        "--log",
        type=Path,
        metavar="PATH",
        help="write the run summary and every reordered table to this file",
    )
    args = parser.parse_args()

    files = read_lists()
    repos = repos_in(files)
    print(f"{len(repos)} repositories in {len(files)} list files")
    try:
        stars = fetch_stars(repos, args.batch_size)
    except RuntimeError as error:
        print(error, file=sys.stderr)
        return 2

    check = args.check or args.dry_run
    changed, messages, dirty = reorder(files, stars, check)
    if not check:
        for path in sorted(dirty):
            path.write_text(
                "\n".join(files[path]) + "\n", encoding="utf-8", newline="\n"
            )

    if check:
        for message in messages:
            print(message.lstrip("- "))
        print(f"{changed} rows out of order" if changed else "every table is sorted")
    else:
        for message in messages:
            print(message)
        print(f"reordered {changed} rows" if changed else "every table is sorted")

    if args.log:
        lines = [
            "# Star sort",
            "",
            f"- repositories: {len(repos)}",
            f"- reordered rows: {changed}",
            "",
            "## Tables",
            "",
            *(messages or ["- none"]),
            "",
        ]
        args.log.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    return 1 if args.check and changed else 0


if __name__ == "__main__":
    sys.exit(main())
