# PT Calendar Manager 0.16.2

**Dostępna aplikacja do obsługi Kalendarza Google**  
**Accessible desktop application for Google Calendar**

PT Calendar Manager jest samodzielną aplikacją dla Windows, przeznaczoną do
szybkiego i dostępnego zarządzania wydarzeniami Kalendarza Google. Interfejs
jest obsługiwany klawiaturą i praktycznie przetestowany z NVDA, JAWS-em oraz
Narratorem.

Wersja 0.16.2 zamraża zakres funkcji przed publiczną weryfikacją Google OAuth i
wprowadza kompletną warstwę wydaniową: licencję, informacje o zależnościach,
metadane pliku EXE, wersję przenośną oraz projekt instalatora Windows.

## Status Google OAuth

Aplikacja nie przeszła jeszcze publicznej weryfikacji Google. Do czasu jej
zakończenia logowanie może być dostępne wyłącznie dla kont dodanych jako
użytkownicy testowi projektu OAuth. Numer 1.0 RC zostanie nadany dopiero po
przejściu tego etapu.

## Dokumentacja / Documentation

- [Dokumentacja polska](docs/DOKUMENTACJA_pl.md)
- [English documentation](docs/DOCUMENTATION_en.md)
- [Instalacja i aktualizacja](docs/INSTALACJA_pl.md)
- [Installation and updates](docs/INSTALLATION_en.md)
- [Polityka prywatności](docs/PRIVACY_pl.md)
- [Privacy Policy](docs/PRIVACY_en.md)
- [Informacje prawne](docs/LEGAL_pl.md)
- [Legal Information](docs/LEGAL_en.md)
- [Licencja](LICENSE)
- [Komponenty zewnętrzne](THIRD_PARTY_NOTICES.md)
- [Kod źródłowy odpowiadający wydaniu](SOURCE_CODE.md)

## Licencja

Copyright (C) 2026 Piotr Tarasewicz.

PT Calendar Manager jest wolnym oprogramowaniem udostępnionym na licencji
GNU General Public License w wersji 3 lub nowszej (`GPL-3.0-or-later`). Program
jest rozpowszechniany bez gwarancji. Pełny tekst znajduje się w pliku
`LICENSE`.

Projekt powstał przez adaptację i znaczące rozwinięcie kodu oraz koncepcji
dodatku Google Calendar Manager dla NVDA, również autorstwa Piotra
Tarasewicza i również objętego GPL-3.0-or-later.

## Pakiety wydaniowe

Na komputerze Windows uruchom:

`zbuduj_wydanie.bat`

Skrypt przygotowuje w katalogu `release`:

- instalator `PT-Calendar-Manager-0.16.2-Setup.exe`;
- wersję przenośną `pt-calendar-manager-0.16.2-portable.zip`;
- odpowiadający kod źródłowy `pt-calendar-manager-0.16.2-source.zip`;
- plik `SHA256SUMS.txt`.

Wymagane są 64-bitowy Python 3.10-3.13 oraz Inno Setup 6 albo 7. Szczegóły są
w `RELEASE_ENGINEERING.md`.

## Ważna informacja / Important notice

PT Calendar Manager jest niezależną aplikacją do obsługi Kalendarza Google.
Program nie jest produktem Google LLC, nie jest przez Google sponsorowany ani
oficjalnie zatwierdzony. Google Calendar jest znakiem towarowym Google LLC.

PT Calendar Manager is an independent application for accessing Google
Calendar. It is not a Google LLC product and is not sponsored or endorsed by
Google. Google Calendar is a trademark of Google LLC.

## Uruchomienie wersji rozwojowej

1. Rozpakuj archiwum do nowego katalogu.
2. Uruchom `uruchom_pt_calendar_manager.bat`.
3. Dane użytkownika są przechowywane w `%APPDATA%\PT Calendar Manager`.

Token Google jest szyfrowany mechanizmem Windows DPAPI i przechowywany w
pliku `token.dat`.
