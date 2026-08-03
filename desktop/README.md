# GCM by Piotrek 0.4.0 — edycja wydarzeń Google

GCM by Piotrek to dostępny klient Kalendarza Google dla Windows. Interfejs
wxPython jest testowany z NVDA, JAWS-em i Narratorem.

## Nowości w wersji 0.4.0

Wersja umożliwia edytowanie zwykłych wydarzeń znajdujących się w kalendarzach,
do których konto ma prawo zapisu.

Można zmienić:

- tytuł;
- typ: całodniowe albo godzinowe;
- datę i godzinę rozpoczęcia;
- datę i godzinę zakończenia;
- lokalizację;
- opis.

Kalendarz wydarzenia jest zachowywany. Przenoszenie wydarzeń między
kalendarzami nie jest jeszcze dostępne.

Aktualizacja używa częściowej operacji Google Calendar API. Pola, których GCM
jeszcze nie obsługuje — na przykład przypomnienia i dane konferencji — nie są
nadpisywane.

Jeżeli wydarzenie ma uczestników, przed zapisem pojawia się informacja, że
Google wyśle im aktualizację. Jeżeli zaznaczone wydarzenie jest pojedynczym
wystąpieniem cyklu, aplikacja ostrzega, że zmiana dotyczy tylko tej instancji.

Specjalne wydarzenia, takie jak urodziny, miejsce pracy, czas skupienia i
wydarzenia utworzone automatycznie z Gmaila, są na razie chronione przed
edycją.

## Uruchomienie

Rozpakuj wersję 0.4.0 do nowego katalogu i uruchom `uruchom_gcm.bat`.

Token i ustawienia są przechowywane w `%APPDATA%\GCM by Piotrek`, dlatego
logowanie oraz wybór kalendarzy powinny zostać zachowane.

## Skróty

- `Ctrl+N` — dodaj wydarzenie;
- `Ctrl+E` — edytuj zaznaczone wydarzenie;
- `Delete` — usuwanie, jeszcze niedostępne;
- `Ctrl+L` — zaloguj lub wyloguj;
- `Ctrl+K` — wybierz kalendarze;
- `Ctrl+F` — wyszukaj w bieżącym miesiącu;
- `Ctrl+G` — przejdź do daty;
- `Ctrl+D` — dzisiaj;
- `F5` — odśwież;
- `Alt+Strzałka w lewo` i `Alt+Strzałka w prawo` — zmiana miesiąca.
