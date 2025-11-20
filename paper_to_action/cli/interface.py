"""
交互式命令行界面 - Enhanced with multi-language support and fancy UI
"""
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.layout import Layout
from rich.text import Text
from rich.align import Align
from rich import box
from rich.live import Live
import sys
import time
from ..config import Config
from ..arxiv_crawler import ArxivCrawler
from ..llm_client import LLMClient
from ..storage import PaperStorage
from ..i18n import get_i18n, set_language

console = Console()


class PaperRobotCLI:
    """Paper Robot 交互式命令行界面"""
    
    def __init__(self):
        """初始化 CLI"""
        self.config = Config()
        self.crawler = None
        self.llm_client = None
        self.storage = None
        
        # Initialize i18n with saved language preference
        language = self.config.get_language()
        set_language(language)
        self.i18n = get_i18n()
        
        # Check if this is first run (no language configured)
        if not self.config.get("language"):
            self.select_language()
    
    def select_language(self):
        """显示语言选择界面"""
        console.clear()
        
        # Fancy language selection banner
        banner = """
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║        📚  PAPER-TO-ACTION  📚                                 ║
║                                                                ║
║         Automated Paper Crawling & AI Summarization            ║
║         自动化论文爬取与智能摘要工具                             ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
        """
        
        console.print(Panel(
            Align.center(banner),
            border_style="bright_cyan",
            box=box.DOUBLE
        ))
        
        console.print()
        console.print(Align.center(
            "[bold bright_yellow]请选择语言 / Please Select Language[/bold bright_yellow]"
        ))
        console.print()
        
        # Language options table
        table = Table(show_header=False, box=box.ROUNDED, border_style="cyan")
        table.add_column("选项", style="bright_cyan bold", width=10, justify="center")
        table.add_column("语言", style="bright_green bold", width=30)
        
        table.add_row("1", "🇨🇳  中文 (Chinese)")
        table.add_row("2", "🇬🇧  English")
        
        console.print(Align.center(table))
        console.print()
        
        choice = Prompt.ask(
            "[bright_yellow]Enter your choice[/bright_yellow]",
            choices=["1", "2"],
            default="1"
        )
        
        language = "zh" if choice == "1" else "en"
        self.config.set_language(language)
        set_language(language)
        self.i18n.set_language(language)
        
        # Show loading animation
        self._show_loading_animation()
    
    def _show_loading_animation(self):
        """显示启动加载动画"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task(self.i18n.get("loading"), total=None)
            time.sleep(1.5)
    
    def show_banner(self):
        """显示欢迎横幅 - Enhanced version"""
        robot_name = self.config.get("robot_name", self.i18n.get("app_name"))
        
        # Create a fancy ASCII art banner
        if self.i18n.language == "zh":
            banner_art = f"""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║              📚  {robot_name:^36}  📚              ║
║                                                                   ║
║                   {self.i18n.get("app_subtitle"):^42}                   ║
║                                                                   ║
║  ┌─────────────────────────────────────────────────────────────┐  ║
║  │  🤖 AI-Powered  │  🔍 ArXiv Search  │  📝 Smart Summary  │  ║
║  └─────────────────────────────────────────────────────────────┘  ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
            """
        else:
            banner_art = f"""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║              📚  {robot_name:^36}  📚              ║
║                                                                   ║
║             {self.i18n.get("app_subtitle"):^50}             ║
║                                                                   ║
║  ┌─────────────────────────────────────────────────────────────┐  ║
║  │  🤖 AI-Powered  │  🔍 ArXiv Search  │  📝 Smart Summary  │  ║
║  └─────────────────────────────────────────────────────────────┘  ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
            """
        
        # Display with gradient colors
        gradient_colors = ["bright_cyan", "cyan", "blue"]
        lines = banner_art.strip().split('\n')
        
        for i, line in enumerate(lines):
            color = gradient_colors[i % len(gradient_colors)]
            console.print(f"[{color}]{line}[/{color}]")
        
        console.print()
    
    def show_menu(self) -> str:
        """显示主菜单并获取用户选择 - Enhanced version"""
        console.print(f"\n[bold bright_yellow]{self.i18n.get('main_menu')}[/bold bright_yellow]\n")
        
        options = [
            ("1", self.i18n.get("menu_search"), "search"),
            ("2", self.i18n.get("menu_config"), "config"),
            ("3", self.i18n.get("menu_history"), "history"),
            ("4", self.i18n.get("menu_test"), "test"),
            ("5", self.i18n.get("menu_exit"), "exit")
        ]
        
        # Create colorful menu table
        table = Table(
            show_header=True,
            box=box.ROUNDED,
            border_style="bright_cyan",
            header_style="bold bright_magenta"
        )
        table.add_column(self.i18n.get("option"), style="bright_cyan bold", width=8, justify="center")
        table.add_column(self.i18n.get("function"), style="bright_green")
        
        for num, desc, _ in options:
            table.add_row(num, desc)
        
        console.print(table)
        
        choice = Prompt.ask(
            f"\n[bright_yellow]{self.i18n.get('menu_prompt')}[/bright_yellow]",
            choices=[opt[0] for opt in options],
            default="1"
        )
        
        # Return corresponding action
        for num, _, action in options:
            if num == choice:
                return action
        
        return "exit"
    
    def configure_api(self):
        """配置 API 设置"""
        console.print(f"\n[bold bright_cyan]{self.i18n.get('config_api_title')}[/bold bright_cyan]\n")
        
        # API Key
        current_key = self.config.get("api_key", "")
        if current_key:
            console.print(f"[yellow]{self.i18n.get('config_api_key_current')}: {current_key[:10]}...{current_key[-4:]}[/yellow]")
            if not Confirm.ask(self.i18n.get("config_api_key_update"), default=False):
                api_key = current_key
            else:
                api_key = Prompt.ask(self.i18n.get("config_api_key"))
        else:
            api_key = Prompt.ask(self.i18n.get("config_api_key"))
        
        # Base URL
        current_url = self.config.get("base_url", "https://api.openai.com/v1")
        base_url = Prompt.ask(self.i18n.get("config_base_url"), default=current_url)
        
        # Model
        current_model = self.config.get("model", "gpt-4o-mini")
        model = Prompt.ask(self.i18n.get("config_model"), default=current_model)
        
        # Save configuration
        self.config.set_api_config(api_key, base_url, model)
        
        console.print(f"\n[green]✓ {self.i18n.get('config_saved')}[/green]")
    
    def configure_robot_name(self):
        """配置机器人名称"""
        console.print(f"\n[bold bright_cyan]{self.i18n.get('config_robot_title')}[/bold bright_cyan]\n")
        
        current_name = self.config.get("robot_name", "Paper Robot")
        console.print(f"{self.i18n.get('config_robot_current')}: [yellow]{current_name}[/yellow]")
        
        new_name = Prompt.ask(self.i18n.get("config_robot_new"), default=current_name)
        self.config.set_robot_name(new_name)
        
        console.print(f"\n[green]✓ {self.i18n.get('config_robot_saved', name=new_name)}[/green]")
    
    def configure_language(self):
        """配置语言"""
        self.select_language()
    
    def configure_settings(self):
        """配置菜单"""
        while True:
            console.print(f"\n[bold bright_cyan]{self.i18n.get('config_title')}[/bold bright_cyan]\n")
            
            options = [
                ("1", self.i18n.get("config_api")),
                ("2", self.i18n.get("config_robot_name")),
                ("3", self.i18n.get("config_language")),
                ("4", self.i18n.get("config_show")),
                ("5", self.i18n.get("config_back"))
            ]
            
            table = Table(show_header=False, box=box.ROUNDED, border_style="cyan")
            table.add_column("", style="bright_cyan bold", width=8)
            table.add_column("", style="bright_green")
            
            for num, desc in options:
                table.add_row(num, desc)
            
            console.print(table)
            
            choice = Prompt.ask(f"\n{self.i18n.get('please_select')}", choices=[opt[0] for opt in options], default="5")
            
            if choice == "1":
                self.configure_api()
            elif choice == "2":
                self.configure_robot_name()
            elif choice == "3":
                self.configure_language()
            elif choice == "4":
                self.config.display_config()
            elif choice == "5":
                break
    
    def search_papers(self):
        """搜索论文 - Enhanced with progress indicators"""
        console.print(f"\n[bold bright_cyan]{self.i18n.get('search_title')}[/bold bright_cyan]\n")
        
        # Check API configuration
        if not self.config.is_configured():
            console.print(f"[red]{self.i18n.get('test_not_configured')}[/red]")
            if Confirm.ask(self.i18n.get("test_now"), default=True):
                self.configure_api()
            else:
                return
        
        # Get search parameters
        keywords = Prompt.ask(self.i18n.get("search_keywords"))
        
        start_date = Prompt.ask(self.i18n.get("search_start_date"), default="")
        end_date = Prompt.ask(self.i18n.get("search_end_date"), default="")
        
        max_results = int(Prompt.ask(
            self.i18n.get("search_max_results"),
            default=str(self.config.get("max_results", 20))
        ))
        
        # Whether to generate AI summary
        generate_summary = Confirm.ask(self.i18n.get("search_generate_summary"), default=True)
        
        # Initialize crawler
        self.crawler = ArxivCrawler(max_results=max_results)
        
        # Search papers with progress
        console.print()
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
        ) as progress:
            task = progress.add_task(f"[cyan]{self.i18n.get('searching')}", total=100)
            
            papers = self.crawler.search_papers(
                keywords=keywords,
                start_date=start_date if start_date else None,
                end_date=end_date if end_date else None
            )
            
            progress.update(task, completed=100)
        
        if not papers:
            console.print(f"[yellow]{self.i18n.get('search_no_results')}[/yellow]")
            return
        
        # Show papers found
        console.print(f"\n[bright_green]✓ Found {len(papers)} papers![/bright_green]\n")
        
        # Display preview of papers
        self._display_paper_preview(papers[:3])  # Show first 3
        
        # Generate AI summary
        if generate_summary:
            self.llm_client = LLMClient(
                api_key=self.config.get("api_key"),
                base_url=self.config.get("base_url"),
                model=self.config.get("model")
            )
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
            ) as progress:
                task = progress.add_task(
                    f"[cyan]{self.i18n.get('generating_summary')}",
                    total=len(papers)
                )
                
                papers = self.llm_client.batch_summarize(
                    papers,
                    language=self.config.get("language", "zh")
                )
        
        # Save results
        self.storage = PaperStorage(output_dir=str(self.config.get_output_dir()))
        
        save_format = Prompt.ask(
            self.i18n.get("search_format"),
            choices=["json", "markdown", "both"],
            default="markdown"
        )
        
        if save_format in ["json", "both"]:
            self.storage.save_papers_json(papers)
        
        if save_format in ["markdown", "both"]:
            self.storage.save_papers_markdown(papers)
        
        console.print(f"\n[bright_green]{self.i18n.get('search_success', count=len(papers))}[/bright_green]")
    
    def _display_paper_preview(self, papers):
        """显示论文预览卡片"""
        for i, paper in enumerate(papers, 1):
            authors = ", ".join(paper.get("authors", [])[:2])
            if len(paper.get("authors", [])) > 2:
                authors += " et al."
            
            paper_info = f"""[bold bright_cyan]{i}. {paper.get('title', 'N/A')}[/bold bright_cyan]

[dim]👤 Authors:[/dim] {authors}
[dim]📅 Published:[/dim] {paper.get('published', 'N/A')}
[dim]📄 ArXiv ID:[/dim] {paper.get('arxiv_id', 'N/A')}
            """
            
            console.print(Panel(
                paper_info.strip(),
                border_style="bright_blue",
                box=box.ROUNDED
            ))
            console.print()
    
    def show_history(self):
        """显示已保存的论文文件"""
        console.print(f"\n[bold bright_cyan]{self.i18n.get('history_title')}[/bold bright_cyan]\n")
        
        self.storage = PaperStorage(output_dir=str(self.config.get_output_dir()))
        files = self.storage.list_saved_files()
        
        if not files:
            console.print(f"[yellow]{self.i18n.get('history_no_files')}[/yellow]")
            return
        
        table = Table(show_header=True, box=box.ROUNDED, border_style="bright_cyan")
        table.add_column(self.i18n.get("history_column_num"), style="bright_cyan", width=8)
        table.add_column(self.i18n.get("history_column_file"), style="bright_green")
        
        for i, filename in enumerate(files, 1):
            table.add_row(str(i), filename)
        
        console.print(table)
    
    def test_api(self):
        """测试 API 连接"""
        console.print(f"\n[bold bright_cyan]{self.i18n.get('test_title')}[/bold bright_cyan]\n")
        
        if not self.config.is_configured():
            console.print(f"[red]{self.i18n.get('test_not_configured')}[/red]")
            return
        
        self.llm_client = LLMClient(
            api_key=self.config.get("api_key"),
            base_url=self.config.get("base_url"),
            model=self.config.get("model")
        )
        
        # Test with progress indicator
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task("[cyan]Testing API connection...", total=None)
            time.sleep(0.5)  # Small delay for visual effect
            self.llm_client.test_connection()
    
    def run(self):
        """运行 CLI"""
        console.clear()
        self.show_banner()
        
        while True:
            try:
                action = self.show_menu()
                
                if action == "search":
                    self.search_papers()
                elif action == "config":
                    self.configure_settings()
                elif action == "history":
                    self.show_history()
                elif action == "test":
                    self.test_api()
                elif action == "exit":
                    console.print(f"\n[bright_cyan]👋 {self.i18n.get('goodbye')}[/bright_cyan]\n")
                    sys.exit(0)
                
            except KeyboardInterrupt:
                console.print(f"\n\n[yellow]{self.i18n.get('operation_cancelled')}[/yellow]")
                if Confirm.ask(self.i18n.get("exit_confirm"), default=False):
                    console.print(f"\n[bright_cyan]👋 {self.i18n.get('goodbye')}[/bright_cyan]\n")
                    sys.exit(0)
            except Exception as e:
                console.print(f"\n[red]{self.i18n.get('error_occurred', error=str(e))}[/red]")
                if Confirm.ask(self.i18n.get("continue"), default=True):
                    continue
                else:
                    sys.exit(1)


def main():
    """CLI 入口函数"""
    cli = PaperRobotCLI()
    cli.run()


if __name__ == "__main__":
    main()
