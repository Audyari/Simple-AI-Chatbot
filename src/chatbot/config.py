import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # API Keys
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    
    # Model configurations
    DEFAULT_MODEL = 'gemini-1.5-flash'
    
    # Chat settings
    MAX_TOKENS = 1000
    TEMPERATURE = 0.7
    
    # UI settings
    BOT_NAME = "AI Assistant"
    USER_NAME = "You"
    
    @classmethod
    def validate_config(cls):
        """Validasi konfigurasi yang diperlukan."""
        if not cls.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY tidak ditemukan di file .env\n"
                "Silakan dapatkan API key dari https://aistudio.google.com/app/apikey"
            )
