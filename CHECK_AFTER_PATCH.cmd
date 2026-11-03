@echo off
setlocal
cd /d "%~dp0"

if not exist "%~dp0manage.py" (
    echo ERROR: manage.py was not found.
    echo Extract this ZIP directly into your tech-creator-studio project folder.
    pause
    exit /b 1
)

set "PYTHON=%~dp0venv\Scripts\python.exe"
if not exist "%PYTHON%" set "PYTHON=python"

echo.
echo Running Django system checks...
"%PYTHON%" manage.py check
if errorlevel 1 goto failed

echo.
echo Running content integration tests...
"%PYTHON%" manage.py test content
if errorlevel 1 goto failed

echo.
echo SUCCESS: system check and content tests passed.
pause
exit /b 0

:failed
echo.
echo A check or test failed. Copy the complete error output and send it in ChatGPT.
pause
exit /b 1
