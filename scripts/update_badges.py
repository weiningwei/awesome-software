"""Rewrite live shields.io release-date badges into static, formatted date badges.

The generated badge looks like:

    ![Date](https://img.shields.io/badge/2026--11--17-blue)

Run it on a file (optionally limited to one "## section") and commit the result:

    python scripts/update_badges.py --section 网络代理 lists/system.md
    python scripts/update_badges.py --check lists/system.md

Set GITHUB_TOKEN to raise the GitHub API rate limit when touching many entries.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATE_BADGE = re.compile(
    r"!\[(?P<alt>[^\]]*)\]"
    r"\(https://img\.shields\.io/github/release-date/"
    r"(?P<owner>[^/?)]+)/(?P<repo>[^/?)]+)\?[^)]*\)"
)
COLOR = "blue"


def latest_release_date(slug: str, token: str | None) -> str | None:
    """Return the ISO date of the newest GitHub release, or None when there is none."""
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "awesome-software-badge-updater",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(
        f"https://api.github.com/repos/{slug}/releases/latest", headers=headers
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise
    published = payload.get("published_at") or ""
    return published[:10] or None


def badge(match: re.Match[str], dates: dict[str, str | None], token: str | None) -> str:
    alt = match.group("alt") or "Date"
    slug = f"{match.group('owner')}/{match.group('repo')}"
    if slug not in dates:
        dates[slug] = latest_release_date(slug, token)
    date = dates[slug]
    if not date:
        return match.group(0)
    return f"![{alt}](https://img.shields.io/badge/{date.replace('-', '--')}-{COLOR})"


def rewrite(
    text: str, sections: set[str], token: str | None, dates: dict[str, str | None]
) -> tuple[str, int]:
    lines = text.split("\n")
    current: str | None = None
    changed = 0
    for index, line in enumerate(lines):
        if line.startswith("## "):
            current = line[3:].strip()
            continue
        if line.startswith("# "):
            current = None
            continue
        if sections and current not in sections:
            continue
        if "img.shields.io/github/release-date/" not in line:
            continue
        updated = DATE_BADGE.sub(lambda m: badge(m, dates, token), line)
        if updated != line:
            lines[index] = updated
            changed += 1
    return "\n".join(lines), changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="Markdown files to update")
    parser.add_argument(
        "--section",
        action="append",
        default=[],
        metavar="NAME",
        help="only rewrite entries under this ## heading (repeatable)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="report files that need updating and exit non-zero",
    )
    args = parser.parse_args()
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    sections = {name.strip() for name in args.section}
    dates: dict[str, str | None] = {}
    stale: list[tuple[Path, int]] = []

    for path in args.paths:
        target = path if path.is_absolute() else ROOT / path
        with open(target, "r", encoding="utf-8", newline="") as handle:
            text = handle.read()
        updated, changed = rewrite(text, sections, token, dates)
        if not changed:
            continue
        stale.append((target, changed))
        if not args.check:
            with open(target, "w", encoding="utf-8", newline="") as handle:
                handle.write(updated)

    for target, changed in stale:
        try:
            shown = target.relative_to(ROOT)
        except ValueError:
            shown = target
        print(f"{shown}: {changed} line(s) need formatted dates")
    if not stale:
        print("All release-date badges are already static")
    return 1 if (args.check and stale) else 0


if __name__ == "__main__":
    sys.exit(main())
