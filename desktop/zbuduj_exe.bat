@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"

set "PYTHON_CMD="
where py >nul 2>nul
if not errorlevel 1 (
    for %%V in (3.13 3.12 3.11 3.10) do (
        py -%%V -c "import sys; raise SystemExit(0 if (3,10) <= sys.version_info[:2] < (3,14) else 1)" >nul 2>nul
        if not errorlevel 1 if not defined PYTHON_CMD set "PYTHON_CMD=py -%%V"
    )
)
if not defined PYTHON_CMD (
    where python >nul 2>nul
    if not errorlevel 1 (
        python -c "import sys; raise SystemExit(0 if (3,10) <= sys.version_info[:2] < (3,14) else 1)" >nul 2>nul
        if not errorlevel 1 set "PYTHON_CMD=python"
    )
)
if not defined PYTHON_CMD (
    echo.
    echo Nie znaleziono 64-bitowego Pythona w wersji 3.10-3.13.
    echo Zainstaluj Python 3.12 albo 3.13 ze strony python.org.
    echo Podczas instalacji zaznacz Add Python to PATH.
    echo.
    pause
    exit /b 1
)

echo Znaleziono zgodny interpreter: %PYTHON_CMD%
if not exist ".venv-build\Scripts\python.exe" (
    echo Tworzenie srodowiska do budowania...
    %PYTHON_CMD% -m venv .venv-build
    if errorlevel 1 goto :error
)
call ".venv-build\Scripts\activate.bat"
python -m pip install --upgrade pip
if errorlevel 1 goto :error
python -m pip install -r requirements-build.txt
if errorlevel 1 goto :error
rmdir /s /q build 2>nul
rmdir /s /q "dist\GCM by Piotrek" 2>nul
python -m PyInstaller ^
    --noconfirm ^
    --clean ^
    --windowed ^
    --onedir ^
    --name "GCM by Piotrek" ^
    --paths src ^
    --collect-all googleapiclient ^
    --collect-all google_auth_oauthlib ^
    --collect-all tzdata ^
    launcher.py
if errorlevel 1 goto :error
echo.
echo Gotowe. Program znajduje sie w:
echo dist\GCM by Piotrek
pause
exit /b 0
:error
echo.
echo Budowanie programu nie powiodlo sie.
pause
exit /b 1
