# Plan testów PT Calendar Manager 0.3.0

## Bezpieczny pierwszy test

1. Uruchom aplikację i poczekaj na pobranie wydarzeń.
2. Zaznacz dzień, w którym możesz utworzyć wydarzenie testowe.
3. Naciśnij `Ctrl+N`.
4. Wpisz tytuł `Test GCM 0.3.0`.
5. Wybierz kalendarz, w którym łatwo znajdziesz i ewentualnie usuniesz test.
6. Ustaw godzinę rozpoczęcia i zakończenia.
7. Wybierz `Utwórz wydarzenie`.
8. Sprawdź podsumowanie i dopiero wtedy potwierdź przyciskiem Tak.
9. Po komunikacie sukcesu sprawdź, czy fokus trafił na nowe wydarzenie.
10. Sprawdź wydarzenie w oficjalnym Kalendarzu Google.

## Test dostępności formularza

Sprawdź z NVDA, JAWS-em i Narratorem kolejno:

- Tytuł wydarzenia;
- Kalendarz docelowy;
- Data rozpoczęcia;
- Wydarzenie całodniowe;
- Godzina rozpoczęcia;
- Data zakończenia włącznie;
- Godzina zakończenia;
- Lokalizacja;
- Opis wydarzenia;
- Utwórz wydarzenie;
- Anuluj.

Po zaznaczeniu `Wydarzenie całodniowe` pola godzin powinny stać się nieaktywne.

## Test walidacji

Sprawdź kolejno:

- pusty tytuł;
- nieprawidłową datę;
- datę zakończenia wcześniejszą od rozpoczęcia;
- godzinę zakończenia wcześniejszą od rozpoczęcia tego samego dnia;
- wydarzenie godzinowe przechodzące przez północ;
- jednodniowe wydarzenie całodniowe;
- wielodniowe wydarzenie całodniowe.

## Ważne

Wersja 0.3.0 naprawdę zapisuje wydarzenia w Google. Edycja i usuwanie nie są
jeszcze dostępne w tej aplikacji.
