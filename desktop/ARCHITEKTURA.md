# Architektura GCM by Piotrek

Projekt jest podzielony na dwie niezależne warstwy.

## `gcm_core`

Rdzeń nie importuje NVDA ani wxPython. Zawiera:

- modele kalendarzy, wydarzeń i danych nowego wydarzenia;
- walidację dat i godzin;
- logowanie OAuth i przechowywanie tokenu;
- ustawienia użytkownika;
- pobieranie kalendarzy oraz wydarzeń;
- budowanie danych wysyłanych do Google;
- tworzenie wydarzeń przez Calendar API;
- zapisywanie szczegółów błędów.

Docelowo ten sam rdzeń może zostać użyty zarówno przez aplikację desktopową,
jak i dodatek NVDA.

## `gcm_desktop`

Warstwa wxPython odpowiada za:

- główne okno;
- listę dni i listę wydarzeń;
- formularz tworzenia wydarzenia;
- wybór kalendarzy;
- okna szczegółów, wyszukiwania i potwierdzeń;
- fokus, skróty klawiaturowe i komunikaty dla użytkownika;
- uruchamianie operacji sieciowych poza wątkiem interfejsu.

Interfejs przekazuje do rdzenia obiekt `EventDraft`. Rdzeń waliduje go ponownie,
buduje zgodny z Google obiekt wydarzenia i wykonuje zapis. Dzięki temu reguły
zapisu nie są uzależnione od wxPython.

## Dane użytkownika

Aplikacja przechowuje własne pliki w `%APPDATA%\GCM by Piotrek` i nie zmienia
plików dodatku NVDA. Przy pierwszym uruchomieniu może jedynie skopiować zgodne
pliki z dodatku, pozostawiając oryginały bez zmian.


## Etap 0.4.0 — edycja

- Formularz dodawania i edycji korzysta ze wspólnej implementacji.
- `CalendarEvent.to_draft()` przekształca dane Google na wartości formularza.
- `build_event_patch_body()` zawiera tylko pola obsługiwane przez GCM i pozwala
  wyczyścić lokalizację lub opis.
- `CalendarGateway.update_event()` używa `events.patch`, zachowując pozostałe
  właściwości wydarzenia.
- Wydarzenie pozostaje w swoim kalendarzu.
- Instancja wydarzenia cyklicznego jest edytowana osobno.
- Specjalne typy wydarzeń są na razie blokowane.


## Etap 0.5.0 — usuwanie

`CalendarGateway.delete_event()` przyjmuje konkretny obiekt
`CalendarEvent`. Dla wystąpienia cyklicznego przekazuje do Google
identyfikator instancji, a nie `recurring_event_id`, dlatego usuwa tylko
zaznaczony termin.

Interfejs nie udostępnia jeszcze operacji usunięcia całej serii.
`sendUpdates` ma wartość `all` tylko wtedy, gdy wydarzenie ma uczestników
innych niż sam właściciel; w pozostałych przypadkach ma wartość `none`.

Po usunięciu dane są pobierane ponownie z Google, a fokus wraca do listy
wydarzeń wybranego dnia.


## Etap 0.6.0 — zakres usuwania cyklu

Model `CalendarEvent` przechowuje `originalStartTime` zwrócone przez Google.
Jest ono potrzebne do określenia miejsca wystąpienia w serii również po
przesunięciu pojedynczego terminu.

`delete_recurring_series()` usuwa identyfikator nadrzędny
`recurringEventId`.

`delete_recurring_from()` pobiera wydarzenie nadrzędne, usuwa z RRULE
dotychczasowe `COUNT` albo `UNTIL` i ustawia nowe `UNTIL` bezpośrednio przed
wybranym wystąpieniem. Elementy takie jak `EXDATE` są zachowywane.

Dla pierwszego wystąpienia skrócenie RRULE przed DTSTART byłoby
nieprawidłowe, dlatego metoda usuwa wtedy całe wydarzenie nadrzędne.


## Etap 0.7.0 — wyszukiwanie zakresowe

`SearchCriteria` przechowuje tekst, datę początkową i datę końcową podawaną
włącznie. Warstwa rdzenia przelicza koniec na datę wyłączną wymaganą przez
`events.list`.

`CalendarGateway.search_events()` pobiera wydarzenia dla całego przedziału,
a następnie filtruje je przez `EventCollection.search()`. Dzięki temu zachowane
jest jednakowe wyszukiwanie po tytule, opisie, lokalizacji i nazwie kalendarza.

Interfejs wykonuje operację w istniejącym wątku roboczym. Wynik wybrany poza
aktualnym miesiącem nie jest wstawiany sztucznie do bieżącej kolekcji: aplikacja
przechodzi do jego miesiąca, pobiera dane ponownie z Google i dopiero wtedy
ustawia fokus według identyfikatora wydarzenia.
