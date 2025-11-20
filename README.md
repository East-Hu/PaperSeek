# 📚 PaperSeek

<div align="center">

![PaperSeek Banner](https://via.placeholder.com/800x200?text=PaperSeek+AI+Research+Assistant)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Stars](https://img.shields.io/github/stars/East-Hu/PaperSeek?style=social)](https://github.com/East-Hu/PaperSeek)

**全自动论文速递与智能分析助手 | AI-Powered Academic Paper Delivery & Analysis Assistant**

让学术研究更高效、更智能 | Making Research More Efficient & Intelligent

[English](#english) | [中文](#中文)

</div>

---

## 中文

### ✨ 核心特性

- 🔍 **多源智能搜索** - 支持 **ArXiv** (CS/物理/数学) 和 **Semantic Scholar** (全领域AI搜索)，一站式获取最新文献
- 🤖 **AI 深度摘要** - 使用 LLM (GPT-4o-mini等) 生成结构化的中英文核心创新点总结，自动提取 **AI 标签**
- 📥 **PDF 自动下载** - 一键批量下载论文 PDF，自动重命名并整理归档
- 📝 **引用一键导出** - 支持 **BibTeX, APA, MLA, IEEE** 等多种格式，方便直接插入论文
- ⭐ **收藏夹管理** - 本地收藏心仪论文，随时查看和管理阅读列表
- 🎨 **精美 CLI** - 极客风命令行界面，支持中英文切换，丰富的动画和交互体验
- ⚙️ **高度可配置** - 自定义机器人名称、关键词、时间范围、输出格式等

### 🚀 快速开始

#### 1. 克隆仓库

```bash
git clone https://github.com/East-Hu/PaperSeek.git
cd PaperSeek
```

#### 2. 创建虚拟环境并安装

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -e .
```

#### 3. 配置 API

首次启动时会引导您配置 LLM API：

```bash
paper-seek
```

您需要准备：
- **API Key**: LLM 服务提供商的 API 密钥
- **Base URL**: API 地址 (默认: OpenAI)
- **Model**: 模型名称 (推荐: gpt-4o-mini)

#### 4. 开始使用

```bash
# 启动交互式界面
paper-seek
```

### 📖 使用指南

#### 交互式模式（推荐）

启动后，您将看到功能菜单：

1. 🔍 **搜索论文** - 支持多关键词、日期范围筛选，可选择数据源 (ArXiv/Semantic Scholar)
2. ⚙️ **配置设置** - 管理 API、机器人名称、语言等
3. ⭐ **查看收藏夹** - 浏览和管理已保存的论文
4. 🧪 **测试 API** - 验证 API 连接
5. ❌ **退出程序**

#### 搜索流程体验

1. **输入关键词**：如 `LLM, RAG`
2. **选择数据源**：ArXiv 或 Semantic Scholar
3. **获取结果**：查看论文列表、作者、发布日期
4. **AI 摘要**：自动生成中文摘要和 AI 标签
5. **后续操作**：
   - 📥 **下载 PDF**
   - 📝 **导出引用** (BibTeX/APA/MLA/IEEE)
   - ⭐ **加入收藏**

### ⚙️ 配置文件

配置保存在 `~/.paper_robot/config.yaml`:

```yaml
robot_name: "PaperSeek"
api_key: "your-api-key"
base_url: "https://api.openai.com/v1"
model: "gpt-4o-mini"
max_results: 20
language: "zh"          # zh 或 en
output_dir: "papers"
```

### 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## English

### ✨ Features

- 🔍 **Multi-Source Search** - Support **ArXiv** (CS/Physics/Math) and **Semantic Scholar** (All-field AI Search)
- 🤖 **AI Summarization** - Generate structured summaries and **AI Tags** using LLM (GPT-4o-mini, etc.)
- 📥 **PDF Download** - One-click batch download of paper PDFs, automatically renamed and organized
- 📝 **Citation Export** - Export citations in **BibTeX, APA, MLA, IEEE** formats
- ⭐ **Favorites Manager** - Save papers to local favorites for easy access
- 🎨 **Beautiful CLI** - Geek-style command-line interface with rich animations and bilingual support
- ⚙️ **Highly Configurable** - Customize robot name, keywords, date range, output formats, etc.

### 🚀 Quick Start

#### 1. Clone the Repository

```bash
git clone https://github.com/East-Hu/PaperSeek.git
cd PaperSeek
```

#### 2. Install

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install
pip install -e .
```

#### 3. Configure API

Run the tool to configure your LLM API:

```bash
paper-seek
```

#### 4. Start Using

```bash
# Launch interactive interface
paper-seek
```

### 📖 Usage Guide

#### Interactive Mode

Launch the tool to access the main menu:

1. 🔍 **Search Papers** - Search with keywords, date range, and data sources
2. ⚙️ **Settings** - Manage API, robot name, language
3. ⭐ **View Favorites** - Browse saved papers
4. 🧪 **Test API** - Verify connection
5. ❌ **Exit**

#### Search Workflow

1. **Enter Keywords**: e.g., `LLM, RAG`
2. **Select Source**: ArXiv or Semantic Scholar
3. **View Results**: Browse paper list with metadata
4. **AI Summary**: Generate summaries and AI tags
5. **Actions**:
   - 📥 **Download PDF**
   - 📝 **Export Citations**
   - ⭐ **Add to Favorites**

### 📄 License

MIT License - see [LICENSE](LICENSE)

---

<div align="center">

**Made with ❤️ for researchers worldwide**

**⭐ Star this repo if it helps your research!**

</div>
