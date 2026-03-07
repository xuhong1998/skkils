#!/usr/bin/env python3
"""
日记记录解析脚本
用于解析时间戳记录、分类、提取健康信息
"""

import re
import urllib.request
import urllib.parse
import urllib.error
import json
from datetime import datetime
from typing import List, Tuple, Dict, Optional, Any

# 默认城市
DEFAULT_CITY = "武汉"

# 高德天气 API Key
AMAP_API_KEY = "ccd040563b7519fe4b8489ff567d2cac"

# 高德天气 API 端点
AMAP_WEATHER_URL = "https://restapi.amap.com/v3/weather/weatherInfo"

# 主要城市列表（优先检测）
MAJOR_CITIES = [
    "北京", "上海", "广州", "深圳", "武汉", "成都", "杭州", "重庆",
    "西安", "南京", "天津", "苏州", "长沙", "郑州", "青岛", "大连",
    "厦门", "宁波", "昆明", "合肥", "福州", "哈尔滨", "济南", "珠海"
]

# 城市编码映射（部分主要城市）
CITY_CODE_MAP = {
    "北京": "110000",
    "上海": "310000",
    "广州": "440100",
    "深圳": "440300",
    "武汉": "420100",
    "成都": "510100",
    "杭州": "330100",
    "重庆": "500000",
    "西安": "610100",
    "南京": "320100",
    "天津": "120000",
    "苏州": "320500",
    "长沙": "430100",
    "郑州": "410100",
    "青岛": "370200",
    "大连": "210200",
    "厦门": "350200",
    "宁波": "330200",
    "昆明": "530100",
    "合肥": "340100",
    "福州": "350100",
    "哈尔滨": "230100",
    "济南": "370100",
    "珠海": "440400"
}

# 天气图标映射
WEATHER_ICONS = {
    "晴": "☀️",
    "多云": "⛅️",
    "阴": "☁️",
    "雨": "🌧️",
    "小雨": "🌧️",
    "中雨": "🌧️",
    "大雨": "⛈️",
    "暴雨": "⛈️",
    "雪": "❄️",
    "小雪": "❄️",
    "中雪": "❄️",
    "大雪": "❄️",
    "雾": "🌫️",
    "霾": "😷",
    "沙尘暴": "🌪️"
}


def detect_city(text: str, default_city: str = DEFAULT_CITY) -> str:
    """
    从文本中检测城市名

    Args:
        text: 输入文本
        default_city: 默认城市

    Returns:
        城市名
    """
    # 优先检测主要城市
    for city in MAJOR_CITIES:
        if city in text:
            return city

    # 检测其他城市（常见模式）
    city_patterns = [
        r"([\u4e00-\u9fa5]{2,4})市"  # 只匹配中文字符后跟"市"
    ]

    for pattern in city_patterns:
        matches = re.findall(pattern, text)
        if matches:
            # 过滤掉明显不是城市的词
            excluded_words = ["没有", "这个", "那个", "哪里", "所有", "其他", "没有城"]
            for match in matches:
                if len(match) >= 2 and match not in excluded_words:
                    return match + "市"  # 返回完整城市名

    # 使用默认城市
    return default_city


def get_weather(city: str, timeout: int = 10) -> Optional[dict]:
    """
    获取城市天气（使用高德天气 API）

    Args:
        city: 城市名
        timeout: 超时时间（秒）

    Returns:
        天气信息字典，或 None（失败时）
    """
    try:
        # 获取城市编码
        city_code = CITY_CODE_MAP.get(city, city)

        # 构造请求参数
        params = {
            "key": AMAP_API_KEY,
            "city": city_code,
            "extensions": "base",  # 基础天气
            "output": "JSON"
        }

        url = f"{AMAP_WEATHER_URL}?{urllib.parse.urlencode(params)}"

        # 发送请求
        response = urllib.request.urlopen(url, timeout=timeout)
        data = json.loads(response.read().decode('utf-8'))

        # 检查响应
        if data.get("status") == "1" and data.get("lives"):
            lives = data["lives"][0]

            weather_info = {
                "city": city,
                "temp": lives.get("temperature", ""),  # 温度（摄氏度）
                "condition": lives.get("weather", ""),  # 天气描述
                "humidity": lives.get("humidity", ""),  # 湿度
                "wind": lives.get("winddirection", ""),  # 风向
            }

            return weather_info
        else:
            status = data.get("status", "unknown")
            info = data.get("info", "unknown error")
            print(f"获取天气失败：{status} - {info}")
            return None

    except urllib.error.URLError as e:
        print(f"获取天气网络错误：{e}")
        return None
    except Exception as e:
        print(f"获取天气失败：{e}")
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

    city = weather_info["city"]
    temp = weather_info["temp"]
    condition = weather_info["condition"]
    humidity = weather_info["humidity"]

    # 获取天气图标
    icon = WEATHER_ICONS.get(condition, "🌤️")

    return f"{icon} {condition}，温度：{temp}°C，湿度：{humidity}%"


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


def parse_records(input_text: str) -> List[Tuple[str, str]]:
    """
    解析时间戳记录（保留兼容性）

    Args:
        input_text: 输入文本

    Returns:
        [(时间, 内容), ...]
    """
    result = parse_input(input_text)
    return result["records"]


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
    weather_str: str = "",
    ideas: str = "",
) -> str:
    """
    生成日记模版

    Args:
        date: 日期（如 '02-24'）
        weekday: 星期（如 '星期二'）
        categorized: 分类后的记录
        health_info: 健康信息
        weather_str: 天气信息字符串（可选）
        ideas: 想法内容（可选）

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

{ideas if ideas else ">"}

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
    # 测试1：基本记录
    test_input = """12:00 中午吃的一碗卤肉饭，不是特别想吃，可能跟担心吃多了长胖有关吧。
13:00 中午睡了一觉，睡的很死，可能跟最近很累有关吧。
16:40 回出租屋拿村里面人跟我带的行李，拿完又回来上班。
19:30 弄了两块糍粑吃"""

    print("=" * 50)
    print("测试1：基本记录（无想法）")
    print("=" * 50)

    result = parse_input(test_input)
    records = result["records"]
    ideas = result["ideas"]

    print("\n解析结果：")
    for record in records:
        print(f"  {record}")
    print(f"\n想法：{'(无)' if not ideas else ideas}")

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

    # 获取天气信息
    weather_str = ""
    print("\n正在获取天气信息...")
    all_content = " ".join([content for _, content in records])
    city = detect_city(all_content, default_city="武汉")
    print(f"检测到城市：{city}")

    weather_info = get_weather(city)
    if weather_info:
        weather_str = format_weather(weather_info)
        print(f"天气信息：{weather_str}")
    else:
        print("天气信息获取失败（使用默认信息）")

    date = datetime.now().strftime("%m-%d")
    weekday = get_weekday(datetime.now().year, datetime.now().month, datetime.now().day)

    template = generate_template(date, weekday, categorized, health_info, weather_str, ideas)
    print("\n生成的模版：")
    print(template)

    # 测试2：带想法的记录
    test_input_with_ideas = """8:30  早上吃了碗热干面
12:00 中午吃千张肉丝
18:00 下班，今天下了一个早班，感觉还不错。回到家后发现天还没黑下来，有出门去了一趟公园散步
19:00 在家自己做饭，还是吃豆丝炒腊肠
20:00 本来想继续写日历app的，但是有刷抖音去了，到了20：40才开始写日历app，让ai把前后端都生成出来，但是还是有很多问题

想法
今天同时叫我下下去香港麦理浩径徒步，我看他坐卧铺去深圳然后去香港，看成本很低我也很想去"""

    print("\n\n")
    print("=" * 50)
    print("测试2：带想法的记录")
    print("=" * 50)

    result2 = parse_input(test_input_with_ideas)
    records2 = result2["records"]
    ideas2 = result2["ideas"]

    print("\n解析结果：")
    for record in records2:
        print(f"  {record}")
    print(f"\n想法：{ideas2}")

    categorized2 = categorize_by_time(records2)
    print("\n分类结果：")
    for category, items in categorized2.items():
        print(f"  {category}: {len(items)} 条")
        for item in items:
            print(f"    {item}")

    health_info2 = extract_health_info(records2)
    print("\n健康信息：")
    for key, value in health_info2.items():
        print(f"  {key}: {value}")

    date2 = datetime.now().strftime("%m-%d")
    weekday2 = get_weekday(datetime.now().year, datetime.now().month, datetime.now().day)

    template2 = generate_template(date2, weekday2, categorized2, health_info2, weather_str, ideas2)
    print("\n生成的模版：")
    print(template2)
