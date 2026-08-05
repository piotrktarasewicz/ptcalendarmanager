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
    echo Compatible 64-bit Python 3.10-3.13 was not found.
    echo Zainstaluj Python 3.12 albo 3.13 ze strony python.org.
    echo Install Python 3.12 or 3.13 from python.org.
    echo Podczas instalacji zaznacz Add Python to PATH.
    echo During installation, select Add Python to PATH.
    echo.
    pause
    exit /b 1
)

echo Interpreter / Python: %PYTHON_CMD%
if not exist ".venv\Scripts\python.exe" (
    echo Tworzenie srodowiska Python / Creating Python environment...
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
echo Uruchomienie PT Calendar Manager nie powiodlo sie.
echo PT Calendar Manager could not be started.
echo Sprawdz komunikaty powyzej oraz plik last_error.txt w katalogu danych aplikacji.
echo Check the messages above and last_error.txt in the application data folder.
pause
exit /b 1
