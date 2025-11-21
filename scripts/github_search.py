#!/usr/bin/env python3
"""
Non-interactive script for GitHub Actions
Directly uses the crawler API without interactive prompts
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from paper_to_action.crawler import ArxivCrawler
from paper_to_action.llm_client import LLMClient
from paper_to_action.storage import PaperStorage
from paper_to_action.config import Config
from rich.console import Console

console = Console()

def main():
    """Run search in non-interactive mode"""
    # Get parameters from command line or environment
    keywords = sys.argv[1] if len(sys.argv) > 1 else os.getenv('KEYWORDS', 'AI Security')
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else int(os.getenv('MAX_RESULTS', '20'))
    
    console.print(f"[cyan]🔍 Searching for: {keywords}[/cyan]")
    console.print(f"[cyan]📊 Max results: {max_results}[/cyan]")
    
    try:
        # Initialize components
        config = Config()
        crawler = ArxivCrawler(max_results=max_results)
        
        # Search papers
        papers = crawler.search_papers(keywords)
        
        if not papers:
            console.print("[yellow]⚠️  No papers found[/yellow]")
            return
        
        console.print(f"[green]✓ Found {len(papers)} papers[/green]")
        
        # Initialize LLM client if API key is available
        api_key = config.get('api_key')
        if api_key:
            console.print("[cyan]🤖 Generating summaries with LLM...[/cyan]")
            llm_client = LLMClient(
                api_key=api_key,
                base_url=config.get('base_url', 'https://api.openai.com/v1'),
                model=config.get('model', 'gpt-4o-mini')
            )
            
            # Add summaries to papers
            for paper in papers:
                try:
                    summary = llm_client.summarize_paper(paper)
                    paper['ai_summary'] = summary
                    console.print(f"[green]✓ Summarized: {paper['title'][:50]}...[/green]")
                except Exception as e:
                    console.print(f"[yellow]⚠️  Failed to summarize: {e}[/yellow]")
                    paper['ai_summary'] = None
        else:
            console.print("[yellow]⚠️  No API key found, skipping LLM summaries[/yellow]")
        
        # Save papers
        output_dir = config.get('output_dir', 'papers')
        storage = PaperStorage(output_dir)
        
        # Save as markdown
        md_file = storage.save_papers_markdown(papers, keywords)
        console.print(f"[green]✓ Saved to: {md_file}[/green]")
        
        # Save as JSON
        json_file = storage.save_papers_json(papers, keywords)
        console.print(f"[green]✓ Saved to: {json_file}[/green]")
        
        console.print("[bold green]🎉 Done![/bold green]")
        
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
