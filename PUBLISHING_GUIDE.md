# 发布到 GitHub 和 VSCode Marketplace 指南

## 第一步：创建 GitHub 仓库

### 方法一：通过 GitHub 网页创建（推荐）

1. **访问 GitHub**
   - 打开 https://github.com
   - 登录您的账号（East-Hu）

2. **创建新仓库**
   - 点击右上角的 "+" 按钮
   - 选择 "New repository"

3. **配置仓库**
   - **Repository name**: `paper-to-action`
   - **Description**: `📚 Automated academic paper delivery robot with AI summarization | 全自动论文速递机器人`
   - **Visibility**: ✅ Public（公开项目）
   - **❌ 不要勾选** "Initialize this repository with:"
     - [ ] Add a README file
     - [ ] Add .gitignore
     - [ ] Choose a license
   
   （因为我们本地已经有这些文件了）

4. **创建仓库**
   - 点击 "Create repository"

5. **推送代码**
   仓库创建后，GitHub会显示推送命令，但我们的本地仓库已经配置好了，直接运行：
   
   ```bash
   cd /Users/east/AntiGravity_projects/paper_robot
   git push -u origin main
   ```

### 方法二：使用 GitHub CLI（如果已安装 gh）

```bash
cd /Users/east/AntiGravity_projects/paper_robot

# 创建仓库并推送
gh repo create paper-to-action --public --source=. --push

# 设置仓库描述
gh repo edit --description "📚 Automated academic paper delivery robot with AI summarization | 全自动论文速递机器人"
```

---

## 第二步：发布 VSCode 插件

### 准备工作

#### 1. 安装 vsce（VSCode Extension Manager）

```bash
npm install -g @vscode/vsce
```

#### 2. 创建 Azure DevOps Publisher 账号

VSCode 扩展需要通过 Azure DevOps 发布：

1. **访问 Azure DevOps**
   - 打开 https://dev.azure.com
   - 使用 Microsoft 账号登录（可以用GitHub账号关联）

2. **创建组织（如果还没有）**
   - 点击 "Create new organization"
   - 输入组织名称，例如：`east-hu-publisher`

3. **创建 Personal Access Token (PAT)**
   - 点击右上角用户图标 → "Personal access tokens"
   - 点击 "New Token"
   - **Name**: `vscode-publisher-token`
   - **Organization**: 选择您的组织
   - **Expiration**: Custom defined → 选择 1 年
   - **Scopes**: 
     - ✅ **Marketplace** → ✅ Manage
   - 点击 "Create"
   - **重要**：复制生成的 token（只显示一次！）

4. **创建 Publisher**
   - 访问 https://marketplace.visualstudio.com/manage
   - 点击 "Create publisher"
   - **ID**: `east-hu` （必须是小写字母、数字、连字符）
   - **Display Name**: `East Hu`
   - **Description**: `Academic tools and productivity extensions`
   - 点击 "Create"

### 发布步骤

#### 1. 登录 vsce

```bash
cd /Users/east/AntiGravity_projects/paper_robot/vscode-extension

# 使用您的 PAT 登录
vsce login east-hu
# 输入刚才复制的 Personal Access Token
```

#### 2. 打包插件（可选，用于本地测试）

```bash
# 打包为 .vsix 文件
vsce package

# 这会生成类似 paper-to-action-0.1.0.vsix 的文件
# 可以手动安装测试：
# VSCode → Extensions → ... → Install from VSIX
```

#### 3. 发布到市场

```bash
# 发布插件
vsce publish

# 或者指定版本号
vsce publish 0.1.0

# 如果是更新，可以自动增加版本号
vsce publish minor  # 0.1.0 -> 0.2.0
vsce publish patch  # 0.1.0 -> 0.1.1
```

#### 4. 验证发布

- 访问 https://marketplace.visualstudio.com/items?itemName=east-hu.paper-to-action
- 等待 5-10 分钟让插件在市场上生效
- 在 VSCode 中搜索 "Paper-to-Action" 测试安装

---

## 第三步：后续维护

### 更新插件

当您修改了插件代码后：

```bash
cd vscode-extension

# 更新版本号并发布
vsce publish patch  # 小更新: 0.1.0 -> 0.1.1
vsce publish minor  # 功能更新: 0.1.0 -> 0.2.0
vsce publish major  # 重大更新: 0.1.0 -> 1.0.0
```

### 撤销发布（如果需要）

```bash
# 撤销特定版本
vsce unpublish east-hu.paper-to-action@0.1.0

# 撤销整个插件（谨慎！）
vsce unpublish east-hu.paper-to-action
```

---

## 常见问题

### Q: push 时提示认证失败？
A: 检查您的 GitHub token 是否有效：
```bash
# 重新设置 remote URL（如果token过期）
git remote set-url origin https://YOUR_NEW_TOKEN@github.com/East-Hu/paper-to-action.git
```

### Q: VSCode 插件发布失败？
A: 确保：
1. `package.json` 中的 `publisher` 字段是 `"east-hu"`
2. Personal Access Token 有 Marketplace → Manage 权限
3. 所有必需的字段都已填写（name, version, description, etc.）

### Q: 插件图标显示不出来？
A: 确保：
1. `icon` 字段指向的文件存在
2. 图标是 PNG 格式，至少 128x128 像素
3. 文件路径相对于 `package.json`

### Q: 如何设置仓库主页的 README 显示？
A: GitHub 会自动显示根目录的 `README.md`。您的已经配置好了！

---

## 推荐的发布前检查清单

- [ ] GitHub 仓库创建成功
- [ ] 代码成功 push 到 GitHub
- [ ] README 在 GitHub 上显示正常
- [ ] 所有图片链接正常工作
- [ ] VSCode 插件本地测试通过
- [ ] package.json 配置正确（publisher, icon, etc.）
- [ ] 插件成功发布到市场
- [ ] 在 VSCode 中能搜索并安装插件

---

## 下一步

1. ✅ 创建 GitHub 仓库
2. ✅ Push 代码
3. ✅ 完善 VSCode 插件配置
4. ✅ 发布到 VSCode Marketplace
5. 🎉 分享您的项目！
