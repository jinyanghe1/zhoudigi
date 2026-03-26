from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    app_name: str = "找到古籍"
    debug: bool = True
    
    # 数据库
    database_url: str = "sqlite:///./guji.db"
    
    # CORS
    cors_origins: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    
    # Minimax API
    minimax_api_key: str = ""
    minimax_group_id: str = ""
    minimax_api_url: str = "https://api.minimax.chat/v1/text/chatcompletion_v2"

    # DeepSeek API (fallback)
    deepseek_api_key: str = ""
    deepseek_api_url: str = "https://api.deepseek.com/chat/completions"

    # 维基文库 API
    wikisource_api_url: str = "https://zh.wikisource.org/w/api.php"
    
    class Config:
        env_file = ".env"
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 处理 cors_origins 如果是字符串的情况
        if isinstance(self.cors_origins, str):
            self.cors_origins = json.loads(self.cors_origins)


settings = Settings()
