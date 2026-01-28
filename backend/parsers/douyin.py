"""
抖音链接解析器
"""

import re
from .base import BaseParser

class DouyinParser(BaseParser):
    """抖音解析器"""
    
    def can_handle(self, url: str) -> bool:
        """判断是否为抖音链接"""
        patterns = [
            r'douyin\.com',
            r'v\.douyin\.com',
        ]
        return any(re.search(p, url) for p in patterns)
    
    async def parse(self, url: str) -> dict:
        """解析抖音链接"""
        try:
            # 获取页面内容
            html = await self.fetch_page(url)
            
            # 提取 meta 信息
            meta = self.extract_meta(html)
            
            return {
                "url": url,
                "title": meta.get('title', ''),
                "description": meta.get('description', ''),
                "platform": "douyin",
                "author": None,
                "thumbnail": meta.get('image', ''),
                "media_urls": [meta.get('image', '')] if meta.get('image') else [],
                "created_at": None
            }
        except Exception as e:
            raise Exception(f"抖音链接解析失败: {str(e)}")
