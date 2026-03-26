import httpx
from typing import List, Dict, Any

from app.config import settings


class DeepSeekService:
    """DeepSeek API 服务 (作为 Minimax 的 fallback)"""

    def __init__(self):
        self.api_key = settings.deepseek_api_key
        self.api_url = settings.deepseek_api_url

    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "deepseek-chat",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """
        与 DeepSeek 模型对话

        Args:
            messages: 消息列表，格式 [{"role": "user", "content": "..."}]
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大生成 token 数

        Returns:
            模型回复文本
        """
        if not self.api_key:
            return "[DeepSeek API 未配置]"

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
                return f"[调用 DeepSeek API 出错: {str(e)}]"

    async def translate_text(self, text: str) -> str:
        """
        翻译古文为现代汉语

        Args:
            text: 古文文本

        Returns:
            现代汉语翻译
        """
        prompt = f"""你是一位精通古文的学者。请将以下古文翻译成流畅的现代白话文。

翻译要求:
1. 准确传达原意,不增不减,不曲解
2. 语言流畅自然,符合现代阅读习惯
3. 适当保留原文的修辞手法和语气
4. 对于一词多义的情况,在翻译后用括号注明其他可能的解释
5. 译文要有一定的文学性,不能生硬直译

古文原文:
{text}

现代译文:"""

        messages = [{"role": "user", "content": prompt}]
        return await self.chat(messages, temperature=0.5)
