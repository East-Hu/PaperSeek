# Paper-to-Action

<div align="center">

![Paper-to-Action Banner](docs/images/banner.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Stars](https://img.shields.io/github/stars/East-Hu/paper-to-action?style=social)](https://github.com/East-Hu/paper-to-action)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/East-Hu/paper-to-action/pulls)

**Automated Academic Paper Delivery Robot | Making Research More Efficient**

English | [简体中文](README.md)

</div>

---

## ✨ Key Features

- 🔍 **Smart Search** - Automatically crawl latest papers from ArXiv with keyword and date range filtering
- 🤖 **AI Summarization** - Generate core innovation summaries in Chinese/English using LLM (GPT-4o-mini, etc.)
- 🎨 **Beautiful CLI** - Stunning command-line interface with Chinese/English support and rich animations
- 💻 **VSCode Extension** - Seamlessly integrated into your editor - code and read papers side by side
- 🚀 **One-Click Deploy** - Fork and use, simple configuration to get started
- ⚙️ **Highly Configurable** - Customize robot name, keywords, date range, output format, and more
- 🌍 **Multi-language Support** - Complete Chinese and English interface support

## 📸 Interface Preview

<div align="center">

### Language Selection
![Language Selection](docs/images/language-selection.png)

### Main Interface
![Main Interface](docs/images/main-interface.png)

### Paper Search
![Search Results](docs/images/search-results.png)

</div>

## 🚀 Quick Start

### 1. Installation

#### Method 1: Install from Source (Recommended)

```bash
# Clone the repository
git clone https://github.com/East-Hu/paper-to-action.git
cd paper-to-action

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

# Install dependencies
pip install -e .
```

#### Method 2: Install via pip (Coming Soon)

```bash
pip install paper-to-action
```

### 2. Configure API

On first launch, you'll be guided to configure your LLM API. You'll need:

- **API Key**: Your LLM service provider API key
- **Base URL**: API base URL (defaults to OpenAI)
- **Model**: Model name to use (recommended: gpt-4o-mini)

#### Supported LLM Providers

- OpenAI (GPT-4, GPT-4o-mini, etc.)
- Azure OpenAI
- Any OpenAI-compatible API service (e.g., vveai.com, deepseek, etc.)

### 3. Launch and Use

```bash
# Start interactive interface
paper-robot

# Or use short alias
pr
```

#### First Run Workflow

1. **Select Language** - Chinese or English
2. **Configure API** - Enter your API credentials
3. **Start Searching** - Enter keywords to automatically crawl papers
4. **AI Summarization** - Optionally generate AI summaries
5. **Save Results** - Automatically save as Markdown or JSON

## 📖 Usage Guide

### Interactive Mode (Recommended)

```bash
paper-robot
```

After launching, you'll see a beautiful welcome interface with these features:

1. 🔍 **Search Papers** - Enter keywords to search for latest papers
2. ⚙️ **Settings** - Manage API, robot name, language, etc.
3. 📂 **View History** - Browse saved papers
4. 🧪 **Test API** - Verify API connection is working
5. ❌ **Exit**

### Command Line Mode

Perfect for scripting and automation:

```bash
# Basic search
paper-robot search "AI Security"

# Specify date range
paper-robot search "RAG" --start-date 2025-01-01 --end-date 2025-01-19

# Specify maximum results
paper-robot search "Machine Learning" --max-results 50

# Skip AI summarization
paper-robot search "NLP" --no-summarize

# Specify output format
paper-robot search "Computer Vision" --format markdown

# View configuration
paper-robot config show

# Set robot name
paper-robot rename "Mark's Auto Paper Robot"

# Test API connection
paper-robot test
```

### Customize Robot Name

Make your paper robot more personal:

```bash
paper-robot rename "Mark's Research Assistant"
```

The welcome screen will then display your custom name!

## 💡 Output Example

Papers are saved as beautiful Markdown files:

```markdown
# Paper Digest - 2025-01-19

**Found 10 papers**

---

## 1. Advanced Techniques in AI Security

**Authors:** John Doe, Jane Smith et al.
**Published:** 2025-01-15
**ArXiv ID:** 2501.12345
**PDF Link:** [https://arxiv.org/pdf/2501.12345](https://arxiv.org/pdf/2501.12345)
**Categories:** cs.AI, cs.CR

### 🤖 AI Summary of Core Innovations

This paper proposes a novel AI security framework with the following key innovations:
1. Robustness enhancement method based on adversarial training
2. Real-time threat detection and response mechanism
3. Achieves SOTA performance on multiple benchmarks

### 📄 Original Abstract

We propose a novel framework for AI security...
```

## 🎨 VSCode Extension

### Install Extension

**Method 1: From Marketplace (Coming Soon)**
1. Press `Ctrl+Shift+X` in VSCode to open Extensions marketplace
2. Search for "Paper-to-Action"
3. Click Install

**Method 2: From Source**

```bash
cd vscode-extension
npm install
npm run compile
# Press F5 to start debugging
```

### Using the Extension

1. Click the 📚 icon in the sidebar
2. First-time users will be prompted to configure API
3. Enter search keywords and date range
4. Click "Search Papers" button
5. View AI-generated summaries

## 🔧 Advanced Usage

### GitHub Actions Automation

Implement daily automatic paper delivery to your repository!

Create `.github/workflows/daily-papers.yml`:

```yaml
name: Daily Papers

on:
  schedule:
    - cron: '0 9 * * *'  # Daily at 9:00 UTC
  workflow_dispatch:

jobs:
  fetch-papers:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install paper-to-action
      
      - name: Configure API
        run: |
          paper-robot config set --key api_key --value ${{ secrets.API_KEY }}
          paper-robot config set --key base_url --value ${{ secrets.BASE_URL }}
      
      - name: Search papers
        run: paper-robot search "AI Security" --format markdown
      
      - name: Commit results
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add papers/
          git commit -m "Daily paper update $(date +'%Y-%m-%d')" || exit 0
          git push
```

**Setup Steps:**
1. Add Secrets in GitHub repository settings
   - `API_KEY`: Your LLM API key
   - `BASE_URL`: Your API base URL
2. Commit the workflow file to your repository
3. Runs automatically daily, papers pushed to `papers/` directory

### Python API

Use directly in your code:

```python
from paper_to_action import ArxivCrawler, LLMClient, PaperStorage

# Initialize
crawler = ArxivCrawler(max_results=20)
llm_client = LLMClient(api_key="your-key", base_url="your-url")
storage = PaperStorage(output_dir="papers")

# Search papers
papers = crawler.search_papers(
    keywords="AI Security",
    start_date="2025-01-01",
    end_date="2025-01-19"
)

# Generate summaries
papers = llm_client.batch_summarize(papers, language="en")

# Save results
storage.save_papers_markdown(papers)
```

## ⚙️ Configuration File

Configuration file location: `~/.paper_robot/config.yaml`

```yaml
robot_name: "Paper Robot"     # Robot name
api_key: "your-api-key"       # API key
base_url: "https://api.openai.com/v1"  # API base URL
model: "gpt-4o-mini"          # Model to use
max_results: 20               # Default maximum results
language: "en"                # Interface language (zh/en)
output_dir: "papers"          # Output directory
```

## 🤝 Contributing

Contributions are welcome! Please see [Contributing Guidelines](CONTRIBUTING.md)

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- [ArXiv](https://arxiv.org/) - Excellent academic paper preprint platform
- [Rich](https://github.com/Textualize/rich) - Beautiful terminal output library
- [Typer](https://github.com/tiangolo/typer) - Modern CLI framework

## 📧 Contact

- GitHub: [@East-Hu](https://github.com/East-Hu)
- Project Link: [https://github.com/East-Hu/paper-to-action](https://github.com/East-Hu/paper-to-action)

## ⭐ Star History

If this project helps you, please give it a Star!

---

<div align="center">

**Made with ❤️ for researchers worldwide**

</div>
