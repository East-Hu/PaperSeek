"""
ArXiv 论文爬虫模块
"""
import arxiv
from datetime import datetime
from typing import List, Dict, Optional
from rich.console import Console

console = Console()


class ArxivCrawler:
    """ArXiv 论文爬虫类"""
    
    def __init__(self, max_results: int = 50):
        """
        初始化爬虫
        
        Args:
            max_results: 最大返回结果数
        """
        self.max_results = max_results
    
    def search_papers(
        self,
        keywords: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[Dict]:
        """
        搜索论文
        
        Args:
            keywords: 搜索关键词
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            category: ArXiv 分类 (如 cs.AI, cs.CL)
            
        Returns:
            论文列表，每个论文包含 title, authors, summary, pdf_url, published 等字段
        """
        console.print(f"[cyan]🔍 正在搜索关键词：{keywords}[/cyan]")
        
        # 构建搜索查询
        query_parts = []
        
        # 添加关键词
        if keywords:
            # 支持多关键词搜索，使用 OR
            keywords_list = [kw.strip() for kw in keywords.split(',')]
            if len(keywords_list) > 1:
                keyword_query = " OR ".join([f'all:"{kw}"' for kw in keywords_list])
                query_parts.append(f"({keyword_query})")
            else:
                query_parts.append(f'all:"{keywords}"')
        
        # 添加分类
        if category:
            query_parts.append(f'cat:{category}')
        
        query = " AND ".join(query_parts)
        
        # 执行搜索
        search = arxiv.Search(
            query=query,
            max_results=self.max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )
        
        papers = []
        for result in search.results():
            paper_date = result.published.date()
            
            # 日期过滤
            if start_date:
                start = datetime.strptime(start_date, "%Y-%m-%d").date()
                if paper_date < start:
                    continue
            
            if end_date:
                end = datetime.strptime(end_date, "%Y-%m-%d").date()
                if paper_date > end:
                    continue
            
            # 提取论文信息
            paper = {
                "title": result.title,
                "authors": [author.name for author in result.authors],
                "summary": result.summary.replace('\n', ' '),
                "pdf_url": result.pdf_url,
                "arxiv_id": result.entry_id.split('/')[-1],
                "published": paper_date.strftime("%Y-%m-%d"),
                "categories": result.categories,
                "primary_category": result.primary_category
            }
            papers.append(paper)
        
        console.print(f"[green]✓ 找到 {len(papers)} 篇论文[/green]")
        return papers
    
    def get_paper_by_id(self, arxiv_id: str) -> Optional[Dict]:
        """
        根据 ArXiv ID 获取论文
        
        Args:
            arxiv_id: ArXiv 论文 ID
            
        Returns:
            论文信息字典
        """
        search = arxiv.Search(id_list=[arxiv_id])
        
        try:
            result = next(search.results())
            paper = {
                "title": result.title,
                "authors": [author.name for author in result.authors],
                "summary": result.summary.replace('\n', ' '),
                "pdf_url": result.pdf_url,
                "arxiv_id": arxiv_id,
                "published": result.published.date().strftime("%Y-%m-%d"),
                "categories": result.categories,
                "primary_category": result.primary_category
            }
            return paper
        except StopIteration:
            console.print(f"[red]✗ 未找到 ID 为 {arxiv_id} 的论文[/red]")
            return None
