@echo off
title Smart Resume Skill-Gap & Career Predictor
echo ======================================================================
echo   Starting Smart Resume Skill-Gap & Career Predictor...
echo ======================================================================
echo.

:: Open browser after 2 seconds in parallel
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:8000"

:: Launch the FastAPI server
py run.py
pause
