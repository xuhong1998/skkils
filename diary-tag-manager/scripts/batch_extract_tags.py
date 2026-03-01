#!/usr/bin/env python3
"""
批量提取日记标签脚本
扫描 ../diary/2026 目录下所有日记，为没有标签的日记提取标签
"""

import os
import re
from pathlib import Path
import sys

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

def generate_tag_block(diary_content, date_str):
    """
    基于日记内容生成标签块
    这是一个简化的标签提取逻辑，实际应该使用AI
    """
    # 分析日记内容，提取关键词
    content_lower = diary_content.lower()
    
    # 主要标签
    main_tags = []
    if any(keyword in content_lower for keyword in ['基金', '股票', '黄金', '白银', '投资', '亏', '赚']):
        main_tags.append('#投资理财')
    if any(keyword in content_lower for keyword in ['抖音', '刷', '短视频', '手机']):
        main_tags.append('#数字成瘾')
    if any(keyword in content_lower for keyword in ['学习', '读', '书', '思考', '计划']):
        main_tags.append('#学习成长')
    if any(keyword in content_lower for keyword in ['散步', '运动', '走', '洗澡', '洗衣服']):
        main_tags.append('#生活日常')
    if any(keyword in content_lower for keyword in ['吃饭', '饮食', '外卖', '买菜', '做饭']):
        main_tags.append('#生活日常')
    if '公司' in content_lower or '年会' in content_lower or '上班' in content_lower:
        main_tags.append('#工作职业')
    
    # 如果没有主要标签，添加默认标签
    if not main_tags:
        main_tags.append('#生活日常')
    
    # 限制主要标签数量
    main_tags = main_tags[:5]
    
    # 子标签
    sub_tags = []
    if '散步' in content_lower:
        sub_tags.append('#散步')
    if '走楼梯' in content_lower:
        sub_tags.append('#走楼梯')
    if '洗衣服' in content_lower:
        sub_tags.append('#家政')
    if '做饭' in content_lower or '外卖' in content_lower:
        sub_tags.append('#饮食')
    if '学习' in content_lower:
        sub_tags.append('#学习')
    if '基金' in content_lower:
        sub_tags.append('#基金交易')
    if '刷抖音' in content_lower or '抖音' in content_lower:
        sub_tags.append('#抖音使用')
    
    # 情绪标签
    emotion_tags = []
    if any(keyword in content_lower for keyword in ['开心', '满足', '不错', '挺好']):
        emotion_tags.append('#开心')
    elif any(keyword in content_lower for keyword in ['焦虑', '烦躁', '压力']):
        emotion_tags.append('#焦虑')
    elif any(keyword in content_lower for keyword in ['亏', '损失', '后悔']):
        emotion_tags.append('#沮丧')
    elif any(keyword in content_lower for keyword in ['反思', '感悟', '思考']):
        emotion_tags.append('#反思')
    else:
        emotion_tags.append('#平静')
    
    # 地点标签
    location_tags = []
    if '武汉' in content_lower or '家中' in content_lower or '家' in content_lower:
        location_tags.append('#家中')
    if '公司' in content_lower:
        location_tags.append('#公司')
    if '公园' in content_lower:
        location_tags.append('#公园')
    
    if not location_tags:
        location_tags.append('#家中')
    
    # 生成标签块
    tag_block = f"""---
## 🏷️ AI提取标签

### 主要标签
{' '.join(main_tags)}

### 子标签
{' '.join(sub_tags) if sub_tags else '#日常'}

### 情绪标签
{' '.join(emotion_tags)}

### 地点标签
{' '.join(location_tags)}

---

"""
    
    return tag_block

def add_tags_to_file(file_path, tag_block):
    """在文件末尾添加标签块"""
    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(tag_block)
        return True
    except Exception as e:
        print(f"写入文件失败 {file_path}: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("批量提取日记标签")
    print("=" * 60)
    
    # 扫描所有日记
    diaries = scan_diaries()
    
    # 统计
    total = len(diaries)
    with_tags = sum(1 for d in diaries if d['has_tag'])
    without_tags = total - with_tags
    
    print(f"\n📊 统计信息:")
    print(f"   总日记数: {total}")
    print(f"   已有标签: {with_tags}")
    print(f"   需要处理: {without_tags}")
    
    if without_tags == 0:
        print("\n✅ 所有日记都已处理！")
        return
    
    # 找出需要处理的日记
    to_process = [d for d in diaries if not d['has_tag']]
    
    print(f"\n🔄 开始处理 {without_tags} 篇日记...")
    print("-" * 60)
    
    # 处理每篇日记
    success_count = 0
    for i, diary in enumerate(to_process, 1):
        print(f"\n[{i}/{without_tags}] 处理: {diary['relative_path']}")
        
        # 读取日记内容
        content = get_diary_content(diary['path'])
        if content is None:
            print(f"   ❌ 读取失败，跳过")
            continue
        
        # 提取日期字符串（从文件名）
        date_str = diary['relative_path'].replace('.md', '')
        
        # 生成标签块
        tag_block = generate_tag_block(content, date_str)
        
        # 添加标签到文件
        if add_tags_to_file(diary['path'], tag_block):
            print(f"   ✅ 标签已添加")
            success_count += 1
        else:
            print(f"   ❌ 添加失败")
    
    # 总结
    print("\n" + "=" * 60)
    print("处理完成")
    print("=" * 60)
    print(f"✅ 成功处理: {success_count}/{without_tags}")
    print(f"❌ 失败: {without_tags - success_count}/{without_tags}")
    
    if success_count > 0:
        print(f"\n💡 提示:")
        print(f"   - 可以在Obsidian中查看标签关联效果")
        print(f"   - 如需重新分析，可以手动调整标签")

if __name__ == "__main__":
    main()
