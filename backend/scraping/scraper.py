"""
古籍采集脚本
从维基文库采集古籍文章，扩充数据库
"""
import httpx
import asyncio
import re
import os
import sys
from typing import List, Dict, Any, Optional
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import Dynasty, Author, Article
from app.services.minimax import MinimaxService
from app.config import settings


# 维基文库分类 - 按朝代组织
WIKISOURCE_CATEGORIES = {
    "先秦": [
        "先秦诸子", "论语", "孟子", "庄子", "墨子", "荀子", "老子", "列子"
    ],
    "汉朝": [
        "汉赋", "史记", "汉书", "说文解字", "汉诗"
    ],
    "魏晋南北朝": [
        "魏晋文学", "陶渊明集", "文心雕龙", "诗品"
    ],
    "唐朝": [
        "唐代散文", "韩愈集", "柳宗元集", "唐代传奇"
    ],
    "宋朝": [
        "宋代散文", "苏轼集", "欧阳修集", "宋人笔记"
    ],
    "元朝": [
        "元曲", "元代散文"
    ],
    "明朝": [
        "明代散文", "明代小品文", "公安派"
    ],
    "清朝": [
        "清代散文", "桐城派", "清代笔记"
    ]
}

# 避免重复采集的已知名篇（已有）
EXCLUDED_TITLES = {
    "桃花源记", "师说", "滕王阁序", "陈情表", "出师表", "岳阳楼记",
    "赤壁赋", "醉翁亭记", "论语", "孟子", "庄子", "逍遥游",
    "得道多助，失道寡助", "原道", "原毁"
}


class GujiScraper:
    """古籍采集器"""

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.base_url = "https://zh.wikisource.org"
        self.api_url = "https://zh.wikisource.org/w/api.php"
        self.translator = MinimaxService()
        self.db = SessionLocal()

    async def close(self):
        await self.client.aclose()
        self.db.close()

    async def fetch_page_content(self, url: str) -> Optional[str]:
        """获取页面内容"""
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            # 提取正文内容（简化版）
            text = response.text
            # 移除 HTML 标签
            text = re.sub(r'<[^>]+>', '', text)
            # 清理空白
            text = re.sub(r'\s+', '\n', text).strip()
            return text
        except Exception as e:
            print(f"获取页面失败 {url}: {e}")
            return None

    async def search_wikisource(self, query: str, limit: int = 10) -> List[Dict]:
        """搜索维基文库"""
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srlimit": limit,
            "format": "json"
        }
        try:
            response = await self.client.get(self.api_url, params=params)
            data = response.json()
            return data.get("query", {}).get("search", [])
        except Exception as e:
            print(f"搜索失败 {query}: {e}")
            return []

    def get_or_create_author(self, name: str, dynasty_id: int, bio: str = "") -> Author:
        """获取或创建作者"""
        author = self.db.query(Author).filter(Author.name == name).first()
        if not author:
            author = Author(
                name=name,
                dynasty_id=dynasty_id,
                bio=bio
            )
            self.db.add(author)
            self.db.commit()
            self.db.refresh(author)
        return author

    def get_dynasty_by_name(self, name: str) -> Optional[Dynasty]:
        """根据名称获取朝代"""
        # 映射可能的名称变体
        dynasty_map = {
            "先秦": ["先秦", "春秋", "战国"],
            "汉朝": ["汉", "西汉", "东汉"],
            "魏晋南北朝": ["魏晋", "南北朝", "六朝", "晋"],
            "唐朝": ["唐", "唐代"],
            "宋朝": ["宋", "宋代", "北宋", "南宋"],
            "元朝": ["元", "元代"],
            "明朝": ["明", "明代"],
            "清朝": ["清", "清代"]
        }

        for key, variants in dynasty_map.items():
            if name in variants:
                return self.db.query(Dynasty).filter(Dynasty.name == key).first()

        return self.db.query(Dynasty).filter(Dynasty.name == name).first()

    async def translate_article(self, content: str) -> str:
        """翻译文章"""
        try:
            translation = await self.translator.translate_text(content[:2000])
            return translation
        except Exception as e:
            print(f"翻译失败: {e}")
            return ""

    def save_article(
        self,
        title: str,
        content: str,
        dynasty_id: int,
        author_id: Optional[int] = None,
        category: str = "",
        translation: str = ""
    ) -> Optional[Article]:
        """保存文章到数据库"""
        # 检查是否已存在
        existing = self.db.query(Article).filter(Article.title == title).first()
        if existing:
            print(f"文章已存在: {title}")
            return None

        # 检查是否在排除列表
        for excluded in EXCLUDED_TITLES:
            if excluded in title:
                print(f"跳过已有名篇: {title}")
                return None

        word_count = len(content)

        article = Article(
            title=title,
            content=content,
            translation=translation,
            dynasty_id=dynasty_id,
            author_id=author_id,
            category=category,
            is_selected=False,  # 新采集的文章默认未精选
            read_count=0,
            word_count=word_count,
            source=f"维基文库"
        )

        self.db.add(article)
        self.db.commit()
        self.db.refresh(article)

        print(f"✅ 保存文章: {title} ({word_count}字)")
        return article

    async def scrape_category(self, category: str, dynasty_name: str) -> int:
        """采集某个分类的文章"""
        print(f"\n{'='*50}")
        print(f"采集分类: {category} (朝代: {dynasty_name})")
        print(f"{'='*50}")

        dynasty = self.get_dynasty_by_name(dynasty_name)
        if not dynasty:
            print(f"未找到朝代: {dynasty_name}")
            return 0

        count = 0

        # 搜索该分类的文章
        search_results = await self.search_wikisource(category, limit=20)

        for result in search_results:
            title = result.get("title", "")

            # 跳过排除的标题
            if any(excluded in title for excluded in EXCLUDED_TITLES):
                continue

            # 构建维基文库页面URL
            page_url = f"{self.base_url}/wiki/{quote(title)}"

            # 获取页面内容
            content = await self.fetch_page_content(page_url)
            if not content or len(content) < 100:
                continue

            # 过滤太短或太长的内容
            if len(content) < 50 or len(content) > 5000:
                continue

            # 清理内容
            content = content.strip()

            # 翻译
            translation = await self.translate_article(content)

            # 保存
            article = self.save_article(
                title=title,
                content=content,
                dynasty_id=dynasty.id,
                category=category,
                translation=translation
            )

            if article:
                count += 1

            # 避免请求过快
            await asyncio.sleep(0.5)

        return count

    async def run(self, target_count: int = 100):
        """运行采集"""
        print(f"🎯 目标: 采集约 {target_count} 篇文章")
        print(f"📊 当前数据库: {self.db.query(Article).count()} 篇文章")

        total_added = 0

        for dynasty_name, categories in WIKISOURCE_CATEGORIES.items():
            if total_added >= target_count:
                break

            for category in categories:
                if total_added >= target_count:
                    break

                count = await self.scrape_category(category, dynasty_name)
                total_added += count

                # 避免请求过快
                await asyncio.sleep(1)

                print(f"累计已采集: {total_added} 篇")

        print(f"\n🎉 采集完成! 共新增 {total_added} 篇文章")
        print(f"📚 数据库现有: {self.db.query(Article).count()} 篇文章")


async def main():
    import argparse

    parser = argparse.ArgumentParser(description="古籍采集脚本")
    parser.add_argument("--count", type=int, default=50, help="目标采集数量")
    args = parser.parse_args()

    scraper = GujiScraper()
    try:
        await scraper.run(target_count=args.count)
    finally:
        await scraper.close()


if __name__ == "__main__":
    asyncio.run(main())
