@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if errorlevel 1 (
    echo Nie znaleziono programu uruchamiajacego Python "py".
    echo Zainstaluj 64-bitowy Python 3.12 i zaznacz dodanie Pythona do PATH.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Tworzenie srodowiska Python...
    py -3.12 -m venv .venv
    if errorlevel 1 goto :error

    call ".venv\Scripts\activate.bat"
    python -m pip install --upgrade pip
    if errorlevel 1 goto :error

    python -m pip install -r requirements.txt
    if errorlevel 1 goto :error
) else (
    call ".venv\Scripts\activate.bat"
)

set "PYTHONPATH=%CD%\src"
python launcher.py
if errorlevel 1 goto :error
exit /b 0

:error
echo.
echo Uruchomienie prototypu nie powiodlo sie.
pause
exit /b 1
