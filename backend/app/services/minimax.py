import httpx
import json
from typing import List, Dict, Any, Optional

from app.config import settings


class MinimaxService:
    """Minimax API 服务"""
    
    def __init__(self):
        self.api_key = settings.minimax_api_key
        self.group_id = settings.minimax_group_id
        self.api_url = settings.minimax_api_url
    
    async def chat(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "abab6.5s-chat",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """
        与 Minimax 模型对话
        
        Args:
            messages: 消息列表，格式 [{"role": "user", "content": "..."}]
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大生成 token 数
            
        Returns:
            模型回复文本
        """
        if not self.api_key:
            return "[Minimax API 未配置]"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=60.0
                )
                response.raise_for_status()
                data = response.json()
                
                if "choices" in data and len(data["choices"]) > 0:
                    return data["choices"][0]["message"]["content"]
                return ""
            except Exception as e:
                return f"[调用 Minimax API 出错: {str(e)}]"
    
    async def select_articles(
        self, 
        user_input: str, 
        article_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        根据用户需求推荐文章
        
        Args:
            user_input: 用户输入的需求描述
            article_list: 可选文章列表
            
        Returns:
            推荐结果
        """
        articles_text = "\n".join([
            f"{i+1}. {a['title']} - {a.get('author', '未知')} ({a.get('dynasty', '未知')})"
            for i, a in enumerate(article_list[:50])  # 限制数量
        ])
        
        prompt = f"""你是一个古文专家。请从以下文章列表中，根据用户需求选择最合适的文章。

用户需求: {user_input}

可选文章:
{articles_text}

请返回 JSON 格式的结果:
{{
    "recommendations": [
        {{
            "article_index": 1,
            "reason": "推荐理由"
        }}
    ],
    "summary": "整体推荐说明"
}}"""

        messages = [{"role": "user", "content": prompt}]
        response = await self.chat(messages, temperature=0.5)
        
        try:
            # 尝试解析 JSON
            result = json.loads(response)
            return result
        except:
            return {
                "recommendations": [],
                "summary": response,
                "raw_response": response
            }
    
    async def generate_knowledge_points(
        self, 
        title: str, 
        author: str, 
        content: str
    ) -> List[Dict[str, Any]]:
        """
        为文章生成知识点
        
        Args:
            title: 文章标题
            author: 作者
            content: 文章内容
            
        Returns:
            知识点列表
        """
        prompt = f"""请分析以下古文，提取重要的知识点。

文章标题: {title}
作者: {author}
内容: {content[:2000]}...

请返回 JSON 格式的结果:
{{
    "points": [
        {{
            "type": "vocab",  // vocab(词汇), background(背景), analysis(赏析)
            "content": "知识点内容",
            "explanation": "详细解释"
        }}
    ]
}}"""

        messages = [{"role": "user", "content": prompt}]
        response = await self.chat(messages, temperature=0.3)
        
        try:
            result = json.loads(response)
            return result.get("points", [])
        except:
            return []
    
    async def translate_text(self, text: str) -> str:
        """
        翻译古文为现代汉语
        
        Args:
            text: 古文文本
            
        Returns:
            现代汉语翻译
        """
        prompt = f"""请将以下古文翻译成现代汉语，保持原文的韵味：

{text}

翻译:"""

        messages = [{"role": "user", "content": prompt}]
        return await self.chat(messages, temperature=0.3)
