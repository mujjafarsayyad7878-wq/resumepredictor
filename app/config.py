"""
Application Configuration and Settings
"""
import os
from pydantic import BaseModel
from typing import List, Dict, Any

class Settings(BaseModel):
    APP_NAME: str = "Smart Resume Skill-Gap & Career Predictor"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    CORS_ORIGINS: List[str] = ["*"]
    
    # Matching algorithm weights (sum to 1.0)
    WEIGHT_TFIDF: float = 0.35          # Semantic content similarity
    WEIGHT_EXACT_SKILLS: float = 0.45   # Hard skills coverage
    WEIGHT_EXPERIENCE: float = 0.12     # Seniority & experience match
    WEIGHT_EDUCATION: float = 0.08      # Education / degree requirement match

settings = Settings()
