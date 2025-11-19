"""
自动配置脚本 - 设置 API 配置
"""
from paper_to_action.config import Config

# 创建配置实例
config = Config()

# 设置 API 配置
API_KEY = "***REMOVED***"
BASE_URL = "https://api.openai.com/v1"

config.set_api_config(
    api_key=API_KEY,
    base_url=BASE_URL,
    model="gpt-4o-mini"
)

# 设置机器人名称
config.set_robot_name("East's Paper Robot")

# 设置其他默认配置
config.set("max_results", 20)
config.set("language", "zh")

print("✓ API 配置完成！")
print("✓ 机器人名称已设置为: East's Paper Robot")
print("\n现在可以使用以下命令启动工具：")
print("  paper-robot")
print("  或简写：pr")
