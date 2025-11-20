"""
多数据源搜索管理器
"""
from typing import List, Optional, Dict
from .base import PaperSource, Paper
from .arxiv import ArxivSource
from .semantic_scholar import SemanticScholarSource
from rich.console import Console

console = Console()


class SourceManager:
    """数据源管理器"""
    
    def __init__(self):
        self.sources: Dict[str, PaperSource] = {
            'arxiv': ArxivSource(),
            'semantic': SemanticScholarSource(),
        }
        self.default_source = 'arxiv'
    
    def get_source(self, name: str) -> Optional[PaperSource]:
        """获取指定数据源"""
        return self.sources.get(name.lower())
    
    def list_sources(self) -> List[tuple]:
        """列出所有可用数据源"""
        return [(name, source.name, source.description) 
                for name, source in self.sources.items()]
    
    def search(
        self,
        keywords: str,
        source_names: List[str] = None,
        max_results: int = 20,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> List[Paper]:
        """
        跨数据源搜索
        
        Args:
            keywords: 搜索关键词
            source_names: 要搜索的数据源列表，None 表示使用默认源
            max_results: 每个源的最大结果数
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            合并后的论文列表
        """
        if source_names is None:
            source_names = [self.default_source]
        
        all_papers = []
        
        for source_name in source_names:
            source = self.get_source(source_name)
            if source:
                console.print(f"\n[cyan]📚 正在搜索 {source.name}...[/cyan]")
                papers = source.search(
                    keywords=keywords,
                    max_results=max_results,
                    start_date=start_date,
                    end_date=end_date,
                    **kwargs
                )
                all_papers.extend(papers)
                console.print(f"[green]✓ {source.name}: 找到 {len(papers)} 篇[/green]")
            else:
                console.print(f"[yellow]⚠ 未知数据源: {source_name}[/yellow]")
        
        # 去重（基于标题）
        unique_papers = self._deduplicate(all_papers)
        
        if len(unique_papers) < len(all_papers):
            console.print(f"[yellow]去除了 {len(all_papers) - len(unique_papers)} 篇重复论文[/yellow]")
        
        return unique_papers
    
    def _deduplicate(self, papers: List[Paper]) -> List[Paper]:
        """基于标题去重"""
        seen_titles = set()
        unique_papers = []
        
        for paper in papers:
            # 标准化标题（小写，去除多余空格）
            normalized_title = ' '.join(paper.title.lower().split())
            
            if normalized_title not in seen_titles:
                seen_titles.add(normalized_title)
                unique_papers.append(paper)
        
        return unique_papers


# 导出所有源
__all__ = [
    'SourceManager',
    'PaperSource',
    'Paper',
    'ArxivSource',
    'SemanticScholarSource',
]
