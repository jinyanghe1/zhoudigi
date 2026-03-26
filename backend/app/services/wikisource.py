import httpx
from typing import List, Dict, Any, Optional
from urllib.parse import quote

from app.config import settings


class WikisourceService:
    """维基文库 API 服务"""
    
    def __init__(self):
        self.api_url = settings.wikisource_api_url
    
    async def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        搜索维基文库
        
        Args:
            query: 搜索关键词
            limit: 返回结果数量
            
        Returns:
            搜索结果列表
        """
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srlimit": limit,
            "format": "json",
            "origin": "*"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.api_url,
                    params=params,
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                
                results = data.get("query", {}).get("search", [])
                return [
                    {
                        "title": r["title"],
                        "snippet": r.get("snippet", ""),
                        "pageid": r["pageid"]
                    }
                    for r in results
                ]
            except Exception as e:
                print(f"搜索维基文库出错: {e}")
                return []
    
    async def get_content(self, title: str) -> Dict[str, Any]:
        """
        获取页面内容
        
        Args:
            title: 页面标题
            
        Returns:
            页面内容
        """
        params = {
            "action": "parse",
            "page": title,
            "prop": "text|categories|links",
            "format": "json",
            "origin": "*"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.api_url,
                    params=params,
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                
                parse_data = data.get("parse", {})
                text = parse_data.get("text", {}).get("*", "")
                
                # 清理 HTML 标签，提取纯文本
                import re
                text = re.sub(r'<[^>]+>', '', text)
                text = re.sub(r'\[.*?\]', '', text)  # 移除 wiki 链接标记
                
                return {
                    "title": parse_data.get("title", title),
                    "content": text,
                    "pageid": parse_data.get("pageid"),
                    "url": f"https://zh.wikisource.org/wiki/{quote(title)}"
                }
            except Exception as e:
                print(f"获取维基文库内容出错: {e}")
                return {
                    "title": title,
                    "content": "",
                    "error": str(e)
                }
    
    async def get_categories(self, title: str) -> List[str]:
        """
        获取页面分类
        
        Args:
            title: 页面标题
            
        Returns:
            分类列表
        """
        params = {
            "action": "parse",
            "page": title,
            "prop": "categories",
            "format": "json",
            "origin": "*"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.api_url,
                    params=params,
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                
                categories = data.get("parse", {}).get("categories", [])
                return [c.get("*", "") for c in categories]
            except Exception as e:
                print(f"获取分类出错: {e}")
                return []
    
    async def get_random_classics(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        获取随机古籍文章
        
        Args:
            limit: 数量
            
        Returns:
            文章列表
        """
        # 预定义一些经典古文标题
        classic_titles = [
            "論語",
            "孟子",
            "道德經",
            "莊子",
            "史記",
            "漢書",
            "後漢書",
            "三國志",
            "資治通鑑",
            "左傳",
            "戰國策",
            "詩經",
            "楚辭",
            "唐詩",
            "宋詞",
            "元曲",
            "古文觀止",
            "昭明文選"
        ]
        
        import random
        selected = random.sample(classic_titles, min(limit, len(classic_titles)))
        
        results = []
        for title in selected:
            content_data = await self.get_content(title)
            if content_data.get("content"):
                results.append(content_data)
        
        return results
