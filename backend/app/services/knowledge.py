from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models import KnowledgePoint, Article
from app.schemas.knowledge_point import KnowledgePointCreate


class KnowledgeService:
    """知识点处理服务"""

    def __init__(self, db: Session):
        self.db = db

    def create_knowledge_point(self, point_data: KnowledgePointCreate) -> KnowledgePoint:
        """
        创建知识点

        Args:
            point_data: 知识点数据

        Returns:
            创建的知识点
        """
        db_point = KnowledgePoint(**point_data.model_dump())
        self.db.add(db_point)
        self.db.commit()
        self.db.refresh(db_point)
        return db_point

    def create_knowledge_points(
        self,
        article_id: int,
        points: List[Dict[str, Any]]
    ) -> List[KnowledgePoint]:
        """
        批量创建知识点

        Args:
            article_id: 文章ID
            points: 知识点列表

        Returns:
            创建的知识点列表
        """
        created_points = []
        for point in points:
            point_data = KnowledgePointCreate(
                article_id=article_id,
                type=point.get("type", "background"),
                content=point.get("content", ""),
                explanation=point.get("explanation", ""),
                position_start=point.get("position_start"),
                position_end=point.get("position_end")
            )
            db_point = self.create_knowledge_point(point_data)
            created_points.append(db_point)
        return created_points

    def get_article_knowledge_points(
        self,
        article_id: int,
        type_filter: Optional[str] = None
    ) -> List[KnowledgePoint]:
        """
        获取文章的所有知识点

        Args:
            article_id: 文章ID
            type_filter: 知识点类型过滤 (vocab, background, analysis)

        Returns:
            知识点列表
        """
        query = self.db.query(KnowledgePoint).filter(
            KnowledgePoint.article_id == article_id
        )
        if type_filter:
            query = query.filter(KnowledgePoint.type == type_filter)
        return query.all()

    def delete_article_knowledge_points(self, article_id: int) -> int:
        """
        删除文章的所有知识点

        Args:
            article_id: 文章ID

        Returns:
            删除的数量
        """
        count = self.db.query(KnowledgePoint).filter(
            KnowledgePoint.article_id == article_id
        ).delete()
        self.db.commit()
        return count

    def get_knowledge_stats(self, article_id: int) -> Dict[str, int]:
        """
        获取文章知识点统计

        Args:
            article_id: 文章ID

        Returns:
            各类型知识点数量
        """
        points = self.get_article_knowledge_points(article_id)
        stats = {
            "total": len(points),
            "vocab": 0,
            "background": 0,
            "analysis": 0
        }
        for point in points:
            if point.type in stats:
                stats[point.type] += 1
        return stats

    @staticmethod
    def extract_text_positions(content: str, keywords: List[str]) -> List[Dict[str, Any]]:
        """
        从文章内容中提取关键词位置

        Args:
            content: 文章内容
            keywords: 关键词列表

        Returns:
            位置信息列表
        """
        positions = []
        for keyword in keywords:
            start = 0
            while True:
                pos = content.find(keyword, start)
                if pos == -1:
                    break
                positions.append({
                    "keyword": keyword,
                    "start": pos,
                    "end": pos + len(keyword)
                })
                start = pos + 1
        return positions

    @staticmethod
    def group_points_by_type(
        points: List[KnowledgePoint]
    ) -> Dict[str, List[KnowledgePoint]]:
        """
        按类型分组知识点

        Args:
            points: 知识点列表

        Returns:
            按类型分组的字典
        """
        grouped = {
            "vocab": [],
            "background": [],
            "analysis": []
        }
        for point in points:
            if point.type in grouped:
                grouped[point.type].append(point)
        return grouped
