# PaperSeek 完整版开发计划

## 📋 项目信息

- **项目名称**: PaperSeek (原 PaperSeek)
- **版本**: 2.0.0 (Max Version)
- **目录**: `/Users/east/AntiGravity_projects/PaperSeek_max`
- **虚拟环境**: `/Users/east/AntiGravity_projects/PaperSeek` (保持不变)

---

## 🐛 立即修复

### 1. 进度条 Bug ✅ 优先
**问题**: 在`batch_summarize`时进度条不更新  
**位置**: `llm_client.py` line 91-116  
**解决方案**: 添加回调函数参数来更新进度

### 2. 全局重命名 ✅ 优先
**PaperSeek** → **PaperSeek**  
需要更新的文件：
- README.md
- CHANGELOG.md  
- CONTRIBUTING.md
- setup.py
- cli/interface.py (banner, app_name等)
- i18n.py (所有翻译字符串)
- 其他所有MD文档

---

## 🚀 新功能开发

### Phase 1: 多数据源支持 (Multi-source Support)

#### 1.1 新增数据源
- [ ] **Google Scholar** - 谷歌学术
- [ ] **PubMed** - 生物医学
- [ ] **IEEE Xplore** - 电气工程
- [ ] **ACM Digital Library** - 计算机科学
- [ ] **Semantic Scholar** - AI驱动的学术搜索

#### 1.2 统一数据接口
创建 `sources/` 目录：
```python
sources/
├── __init__.py
├── base.py           # 抽象基类
├── arxiv.py          # ArXiv 源
├──google_scholar.py  # Google Scholar
├── pubmed.py         # PubMed
├── ieee.py           # IEEE
└── semantic.py       # Semantic Scholar
```

---

### Phase 2: 论文管理功能 (Paper Management)

#### 2.1 数据库增强
扩展 `database.py`：
- [ ] **收藏功能** - Favorites table
- [ ] **标签系统** - Tags table (多对多关系)
- [ ] **笔记功能** - Notes table
- [ ] **阅读状态** - Reading status (未读/阅读中/已读)
- [ ] **评分系统** - 5星评分

数据库结构：
```sql
-- Papers table (已存在，增强)
papers (id, title, authors, summary, arxiv_id, published, source, ...)

-- Favorites (新增)
favorites (id, paper_id, created_at)

-- Tags (新增)
tags (id, name, color)
paper_tags (paper_id, tag_id)

-- Notes (新增)
notes (id, paper_id, content, created_at, updated_at)

-- Reading Status (新增)
reading_status (paper_id, status, progress, last_read)
```

#### 2.2 CLI 命令扩展
新增命令：
- `paper-seek favorite <paper_id>` - 收藏论文
- `paper-seek tag <paper_id> <tag>` - 添加标签
- `paper-seek note <paper_id>` - 添加/编辑笔记
- `paper-seek list favorites` - 列出收藏
- `paper-seek filter --tag <tag>` - 按标签筛选

---

### Phase 3: 引用管理器导出 (Citation Export)

#### 3.1 支持的格式
创建 `export/` 目录：
```python
export/
├── __init__.py
├── base.py           # 抽象导出类
├── zotero.py         # Zotero 格式
├── mendeley.py       # Mendeley 格式
├── endnote.py        # EndNote 格式
└── bibtex.py         # BibTeX 格式
```

#### 3.2 导出功能
- [ ] **Zotero** - RDF 格式
- [ ] **Mendeley** - RIS 格式
- [ ] **EndNote** - XML 格式
- [ ] **BibTeX** - .bib 文件
- [ ] **直接同步** - Zotero/Mendeley API 集成

#### 3.3 引用格式生成
- [ ] APA
- [ ] MLA
- [ ] Chicago
- [ ] IEEE
- [ ] Nature
- [ ] Science

---

### Phase 4: 高级搜索功能

#### 4.1 搜索增强
- [ ] **布尔搜索** - AND, OR, NOT
- [ ] **字段搜索** - title:xxx, author:xxx
- [ ] **引用次数过滤**
- [ ] **期刊/会议过滤**
- [ ] **影响因子过滤**

#### 4.2 智能推荐
- [ ] **相似论文推荐** - 基于向量相似度
- [ ] **引用关系图** - 可视化引用网络
- [ ] **热门趋势分析**

---

### Phase 5: 增强的 AI 功能

#### 5.1 更多 AI 能力
- [ ] **多语言摘要** - 支持更多语言
- [ ] **关键词提取**
- [ ] **研究方向分类**
- [ ] **论文批判性分析**
- [ ] **研究差距识别**

#### 5.2 批量处理优化
- [ ] **异步并发** - 加速摘要生成
- [ ] **缓存机制** - 避免重复调用
- [ ] **失败重试** - 自动重试失败的请求

---

### Phase 6: 用户体验提升

#### 6.1 CLI 增强
- [ ] **交互式搜索** - 实时预览搜索结果
- [ ] **论文预览** - 快速查看论文详情
- [ ] **PDF 下载** - 自动下载 PDF
- [ ] **阅读模式** - 终端内阅读论文

#### 6.2 导出格式
- [ ] **PDF 报告** - 生成精美的PDF
- [ ] **HTML 网页** - 可分享的网页版
- [ ] **Notion** - 导出到 Notion
- [ ] **Obsidian** - Markdown + 链接

---

## 📦 技术栈升级

### 新增依赖
```
beautifulsoup4      # 网页解析
scholarly           # Google Scholar API
biopython          # PubMed 访问
aiohttp            # 异步HTTP
sqlalchemy         # ORM (如果需要)
plotly             # 可视化
fpdf2              # PDF生成
```

---

## 🗂️ 文件结构 (完整版)

```
PaperSeek_max/
├── paper_to_action/
│   ├── __init__.py
│   ├── cli/
│   │   ├── commands.py      # 新命令
│   │   └── interface.py     # 增强的UI
│   ├── sources/             # 📌 新增：多数据源
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── arxiv.py
│   │   ├── google_scholar.py
│   │   ├── pubmed.py
│   │   └── semantic.py
│   ├── export/              # 📌 新增：导出功能
│   │   ├── __init__.py
│   │   ├── citation.py
│   │   ├── zotero.py
│   │   └── bibtex.py
│   ├── database.py          # ✏️ 增强：新表和功能
│   ├── llm_client.py        # ✏️ 修复：进度条回调
│   ├── config.py
│   ├── storage.py
│   └── i18n.py             # ✏️ 更新：PaperSeek
├── tests/                   # 测试
├── docs/                    # 文档
├── README.md               # ✏️ 更新
├── CHANGELOG.md            # ✏️ 更新
└── setup.py                # ✏️ 更新

```

---

## 📅 开发时间线

### 立即完成 (今天)
1. ✅ 修复进度条  bug
2. ✅ 全局重命名 PaperSeek → PaperSeek
3. ✅ 更新所有文档

### Phase 1 (核心功能)
- 多数据源支持
- 基础论文管理
- 引用导出

### Phase 2 (增强功能)  
- 高级搜索
- 智能推荐
- AI 增强

### Phase 3 (用户体验)
- PDF 下载
- 可视化
- 更多导出格式

---

## ✅ 当前任务优先级

**P0 (立即)**:
1. 修复进度条 bug
2. 重命名为 PaperSeek
3. ArXiv 范围说明

**P1 (核心)**:
1. 多数据源框架
2. 论文管理数据库
3. BibTeX 导出

**P2 (增强)**:
1. Zotero/Mendeley 导出
2. Google Scholar 集成
3. 标签和笔记

---

开始吗？ 🚀
