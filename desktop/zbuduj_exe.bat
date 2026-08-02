@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if errorlevel 1 (
    echo Nie znaleziono programu uruchamiajacego Python "py".
    echo Zainstaluj 64-bitowy Python 3.12.
    pause
    exit /b 1
)

if not exist ".venv-build\Scripts\python.exe" (
    echo Tworzenie srodowiska do budowania...
    py -3.12 -m venv .venv-build
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
pause
exit /b 1
