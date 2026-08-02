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
if not exist ".venv\Scripts\python.exe" (
    echo Tworzenie srodowiska Python...
    %PYTHON_CMD% -m venv .venv
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
echo Uruchomienie GCM by Piotrek nie powiodlo sie.
echo Sprawdz komunikaty powyzej oraz plik last_error.txt w katalogu danych aplikacji.
pause
exit /b 1
