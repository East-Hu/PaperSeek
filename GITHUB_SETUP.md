# GitHub 仓库设置说明

## 步骤 1: 在 GitHub 上创建仓库

1. 访问 https://github.com/new
2. 仓库名称: `paper-to-action`
3. 描述: `全自动论文速递机器人 - CLI 工具 + VSCode 插件`
4. 选择 Public（公开）
5. **不要**勾选 "Initialize this repository with a README"
6. 点击 "Create repository"

## 步骤 2: 推送代码到 GitHub

在终端中运行：

```bash
cd /Users/east/AntiGravity_projects/paper_robot

# 推送代码
git push -u origin main
```

## 步骤 3: 配置 GitHub Secrets（如需使用 Actions）

1. 进入仓库设置: Settings > Secrets and variables > Actions
2. 添加以下 secrets:
   - `API_KEY`: 你的 LLM API 密钥
   - `BASE_URL`: 你的 API Base URL

## 步骤 4: 启用 GitHub Actions

1. 进入仓库的 Actions 标签
2. 如果看到提示，点击 "I understand my workflows, go ahead and enable them"

完成！现在你的论文机器人仓库已经在 GitHub 上了。
