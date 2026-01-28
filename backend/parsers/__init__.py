"""
链接解析器模块
"""

from .base import BaseParser
from .xiaohongshu import XiaohongshuParser
from .douyin import DouyinParser
from .bilibili import BilibiliParser
from .weibo import WeiboParser

def get_parser(url: str) -> BaseParser | None:
    """
    根据 URL 获取对应的解析器
    """
    parsers = [
        XiaohongshuParser(),
        DouyinParser(),
        BilibiliParser(),
        WeiboParser(),
    ]
    
    for parser in parsers:
        if parser.can_handle(url):
            return parser
    
    return None

__all__ = [
    'BaseParser',
    'XiaohongshuParser',
    'DouyinParser',
    'BilibiliParser',
    'WeiboParser',
    'get_parser',
]
