"""
PDF 下载模块 - 用于下载 ArXiv 论文 PDF
"""
import requests
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
import time

console = Console()


@dataclass
class DownloadResult:
    """单个 PDF 下载结果"""
    paper_id: str
    title: str
    success: bool
    file_path: Optional[str] = None
    error: Optional[str] = None
    url: Optional[str] = None


@dataclass
class DownloadStats:
    """批量下载统计"""
    total: int
    successful: int
    failed: int
    results: List[DownloadResult]


class PDFDownloader:
    """ArXiv PDF 下载器"""
    
    def __init__(self, output_dir: str = "papers/pdfs", timeout: int = 30, max_retries: int = 3):
        """
        初始化 PDF 下载器
        
        Args:
            output_dir: PDF 保存目录
            timeout: 下载超时时间（秒）
            max_retries: 最大重试次数
        """
        self.output_dir = output_dir
        self.timeout = timeout
        self.max_retries = max_retries
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
    
    def get_pdf_url(self, arxiv_id: str) -> str:
        """
        获取 ArXiv PDF URL
        
        Args:
            arxiv_id: ArXiv ID (例如: 2301.01234 或 abs/2301.01234)
            
        Returns:
            PDF URL
        """
        # 清理 arxiv_id
        arxiv_id = arxiv_id.replace('http://arxiv.org/', '')
        arxiv_id = arxiv_id.replace('https://arxiv.org/', '')
        arxiv_id = arxiv_id.replace('abs/', '')
        arxiv_id = arxiv_id.replace('pdf/', '')
        arxiv_id = arxiv_id.replace('.pdf', '')
        
        return f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    
    def sanitize_filename(self, title: str, arxiv_id: str) -> str:
        """
        生成安全的文件名
        
        Args:
            title: 论文标题
            arxiv_id: ArXiv ID
            
        Returns:
            安全的文件名
        """
        # 移除或替换不安全字符
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
        # 限制长度
        safe_title = safe_title[:50]
        # 清理 arxiv_id
        clean_id = arxiv_id.split('/')[-1].replace('.pdf', '')
        
        return f"{clean_id}_{safe_title}.pdf"
    
    def download_with_retry(self, url: str, filepath: str) -> Tuple[bool, Optional[str]]:
        """
        带重试的下载
        
        Args:
            url: 下载 URL
            filepath: 保存路径
            
        Returns:
            (成功与否, 错误信息)
        """
        for attempt in range(self.max_retries):
            try:
                response = requests.get(
                    url,
                    timeout=self.timeout,
                    headers={'User-Agent': 'Mozilla/5.0 (PaperSeek Bot)'},
                    stream=True
                )
                
                if response.status_code == 200:
                    # 检查是否真的是 PDF
                    content_type = response.headers.get('Content-Type', '')
                    if 'application/pdf' not in content_type:
                        return False, f"响应不是 PDF 文件 (Content-Type: {content_type})"
                    
                    # 保存文件
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    
                    # 验证文件大小
                    file_size = os.path.getsize(filepath)
                    if file_size < 1000:  # 小于 1KB 可能是错误页面
                        os.remove(filepath)
                        return False, f"文件过小 ({file_size} bytes)，可能不是有效的 PDF"
                    
                    return True, None
                
                elif response.status_code == 404:
                    return False, "PDF 不存在 (404)"
                
                elif response.status_code == 403:
                    return False, "访问被拒绝 (403)"
                
                else:
                    error_msg = f"HTTP {response.status_code}"
                    if attempt < self.max_retries - 1:
                        wait_time = 2 ** attempt  # 指数退避: 1s, 2s, 4s
                        time.sleep(wait_time)
                        continue
                    return False, error_msg
                    
            except requests.exceptions.Timeout:
                error_msg = "下载超时"
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                    continue
                return False, error_msg
                
            except requests.exceptions.ConnectionError:
                error_msg = "连接失败"
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                    continue
                return False, error_msg
                
            except Exception as e:
                return False, f"未知错误: {str(e)}"
        
        return False, f"重试 {self.max_retries} 次后仍然失败"
    
    def download_paper(self, paper: Dict) -> DownloadResult:
        """
        下载单篇论文的 PDF
        
        Args:
            paper: 论文信息字典
            
        Returns:
            下载结果
        """
        arxiv_id = paper.get('arxiv_id', '')
        title = paper.get('title', 'untitled')
        
        if not arxiv_id:
            return DownloadResult(
                paper_id=arxiv_id,
                title=title,
                success=False,
                error="缺少 ArXiv ID"
            )
        
        # 生成 URL 和文件路径
        pdf_url = self.get_pdf_url(arxiv_id)
        filename = self.sanitize_filename(title, arxiv_id)
        filepath = os.path.join(self.output_dir, filename)
        
        # 检查文件是否已存在
        if os.path.exists(filepath):
            return DownloadResult(
                paper_id=arxiv_id,
                title=title,
                success=True,
                file_path=filepath,
                url=pdf_url
            )
        
        # 下载
        success, error = self.download_with_retry(pdf_url, filepath)
        
        return DownloadResult(
            paper_id=arxiv_id,
            title=title,
            success=success,
            file_path=filepath if success else None,
            error=error,
            url=pdf_url
        )
    
    def batch_download(
        self, 
        papers: List[Dict], 
        progress_callback=None
    ) -> DownloadStats:
        """
        批量下载论文 PDF
        
        Args:
            papers: 论文列表
            progress_callback: 进度回调函数，接收 (current, total) 参数
            
        Returns:
            下载统计
        """
        results = []
        successful = 0
        failed = 0
        
        for i, paper in enumerate(papers, 1):
            result = self.download_paper(paper)
            results.append(result)
            
            if result.success:
                successful += 1
            else:
                failed += 1
            
            # 回调进度
            if progress_callback:
                progress_callback(i)
            
            # 小延迟，避免过快请求
            if i < len(papers):
                time.sleep(0.5)
        
        return DownloadStats(
            total=len(papers),
            successful=successful,
            failed=failed,
            results=results
        )
    
    def print_download_report(self, stats: DownloadStats):
        """
        打印下载报告
        
        Args:
            stats: 下载统计
        """
        console.print("\n" + "="*60)
        console.print(f"[bold bright_cyan]📊 下载统计报告[/bold bright_cyan]\n")
        
        console.print(f"[cyan]总计尝试:[/cyan] {stats.total} 篇")
        console.print(f"[green]成功下载:[/green] {stats.successful} 篇 ✓")
        console.print(f"[red]下载失败:[/red] {stats.failed} 篇 ✗")
        
        if stats.failed > 0:
            console.print(f"\n[yellow]❌ 下载失败的论文:[/yellow]\n")
            
            for i, result in enumerate([r for r in stats.results if not r.success], 1):
                console.print(f"  {i}. [bold]{result.title[:60]}...[/bold]")
                console.print(f"     [dim]原因:[/dim] {result.error}")
                console.print(f"     [dim]链接:[/dim] {result.url}")
                console.print()
        
        if stats.successful > 0:
            console.print(f"\n[green]✓ 成功下载的 PDF 已保存到:[/green]")
            console.print(f"  [cyan]{self.output_dir}/[/cyan]")
        
        console.print("="*60 + "\n")
