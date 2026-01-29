import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ------------------------
# Database Configuration
# ------------------------
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ai:ai123@localhost:5432/digest")

# ------------------------
# OpenRouter API Configuration
# ------------------------
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")
OPENROUTER_API_BASE = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_URL = OPENROUTER_API_BASE  

# ------------------------
# Email Configuration
# ------------------------
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = SMTP_USER

# ------------------------
# Application Settings
# ------------------------
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DIGEST_GENERATION_TIME = os.getenv("DIGEST_GENERATION_TIME", "09:00")
MAX_ARTICLES_PER_DIGEST = int(os.getenv("MAX_ARTICLES_PER_DIGEST", 5))
ARTICLE_AGE_LIMIT_DAYS = int(os.getenv("ARTICLE_AGE_LIMIT_DAYS", 7))

# ------------------------
# Constants
# ------------------------
RETRY_ATTEMPTS = 3
RETRY_DELAY_SECONDS = 5
REQUEST_TIMEOUT = 30