@echo off
echo ===============================================
echo   SmartApply Pro - Web Application
echo ===============================================
echo.
echo Starting Flask development server...
echo.
echo Access the application at:
echo   http://localhost:5000
echo.
echo Press CTRL+C to stop the server
echo ===============================================
echo.

cd /d "%~dp0"
python app.py

pause
