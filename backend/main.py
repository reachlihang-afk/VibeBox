"""
VibeBox Backend API
链接解析服务
"""

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

from parsers import get_parser

app = FastAPI(
    title="VibeBox Link Parser API",
    description="解析各平台分享链接的后端服务",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请求模型
class ParseRequest(BaseModel):
    url: str
    user_id: Optional[str] = None

# 响应模型
class ParseResponse(BaseModel):
    status: str
    task_id: str
    message: str

class ContentItem(BaseModel):
    url: str
    title: Optional[str] = None
    description: Optional[str] = None
    platform: str
    author: Optional[str] = None
    thumbnail: Optional[str] = None
    media_urls: list[str] = []
    created_at: Optional[str] = None

# 内存中的任务存储（生产环境应使用 Redis）
tasks = {}

@app.get("/")
async def root():
    """API 根路径"""
    return {
        "name": "VibeBox Link Parser API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}

@app.post("/api/parse", response_model=ParseResponse)
async def parse_link(request: ParseRequest, background_tasks: BackgroundTasks):
    """
    解析分享链接
    
    支持的平台：
    - 小红书 (xiaohongshu.com, xhslink.com)
    - 抖音 (douyin.com, v.douyin.com)
    - B站 (bilibili.com, b23.tv)
    - 微博 (weibo.com, weibo.cn)
    """
    task_id = str(uuid.uuid4())
    
    # 初始化任务状态
    tasks[task_id] = {
        "status": "processing",
        "created_at": datetime.now().isoformat(),
        "result": None,
        "error": None
    }
    
    # 后台处理
    background_tasks.add_task(
        parse_and_save,
        url=request.url,
        user_id=request.user_id or "anonymous",
        task_id=task_id
    )
    
    return ParseResponse(
        status="processing",
        task_id=task_id,
        message="正在解析内容..."
    )

@app.get("/api/task/{task_id}")
async def get_task_status(task_id: str):
    """获取任务状态"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return tasks[task_id]

async def parse_and_save(url: str, user_id: str, task_id: str):
    """后台解析任务"""
    try:
        # 获取对应的解析器
        parser = get_parser(url)
        
        if parser is None:
            tasks[task_id]["status"] = "failed"
            tasks[task_id]["error"] = "不支持的链接类型"
            return
        
        # 解析内容
        content = await parser.parse(url)
        
        # 更新任务状态
        tasks[task_id]["status"] = "completed"
        tasks[task_id]["result"] = content
        tasks[task_id]["completed_at"] = datetime.now().isoformat()
        
    except Exception as e:
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["error"] = str(e)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
