"""Build the badge-free, collapsible README index from category Markdown files."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CATEGORIES = [
    ("截图与录屏", "lists/screenshot-recording.md"),
    ("剪贴板", "lists/clipboard.md"),
    ("文件搜索与启动", "lists/search-launch.md"),
    ("识别与翻译", "lists/recognition-translation.md"),
    ("局域网传输", "lists/local-transfer.md"),
    ("远程桌面", "lists/remote-desktop.md"),
    ("网页转桌面", "lists/web-to-desktop.md"),
    ("系统工具", "lists/system.md"),
    ("下载", "lists/download.md"),
    ("开发工具", "lists/development.md"),
    ("字体", "lists/fonts.md"),
    ("AI 工具", "lists/ai.md"),
    ("多媒体", "lists/media.md"),
    ("文档与阅读", "lists/documents.md"),
    ("网站", "lists/websites.md"),
]
BADGE = re.compile(r"\s*!\[[^]]*\]\(https://img\.shields\.io/[^)]*\)")
ENTRY = re.compile(r"^- \[[^]]+\]\(https?://")


def index_lines(path: str) -> tuple[list[str], int]:
    lines = (ROOT / path).read_text(encoding="utf-8").splitlines()
    result: list[str] = []
    count = 0
    for line in lines:
        if line.startswith("## "):
            result.extend(("#### " + line[3:], ""))
        elif ENTRY.match(line):
            result.append(BADGE.sub("", line).rstrip())
            count += 1
    if not count:
        raise ValueError(f"No software entries found in {path}")
    return result, count


def build() -> str:
    sections = []
    for name, path in CATEGORIES:
        entries, count = index_lines(path)
        sections.append((name, path, entries, count))
    total = sum(count for *_, count in sections)

    output = [
        "# awesome-software",
        "",
        "<!-- 由 scripts/build_readme.py 生成；请编辑 lists/*.md。 -->",
        "",
        f"按功能整理的软件清单，共收录 {total} 款。首页列出全部软件；"
        "点击分类标题可打开分类页面，查看星标、最新版本与发布日期。",
        "",
        "## 分类",
        "",
    ]
    for name, _, _, count in sections:
        anchor = name.lower().replace(" ", "-")
        output.append(f"- [{name}](#{anchor}) · {count} 款")
    output.extend(("", "## 软件清单", ""))
    for name, path, entries, count in sections:
        output.extend(
            (
                f"### [{name}]({path})",
                "",
                "<details>",
                f"<summary>展开 {count} 款软件</summary>",
                "",
                *entries,
                "",
                "</details>",
                "",
            )
        )
    output.extend(
        (
            "## 贡献",
            "",
            "欢迎推荐好用的开源或免费软件。添加条目的格式与分类规则请阅读 [贡献指南](CONTRIBUTING.md)。",
            "",
        )
    )
    return "\n".join(output)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if README.md is out of date")
    args = parser.parse_args()
    target = ROOT / "README.md"
    generated = build()
    if args.check:
        if target.read_text(encoding="utf-8") != generated:
            parser.exit(1, "README.md is out of date; run python scripts/build_readme.py\n")
        print("README.md is up to date")
    else:
        target.write_text(generated, encoding="utf-8", newline="\n")
        print("Updated README.md")


if __name__ == "__main__":
    main()
