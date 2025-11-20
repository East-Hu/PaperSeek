"""
Export and Citation Module
"""
from typing import List, Dict

class Exporter:
    @staticmethod
    def to_bibtex(paper: Dict) -> str:
        """Generate BibTeX entry for a paper"""
        # Simple BibTeX generation
        first_author = paper.get('authors', ['Unknown'])[0].split()[-1]
        year = paper.get('published', '0000').split('-')[0]
        title_word = paper.get('title', 'title').split()[0]
        citation_key = f"{first_author}{year}{title_word}"
        
        bib = f"@article{{{citation_key},\n"
        bib += f"  title = {{{paper.get('title')}}},\n"
        bib += f"  author = {{{' and '.join(paper.get('authors', []))}}},\n"
        bib += f"  year = {{{year}}},\n"
        bib += f"  journal = {{ArXiv preprint}},\n" # Assuming ArXiv for now
        bib += f"  url = {{{paper.get('pdf_url')}}}\n"
        bib += "}"
        return bib

    @staticmethod
    def to_ris(paper: Dict) -> str:
        """Generate RIS entry for a paper"""
        ris = "TY  - JOUR\n"
        ris += f"TI  - {paper.get('title')}\n"
        for author in paper.get('authors', []):
            ris += f"AU  - {author}\n"
        ris += f"PY  - {paper.get('published', '').replace('-', '/')}\n"
        ris += f"UR  - {paper.get('pdf_url')}\n"
        ris += "ER  - \n"
        return ris

    @staticmethod
    def generate_citation(paper: Dict, style: str = "apa") -> str:
        """Generate citation string"""
        authors = paper.get('authors', [])
        title = paper.get('title')
        year = paper.get('published', '0000').split('-')[0]
        
        if style.lower() == "apa":
            # Author, A. A. (Year). Title of article.
            author_str = ", ".join(authors) # Simplified
            return f"{author_str} ({year}). {title}. ArXiv."
        elif style.lower() == "mla":
            # Author. "Title." Title of Container, Other contributors, Version, Number, Publisher, Publication Date, Location.
            author_str = authors[0] if authors else "Unknown"
            if len(authors) > 1:
                author_str += " et al."
            return f"{author_str} \"{title}.\" ArXiv, {year}."
        else:
            return f"{title} - {', '.join(authors)} ({year})"
