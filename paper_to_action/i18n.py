"""
Internationalization (i18n) module for Paper-to-Action
Provides multi-language support for CLI interface
"""
from typing import Dict, Any

# Language text resources
TEXTS = {
    "zh": {
        # Banner and welcome
        "app_name": "Paper Robot",
        "app_subtitle": "自动化论文爬取与智能摘要工具",
        "welcome": "欢迎使用 Paper-to-Action",
        "goodbye": "再见！",
        
        # Language selection
        "select_language": "请选择语言 / Please Select Language",
        "language_chinese": "中文",
        "language_english": "English", 
        "language_set": "语言已设置为中文",
        
        # Main menu
        "main_menu": "请选择操作：",
        "menu_search": "🔍 搜索论文",
        "menu_config": "⚙️  配置设置",
        "menu_history": "📂 查看已保存的论文",
        "menu_test": "🧪 测试 API 连接",
        "menu_exit": "❌ 退出",
        "menu_prompt": "请输入选项",
        
        # Search
        "search_title": "🔍 搜索论文",
        "search_keywords": "请输入搜索关键词 (多个关键词用逗号分隔)",
        "search_start_date": "开始日期 (YYYY-MM-DD，留空表示不限)",
        "search_end_date": "结束日期 (YYYY-MM-DD，留空表示不限)",
        "search_max_results": "最大结果数",
        "search_generate_summary": "是否生成 AI 摘要?",
        "search_no_results": "未找到相关论文",
        "search_success": "✓ 成功处理 {count} 篇论文！",
        "search_format": "保存格式",
        "searching": "正在搜索论文...",
        "generating_summary": "正在生成 AI 摘要...",
        
        # Configuration
        "config_title": "⚙️  配置菜单",
        "config_api": "设置 API 配置",
        "config_robot_name": "设置机器人名称",
        "config_language": "设置语言",
        "config_show": "查看当前配置",
        "config_back": "返回主菜单",
        "config_api_title": "⚙️  API 配置",
        "config_api_key": "请输入 API Key",
        "config_api_key_current": "当前 API Key",
        "config_api_key_update": "是否更新 API Key?",
        "config_base_url": "请输入 Base URL",
        "config_model": "请输入模型名称",
        "config_saved": "✓ API 配置已保存！",
        "config_robot_title": "🤖 设置机器人名称",
        "config_robot_current": "当前名称",
        "config_robot_new": "请输入新名称",
        "config_robot_saved": "✓ 机器人名称已设置为：{name}",
        "current_config": "当前配置",
        
        # API Test
        "test_title": "🧪 测试 API 连接",
        "test_not_configured": "⚠ 请先配置 API！",
        "test_now": "是否现在配置?",
        "test_success": "✓ API 连接成功！",
        "test_failed": "✗ API 连接失败：{error}",
        
        # History
        "history_title": "📂 已保存的文件",
        "history_no_files": "暂无已保存的文件",
        "history_column_num": "序号",
        "history_column_file": "文件名",
        
        # Common
        "yes": "是",
        "no": "否",
        "continue": "是否继续?",
        "exit_confirm": "是否退出程序?",
        "operation_cancelled": "操作已取消",
        "error_occurred": "✗ 发生错误：{error}",
        "please_select": "请选择",
        "option": "选项",
        "function": "功能",
        
        # Status messages
        "loading": "加载中...",
        "processing": "处理中...",
        "done": "完成",
        "failed": "失败",
    },
    
    "en": {
        # Banner and welcome
        "app_name": "Paper Robot",
        "app_subtitle": "Automated Paper Crawling & AI Summarization Tool",
        "welcome": "Welcome to Paper-to-Action",
        "goodbye": "Goodbye!",
        
        # Language selection
        "select_language": "请选择语言 / Please Select Language",
        "language_chinese": "中文",
        "language_english": "English",
        "language_set": "Language set to English",
        
        # Main menu
        "main_menu": "Please select an option:",
        "menu_search": "🔍 Search Papers",
        "menu_config": "⚙️  Settings",
        "menu_history": "📂 View Saved Papers",
        "menu_test": "🧪 Test API Connection",
        "menu_exit": "❌ Exit",
        "menu_prompt": "Enter your choice",
        
        # Search
        "search_title": "🔍 Search Papers",
        "search_keywords": "Enter search keywords (separate multiple keywords with commas)",
        "search_start_date": "Start date (YYYY-MM-DD, leave blank for no limit)",
        "search_end_date": "End date (YYYY-MM-DD, leave blank for no limit)",
        "search_max_results": "Maximum number of results",
        "search_generate_summary": "Generate AI summary?",
        "search_no_results": "No papers found",
        "search_success": "✓ Successfully processed {count} papers!",
        "search_format": "Save format",
        "searching": "Searching for papers...",
        "generating_summary": "Generating AI summaries...",
        
        # Configuration
        "config_title": "⚙️  Settings Menu",
        "config_api": "Configure API",
        "config_robot_name": "Set Robot Name",
        "config_language": "Set Language",
        "config_show": "Show Current Configuration",
        "config_back": "Back to Main Menu",
        "config_api_title": "⚙️  API Configuration",
        "config_api_key": "Enter API Key",
        "config_api_key_current": "Current API Key",
        "config_api_key_update": "Update API Key?",
        "config_base_url": "Enter Base URL",
        "config_model": "Enter model name",
        "config_saved": "✓ API configuration saved!",
        "config_robot_title": "🤖 Set Robot Name",
        "config_robot_current": "Current name",
        "config_robot_new": "Enter new name",
        "config_robot_saved": "✓ Robot name set to: {name}",
        "current_config": "Current Configuration",
        
        # API Test
        "test_title": "🧪 Test API Connection",
        "test_not_configured": "⚠ Please configure API first!",
        "test_now": "Configure now?",
        "test_success": "✓ API connection successful!",
        "test_failed": "✗ API connection failed: {error}",
        
        # History
        "history_title": "📂 Saved Files",
        "history_no_files": "No saved files yet",
        "history_column_num": "No.",
        "history_column_file": "Filename",
        
        # Common
        "yes": "Yes",
        "no": "No",
        "continue": "Continue?",
        "exit_confirm": "Exit program?",
        "operation_cancelled": "Operation cancelled",
        "error_occurred": "✗ Error occurred: {error}",
        "please_select": "Please select",
        "option": "Option",
        "function": "Function",
        
        # Status messages
        "loading": "Loading...",
        "processing": "Processing...",
        "done": "Done",
        "failed": "Failed",
    }
}


class I18n:
    """Internationalization helper class"""
    
    def __init__(self, language: str = "zh"):
        """
        Initialize i18n
        
        Args:
            language: Language code ('zh' or 'en')
        """
        self.language = language if language in TEXTS else "zh"
    
    def set_language(self, language: str):
        """Set current language"""
        if language in TEXTS:
            self.language = language
    
    def get(self, key: str, **kwargs) -> str:
        """
        Get localized text
        
        Args:
            key: Text key
            **kwargs: Format parameters
            
        Returns:
            Localized text string
        """
        text = TEXTS.get(self.language, {}).get(key, key)
        
        # Format with parameters if provided
        if kwargs:
            try:
                text = text.format(**kwargs)
            except KeyError:
                pass
        
        return text
    
    def __call__(self, key: str, **kwargs) -> str:
        """Shorthand for get()"""
        return self.get(key, **kwargs)


# Global i18n instance
_i18n = I18n()


def get_text(key: str, language: str = None, **kwargs) -> str:
    """
    Get localized text (convenience function)
    
    Args:
        key: Text key
        language: Language code (optional, uses current language if not provided)
        **kwargs: Format parameters
        
    Returns:
        Localized text string
    """
    if language:
        temp_i18n = I18n(language)
        return temp_i18n.get(key, **kwargs)
    else:
        return _i18n.get(key, **kwargs)


def set_language(language: str):
    """Set global language"""
    _i18n.set_language(language)


def get_i18n() -> I18n:
    """Get global i18n instance"""
    return _i18n
