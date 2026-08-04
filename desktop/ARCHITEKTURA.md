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


## Etap 0.8.0 — pomoc i klawisze dostępu

Główne przyciski używają standardowych etykiet wxWidgets z ampersandem,
który oznacza mnemoniczną literę uruchamianą z klawiszem Alt.

`ExplicitNameAccessible.GetKeyboardShortcut()` przekazuje ten sam klawisz
dostępu przez Microsoft Active Accessibility. Pełny skrót aplikacji, taki
jak `Ctrl+N`, pozostaje w opisie i w oknie pomocy.

Klawisz dostępu i skrót aplikacji są celowo rozdzielone:

- `Alt+litera` aktywuje konkretny przycisk zgodnie ze standardem Windows;
- `Ctrl+litera`, `F1`, `F5` lub `Delete` wykonują polecenie bezpośrednio.

Pomoc jest zwykłym modalnym oknem z wielowierszowym polem tekstowym tylko do
odczytu, dzięki czemu jej treść można czytać strzałkami, zaznaczać i kopiować.


## Etap 0.9.0 — podstawowa cykliczność

`RecurrenceSettings` opisuje zamknięty zestaw prostych trybów: brak cyklu,
codziennie, co tydzień, co miesiąc, co 3 miesiące, co 6 miesięcy i co rok.
Generator zapisuje je jako RRULE. Odstępy kwartalny i półroczny używają
`FREQ=MONTHLY` wraz z `INTERVAL=3` albo `INTERVAL=6`.

Data końca cyklu jest zapisywana przez `UNTIL`. Dla wydarzeń całodniowych jest
to wartość datowa. Dla wydarzeń godzinowych koniec wskazanego dnia w strefie
kalendarza jest przeliczany na UTC. Zależność `tzdata` zapewnia bazę stref IANA
na Windowsie.

Parser reguł przyjmuje tylko jedno RRULE i zamknięty zestaw składników. Akceptuje
nieszkodliwe `WKST` oraz proste `BYDAY`, `BYMONTHDAY` i `BYMONTH`, jeśli zgadzają
się z datą rozpoczęcia. Odrzuca `COUNT`, nietypowe `INTERVAL`, kilka dni tygodnia,
dodatkowe linie oraz inne rozszerzenia. Dzięki temu edycja całej serii nie może
przypadkowo uprościć cyklu utworzonego poza GCM.

Edycja wystąpienia używa jego własnego identyfikatora i nie przesyła pola
`recurrence`. Edycja całej prostej serii pobiera wydarzenie nadrzędne przez
`recurringEventId`, zachowuje nieobsługiwane pola zasobu i zastępuje start, end
oraz RRULE. Zwykłe wydarzenie może zostać zamienione w prosty cykl.


## Etap 0.10.0 — przekazanie zaawansowanej obsługi do Google

`CalendarEvent` przechowuje bezpieczny `html_link` do internetowego interfejsu
wydarzenia oraz opcjonalny `meeting_url` i nazwę rozwiązania konferencyjnego.

Link spotkania jest wybierany w kolejności:

1. bezpośredni `hangoutLink`;
2. punkt wejścia `conferenceData.entryPoints` typu `video`;
3. internetowy punkt typu `more` jako strona zapasowa.

Punkty `phone` i `sip` nie są otwierane w przeglądarce. Wszystkie adresy są
akceptowane tylko wtedy, gdy są bezwzględnymi adresami HTTP albo HTTPS.

Aplikacja wyłącznie odczytuje istniejące dane konferencji. Nie generuje Meet,
nie modyfikuje `conferenceData` i nie rozszerza zakresów OAuth. Otwieranie
wydarzenia w Google stanowi świadomą granicę między prostą obsługą w GCM a
zaawansowaną edycją w oficjalnym interfejsie.


## Etap 0.11.0 — internacjonalizacja i wspólne ustawienia

Warstwa `gcm_core.i18n` przechowuje stabilne polskie komunikaty źródłowe i
kontrolowane tłumaczenia angielskie. `tr()` zwraca tekst aktywnego języka, a
`localized()` służy tylko do krótkich elementów wymagających innej litery
mnemonicznej w każdym języku. Aplikacja nie wykonuje tłumaczeń sieciowych.

Ustawienie języka ma wartości `auto`, `pl` i `en`. Tryb `auto` odczytuje język
interfejsu Windows; dla polskiego wybiera polski, a dla pozostałych angielski.
Ręczny wybór ma pierwszeństwo i zaczyna działać po ponownym uruchomieniu.

`AppSettings` przechowuje razem język oraz identyfikatory wybranych kalendarzy.
Brak pola `language` w starszym `settings.json` jest automatycznie migrowany do
`auto`. Główne okno ma jeden przycisk Ustawienia zamiast osobnego przycisku
wyboru kalendarzy. `Ctrl+,` i zachowany `Ctrl+K` otwierają ten sam dialog.

Daty wejściowe są niezależne od tłumaczenia: parser akceptuje `DD.MM.RRRR` oraz
ISO `RRRR-MM-DD`. Nazwy dni, miesięcy, liczebniki, szczegóły wydarzeń i
komunikaty błędów są formatowane przez aktywną warstwę językową.
