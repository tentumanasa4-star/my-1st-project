@echo off
echo ======================================================================
echo           Starting CampusEvents - College Event Management Platform
echo ======================================================================
echo.

echo Starting Flask REST API Backend (Port 5000)...
start "CampusEvents Backend (Flask)" cmd /k "cd /d %~dp0backend && .\venv\Scripts\python app.py"

timeout /t 3 /nobreak >nul

echo Starting React + TypeScript Frontend (Port 5173)...
start "CampusEvents Frontend (Vite)" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ======================================================================
echo   Backend URL : http://127.0.0.1:5000
echo   Frontend URL: http://localhost:5173
echo.
echo   Demo Student: student@campus.edu  / password123
echo   Demo Admin  : admin@campus.edu    / admin123
echo ======================================================================
echo.
pause
