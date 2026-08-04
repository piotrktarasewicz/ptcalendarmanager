# GCM by Piotrek 0.11.0 — Polski i English

GCM by Piotrek jest dostępnym klientem Kalendarza Google dla Windows,
testowanym z NVDA, JAWS-em i Narratorem. Służy do szybkiego, doraźnego
zarządzania kalendarzem, a bardziej zaawansowane funkcje pozostawia oficjalnemu
interfejsowi Google.

## Nowości w wersji 0.11.0

- pełny interfejs po polsku i po angielsku;
- automatyczny wybór języka na podstawie języka interfejsu Windows;
- ręczny wybór: `Automatycznie`, `Polski` albo `English`;
- jedno okno `Ustawienia`, zawierające język aplikacji i wybór kalendarzy;
- usunięcie osobnego przycisku wyboru kalendarzy z głównego okna;
- skrót `Ctrl+,` do ustawień;
- zachowanie `Ctrl+K` jako zgodnego wstecz skrótu do ustawień;
- angielska pomoc, komunikaty, formularze, potwierdzenia, błędy, daty, dni,
  miesiące i opisy dostępności;
- przyjmowanie dat w formacie `DD.MM.RRRR` albo ISO `RRRR-MM-DD` niezależnie
  od języka interfejsu;
- automatyczna migracja starszego pliku ustawień bez pola języka.

Zmiana języka zaczyna działać po ponownym uruchomieniu aplikacji. Nie jest
używane tłumaczenie internetowe ani maszynowe — oba zestawy komunikatów są
wbudowane i kontrolowane razem z kodem aplikacji.

## Ustawienia

Przycisk `Ustawienia` jest dostępny także przed zalogowaniem. Bez logowania
można zmienić język. Po zalogowaniu w tym samym oknie można wybrać kalendarze,
których wydarzenia mają być pokazywane.

Ustawienia są zapisywane w `%APPDATA%\GCM by Piotrek\settings.json`.
Dotychczasowy token OAuth i wybór kalendarzy pozostają zachowane podczas
uruchomienia wersji 0.11.0.

## Najważniejsze skróty

- `Ctrl+,` — ustawienia;
- `Ctrl+K` — ustawienia, zachowany dawny skrót wyboru kalendarzy;
- `Ctrl+L` — logowanie albo wylogowanie;
- `F1` — pomoc;
- `Ctrl+N` — dodawanie wydarzenia;
- `Ctrl+E` — edycja wydarzenia;
- `Delete` — usuwanie;
- `Ctrl+F` — wyszukiwanie;
- `Ctrl+G` — przejście do daty;
- `F5` — odświeżenie;
- `Ctrl+Shift+G` — otwarcie wydarzenia w Kalendarzu Google;
- `Ctrl+J` — otwarcie lub skopiowanie istniejącego linku spotkania.

Pełna lista znajduje się w pomocy otwieranej klawiszem `F1`.

## Uruchomienie wersji rozwojowej

Rozpakuj archiwum do nowego katalogu i uruchom `uruchom_gcm.bat`.
Pierwsze uruchomienie tworzy lokalne środowisko Pythona i instaluje zależności.

---

# GCM by Piotrek 0.11.0 — Polish and English

GCM by Piotrek is an accessible Google Calendar client for Windows, tested
with NVDA, JAWS and Narrator. It is designed for quick everyday calendar
management. More advanced operations remain available in Google's official
interface.

## What's new in 0.11.0

- complete Polish and English interface;
- automatic language selection based on the Windows display language;
- manual `Automatic`, `Polish` or `English` selection;
- one `Settings` window for both language and calendar selection;
- the separate calendar button was removed from the main window;
- `Ctrl+,` opens Settings;
- `Ctrl+K` remains available as a backward-compatible Settings shortcut;
- English help, messages, forms, confirmations, errors, dates, weekdays,
  months and accessibility descriptions;
- both `DD.MM.YYYY` and ISO `YYYY-MM-DD` date input in either interface language;
- automatic migration of older settings files without a language field.

A language change takes effect after the application is restarted. GCM does
not use online or machine translation; both language sets are bundled with and
reviewed as part of the application.

## Settings

Settings can be opened before signing in, so the application language is always
available. After signing in, the same window also contains the calendars whose
events should be displayed.

Settings are stored in `%APPDATA%\GCM by Piotrek\settings.json`. Existing OAuth
tokens and calendar selection are preserved when upgrading to 0.11.0.

## Development launch

Extract the archive into a new folder and run `uruchom_gcm.bat`. The first run
creates a local Python environment and installs the required dependencies.
