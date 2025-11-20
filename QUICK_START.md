# 🚀 快速发布指南

## 第一步：创建并推送到 GitHub

### 1. 在 GitHub 上创建仓库

访问：https://github.com/new

配置：
- **Repository name**: `paper-to-action`
- **Description**: `📚 Automated academic paper delivery robot with AI summarization | 全自动论文速递机器人`
- **Public**: ✅
- **不要勾选任何初始化选项**（README, .gitignore, license）

点击 "Create repository"

### 2. 推送代码

```bash
cd /Users/east/AntiGravity_projects/paper_robot
git push -u origin main
```

✅ 完成后，访问 https://github.com/East-Hu/paper-to-action 查看您的项目！

---

## 第二步：发布 VSCode 插件（可选）

### 1. 安装 vsce

```bash
npm install -g @vscode/vsce
```

### 2. 创建 Publisher 账号

1. 访问 https://marketplace.visualstudio.com/manage
2. 使用 Microsoft/GitHub 账号登录
3. 创建 Publisher ID: `east-hu`

### 3. 获取 Personal Access Token

1. 访问 https://dev.azure.com
2. 创建组织（如果还没有）
3. 点击用户设置 → Personal Access Tokens
4. 创建新 Token:
   - Scopes: ✅ Marketplace (Manage)
5. 复制 Token（只显示一次！）

### 4. 登录并发布

```bash
cd /Users/east/AntiGravity_projects/paper_robot/vscode-extension

# 登录
vsce login east-hu
# 粘贴您的 Personal Access Token

# 发布
vsce publish
```

---

## 当前状态检查

运行这些命令检查一切是否就绪：

```bash
cd /Users/east/AntiGravity_projects/paper_robot

# 检查 git 状态
git status

# 检查远程仓库配置
git remote -v

# 查看最近的提交
git log --oneline -5

# 测试 CLI
paper-robot --help
```

---

## 故障排除

### 问题：GitHub 推送失败 "Repository not found"
**解决**：需要先在 GitHub 上创建仓库（见第一步）

### 问题：VSCode 发布失败 "Publisher not found"
**解决**：
1. 确认 publisher ID 是 `east-hu`（小写）
2. 确认已在 https://marketplace.visualstudio.com/manage 创建 publisher

### 问题：Token 失效
**解决**：重新创建 Personal Access Token

---

## 📋 发布检查清单

- [ ] ✅ GitHub 仓库已创建
- [ ] ✅ 代码已推送到 GitHub
- [ ] ✅ README 在 GitHub 上正常显示
- [ ] ✅ 图片链接正常工作
- [ ] VSCode 插件:
  - [ ] Publisher 账号已创建
  - [ ] Personal Access Token 已获取
  - [ ] vsce 已安装
  - [ ] 插件已发布

---

## 🎉 完成后...

### 分享您的项目

- README 中添加了完整的使用说明
- 包含中英文双语文档
- 精美的 CLI 界面截图
- 清晰的安装步骤

### 下一步可做的事

1. 在社交媒体分享您的项目
2. 提交到 awesome-lists
3. 写一篇博客介绍项目
4. 收集用户反馈并持续改进

---

**需要帮助？** 查看完整的 [PUBLISHING_GUIDE.md](file:///Users/east/AntiGravity_projects/paper_robot/PUBLISHING_GUIDE.md)
