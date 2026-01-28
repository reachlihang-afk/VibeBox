# VibeBox API 文档

## 后端 API

### 基础信息

- **Base URL**: `http://localhost:8000`
- **Content-Type**: `application/json`

---

## 端点列表

### 1. 健康检查

**GET** `/health`

检查服务是否正常运行

**响应示例**:
```json
{
  "status": "healthy"
}
```

---

### 2. 解析链接

**POST** `/api/parse`

解析分享链接并提取内容信息

**请求体**:
```json
{
  "url": "https://xhslink.com/xxxxx",
  "user_id": "optional_user_id"
}
```

**参数说明**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| url | string | 是 | 要解析的链接 |
| user_id | string | 否 | 用户ID（可选） |

**响应示例**:
```json
{
  "status": "processing",
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "正在解析内容..."
}
```

**支持的平台**:
- 小红书: `xiaohongshu.com`, `xhslink.com`
- 抖音: `douyin.com`, `v.douyin.com`
- B站: `bilibili.com`, `b23.tv`
- 微博: `weibo.com`, `weibo.cn`

---

### 3. 获取任务状态

**GET** `/api/task/{task_id}`

获取解析任务的状态和结果

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| task_id | string | 任务ID |

**响应示例 - 处理中**:
```json
{
  "status": "processing",
  "created_at": "2026-01-28T10:00:00",
  "result": null,
  "error": null
}
```

**响应示例 - 完成**:
```json
{
  "status": "completed",
  "created_at": "2026-01-28T10:00:00",
  "completed_at": "2026-01-28T10:00:05",
  "result": {
    "url": "https://xiaohongshu.com/explore/...",
    "title": "夏日穿搭分享",
    "description": "今天分享一套超好看的穿搭...",
    "platform": "xiaohongshu",
    "author": "时尚博主",
    "thumbnail": "https://ci.xiaohongshu.com/xxx.jpg",
    "media_urls": [
      "https://ci.xiaohongshu.com/xxx.jpg",
      "https://ci.xiaohongshu.com/yyy.jpg"
    ],
    "created_at": "2026-01-28"
  },
  "error": null
}
```

**响应示例 - 失败**:
```json
{
  "status": "failed",
  "created_at": "2026-01-28T10:00:00",
  "result": null,
  "error": "不支持的链接类型"
}
```

---

## 状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 错误响应

所有错误响应都遵循以下格式：

```json
{
  "detail": "错误描述信息"
}
```

---

## 使用示例

### Python

```python
import requests

# 解析链接
response = requests.post(
    "http://localhost:8000/api/parse",
    json={
        "url": "https://xhslink.com/xxxxx",
        "user_id": "user123"
    }
)

task_id = response.json()["task_id"]

# 获取结果
import time
while True:
    result = requests.get(f"http://localhost:8000/api/task/{task_id}")
    data = result.json()
    
    if data["status"] == "completed":
        print(data["result"])
        break
    elif data["status"] == "failed":
        print(f"Error: {data['error']}")
        break
    
    time.sleep(1)
```

### JavaScript

```javascript
// 解析链接
const response = await fetch('http://localhost:8000/api/parse', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    url: 'https://xhslink.com/xxxxx',
    user_id: 'user123'
  })
});

const { task_id } = await response.json();

// 轮询获取结果
const checkStatus = async () => {
  const result = await fetch(`http://localhost:8000/api/task/${task_id}`);
  const data = await result.json();
  
  if (data.status === 'completed') {
    console.log(data.result);
  } else if (data.status === 'failed') {
    console.error(data.error);
  } else {
    setTimeout(checkStatus, 1000);
  }
};

checkStatus();
```

### Dart (Flutter)

```dart
import 'package:dio/dio.dart';

final dio = Dio(BaseOptions(
  baseUrl: 'http://localhost:8000',
));

// 解析链接
Future<Map<String, dynamic>> parseLink(String url) async {
  final response = await dio.post('/api/parse', data: {
    'url': url,
    'user_id': 'user123',
  });
  
  final taskId = response.data['task_id'];
  
  // 轮询获取结果
  while (true) {
    await Future.delayed(Duration(seconds: 1));
    
    final result = await dio.get('/api/task/$taskId');
    final data = result.data;
    
    if (data['status'] == 'completed') {
      return data['result'];
    } else if (data['status'] == 'failed') {
      throw Exception(data['error']);
    }
  }
}
```

---

## 限流

当前版本暂无限流，生产环境建议添加：
- 每个 IP 每分钟最多 60 次请求
- 每个用户每天最多 1000 次请求

---

## 版本历史

### v1.0.0 (2026-01-28)
- 初始版本
- 支持小红书、抖音、B站、微博链接解析
- 异步任务处理
- RESTful API 设计
