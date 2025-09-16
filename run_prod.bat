@echo off
REM Start FastAPI backend
start "FastAPI Backend" cmd /k ".venv\Scripts\activate && python main.py"

REM Start Next.js frontend
start "Next.js Frontend" cmd /k "cd frontend && yarn build && yarn start --port 3001"

REM Keep the window open
pause
