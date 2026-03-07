#!/usr/bin/env python3
"""
测试天气功能的基本逻辑（不依赖外部 API）
"""

import sys
import os

# 添加 weather-cn skill 的脚本路径到 Python 路径
weather_cn_script = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "weather-cn",
    "scripts"
)
sys.path.insert(0, weather_cn_script)

from get_weather import detect_city, WEATHER_ICONS

def test_city_detection():
    """测试城市检测功能"""
    print("=" * 50)
    print("测试城市检测功能")
    print("=" * 50)

    test_cases = [
        ("今天在北京上班，天气不错", "北京"),
        ("准备去上海参加会议", "上海"),
        ("武汉的天气真是不错", "武汉"),
        ("回广州的路上", "广州"),
        ("没有城市信息", "武汉"),  # 默认城市
    ]

    all_passed = True
    for text, expected_city in test_cases:
        detected_city = detect_city(text, default_city="武汉")
        passed = detected_city == expected_city
        status = "✅" if passed else "❌"
        print(f"{status} 文本: {text}")
        print(f"   期望: {expected_city}, 实际: {detected_city}")
        if not passed:
            all_passed = False

    print()
    return all_passed

def test_weather_icons():
    """测试天气图标映射"""
    print("=" * 50)
    print("测试天气图标映射")
    print("=" * 50)

    test_cases = [
        ("晴", "☀️"),
        ("多云", "⛅️"),
        ("阴", "☁️"),
        ("雨", "🌧️"),
        ("雪", "❄️"),
    ]

    all_passed = True
    for condition, expected_icon in test_cases:
        icon = WEATHER_ICONS.get(condition, "🌤️")
        passed = icon == expected_icon
        status = "✅" if passed else "❌"
        print(f"{status} {condition}: {icon}")
        if not passed:
            all_passed = False

    print()
    return all_passed

def main():
    """运行所有测试"""
    print()
    print("🧪 Weather-CN Skill 功能测试")
    print()

    test_results = []

    # 运行测试
    test_results.append(("城市检测", test_city_detection()))
    test_results.append(("天气图标", test_weather_icons()))

    # 汇总结果
    print("=" * 50)
    print("测试结果汇总")
    print("=" * 50)

    for test_name, passed in test_results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{status} - {test_name}")

    all_passed = all(passed for _, passed in test_results)

    print()
    if all_passed:
        print("🎉 所有测试通过！")
    else:
        print("⚠️ 部分测试失败，请检查")

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
