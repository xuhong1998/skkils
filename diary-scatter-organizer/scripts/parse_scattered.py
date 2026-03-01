#!/usr/bin/env python3
"""
日记记录解析脚本
用于解析时间戳记录、分类、提取健康信息
"""

import re
from datetime import datetime
from typing import List, Tuple, Dict


def parse_records(input_text: str) -> List[Tuple[str, str]]:
    """
    解析时间戳记录

    Args:
        input_text: 输入文本

    Returns:
        [(时间, 内容), ...]
    """
    records = []
    lines = input_text.strip().split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 匹配时间戳格式：HH:MM 或 H:MM
        match = re.match(r"^(\d{1,2}:\d{2})\s+(.+)$", line)
        if match:
            time_str = match.group(1)
            content = match.group(2)
            records.append((time_str, content))

    return records


def categorize_by_time(
    records: List[Tuple[str, str]],
) -> Dict[str, List[Tuple[str, str]]]:
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
    categorized = {"上午": [], "下午": [], "晚上": []}

    for time_str, content in records:
        # 解析时间
        hour, minute = map(int, time_str.split(":"))
        time_minutes = hour * 60 + minute

        # 分类
        if 6 * 60 <= time_minutes < 12 * 60:
            category = "上午"
        elif 12 * 60 <= time_minutes < 18 * 60:
            category = "下午"
        elif 18 * 60 <= time_minutes < 24 * 60:
            category = "晚上"
        else:
            category = "上午"  # 凌晨归入上午

        categorized[category].append((time_str, content))

    return categorized


def extract_meal_content(content: str) -> str:
    """
    提取餐食内容
    只提取餐食名称，不包含评价或描述
    """
    # 删除时间描述词和冗余描述
    patterns = [
        r"中午吃的一碗",
        r"中午吃了",
        r"中午吃",
        r"晚上吃了",
        r"晚上吃",
        r"弄了两块",
        r"吃",
        r"的",  # 删除"的"字
    ]

    result = content
    for pattern in patterns:
        result = re.sub(pattern, "", result)

    # 删除逗号和标点以及后面的描述（从第一个逗号开始截断）
    result = re.sub(r"[，。、；：,.;:].*$", "", result)

    return result.strip()


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
    health_info = {"午餐": "", "晚餐": "", "运动": "", "喝水": ""}

    lunch_keywords = ["午餐", "午饭", "中午吃", "中午饭", "吃的一碗"]
    dinner_keywords = ["晚餐", "晚饭", "晚上吃", "弄了几块", "弄了两块", "做了", "吃了"]
    exercise_keywords = ["跑步", "走了", "健身", "锻炼", "运动", "打球", "跑了", "走了"]
    water_keywords = ["喝水", "喝了", "喝水", "水"]

    for time_str, content in records:
        # 提取午餐
        if any(kw in content for kw in lunch_keywords) and not health_info["午餐"]:
            health_info["午餐"] = extract_meal_content(content)

        # 提取晚餐
        if any(kw in content for kw in dinner_keywords) and not health_info["晚餐"]:
            # 如果是晚上时间段的记录，优先认为是晚餐
            hour, minute = map(int, time_str.split(":"))
            time_minutes = hour * 60 + minute
            if 18 * 60 <= time_minutes < 24 * 60:
                health_info["晚餐"] = extract_meal_content(content)

        # 提取运动
        if any(kw in content for kw in exercise_keywords) and not health_info["运动"]:
            health_info["运动"] = content

        # 提取喝水
        if any(kw in content for kw in water_keywords) and not health_info["喝水"]:
            health_info["喝水"] = content

    return health_info


def get_weekday(year: int, month: int, day: int) -> str:
    """
    获取星期

    Args:
        year: 年
        month: 月
        day: 日

    Returns:
        星期（如 '星期二'）
    """
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    return weekdays[datetime(year, month, day).weekday()]


def generate_template(
    date: str,
    weekday: str,
    categorized: Dict[str, List[Tuple[str, str]]],
    health_info: Dict[str, str],
) -> str:
    """
    生成日记模版

    Args:
        date: 日期（如 '02-24'）
        weekday: 星期（如 '星期二'）
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

### 上午

"""

    # 填充上午记录
    if categorized["上午"]:
        for time_str, content in categorized["上午"]:
            template += f"{time_str} {content}\n"
    else:
        template += "---\n\n"

    template += "---\n\n### 下午\n\n"

    # 填充下午记录
    if categorized["下午"]:
        for time_str, content in categorized["下午"]:
            template += f"{time_str} {content}\n"
    else:
        template += "---\n\n"

    template += "---\n\n### 晚上\n\n"

    # 填充晚上记录
    if categorized["晚上"]:
        for time_str, content in categorized["晚上"]:
            template += f"{time_str} {content}\n"
    else:
        template += "---\n\n"

    template += f"""---

## 状态

* 精力：{{{{x}}}} / 10
* 情绪：{{{{x}}}} / 10

---

## 健康打卡

* 午餐：{health_info["午餐"] or ""}
* 晚餐：{health_info["晚餐"] or ""}
* 运动：{health_info["运动"] or ""}
* 喝水：{health_info["喝水"] or ""}

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
"""

    return template


if __name__ == "__main__":
    # 测试
    test_input = """12:00 中午吃的一碗卤肉饭，不是特别想吃，可能跟担心吃多了长胖有关吧。
13:00 中午睡了一觉，睡的很死，可能跟最近很累有关吧。
16:40 回出租屋拿村里面人跟我带的行李，拿完又回来上班。
19:30 弄了两块糍粑吃"""

    records = parse_records(test_input)
    print("解析结果：")
    for record in records:
        print(f"  {record}")

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

    date = datetime.now().strftime("%m-%d")
    weekday = get_weekday(datetime.now().year, datetime.now().month, datetime.now().day)

    template = generate_template(date, weekday, categorized, health_info)
    print("\n生成的模版：")
    print(template)
