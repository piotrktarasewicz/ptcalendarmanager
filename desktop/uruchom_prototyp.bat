@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"

set "PYTHON_CMD="

rem Najpierw próbujemy znaleźć interpreter przez launcher py.
where py >nul 2>nul
if not errorlevel 1 (
    for %%V in (3.13 3.12 3.11 3.10) do (
        py -%%V -c "import sys; raise SystemExit(0 if sys.version_info >= (3,10) else 1)" >nul 2>nul
        if not errorlevel 1 if not defined PYTHON_CMD set "PYTHON_CMD=py -%%V"
    )
)

rem Jeżeli launcher nie znalazł Pythona, próbujemy zwykłego polecenia python.
if not defined PYTHON_CMD (
    where python >nul 2>nul
    if not errorlevel 1 (
        python -c "import sys; raise SystemExit(0 if sys.version_info >= (3,10) else 1)" >nul 2>nul
        if not errorlevel 1 set "PYTHON_CMD=python"
    )
)

if not defined PYTHON_CMD (
    echo.
    echo Nie znaleziono zainstalowanego interpretera Python 3.10 lub nowszego.
    echo.
    echo Na komputerze jest launcher "py", ale nie ma wlasciwego Pythona.
    echo Zainstaluj 64-bitowy Python 3.12 albo 3.13 ze strony python.org.
    echo Podczas instalacji zaznacz opcje:
    echo   1. Add Python to PATH
    echo   2. Install launcher for all users
    echo.
    echo Po instalacji ponownie uruchom ten plik.
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
echo Uruchomienie prototypu nie powiodlo sie.
echo Sprawdz komunikaty powyzej.
pause
exit /b 1
