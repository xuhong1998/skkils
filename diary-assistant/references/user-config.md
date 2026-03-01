# User Configuration

## 日记路径配置

请配置您的日记存储路径：

```bash
# 设置环境变量（添加到 ~/.bashrc 或 ~/.zshrc）
export DIARY_PATH="$HOME/Documents/diary"
```

或者直接在日记过程中询问用户路径。

## 目录结构

日记按年份分类组织：

```text
~/Documents/diary/
├── .git/
├── README.md
└── 2026/
    ├── 2026-01.md
    ├── 2026-02.md
    └── ...
```

## 月度日记文件格式

- **文件命名**：`YYYY/YYYY-MM.md`（例如：`2026/2026-02.md`）
- **文件位置**：`$DIARY_PATH/YYYY/YYYY-MM.md`
- **内容组织**：按日期分节，每个日期使用二级标题 `## MM-DD WeekDay`

示例结构：

```markdown
# 2026-02

## 02-01 Sun
### 今日记录

[Work Log]

今天做了什么...

### 收获与感受

...

---

## 02-02 Mon
### 今日记录

...

### 收获与感受

...

---

## 02-24 Tue
### 今日记录

...

### 收获与感受

...
```

## Git 同步配置

### 初始化 Git 仓库（首次使用）

```bash
cd ~/Documents/diary
git init
git add .
git commit -m "init: 初始化日记仓库"
git remote add origin <远程仓库地址>
git push -u origin main
```

### 配置远程仓库

可以选择以下平台之一：

- **GitHub**：https://github.com
- **Gitea/码云**：https://gitee.com
- **GitLab**：https://gitlab.com
- **自建 Gitea**：如果你有自己的服务器

示例：

```bash
# 使用 GitHub
git remote add origin https://github.com/你的用户名/diary.git

# 使用 Gitea（私有）
git remote add origin https://gitea.com/你的用户名/diary.git
```

### 移动端配置

**iOS：**
1. 安装 Working Copy（Git 客户端）
2. 安装 Textastic（Markdown 编辑器）
3. 配置 Working Clone：
   - 添加远程仓库
   - 选择 `~/Documents/diary` 作为本地目录

**Android：**
1. 安装 Termux（终端）
2. 安装 Markor（Markdown 编辑器）
3. 在 Termux 中：

```bash
# 安装 Git
pkg install git

# 克隆仓库
git clone <远程仓库地址> ~/Documents/diary

# 日常操作
cd ~/Documents/diary
git pull  # 写日记前
# 编辑日记
git add .
git commit -m "update: $(date +%Y-%m-%d)"
git push  # 写日记后
```

## Work Log 仓库配置

worklog skill 需要知道您的工作仓库位置，以便生成 git 统计。

在 `~/.config/worklog/config.json` 中配置：

```json
{
  "repos": [
    {
      "name": "项目A",
      "path": "/home/xh/work/project-a"
    },
    {
      "name": "项目B",
      "path": "/home/xh/work/project-b"
    }
  ]
}
```

如果没有配置，worklog 会自动扫描当前工作目录下的 git 仓库。
