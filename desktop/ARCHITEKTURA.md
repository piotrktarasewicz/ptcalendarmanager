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
