#!/usr/bin/env python3
"""
处理日记：整理记录、获取天气、保存到文件、Git 推送
"""

import sys
import os
import subprocess
from datetime import datetime

# 添加脚本路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'diary-scatter-organizer/scripts'))

from parse_scattered import (
    parse_input,
    categorize_by_time,
    extract_health_info,
    get_weekday,
    generate_template,
    get_weather,
    format_weather,
    detect_city,
    DEFAULT_CITY
)

# 日记路径配置
DIARY_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "diary")


def save_diary(template: str, date: str, weekday: str) -> str:
    """
    保存日记到文件

    Args:
        template: 日记内容
        date: 日期（MM-DD）
        weekday: 星期（如 'Mon'）

    Returns:
        保存的文件路径
    """
    now = datetime.now()
    year = str(now.year)
    month = now.strftime("%m")
    weekday_cn = get_weekday(now.year, now.month, now.day)

    # 文件名格式：MM-DD-WeekDay.md
    filename = f"{date}-{weekday}.md"

    # 完整路径
    dir_path = os.path.join(DIARY_PATH, year, month)
    file_path = os.path.join(dir_path, filename)

    # 创建目录
    os.makedirs(dir_path, exist_ok=True)

    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(template)

    return file_path


def git_operations(file_path: str):
    """
    Git 操作：拉取、添加、提交、推送

    Args:
        file_path: 日记文件路径
    """
    print("\n" + "=" * 60)
    print("Git 操作")
    print("=" * 60)

    # 1. Git 拉取
    print("\n1. Git 拉取...")
    os.chdir(DIARY_PATH)
    try:
        subprocess.run(["git", "pull", "origin", "main"],
                      capture_output=True, text=True, check=True)
        print("  ✓ 拉取成功")
    except subprocess.CalledProcessError as e:
        print(f"  ✗ 拉取失败：{e.stderr}")

    # 2. Git 添加
    print("\n2. Git 添加...")
    try:
        subprocess.run(["git", "add", file_path],
                      capture_output=True, text=True, check=True)
        print(f"  ✓ 已添加：{file_path}")
    except subprocess.CalledProcessError as e:
        print(f"  ✗ 添加失败：{e.stderr}")

    # 3. Git 提交
    print("\n3. Git 提交...")
    now = datetime.now()
    commit_msg = f"update: {now.strftime('%Y-%m-%d')}"
    try:
        subprocess.run(["git", "commit", "-m", commit_msg],
                      capture_output=True, text=True, check=True)
        print(f"  ✓ 提交成功：{commit_msg}")
    except subprocess.CalledProcessError as e:
        print(f"  ✗ 提交失败：{e.stderr}")

    # 4. Git 推送
    print("\n4. Git 推送...")
    try:
        subprocess.run(["git", "push", "origin", "main"],
                      capture_output=True, text=True, check=True)
        print("  ✓ 推送成功")
    except subprocess.CalledProcessError as e:
        print(f"  ✗ 推送失败：{e.stderr}")


def process_diary(input_text: str):
    """
    完整的日记处理流程

    Args:
        input_text: 用户输入的日记文本
    """
    print("=" * 60)
    print("开始整理日记...")
    print("=" * 60)

    # 1. 解析输入
    print("\n1. 解析日记记录...")
    result = parse_input(input_text)
    records = result["records"]
    ideas = result["ideas"]

    print(f"  ✓ 解析到 {len(records)} 条记录")
    print(f"  ✓ 想法：{'有' if ideas else '无'}")

    # 2. 分类
    print("\n2. 按时间段分类...")
    categorized = categorize_by_time(records)
    for category, items in categorized.items():
        print(f"  {category}：{len(items)} 条")

    # 3. 提取健康信息
    print("\n3. 提取健康信息...")
    health_info = extract_health_info(records)
    for key, value in health_info.items():
        if value:
            print(f"  {key}：{value}")

    # 4. 获取天气
    print("\n4. 获取天气信息...")
    all_content = ' '.join([content for _, content in records])
    city = detect_city(all_content, default_city=DEFAULT_CITY)
    print(f"  检测到城市：{city}")

    weather_info = get_weather(city)
    weather_str = ""
    if weather_info:
        weather_str = format_weather(weather_info)
        print(f"  {weather_str}")
    else:
        print("  ⚠ 天气信息获取失败，使用默认信息")
        weather_str = f"{city}天气：⛅️（天气信息暂时无法获取）"

    # 5. 生成模版
    print("\n5. 生成日记模版...")
    date = datetime.now().strftime("%m-%d")
    weekday_cn = get_weekday(datetime.now().year, datetime.now().month, datetime.now().day)
    weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][datetime.now().weekday()]

    template = generate_template(date, weekday_cn, categorized, health_info, weather_str, ideas)
    print("  ✓ 模版生成完成")

    # 6. 保存到文件
    print("\n6. 保存日记到文件...")
    file_path = save_diary(template, date, weekday)
    print(f"  ✓ 已保存到：{file_path}")

    # 7. Git 操作
    git_operations(file_path)

    # 8. 完成
    print("\n" + "=" * 60)
    print("✓ 日记整理完成！")
    print("=" * 60)

    return file_path


def main():
    """主函数"""
    if len(sys.argv) > 1:
        # 从命令行参数读取输入文本
        input_text = sys.argv[1]
    else:
        # 从标准输入读取
        input_text = sys.stdin.read().strip()
        if not input_text:
            print("请输入日记记录")
            sys.exit(1)

    process_diary(input_text)


if __name__ == "__main__":
    main()
