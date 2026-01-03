"""Configuration settings for AI Executive Agent"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Global settings for the AI agent"""
    
    # LLM Configuration
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    LLM_MODEL = "gemini-pro"
    LLM_TEMPERATURE = 0.3
    LLM_MAX_TOKENS = 2000
    
    # Comet ML Configuration
    COMET_API_KEY = os.getenv("COMET_API_KEY")
    COMET_PROJECT_NAME = os.getenv("COMET_PROJECT_NAME", "ai-executive-agent")
    COMET_WORKSPACE = os.getenv("COMET_WORKSPACE")
    
    # Opik Configuration
    OPIK_API_KEY = os.getenv("OPIK_API_KEY")
    OPIK_WORKSPACE = os.getenv("OPIK_WORKSPACE")
    
    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/ai_agent")
    
    # ChromaDB Configuration
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./data/chromadb")
    
    # Browser Configuration
    BROWSER_TIMEOUT = int(os.getenv("BROWSER_TIMEOUT", "30000"))
    BROWSER_HEADLESS = os.getenv("BROWSER_HEADLESS", "true").lower() == "true"
    
    # Agent Configuration
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY = int(os.getenv("RETRY_DELAY", "5"))
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "./logs/agent.log")
    
    # API Configuration
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", os.getenv("PORT", "7860")))  # Support Spaces PORT env
    
    # Feature Flags
    ENABLE_MONITORING = os.getenv("ENABLE_MONITORING", "true").lower() == "true"
    ENABLE_LOGGING = os.getenv("ENABLE_LOGGING", "true").lower() == "true"
    ENABLE_BROWSER_AUTOMATION = os.getenv("ENABLE_BROWSER_AUTOMATION", "true").lower() == "true"

# Create settings instance
settings = Settings()
