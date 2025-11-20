"""
论文收藏管理模块
"""
import os
import json
import shutil
from typing import List, Dict
from pathlib import Path
from rich.console import Console

console = Console()


class FavoriteManager:
    """论文收藏管理器"""
    
    def __init__(self, output_dir: str = "papers"):
        """
        初始化收藏管理器
        
        Args:
            output_dir: 输出目录
        """
        self.output_dir = Path(output_dir)
        self.favorites_dir = self.output_dir / "favorites"
        self.metadata_file = self.favorites_dir / "metadata.json"
        
        # 创建收藏夹目录
        self._ensure_favorites_dir()
    
    def _ensure_favorites_dir(self):
        """确保收藏夹目录存在"""
        if not self.favorites_dir.exists():
            self.favorites_dir.mkdir(parents=True, exist_ok=True)
            console.print(f"[green]✓ 创建收藏夹: {self.favorites_dir}[/green]")
        
        # 创建metadata文件
        if not self.metadata_file.exists():
            self._save_metadata({"favorites": []})
    
    def _load_metadata(self) -> Dict:
        """加载元数据"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"favorites": []}
    
    def _save_metadata(self, metadata: Dict):
        """保存元数据"""
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, indent=2, fp=f, ensure_ascii=False)
    
    def add_favorite(self, paper: Dict) -> bool:
        """
        将论文添加到收藏夹
        
        Args:
            paper: 论文信息
            
        Returns:
            是否成功添加
        """
        # 加载现有收藏
        metadata = self._load_metadata()
        favorites = metadata.get("favorites", [])
        
        # 检查是否已收藏
        paper_id = paper.get('source_id') or paper.get('arxiv_id', '')
        
        for fav in favorites:
            if fav.get('id') == paper_id:
                console.print(f"[yellow]⚠ 论文已在收藏夹中[/yellow]")
                return False
        
        # 添加到收藏列表
        favorite_entry = {
            'id': paper_id,
            'title': paper.get('title', ''),
            'authors': paper.get('authors', []),
            'added_date': self._get_current_time(),
            'source': paper.get('source', 'unknown'),
            'tags': paper.get('tags', [])
        }
        
        favorites.append(favorite_entry)
        
        # 复制论文PDF（如果有）
        if 'pdf_path' in paper and os.path.exists(paper['pdf_path']):
            pdf_filename = os.path.basename(paper['pdf_path'])
            dest_path = self.favorites_dir / pdf_filename
            shutil.copy2(paper['pdf_path'], dest_path)
            favorite_entry['pdf_path'] = str(dest_path)
        
        # 保存完整论文信息
        paper_file = self.favorites_dir / f"{paper_id}.json"
        with open(paper_file, 'w', encoding='utf-8') as f:
           json.dump(paper, fp=f, indent=2, ensure_ascii=False)
        
        favorite_entry['data_file'] = str(paper_file)
        
        # 更新元数据
        metadata['favorites'] = favorites
        self._save_metadata(metadata)
        
        console.print(f"[green]✓ 已添加到收藏夹: {paper.get('title', '')[:50]}...[/green]")
        return True
    
    def remove_favorite(self, paper_id: str) -> bool:
        """
        从收藏夹移除论文
        
        Args:
            paper_id: 论文ID
            
        Returns:
            是否成功移除
        """
        metadata = self._load_metadata()
        favorites = metadata.get("favorites", [])
        
        # 查找并移除
        for i, fav in enumerate(favorites):
            if fav.get('id') == paper_id:
                # 删除关联文件
                if 'data_file' in fav and os.path.exists(fav['data_file']):
                    os.remove(fav['data_file'])
                if 'pdf_path' in fav and os.path.exists(fav['pdf_path']):
                    os.remove(fav['pdf_path'])
                
                favorites.pop(i)
                metadata['favorites'] = favorites
                self._save_metadata(metadata)
                
                console.print(f"[green]✓ 已从收藏夹移除[/green]")
                return True
        
        console.print(f"[yellow]⚠ 未找到该论文[/yellow]")
        return False
    
    def list_favorites(self) -> List[Dict]:
        """
        列出所有收藏的论文
        
        Returns:
            收藏列表
        """
        metadata = self._load_metadata()
        return metadata.get("favorites", [])
    
    def get_favorite(self, paper_id: str) -> Dict:
        """
        获取收藏的论文详细信息
        
        Args:
            paper_id: 论文ID
            
        Returns:
            论文信息字典
        """
        paper_file = self.favorites_dir / f"{paper_id}.json"
        if paper_file.exists():
            with open(paper_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _get_current_time(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def display_favorites(self):
        """显示收藏列表"""
        favorites = self.list_favorites()
        
        if not favorites:
            console.print("[yellow]收藏夹为空[/yellow]")
            return
        
        console.print(f"\n[bold cyan]📚 收藏夹 ({len(favorites)} 篇论文)[/bold cyan]\n")
        
        from rich.table import Table
        from rich import box
        
        table = Table(show_header=True, box=box.ROUNDED, border_style="cyan")
        table.add_column("#", style="bright_cyan", width=4)
        table.add_column("标题", style="bright_green", width=50)
        table.add_column("作者", style="white", width=25)
        table.add_column("标签", style="yellow", width=20)
        
        for i, fav in enumerate(favorites, 1):
            title = fav.get('title', '')[:47] + "..." if len(fav.get('title', '')) > 50 else fav.get('title', '')
            authors = fav.get('authors', [])
            author_str = authors[0] if authors else "Unknown"
            tags_str = ', '.join(fav.get('tags', [])[:2])
            
            table.add_row(str(i), title, author_str, tags_str)
        
        console.print(table)
        console.print(f"\n[dim]收藏夹路径: {self.favorites_dir}[/dim]\n")
