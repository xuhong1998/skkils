---
name: weather-cn
description: 获取中国城市天气信息。支持自动城市检测、温度、天气状况、湿度和风速查询。使用 wttr.in API。
---

## Prerequisites

| Tool | Type | Required | Install |
|------|------|----------|---------|
| Python 3 | cli | Yes | Linux: `sudo apt install python3`<br>Mac: `brew install python3` or included with macOS<br>Windows: `winget install Python.Python.3` or download from python.org |
| 和风天气 API Key | api | Yes | 注册地址：https://dev.qweather.com/ |

> Do NOT proactively verify these tools on skill load. If a command fails due to a missing tool, directly guide the user through installation and configuration step by step.

> Do NOT proactively verify these tools on skill load. If a command fails due to a missing tool, directly guide the user through installation and configuration step by step.

## 核心功能

| 功能 | 说明 |
|------|------|
| **自动城市检测** | 从文本中自动检测城市名，支持中国主要城市 |
| **实时天气获取** | 获取当前温度、天气状况、湿度、风速 |
| **格式化输出** | 支持多种格式（简洁/详细/JSON） |
| **默认城市** | 无检测到城市时使用默认城市（武汉） |

## 支持的城市

支持中国所有省、市、自治区，包括：
- 直辖市：北京、上海、天津、重庆
- 省会城市：广州、深圳、武汉、成都、杭州、西安、南京等
- 地级市：苏州、青岛、大连、厦门等
- 特别行政区：香港、澳门
- 台湾地区：台北、高雄、台中、台南等

## 完整流程

```text
┌─────────────────────────────────────┐
│    weather-cn 天气获取流程          │
└─────────────────────────────────────┘
```

## 配置

### 配置和风天气 API Key

**注册和风天气：**
1. 访问 https://dev.qweather.com/
2. 注册账号
3. 创建应用，获取 API Key

**配置方法（任选其一）：**

**方法 1：环境变量**
```bash
export QWEATHER_API_KEY='your-api-key'
```

**方法 2：配置文件**
```bash
mkdir -p ~/.config
echo '{"api_key": "your-api-key"}' > ~/.config/qweather.json
```

**永久配置（添加到 ~/.bashrc 或 ~/.zshrc）：**
```bash
export QWEATHER_API_KEY='your-api-key'
```

### 验证配置

```bash
python3 weather-cn/scripts/get_weather.py 武汉
```

如果输出天气信息，说明配置成功。

## 使用方式

### 方式 1：从文本中检测城市

**输入：**
```text
今天在北京上班，天气怎么样？
```

**输出：**
```
北京天气：☀️，温度：8°C，湿度：45%
```

### 方式 2：指定城市

**输入：**
```text
查询上海天气
```

**输出：**
```
上海天气：⛅️，温度：12°C，湿度：68%
```

### 方式 3：详细格式

**输入：**
```text
武汉天气（详细）
```

**输出：**
```json
{
  "city": "武汉",
  "temp": "15",
  "condition": "多云",
  "humidity": "72",
  "wind": "10"
}
```

## 脚本使用

### scripts/get_weather.py

**功能：**
- 检测文本中的城市
- 获取天气信息
- 格式化输出

**参数：**
```bash
python3 get_weather.py [城市名] [格式]

城市名: 可选，不指定则从输入文本检测
格式: 可选，simple（简洁）| detail（详细）| json，默认 simple
```

**示例：**

```bash
# 自动检测城市
echo "今天在北京上班" | python3 get_weather.py

# 指定城市
python3 get_weather.py 上海

# 指定格式
python3 get_weather.py 武汉 json
```

## Python API

### get_weather()

```python
from scripts.get_weather import get_weather, format_weather

# 获取天气
weather_info = get_weather('武汉')
print(weather_info)
# {'city': '武汉', 'temp': '15', 'condition': '多云', 'humidity': '72', 'wind': '10'}

# 格式化输出
weather_str = format_weather(weather_info)
print(weather_str)
# 武汉天气：⛅️，温度：15°C，湿度：72%
```

### detect_city()

```python
from scripts.get_weather import detect_city

# 从文本中检测城市
text = "今天在北京上班，天气不错"
city = detect_city(text)
print(city)  # 北京
```

## 错误处理

| 错误 | 处理 |
|------|------|
| 城市检测失败 | 使用默认城市（武汉） |
| 天气获取失败 | 返回 None 或默认提示信息 |
| 网络超时 | 自动重试 1 次 |
| 无效城市 | 提示用户检查城市名称 |

## 天气图标映射

| 天气状况 | 图标 |
|---------|------|
| 晴 | ☀️ |
| 多云 | ⛅️ |
| 阴 | ☁️ |
| 雨/小雨/中雨 | 🌧️ |
| 大雨/暴雨 | ⛈️ |
| 雪/小雪/中雪/大雪 | ❄️ |
| 雾 | 🌫️ |
| 霾 | 😷 |
| 其他 | 🌤️ |

## 配置

### 默认城市

可以在脚本中修改默认城市：

```python
DEFAULT_CITY = '武汉'  # 修改为你所在的城市
```

### API 端点

默认使用 wttr.in API：

```python
API_URL = "https://wttr.in/{city}?lang=zh&format=j1"
```

## 示例

### 示例 1：基本使用

```python
from scripts.get_weather import get_weather, format_weather

weather_info = get_weather('北京')
weather_str = format_weather(weather_info)
print(weather_str)
# 输出：北京天气：☀️，温度：8°C，湿度：45%
```

### 示例 2：从文本检测

```python
from scripts.get_weather import detect_city, get_weather, format_weather

text = "今天在上海参加会议"
city = detect_city(text)
weather_info = get_weather(city)
weather_str = format_weather(weather_info)
print(weather_str)
# 输出：上海天气：⛅️，温度：12°C，湿度：68%
```

### 示例 3：错误处理

```python
from scripts.get_weather import get_weather, format_weather

weather_info = get_weather('不存在的城市')
if not weather_info:
    print("天气信息获取失败")
else:
    weather_str = format_weather(weather_info)
    print(weather_str)
```

## 注意事项

1. **网络依赖：** 需要联网访问 wttr.in API
2. **速率限制：** wttr.in 有速率限制，避免频繁请求
3. **城市名称：** 使用中文城市名（如"北京"而非"Beijing"）
4. **超时设置：** 默认 10 秒超时，可在代码中调整

## 相关技能

- diary-scatter-organizer: 在整理日记时自动获取天气信息
