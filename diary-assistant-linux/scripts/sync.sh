#!/bin/bash
# Git 推送脚本

cd ~/Documents/diary

# 检查是否是 Git 仓库
if [ ! -d ".git" ]; then
  echo "⚠️  不是一个 Git 仓库，请先初始化："
  echo "cd ~/Documents/diary"
  echo "git init"
  echo "git add ."
  echo "git commit -m 'init: 初始化日记仓库'"
  echo "git remote add origin <远程仓库地址>"
  echo "git push -u origin main"
  exit 1
fi

# 检查是否有远程仓库
if [ -z "$(git remote get-url origin 2>/dev/null)" ]; then
  echo "⚠️  没有配置远程仓库，请先添加："
  echo "git remote add origin <远程仓库地址>"
  exit 1
fi

# 添加修改
echo "📝 添加本地修改..."
git add .

# 检查是否有修改
if git diff --cached --quiet; then
  echo "✅ 没有需要提交的修改"
  exit 0
fi

# 提交
echo "💾 提交修改..."
git commit -m "update: $(date +%Y-%m-%d)"

# 推送
echo "📤 推送到远端..."
if git push origin main; then
  echo "✅ 推送完成！"
else
  echo "❌ 推送失败，请检查网络或手动解决冲突"
  echo "💡 提示：可能需要先拉取远端更新：git pull origin main"
  exit 1
fi
