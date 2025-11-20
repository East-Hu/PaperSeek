"""
自动配置脚本 - 设置 API 配置
"""
from paper_to_action.config import Config

# 创建配置实例
config = Config()

# 设置 API 配置
API_KEY = "YOUR-API-KEY"
BASE_URL = "YOUR-BASE-URL"

config.set_api_config(
    api_key=API_KEY,
    base_url=BASE_URL,
    model="gpt-4o-mini"
)

# 设置机器人名称
config.set_robot_name("Yourname PaperSeek Robot")

# 设置其他默认配置
config.set("max_results", 20)
config.set("language", "zh")

print("✓ API 配置完成！")
print("✓ 机器人名称已设置为: Yourname PaperSeek Robot")
print("\n现在可以使用以下命令启动工具：")
print("  paper-seek")
print("  或简写：pr")
