# GCM by Piotrek 0.12.0 — stabilizacja dostępnego interfejsu

Wersja 0.12.0 rozpoczyna stabilizację przed dokumentacją i instalatorem.
Zakres funkcjonalny pozostaje taki sam jak w 0.11.2.

## Najważniejsza zmiana

Przyciski przekazują czytnikowi ekranu tylko:

- krótką nazwę;
- rolę przycisku;
- standardowy klawisz dostępu Windows `Alt+litera`.

Długie opisy działania oraz skróty `Ctrl`, `F1`, `F5` i `Delete` nie są już
powtarzane przy każdym przejściu Tabulatorem. Pełna lista skrótów nadal znajduje
się w pomocy otwieranej klawiszem `F1`.

Opisy pozostają przy polach, przy których wyjaśniają format albo sposób użycia.
Przycisk Ustawienia ma teraz krótką nazwę „Ustawienia”, ponieważ jego zawartość
jest opisana wewnątrz okna.

## Cel testu

Po przejściu na przycisk oczekiwany odczyt jest zbliżony do:

`Dodaj wydarzenie, N, przycisk`

Szczegółowa kolejność słów może zależeć od NVDA, JAWS-a albo Narratora, ale
czytnik nie powinien dopowiadać długiego opisu ani skrótu `Ctrl+N`.

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


## Aktualizacja 0.11.1

Po zapisaniu zmiany języka GCM pyta, czy uruchomić aplikację ponownie teraz. Użytkownik może wybrać „Uruchom ponownie teraz” albo „Później”. Ponowne uruchomienie zachowuje token Google, ustawienia i wybór kalendarzy. Pytanie nie pojawia się przy zmianie samych kalendarzy ani wtedy, gdy zmiana preferencji nie zmienia faktycznego języka interfejsu.


## Aktualizacja 0.11.2

- sprawdzanie stanu zapisanej sesji OAuth nie wykonuje już operacji sieciowej w głównym wątku interfejsu;
- odświeżenie wygasłego tokenu odbywa się wyłącznie w zadaniu działającym w tle;
- Ustawienia otwierają się natychmiast nawet wtedy, gdy Google jest niedostępny lub lista kalendarzy nie została pobrana;
- przycisk Ustawienia pozostaje dostępny podczas operacji Google;
- operacja Google, która nie odpowie w ciągu 45 sekund, nie może już pozostawić interfejsu trwale zablokowanego;
- brak `client_secret.json` jest wyjaśniany w dostępnym komunikacie przed otwarciem okna wyboru pliku;
- błędy otwierania Ustawień są pokazywane użytkownikowi i zapisywane w `last_error.txt`.

Na komputerze bez wcześniejszej konfiguracji GCM nadal wymaga pliku OAuth `client_secret.json` do rozpoczęcia logowania. Można skopiować go z `%APPDATA%\GCM by Piotrek` na poprzednim komputerze albo wskazać egzemplarz używany przez wtyczkę NVDA.
