# User Configuration

## 日记路径配置

日记存储路径：

```bash
export DIARY_PATH="$HOME/Documents/diary"
```

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

## 文件命名规则

按月生成文件：`YYYY/YYYY-MM.md`（例如：`2026/2026-02.md`）

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
git remote add origin git@github.com:你的用户名/diary.git

# 使用 Gitea（私有）
git remote add origin git@gitea.com:你的用户名/diary.git
```

## 移动端配置

### iOS

**Working Copy（Git 客户端）**
- 添加远程仓库
- 选择 `~/Documents/diary` 作为本地目录
- 操作：Pull → 编辑 → Commit → Push

### Android

**Termux + Git**
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

## 日期格式说明

### 支持的日期格式

| 输入格式 | 解析结果 |
|---------|---------|
| `写日记：内容` | 今天的日期 |
| `写日记 2-1：内容` | 当年 2 月 1 日 |
| `写日记 02-01：内容` | 当年 2 月 1 日 |
| `写日记 2月1日：内容` | 当年 2 月 1 日 |

### 星期自动计算

skill 会自动计算日期对应的星期，例如：
- 2026-02-01 → 星期日
- 2026-02-24 → 星期二
