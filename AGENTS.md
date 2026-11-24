# Repository Guidelines

## Project Structure & Module Organization

This repository is a curated Markdown directory rather than an executable application:

- `README.md` is the generated, badge-free index of every software entry, grouped by category and subcategory.
- `lists/*.md` contains the editable software entries, organized by functional category and subcategory.
- `lists/android.md` contains the editable list of Android applications.
- `scripts/build_readme.py` regenerates the README index from the category files in `lists/`.
- `CONTRIBUTING.md` is the authoritative reference for entry format, badges, categorization, and quality standards.
- `LICENSE` describes the license for the curated content; `.gitignore` contains repository exclusions.

There is no application build or test suite. Add or edit software only in the relevant category file, then regenerate `README.md`.

## Build, Test, and Development Commands

No application build or run commands are configured. Before submitting documentation changes, use:

```text
python scripts/build_readme.py
python scripts/build_readme.py --check
python scripts/refresh_dates.py --dry-run
git diff --check
rg "软件名或仓库名" lists
```

`refresh_dates.py` refreshes the static release-date column (GraphQL batches by default, `--mode rest` per repository, `--style dynamic` for auto-updating badges); `git diff --check` catches whitespace errors; `rg` (ripgrep) helps prevent duplicate entries. If `rg` is unavailable, use `git grep` or editor search instead. Review the rendered Markdown and verify every external link manually when adding entries.

## Coding Style & Naming Conventions

Use UTF-8 Markdown with two-space-friendly readable wrapping and consistent list syntax. Software entries follow:

```markdown
| 软件 | Stars | 版本 | 发布日期 | 简介 |
| --- | --- | --- | --- | --- |
| [Official Name](https://github.com/owner/repo) | ![GitHub Repo stars](https://img.shields.io/github/stars/owner/repo?style=flat) | ![GitHub Release](https://img.shields.io/github/v/release/owner/repo?style=flat) | ![Date](https://img.shields.io/badge/YYYY--MM--DD-1a7f37) | 客观的一句话简介。 `平台` `SPDX-License` |
```

Each subcategory is a fixed five-column table: software, Stars, version, release date, description. Use the official software name linked to its repo, shields.io stars and version badges plus a static green date badge (`![Date](https://img.shields.io/badge/YYYY--MM--DD-1a7f37)`, the latest Release date in UTC) in the three badge columns, and a concise factual description ending in `。`, followed by backtick platform/license labels such as `` `Windows` `` or `` `跨平台` ``. Leave a cell empty when it does not apply, and use only stars when the project has no GitHub Release. Add new rows anywhere in the best-matching subcategory table; the daily workflow re-sorts rows by stars. Never edit the generated README entries directly.

## Testing Guidelines

There is no test framework or coverage requirement. Validate structural correctness through `git diff --check`, duplicate searches, link checks, and a rendered Markdown review. Confirm that the project is open source or offers a free version and is not clearly archived, abandoned, or ad-supported/malicious.

## Commit & Pull Request Guidelines

Recent commits use concise documentation subjects, commonly `docs: ...` or Chinese descriptions such as `添加 ...`. Follow that style and describe the category change directly (for example, `docs: add ExampleApp to clipboard tools`). PRs should identify the added or changed software, explain its category choice, follow `CONTRIBUTING.md`, and include no unrelated edits. Link an issue when one exists; screenshots are unnecessary for text-only changes.
