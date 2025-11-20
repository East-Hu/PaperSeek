"""
Paper Crawler Module
Supports multiple sources (ArXiv, etc.)
"""
import arxiv
import requests
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Optional
from rich.console import Console

console = Console()

class BaseCrawler(ABC):
    """Base class for paper crawlers"""
    
    def __init__(self, max_results: int = 50):
        self.max_results = max_results
        
    @abstractmethod
    def search_papers(self, keywords: str, start_date: Optional[str] = None, end_date: Optional[str] = None, **kwargs) -> List[Dict]:
        pass
        
    @abstractmethod
    def get_paper_by_id(self, paper_id: str) -> Optional[Dict]:
        pass

class ArxivCrawler(BaseCrawler):
    """ArXiv Crawler Implementation"""
    
    def search_papers(
        self,
        keywords: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        category: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        console.print(f"[cyan]🔍 Searching ArXiv for: {keywords}[/cyan]")
        
        query_parts = []
        if keywords:
            keywords_list = [kw.strip() for kw in keywords.split(',')]
            if len(keywords_list) > 1:
                keyword_query = " OR ".join([f'all:"{kw}"' for kw in keywords_list])
                query_parts.append(f"({keyword_query})")
            else:
                query_parts.append(f'all:"{keywords}"')
        
        if category:
            query_parts.append(f'cat:{category}')
        
        query = " AND ".join(query_parts)
        
        search = arxiv.Search(
            query=query,
            max_results=self.max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )
        
        papers = []
        for result in search.results():
            paper_date = result.published.date()
            
            if start_date:
                start = datetime.strptime(start_date, "%Y-%m-%d").date()
                if paper_date < start:
                    continue
            
            if end_date:
                end = datetime.strptime(end_date, "%Y-%m-%d").date()
                if paper_date > end:
                    continue
            
            paper = {
                "source": "arxiv",
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
        
        console.print(f"[green]✓ Found {len(papers)} papers from ArXiv[/green]")
        return papers
    
    def get_paper_by_id(self, paper_id: str) -> Optional[Dict]:
        search = arxiv.Search(id_list=[paper_id])
        try:
            result = next(search.results())
            return {
                "source": "arxiv",
                "title": result.title,
                "authors": [author.name for author in result.authors],
                "summary": result.summary.replace('\n', ' '),
                "pdf_url": result.pdf_url,
                "arxiv_id": paper_id,
                "published": result.published.date().strftime("%Y-%m-%d"),
                "categories": result.categories,
                "primary_category": result.primary_category
            }
        except StopIteration:
            return None

class SemanticScholarCrawler(BaseCrawler):
    """Semantic Scholar Crawler (Basic Implementation)"""
    
    BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
    
    def search_papers(
        self,
        keywords: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        console.print(f"[cyan]🔍 Searching Semantic Scholar for: {keywords}[/cyan]")
        
        params = {
            "query": keywords,
            "limit": self.max_results,
            "fields": "title,authors,abstract,url,publicationDate,paperId"
        }
        
        if start_date:
            # Semantic Scholar API supports year range, but let's filter manually for simplicity or check API docs
            # API supports `year` parameter like `2019-2023`
            start_year = start_date.split('-')[0]
            end_year = end_date.split('-')[0] if end_date else datetime.now().year
            params["year"] = f"{start_year}-{end_year}"

        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            papers = []
            for item in data.get('data', []):
                paper = {
                    "source": "semantic_scholar",
                    "title": item.get('title'),
                    "authors": [a['name'] for a in item.get('authors', [])],
                    "summary": item.get('abstract'),
                    "pdf_url": item.get('url'), # Might not be direct PDF
                    "source_id": item.get('paperId'),
                    "published": item.get('publicationDate'),
                    "categories": [] # Semantic scholar doesn't give categories easily in search
                }
                papers.append(paper)
                
            console.print(f"[green]✓ Found {len(papers)} papers from Semantic Scholar[/green]")
            return papers
            
        except Exception as e:
            console.print(f"[red]Error searching Semantic Scholar: {e}[/red]")
            return []

    def get_paper_by_id(self, paper_id: str) -> Optional[Dict]:
        # Implementation for fetching by ID
        pass
