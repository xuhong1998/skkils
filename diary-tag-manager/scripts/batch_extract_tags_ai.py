#!/usr/bin/env python3
"""
基于AI的批量标签提取脚本
扫描 ../diary/2026 目录下所有日记，为没有标签的日记使用AI提取标签
"""

import os
import re
from pathlib import Path
import sys
import subprocess
import tempfile

# 日记目录
DIARY_DIR = Path("/Users/xuhong/individual/diary/2026")

# 标签块标记
TAG_MARKER = "## 🏷️ AI提取标签"

def has_tags(file_path):
    """检查文件是否已经有标签"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return TAG_MARKER in content
    except Exception as e:
        print(f"读取文件失败 {file_path}: {e}")
        return False

def get_diary_content(file_path):
    """读取日记内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"读取文件失败 {file_path}: {e}")
        return None

def scan_diaries():
    """扫描所有日记文件"""
    diaries = []
    for month_dir in sorted(DIARY_DIR.iterdir()):
        if month_dir.is_dir():
            for diary_file in sorted(month_dir.glob("*.md")):
                full_path = str(diary_file)
                has_tag = has_tags(full_path)
                diaries.append({
                    'path': full_path,
                    'relative_path': full_path.replace(str(DIARY_DIR) + '/', ''),
                    'has_tag': has_tag
                })
    return diaries

def write_diary_content(file_path, content):
    """写日记内容到文件"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"写入文件失败 {file_path}: {e}")
        return False

def get_diaries_to_process():
    """获取需要处理的日记列表（没有标签的）"""
    diaries = scan_diaries()
    return [d for d in diaries if not d['has_tag']]

if __name__ == "__main__":
    # 扫描所有日记
    diaries = scan_diaries()
    
    # 统计
    total = len(diaries)
    with_tags = sum(1 for d in diaries if d['has_tag'])
    without_tags = total - with_tags
    
    print("=" * 60)
    print("批量提取日记标签 (AI方式)")
    print("=" * 60)
    print(f"\n📊 统计信息:")
    print(f"   总日记数: {total}")
    print(f"   已有标签: {with_tags}")
    print(f"   需要处理: {without_tags}")
    
    if without_tags > 0:
        # 输出需要处理的日记列表
        print(f"\n📋 需要处理的日记:")
        for i, d in enumerate([d for d in diaries if not d['has_tag']], 1):
            print(f"   {i}. {d['relative_path']}")
        
        print(f"\n💡 请使用AI处理这些日记，为每篇日记提取标签")
    else:
        print("\n✅ 所有日记都已处理！")
