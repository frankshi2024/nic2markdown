# nic2markdown

> Convert MkDocs Material documentation pages to clean, GitHub-compatible Markdown — for both humans and coding agents.

---

## 起源

本项目起源于：开发者在**使用 coding agent 理解、完成和 debug 课程实验作业**时，发现在 fetch 实验文档时，无论使用直接下载 HTML、借助 MCP 截图保存还是内置的其他工具，都存在形式冗余、消耗 token 较多乃至识别错误的问题。

调查发现，**中科大大部分计算机实验课程文档由 MkDocs Material 开发**。这也意味着，本就由 Markdown 生成的网页，最好的处理方法也是将其回归为 Markdown — 本项目应运而生。

希望本校和其他友校的同学在 **Issues** 中提供该工具的问题，以及其他实验课程使用的其他框架的反馈。

> ⚠️ 本工具不作为爬虫相关工具使用，仅提供有限数据清洗功能，不承担有关法律责任。

---

## 安装

**前置要求：[uv](https://docs.astral.sh/uv/)**

### 方式一：从 GitHub（推荐）

**Linux / macOS / Git Bash / WSL**

```bash
curl -fsSL https://raw.githubusercontent.com/frankshi2024/nic2markdown/main/install.sh | bash
```

**Windows PowerShell**

```powershell
iwr -useb https://raw.githubusercontent.com/frankshi2024/nic2markdown/main/install.ps1 | iex
```

### 方式二：从 Gitee 镜像（国内网络友好）

**Linux / macOS / Git Bash / WSL**

```bash
curl -fsSL https://gitee.com/frankshi2024/nic2markdown/raw/main/install-gitee.sh | bash
```

**Windows PowerShell**

```powershell
iwr -useb https://gitee.com/frankshi2024/nic2markdown/raw/main/install-gitee.ps1 | iex
```

### 手动安装（开发者）

```bash
git clone https://github.com/frankshi2024/nic2markdown.git
# 或国内镜像：git clone https://gitee.com/frankshi2024/nic2markdown.git
cd nic2markdown
uv sync
uv run nic2markdown --help
```

---

## 使用

```bash
# 基本转换 → output/<stem>.<yyyymmddhhmmss>.md
nic2markdown https://soc.ustc.edu.cn/COD/lab5/

# 同时提取侧边栏导航链接
nic2markdown https://soc.ustc.edu.cn/COD/lab5/ -s

# 指定输出目录
nic2markdown https://soc.ustc.edu.cn/Digital/2025/lab1/intro/ -o ./notes -s

# 非 MkDocs Material 页面 → 报错退出
nic2markdown https://example.com
# Error: Unsupported framework.
```

---

## 功能特性

| 原始结构 | 转换结果 |
|---------|---------|
| `<div class="admonition note">` | `> [!NOTE]` (GFM Alert) |
| `<div class="admonition warning">` | `> [!WARNING]` |
| `<div class="admonition danger">` | `> [!CAUTION]` |
| `<div class="admonition tip/success">` | `> [!TIP]` |
| `<div class="admonition question">` | `> [!IMPORTANT]` |
| `<div class="highlight"><pre><code>` | ` ``` ` fenced code blocks |
| 相对链接 | 补全为绝对 URL |
| 侧边栏导航 (`-s`) | 嵌套 Markdown 列表 |
| Task list | `- [ ]` / `- [x]` |
| MathJax | `$` / `$$` 公式 |
| Tabbed set | 带标签的多代码块 |

## 支持的框架

| 框架 | 状态 |
|------|------|
| **MkDocs Material** | ✅ 完整支持 |
| 更多框架 | 🚧 计划中（欢迎提 Issue） |

## 架构

```
URL 输入 → gateway（框架检测） → framework converter → GFM Markdown
                                    ├── extractor（正文提取）
                                    ├── converter（HTML→MD）
                                    └── sidebar（侧边栏链接）
```

新增框架只需：
1. 在 `frameworks/` 下新建子包
2. 实现 `BaseConverter` 的 4 个方法
3. 在 `gateway.py` 注册

## 开发

```bash
git clone https://github.com/frankshi2024/nic2markdown.git
cd nic2markdown
uv sync
uv run pytest -v    # 46 个测试
```

---

## 特别鸣谢

**DeepSeek-V4-Pro** 承担了本项目绝大部分代码编写工作。开发者和他度过了一段很好的 vibe coding 开发时光 🤖✨
