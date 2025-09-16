@echo off
REM Start FastAPI backend
start "FastAPI Backend" cmd /k ".venv\Scripts\activate && export DEBUG=1 && python main.py"

REM Start Next.js frontend
start "Next.js Frontend" cmd /k "cd frontend && yarn dev"

REM Keep the window open
pause
