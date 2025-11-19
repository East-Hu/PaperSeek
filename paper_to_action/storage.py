"""
论文存储模块
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from rich.console import Console

console = Console()


class PaperStorage:
    """论文存储类"""
    
    def __init__(self, output_dir: str = "papers"):
        """
        初始化存储
        
        Args:
            output_dir: 输出目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def save_papers_json(self, papers: List[Dict], filename: Optional[str] = None) -> str:
        """
        保存论文列表为 JSON 文件
        
        Args:
            papers: 论文列表
            filename: 文件名（可选，默认使用时间戳）
            
        Returns:
            保存的文件路径
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"papers_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(papers, f, ensure_ascii=False, indent=2)
            
            console.print(f"[green]✓ 论文数据已保存到 {filepath}[/green]")
            return str(filepath)
        except Exception as e:
            console.print(f"[red]✗ 保存失败：{str(e)}[/red]")
            return ""
    
    def save_papers_markdown(self, papers: List[Dict], filename: Optional[str] = None) -> str:
        """
        保存论文列表为 Markdown 文件
        
        Args:
            papers: 论文列表
            filename: 文件名（可选）
            
        Returns:
            保存的文件路径
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"papers_{timestamp}.md"
        
        filepath = self.output_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                # 写入标题
                f.write(f"# 论文速递 - {datetime.now().strftime('%Y-%m-%d')}\n\n")
                f.write(f"**共找到 {len(papers)} 篇论文**\n\n")
                f.write("---\n\n")
                
                # 写入每篇论文
                for i, paper in enumerate(papers, 1):
                    f.write(f"## {i}. {paper.get('title', 'N/A')}\n\n")
                    
                    # 基本信息
                    authors = ", ".join(paper.get('authors', [])[:3])
                    if len(paper.get('authors', [])) > 3:
                        authors += " et al."
                    
                    f.write(f"**作者：** {authors}\n\n")
                    f.write(f"**发布日期：** {paper.get('published', 'N/A')}\n\n")
                    f.write(f"**ArXiv ID：** {paper.get('arxiv_id', 'N/A')}\n\n")
                    f.write(f"**PDF 链接：** [{paper.get('pdf_url', 'N/A')}]({paper.get('pdf_url', 'N/A')})\n\n")
                    
                    # 分类
                    categories = ", ".join(paper.get('categories', []))
                    f.write(f"**分类：** {categories}\n\n")
                    
                    # AI 摘要
                    if 'ai_summary' in paper:
                        f.write("### 🤖 AI 核心创新点总结\n\n")
                        f.write(f"{paper['ai_summary']}\n\n")
                    
                    # 原始摘要
                    f.write("### 📄 原始摘要\n\n")
                    f.write(f"{paper.get('summary', 'N/A')}\n\n")
                    
                    f.write("---\n\n")
            
            console.print(f"[green]✓ Markdown 报告已保存到 {filepath}[/green]")
            return str(filepath)
        except Exception as e:
            console.print(f"[red]✗ 保存 Markdown 失败：{str(e)}[/red]")
            return ""
    
    def load_papers(self, filename: str) -> List[Dict]:
        """
        从 JSON 文件加载论文
        
        Args:
            filename: 文件名
            
        Returns:
            论文列表
        """
        filepath = self.output_dir / filename
        
        if not filepath.exists():
            console.print(f"[red]✗ 文件不存在：{filepath}[/red]")
            return []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                papers = json.load(f)
            
            console.print(f"[green]✓ 已从 {filepath} 加载 {len(papers)} 篇论文[/green]")
            return papers
        except Exception as e:
            console.print(f"[red]✗ 加载失败：{str(e)}[/red]")
            return []
    
    def list_saved_files(self) -> List[str]:
        """列出所有已保存的文件"""
        files = []
        
        for file in self.output_dir.glob("*"):
            if file.is_file():
                files.append(file.name)
        
        return sorted(files, reverse=True)
    
    def deduplicate_papers(self, papers: List[Dict]) -> List[Dict]:
        """
        去重论文列表（基于 ArXiv ID）
        
        Args:
            papers: 论文列表
            
        Returns:
            去重后的论文列表
        """
        seen_ids = set()
        unique_papers = []
        
        for paper in papers:
            arxiv_id = paper.get('arxiv_id')
            if arxiv_id and arxiv_id not in seen_ids:
                seen_ids.add(arxiv_id)
                unique_papers.append(paper)
        
        if len(unique_papers) < len(papers):
            console.print(f"[yellow]⚠ 去除了 {len(papers) - len(unique_papers)} 篇重复论文[/yellow]")
        

        return unique_papers
