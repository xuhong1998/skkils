---
name: diary-quick-append
description: (Linux/WSL) Use when user wants to quickly append diary content. Trigger pattern: "写日记：[content]" or "写日记 [date]: [content]". Automatically polishes and appends to the diary file. No questions asked.
---

# Diary Quick Append

快速追加日记，自动润色并保存到月度日记文件，无需交互。

## Prerequisites

| Tool | Type | Required | Install |
|------|------|----------|---------|
| Linux/WSL | system | Yes | Ubuntu or other Linux distributions |
| git | cli | Yes | `sudo apt install git` |

> Do NOT proactively verify these tools on skill load. If a command fails due to a missing tool, directly guide the user through installation and configuration step by step.

## 核心原则

| 原则 | 说明 |
|------|------|
| **零交互** | 自动完成所有操作，不询问用户 |
| **自动润色** | 修正错别字、优化语句流畅度 |
| **自动追加** | 自动识别日期并追加到文件 |
| **自动同步** | 自动提交并推送到 Git |

## 触发格式

### 格式 1：今日日记

```text
写日记：今天做了什么，有什么感受...
```

### 格式 2：指定日期

```text
写日记 2-1：今天做了什么...
写日记 02-01：今天做了什么...
写日记 2月1日：今天做了什么...
```

## 完整流程

```text
┌─────────────────────────────────────────────────────────────┐
│     diary-quick-append 完整流程（目标 ≤30秒）            │
└─────────────────────────────────────────────────────────────┘

  ┌──────────────┐
  │ 用户输入日记  │
  └──────┬───────┘
         │
         ▼
  ┌────────────────────────────────────┐
  │ 1. 解析输入               (~1sec)   │
  │    提取日期（默认今天）             │
  │    提取日记内容                 │
  └──────┬─────────────────────────────┘
         │
         ▼
  ┌────────────────────────────────────┐
  │ 2. Git 拉取               (~2sec)   │
  │    git pull origin main          │
  └──────┬─────────────────────────────┘
         │
         ▼
  ┌────────────────────────────────────┐
  │ 3. 润色日记内容           (~5sec)   │
  │    修正错别字                   │
  │    优化语句流畅度                 │
  └──────┬─────────────────────────────┘
         │
         ▼
  ┌────────────────────────────────────┐
  │ 4. 追加到文件            (~2sec)   │
  │    打开 2026/2026-02.md         │
  │    追加日记内容                 │
  └──────┬─────────────────────────────┘
         │
         ▼
  ┌────────────────────────────────────┐
  │ 5. Git 推送              (~3sec)   │
  │    git add                     │
  │    git commit                  │
  │    git push                    │
  └──────┬─────────────────────────────┘
         │
         ▼
       ┌──────┐
       │ 完成  │  总计 ~13秒
       └──────┘
```

## 1. 解析输入

### 格式识别

| 输入格式 | 解析结果 |
|---------|---------|
| `写日记：内容` | 日期=今天，内容=内容 |
| `写日记 2-1：内容` | 日期=2-1，内容=内容 |
| `写日记 02-01：内容` | 日期=02-01，内容=内容 |
| `写日记 2月1日：内容` | 日期=2-1，内容=内容 |

### 日期解析

使用 Python 解析日期：

```python
import re
from datetime import datetime

def parse_date(date_str):
    today = datetime.now()
    year = today.year
    month = today.month
    day = today.day
    
    if date_str:
        # 匹配 MM-DD 或 M-D 格式
        match = re.match(r'(\d{1,2})[-/月](\d{1,2})', date_str)
        if match:
            month = int(match.group(1))
            day = int(match.group(2))
    
    return year, month, day

# 获取星期
def get_weekday(year, month, day):
    weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    return weekdays[datetime(year, month, day).weekday()]
```

## 2. Git 拉取

```bash
cd ~/Documents/diary
git pull origin main
```

## 3. 润色日记内容

### 润色规则

**可以修改：**
- 错别字（的/地/得混用、同音字错误）
- 标点符号使用不当
- 明显的语法错误
- 语序调整使语句更通顺（不改变原意）
- 删除冗余词语（如：重复的"那个""就是"）

**绝对不能修改：**
- 任何事实内容（发生了什么事）
- 观点和看法（你的想法、感受）
- 情感表达（开心、难过、愤怒等）
- 具体描述（人名、地点、数字、时间）
- 简洁改详细（保持原有信息量）
- 口语化改书面语（保持原有风格）

### 润色提示词

```text
请修正以下日记内容中的错别字并优化语句流畅度：

【修正原则】
✅ 可以修改：
  1. 错别字（如：的/地/得混用、同音字错误）
  2. 标点符号使用不当
  3. 明显的语法错误
  4. 语序调整使语句更通顺（不改变原意）
  5. 删除冗余词语（如：重复的"那个""就是"）

❌ 绝对不能修改：
  1. 任何事实内容（发生了什么事）
  2. 观点和看法（你的想法、感受）
  3. 情感表达（开心、难过、愤怒等）
  4. 具体描述（人名、地点、数字、时间）
  5. 简洁改详细（保持原有信息量）
  6. 口语化改书面语（保持原有风格）

---

请根据上述原则修正以下内容：
【日记内容】
```

## 4. 追加到文件

### 文件路径

```bash
# 格式：YYYY/YYYY-MM.md
file_path="~/Documents/diary/$(date +%Y)/$(date +%Y-%m).md"
```

### 追加格式

```markdown

---

## MM-DD 星期X
### 今日记录

[润色后的日记内容]

### 收获与感受
```

### 追加逻辑

```python
# 1. 检查文件是否存在
if not os.path.exists(file_path):
    # 创建新文件
    create_new_file(file_path, year, month)

# 2. 追加内容
append_content(file_path, content)

def create_new_file(file_path, year, month):
    content = f"# {year}-{month:02d}\n\n"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def append_content(file_path, date, weekday, content):
    header = f"\n---\n\n## {date} {weekday}\n### 今日记录\n\n"
    footer = "\n### 收获与感受\n"
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(header)
        f.write(content)
        f.write(footer)
```

## 5. Git 推送

```bash
cd ~/Documents/diary
git add .
git commit -m "update: $(date +%Y-%m-%d)"
git push origin main
```

## 时间预算

| 步骤 | 时间 |
|------|------|
| 解析输入 | ~1 秒 |
| Git 拉取 | ~2 秒 |
| 润色内容 | ~5 秒 |
| 追加文件 | ~2 秒 |
| Git 推送 | ~3 秒 |
| **总计** | **~13 秒** |

## 错误处理

| 错误 | 处理 |
|------|------|
| 日期解析失败 | 使用今天的日期 |
| Git 拉取失败 | 跳过拉取，直接追加 |
| 文件写入失败 | 提示用户检查权限 |
| Git 推送失败 | 提示用户检查网络 |

## 用户配置

见 [user-config.md](references/user-config.md) 配置日记路径和 Git 仓库。

## 示例

### 示例 1：今日日记

**输入：**
```
写日记：今天中午没有睡觉，而是在园区转了一圈。
```

**处理流程：**
1. 解析：日期=2026-02-24，内容="今天中午没有睡觉，而是在园区转了一圈。"
2. Git 拉取
3. 润色：内容保持不变（已通顺）
4. 追加到：`2026/2026-02.md`
5. Git 推送

**结果：**
```markdown
---

## 02-24 星期二
### 今日记录

今天中午没有睡觉，而是在园区转了一圈。

### 收获与感受
```

### 示例 2：指定日期

**输入：**
```
写日记 2-1：今天收到一个利空信息。
```

**处理流程：**
1. 解析：日期=2026-02-01，内容="今天收到一个利空信息。"
2. Git 拉取
3. 润色：内容保持不变（已通顺）
4. 追加到：`2026/2026-02.md`
5. Git 推送

**结果：**
```markdown
---

## 02-01 星期日
### 今日记录

今天收到一个利空信息。

### 收获与感受
```
