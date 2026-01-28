"""
解析器基类
"""

from abc import ABC, abstractmethod
import httpx
from bs4 import BeautifulSoup
from typing import Optional

class BaseParser(ABC):
    """链接解析器基类"""
    
    def __init__(self):
        self.client = httpx.AsyncClient(
            headers={
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
            },
            timeout=30.0,
            follow_redirects=True
        )
    
    @abstractmethod
    async def parse(self, url: str) -> dict:
        """
        解析链接，返回内容数据
        
        返回格式：
        {
            "url": "原始链接",
            "title": "标题",
            "description": "描述",
            "platform": "平台名称",
            "author": "作者",
            "thumbnail": "缩略图 URL",
            "media_urls": ["媒体文件 URL 列表"],
            "created_at": "发布时间"
        }
        """
        pass
    
    @abstractmethod
    def can_handle(self, url: str) -> bool:
        """判断是否能处理该链接"""
        pass
    
    async def fetch_page(self, url: str) -> str:
        """获取页面内容"""
        response = await self.client.get(url)
        response.raise_for_status()
        return response.text
    
    def extract_meta(self, html: str) -> dict:
        """提取 meta 标签信息"""
        soup = BeautifulSoup(html, 'html.parser')
        
        return {
            'title': self._get_meta(soup, 'og:title') or self._get_meta(soup, 'twitter:title'),
            'description': self._get_meta(soup, 'og:description') or self._get_meta(soup, 'twitter:description'),
            'image': self._get_meta(soup, 'og:image') or self._get_meta(soup, 'twitter:image'),
        }
    
    def _get_meta(self, soup: BeautifulSoup, property: str) -> Optional[str]:
        """获取 meta 标签内容"""
        tag = soup.find('meta', property=property) or soup.find('meta', attrs={'name': property})
        return tag.get('content') if tag else None
    
    async def close(self):
        """关闭 HTTP 客户端"""
        await self.client.aclose()
