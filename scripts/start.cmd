@echo off
rem Start MyGallery. Double-click this file.
rem
rem Prepares a private Python environment on first run, then starts the
rem application and opens it in your browser. See README.md.

setlocal
cd /d "%~dp0.."

set "PYTHON=.venv\Scripts\python.exe"

if not exist "%PYTHON%" (
    echo Setting up MyGallery for the first time. This takes a minute...
    py -3 -m venv .venv 2>nul || python -m venv .venv
    if errorlevel 1 (
        echo.
        echo Could not find Python. Install Python 3.12 or later from
        echo https://www.python.org/downloads/windows/ and tick
        echo "Add python.exe to PATH" during installation.
        echo.
        pause
        exit /b 1
    )
    "%PYTHON%" -m pip install --quiet --upgrade pip
    "%PYTHON%" -m pip install --quiet -e .
)

"%PYTHON%" -m mygallery
