#!/usr/bin/env python3
"""
天气获取脚本
支持自动城市检测和实时天气查询（使用高德天气 API）
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import sys
from typing import Optional

# 默认城市
DEFAULT_CITY = "武汉"

# 高德天气 API Key
AMAP_API_KEY = "ccd040563b7519fe4b8489ff567d2cac"

# 高德天气 API 端点
AMAP_WEATHER_URL = "https://restapi.amap.com/v3/weather/weatherInfo"
AMAP_DISTRICT_URL = "https://restapi.amap.com/v3/config/district"

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
    import re
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
    格式化天气信息（简洁格式）

    Args:
        weather_info: 天气信息字典

    Returns:
        格式化的天气字符串
    """
    if not weather_info:
        return "天气信息获取失败"

    temp = weather_info["temp"]
    condition = weather_info["condition"]
    humidity = weather_info["humidity"]

    # 获取天气图标
    icon = WEATHER_ICONS.get(condition, "🌤️")

    return f"{icon} {condition}，温度：{temp}°C，湿度：{humidity}%"


def format_weather_detail(weather_info: Optional[dict]) -> str:
    """
    格式化天气信息（详细格式）

    Args:
        weather_info: 天气信息字典

    Returns:
        格式化的天气字符串（JSON）
    """
    if not weather_info:
        return "天气信息获取失败"

    return json.dumps(weather_info, ensure_ascii=False, indent=2)


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="获取城市天气（高德天气 API）")
    parser.add_argument("city", nargs="?", help="城市名，不指定则从标准输入检测")
    parser.add_argument("--format", "-f", choices=["simple", "detail", "json"],
                       default="simple", help="输出格式：simple（简洁）| detail（详细）| json")

    args = parser.parse_args()

    # 获取城市
    if args.city:
        city = args.city
    else:
        # 从标准输入读取
        text = sys.stdin.read().strip()
        if not text:
            print("请提供城市名或输入文本")
            sys.exit(1)
        city = detect_city(text)
        print(f"检测到城市：{city}")

    # 获取天气
    weather_info = get_weather(city)

    # 格式化输出
    output = ""
    if args.format == "simple":
        output = format_weather(weather_info)
    elif args.format == "detail":
        output = format_weather_detail(weather_info)
    elif args.format == "json":
        output = json.dumps(weather_info, ensure_ascii=False, indent=2) if weather_info else "{}"

    if output:
        print(output)


if __name__ == "__main__":
    main()
