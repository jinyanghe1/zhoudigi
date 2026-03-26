from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from io import BytesIO
from fastapi.responses import StreamingResponse

from app.database import get_db
from app.schemas import ResponseModel
from app.models import Article as ArticleModel

router = APIRouter()


class ExportRequest(BaseModel):
    article_ids: List[int]
    include_translation: bool = True
    include_knowledge: bool = True


@router.post("/pdf")
async def export_pdf(
    request: ExportRequest,
    db: Session = Depends(get_db)
):
    """导出文章为 PDF"""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
    except ImportError:
        raise HTTPException(status_code=500, detail="PDF 导出功能需要安装 reportlab")
    
    # 获取文章
    articles = db.query(ArticleModel).filter(
        ArticleModel.id.in_(request.article_ids)
    ).all()
    
    if not articles:
        raise HTTPException(status_code=404, detail="未找到指定文章")
    
    # 创建 PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # 注册中文字体（使用系统默认字体）
    try:
        # 尝试使用常见的中文字体
        font_paths = [
            "/System/Library/Fonts/PingFang.ttc",  # macOS
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",  # Linux
            "C:/Windows/Fonts/simhei.ttf",  # Windows
        ]
        font_registered = False
        for font_path in font_paths:
            try:
                pdfmetrics.registerFont(TTFont('Chinese', font_path))
                font_registered = True
                break
            except:
                continue
        
        if not font_registered:
            # 如果没有中文字体，使用默认字体并提示
            print("警告: 未找到中文字体，PDF 中文可能显示异常")
    except Exception as e:
        print(f"字体注册失败: {e}")
    
    # 构建内容
    styles = getSampleStyleSheet()
    story = []
    
    # 标题样式
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    # 正文样式
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=12,
        leading=20,
        alignment=TA_JUSTIFY
    )
    
    for i, article in enumerate(articles):
        # 标题
        story.append(Paragraph(article.title, title_style))
        
        # 作者信息
        author_name = article.author.name if article.author else "未知"
        dynasty_name = article.dynasty.name if article.dynasty else "未知"
        story.append(Paragraph(f"{dynasty_name} · {author_name}", styles['Heading3']))
        story.append(Spacer(1, 0.2 * inch))
        
        # 原文
        story.append(Paragraph("原文", styles['Heading2']))
        story.append(Spacer(1, 0.1 * inch))
        
        # 分段显示原文
        paragraphs = article.content.split('\n')
        for para in paragraphs:
            if para.strip():
                story.append(Paragraph(para, body_style))
                story.append(Spacer(1, 0.1 * inch))
        
        # 翻译
        if request.include_translation and article.translation:
            story.append(Spacer(1, 0.2 * inch))
            story.append(Paragraph("译文", styles['Heading2']))
            story.append(Spacer(1, 0.1 * inch))
            
            trans_paragraphs = article.translation.split('\n')
            for para in trans_paragraphs:
                if para.strip():
                    story.append(Paragraph(para, body_style))
                    story.append(Spacer(1, 0.1 * inch))
        
        # 知识点
        if request.include_knowledge and article.knowledge_points:
            story.append(Spacer(1, 0.2 * inch))
            story.append(Paragraph("知识点", styles['Heading2']))
            story.append(Spacer(1, 0.1 * inch))
            
            for kp in article.knowledge_points:
                type_name = {
                    'vocab': '词汇',
                    'background': '背景',
                    'analysis': '赏析'
                }.get(kp.type, '其他')
                
                story.append(Paragraph(f"【{type_name}】{kp.content}", styles['Heading4']))
                if kp.explanation:
                    story.append(Paragraph(kp.explanation, body_style))
                story.append(Spacer(1, 0.1 * inch))
        
        # 分页
        if i < len(articles) - 1:
            story.append(PageBreak())
    
    # 生成 PDF
    doc.build(story)
    buffer.seek(0)
    
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=guji_articles.pdf"
        }
    )
