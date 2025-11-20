"""
Database module for PaperSeek
Handles storage of papers, tags, notes, and favorites using SQLite.
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any
from rich.console import Console

console = Console()

class Database:
    def __init__(self, db_path: str = "paper_robot.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """Initialize database tables"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Papers table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            source_id TEXT NOT NULL,
            title TEXT NOT NULL,
            authors TEXT,
            summary TEXT,
            pdf_url TEXT,
            published_date TEXT,
            added_date TEXT,
            is_favorite INTEGER DEFAULT 0,
            read_status INTEGER DEFAULT 0,
            ai_summary TEXT,
            UNIQUE(source, source_id)
        )
        ''')
        
        # Tags table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            color TEXT DEFAULT 'blue'
        )
        ''')
        
        # Paper Tags relation
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS paper_tags (
            paper_id INTEGER,
            tag_id INTEGER,
            FOREIGN KEY(paper_id) REFERENCES papers(id),
            FOREIGN KEY(tag_id) REFERENCES tags(id),
            PRIMARY KEY(paper_id, tag_id)
        )
        ''')
        
        # Notes table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paper_id INTEGER,
            content TEXT NOT NULL,
            created_at TEXT,
            updated_at TEXT,
            FOREIGN KEY(paper_id) REFERENCES papers(id)
        )
        ''')
        
        conn.commit()
        conn.close()

    def add_paper(self, paper_data: Dict[str, Any]) -> int:
        """Add a paper to the database. Returns paper ID."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        authors = json.dumps(paper_data.get('authors', []))
        added_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            cursor.execute('''
            INSERT INTO papers (source, source_id, title, authors, summary, pdf_url, published_date, added_date, ai_summary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(source, source_id) DO UPDATE SET
            title=excluded.title,
            authors=excluded.authors,
            summary=excluded.summary,
            pdf_url=excluded.pdf_url,
            ai_summary=COALESCE(excluded.ai_summary, papers.ai_summary)
            ''', (
                paper_data.get('source', 'arxiv'),
                paper_data.get('arxiv_id') or paper_data.get('id'), # Handle different ID keys
                paper_data.get('title'),
                authors,
                paper_data.get('summary'),
                paper_data.get('pdf_url'),
                paper_data.get('published'),
                added_date,
                paper_data.get('ai_summary')
            ))
            conn.commit()
            
            # Get the ID
            cursor.execute('SELECT id FROM papers WHERE source=? AND source_id=?', 
                          (paper_data.get('source', 'arxiv'), paper_data.get('arxiv_id') or paper_data.get('id')))
            paper_id = cursor.fetchone()[0]
            return paper_id
        except Exception as e:
            console.print(f"[red]Error adding paper: {e}[/red]")
            return -1
        finally:
            conn.close()

    def get_paper(self, paper_id: int) -> Optional[Dict]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM papers WHERE id = ?', (paper_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_dict(row)
        return None

    def get_all_papers(self, filter_favorite=False) -> List[Dict]:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM papers'
        if filter_favorite:
            query += ' WHERE is_favorite = 1'
        query += ' ORDER BY added_date DESC'
            
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row) for row in rows]

    def toggle_favorite(self, paper_id: int) -> bool:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT is_favorite FROM papers WHERE id = ?', (paper_id,))
        current = cursor.fetchone()
        if not current:
            return False
            
        new_status = 0 if current[0] else 1
        cursor.execute('UPDATE papers SET is_favorite = ? WHERE id = ?', (new_status, paper_id))
        conn.commit()
        conn.close()
        return bool(new_status)

    def add_tag(self, name: str, color: str = 'blue') -> int:
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO tags (name, color) VALUES (?, ?)', (name, color))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            cursor.execute('SELECT id FROM tags WHERE name = ?', (name,))
            return cursor.fetchone()[0]
        finally:
            conn.close()

    def tag_paper(self, paper_id: int, tag_name: str):
        tag_id = self.add_tag(tag_name)
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO paper_tags (paper_id, tag_id) VALUES (?, ?)', (paper_id, tag_id))
            conn.commit()
        except sqlite3.IntegrityError:
            pass # Already tagged
        finally:
            conn.close()

    def add_note(self, paper_id: int, content: str):
        conn = self._get_connection()
        cursor = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('INSERT INTO notes (paper_id, content, created_at, updated_at) VALUES (?, ?, ?, ?)',
                      (paper_id, content, now, now))
        conn.commit()
        conn.close()

    def get_paper_notes(self, paper_id: int) -> List[Dict]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM notes WHERE paper_id = ? ORDER BY created_at DESC', (paper_id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [{'id': r[0], 'content': r[2], 'created_at': r[3]} for r in rows]

    def _row_to_dict(self, row) -> Dict:
        # Helper to convert tuple to dict based on schema
        # id, source, source_id, title, authors, summary, pdf_url, published_date, added_date, is_favorite, read_status, ai_summary
        return {
            'id': row[0],
            'source': row[1],
            'source_id': row[2],
            'title': row[3],
            'authors': json.loads(row[4]) if row[4] else [],
            'summary': row[5],
            'pdf_url': row[6],
            'published': row[7],
            'added_date': row[8],
            'is_favorite': bool(row[9]),
            'read_status': bool(row[10]),
            'ai_summary': row[11]
        }
