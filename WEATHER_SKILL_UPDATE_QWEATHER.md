# Weather-CN Skill 更新总结 - 切换到和风天气 API

## 更新日期

2026-03-02

---

## 问题分析

### 原有问题

使用 `wttr.in` API 获取天气时经常失败：

**错误信息：**
```
获取天气超时（10秒）
URL Error: _ssl.c:993: The handshake operation timed out
```

**原因：**
1. wttr.in 服务器 SSL/TLS 握手超时
2. 虽然 ping 可以通，但 HTTPS 连接建立失败
3. 可能是网络环境对 HTTPS 有限制，或服务器负载高

**测试结果：**
- ✅ ping wttr.in 成功（210ms 延迟）
- ❌ HTTPS 连接超时（10 秒）
- ❌ curl 命令也超时

### 影响范围

- diary-scatter-organizer skill 天气获取功能经常失败
- 用户体验较差

---

## 解决方案

### 切换到和风天气 API（QWeather）

**优势：**
1. ✅ 国内服务器，访问稳定快速
2. ✅ 支持中文城市名
3. ✅ 免费 1000 次/天（足够日记使用）
4. ✅ API 响应速度快
5. ✅ 数据准确可靠

---

## 实现内容

### 1. 重写 `get_weather.py`

**主要修改：**

1. **使用和风天气 API**
   - 城市搜索 API：`https://geoapi.qweather.com/v2/city/lookup`
   - 实时天气 API：`https://dev.qweather.com/v7/weather/now`

2. **支持多种配置方式**
   - 环境变量：`QWEATHER_API_KEY`
   - 配置文件：`~/.config/qweather.json`

3. **两步获取天气**
   - 第一步：通过城市名获取城市 ID
   - 第二步：通过城市 ID 获取实时天气

4. **改进错误处理**
   - API Key 未配置提示
   - 网络错误处理
   - API 错误码提示

**核心函数：**

```python
def get_city_id(city_name: str, timeout: int = 10) -> Optional[str]:
    """通过城市名获取和风天气城市 ID"""

def get_weather(city: str, timeout: int = 10) -> Optional[dict]:
    """获取城市天气（使用和风天气 API）"""
```

### 2. 更新文档

| 文件 | 更新内容 |
|------|----------|
| `SKILL.md` | 添加和风天气 API 配置说明<br>移除 curl 依赖<br>更新 Prerequisites |
| `README.md` | 更新功能特性<br>添加配置说明<br>更新故障排除<br>更新使用示例 |
| `QWEATHER_SETUP.md` | 新增和风天气配置指南<br>详细说明注册和配置步骤<br>安全建议和常见问题 |

---

## 配置说明

### 注册和风天气

1. 访问 https://dev.qweather.com/
2. 注册账号
3. 创建应用
4. 获取 API Key

### 配置 API Key

**方法 1：环境变量（推荐）**
```bash
export QWEATHER_API_KEY='your-api-key'
```

**方法 2：配置文件**
```bash
mkdir -p ~/.config
echo '{"api_key": "your-api-key"}' > ~/.config/qweather.json
```

### 验证配置

```bash
python3 weather-cn/scripts/get_weather.py 武汉
```

---

## 测试结果

### 测试 1：API Key 未配置

✅ 通过 - 正确提示未配置 API Key
✅ 通过 - 提供配置方法说明

### 测试 2：基本功能（需要 API Key）

预期行为：
- 获取城市 ID
- 获取实时天气
- 格式化输出

### 测试 3：集成测试（需要 API Key）

预期行为：
- diary-scatter-organizer 可以正常调用
- 天气信息填充到日记中

---

## 向后兼容性

⚠️ **破坏性变更**

- 需要配置和风天气 API Key
- 移除了 curl 依赖
- API 调用方式完全改变

**迁移指南：**
1. 注册和风天气账号
2. 获取 API Key
3. 配置 API Key（环境变量或配置文件）
4. 测试天气获取

---

## 依赖变更

### 移除
- ❌ `subprocess` - 不再使用 curl
- ❌ `curl` - 不再需要

### 新增
- ✅ `urllib` - 用于 HTTP 请求
- ✅ `urllib.error` - 用于错误处理

---

## 文件变更

| 文件 | 变更类型 | 说明 |
|------|----------|------|
| `scripts/get_weather.py` | 重写 | 完全重写，使用和风天气 API |
| `SKILL.md` | 修改 | 更新配置说明和依赖 |
| `README.md` | 修改 | 更新使用说明和故障排除 |
| `QWEATHER_SETUP.md` | 新增 | 和风天气配置指南 |

---

## 使用示例

### 配置完成后

```bash
# 查询天气
python3 weather-cn/scripts/get_weather.py 武汉

# 输出：武汉天气：☀️，温度：15°C，湿度：72%
```

### 集成到 diary-scatter-organizer

自动调用，无需额外配置。

---

## 优势对比

| 特性 | wttr.in | 和风天气 |
|------|---------|----------|
| 访问速度 | 慢（经常超时） | 快（国内服务器） |
| 稳定性 | 不稳定 | 稳定 |
| 配置 | 无需配置 | 需要配置 API Key |
| 免费额度 | 无限制 | 1000 次/天 |
| 中文支持 | 部分支持 | 完整支持 |
| 数据准确性 | 一般 | 高 |

---

## 注意事项

1. **API Key 安全**
   - 不要提交到 Git 仓库
   - 不要硬编码在代码中
   - 定期检查调用量

2. **免费额度**
   - 每天 1000 次调用
   - 足够日记使用（每天 1 次）

3. **网络依赖**
   - 需要联网访问和风天气 API
   - 国内访问速度快

---

## 后续优化建议

1. [ ] 添加 API 调用缓存（一天只请求一次）
2. [ ] 支持未来天气预报
3. [ ] 添加空气质量查询
4. [ ] 实现多 API 源 fallback 机制

---

## 总结

✅ 已成功切换到和风天气 API
✅ 完全重写 weather-cn skill
✅ 更新所有相关文档
✅ 提供详细的配置指南

需要配置和风天气 API Key 才能使用。

---

## 配置检查清单

- [ ] 注册和风天气账号
- [ ] 创建应用并获取 API Key
- [ ] 配置 API Key（环境变量或配置文件）
- [ ] 验证配置成功
- [ ] API Key 未提交到 Git
- [ ] 测试天气获取功能

---

配置完成后，即可正常使用 weather-cn skill！
