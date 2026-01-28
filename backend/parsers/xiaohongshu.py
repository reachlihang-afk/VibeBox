"""
小红书链接解析器
"""

import re
from .base import BaseParser

class XiaohongshuParser(BaseParser):
    """小红书解析器"""
    
    def can_handle(self, url: str) -> bool:
        """判断是否为小红书链接"""
        patterns = [
            r'xhslink\.com',
            r'xiaohongshu\.com',
        ]
        return any(re.search(p, url) for p in patterns)
    
    async def parse(self, url: str) -> dict:
        """解析小红书链接"""
        try:
            # 获取页面内容
            html = await self.fetch_page(url)
            
            # 提取 meta 信息
            meta = self.extract_meta(html)
            
            # 获取真实 URL（如果是短链接）
            real_url = str(self.client.get(url, follow_redirects=True).url) if 'xhslink' in url else url
            
            return {
                "url": real_url,
                "title": meta.get('title', ''),
                "description": meta.get('description', ''),
                "platform": "xiaohongshu",
                "author": None,  # 需要进一步解析
                "thumbnail": meta.get('image', ''),
                "media_urls": [meta.get('image', '')] if meta.get('image') else [],
                "created_at": None
            }
        except Exception as e:
            raise Exception(f"小红书链接解析失败: {str(e)}")
