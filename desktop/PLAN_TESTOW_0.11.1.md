# Plan testów GCM by Piotrek 0.11.1

Test wykonaj osobno z NVDA, JAWS-em 2025 i Narratorem.

## 1. Zmiana języka z polskiego na angielski

1. Otwórz Ustawienia.
2. Zmień język z polskiego na English i zapisz.
3. Powinno pojawić się okno „Ponowne uruchomienie GCM”.
4. Sprawdź odczyt komunikatu oraz przycisków „Uruchom ponownie teraz” i „Później”.
5. Przycisk ponownego uruchomienia powinien być domyślny.
6. Wybierz „Uruchom ponownie teraz”.
7. Bieżąca instancja powinna się zamknąć, a nowa uruchomić po angielsku.
8. Logowanie Google, token i wybór kalendarzy powinny pozostać zachowane.

## 2. Zmiana języka z angielskiego na polski

Powtórz test w przeciwną stronę. Okno pytania powinno być wyświetlone w języku aktualnie działającego interfejsu, a nowa instancja już w języku wybranym.

## 3. Przycisk „Później”

1. Zmień język i zapisz ustawienia.
2. Wybierz „Później”.
3. Aplikacja powinna pozostać otwarta w dotychczasowym języku.
4. Pasek stanu powinien poinformować, że zmiana nastąpi przy następnym uruchomieniu.
5. Zamknij GCM ręcznie i uruchom ponownie. Nowy język powinien zostać zastosowany.

## 4. Zmiana tylko kalendarzy

Zmień wybór kalendarzy bez zmieniania języka. Pytanie o ponowne uruchomienie nie powinno się pojawić. Lista wydarzeń powinna zostać odświeżona normalnie.

## 5. Zmiana preferencji bez zmiany widocznego języka

Na polskim Windowsie zmień „Automatycznie” na „Polski” albo odwrotnie. Jeżeli efektywny język pozostaje polski, restart nie powinien być proponowany. Analogicznie sprawdź „Automatycznie” i „English” na angielskim Windowsie, jeśli jest dostępny.

## 6. Obsługa klawiatury

- polski: `Alt+U` — Uruchom ponownie teraz, `Alt+P` — Później;
- angielski: `Alt+R` — Restart now, `Alt+L` — Later;
- Escape powinien działać jak „Później”;
- Enter powinien uruchomić domyślny przycisk ponownego uruchomienia.

## 7. Regresja

Sprawdź ustawienia, logowanie, odczyt wydarzeń, dodawanie, edycję, usuwanie, wyszukiwanie, cykliczność i linki wydarzeń w obu językach.
