import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    """Base configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'crm_local.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-in-production")
    
    CHATBOT_BASE_URL = os.getenv("CHATBOT_BASE_URL", "http://localhost:5001")
    CHATBOT_TIMEOUT = (5, 10)
    CHATBOT_MAX_RETRIES = 3
    
    WEBHOOK_ENABLED = os.getenv("WEBHOOK_ENABLED", "True").lower() == "true"
    WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "dev-webhook-secret")
    
    RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
    EMAIL_FROM = os.getenv("EMAIL_FROM", "onboarding@resend.dev")
    EMAIL_FROM_NAME = os.getenv("EMAIL_FROM_NAME", "LexFlow")
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")
    
    CORS_ORIGINS = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000;http://localhost:5173"
    ).split(";")


class DevelopmentConfig(Config):
    """Development configuration."""
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = False
    
    CHATBOT_BASE_URL = os.getenv("CHATBOT_BASE_URL", "http://localhost:5001")
    
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]


class ProductionConfig(Config):
    """Production configuration."""
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False
    
    CHATBOT_BASE_URL = os.getenv("CHATBOT_BASE_URL", "https://chatbot-prod.example.com")
    
    CORS_ORIGINS = [
        "https://poetic-kleicha-28d058.netlify.app",
        os.getenv("RAILWAY_PUBLIC_DOMAIN", "https://lexflow-prod.up.railway.app"),
        os.getenv("FRONTEND_URL", "https://lexflow.example.com")
    ]


class TestingConfig(Config):
    """Testing configuration."""
    FLASK_ENV = "testing"
    DEBUG = True
    TESTING = True
    
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    
    CHATBOT_BASE_URL = "http://localhost:5001"
    
    CORS_ORIGINS = ["*"]


def get_config():
    """Get configuration based on FLASK_ENV."""
    env = os.getenv("FLASK_ENV", "development")
    
    config_map = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }
    
    return config_map.get(env, DevelopmentConfig)


Config = get_config()
