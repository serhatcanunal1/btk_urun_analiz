"""
Konfigürasyon ayarları
"""

import os
from dotenv import load_dotenv
from typing import Optional

# .env dosyasını yükle
load_dotenv()


class Config:
    """Uygulama konfigürasyonu"""
    
    def __init__(self):
        # Gemini API
        self.gemini_api_key: str = os.getenv('GEMINI_API_KEY', 'your_gemini_api_key_here')
        
        # Database
        self.database_url: str = os.getenv('DATABASE_URL', 'sqlite:///./product_analysis.db')
        
        # Web scraping ayarları
        self.user_agent: str = os.getenv(
            'USER_AGENT', 
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        self.request_delay: int = int(os.getenv('REQUEST_DELAY', '2'))
        self.max_retries: int = int(os.getenv('MAX_RETRIES', '3'))
        
        # API ayarları
        self.max_workers: int = int(os.getenv('MAX_WORKERS', '5'))
        self.analysis_timeout: int = int(os.getenv('ANALYSIS_TIMEOUT', '300'))
        
        # Debug mod
        self.debug: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    
    def validate(self) -> bool:
        """Konfigürasyonu doğrula"""
        if self.gemini_api_key == 'your_gemini_api_key_here':
            print("⚠️  UYARI: Gemini API anahtarı ayarlanmamış!")
            return False
        return True
    
    def get_selenium_options(self) -> dict:
        """Selenium ayarlarını döndür"""
        return {
            'headless': not self.debug,
            'user_agent': self.user_agent,
            'window_size': (1920, 1080),
            'page_load_timeout': 30
        }
