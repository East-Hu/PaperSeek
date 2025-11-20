"""
ArXiv 数据源实现
"""
import requests
import xml.etree.ElementTree as ET
from typing import List, Optional
from .base import PaperSource, Paper
from rich.console import Console

console = Console()


class ArxivSource(PaperSource):
    """ArXiv 论文数据源"""
    
    @property
    def name(self) -> str:
        return "ArXiv"
    
    @property
    def description(self) -> str:
        return "开放获取的预印本论文库 (物理、数学、CS、生物等)"
    
    def __init__(self, max_results: int = 20):
        self.max_results = max_results
        self.base_url = "http://export.arxiv.org/api/query"
    
    def search(
        self,
        keywords: str,
        max_results: int = 20,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> List[Paper]:
        """
        搜索 ArXiv 论文
        
        Args:
            keywords: 搜索关键词
            max_results: 最大结果数
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            
        Returns:
            论文列表
        """
        # 构建查询参数
        params = {
            'search_query': f'all:{keywords}',
            'start': 0,
            'max_results': max_results,
            'sortBy': 'lastUpdatedDate',
            'sortOrder': 'descending'
        }
        
        
        # 重试机制
        import time
        max_retries = 3
        retry_delay = 3  # 秒
        
        for attempt in range(max_retries):
            try:
                response = requests.get(self.base_url, params=params, timeout=30)
                
                # 检查 429 错误
                if response.status_code == 429:
                    if attempt < max_retries - 1:
                        console.print(f"[yellow]⚠ ArXiv API 限流，{retry_delay}秒后重试...[/yellow]")
                        time.sleep(retry_delay)
                        retry_delay *= 2  # 指数退避
                        continue
                    else:
                        console.print(f"[red]✗ ArXiv API 限流，请稍后再试或减少搜索频率[/red]")
                        return []
                
                response.raise_for_status()
                papers = self._parse_response(response.text, start_date, end_date)
                
                # 添加小延迟避免触发限流
                time.sleep(1)
                return papers
                
            except requests.exceptions.HTTPError as e:
                if attempt < max_retries - 1:
                    console.print(f"[yellow]⚠ 请求失败，{retry_delay}秒后重试...[/yellow]")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                else:
                    console.print(f"[red]ArXiv 搜索失败: {str(e)}[/red]")
                    return []
            except Exception as e:
                console.print(f"[red]ArXiv 搜索失败: {str(e)}[/red]")
                return []
        
        return []
    
    def _parse_response(
        self,
        xml_data: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Paper]:
        """解析 ArXiv API 返回的 XML 数据"""
        papers = []
        
        try:
            root = ET.fromstring(xml_data)
            namespace = {'atom': 'http://www.w3.org/2005/Atom'}
            
            for entry in root.findall('atom:entry', namespace):
                try:
                    # 提取基本信息
                    title = entry.find('atom:title', namespace).text.strip().replace('\n', ' ')
                    summary = entry.find('atom:summary', namespace).text.strip().replace('\n', ' ')
                    
                    # 提取日期
                    published = entry.find('atom:published', namespace).text
                    updated = entry.find('atom:updated', namespace).text
                    
                    # 日期过滤
                    pub_date = published.split('T')[0]
                    if start_date and pub_date < start_date:
                        continue
                    if end_date and pub_date > end_date:
                        continue
                    
                    # 提取作者
                    authors = []
                    for author in entry.findall('atom:author', namespace):
                        name = author.find('atom:name', namespace)
                        if name is not None:
                            authors.append(name.text)
                    
                    # 提取链接
                    url = None
                    pdf_url = None
                    for link in entry.findall('atom:link', namespace):
                        if link.get('type') == 'text/html':
                            url = link.get('href')
                        elif link.get('title') == 'pdf':
                            pdf_url = link.get('href')
                    
                    # 提取 ArXiv ID
                    id_text = entry.find('atom:id', namespace).text
                    arxiv_id = id_text.split('/abs/')[-1]
                    
                    # 提取分类
                    categories = []
                    for category in entry.findall('atom:category', namespace):
                        term = category.get('term')
                        if term:
                            categories.append(term)
                    
                    # 提取 DOI (如果有)
                    doi = None
                    doi_elem = entry.find('arxiv:doi', {'arxiv': 'http://arxiv.org/schemas/atom'})
                    if doi_elem is not None:
                        doi = doi_elem.text
                    
                    # 创建 Paper 对象
                    paper = Paper(
                        title=title,
                        authors=authors,
                        abstract=summary,
                        published=published,
                        updated=updated,
                        source='arxiv',
                        source_id=arxiv_id,
                        doi=doi,
                        url=url or f"https://arxiv.org/abs/{arxiv_id}",
                        pdf_url=pdf_url or f"https://arxiv.org/pdf/{arxiv_id}.pdf",
                        categories=categories
                    )
                    
                    papers.append(paper)
                    
                except Exception as e:
                    console.print(f"[yellow]解析论文条目失败: {str(e)}[/yellow]")
                    continue
            
        except ET.ParseError as e:
            console.print(f"[red]XML 解析失败: {str(e)}[/red]")
        
        return papers
    
    def get_pdf_url(self, paper: Paper) -> Optional[str]:
        """获取 PDF URL"""
        if paper.pdf_url:
            return paper.pdf_url
        
        if paper.source == 'arxiv' and paper.source_id:
            return f"https://arxiv.org/pdf/{paper.source_id}.pdf"
        
        return None
    
    def supports_pdf_download(self) -> bool:
        """ArXiv 支持 PDF 下载"""
        return True
