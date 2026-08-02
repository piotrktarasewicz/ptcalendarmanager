@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"

set "PYTHON_CMD="

where py >nul 2>nul
if not errorlevel 1 (
    for %%V in (3.13 3.12 3.11 3.10) do (
        py -%%V -c "import sys; raise SystemExit(0 if sys.version_info >= (3,10) else 1)" >nul 2>nul
        if not errorlevel 1 if not defined PYTHON_CMD set "PYTHON_CMD=py -%%V"
    )
)

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
    echo Zainstaluj 64-bitowy Python 3.12 albo 3.13 ze strony python.org.
    echo Podczas instalacji zaznacz opcje Add Python to PATH.
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
rmdir /s /q "dist\GCM by Piotrek - prototyp" 2>nul

python -m PyInstaller ^
    --noconfirm ^
    --clean ^
    --windowed ^
    --onedir ^
    --name "GCM by Piotrek - prototyp" ^
    --paths src ^
    launcher.py

if errorlevel 1 goto :error

echo.
echo Gotowe.
echo Program znajduje sie w katalogu:
echo dist\GCM by Piotrek - prototyp
pause
exit /b 0

:error
echo.
echo Budowanie pliku EXE nie powiodlo sie.
echo Sprawdz komunikaty powyzej.
pause
exit /b 1
