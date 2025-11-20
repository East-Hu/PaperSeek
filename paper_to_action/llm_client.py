"""
LLM 客户端模块 - 用于生成论文摘要和标签
"""
import openai
from typing import Dict, Optional, List
from rich.console import Console
import time

console = Console()


class LLMClient:
    """LLM 客户端类，用于调用 LLM API 生成论文摘要"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1", model: str = "gpt-4o-mini"):
        """
        初始化 LLM 客户端
        
        Args:
            api_key: API 密钥
            base_url: API 基础 URL
            model: 使用的模型名称
        """
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
    
    def summarize_paper(self, paper: Dict, language: str = "zh") -> str:
        """
        生成论文摘要
        
        Args:
            paper: 论文信息字典
            language: 摘要语言 (zh: 中文, en: 英文)
            
        Returns:
            生成的摘要文本
        """
        title = paper.get("title", "")
        abstract = paper.get("summary", "")
        
        # 构建 prompt
        if language == "zh":
            prompt = f"""请用中文总结以下论文的核心创新点，要求：
1. 简洁明了，控制在 200 字以内
2. 突出论文的主要贡献和创新之处
3. 使用学术但易懂的语言
4. 分点列出（如果有多个创新点）

论文标题：{title}

论文摘要：{abstract}

请开始总结："""
        else:
            prompt = f"""Please summarize the core innovations of the following paper:
1. Keep it concise (within 200 words)
2. Highlight main contributions and innovations
3. Use clear academic language
4. Use bullet points if there are multiple innovations

Paper Title: {title}

Abstract: {abstract}

Summary:"""
        
        try:
            console.print(f"[cyan]🤖 正在生成论文摘要：{title[:50]}...[/cyan]")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的学术论文分析助手，擅长提取论文的核心创新点。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            summary = response.choices[0].message.content.strip()
            console.print(f"[green]✓ 摘要生成完成[/green]")
            
            return summary
            
        except Exception as e:
            console.print(f"[red]✗ 生成摘要失败：{str(e)}[/red]")
            return f"摘要生成失败：{str(e)}"
    
    def batch_summarize(self, papers: list, language: str = "zh", delay: float = 1.0, progress_callback=None) -> list:
        """
        批量生成论文摘要
        
        Args:
            papers: 论文列表
            language: 摘要语言
            delay: 请求之间的延迟（秒），避免触发 API 限流
            progress_callback: 进度回调函数，接收 (current) 参数
            
        Returns:
            包含摘要的论文列表
        """
        console.print(f"[cyan]📝 开始批量生成 {len(papers)} 篇论文的摘要[/cyan]")
        
        for i, paper in enumerate(papers, 1):
            console.print(f"\n[yellow]进度：{i}/{len(papers)}[/yellow]")
            
            summary = self.summarize_paper(paper, language)
            paper["ai_summary"] = summary
            
            # 调用progress回调
            if progress_callback:
                progress_callback(i)
            
            # 延迟以避免 API 限流
            if i < len(papers):
                time.sleep(delay)
        
        console.print(f"\n[green]✓ 所有摘要生成完成！[/green]")
        return papers
    
    def generate_tags(self, paper: Dict, max_tags: int = 5) -> List[str]:
        """
        为论文生成标签/关键词
        
        Args:
            paper: 论文信息字典
            max_tags: 最大标签数量
            
        Returns:
            标签列表
        """
        title = paper.get("title", "")
        abstract = paper.get("summary", paper.get("abstract", ""))
        
        if not title and not abstract:
            return []
        
        # 构建 prompt
        prompt = f"""Based on the following academic paper, generate {max_tags} relevant tags/keywords that describe the main topics and methods.

Paper Title: {title}

Abstract: {abstract}

Please provide exactly {max_tags} tags, separated by commas. Tags should be:
- Specific and relevant
- Mix of broad topics and specific methods
- Useful for categorization

Tags:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at academic paper categorization."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=100
            )
            
            tags_text = response.choices[0].message.content.strip()
            # 解析标签
            tags = [tag.strip() for tag in tags_text.split(',')]
            tags = [tag for tag in tags if tag][:max_tags]
            
            return tags
            
        except Exception as e:
            console.print(f"[yellow]⚠ 标签生成失败: {str(e)}[/yellow]")
            return []
    
    def batch_generate_tags(
        self,
        papers: list,
        max_tags: int = 5,
        progress_callback=None
    ) -> list:
        """
        批量生成论文标签
        
        Args:
            papers: 论文列表
            max_tags: 每篇论文的最大标签数
            progress_callback: 进度回调
            
        Returns:
            包含标签的论文列表
        """
        console.print(f"[cyan]🏷️  开始生成论文标签...[/cyan]")
        
        for i, paper in enumerate(papers, 1):
            tags = self.generate_tags(paper, max_tags)
            paper['tags'] = tags
            
            if tags:
                console.print(f"[green]✓ {paper.get('title', '')[:40]}... | 标签: {', '.join(tags[:3])}{'...' if len(tags) > 3 else ''}[/green]")
            
            # 回调进度
            if progress_callback:
                progress_callback(i)
            
            # 延迟避免API限流
            if i < len(papers):
                time.sleep(0.5)
        
        console.print(f"[green]✓ 标签生成完成！[/green]")
        return papers
    
    def test_connection(self) -> bool:
        """
        测试 API 连接
        
        Returns:
            连接是否成功
        """
        try:
            console.print("[cyan]🔌 测试 API 连接...[/cyan]")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            
            console.print("[green]✓ API 连接成功！[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]✗ API 连接失败：{str(e)}[/red]")
            return False
