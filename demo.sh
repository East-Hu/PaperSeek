#!/bin/bash

# Paper-to-Action 快速演示脚本

echo "=========================================="
echo "📚 Paper-to-Action 演示"
echo "=========================================="
echo ""

# 激活虚拟环境
source xxx

echo "✓ 虚拟环境已激活"
echo ""

# 显示配置
echo "📋 当前配置："
paper-robot config show
echo ""

# 测试 API 连接
echo "🧪 测试 API 连接..."
paper-robot test
echo ""

# 示例搜索（小范围测试）
echo "🔍 示例搜索：搜索 'Retrieval Augmented Generation' 相关论文（最近3天，最多5篇）"
echo ""

# 计算日期
END_DATE=$(date +%Y-%m-%d)
START_DATE=$(date -v-3d +%Y-%m-%d)

echo "搜索时间范围：$START_DATE 到 $END_DATE"
echo ""

# 执行搜索
paper-robot search "Retrieval Augmented Generation" \
    --start-date "$START_DATE" \
    --end-date "$END_DATE" \
    --max-results 5 \
    --format markdown

echo ""
echo "=========================================="
echo "✓ 演示完成！"
echo "=========================================="
echo ""
echo "查看结果："
echo "  cd ~/papers"
echo "  ls -la"
echo ""
echo "启动交互式界面："
echo "  paper-robot"
echo ""
