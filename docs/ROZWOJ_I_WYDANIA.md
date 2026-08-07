# Rozwój i wydania

## Wymagania wspólne

- Windows 10 lub 11 do uruchamiania i ręcznych testów interfejsu;
- Python 3.10–3.13 dla aplikacji samodzielnej;
- Python 3.13 AMD64 dla dodatku zgodnego z NVDA 2026.1;
- PowerShell;
- Inno Setup 6 lub 7 do budowania instalatora aplikacji.

## Aplikacja samodzielna

Kod aplikacji znajduje się w `desktop/`.

Uruchomienie wersji rozwojowej w Windows:

```text
desktop\uruchom_pt_calendar_manager.bat
```

Kontrola składni i testy:

```text
python -m compileall -q desktop/src desktop/tools desktop/tests
set PYTHONPATH=desktop\src
python -m unittest discover -s desktop/tests -p "test*.py" -v
```

Oficjalne wydanie z konfiguracją klienta OAuth buduje polecenie uruchomione w katalogu `desktop`:

```text
powershell -ExecutionPolicy Bypass -File tools\build_release.ps1 -IncludeOAuthClient
```

Proces tworzy instalator, wersję przenośną, źródłowy ZIP i plik sum SHA-256. Artefakty binarne należy publikować w GitHub Releases, nie w historii Git.

## Dodatek NVDA

Kod dodatku znajduje się w `nvda-addon/`. Szczegółowy proces przygotowania zależności i paczki opisuje `nvda-addon/BUILD.md`.

Podstawowa kontrola składni:

```text
python -m compileall -q nvda-addon/globalPlugins/googleCalendarManager
```

Paczka wydania musi zawierać zależności zgodne z CPython 3.13 AMD64 oraz wymaganą konfigurację klienta OAuth. Publiczne źródła zawierają wyłącznie `client_secret.example.json`.

## Lista kontrolna przed wydaniem

1. Sprawdź numery wersji we wszystkich metadanych.
2. Uruchom kompilację składni i testy automatyczne.
3. Wykonaj ręczny test klawiatury i czytnika ekranu.
4. Sprawdź czyste konto Windows oraz instalację lub aktualizację.
5. Potwierdź brak `client_secret.json`, `token.json`, `token.dat`, `.env`, plików diagnostycznych i danych użytkownika w źródłach.
6. Sprawdź integralność archiwów i oblicz SHA-256.
7. Opublikuj gotowe paczki w GitHub Releases.
8. Zaktualizuj README, dokumentację i informacje o wydaniu.

## Tagi

- `desktop-v0.16.3` wskazuje wydanie PT Calendar Manager 0.16.3;
- `v1.0.4` wskazuje wydanie dodatku Google Calendar Manager 1.0.4.

Numery wersji aplikacji i dodatku są niezależne.
