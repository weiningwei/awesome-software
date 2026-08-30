# Repository Guidelines

## Project Structure & Module Organization

This repository is a curated Markdown directory rather than an executable application:

- `README.md` contains the primary software list, organized by functional category and subcategory.
- `app.md` contains a separate list of Android applications.
- `CONTRIBUTING.md` is the authoritative reference for entry format, badges, categorization, and quality standards.
- `LICENSE` describes the license for the curated content; `.gitignore` contains repository exclusions.

There are no source-code, asset, or test directories. Keep changes focused on the relevant Markdown file.

## Build, Test, and Development Commands

No build, package, or application-run commands are configured. Before submitting documentation changes, use:

```text
git diff --check
rg "软件名或仓库名" README.md app.md
```

`git diff --check` catches whitespace errors; `rg` (ripgrep) helps prevent duplicate entries. If `rg` is unavailable, use `git grep` or editor search instead. Review the rendered Markdown and verify every external link manually when adding entries.

## Coding Style & Naming Conventions

Use UTF-8 Markdown with two-space-friendly readable wrapping and consistent list syntax. Software entries follow:

```markdown
- [Official Name](https://github.com/owner/repo) - 客观的一句话简介。 `平台` `SPDX-License` ![GitHub Repo stars](...)
```

Use the official software name, a concise factual description ending in `。`, and backtick labels such as `` `Windows` `` or `` `跨平台` ``. For GitHub projects, use shields.io badges in the established order: stars, latest release, then release date. Append new entries to the end of the best-matching category.

## Testing Guidelines

There is no test framework or coverage requirement. Validate structural correctness through `git diff --check`, duplicate searches, link checks, and a rendered Markdown review. Confirm that the project is open source or offers a free version and is not clearly archived, abandoned, or ad-supported/malicious.

## Commit & Pull Request Guidelines

Recent commits use concise documentation subjects, commonly `docs: ...` or Chinese descriptions such as `添加 ...`. Follow that style and describe the category change directly (for example, `docs: add ExampleApp to clipboard tools`). PRs should identify the added or changed software, explain its category choice, follow `CONTRIBUTING.md`, and include no unrelated edits. Link an issue when one exists; screenshots are unnecessary for text-only changes.
