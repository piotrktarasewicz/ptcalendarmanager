# PT Calendar Manager 0.15.1

**Dostępna aplikacja do obsługi Kalendarza Google**  
**Accessible desktop application for Google Calendar**

PT Calendar Manager jest samodzielną aplikacją dla Windows, przeznaczoną do szybkiego i dostępnego zarządzania wydarzeniami Kalendarza Google. Interfejs jest obsługiwany klawiaturą i testowany z NVDA, JAWS-em oraz Narratorem.

PT Calendar Manager is a standalone Windows application for quick and accessible Google Calendar event management. Its interface is keyboard-driven and tested with NVDA, JAWS and Narrator.

## Interfejs 0.15.1

Główne okno zawiera natywny pasek menu Windows oraz dwie listy: dni miesiąca i wydarzenia wybranego dnia. Tabulator przełącza tylko między listami. Wszystkie polecenia są dostępne z menu, przez dotychczasowe skróty oraz z menu kontekstowych otwieranych klawiszem `Shift+F10`.

The main window contains a native Windows menu bar and two lists: days of the month and events on the selected day. Tab moves only between the lists. All commands remain available from the menu bar, existing keyboard shortcuts and context menus opened with `Shift+F10`.

Kolory pozostają zgodne z ustawieniami Windows. Systemowy kolor akcentu jest używany jedynie przy nagłówku miesiąca i nazwach dwóch paneli.

W oknie Ustawień instrukcja wyboru kalendarzy jest osobnym elementem tylko do odczytu w kolejności Tabulatora, dzięki czemu jest odczytywana także przez JAWS i Narratora.

## Dokumentacja / Documentation

- [Dokumentacja polska](docs/DOKUMENTACJA_pl.md)
- [English documentation](docs/DOCUMENTATION_en.md)
- [Polityka prywatności](docs/PRIVACY_pl.md)
- [Privacy Policy](docs/PRIVACY_en.md)
- [Informacje prawne](docs/LEGAL_pl.md)
- [Legal Information](docs/LEGAL_en.md)

## Ważna informacja / Important notice

PT Calendar Manager jest niezależną aplikacją do obsługi Kalendarza Google. Program nie jest produktem Google LLC, nie jest przez Google sponsorowany ani oficjalnie zatwierdzony. Google Calendar jest znakiem towarowym Google LLC.

PT Calendar Manager is an independent application for accessing Google Calendar. It is not a Google LLC product and is not sponsored or endorsed by Google. Google Calendar is a trademark of Google LLC.

## Uruchomienie wersji rozwojowej

1. Rozpakuj archiwum do nowego katalogu.
2. Uruchom `uruchom_pt_calendar_manager.bat`.
3. Dane użytkownika są przechowywane w `%APPDATA%\PT Calendar Manager`.

Token Google jest szyfrowany mechanizmem Windows DPAPI i przechowywany w pliku `token.dat`.
