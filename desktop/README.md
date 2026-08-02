# GCM by Piotrek 0.3.0 — dodawanie wydarzeń

GCM by Piotrek to dostępny klient Kalendarza Google dla Windows. Interfejs
wxPython został praktycznie sprawdzony z NVDA, JAWS-em i Narratorem.

## Nowość w wersji 0.3.0

W tej wersji po raz pierwszy można tworzyć prawdziwe wydarzenia w Kalendarzu
Google. Odczyt z wersji 0.2.0 pozostaje bez zmian.

Dodawanie obsługuje:

- wybór kalendarza docelowego;
- pokazywanie tylko kalendarzy, do których konto ma prawo zapisu;
- wydarzenia godzinowe i całodniowe;
- wydarzenia jednodniowe i wielodniowe;
- osobną datę rozpoczęcia i datę zakończenia;
- tytuł, lokalizację i opis;
- walidację dat oraz godzin;
- potwierdzenie przed wysłaniem danych do Google;
- automatyczne odświeżenie miesiąca i ustawienie fokusu na utworzonym wydarzeniu.

Data zakończenia wydarzenia całodniowego jest wpisywana **włącznie**. Aplikacja
sama przelicza ją na wymagany przez Google wyłączny koniec zakresu.

## Czego jeszcze nie ma

Edycja i usuwanie pozostają nieaktywne funkcjonalnie i pokazują informację o
kolejnym etapie. Zostaną wdrożone osobno, po potwierdzeniu bezpiecznego tworzenia
wydarzeń.

## Uruchomienie

Rozpakuj katalog i uruchom `uruchom_gcm.bat`. Jeżeli środowisko `.venv` z
poprzedniej wersji nie znajduje się w tym nowym katalogu, skrypt utworzy je i
zainstaluje biblioteki.

Aplikacja nadal przechowuje własny token i ustawienia w:

`%APPDATA%\GCM by Piotrek`

Nie zmienia tokenu ani ustawień dodatku NVDA.

## Skróty

- `Ctrl+N` — dodaj wydarzenie;
- `Ctrl+E` — edycja, jeszcze niedostępna;
- `Delete` — usuwanie, jeszcze niedostępne;
- `Ctrl+L` — zaloguj lub wyloguj;
- `Ctrl+K` — wybierz kalendarze;
- `Ctrl+F` — wyszukaj w bieżącym miesiącu;
- `Ctrl+G` — przejdź do daty;
- `Ctrl+D` — dzisiaj;
- `F5` — odśwież;
- `Alt+Strzałka w lewo` i `Alt+Strzałka w prawo` — zmiana miesiąca.

## Zalecany pierwszy test zapisu

Utwórz jedno wyraźnie testowe wydarzenie, na przykład `Test GCM 0.3.0`, w
wybranym kalendarzu i na bliski termin. Po zapisaniu sprawdź je także w oficjalnym
Kalendarzu Google. Do czasu wdrożenia usuwania możesz usunąć test ręcznie w
Kalendarzu Google albo za pomocą dodatku NVDA.
