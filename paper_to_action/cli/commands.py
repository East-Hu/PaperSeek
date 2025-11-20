"""
命令行命令处理模块
"""
import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from ..config import Config
from ..crawler import ArxivCrawler, SemanticScholarCrawler
from ..llm_client import LLMClient
from ..storage import PaperStorage
from ..database import Database

console = Console()
app = typer.Typer(help="Paper-to-Action: 自动化论文爬取与智能摘要工具")


@app.command()
def interactive():
    """启动交互式界面（默认模式）"""
    from .interface import PaperSeekCLI
    cli = PaperSeekCLI()
    cli.run()


@app.command()
def search(
    keywords: str = typer.Argument(..., help="搜索关键词"),
    source: str = typer.Option("arxiv", "--source", "-src", help="数据源 (arxiv/semantic_scholar)"),
    start_date: Optional[str] = typer.Option(None, "--start-date", "-s", help="开始日期 (YYYY-MM-DD)"),
    end_date: Optional[str] = typer.Option(None, "--end-date", "-e", help="结束日期 (YYYY-MM-DD)"),
    max_results: int = typer.Option(20, "--max-results", "-n", help="最大结果数"),
    summarize: bool = typer.Option(True, "--summarize/--no-summarize", help="是否生成 AI 摘要"),
    output_format: str = typer.Option("markdown", "--format", "-f", help="输出格式 (json/markdown/both)"),
    save_db: bool = typer.Option(True, "--save-db/--no-save-db", help="是否保存到数据库")
):
    """直接搜索论文（非交互模式）"""
    config = Config()
    
    # 检查 API 配置
    if summarize and not config.is_configured():
        console.print("[red]⚠ 生成摘要需要先配置 API！请运行 'paper-seek config api' 配置[/red]")
        raise typer.Exit(1)
    
    # 选择爬虫
    if source.lower() == "arxiv":
        crawler = ArxivCrawler(max_results=max_results)
    elif source.lower() == "semantic_scholar":
        crawler = SemanticScholarCrawler(max_results=max_results)
    else:
        console.print(f"[red]未知数据源: {source}[/red]")
        raise typer.Exit(1)

    # 搜索论文
    papers = crawler.search_papers(
        keywords=keywords,
        start_date=start_date,
        end_date=end_date
    )
    
    if not papers:
        console.print("[yellow]未找到相关论文[/yellow]")
        raise typer.Exit(0)
    
    # 生成摘要
    if summarize:
        llm_client = LLMClient(
            api_key=config.get("api_key"),
            base_url=config.get("base_url"),
            model=config.get("model")
        )
        papers = llm_client.batch_summarize(papers)
    
    # 保存结果
    storage = PaperStorage(output_dir=str(config.get_output_dir()))
    
    if output_format in ["json", "both"]:
        storage.save_papers_json(papers)
    
    if output_format in ["markdown", "both"]:
        storage.save_papers_markdown(papers)

    # 保存到数据库
    if save_db:
        db = Database()
        count = 0
        for paper in papers:
            if db.add_paper(paper) != -1:
                count += 1
        console.print(f"[green]✓ 已保存 {count} 篇论文到数据库[/green]")
    
    console.print(f"\n[green]✓ 成功处理 {len(papers)} 篇论文！[/green]")


@app.command()
def list(
    favorite: bool = typer.Option(False, "--favorite", "-fav", help="只显示收藏的论文"),
    limit: int = typer.Option(20, "--limit", "-l", help="显示数量限制")
):
    """列出数据库中的论文"""
    db = Database()
    papers = db.get_all_papers(filter_favorite=favorite)
    
    if not papers:
        console.print("[yellow]数据库中没有论文[/yellow]")
        return

    table = Table(title="已保存的论文")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("标题", style="magenta")
    table.add_column("作者", style="green")
    table.add_column("日期", style="blue")
    table.add_column("收藏", justify="center")

    for paper in papers[:limit]:
        fav_icon = "⭐" if paper['is_favorite'] else ""
        authors = ", ".join(paper['authors'][:2]) + ("..." if len(paper['authors']) > 2 else "")
        table.add_row(str(paper['id']), paper['title'], authors, paper['published'], fav_icon)

    console.print(table)


@app.command()
def fav(paper_id: int = typer.Argument(..., help="论文 ID")):
    """切换论文收藏状态"""
    db = Database()
    is_fav = db.toggle_favorite(paper_id)
    status = "已收藏" if is_fav else "已取消收藏"
    console.print(f"[green]论文 {paper_id} {status}[/green]")


@app.command()
def tag(
    paper_id: int = typer.Argument(..., help="论文 ID"),
    tag_name: str = typer.Argument(..., help="标签名称")
):
    """给论文添加标签"""
    db = Database()
    db.tag_paper(paper_id, tag_name)
    console.print(f"[green]已给论文 {paper_id} 添加标签: {tag_name}[/green]")


@app.command()
def note(
    paper_id: int = typer.Argument(..., help="论文 ID"),
    content: str = typer.Argument(..., help="笔记内容")
):
    """给论文添加笔记"""
    db = Database()
    db.add_note(paper_id, content)
    console.print(f"[green]已给论文 {paper_id} 添加笔记[/green]")


@app.command()
def export(
    format: str = typer.Option("bibtex", "--format", "-f", help="导出格式 (bibtex/apa/mla/ieee)"),
    paper_id: Optional[int] = typer.Option(None, "--id", help="指定论文 ID，不指定则导出所有")
):
    """导出论文引用"""
    db = Database()
    if paper_id:
        paper = db.get_paper(paper_id)
        if not paper:
            console.print(f"[red]未找到论文 {paper_id}[/red]")
            return
        papers = [paper]
    else:
        papers = db.get_all_papers()
    
    if not papers:
        console.print("[yellow]没有可导出的论文[/yellow]")
        return

    from ..export.citation import CitationExporter
    
    # 转换为 Paper 对象列表
    from ..sources.base import Paper
    paper_objs = []
    for p in papers:
        # 简单的字典转对象
        paper_obj = Paper(
            title=p['title'],
            authors=p['authors'],
            abstract=p.get('abstract', ''),
            published=p.get('published', ''),
            source=p.get('source', 'arxiv'),
            source_id=p.get('source_id', str(p['id'])),
            url=p.get('url'),
            pdf_url=p.get('pdf_url')
        )
        paper_objs.append(paper_obj)

    output_dir = Config().get_output_dir() / "citations"
    CitationExporter.export_all_formats(paper_objs, str(output_dir))
    
    console.print(f"[green]✓ 引用已导出到 {output_dir}[/green]")


@app.command()
def config(
    action: str = typer.Argument("show", help="操作: show/set"),
    key: Optional[str] = typer.Option(None, "--key", "-k", help="配置项名称"),
    value: Optional[str] = typer.Option(None, "--value", "-v", help="配置项值")
):
    """管理配置"""
    cfg = Config()
    
    if action == "show":
        cfg.display_config()
    elif action == "set":
        if not key:
            console.print("[red]请指定配置项名称 (--key)[/red]")
            raise typer.Exit(1)
        if not value:
            console.print("[red]请指定配置项值 (--value)[/red]")
            raise typer.Exit(1)
        
        cfg.set(key, value)
        cfg.save_config()
    else:
        console.print(f"[red]未知操作: {action}[/red]")
        raise typer.Exit(1)


@app.command()
def rename(name: str = typer.Argument(..., help="新的机器人名称")):
    """重命名机器人"""
    cfg = Config()
    cfg.set_robot_name(name)


@app.command()
def test():
    """测试 API 连接"""
    cfg = Config()
    
    if not cfg.is_configured():
        console.print("[red]⚠ 请先配置 API！[/red]")
        raise typer.Exit(1)
    
    llm_client = LLMClient(
        api_key=cfg.get("api_key"),
        base_url=cfg.get("base_url"),
        model=cfg.get("model")
    )
    
    if llm_client.test_connection():
        raise typer.Exit(0)
    else:
        raise typer.Exit(1)


@app.command()
def version():
    """显示版本信息"""
    from .. import __version__, __author__
    console.print(f"[cyan]Paper-to-Action v{__version__}[/cyan]")
    console.print(f"[green]作者: {__author__}[/green]")


if __name__ == "__main__":
    app()
