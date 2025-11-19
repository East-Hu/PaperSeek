"""
交互式命令行界面
"""
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.layout import Layout
from rich.text import Text
from rich import box
import sys
from ..config import Config
from ..arxiv_crawler import ArxivCrawler
from ..llm_client import LLMClient
from ..storage import PaperStorage

console = Console()


class PaperRobotCLI:
    """Paper Robot 交互式命令行界面"""
    
    def __init__(self):
        """初始化 CLI"""
        self.config = Config()
        self.crawler = None
        self.llm_client = None
        self.storage = None
    
    def show_banner(self):
        """显示欢迎横幅"""
        robot_name = self.config.get("robot_name", "Paper Robot")
        
        banner_text = f"""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║           📚  {robot_name:^30}  📚           ║
║                                                           ║
║              自动化论文爬取与智能摘要工具                ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
        """
        
        console.print(Panel(
            banner_text,
            border_style="cyan",
            box=box.DOUBLE
        ))
    
    def show_menu(self) -> str:
        """显示主菜单并获取用户选择"""
        console.print("\n[bold cyan]请选择操作：[/bold cyan]\n")
        
        options = [
            ("1", "🔍 搜索论文", "search"),
            ("2", "⚙️  配置设置", "config"),
            ("3", "📂 查看已保存的论文", "history"),
            ("4", "🧪 测试 API 连接", "test"),
            ("5", "❌ 退出", "exit")
        ]
        
        table = Table(show_header=False, box=box.SIMPLE)
        table.add_column("选项", style="cyan", width=6)
        table.add_column("功能", style="green")
        
        for num, desc, _ in options:
            table.add_row(num, desc)
        
        console.print(table)
        
        choice = Prompt.ask("\n请输入选项", choices=[opt[0] for opt in options], default="1")
        
        # 返回对应的操作
        for num, _, action in options:
            if num == choice:
                return action
        
        return "exit"
    
    def configure_api(self):
        """配置 API 设置"""
        console.print("\n[bold cyan]⚙️  API 配置[/bold cyan]\n")
        
        # API Key
        current_key = self.config.get("api_key", "")
        if current_key:
            console.print(f"[yellow]当前 API Key: {current_key[:10]}...{current_key[-4:]}[/yellow]")
            if not Confirm.ask("是否更新 API Key?", default=False):
                api_key = current_key
            else:
                api_key = Prompt.ask("请输入新的 API Key")
        else:
            api_key = Prompt.ask("请输入 API Key")
        
        # Base URL
        current_url = self.config.get("base_url", "https://api.openai.com/v1")
        base_url = Prompt.ask("请输入 Base URL", default=current_url)
        
        # Model
        current_model = self.config.get("model", "gpt-4o-mini")
        model = Prompt.ask("请输入模型名称", default=current_model)
        
        # 保存配置
        self.config.set_api_config(api_key, base_url, model)
        
        console.print("\n[green]✓ API 配置已保存！[/green]")
    
    def configure_robot_name(self):
        """配置机器人名称"""
        console.print("\n[bold cyan]🤖 设置机器人名称[/bold cyan]\n")
        
        current_name = self.config.get("robot_name", "Paper Robot")
        console.print(f"当前名称: [yellow]{current_name}[/yellow]")
        
        new_name = Prompt.ask("请输入新名称", default=current_name)
        self.config.set_robot_name(new_name)
    
    def configure_settings(self):
        """配置菜单"""
        while True:
            console.print("\n[bold cyan]⚙️  配置菜单[/bold cyan]\n")
            
            options = [
                ("1", "设置 API 配置"),
                ("2", "设置机器人名称"),
                ("3", "查看当前配置"),
                ("4", "返回主菜单")
            ]
            
            for num, desc in options:
                console.print(f"  {num}. {desc}")
            
            choice = Prompt.ask("\n请选择", choices=[opt[0] for opt in options], default="4")
            
            if choice == "1":
                self.configure_api()
            elif choice == "2":
                self.configure_robot_name()
            elif choice == "3":
                self.config.display_config()
            elif choice == "4":
                break
    
    def search_papers(self):
        """搜索论文"""
        console.print("\n[bold cyan]🔍 搜索论文[/bold cyan]\n")
        
        # 检查 API 配置
        if not self.config.is_configured():
            console.print("[red]⚠ 请先配置 API！[/red]")
            if Confirm.ask("是否现在配置?", default=True):
                self.configure_api()
            else:
                return
        
        # 获取搜索参数
        keywords = Prompt.ask("请输入搜索关键词 (多个关键词用逗号分隔)")
        
        start_date = Prompt.ask("开始日期 (YYYY-MM-DD，留空表示不限)", default="")
        end_date = Prompt.ask("结束日期 (YYYY-MM-DD，留空表示不限)", default="")
        
        max_results = int(Prompt.ask("最大结果数", default=str(self.config.get("max_results", 20))))
        
        # 是否生成 AI 摘要
        generate_summary = Confirm.ask("是否生成 AI 摘要?", default=True)
        
        # 初始化爬虫
        self.crawler = ArxivCrawler(max_results=max_results)
        
        # 搜索论文
        console.print("\n")
        papers = self.crawler.search_papers(
            keywords=keywords,
            start_date=start_date if start_date else None,
            end_date=end_date if end_date else None
        )
        
        if not papers:
            console.print("[yellow]未找到相关论文[/yellow]")
            return
        
        # 生成 AI 摘要
        if generate_summary:
            self.llm_client = LLMClient(
                api_key=self.config.get("api_key"),
                base_url=self.config.get("base_url"),
                model=self.config.get("model")
            )
            
            papers = self.llm_client.batch_summarize(papers, language=self.config.get("language", "zh"))
        
        # 保存结果
        self.storage = PaperStorage(output_dir=str(self.config.get_output_dir()))
        
        save_format = Prompt.ask(
            "保存格式",
            choices=["json", "markdown", "both"],
            default="markdown"
        )
        
        if save_format in ["json", "both"]:
            self.storage.save_papers_json(papers)
        
        if save_format in ["markdown", "both"]:
            self.storage.save_papers_markdown(papers)
        
        console.print(f"\n[green]✓ 成功处理 {len(papers)} 篇论文！[/green]")
    
    def show_history(self):
        """显示已保存的论文文件"""
        console.print("\n[bold cyan]📂 已保存的文件[/bold cyan]\n")
        
        self.storage = PaperStorage(output_dir=str(self.config.get_output_dir()))
        files = self.storage.list_saved_files()
        
        if not files:
            console.print("[yellow]暂无已保存的文件[/yellow]")
            return
        
        table = Table(show_header=True)
        table.add_column("序号", style="cyan", width=6)
        table.add_column("文件名", style="green")
        
        for i, filename in enumerate(files, 1):
            table.add_row(str(i), filename)
        
        console.print(table)
    
    def test_api(self):
        """测试 API 连接"""
        console.print("\n[bold cyan]🧪 测试 API 连接[/bold cyan]\n")
        
        if not self.config.is_configured():
            console.print("[red]⚠ 请先配置 API！[/red]")
            return
        
        self.llm_client = LLMClient(
            api_key=self.config.get("api_key"),
            base_url=self.config.get("base_url"),
            model=self.config.get("model")
        )
        
        self.llm_client.test_connection()
    
    def run(self):
        """运行 CLI"""
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
                    console.print("\n[cyan]👋 再见！[/cyan]\n")
                    sys.exit(0)
                
            except KeyboardInterrupt:
                console.print("\n\n[yellow]操作已取消[/yellow]")
                if Confirm.ask("是否退出程序?", default=False):
                    console.print("\n[cyan]👋 再见！[/cyan]\n")
                    sys.exit(0)
            except Exception as e:
                console.print(f"\n[red]✗ 发生错误：{str(e)}[/red]")
                if Confirm.ask("是否继续?", default=True):
                    continue
                else:
                    sys.exit(1)


def main():
    """CLI 入口函数"""
    cli = PaperRobotCLI()
    cli.run()


if __name__ == "__main__":
    main()
