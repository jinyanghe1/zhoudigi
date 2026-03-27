"""
知识图谱数据生成工具
"""
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.models import Dynasty, Author, Article


def generate_dynasty_graph(db: Session) -> Dict[str, Any]:
    """
    生成朝代关系图数据
    
    Returns:
        ECharts 可用的图数据
    """
    nodes = []
    links = []
    categories = [
        {"name": "朝代"},
        {"name": "作者"},
        {"name": "文章"}
    ]
    
    # 获取所有朝代
    dynasties = db.query(Dynasty).all()
    
    # 添加朝代节点
    for dynasty in dynasties:
        nodes.append({
            "id": f"dynasty_{dynasty.id}",
            "name": dynasty.name,
            "symbolSize": 50,
            "category": 0,
            "value": dynasty.name,
            "label": {"show": True, "fontSize": 14, "fontWeight": "bold"},
            "itemStyle": {"color": "#409eff"}
        })
    
    # 获取所有作者
    authors = db.query(Author).all()
    
    # 添加作者节点和连接
    for author in authors:
        nodes.append({
            "id": f"author_{author.id}",
            "name": author.name,
            "symbolSize": 30,
            "category": 1,
            "value": author.name,
            "label": {"show": True},
            "itemStyle": {"color": "#67c23a"}
        })
        
        # 连接作者和朝代
        if author.dynasty_id:
            links.append({
                "source": f"dynasty_{author.dynasty_id}",
                "target": f"author_{author.id}",
                "value": "所属"
            })
    
    # 获取精选文章
    articles = db.query(Article).filter(Article.is_selected == True).limit(30).all()
    
    # 添加文章节点和连接
    for article in articles:
        nodes.append({
            "id": f"article_{article.id}",
            "name": article.title,
            "symbolSize": 20,
            "category": 2,
            "value": article.title,
            "label": {"show": True, "fontSize": 10},
            "itemStyle": {"color": "#e6a23c"}
        })
        
        # 连接文章和作者
        if article.author_id:
            links.append({
                "source": f"author_{article.author_id}",
                "target": f"article_{article.id}",
                "value": "著作"
            })
    
    return {
        "nodes": nodes,
        "links": links,
        "categories": categories
    }


def generate_author_graph(db: Session, author_id: int) -> Dict[str, Any]:
    """
    生成单个作者的关系图
    
    Args:
        author_id: 作者ID
        
    Returns:
        ECharts 可用的图数据
    """
    nodes = []
    links = []
    
    # 获取中心作者
    center_author = db.query(Author).filter(Author.id == author_id).first()
    if not center_author:
        return {"nodes": [], "links": []}
    
    # 添加中心节点
    nodes.append({
        "id": f"author_{center_author.id}",
        "name": center_author.name,
        "symbolSize": 60,
        "category": 0,
        "value": center_author.name,
        "label": {"show": True, "fontSize": 16, "fontWeight": "bold"},
        "itemStyle": {"color": "#f56c6c"}
    })
    
    # 获取同朝代作者
    if center_author.dynasty_id:
        same_dynasty_authors = db.query(Author).filter(
            Author.dynasty_id == center_author.dynasty_id,
            Author.id != author_id
        ).limit(5).all()
        
        for author in same_dynasty_authors:
            nodes.append({
                "id": f"author_{author.id}",
                "name": author.name,
                "symbolSize": 35,
                "category": 1,
                "value": author.name,
                "label": {"show": True},
                "itemStyle": {"color": "#409eff"}
            })
            
            links.append({
                "source": f"author_{center_author.id}",
                "target": f"author_{author.id}",
                "value": "同时代",
                "lineStyle": {"type": "dashed"}
            })
    
    # 获取该作者的文章
    articles = db.query(Article).filter(Article.author_id == author_id).all()
    
    for article in articles:
        nodes.append({
            "id": f"article_{article.id}",
            "name": article.title,
            "symbolSize": 25,
            "category": 2,
            "value": article.title,
            "label": {"show": True, "fontSize": 10},
            "itemStyle": {"color": "#67c23a"}
        })
        
        links.append({
            "source": f"author_{center_author.id}",
            "target": f"article_{article.id}",
            "value": "著作"
        })
    
    categories = [
        {"name": "中心人物"},
        {"name": "同时代文人"},
        {"name": "著作"}
    ]
    
    return {
        "nodes": nodes,
        "links": links,
        "categories": categories
    }


def generate_style_graph(db: Session) -> Dict[str, Any]:
    """
    生成风格分类图
    
    Returns:
        ECharts 可用的图数据
    """
    # 定义风格分类
    styles = {
        "豪放派": ["苏轼", "李白", "韩愈"],
        "婉约派": ["欧阳修", "归有光"],
        "田园派": ["陶渊明"],
        "哲理派": ["庄子", "孔子", "孟子"],
        "政论派": ["范仲淹", "王安石"]
    }
    
    nodes = []
    links = []
    categories = [
        {"name": "风格流派"},
        {"name": "代表人物"}
    ]
    
    # 添加风格节点
    for i, (style, authors_list) in enumerate(styles.items()):
        nodes.append({
            "id": f"style_{i}",
            "name": style,
            "symbolSize": 50,
            "category": 0,
            "value": style,
            "label": {"show": True, "fontSize": 14, "fontWeight": "bold"},
            "itemStyle": {"color": "#409eff"}
        })
        
        # 查找作者并连接
        for author_name in authors_list:
            author = db.query(Author).filter(Author.name == author_name).first()
            if author:
                # 检查作者节点是否已存在
                author_node_id = f"author_{author.id}"
                if not any(n["id"] == author_node_id for n in nodes):
                    nodes.append({
                        "id": author_node_id,
                        "name": author.name,
                        "symbolSize": 30,
                        "category": 1,
                        "value": author.name,
                        "label": {"show": True},
                        "itemStyle": {"color": "#67c23a"}
                    })
                
                links.append({
                    "source": f"style_{i}",
                    "target": author_node_id,
                    "value": "代表"
                })
    
    return {
        "nodes": nodes,
        "links": links,
        "categories": categories
    }
