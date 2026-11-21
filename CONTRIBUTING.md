# 贡献指南 / Contributing

感谢你为 awesome-software 推荐好用的开源软件！本指南说明条目的**标准格式**、**徽章约定**、**分类规则**与**提交流程**，新增条目请遵循此处规范。分类文件（`lists/*.md`）是软件与字体条目的维护位置；下载站等资料见 `RESOURCES.md`。`README.md` 中的索引由脚本生成。

## 条目格式标准

每个子分类维护一张对照表，列固定为 **软件 / Stars / 版本 / 发布日期 / 简介**，平台与协议以反引号标签附在简介末尾，同一列的徽章自然对齐，便于比较星标与版本（参考 [awesome-selfhosted](https://github.com/awesome-selfhosted/awesome-selfhosted) 与 [sindresorhus/awesome](https://github.com/sindresorhus/awesome) 规范）：

```markdown
| 软件 | Stars | 版本 | 发布日期 | 简介 |
| --- | --- | --- | --- | --- |
| [软件名](仓库或主页链接) | ![GitHub Repo stars](https://img.shields.io/github/stars/owner/repo?label=&style=flat) | ![GitHub Release](https://img.shields.io/github/v/release/owner/repo?label=&style=flat) | ![GitHub Release Date](https://img.shields.io/github/release-date/owner/repo?label=&display_date=published_at&style=flat) | 一句话简介。 `平台` `开源协议` |
```

### 字段说明

| 列 | 必填 | 说明 |
| --- | --- | --- |
| 软件 | ✅ | 官方名称的链接；优先填 GitHub 仓库地址，官网也可 |
| Stars | 🔶 | GitHub 项目的 stars 徽章；非 GitHub 项目留空 |
| 版本 / 发布日期 | 🔶 | 有 GitHub Release 时填写版本徽章与静态日期徽章（`![Date](https://img.shields.io/badge/YYYY--MM--DD-1a7f37)`），没有则留空 |
| 简介 | ✅ | 一句话客观描述功能，以句号（。）结尾，避免营销用语；末尾可附平台与协议标签 |

> 🔶 = 建议填写，但非强制；存量条目正在逐步统一为该格式。

### 格式细则

- 表头与分隔行固定为五列，不要增删列或调换顺序；同一子分类只维护一张表
- 新增条目追加为表格最后一行；没有值的单元格留空，不要写 `-` 或 `无`
- 单元格内不要出现 `|`，简介不换行；软件名与简介之间不再使用 ` - ` 分隔
- 平台、协议用反引号（`` ` ``）包裹，附在简介末尾，多个标签以空格分隔
- 简介客观准确，不写「最好用」「神器」「必备」等主观评价
- GitHub 条目填写 stars 徽章；有 Release 的条目再填写版本与发布日期徽章

### 正反例对比

✅ **正确**
```markdown
| [LocalSend](https://github.com/localsend/localsend) | ![GitHub Repo stars](https://img.shields.io/github/stars/localsend/localsend?label=&style=flat) | ![GitHub Release](https://img.shields.io/github/v/release/localsend/localsend?label=&style=flat) | ![GitHub Release Date](https://img.shields.io/github/release-date/localsend/localsend?label=&display_date=published_at&style=flat) | 局域网内跨设备文件传输工具。 `跨平台` `MIT` |
```

❌ **错误**（问题：用列表项而非表格行、缺平台/协议、营销用语）
```markdown
- [localsend](https://github.com/localsend/localsend) : 超好用的局域网传文件神器
```

## 徽章约定

GitHub 条目使用 [shields.io](https://shields.io) 徽章，按 **Stars → 版本 → 发布日期** 依次放在三列中。如果项目没有 GitHub Release，后两列留空，只填 stars 徽章：

```markdown
![GitHub Repo stars](https://img.shields.io/github/stars/owner/repo?label=&style=flat)
![GitHub Release](https://img.shields.io/github/v/release/owner/repo?label=&style=flat)
![Date](https://img.shields.io/badge/2026--11--03-1a7f37)
```

- `owner/repo` 需替换为真实路径，且必须与条目链接指向同一仓库
- 非 GitHub 项目（如官网、GitLab）不添加这些徽章
- 徽章左标签留空（`label=`），只显示数值，避免重复出现 stars / release 字样
- 无 GitHub Release 的项目不添加版本与发布日期徽章，这两列留空（`refresh_dates.py` 会清空）；不要添加 CI / build 状态等无关徽章
- 发布日期使用静态 badge，日期取最新 Release 的发布时间（UTC），格式 `YYYY--MM--DD`，颜色固定 `1a7f37`；可用 `python scripts/refresh_dates.py` 批量同步
- 刷新脚本兼容两种取数方式：`--mode graphql`（默认，批量）与 `--mode rest`（逐个仓库）；也兼容两种徽章写法：`--style static`（默认）与 `--style dynamic`
- 静态日期 badge 不代表仓库最近提交时间，也不随 Release 自动更新
- `README.md` 首页索引不显示逐项徽章，徽章仅保留在分类文件（`lists/*.md`）

## 如何添加一款软件

1. 在 `README.md` 中找到最匹配的**分类 / 子分类**，打开对应的 `lists/*.md`
2. 将新条目作为该子分类表格的**最后一行**追加，不要直接修改 `README.md` 中的生成内容
3. 按上述列填写（至少包含：软件、简介）
4. 运行 `python scripts/refresh_dates.py` 刷新发布日期：默认用 GraphQL 每批 50 个仓库查询，一次调用即可覆盖大部分条目；`--mode rest` 改为逐个仓库查询，`--style dynamic` 可切回自动更新的动态徽章
5. 运行 `python scripts/build_readme.py` 更新首页，再运行 `python scripts/build_readme.py --check` 和 `git diff --check`
6. 提交 Pull Request，标题形如 `Add 软件名` 或 `新增 软件名`

## 分类标准

分类以**核心功能**为唯一维度，遵循以下规则：

1. **唯一归属**：每款软件按其核心功能归入且仅归入一个分类；具备多项功能时，按用户最常使用的功能判定。
2. **二级结构**：分类文件的标题（`#`）为功能域，子级（`##`）为具体功能。子分类一般不少于 3 款；功能独立、无法合并的子分类不少于 2 款；仅 1 款时并入最相近的子分类或上级，避免单条目子分类。
3. **互斥**：分类之间含义不重叠，同一核心功能不会散落到多个分类。
4. **平台作标签**：平台（`Windows` / `macOS` / `Linux` / `跨平台` / `Android` / `Web`）仅作反引号标签，不作为分类维度。
5. **不设「其他 / 杂项」**：无法明确归类者，归入最相近的功能域。
6. **边界判定**：
   - OCR、翻译、语音识别 / 转写 → `识别与翻译`
   - PDF / 电子书阅读与处理、文件格式转换 → `文档与阅读`
   - 视频 / 流媒体下载（含 m3u8、B 站下载）→ `下载`
   - 桌面壁纸、任务栏美化 → `桌面美化`；窗口管理、音量、亮度、输入法状态 → `窗口与桌面工具`
   - 跨平台软件按主要功能归类，用 `平台` 标签标注兼容系统

## 质量要求

- 仅收录**开源**或提供免费版本的软件
- 优先收录仍在维护、star 数较高的项目
- 不收录已归档（archived）、长期无更新或含明显广告 / 流氓行为的软件
- 不重复收录已有条目（提交前请先搜索）

## 仓库结构

```
awesome-software/
├── README.md             # 自动生成的无徽章索引
├── lists/                # 按功能分类的详细软件条目
├── scripts/build_readme.py  # 生成首页索引
├── CONTRIBUTING.md       # 本贡献指南
├── LICENSE               # 清单本身的许可（CC0）
├── RESOURCES.md          # 下载站、镜像站与资料合集
└── .gitignore
```

## 许可

本清单（`README.md`、`lists/*.md` 及整理成果）以 **CC0 1.0** 发布，可自由复制与再分发；所收录的各款软件仍归其原作者所有，请遵守各自的许可证。

感谢你的贡献！🎉
