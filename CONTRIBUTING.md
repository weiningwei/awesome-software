# 贡献指南 / Contributing

感谢你为 awesome-software 推荐好用的开源软件！本指南说明条目的**标准格式**、**徽章约定**、**分类规则**与**提交流程**，新增条目请遵循此处规范。

## 条目格式标准

每款软件统一为「列表项 + 链接 + 简介 + 标签 + 徽章」的形式（参考 [awesome-selfhosted](https://github.com/awesome-selfhosted/awesome-selfhosted) 与 [sindresorhus/awesome](https://github.com/sindresorhus/awesome) 规范）：

```markdown
- [软件名](仓库或主页链接) - 一句话简介。`平台` `开源协议` ![GitHub Repo stars](https://img.shields.io/github/stars/owner/repo?style=flat)
```

### 字段说明

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| 软件名 | ✅ | 作为链接文本，使用官方名称 |
| 链接 | ✅ | 优先填 GitHub 仓库地址，便于显示 stars；官网也可 |
| 简介 | ✅ | 一句话客观描述功能，以句号（。）结尾，避免营销用语 |
| 平台 | 🔶 | 反引号标签：`Windows` / `macOS` / `Linux` / `跨平台` |
| 开源协议 | 🔶 | 使用 SPDX 标识，如 `MIT` / `GPL-3.0` / `AGPL-3.0` / `Unlicense` |
| stars 徽章 | 🔶 | 仅 GitHub 项目添加，直观体现热度（详见下方徽章约定） |

> 🔶 = 建议填写，但非强制；存量条目正在逐步统一为该格式。

### 格式细则

- 软件名与简介之间用 ` - `（空格 + 短横 + 空格）分隔，**不要用** `:` 或 `：`
- 平台、协议用反引号（`` ` ``）包裹，放在简介之后、徽章之前
- 简介客观准确，不写「最好用」「神器」「必备」等主观评价
- 同一分类下的条目保持风格一致（都带或都不带某类徽章）

### 正反例对比

✅ **正确**
```markdown
- [localsend](https://github.com/localsend/localsend) - 局域网内跨设备文件传输工具。`跨平台` `MIT` ![GitHub Repo stars](https://img.shields.io/github/stars/localsend/localsend?style=flat)
```

❌ **错误**（问题：用冒号分隔、缺平台/协议、营销用语、无徽章）
```markdown
- [localsend](https://github.com/localsend/localsend) : 超好用的局域网传文件神器
```

## 徽章约定

GitHub 托管的条目，统一使用 [shields.io](https://shields.io) 徽章，顺序为 **stars → 最新 release → release 日期**：

```markdown
![GitHub Repo stars](https://img.shields.io/github/stars/owner/repo?style=flat)
![GitHub Release](https://img.shields.io/github/v/release/owner/repo)
![GitHub Release Date](https://img.shields.io/github/release-date/owner/repo)
```

- `owner/repo` 需替换为真实路径，且必须与条目链接指向同一仓库
- 非 GitHub 项目（如官网、GitLab）不添加上述徽章
- 不要添加 CI / build 状态等无关徽章
- release 日期徽章采用 shields.io 默认显示样式（仅月份，或非当年时显示 月份+年份，如 `may 2023`），目前不支持 `YYYY-MM-DD` 数字格式

## 如何添加一款软件

1. 在 `README.md` 中找到最匹配的**分类 / 子分类**
2. 将新条目添加到该分类列表的**末尾**
3. 按上述标准格式填写（至少包含：名称、链接、简介）
4. 提交 Pull Request，标题形如 `Add 软件名` 或 `新增 软件名`
5. 如软件特别优秀，可在 `README.md` 顶部的 `## 精选推荐` 中补充（该区块暂未启用，启用后再补充）

## 分类标准

分类以**核心功能**为唯一维度，遵循以下规则：

1. **唯一归属**：每款软件按其核心功能归入且仅归入一个分类；具备多项功能时，按用户最常使用的功能判定。
2. **二级结构**：顶级（`##`）为功能域，子级（`###`）为具体功能。子分类一般不少于 3 款；功能独立、无法合并的子分类不少于 2 款；仅 1 款时并入最相近的子分类或上级，避免单条目子分类。
3. **互斥**：分类之间含义不重叠，同一核心功能不会散落到多个分类。
4. **平台作标签**：平台（`Windows` / `macOS` / `Linux` / `跨平台` / `Android`）仅作反引号标签，不作为分类维度。
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
├── README.md        # 软件清单主体（按分类组织）
├── CONTRIBUTING.md  # 本贡献指南
├── LICENSE          # 清单本身的许可（CC0）
└── .gitignore
```

## 许可

本清单（README.md 及整理成果）以 **CC0 1.0** 发布，可自由复制与再分发；所收录的各款软件仍归其原作者所有，请遵守各自的许可证。

感谢你的贡献！🎉
