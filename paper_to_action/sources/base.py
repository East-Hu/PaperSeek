"""
抽象基类 - 定义论文数据源的统一接口
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Paper:
    """统一的论文数据结构"""
    # --- 必填字段 (无默认值) ---
    title: str
    authors: List[str]
    abstract: str
    published: str  # ISO 8601 格式
    source: str  # 数据源: arxiv, pubmed, scholar等
    source_id: str  # 在该源的 ID
    url: str
    
    # --- 可选字段 (有默认值) ---
    updated: Optional[str] = None
    doi: Optional[str] = None
    pdf_url: Optional[str] = None
    journal: Optional[str] = None
    categories: List[str] = None
    citations: Optional[int] = None  # 引用次数
    ai_summary: Optional[str] = None
    
    def __post_init__(self):
        if self.categories is None:
            self.categories = []
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'title': self.title,
            'authors': self.authors,
            'abstract': self.abstract,
            'summary': self.abstract,  # 兼容旧字段名
            'published': self.published,
            'updated': self.updated,
            'source': self.source,
            'source_id': self.source_id,
            'arxiv_id': self.source_id if self.source == 'arxiv' else None,  # 兼容
            'doi': self.doi,
            'url': self.url,
            'link': self.url,  # 兼容旧字段名
            'pdf_url': self.pdf_url,
            'journal': self.journal,
            'categories': self.categories,
            'citations': self.citations,
            'ai_summary': self.ai_summary
        }


class PaperSource(ABC):
    """论文数据源抽象基类"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """数据源名称"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """数据源描述"""
        pass
    
    @abstractmethod
    def search(
        self,
        keywords: str,
        max_results: int = 20,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> List[Paper]:
        """
        搜索论文
        
        Args:
            keywords: 搜索关键词
            max_results: 最大结果数
            start_date: 开始日期 (可选)
            end_date: 结束日期 (可选)
            **kwargs: 其他特定于数据源的参数
            
        Returns:
            论文列表
        """
        pass
    
    @abstractmethod
    def get_pdf_url(self, paper: Paper) -> Optional[str]:
        """
        获取论文的 PDF URL
        
        Args:
            paper: 论文对象
            
        Returns:
            PDF URL，如果不可用则返回 None
        """
        pass
    
    def get_details(self, source_id: str) -> Optional[Paper]:
        """
        获取论文详细信息
        
        Args:
            source_id: 论文在该数据源的 ID
            
        Returns:
            论文对象，如果不存在则返回 None
        """
        # 默认实现：子类可以覆盖
        return None
    
    def supports_pdf_download(self) -> bool:
        """
        是否支持 PDF 下载
        
        Returns:
            True 如果支持
        """
        return False
