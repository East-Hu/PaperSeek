"""
Semantic Scholar 数据源实现
"""
import requests
from typing import List, Optional
from .base import PaperSource, Paper
from rich.console import Console
import time

console = Console()


class SemanticScholarSource(PaperSource):
    """Semantic Scholar 论文数据源 - AI驱动的学术搜索"""
    
    @property
    def name(self) -> str:
        return "Semantic Scholar"
    
    @property
    def description(self) -> str:
        return "AI驱动的学术搜索引擎 (计算机科学、神经科学等)"
    
    def __init__(self):
        self.base_url = "https://api.semanticscholar.org/graph/v1"
        self.search_url = f"{self.base_url}/paper/search"
    
    def search(
        self,
        keywords: str,
        max_results: int = 20,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> List[Paper]:
        """
        搜索 Semantic Scholar 论文
        
        Args:
            keywords: 搜索关键词
            max_results: 最大结果数
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            
        Returns:
            论文列表
        """
        papers = []
        
        try:
            # Semantic Scholar API 参数
            params = {
                'query': keywords,
                'limit': min(max_results, 100),  # API 限制
                'fields': 'paperId,title,abstract,authors,year,publicationDate,citationCount,url,openAccessPdf,journal,externalIds'
            }
            
            # 添加年份过滤
            if start_date:
                start_year = start_date[:4]
                if end_date:
                    end_year = end_date[:4]
                    params['year'] = f"{start_year}-{end_year}"
                else:
                    params['year'] = f"{start_year}-"
            elif end_date:
                params['year'] = f"-{end_date[:4]}"
            
            response = requests.get(
                self.search_url,
                params=params,
                timeout=30,
                headers={'User-Agent': 'PaperSeek (mailto:research@example.com)'}
            )
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' in data:
                for item in data['data']:
                    paper = self._parse_paper(item, start_date, end_date)
                    if paper:
                        papers.append(paper)
            
            console.print(f"[green]✓ Semantic Scholar 找到 {len(papers)} 篇论文[/green]")
            
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Semantic Scholar 搜索失败: {str(e)}[/red]")
        except Exception as e:
            console.print(f"[red]Semantic Scholar 错误: {str(e)}[/red]")
        
        return papers
    
    def _parse_paper(
        self,
        data: dict,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Optional[Paper]:
        """解析单篇论文数据"""
        try:
            # 基本信息
            title = data.get('title', '')
            abstract = data.get('abstract', '') or '无摘要'
            
            # 作者
            authors = []
            for author in data.get('authors', []):
                if 'name' in author:
                    authors.append(author['name'])
            
            # 日期
            pub_date = data.get('publicationDate', '')
            if not pub_date  and 'year' in data:
                pub_date = f"{data['year']}-01-01"
            
            # 日期过滤
            if pub_date:
                if start_date and pub_date < start_date:
                    return None
                if end_date and pub_date > end_date:
                    return None
            
            # URL
            paper_id = data.get('paperId', '')
            url = data.get('url', f"https://www.semanticscholar.org/paper/{paper_id}")
            
            # PDF URL
            pdf_url = None
            if 'openAccessPdf' in data and data['openAccessPdf']:
                pdf_url = data['openAccessPdf'].get('url')
            
            # 获取 DOI 和 ArXiv ID
            doi = None
            arxiv_id = None
            if 'externalIds' in data:
                ext_ids = data['externalIds']
                doi = ext_ids.get('DOI')
                arxiv_id = ext_ids.get('ArXiv')
            
            # 期刊信息
            journal = None
            if 'journal' in data and data['journal']:
                journal = data['journal'].get('name')
            
            # 引用次数
            citations = data.get('citationCount', 0)
            
            # 创建 Paper 对象
            paper = Paper(
                title=title,
                authors=authors,
                abstract=abstract,
                published=pub_date or "Unknown",
                source='semantic_scholar',
                source_id=paper_id,
                doi=doi,
                url=url,
                pdf_url=pdf_url,
                journal=journal,
                citations=citations,
                categories=[]
            )
            
            return paper
            
        except Exception as e:
            console.print(f"[yellow]解析 Semantic Scholar 论文失败: {str(e)}[/yellow]")
            return None
    
    def get_pdf_url(self, paper: Paper) -> Optional[str]:
        """获取 PDF URL"""
        return paper.pdf_url
    
    def supports_pdf_download(self) -> bool:
        """部分论文支持 PDF 下载"""
        return True
    
    def get_details(self, source_id: str) -> Optional[Paper]:
        """获取论文详细信息"""
        try:
            url = f"{self.base_url}/paper/{source_id}"
            params = {
                'fields': 'paperId,title,abstract,authors,year,publicationDate,citationCount,url,openAccessPdf,journal,externalIds'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return self._parse_paper(data)
            
        except Exception as e:
            console.print(f"[red]获取论文详情失败: {str(e)}[/red]")
            return None
