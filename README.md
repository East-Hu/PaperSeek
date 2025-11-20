# 📚 PaperSeek

<div align="center">

```
██████╗    █████╗   ██████╗   ███████╗  ██████╗   ███████╗  ███████╗  ███████╗  ██╗  ██╗
██╔══██╗  ██╔══██╗  ██╔══██╗  ██╔════╝  ██╔══██╗  ██╔════╝  ██╔════╝  ██╔════╝  ██║ ██╔╝
██████╔╝  ███████║  ██████╔╝  █████╗    ██████╔╝  ███████╗  █████╗    █████╗    █████╔╝ 
██╔═══╝   ██╔══██║  ██╔═══╝   ██╔══╝    ██╔══██╗  ╚════██║  ██╔══╝    ██╔══╝    ██╔═██╗ 
██║       ██║  ██║  ██║       ███████╗  ██║  ██║  ███████║  ███████╗  ███████╗  ██║  ██╗
╚═╝       ╚═╝  ╚═╝  ╚═╝       ╚══════╝  ╚═╝  ╚═╝  ╚══════╝  ╚══════╝  ╚══════╝  ╚═╝  ╚═╝
```

### 🚀 全自动论文速递与智能分析助手
**AI-Powered Academic Paper Delivery & Analysis Assistant**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

[中文](#中文) | [English](#english)

</div>

---

## 中文

**PaperSeek** 是一款专为科研人员打造的命令行工具，旨在通过 AI 技术革新文献获取与阅读体验。它不仅能从多个权威数据源聚合最新论文，还能利用大语言模型（LLM）自动生成深度摘要、提取核心创新点，并提供一键下载、引用管理等全流程支持。

### ✨ 核心特性

| 功能模块 | 详细说明 |
| :--- | :--- |
| **🔍 多源智能搜索** | 支持 **ArXiv** (CS/物理/数学) 和 **Semantic Scholar** (全领域 AI 搜索)，打破信息茧房，一站式获取最新文献。 |
| **🤖 AI 深度摘要** | 内置 LLM 引擎 (支持 GPT-4o, Claude 等)，自动生成结构化的**中文摘要**，提取**核心创新点**，并生成**AI 标签**。 |
| **📥 自动化工作流** | **批量下载 PDF** 并自动重命名；一键导出 **BibTeX, APA, MLA, IEEE** 引用格式，直接插入论文。 |
| **⭐ 知识管理** | 本地**收藏夹**功能，构建个人专属的文献库；支持 Markdown/JSON 格式导出阅读报告。 |
| **🎨 极客体验** | 精心设计的 CLI 界面，支持**中英双语**切换，拥有流畅的动画效果和直观的交互流程。 |

### 🚀 快速开始

#### 1. 环境准备

确保您的系统已安装 Python 3.8 或更高版本。

#### 2. 安装 PaperSeek

```bash
# 克隆仓库
git clone https://github.com/East-Hu/PaperSeek.git
cd PaperSeek

# 创建并激活虚拟环境 (推荐)
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# 安装依赖
pip install -e .
```

#### 3. 初始化配置

首次运行会自动引导配置：

```bash
paper-seek
```

您需要配置以下信息（保存在 `~/.paper_robot/config.yaml`）：
- **API Key**: 您的 LLM 服务商 API 密钥（如 OpenAI, Azure, DeepSeek 等）
- **Base URL**: API 接口地址 (默认: `https://api.openai.com/v1`)
- **Model**: 模型名称 (推荐: `gpt-4o-mini` 或 `gpt-3.5-turbo`)

### 📖 使用指南

#### 交互式模式 (Interactive Mode)

直接输入 `paper-seek` 进入主菜单：

```text
╭──────────┬─────────────────────╮
│   选项   │ 功能                │
├──────────┼─────────────────────┤
│    1     │ 🔍 搜索论文         │
│    2     │ ⚙️  配置设置         │
│    3     │ ⭐ 查看收藏夹       │
│    4     │ 🧪 测试 API 连接    │
│    5     │ ❌ 退出             │
╰──────────┴─────────────────────╯
```

#### 典型工作流

1.  **搜索**: 输入关键词（如 `Large Language Models, RAG`），选择时间范围。
2.  **筛选**: 选择数据源（ArXiv 或 Semantic Scholar）。
3.  **阅读**: 浏览 AI 生成的中文摘要和标签。
4.  **获取**: 满意后，一键下载 PDF 并导出引用。
5.  **收藏**: 将高质量论文加入本地收藏夹。

### ⚙️ 高级配置

配置文件位于 `~/.paper_robot/config.yaml`，您可以手动修改：

```yaml
robot_name: "PaperSeek"       # 机器人名称
language: "zh"                # 界面语言: zh/en
output_dir: "papers"          # 输出目录
max_results: 20               # 默认最大搜索结果
api_key: "sk-..."             # LLM API Key
base_url: "..."               # LLM Base URL
model: "gpt-4o-mini"          # LLM Model
```

### 🤝 参与贡献

我们非常欢迎社区贡献！如果您有新的想法或发现了 Bug：

1.  Fork 本仓库
2.  创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3.  提交更改 (`git commit -m 'Add some AmazingFeature'`)
4.  推送到分支 (`git push origin feature/AmazingFeature`)
5.  提交 Pull Request

### 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。

---

## English

**PaperSeek** is a command-line tool designed for researchers to revolutionize the literature acquisition and reading experience through AI technology. It aggregates the latest papers from multiple authoritative sources, uses Large Language Models (LLMs) to automatically generate in-depth summaries, extracts core innovations, and provides full-process support such as one-click download and citation management.

### ✨ Key Features

| Feature | Description |
| :--- | :--- |
| **🔍 Multi-Source Search** | Support **ArXiv** (CS/Physics/Math) and **Semantic Scholar** (All-field AI Search) for one-stop literature access. |
| **🤖 AI Summarization** | Built-in LLM engine generates structured **summaries**, extracts **core innovations**, and generates **AI Tags**. |
| **📥 Automated Workflow** | **Batch download PDFs** with auto-renaming; one-click export of **BibTeX, APA, MLA, IEEE** citations. |
| **⭐ Knowledge Management** | Local **Favorites** to build your personal library; export reading reports in Markdown/JSON. |
| **🎨 Geek Experience** | Beautiful CLI interface with **Bilingual Support** (English/Chinese), smooth animations, and intuitive interaction. |

### 🚀 Quick Start

#### 1. Prerequisites

Ensure you have Python 3.8+ installed.

#### 2. Installation

```bash
# Clone repository
git clone https://github.com/East-Hu/PaperSeek.git
cd PaperSeek

# Create & activate virtual environment (Recommended)
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install
pip install -e .
```

#### 3. Configuration

Run the tool to initialize configuration:

```bash
paper-seek
```

You will need:
- **API Key**: Your LLM provider's API key
- **Base URL**: API endpoint (Default: `https://api.openai.com/v1`)
- **Model**: Model name (Recommended: `gpt-4o-mini`)

### 📖 Usage Guide

#### Interactive Mode

Run `paper-seek` to enter the main menu:

1.  **Search Papers**: Search with keywords, date range, and sources.
2.  **Settings**: Manage API, robot name, language.
3.  **View Favorites**: Browse and manage saved papers.
4.  **Test API**: Verify connection.

#### Typical Workflow

1.  **Search**: Enter keywords (e.g., `LLM, RAG`) and date range.
2.  **Filter**: Select data source (ArXiv or Semantic Scholar).
3.  **Read**: Review AI-generated summaries and tags.
4.  **Acquire**: Download PDFs and export citations.
5.  **Save**: Add high-quality papers to favorites.

### 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

---

<div align="center">

**Made with ❤️ for researchers worldwide**

**⭐ Star this repo if it helps your research!**

</div>
