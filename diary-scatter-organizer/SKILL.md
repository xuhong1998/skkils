---
name: diary-scatter-organizer
description: (Linux/Mac/Windows) Use when user wants to organize scattered diary records. Triggers on「整理日记」「整理记录」「organize diary」. Parses timestamp-based records, categorizes by time, extracts health info, and generates structured diary.
---

## Prerequisites

| Tool | Type | Required | Install |
|------|------|----------|---------|
| Linux/Mac/Windows | system | Yes | Ubuntu, macOS, or Windows with WSL |
| git | cli | Yes | Linux: `sudo apt install git`<br>Mac: `brew install git` or included with Xcode<br>Windows: `winget install Git.Git` or download from git-scm.com |
| Python 3 | cli | Yes | Linux: `sudo apt install python3`<br>Mac: `brew install python3` or included with macOS<br>Windows: `winget install Python.Python.3` or download from python.org |
| weather-cn | skill | No | 获取天气信息的独立 skill |
| curl | cli | Yes | Linux: `sudo apt install curl`<br>Mac: included with macOS<br>Windows: included with Windows 10+ or install from curl.se |

> Do NOT proactively verify these tools on skill load. If a command fails due to a missing tool, directly guide the user through installation and configuration step by step.

## 核心原则

| 原则 | 说明 |
|------|------|
| **自动解析** | 识别时间戳格式（如 `12:00`）和内容 |
| **想法提取** | 识别"想法""感悟""思考""感想"等关键词，提取非时间戳内容 |
| **智能分类** | 按时间自动分配到上午/下午/晚上 |
| **健康提取** | 自动识别餐食、运动、喝水等健康信息 |
| **天气获取** | 自动检测城市，获取当日天气信息（默认武汉） |
| **模版框架** | 生成完整模版，未知部分留空 |
| **自动润色** | 修正错别字、优化语句流畅度 |
| **标签管理调用** | 调用 diary-tag-manager 提取标签 |

## 完整流程

```text
┌─────────────────────────────────────────────────────┐
│       diary-scatter-organizer 完整流程（目标 ≤5分钟）       │
└─────────────────────────────────────────────────────┘

   ┌──────────────┐
   │ 用户输入：    │
   │ 整理日记：    │
   │ [零散记录...]│
   └──────┬───────┘
          │
          ▼
   ┌────────────────────────────────────┐
   │ 1. Git 拉取              (~10sec)   │
   │    git pull origin main            │
   └──────┬─────────────────────────────┘
          │
          ▼
    ┌────────────────────────────────────┐
    │ 2. 解析时间戳记录和想法   (~30sec)  │
    │    提取 时间 + 内容                 │
    │    识别想法部分（想法/感悟/思考）    │
    └──────┬─────────────────────────────┘
          │
          ▼
   ┌────────────────────────────────────┐
   │ 3. 检测城市并获取天气    (~30sec)  │
   │    检测记录中的城市名               │
   │    调用 weather-cn 获取天气        │
   │    默认城市：武汉                    │
   └──────┬─────────────────────────────┘
          │
          ▼
   ┌────────────────────────────────────┐
   │ 4. 按时间段分类           (~20sec)  │
   │    上午：06:00-12:00               │
   │    下午：12:00-18:00               │
   │    晚上：18:00-24:00               │
   └──────┬─────────────────────────────┘
          │
          ▼
   ┌────────────────────────────────────┐
   │ 5. 提取健康信息           (~30sec)  │
   │    午餐、晚餐、运动、喝水           │
   └──────┬─────────────────────────────┘
          │
          ▼
   ┌────────────────────────────────────┐
   │ 6. 润色文本内容           (~1min)   │
   │    修正错别字                       │
   │    优化语句流畅度                   │
   └──────┬─────────────────────────────┘
          │
          ▼
   ┌────────────────────────────────────┐
   │ 7. AI标签提取（调用diary-tag-manager） (~1-2min) │
   │    调用 diary-tag-manager skill      │
   │    使用最新的标签提取策略            │
   └──────┬─────────────────────────────┘
          │
          ▼
   ┌────────────────────────────────────┐
   │ 7. 生成模版框架           (~1min)   │
   │    填充已知部分（含天气）           │
   │    未知部分留空                     │
   └──────┬─────────────────────────────┘
          │
          ▼
   ┌────────────────────────────────────┐
   │ 8. 保存到文件            (~10sec)   │
    │    2026/02/02-24-Tue.md           │
   └──────┬─────────────────────────────┘
          │
          ▼
   ┌────────────────────────────────────┐
   │ 9. Git 推送             (~10sec)   │
   │    git add → commit → push        │
   └──────┬─────────────────────────────┘
          │
          ▼
        ┌──────┐
        │ 完成  │
        └──────┘
```

## 1. Git 拉取（获取最新）

```bash
cd ../diary
git pull origin main
```

### 拉取流程

```text
Claude: 「开始前先从 Git 远程仓库拉取最新内容...」

执行：git pull origin main

输出：
✅ 拉取成功（最新）
或
⚠️ 检测到冲突，请手动解决后重试

如果成功：
Claude: 「拉取完成，现在开始整理记录。」

如果失败：
Claude: 「⚠️ Git 拉取失败，请检查网络或手动解决冲突。」
```

## 2. 解析时间戳记录和想法

### 支持的格式

#### 时间戳记录
| 格式 | 示例 |
|------|------|
| HH:MM | `12:00`、`09:30` |
| H:MM | `9:00`、`8:30` |

#### 想法部分
| 关键词 | 说明 |
|--------|------|
| 想法 | 单独一行或带冒号 |
| 感悟 | 单独一行或带冒号 |
| 思考 | 单独一行或带冒号 |
| 感想 | 单独一行或带冒号 |

### 解析规则

```text
# 时间戳记录
12:00 中午吃的一碗卤肉饭，不是特别想吃，可能跟担心吃多了长胖有关吧。
│    │
│    └─ 内容
└────── 时间戳

# 想法部分
想法
今天同时叫我下下去香港麦理浩径徒步...
│
└─ 想法关键词
```

### 解析函数（Python）

```python
import re
from typing import List, Tuple, Dict, Any

def parse_input(input_text: str) -> Dict[str, Any]:
    """
    解析输入，分离时间戳记录和想法

    Args:
        input_text: 输入文本

    Returns:
        {
            'records': [(时间, 内容), ...],
            'ideas': '想法内容（或空字符串）'
        }
    """
    lines = input_text.strip().split("\n")

    # 想法关键词（支持多种格式）
    idea_keywords = ["想法", "感悟", "思考", "感想"]

    records = []
    ideas = []
    current_section = "records"

    for line in lines:
        line_stripped = line.strip()

        if not line_stripped:
            continue

        # 检查是否是想法部分的开始
        is_idea_keyword = False
        for keyword in idea_keywords:
            if line_stripped == keyword or line_stripped.startswith(keyword + "：") or line_stripped.startswith(keyword + ":"):
                is_idea_keyword = True
                current_section = "ideas"
                break

        if is_idea_keyword:
            continue

        # 检查是否是时间戳记录
        match = re.match(r"^(\d{1,2}:\d{2})\s+(.+)$", line_stripped)
        if match:
            current_section = "records"
            time_str = match.group(1)
            content = match.group(2)
            records.append((time_str, content))
        elif current_section == "ideas":
            ideas.append(line_stripped)

    return {
        "records": records,
        "ideas": "\n".join(ideas)
    }
```

### 示例

#### 示例 1：纯时间戳记录

**输入：**
```
12:00 中午吃的一碗卤肉饭，不是特别想吃，可能跟担心吃多了长胖有关吧。
13:00 中午睡了一觉，睡的很死，可能跟最近很累有关吧。
16:40 回出租屋拿村里面人跟我带的行李，拿完又回来上班。
19:30 弄了两块糍粑吃
```

**解析结果：**
```python
{
    'records': [
        ('12:00', '中午吃的一碗卤肉饭，不是特别想吃，可能跟担心吃多了长胖有关吧。'),
        ('13:00', '中午睡了一觉，睡的很死，可能跟最近很累有关吧。'),
        ('16:40', '回出租屋拿村里面人跟我带的行李，拿完又回来上班。'),
        ('19:30', '弄了两块糍粑吃')
    ],
    'ideas': ''
}
```

#### 示例 2：带想法的记录

**输入：**
```
8:30  早上吃了碗热干面
12:00 中午吃千张肉丝
18:00 下班，今天下了一个早班，感觉还不错。回到家后发现天还没黑下来，有出门去了一趟公园散步
19:00 在家自己做饭，还是吃豆丝炒腊肠
20:00 本来想继续写日历app的，但是有刷抖音去了，到了20：40才开始写日历app，让ai把前后端都生成出来，但是还是有很多问题

想法
今天同时叫我下下去香港麦理浩径徒步，我看他坐卧铺去深圳然后去香港，看成本很低我也很想去
```

**解析结果：**
```python
{
    'records': [
        ('8:30', '早上吃了碗热干面'),
        ('12:00', '中午吃千张肉丝'),
        ('18:00', '下班，今天下了一个早班，感觉还不错。回到家后发现天还没黑下来，有出门去了一趟公园散步'),
        ('19:00', '在家自己做饭，还是吃豆丝炒腊肠'),
        ('20:00', '本来想继续写日历app的，但是有刷抖音去了，到了20：40才开始写日历app，让ai把前后端都生成出来，但是还是有很多问题')
    ],
    'ideas': '今天同时叫我下下去香港麦理浩径徒步，我看他坐卧铺去深圳然后去香港，看成本很低我也很想去'
}
```

## 3. 检测城市并获取天气

### 调用 weather-cn skill

此功能通过调用独立的 `weather-cn` skill 实现。

**调用流程：**
1. 从记录内容中检测城市名
2. 调用 `weather-cn` skill 获取天气信息
3. 格式化天气信息用于日记模版

### 城市检测规则

| 检测方式 | 说明 | 示例 |
|---------|------|------|
| 自动检测 | 从记录内容中匹配城市名 | "今天北京天气不错" → 北京 |
| 默认城市 | 无城市时使用默认 | 默认：武汉 |

### Python 调用示例

```python
from weather_cn.scripts.get_weather import detect_city, get_weather, format_weather

# 合并所有记录内容
all_content = ' '.join([content for _, content in records])

# 检测城市
city = detect_city(all_content, default_city='武汉')
print(f"检测到城市：{city}")

# 获取天气
weather_info = get_weather(city)
if weather_info:
    # 格式化天气信息
    weather_str = format_weather(weather_info)
    print(f"天气信息：{weather_str}")
    # 输出：武汉天气：⛅️，温度：15°C，湿度：72%
else:
    print("天气信息获取失败")
```

### 示例

**输入：**
```python
records = [
    ('12:00', '中午吃的一碗卤肉饭，不是特别想吃，可能跟担心吃多了长胖有关吧。'),
    ('13:00', '中午睡了一觉，睡的很死，可能跟最近很累有关吧。'),
    ('16:40', '回出租屋拿村里面人跟我带的行李，拿完又回来上班。'),
    ('19:30', '弄了两块糍粑吃')
]
```

**城市检测：**
```python
from weather_cn.scripts.get_weather import detect_city

all_content = ' '.join([content for _, content in records])
city = detect_city(all_content, default_city='武汉')
# 输出：'武汉'（记录中无城市，使用默认）
```

**天气获取：**
```python
from weather_cn.scripts.get_weather import get_weather

weather_info = get_weather(city)
# 输出：{'city': '武汉', 'temp': '15', 'condition': '多云', 'humidity': '72', 'wind': '10'}
```

**天气格式化：**
```python
from weather_cn.scripts.get_weather import format_weather

weather_str = format_weather(weather_info)
# 输出：'武汉天气：⛅️，温度：15°C，湿度：72%'
```

**包含城市名的情况：**
```python
records = [
    ('12:00', '中午在北京吃的一碗卤肉饭，不是特别想吃。'),
    ('13:00', '中午睡了一觉，睡的很死。')
]

from weather_cn.scripts.get_weather import detect_city, get_weather, format_weather

all_content = ' '.join([content for _, content in records])
city = detect_city(all_content, default_city='武汉')
# 输出：'北京'（检测到北京）

weather_info = get_weather(city)
weather_str = format_weather(weather_info)
# 输出：'北京天气：☀️，温度：8°C，湿度：45%'
```

## 4. 按时间段分类

### 时间段分类规则

| 时间段 | 时间范围 | 模版对应 |
|--------|----------|----------|
| 上午 | 06:00 - 11:59 | ### 上午 |
| 下午 | 12:00 - 17:59 | ### 下午 |
| 晚上 | 18:00 - 23:59 | ### 晚上 |
| 凌晨 | 00:00 - 05:59 | ### 上午 |

### 分类函数（Python）

```python
def categorize_by_time(records: List[Tuple[str, str]]) -> dict:
    """
    按时间段分类记录

    Args:
        records: [(时间, 内容), ...]

    Returns:
        {
            '上午': [...],
            '下午': [...],
            '晚上': [...]
        }
    """
    categorized = {
        '上午': [],
        '下午': [],
        '晚上': []
    }

    for time_str, content in records:
        # 解析时间
        hour, minute = map(int, time_str.split(':'))
        time_minutes = hour * 60 + minute

        # 分类
        if 6 * 60 <= time_minutes < 12 * 60:
            category = '上午'
        elif 12 * 60 <= time_minutes < 18 * 60:
            category = '下午'
        elif 18 * 60 <= time_minutes < 24 * 60:
            category = '晚上'
        else:
            category = '上午'  # 凌晨归入上午

        categorized[category].append((time_str, content))

    return categorized
```

### 示例

**输入：**
```python
[
    ('12:00', '中午吃的一碗卤肉饭，不是特别想吃，可能跟担心吃多了长胖有关吧。'),
    ('13:00', '中午睡了一觉，睡的很死，可能跟最近很累有关吧。'),
    ('16:40', '回出租屋拿村里面人跟我带的行李，拿完又回来上班。'),
    ('19:30', '弄了两块糍粑吃')
]
```

**分类结果：**
```python
{
    '上午': [],
    '下午': [
        ('12:00', '中午吃的一碗卤肉饭，不是特别想吃，可能跟担心吃多了长胖有关吧。'),
        ('13:00', '中午睡了一觉，睡的很死，可能跟最近很累有关吧。'),
        ('16:40', '回出租屋拿村里面人跟我带的行李，拿完又回来上班。')
    ],
    '晚上': [
        ('19:30', '弄了两块糍粑吃')
    ]
}
```

## 5. 提取健康信息

### 关键词识别

| 类别 | 关键词 | 模版字段 |
|------|--------|----------|
| 午餐 | 午餐、午饭、中午吃、中午饭、吃的一碗 | 午餐 |
| 晚餐 | 晚餐、晚饭、晚上吃、晚饭 | 晚餐 |
| 运动 | 跑步、走路、健身、锻炼、运动、打球 | 运动 |
| 喝水 | 喝水、喝水、喝水、水 | 喝水 |

### 提取函数（Python）

```python
def extract_health_info(records: List[Tuple[str, str]]) -> dict:
    """
    提取健康信息

    Args:
        records: [(时间, 内容), ...]

    Returns:
        {
            '午餐': '内容',
            '晚餐': '内容',
            '运动': '内容',
            '喝水': '内容'
        }
    """
    health_info = {
        '午餐': '',
        '晚餐': '',
        '运动': '',
        '喝水': ''
    }

    lunch_keywords = ['午餐', '午饭', '中午吃', '中午饭', '吃的一碗']
    dinner_keywords = ['晚餐', '晚饭', '晚上吃', '晚饭']
    exercise_keywords = ['跑步', '走路', '健身', '锻炼', '运动', '打球']
    water_keywords = ['喝水', '喝水', '喝水', '水']

    for time_str, content in records:
        # 提取午餐
        if any(kw in content for kw in lunch_keywords) and not health_info['午餐']:
            health_info['午餐'] = content

        # 提取晚餐
        if any(kw in content for kw in dinner_keywords) and not health_info['晚餐']:
            health_info['晚餐'] = content

        # 提取运动
        if any(kw in content for kw in exercise_keywords) and not health_info['运动']:
            health_info['运动'] = content

        # 提取喝水
        if any(kw in content for kw in water_keywords) and not health_info['喝水']:
            health_info['喝水'] = content

    return health_info
```

### 提取逻辑细化

对于餐食信息，只提取具体内容，删除前缀描述：

```python
def extract_meal_content(content: str) -> str:
    """
    提取餐食内容
    """
    # 删除时间描述词
    patterns = [
        r'中午吃的一碗',
        r'中午吃了',
        r'中午吃',
        r'晚上吃了',
        r'晚上吃',
    ]

    result = content
    for pattern in patterns:
        result = re.sub(pattern, '', result)

    return result.strip()
```

### 示例

**输入：**
```python
[
    ('12:00', '中午吃的一碗卤肉饭，不是特别想吃，可能跟担心吃多了长胖有关吧。'),
    ('13:00', '中午睡了一觉，睡的很死，可能跟最近很累有关吧。'),
    ('16:40', '回出租屋拿村里面人跟我带的行李，拿完又回来上班。'),
    ('19:30', '弄了两块糍粑吃')
]
```

**提取结果：**
```python
{
    '午餐': '卤肉饭',
    '晚餐': '糍粑',
    '运动': '',
    '喝水': ''
}
```

## 6. 润色文本内容

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

## 7. AI标签提取（调用diary-tag-manager）

### 调用流程

Claude: 「正在调用 diary-tag-manager 提取标签...」

**调用方式：**
1. 读取已生成的日记内容
2. 调用 diary-tag-manager skill 进行标签提取
3. 使用最新的标签提取策略（包含详细标签和紧凑格式）
4. 将提取的标签块添加到日记文件末尾

### 标签提取结果

diary-tag-manager 会自动：
- 使用最新的AI标签提取提示词
- 提取详细标签（具体菜名、运动距离、学习内容等）
- 生成紧凑格式的标签块（分类和标签在同一行）
- 严格遵循"不要无中生有标签"的原则

**示例输出：**
```
✅ 标签提取完成！

📊 主要标签：#生活日常 #数字成瘾 #运动健康 #饮食健康 #学习成长
🏷️ 子标签：#辣椒炒肉 #豆丝炒腊肠 #散步 #走楼梯-25层 #抖音 #Mac #自控管理
😊 情绪标签：#平静 #反思 #满足
📍 地点标签：#武汉 #家中 #公园

正在添加标签块到日记文件末尾...
✅ 标签块已添加！
```

## 8. 生成模版框架

### 完整模版

```markdown
# 📅 MM-DD 星期X

---

## 昨日计划完成情况

* [ ]
* [ ]
* [ ]
* [ ]

---

## 今日记录

[天气信息]

### 上午

[上午记录]

---

### 下午

[下午记录]

---

### 晚上

[晚上记录]

---

## 状态

* 精力：{{x}} / 10
* 情绪：{{x}} / 10

---

## 健康打卡

* 午餐：[内容]
* 晚餐：[内容]
* 运动：[类型 + 数量]
* 喝水：[数量]

---

## 今日收获

*
*
*

---

## 今日卡点

*
*
*

---

## 感悟

[想法内容，若无想法则为空引用块]

---

## 明日计划

* [ ]
* [ ]
* [ ]
* [ ]

---
```

### 填充规则

| 部分 | 处理方式 |
|------|----------|
| 标题（日期、星期） | 自动填充 |
| 昨日计划完成情况 | 留空（4 个空任务） |
| 今日记录（天气） | 自动获取填充 |
| 今日记录（上午/下午/晚上） | 自动填充 |
| 状态（精力、情绪） | 留空（`{{x}} / 10`） |
| 健康打卡 | 自动提取填充 |
| 今日收获 | 留空（3 个空项） |
| 今日卡点 | 留空（3 个空项） |
| 感悟 | 自动填充想法内容（若有），否则留空（`>`） |
| 明日计划 | 留空（4 个空任务） |

### 生成函数（Python）

```python
def generate_template(date: str, weekday: str, weather_str: str, categorized: dict, health_info: dict) -> str:
    """
    生成日记模版

    Args:
        date: 日期（如 '02-24'）
        weekday: 星期（如 '星期二'）
        weather_str: 天气信息字符串
        categorized: 分类后的记录
        health_info: 健康信息

    Returns:
        完整模版内容
    """
    template = f"""# 📅 {date} {weekday}

---

## 昨日计划完成情况

* [ ]
* [ ]
* [ ]
* [ ]

---

## 今日记录

{weather_str}

### 上午

"""

    # 填充上午记录
    if categorized['上午']:
        for time_str, content in categorized['上午']:
            template += f"{time_str} {content}\n"
    else:
        template += "---\n\n"

    template += "---\n\n### 下午\n\n"

    # 填充下午记录
    if categorized['下午']:
        for time_str, content in categorized['下午']:
            template += f"{time_str} {content}\n"
    else:
        template += "---\n\n"

    template += "---\n\n### 晚上\n\n"

    # 填充晚上记录
    if categorized['晚上']:
        for time_str, content in categorized['晚上']:
            template += f"{time_str} {content}\n"
    else:
        template += "---\n\n"

    template += """---

## 状态

* 精力：{{x}} / 10
* 情绪：{{x}} / 10

---

## 健康打卡

* 午餐：{lunch}
* 晚餐：{dinner}
* 运动：{exercise}
* 喝水：{water}

---

## 今日收获

*
*
*

---

## 今日卡点

*
*
*

---

## 感悟

>

---

## 明日计划

* [ ] 
* [ ] 
* [ ] 
* [ ] 

---
""".format(
        lunch=health_info['午餐'] or '',
        dinner=health_info['晚餐'] or '',
        exercise=health_info['运动'] or '',
        water=health_info['喝水'] or ''
    )

    return template
```

## 9. 保存到文件

### 文件路径

```bash
# 格式：YYYY/MM/MM-DD-WeekDay.md
file_path="../diary/$(date +%Y)/$(date +%m)/$(date +%m-%d)-$(date +%a).md"

例如：`../diary/2026/02/02-24-Tue.md`

### 写入逻辑

```bash
#!/bin/bash
# 写入日记文件

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
diary_path="$SCRIPT_DIR/../../diary"
year=$(date +%Y)
month=$(date +%m)
date=$(date +%m-%d)
weekday=$(date +%a)

file_path="$diary_path/$year/$month/$date-$weekday.md"

# 创建目录（如果不存在）
mkdir -p "$diary_path/$year/$month"

# 写入内容
echo "$diary_content" > "$file_path"

echo "✅ 日记已保存到：$file_path"
```

### 文件覆盖处理

```text
Claude: 「检测到文件已存在：2026/02/02-24-Tue.md
是否覆盖？(y/n)」

用户: 「y」 → 覆盖
用户: 「n」 → 退出
```

## 10. Git 推送（保存修改）

```bash
cd ../diary
git add .
git commit -m "update: $(date +%Y-%m-%d)"
git push origin main
```

### 推送流程

```text
Claude: 「日记已完成。现在推送到 Git 远程仓库。」

执行：
cd ../diary
git add .
git commit -m "update: $(date +%Y-%m-%d)"
git push origin main

输出：
✅ 提交完成（1 个文件）
✅ 推送成功

Claude: 「推送完成！」

如果遇到冲突：
Claude: 「⚠️ 检测到 Git 冲突，需要先拉取。

请先执行：
cd ../diary
git pull origin main
解决冲突后，再推送。」
```

## 时间预算

| 步骤 | 时间 |
|------|------|
| Git 拉取（获取最新） | ~10 秒 |
| 解析时间戳记录和想法 | ~30 秒 |
| 检测城市并获取天气 | ~30 秒 |
| 按时间段分类 | ~20 秒 |
| 提取健康信息 | ~30 秒 |
| 润色文本内容 | ~1 分钟 |
| 生成模版框架（含天气、想法） | ~1 分钟 |
| 保存到文件 | ~10 秒 |
| Git 推送（保存修改） | ~10 秒 |
| **总计** | **~4.5 分钟** |

## 用户配置

见 [user-config.md](references/user-config.md) 配置日记路径和 Git 仓库。

## 示例

### 示例 1：基本整理

**用户输入：**
```
整理日记：
12:00 中午吃的一碗卤肉饭，不是特别想吃，可能跟担心吃多了长胖有关吧。
13:00 中午睡了一觉，睡的很死，可能跟最近很累有关吧。
16:40 回出租屋拿村里面人跟我带的行李，拿完又回来上班。
19:30 弄了两块糍粑吃
```

**处理结果：**
```markdown
# 📅 02-24 Tue

---

## 昨日计划完成情况

* [ ] 
* [ ] 
* [ ] 
* [ ] 

---

## 今日记录

武汉天气：⛅️，温度：15°C，湿度：72%

### 上午

---

### 下午

12:00 中午吃的一碗卤肉饭，不是特别想吃，可能跟担心吃多了长胖有关吧。
13:00 中午睡了一觉，睡的很死，可能跟最近很累有关吧。
16:40 回出租屋拿村里面人跟我带的行李，拿完又回来上班。

---

### 晚上

19:30 弄了两块糍粑吃

---

## 状态

* 精力：{{x}} / 10
* 情绪：{{x}} / 10

---

## 健康打卡

* 午餐：卤肉饭
* 晚餐：糍粑
* 运动： 
* 喝水： 

---

## 今日收获

* 
* 
* 

---

## 今日卡点

* 
* 
* 

---

## 感悟

> 

---

## 明日计划

* [ ] 
* [ ] 
* [ ] 
* [ ] 

---
```

### 示例 2：包含运动和喝水

**用户输入：**
```
整理日记：
8:00 起床，今天天气不错
9:30 跑了3公里，感觉精神好多了
12:00 中午吃的牛肉面，味道还行
14:00 喝了500ml水
18:00 晚上吃的火锅
```

**处理结果：**
```markdown
# 📅 02-24 Tue

---

## 昨日计划完成情况

* [ ]
* [ ]
* [ ]
* [ ]

---

## 今日记录

武汉天气：☀️，温度：18°C，湿度：60%

### 上午

8:00 起床，今天天气不错
9:30 跑了3公里，感觉精神好多了

---

### 下午

12:00 中午吃的牛肉面，味道还行
14:00 喝了500ml水

---

### 晚上

18:00 晚上吃的火锅

---

## 状态

* 精力：{{x}} / 10
* 情绪：{{x}} / 10

---

## 健康打卡

* 午餐：牛肉面
* 晚餐：火锅
* 运动：跑了3公里
* 喝水：500ml

---

## 今日收获

*
*
*

---

## 今日卡点

*
*
*

---

## 感悟

>

---

## 明日计划

* [ ]
* [ ]
* [ ]
* [ ]

---
```

### 示例 3：带想法的记录

**用户输入：**
```
整理日记：
8:30  早上吃了碗热干面
12:00 中午吃千张肉丝
18:00 下班，今天下了一个早班，感觉还不错。回到家后发现天还没黑下来，有出门去了一趟公园散步
19:00 在家自己做饭，还是吃豆丝炒腊肠
20:00 本来想继续写日历app的，但是有刷抖音去了，到了20：40才开始写日历app，让ai把前后端都生成出来，但是还是有很多问题

想法
今天同时叫我下下去香港麦理浩径徒步，我看他坐卧铺去深圳然后去香港，看成本很低我也很想去
```

**处理结果：**
```markdown
# 📅 02-24 Tue

---

## 昨日计划完成情况

* [ ]
* [ ]
* [ ]
* [ ]

---

## 今日记录

武汉天气：⛅️，温度：15°C，湿度：72%

### 上午

8:30 早上吃了碗热干面

---

### 下午

12:00 中午吃千张肉丝

---

### 晚上

18:00 下班，今天下了一个早班，感觉还不错。回到家后发现天还没黑下来，有出门去了一趟公园散步
19:00 在家自己做饭，还是吃豆丝炒腊肠
20:00 本来想继续写日历app的，但是有刷抖音去了，到了20：40才开始写日历app，让ai把前后端都生成出来，但是还是有很多问题

---

## 状态

* 精力：{{x}} / 10
* 情绪：{{x}} / 10

---

## 健康打卡

* 午餐：千张肉丝
* 晚餐：豆丝炒腊肠
* 运动：
* 喝水：

---

## 今日收获

*
*
*

---

## 今日卡点

*
*
*

---

## 感悟

今天同时叫我下下去香港麦理浩径徒步，我看他坐卧铺去深圳然后去香港，看成本很低我也很想去

---

## 明日计划

* [ ]
* [ ]
* [ ]
* [ ]

---
```

## 辅助脚本

### scripts/parse_scattered.py

完整的辅助脚本，包含所有解析、分类、提取、生成函数。

```python
#!/usr/bin/env python3
"""
日记记录解析脚本
用于解析时间戳记录、分类、提取健康信息
"""

import re
import subprocess
import json
from datetime import datetime
from typing import List, Tuple, Dict, Optional


def parse_records(input_text: str) -> List[Tuple[str, str]]:
    """
    解析时间戳记录

    Args:
        input_text: 输入文本

    Returns:
        [(时间, 内容), ...]
    """
    records = []
    lines = input_text.strip().split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 匹配时间戳格式：HH:MM 或 H:MM
        match = re.match(r'^(\d{1,2}:\d{2})\s+(.+)$', line)
        if match:
            time_str = match.group(1)
            content = match.group(2)
            records.append((time_str, content))

    return records


def categorize_by_time(records: List[Tuple[str, str]]) -> Dict[str, List[Tuple[str, str]]]:
    """
    按时间段分类记录

    Args:
        records: [(时间, 内容), ...]

    Returns:
        {
            '上午': [...],
            '下午': [...],
            '晚上': [...]
        }
    """
    categorized = {
        '上午': [],
        '下午': [],
        '晚上': []
    }

    for time_str, content in records:
        # 解析时间
        hour, minute = map(int, time_str.split(':'))
        time_minutes = hour * 60 + minute

        # 分类
        if 6 * 60 <= time_minutes < 12 * 60:
            category = '上午'
        elif 12 * 60 <= time_minutes < 18 * 60:
            category = '下午'
        elif 18 * 60 <= time_minutes < 24 * 60:
            category = '晚上'
        else:
            category = '上午'  # 凌晨归入上午

        categorized[category].append((time_str, content))

    return categorized


def extract_meal_content(content: str) -> str:
    """
    提取餐食内容
    """
    # 删除时间描述词
    patterns = [
        r'中午吃的一碗',
        r'中午吃了',
        r'中午吃',
        r'晚上吃了',
        r'晚上吃',
    ]

    result = content
    for pattern in patterns:
        result = re.sub(pattern, '', result)

    return result.strip()


def detect_city(records: List[Tuple[str, str]], default_city: str = '武汉') -> str:
    """
    检测记录中的城市

    Args:
        records: [(时间, 内容), ...]
        default_city: 默认城市

    Returns:
        城市名
    """
    # 合并所有内容
    all_content = ' '.join([content for _, content in records])

    # 城市关键词（优先级高）
    city_keywords = [
        '北京', '上海', '广州', '深圳', '武汉', '成都', '杭州', '重庆',
        '西安', '南京', '天津', '苏州', '长沙', '郑州', '青岛', '大连',
        '厦门', '宁波', '昆明', '合肥', '福州', '哈尔滨', '济南', '珠海'
    ]

    # 优先检测主要城市
    for city in city_keywords:
        if city in all_content:
            return city

    # 检测其他城市（常见模式）
    city_patterns = [
        r'(\w{2,4})市',
        r'去(\w{2,4})',
        r'在(\w{2,4})',
        r'回(\w{2,4})',
        r'到(\w{2,4})'
    ]

    for pattern in city_patterns:
        matches = re.findall(pattern, all_content)
        if matches:
            # 返回第一个匹配的城市
            return matches[0]

    # 使用默认城市
    return default_city


def get_weather(city: str) -> Optional[dict]:
    """
    获取城市天气

    Args:
        city: 城市名

    Returns:
        天气信息字典，或 None（失败时）
    """
    try:
        # 使用 wttr.in API（通过 curl）
        url = f"https://wttr.in/{city}?lang=zh&format=j1"
        result = subprocess.run(
            ['curl', '-s', url],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            return None

        data = json.loads(result.stdout)

        # 提取当前天气
        current = data['current_condition'][0]

        weather_info = {
            'city': city,
            'temp': current['temp_C'],  # 温度（摄氏度）
            'condition': current['lang_zh'][0]['value'],  # 天气描述
            'humidity': current['humidity'],  # 湿度
            'wind': current['windspeedKmph'],  # 风速
        }

        return weather_info

    except Exception as e:
        print(f"获取天气失败: {e}")
        return None


def format_weather(weather_info: Optional[dict]) -> str:
    """
    格式化天气信息

    Args:
        weather_info: 天气信息字典

    Returns:
        格式化的天气字符串
    """
    if not weather_info:
        return "天气信息获取失败"

    city = weather_info['city']
    temp = weather_info['temp']
    condition = weather_info['condition']
    humidity = weather_info['humidity']

    # 天气描述简化
    condition_map = {
        '晴': '☀️',
        '多云': '⛅️',
        '阴': '☁️',
        '雨': '🌧️',
        '小雨': '🌧️',
        '中雨': '🌧️',
        '大雨': '⛈️',
        '暴雨': '⛈️',
        '雪': '❄️',
        '小雪': '❄️',
        '中雪': '❄️',
        '大雪': '❄️',
        '雾': '🌫️',
        '霾': '😷'
    }

    icon = condition_map.get(condition, '🌤️')

    return f"{city}天气：{icon}，温度：{temp}°C，湿度：{humidity}%"


def extract_health_info(records: List[Tuple[str, str]]) -> Dict[str, str]:
    """
    提取健康信息

    Args:
        records: [(时间, 内容), ...]

    Returns:
        {
            '午餐': '内容',
            '晚餐': '内容',
            '运动': '内容',
            '喝水': '内容'
        }
    """
    health_info = {
        '午餐': '',
        '晚餐': '',
        '运动': '',
        '喝水': ''
    }

    lunch_keywords = ['午餐', '午饭', '中午吃', '中午饭', '吃的一碗']
    dinner_keywords = ['晚餐', '晚饭', '晚上吃', '晚饭']
    exercise_keywords = ['跑步', '走路', '健身', '锻炼', '运动', '打球']
    water_keywords = ['喝水', '喝水', '喝水', '水']

    for time_str, content in records:
        # 提取午餐
        if any(kw in content for kw in lunch_keywords) and not health_info['午餐']:
            health_info['午餐'] = extract_meal_content(content)

        # 提取晚餐
        if any(kw in content for kw in dinner_keywords) and not health_info['晚餐']:
            health_info['晚餐'] = extract_meal_content(content)

        # 提取运动
        if any(kw in content for kw in exercise_keywords) and not health_info['运动']:
            health_info['运动'] = content

        # 提取喝水
        if any(kw in content for kw in water_keywords) and not health_info['喝水']:
            health_info['喝水'] = content

    return health_info


def get_weekday(year: int, month: int, day: int) -> str:
    """
    获取星期

    Args:
        year: 年
        month: 月
        day: 日

    Returns:
        星期英文缩写（如 'Tue'）
    """
    weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    return weekdays[datetime(year, month, day).weekday()]


def generate_template(date: str, weekday: str, weather_str: str, categorized: Dict[str, List[Tuple[str, str]]], health_info: Dict[str, str]) -> str:
    """
    生成日记模版

    Args:
        date: 日期（如 '02-24'）
        weekday: 星期英文缩写（如 'Tue'）
        weather_str: 天气信息字符串
        categorized: 分类后的记录
        health_info: 健康信息

    Returns:
        完整模版内容
    """
    template = f"""# 📅 {date} {weekday}

---

## 昨日计划完成情况

* [ ]
* [ ]
* [ ]
* [ ]

---

## 今日记录

{weather_str}

### 上午

"""

    # 填充上午记录
    if categorized['上午']:
        for time_str, content in categorized['上午']:
            template += f"{time_str} {content}\n"
    else:
        template += "---\n\n"

    template += "---\n\n### 下午\n\n"

    # 填充下午记录
    if categorized['下午']:
        for time_str, content in categorized['下午']:
            template += f"{time_str} {content}\n"
    else:
        template += "---\n\n"

    template += "---\n\n### 晚上\n\n"

    # 填充晚上记录
    if categorized['晚上']:
        for time_str, content in categorized['晚上']:
            template += f"{time_str} {content}\n"
    else:
        template += "---\n\n"

    template += """---

## 状态

* 精力：{{x}} / 10
* 情绪：{{x}} / 10

---

## 健康打卡

* 午餐：{lunch}
* 晚餐：{dinner}
* 运动：{exercise}
* 喝水：{water}

---

## 今日收获

*
*
*

---

## 今日卡点

*
*
*

---

## 感悟

>

---

## 明日计划

* [ ]
* [ ] 
* [ ] 
* [ ] 

---
""".format(
        lunch=health_info['午餐'] or '',
        dinner=health_info['晚餐'] or '',
        exercise=health_info['运动'] or '',
        water=health_info['喝水'] or ''
    )

    return template


if __name__ == '__main__':
    # 测试
    test_input = """12:00 中午吃的一碗卤肉饭，不是特别想吃，可能跟担心吃多了长胖有关吧。
13:00 中午睡了一觉，睡的很死，可能跟最近很累有关吧。
16:40 回出租屋拿村里面人跟我带的行李，拿完又回来上班。
19:30 弄了两块糍粑吃"""

    records = parse_records(test_input)
    print("解析结果：")
    for record in records:
        print(f"  {record}")

    # 检测城市
    city = detect_city(records, default_city='武汉')
    print(f"\n检测到城市：{city}")

    # 获取天气
    weather_info = get_weather(city)
    weather_str = format_weather(weather_info)
    print(f"天气信息：{weather_str}")

    categorized = categorize_by_time(records)
    print("\n分类结果：")
    for category, items in categorized.items():
        print(f"  {category}: {len(items)} 条")
        for item in items:
            print(f"    {item}")

    health_info = extract_health_info(records)
    print("\n健康信息：")
    for key, value in health_info.items():
        print(f"  {key}: {value}")

    date = datetime.now().strftime('%m-%d')
    weekday = get_weekday(datetime.now().year, datetime.now().month, datetime.now().day)

    template = generate_template(date, weekday, weather_str, categorized, health_info)
    print("\n生成的模版：")
    print(template)
```

## 使用方式

### 快速开始

```text
用户: 整理日记：
12:00 中午吃的一碗卤肉饭，不是特别想吃，可能跟担心吃多了长胖有关吧。
13:00 中午睡了一觉，睡的很死，可能跟最近很累有关吧。
16:40 回出租屋拿村里面人跟我带的行李，拿完又回来上班。
19:30 弄了两块糍粑吃

Claude: [执行完整流程]
- Git 拉取
- 解析记录
- 检测城市并获取天气
- 分类整理
- 提取健康信息
- 润色文本
- 生成模版（含天气）
- 保存文件
- Git 推送

✅ 日记整理完成！已保存到：2026/02/02-24.md
```

### 脚本调用

```bash
# 测试脚本
python3 /home/xh/.agents/skills/diary-scatter-organizer/scripts/parse_scattered.py
```

## 错误处理

| 错误 | 处理 |
|------|------|
| Git 拉取失败 | 跳过拉取，继续整理 |
| 天气获取失败 | 使用默认天气信息，继续整理 |
| 时间解析失败 | 跳过该行，继续处理 |
| 文件写入失败 | 提示用户检查权限 |
| Git 推送失败 | 提示用户检查网络 |
| 文件已存在 | 询问用户是否覆盖 |
