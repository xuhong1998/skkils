# Weather-CN Skill

独立的天气获取 skill，用于获取中国城市天气信息（使用和风天气 API）。

## 目录结构

```
weather-cn/
├── SKILL.md                    # 技能文档
├── README.md                   # 使用说明
└── scripts/
    ├── get_weather.py          # 天气获取脚本
    └── test_weather.py         # 测试脚本
```

## 功能特性

- ✅ 自动城市检测（支持中国所有主要城市）
- ✅ 实时天气获取（温度、天气状况、湿度、风速）
- ✅ 多种输出格式（简洁/详细/JSON）
- ✅ 可配置默认城市
- ✅ 错误处理和超时机制
- ✅ 使用和风天气 API（稳定快速）

## 使用示例

### 配置 API Key

**方法 1：环境变量**
```bash
export QWEATHER_API_KEY='your-api-key'
```

**方法 2：配置文件**
```bash
mkdir -p ~/.config
echo '{"api_key": "your-api-key"}' > ~/.config/qweather.json
```

**注册地址：** https://dev.qweather.com/

### Python API

```python
from weather_cn.scripts.get_weather import detect_city, get_weather, format_weather

# 检测城市
city = detect_city("今天在北京上班")
print(f"检测到城市：{city}")

# 获取天气
weather_info = get_weather("北京")
print(f"天气信息：{weather_info}")

# 格式化输出
weather_str = format_weather(weather_info)
print(f"{city}天气：{weather_str}")
```

### 命令行

```bash
# 查询指定城市天气
python3 weather-cn/scripts/get_weather.py 武汉

# 从文本中自动检测城市
echo "今天在上海参加会议" | python3 weather-cn/scripts/get_weather.py

# 输出 JSON 格式
python3 weather-cn/scripts/get_weather.py 北京 --format json
```

## 集成到其他 skills

### diary-scatter-organizer

在 `diary-scatter-organizer` 中使用天气功能：

```python
from diary_scatter_organizer.scripts.parse_scattered import import_weather_functions, WEATHER_AVAILABLE

# 导入天气函数
import_weather_functions()

if WEATHER_AVAILABLE:
    from diary_scatter_organizer.scripts.parse_scattered import detect_city, get_weather, format_weather

    # 检测城市
    city = detect_city(all_content, default_city="武汉")

    # 获取天气
    weather_info = get_weather(city)

    # 格式化输出
    weather_str = format_weather(weather_info) if weather_info else ""
```

## 测试

### 测试天气获取

```bash
# 1. 先配置 API Key
export QWEATHER_API_KEY='your-api-key'

# 2. 测试天气获取
python3 weather-cn/scripts/get_weather.py 武汉

# 3. 测试城市检测
echo "今天在北京上班" | python3 weather-cn/scripts/get_weather.py
```

### 测试 diary-scatter-organizer 集成

```bash
# 测试日记整理功能（包含天气）
python3 diary-scatter-organizer/scripts/parse_scattered.py
```

## 注意事项

1. **API Key：** 需要注册和风天气获取 API Key
2. **免费额度：** 和风天气免费版每天 1000 次调用
3. **城市名称：** 使用中文城市名（如"北京"而非"Beijing"）
4. **超时设置：** 默认 10 秒超时，可在代码中调整

## 故障排除

### 未配置 API Key

**症状：**
```
❌ 未配置 QWEATHER_API_KEY
```

**解决方案：**
```bash
# 方法 1：环境变量
export QWEATHER_API_KEY='your-api-key'

# 方法 2：配置文件
mkdir -p ~/.config
echo '{"api_key": "your-api-key"}' > ~/.config/qweather.json
```

**注册地址：** https://dev.qweather.com/

### 天气获取失败

**症状：**
```
获取天气失败：401 - unauthorized
```

**可能原因：**
1. API Key 无效或已过期
2. API Key 配置错误

**解决方案：**
1. 检查 API Key 是否正确
2. 访问和风天气控制台验证 API Key
3. 重新生成 API Key

**症状：**
```
获取天气失败：402 - payment required
```

**可能原因：**
1. 超过免费额度

**解决方案：**
1. 检查 API 调用量
2. 升级到付费套餐

### 模块导入失败

**症状：**
```
ModuleNotFoundError: No module named 'get_weather'
```

**可能原因：**
1. weather-cn skill 路径配置错误
2. Python 路径未正确设置

**解决方案：**
1. 检查 weather-cn skill 是否存在：`ls weather-cn/scripts/`
2. 检查 Python 路径：`python3 -c "import sys; print(sys.path)"`

## 更新日志

### 2026-03-02 (v2.0)
- ✅ 切换到和风天气 API（更稳定、更快速）
- ✅ 支持配置文件和环境变量配置 API Key
- ✅ 改进错误提示和处理机制
- ✅ 更新文档和配置说明

### 2026-03-02 (v1.0)
- ✅ 创建独立的 weather-cn skill
- ✅ 实现城市检测功能
- ✅ 实现天气获取功能（wttr.in）
- ✅ 实现多种输出格式
- ✅ 集成到 diary-scatter-organizer skill
