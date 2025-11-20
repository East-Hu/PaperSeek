"""
配置管理模块
"""
import os
import yaml
import json
from pathlib import Path
from typing import Optional, Dict
from rich.console import Console

console = Console()


class Config:
    """配置管理类"""
    
    DEFAULT_CONFIG = {
        "robot_name": "Paper Robot",
        "api_key": "",
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4o-mini",
        "max_results": 20,
        "default_keywords": "",
        "language": "zh",
        "output_dir": "papers"
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化配置
        
        Args:
            config_path: 配置文件路径，默认为 ~/.paper_robot/config.yaml
        """
        if config_path is None:
            config_dir = Path.home() / ".paper_robot"
            config_dir.mkdir(exist_ok=True)
            config_path = str(config_dir / "config.yaml")
        
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """加载配置文件"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f) or {}
                
                # 合并默认配置
                merged_config = self.DEFAULT_CONFIG.copy()
                merged_config.update(config)
                
                return merged_config
            except Exception as e:
                console.print(f"[yellow]⚠ 加载配置文件失败，使用默认配置：{str(e)}[/yellow]")
                return self.DEFAULT_CONFIG.copy()
        else:
            # 首次使用，创建默认配置
            return self.DEFAULT_CONFIG.copy()
    
    def save_config(self):
        """保存配置到文件"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, allow_unicode=True, default_flow_style=False)
            
            console.print(f"[green]✓ 配置已保存到 {self.config_path}[/green]")
        except Exception as e:
            console.print(f"[red]✗ 保存配置失败：{str(e)}[/red]")
    
    def get(self, key: str, default=None):
        """获取配置项"""
        return self.config.get(key, default)
    
    def set(self, key: str, value):
        """设置配置项"""
        self.config[key] = value
    
    def set_robot_name(self, name: str):
        """设置机器人名称"""
        self.set("robot_name", name)
        self.save_config()
        console.print(f"[green]✓ 机器人名称已设置为：{name}[/green]")
    
    def set_api_config(self, api_key: str, base_url: Optional[str] = None, model: Optional[str] = None):
        """设置 API 配置"""
        self.set("api_key", api_key)
        
        if base_url:
            self.set("base_url", base_url)
        
        if model:
            self.set("model", model)
        
        self.save_config()
        console.print("[green]✓ API 配置已保存[/green]")
    
    def is_configured(self) -> bool:
        """检查是否已配置 API"""
        return bool(self.get("api_key"))
    
    def display_config(self):
        """显示当前配置"""
        from rich.table import Table
        
        table = Table(title="当前配置", show_header=True)
        table.add_column("配置项", style="cyan")
        table.add_column("值", style="green")
        
        for key, value in self.config.items():
            # 隐藏 API 密钥的部分内容
            if key == "api_key" and value:
                display_value = value[:10] + "..." + value[-4:] if len(value) > 14 else "***"
            else:
                display_value = str(value)
            
            table.add_row(key, display_value)
        
        console.print(table)
    
    def get_output_dir(self) -> Path:
        """获取输出目录路径"""
        output_dir = Path(self.get("output_dir", "papers"))
        output_dir.mkdir(exist_ok=True)
        return output_dir
    
    def set_language(self, language: str):
        """
        设置界面语言
        
        Args:
            language: 语言代码 ('zh' 或 'en')
        """
        if language in ["zh", "en"]:
            self.set("language", language)
            self.save_config()
            
            # Import i18n to show localized message
            from .i18n import get_text
            message = get_text("language_set", language)
            console.print(f"[green]✓ {message}[/green]")
        else:
            console.print(f"[red]✗ 不支持的语言: {language}[/red]")
    
    def get_language(self) -> str:
        """
        获取当前语言设置
        
        Returns:
            语言代码 ('zh' 或 'en')
        """
        return self.get("language", "zh")
