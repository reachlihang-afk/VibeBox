"""
B站链接解析器
"""

import re
from .base import BaseParser

class BilibiliParser(BaseParser):
    """B站解析器"""
    
    def can_handle(self, url: str) -> bool:
        """判断是否为B站链接"""
        patterns = [
            r'bilibili\.com',
            r'b23\.tv',
        ]
        return any(re.search(p, url) for p in patterns)
    
    async def parse(self, url: str) -> dict:
        """解析B站链接"""
        try:
            # 获取页面内容
            html = await self.fetch_page(url)
            
            # 提取 meta 信息
            meta = self.extract_meta(html)
            
            return {
                "url": url,
                "title": meta.get('title', ''),
                "description": meta.get('description', ''),
                "platform": "bilibili",
                "author": None,
                "thumbnail": meta.get('image', ''),
                "media_urls": [meta.get('image', '')] if meta.get('image') else [],
                "created_at": None
            }
        except Exception as e:
            raise Exception(f"B站链接解析失败: {str(e)}")
