# 📚 Paper-to-Action

> 全自动论文速递机器人 - CLI 工具 + VSCode 插件

[![GitHub](https://img.shields.io/github/license/East-Hu/paper-to-action)](https://github.com/East-Hu/paper-to-action/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![VSCode](https://img.shields.io/badge/VSCode-Extension-blue.svg)](https://code.visualstudio.com/)

## 🌟 特性

- 🔍 **智能搜索** - 自动从 ArXiv 爬取最新论文
- 🤖 **AI 摘要** - 使用 LLM 生成中文核心创新点总结
- 💻 **交互式 CLI** - 精美的命令行界面
- 🎨 **VSCode 插件** - 无缝集成到编辑器
- 🚀 **Fork 即用** - 简单配置即可开始使用
- ⚙️ **高度可配置** - 自定义机器人名称、关键词、时间范围等

## 📦 安装

### 方法一：从源码安装（推荐）

```bash
# 克隆仓库
git clone https://github.com/East-Hu/paper-to-action.git
cd paper-to-action

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

# 安装依赖
pip install -e .
```

### 方法二：使用 pip 安装

```bash
pip install paper-to-action
```

## 🚀 快速开始

### 1. 配置 API

首次使用需要配置 LLM API：

```bash
# 方法一：使用交互式界面配置
paper-robot

# 方法二：使用命令行配置
paper-robot config set --key api_key --value YOUR_API_KEY
paper-robot config set --key base_url --value YOUR_BASE_URL
paper-robot config set --key model --value gpt-4o-mini
```

### 2. 自定义机器人名称

```bash
paper-robot rename "Mark's Auto Paper Robot"
```

### 3. 搜索论文

#### 交互式模式（推荐）

```bash
# 启动交互式界面
paper-robot

# 或使用简写
pr
```

#### 命令行模式

```bash
# 基础搜索
paper-robot search "AI Security"

# 指定时间范围
paper-robot search "RAG" --start-date 2025-01-01 --end-date 2025-01-19

# 指定结果数量
paper-robot search "Machine Learning" --max-results 50

# 不生成 AI 摘要
paper-robot search "NLP" --no-summarize

# 指定输出格式
paper-robot search "Computer Vision" --format markdown
```

## 🎨 VSCode 插件

### 安装插件

1. 在 VSCode 中按 `Ctrl+Shift+X` 打开扩展市场
2. 搜索 "Paper-to-Action"
3. 点击安装

或者从源码安装：

```bash
cd vscode-extension
npm install
npm run compile
# 按 F5 启动调试
```

### 使用插件

1. 点击侧边栏的 📚 图标
2. 首次使用会提示配置 API
3. 输入搜索关键词、日期范围
4. 点击"搜索论文"按钮
5. 查看 AI 生成的摘要

## 📖 使用示例

### CLI 工具演示

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║           📚     East's Paper Robot      📚           ║
║                                                           ║
║              自动化论文爬取与智能摘要工具                ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

请选择操作：

┌────────┬──────────────────────┐
│ 选项   │ 功能                 │
├────────┼──────────────────────┤
│ 1      │ 🔍 搜索论文          │
│ 2      │ ⚙️  配置设置         │
│ 3      │ 📂 查看已保存的论文  │
│ 4      │ 🧪 测试 API 连接     │
│ 5      │ ❌ 退出              │
└────────┴──────────────────────┘
```

### 输出示例

论文会保存为 Markdown 文件：

```markdown
# 论文速递 - 2025-01-19

**共找到 10 篇论文**

---

## 1. Advanced Techniques in AI Security

**作者：** John Doe, Jane Smith et al.
**发布日期：** 2025-01-15
**ArXiv ID：** 2501.12345
**PDF 链接：** [https://arxiv.org/pdf/2501.12345](https://arxiv.org/pdf/2501.12345)
**分类：** cs.AI, cs.CR

### 🤖 AI 核心创新点总结

本文提出了一种新的 AI 安全防护框架，主要创新点包括：
1. 基于对抗训练的鲁棒性增强方法
2. 实时威胁检测与响应机制
3. 在多个基准测试上达到 SOTA 性能

### 📄 原始摘要

We propose a novel framework for AI security...
```

## ⚙️ 配置选项

配置文件位置：`~/.paper_robot/config.yaml`

```yaml
robot_name: "Paper Robot"
api_key: "your-api-key"
base_url: "https://api.openai.com/v1"
model: "gpt-4o-mini"
max_results: 20
default_keywords: ""
language: "zh"
output_dir: "papers"
```

## 🔧 高级用法

### 批量处理

```bash
# 创建一个脚本自动化多个搜索
cat > search_papers.sh << 'EOF'
#!/bin/bash
paper-robot search "AI Security" --format markdown
paper-robot search "RAG" --format markdown
paper-robot search "LLM" --format markdown
EOF

chmod +x search_papers.sh
./search_papers.sh
```

### GitHub Actions 定时任务

创建 `.github/workflows/daily-papers.yml`：

```yaml
name: Daily Papers

on:
  schedule:
    - cron: '0 9 * * *'  # 每天 9:00 UTC
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
        run: |
          pip install paper-to-action
      
      - name: Configure API
        run: |
          paper-robot config set --key api_key --value ${{ secrets.API_KEY }}
          paper-robot config set --key base_url --value ${{ secrets.BASE_URL }}
      
      - name: Search papers
        run: |
          paper-robot search "AI Security" --format markdown
      
      - name: Commit results
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add papers/
          git commit -m "Daily paper update $(date +'%Y-%m-%d')" || exit 0
          git push
```

## 📚 API 文档

### Python API

```python
from paper_to_action import ArxivCrawler, LLMClient, PaperStorage

# 初始化
crawler = ArxivCrawler(max_results=20)
llm_client = LLMClient(api_key="your-key", base_url="your-url")
storage = PaperStorage(output_dir="papers")

# 搜索论文
papers = crawler.search_papers(
    keywords="AI Security",
    start_date="2025-01-01",
    end_date="2025-01-19"
)

# 生成摘要
papers = llm_client.batch_summarize(papers, language="zh")

# 保存结果
storage.save_papers_markdown(papers)
```

## 🤝 贡献

欢迎贡献！请随时提交 Issue 或 Pull Request。

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- [ArXiv API](https://arxiv.org/help/api) - 论文数据源
- [Rich](https://github.com/Textualize/rich) - 精美的终端输出
- [Typer](https://github.com/tiangolo/typer) - 现代 CLI 框架

## 📧 联系方式

- GitHub: [@East-Hu](https://github.com/East-Hu)
- 项目链接: [https://github.com/East-Hu/paper-to-action](https://github.com/East-Hu/paper-to-action)

---

⭐ 如果这个项目对您有帮助，请给个 Star！
