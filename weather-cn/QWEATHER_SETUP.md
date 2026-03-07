# 和风天气 API 配置指南

## 快速开始

### 1. 注册和风天气

访问 https://dev.qweather.com/ 注册账号。

### 2. 创建应用

1. 登录后进入"控制台"
2. 点击"创建应用"
3. 选择"Web API"
4. 填写应用名称（如：diary-skills）
5. 选择 Key 类型（个人开发选"免费"）

### 3. 获取 API Key

创建完成后，在应用详情页面可以看到 API Key。

### 4. 配置 API Key

**方法 1：环境变量（推荐）**

临时配置（当前终端会话）：
```bash
export QWEATHER_API_KEY='your-api-key'
```

永久配置（添加到 ~/.zshrc 或 ~/.bashrc）：
```bash
echo "export QWEATHER_API_KEY='your-api-key'" >> ~/.zshrc
source ~/.zshrc
```

**方法 2：配置文件**

```bash
# 创建配置目录
mkdir -p ~/.config

# 写入 API Key
echo '{"api_key": "your-api-key"}' > ~/.config/qweather.json

# 设置权限（保护 API Key）
chmod 600 ~/.config/qweather.json
```

### 5. 验证配置

```bash
# 测试天气查询
python3 weather-cn/scripts/get_weather.py 武汉
```

如果输出天气信息，说明配置成功。

---

## API Key 安全建议

### ✅ 推荐做法

1. **不要提交到 Git**
   ```bash
   echo "*.json" >> .gitignore
   echo "qweather.json" >> .gitignore
   ```

2. **使用环境变量**
   - 更安全，不会意外提交
   - 适合 CI/CD 环境

3. **设置文件权限**
   ```bash
   chmod 600 ~/.config/qweather.json
   ```

4. **定期更新 API Key**
   - 如果 API Key 泄露，立即重新生成

### ❌ 不推荐做法

1. **不要硬编码在代码中**
   ```python
   # ❌ 错误
   API_KEY = "your-api-key"
   ```

2. **不要提交到公开仓库**

---

## 和风天气 API 使用说明

### 免费版限制

| 项目 | 限制 |
|------|------|
| 每日调用量 | 1000 次 |
| 实时天气 | 1000 次/天 |
| 7 天预报 | 100 次/天 |
| 空气质量 | 100 次/天 |

### 使用场景

**diary-scatter-organizer 使用情况：**
- 每天整理日记时调用 1 次
- 实时天气查询
- 免费额度完全够用

### 查看使用量

1. 登录和风天气控制台
2. 进入"我的应用"
3. 查看每个应用的调用统计

---

## 常见问题

### Q: 免费版够用吗？

A: 对于 diary-skills 的使用场景，免费版完全够用。每天整理日记调用 1 次，1000 次/天足够使用。

### Q: API Key 过期怎么办？

A: 和风天气 API Key 长期有效，不会过期。如果泄露了，可以在控制台重新生成。

### Q: 如何升级到付费版？

A: 在和风天气控制台选择"升级套餐"，查看付费版详情和价格。

### Q: 支持 GPU/CPU 渲染吗？

A: 和风天气只提供天气数据 API，不涉及渲染。

---

## 参考链接

- 和风天气官网：https://www.qweather.com/
- 开发者控制台：https://console.qweather.com/
- API 文档：https://dev.qweather.com/docs/
- 定价说明：https://www.qweather.com/pricing

---

## 配置示例

### macOS / Linux

**使用 zsh：**
```bash
echo 'export QWEATHER_API_KEY="your-api-key"' >> ~/.zshrc
source ~/.zshrc
```

**使用 bash：**
```bash
echo 'export QWEATHER_API_KEY="your-api-key"' >> ~/.bashrc
source ~/.bashrc
```

**使用配置文件：**
```bash
mkdir -p ~/.config
cat > ~/.config/qweather.json << EOF
{
  "api_key": "your-api-key"
}
EOF
chmod 600 ~/.config/qweather.json
```

### Windows (PowerShell)

**环境变量：**
```powershell
[Environment]::SetEnvironmentVariable("QWEATHER_API_KEY", "your-api-key", "User")
```

**配置文件：**
```powershell
New-Item -ItemType Directory -Force -Path $env:USERPROFILE\.config
@{ api_key = "your-api-key" } | ConvertTo-Json | Out-File $env:USERPROFILE\.config\qweather.json -Encoding utf8
```

---

## 完成检查清单

完成配置后，请检查以下项目：

- [ ] 已注册和风天气账号
- [ ] 已创建应用并获取 API Key
- [ ] 已配置 API Key（环境变量或配置文件）
- [ ] 已验证配置成功（运行测试命令）
- [ ] API Key 未提交到 Git 仓库
- [ ] 配置文件权限已设置（如使用文件方式）

---

完成所有检查项后，你就可以正常使用 weather-cn skill 了！
