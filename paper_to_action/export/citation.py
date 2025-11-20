"""
引用导出模块 - 支持多种引用格式
"""
from typing import List, Dict
from datetime import datetime


class CitationExporter:
    """引用格式导出器"""
    
    @staticmethod
    def to_bibtex(papers: List[Dict]) -> str:
        """
        导出为 BibTeX 格式
        
        Args:
            papers: 论文列表
            
        Returns:
            BibTeX 格式的字符串
        """
        bibtex_entries = []
        
        for i, paper in enumerate(papers, 1):
            # 生成唯一的 citation key
            first_author = paper.get('authors', ['Unknown'])[0].split()[-1] if paper.get('authors') else 'Unknown'
            year = paper.get('published', '2024')[:4]
            title_word = ''.join(filter(str.isalnum, paper.get('title', 'paper').split()[0]))
            cite_key = f"{first_author}{year}{title_word}"
            
            # 获取字段
            title = paper.get('title', 'Untitled')
            authors = ' and '.join(paper.get('authors', ['Unknown']))
            abstract = paper.get('abstract', paper.get('summary', ''))
            year = paper.get('published', '')[:4]
            
            # ArXiv ID
            arxiv_id = paper.get('arxiv_id') or paper.get('source_id', '')
            if paper.get('source') == 'arxiv' and not arxiv_id:
                # 从 URL 提取
                url = paper.get('url', '')
                if 'arxiv.org/abs/' in url:
                    arxiv_id = url.split('/abs/')[-1]
            
            # Journal或来源
            journal = paper.get('journal', 'arXiv' if arxiv_id else 'Unknown')
            
            # DOI
            doi = paper.get('doi', '')
            
            # URL
            url = paper.get('url', paper.get('link', ''))
            
            # 构建 BibTeX entry
            entry = f"""@article{{{cite_key},
  title = {{{{{title}}}}},
  author = {{{authors}}},
  year = {{{year}}},
  journal = {{{journal}}},"""
            
            if abstract:
                entry += f"\n  abstract = {{{{{abstract}}}}},"
            
            if arxiv_id:
                entry += f"\n  eprint = {{{arxiv_id}}},"
                entry += f"\n  archivePrefix = {{arXiv}},"
            
            if doi:
                entry += f"\n  doi = {{{doi}}},"
            
            if url:
                entry += f"\n  url = {{{url}}},"
            
            entry += "\n}"
            
            bibtex_entries.append(entry)
        
        return '\n\n'.join(bibtex_entries)
    
    @staticmethod
    def to_apa(paper: Dict) -> str:
        """
        生成 APA 格式引用
        
        Args:
            paper: 论文信息
            
        Returns:
            APA 格式引用
        """
        authors = paper.get('authors', ['Unknown'])
        
        # 格式化作者（最多3个，超过则用 et al.）
        if len(authors) == 1:
            author_str = authors[0]
        elif len(authors) == 2:
            author_str = f"{authors[0]} & {authors[1]}"
        elif len(authors) > 2:
            author_str = f"{authors[0]} et al."
        else:
            author_str = "Unknown"
        
        # 年份
        year = paper.get('published', '2024')[:4]
        
        # 标题
        title = paper.get('title', 'Untitled')
        
        # Journal/来源
        journal = paper.get('journal') or 'arXiv preprint'
        
        # ArXiv ID
        arxiv_id = paper.get('arxiv_id') or paper.get('source_id', '')
        
        # 构建引用
        citation = f"{author_str}. ({year}). {title}. *{journal}*"
        
        if arxiv_id and 'arxiv' in journal.lower():
            citation += f", {arxiv_id}"
        
        citation += "."
        
        return citation
    
    @staticmethod
    def to_mla(paper: Dict) -> str:
        """
        生成 MLA 格式引用
        
        Args:
            paper: 论文信息
            
        Returns:
            MLA 格式引用
        """
        authors = paper.get('authors', ['Unknown'])
        
        # 第一作者 Last, First
        if authors:
            first_author = authors[0]
            if first_author:
                parts = first_author.split()
                if len(parts) > 1:
                    author_str = f"{parts[-1]}, {' '.join(parts[:-1])}"
                else:
                    author_str = first_author
            else:
                author_str = "Unknown"
            
            # 如果有多个作者
            if len(authors) > 1:
                author_str += ", et al."
        else:
            author_str = "Unknown"
        
        # 标题
        title = paper.get('title', 'Untitled')
        
        # Journal
        journal = paper.get('journal') or 'ArXiv'
        
        # 年份
        year = paper.get('published', '2024')[:4]
        
        # ArXiv ID
        arxiv_id = paper.get('arxiv_id') or paper.get('source_id', '')
        
        # 构建引用
        citation = f"{author_str}. \"{title}.\" *{journal}*"
        
        if arxiv_id:
            citation += f", {arxiv_id}"
        
        citation += f", {year}."
        
        return citation
    
    @staticmethod
    def to_ieee(paper: Dict) -> str:
        """
        生成 IEEE 格式引用
        
        Args:
            paper: 论文信息
            
        Returns:
            IEEE 格式引用
        """
        authors = paper.get('authors', ['Unknown'])
        
        # 格式化作者（First Initial. Last）
        author_strs = []
        for author in authors[:3]:  # 最多3个
            parts = author.split()
            if len(parts) > 1:
                initials = '. '.join([p[0] for p in parts[:-1]]) + '.'
                author_strs.append(f"{initials} {parts[-1]}")
            else:
                author_strs.append(author)
        
        if len(authors) > 3:
            author_str = ', '.join(author_strs) + ', et al.'
        else:
            author_str = ', '.join(author_strs)
        
        # 标题
        title = paper.get('title', 'Untitled')
        
        # Journal
        journal = paper.get('journal') or 'arXiv'
        
        # 年份
        year = paper.get('published', '2024')[:4]
        
        # ArXiv ID
        arxiv_id = paper.get('arxiv_id') or paper.get('source_id', '')
        
        # 构建引用
        citation = f"{author_str}, \"{title},\" *{journal}*"
        
        if arxiv_id:
            citation += f", {arxiv_id}"
        
        citation += f", {year}."
        
        return citation
    
    @staticmethod
    def export_all_formats(papers: List[Dict], output_dir: str = "papers/citations"):
        """
        导出所有格式
        
        Args:
            papers: 论文列表 (Paper对象或字典)
            output_dir: 输出目录
            
        Returns:
            保存的文件路径列表
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # 确保所有论文都是字典格式
        paper_dicts = []
        for p in papers:
            if hasattr(p, 'to_dict'):
                paper_dicts.append(p.to_dict())
            elif isinstance(p, dict):
                paper_dicts.append(p)
            else:
                try:
                    paper_dicts.append(p.__dict__)
                except:
                    continue
        
        papers = paper_dicts
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        saved_files = []
        
        # BibTeX
        bibtex_path = os.path.join(output_dir, f"citations_{timestamp}.bib")
        with open(bibtex_path, 'w', encoding='utf-8') as f:
            f.write(CitationExporter.to_bibtex(papers))
        saved_files.append(bibtex_path)
        
        # TXT with all formats
        txt_path = os.path.join(output_dir, f"citations_{timestamp}.txt")
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("# Citation Formats\n\n")
            
            for i, paper in enumerate(papers, 1):
                title = paper.get('title', 'Untitled')
                f.write(f"## {i}. {title}\n\n")
                f.write(f"**APA**:\n{CitationExporter.to_apa(paper)}\n\n")
                f.write(f"**MLA**:\n{CitationExporter.to_mla(paper)}\n\n")
                f.write(f"**IEEE**:\n{CitationExporter.to_ieee(paper)}\n\n")
                f.write("-" * 80 + "\n\n")
        
        saved_files.append(txt_path)
        
        return saved_files
