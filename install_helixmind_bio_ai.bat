@echo off
title Install HelixMind Bio AI
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Install Python 3.10+ and enable Add Python to PATH.
  pause
  exit /b 1
)

if not exist ".venv" python -m venv .venv
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
pip install -r requirements_helixmind_bio_ai.txt

echo.
echo Done. Double-click HelixMindBioAI.bat to start.
pause
