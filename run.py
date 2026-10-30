"""
Launch script for Smart Resume Skill-Gap & Career Predictor
Usage: py run.py
"""
import sys
import io

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import uvicorn
from app.config import settings

if __name__ == "__main__":
    print("=" * 70)
    print(f"[*] Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"[*] Dashboard available at: http://{settings.HOST}:{settings.PORT}")
    print(f"[*] Swagger OpenAPI docs at: http://{settings.HOST}:{settings.PORT}/docs")
    print("=" * 70)
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        log_level="info"
    )
