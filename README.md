# 📚 PaperRobot

<div align="center">

![PaperRobot Banner](docs/images/banner.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Stars](https://img.shields.io/github/stars/East-Hu/PaperRobot?style=social)](https://github.com/East-Hu/PaperRobot)

**全自动论文速递机器人 | AI-Powered Academic Paper Delivery Bot**

让学术研究更高效 | Making Research More Efficient

[English](#english) | [中文](#中文)

</div>

---

## 中文

### ✨ 特性

- 🔍 **智能搜索** - 自动从 ArXiv 爬取最新论文，支持关键词、时间范围、分类筛选
- 🤖 **AI 摘要** - 使用 LLM (GPT-4o-mini等) 生成中英文核心创新点总结  
- 🎨 **精美 CLI** - 炫酷的命令行界面，支持中英文切换，丰富的动画和渐变色彩
- 💾 **多种格式** - 支持 Markdown 和 JSON 格式保存
- 🌍 **多语言** - 完整的中英文界面支持
- ⚙️ **高度可配置** - 自定义机器人名称、关键词、时间范围、输出格式等
- 🚀 **简单部署** - 克隆即用，5分钟上手

### 📸 界面预览

#### 语言选择
![Language Selection](docs/images/language-selection.png)

#### 主菜单
![Main Interface](docs/images/main-interface.png)

### 🚀 快速开始

#### 1. 克隆仓库

```bash
git clone https://github.com/East-Hu/PaperRobot.git
cd PaperRobot
```

#### 2. 创建虚拟环境并安装

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装
pip install -e .
```

#### 3. 配置 API

首次启动时会引导您配置 LLM API：

```bash
paper-robot
```

您需要准备：
- **API Key**: LLM 服务提供商的 API 密钥
- **Base URL**: API 地址 (默认: OpenAI)
- **Model**: 模型名称 (推荐: gpt-4o-mini)

**支持的 LLM 提供商**:
- OpenAI (GPT-4, GPT-4o-mini)
- Azure OpenAI
- 任何兼容 OpenAI API 的服务

#### 4. 开始使用

```bash
# 启动交互式界面
paper-robot

# 或使用简写
pr
```

### 📖 使用方法

#### 交互式模式（推荐）

启动后选择操作：
1. 🔍 **搜索论文** - 输入关键词搜索最新论文
2. ⚙️ **配置设置** - 管理 API、机器人名称、语言等
3. 📂 **查看历史** - 浏览已保存的论文
4. 🧪 **测试 API** - 验证 API 连接
5. ❌ **退出程序**

#### 命令行模式

```bash
# 基础搜索
paper-robot search "AI Security"

# 指定时间范围
paper-robot search "RAG" --start-date 2025-01-01 --end-date 2025-01-19

# 指定结果数量和格式
paper-robot search "Machine Learning" --max-results 50 --format markdown

# 不生成 AI 摘要
paper-robot search "NLP" --no-summarize

# 查看配置
paper-robot config show

# 自定义机器人名称
paper-robot rename "我的论文助手"

# 测试 API 连接
paper-robot test
```

### 💡 输出示例

论文保存为精美的 Markdown 文件：

```markdown
# 论文速递 - 2025-01-19

**共找到 10 篇论文**

## 1. Advanced Techniques in AI Security

**作者：** John Doe, Jane Smith et al.
**发布日期：** 2025-01-15
**ArXiv ID：** 2501.12345
**PDF 链接：** [下载](https://arxiv.org/pdf/2501.12345)

### 🤖 AI 核心创新点总结

本文提出了一种新的 AI 安全防护框架，主要创新点包括：
1. 基于对抗训练的鲁棒性增强方法
2. 实时威胁检测与响应机制
3. 在多个基准测试上达到 SOTA 性能
```

### ⚙️ 配置文件

配置保存在 `~/.paper_robot/config.yaml`:

```yaml
robot_name: "Paper Robot"
api_key: "your-api-key"
base_url: "https://api.openai.com/v1"
model: "gpt-4o-mini"
max_results: 20
language: "zh"          # zh 或 en
output_dir: "papers"
```

### 🔧 GitHub Actions 自动化

可以配置每日自动推送论文（参见 `.github/workflows/daily-papers.yml`）。

### 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md)

### 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

### 🙏 致谢

- [ArXiv](https://arxiv.org/) - 学术论文预印本平台
- [Rich](https://github.com/Textualize/rich) - 精美的终端输出库
- [Typer](https://github.com/tiangolo/typer) - 现代 CLI 框架

---

## English

### ✨ Features

- 🔍 **Smart Search** - Auto-crawl latest papers from ArXiv with keyword, date range, and category filtering
- 🤖 **AI Summarization** - Generate summaries in Chinese/English using LLM (GPT-4o-mini, etc.)
- 🎨 **Beautiful CLI** - Stunning command-line interface with Chinese/English support and rich animations
- 💾 **Multiple Formats** - Save as Markdown or JSON
- 🌍 **Multi-language** - Complete Chinese and English interface support
- ⚙️ **Highly Configurable** - Customize robot name, keywords, date range, output format, etc.
- 🚀 **Easy Setup** - Clone and use, ready in 5 minutes

### 🚀 Quick Start

#### 1. Clone the Repository

```bash
git clone https://github.com/East-Hu/PaperRobot.git
cd PaperRobot
```

#### 2. Create Virtual Environment and Install

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install
pip install -e .
```

#### 3. Configure API

On first launch, you'll be guided to configure your LLM API:

```bash
paper-robot
```

You'll need:
- **API Key**: Your LLM provider's API key
- **Base URL**: API endpoint (default: OpenAI)
- **Model**: Model name (recommended: gpt-4o-mini)

**Supported LLM Providers**:
- OpenAI (GPT-4, GPT-4o-mini)
- Azure OpenAI
- Any OpenAI-compatible API service

#### 4. Start Using

```bash
# Launch interactive interface
paper-robot

# Or use short alias
pr
```

### 📖 Usage

#### Interactive Mode (Recommended)

After launching, select an option:
1. 🔍 **Search Papers** - Enter keywords to search latest papers
2. ⚙️ **Settings** - Manage API, robot name, language, etc.
3. 📂 **View History** - Browse saved papers
4. 🧪 **Test API** - Verify API connection
5. ❌ **Exit**

#### Command Line Mode

```bash
# Basic search
paper-robot search "AI Security"

# Specify date range
paper-robot search "RAG" --start-date 2025-01-01 --end-date 2025-01-19

# Specify max results and format
paper-robot search "Machine Learning" --max-results 50 --format markdown

# Skip AI summarization
paper-robot search "NLP" --no-summarize

# View configuration
paper-robot config show

# Customize robot name
paper-robot rename "My Research Assistant"

# Test API connection
paper-robot test
```

### ⚙️ Configuration

Configuration is saved in `~/.paper_robot/config.yaml`:

```yaml
robot_name: "Paper Robot"
api_key: "your-api-key"
base_url: "https://api.openai.com/v1"
model: "gpt-4o-mini"
max_results: 20
language: "en"          # zh or en
output_dir: "papers"
```

### 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

### 📄 License

MIT License - see [LICENSE](LICENSE)

---

<div align="center">

**Made with ❤️ for researchers worldwide**

**⭐ Star this repo if it helps your research!**

</div>
