# Repository Guidelines

## Project Structure & Module Organization

This repository is a curated Markdown directory rather than an executable application:

- `README.md` is the generated, badge-free index of every software entry, grouped into collapsible categories.
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
git diff --check
rg "软件名或仓库名" lists
```

`git diff --check` catches whitespace errors; `rg` (ripgrep) helps prevent duplicate entries. If `rg` is unavailable, use `git grep` or editor search instead. Review the rendered Markdown and verify every external link manually when adding entries.

## Coding Style & Naming Conventions

Use UTF-8 Markdown with two-space-friendly readable wrapping and consistent list syntax. Software entries follow:

```markdown
- [Official Name](https://github.com/owner/repo) - 客观的一句话简介。 `平台` `SPDX-License` ![GitHub Repo stars](https://img.shields.io/github/stars/owner/repo?style=flat) ![GitHub Release](https://img.shields.io/github/v/release/owner/repo?style=flat) ![GitHub Release Date](https://img.shields.io/github/release-date/owner/repo?display_date=published_at&style=flat)
```

Use the official software name, a concise factual description ending in `。`, and backtick labels such as `` `Windows` `` or `` `跨平台` ``. For GitHub projects, use shields.io badges in this order: stars, latest release, release date. Omit the latter two when the project has no GitHub Release. Append new entries to the end of the best-matching category. Never edit the generated README entries directly.

## Testing Guidelines

There is no test framework or coverage requirement. Validate structural correctness through `git diff --check`, duplicate searches, link checks, and a rendered Markdown review. Confirm that the project is open source or offers a free version and is not clearly archived, abandoned, or ad-supported/malicious.

## Commit & Pull Request Guidelines

Recent commits use concise documentation subjects, commonly `docs: ...` or Chinese descriptions such as `添加 ...`. Follow that style and describe the category change directly (for example, `docs: add ExampleApp to clipboard tools`). PRs should identify the added or changed software, explain its category choice, follow `CONTRIBUTING.md`, and include no unrelated edits. Link an issue when one exists; screenshots are unnecessary for text-only changes.
