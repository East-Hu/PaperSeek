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
    enable_ai_summary = (sys.argv[3] if len(sys.argv) > 3 else os.getenv('ENABLE_AI_SUMMARY', 'true')).lower() == 'true'
    enable_tagging = (sys.argv[4] if len(sys.argv) > 4 else os.getenv('ENABLE_TAGGING', 'true')).lower() == 'true'
    download_pdf = (sys.argv[5] if len(sys.argv) > 5 else os.getenv('DOWNLOAD_PDF', 'false')).lower() == 'true'
    
    console.print(f"[cyan]🔍 搜索关键词: {keywords}[/cyan]")
    console.print(f"[cyan]📊 最大结果数: {max_results}[/cyan]")
    console.print(f"[cyan]🤖 AI摘要: {'✅ 开启' if enable_ai_summary else '❌ 关闭'}[/cyan]")
    console.print(f"[cyan]🏷️  自动标签: {'✅ 开启' if enable_tagging else '❌ 关闭'}[/cyan]")
    console.print(f"[cyan]📄 下载PDF: {'✅ 开启' if download_pdf else '❌ 关闭'}[/cyan]")
    
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
        
        # Generate AI summaries if enabled
        if enable_ai_summary:
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
        else:
            console.print("[yellow]ℹ️  AI summary disabled by user[/yellow]")
        
        # Add tags if enabled
        if enable_tagging:
            console.print("[cyan]🏷️  Auto-tagging papers...[/cyan]")
            for paper in papers:
                # Auto-generate tags from categories and keywords
                tags = []
                if 'categories' in paper and paper['categories']:
                    tags.extend(paper['categories'][:3])  # Top 3 categories
                if 'primary_category' in paper:
                    tags.append(paper['primary_category'])
                # Add keyword as tag
                tags.append(keywords.split()[0] if ' ' in keywords else keywords)
                paper['tags'] = list(set(tags))  # Remove duplicates
                console.print(f"[green]✓ Tagged: {paper['title'][:40]}... with {len(paper['tags'])} tags[/green]")
        else:
            console.print("[yellow]ℹ️  Auto-tagging disabled by user[/yellow]")
        
        # Download PDFs if enabled (placeholder for future implementation)
        if download_pdf:
            console.print("[yellow]ℹ️  PDF download feature coming soon...[/yellow]")
            # TODO: Implement PDF download functionality
            # for paper in papers:
            #     download_paper_pdf(paper['pdf_url'], output_dir)
        
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
