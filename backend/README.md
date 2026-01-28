# VibeBox Backend

链接解析服务后端

## 快速开始

### 安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 运行服务

```bash
# 开发模式
uvicorn main:app --reload

# 生产模式
uvicorn main:app --host 0.0.0.0 --port 8000
```

### API 文档

启动服务后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 端点

### POST /api/parse

解析分享链接

**请求体**:
```json
{
  "url": "https://xhslink.com/xxxxx",
  "user_id": "optional_user_id"
}
```

**响应**:
```json
{
  "status": "processing",
  "task_id": "uuid",
  "message": "正在解析内容..."
}
```

### GET /api/task/{task_id}

获取任务状态

**响应**:
```json
{
  "status": "completed",
  "result": {
    "url": "https://xiaohongshu.com/...",
    "title": "标题",
    "description": "描述",
    "platform": "xiaohongshu",
    "thumbnail": "https://...",
    "media_urls": ["https://..."]
  }
}
```

## 支持的平台

- ✅ 小红书 (xiaohongshu.com, xhslink.com)
- ✅ 抖音 (douyin.com, v.douyin.com)
- ✅ B站 (bilibili.com, b23.tv)
- ✅ 微博 (weibo.com, weibo.cn)

## 部署

### Docker

```bash
# 构建镜像
docker build -t vibebox-backend .

# 运行容器
docker run -p 8000:8000 vibebox-backend
```

### Railway / Render

直接连接 GitHub 仓库即可自动部署
