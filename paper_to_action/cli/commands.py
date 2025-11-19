"""
命令行命令处理模块
"""
import typer
from typing import Optional
from rich.console import Console
from ..config import Config
from ..arxiv_crawler import ArxivCrawler
from ..llm_client import LLMClient
from ..storage import PaperStorage

console = Console()
app = typer.Typer(help="Paper-to-Action: 自动化论文爬取与智能摘要工具")


@app.command()
def interactive():
    """启动交互式界面（默认模式）"""
    from .interface import PaperRobotCLI
    cli = PaperRobotCLI()
    cli.run()


@app.command()
def search(
    keywords: str = typer.Argument(..., help="搜索关键词"),
    start_date: Optional[str] = typer.Option(None, "--start-date", "-s", help="开始日期 (YYYY-MM-DD)"),
    end_date: Optional[str] = typer.Option(None, "--end-date", "-e", help="结束日期 (YYYY-MM-DD)"),
    max_results: int = typer.Option(20, "--max-results", "-n", help="最大结果数"),
    summarize: bool = typer.Option(True, "--summarize/--no-summarize", help="是否生成 AI 摘要"),
    output_format: str = typer.Option("markdown", "--format", "-f", help="输出格式 (json/markdown/both)")
):
    """直接搜索论文（非交互模式）"""
    config = Config()
    
    # 检查 API 配置
    if summarize and not config.is_configured():
        console.print("[red]⚠ 生成摘要需要先配置 API！请运行 'paper-robot config api' 配置[/red]")
        raise typer.Exit(1)
    
    # 搜索论文
    crawler = ArxivCrawler(max_results=max_results)
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
    
    console.print(f"\n[green]✓ 成功处理 {len(papers)} 篇论文！[/green]")


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
