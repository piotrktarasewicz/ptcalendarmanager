# Plan testów GCM by Piotrek 0.10.0

Test wykonaj osobno z NVDA, JAWS-em 2025 i Narratorem.

## 1. Wydarzenie bez linków

1. Zaznacz zwykłe wydarzenie bez spotkania online.
2. Przycisk `Otwórz w Google` powinien być dostępny, jeżeli Google zwróciło
   stronę wydarzenia.
3. Przycisk `Link spotkania` powinien być niedostępny.
4. Zmiana zaznaczenia na inne wydarzenie powinna od razu aktualizować stan
   obu przycisków.

## 2. Otwieranie wydarzenia w Google

1. Zaznacz wydarzenie i użyj przycisku `Otwórz w Google`.
2. Powinna otworzyć się domyślna przeglądarka bez ponownego wyszukiwania
   wydarzenia.
3. Powtórz test skrótem `Ctrl+Shift+G` i klawiszem dostępu `Alt+W`.
4. Sprawdź zwykłe wydarzenie oraz pojedyncze wystąpienie cyklu.

## 3. Istniejący link Google Meet

1. Poza GCM utwórz wydarzenie zawierające Google Meet.
2. Odśwież dane w GCM i zaznacz wydarzenie.
3. Przycisk `Link spotkania` powinien stać się dostępny.
4. Otwórz go klawiszem `Ctrl+J` oraz `Alt+I`.
5. Fokus powinien trafić na przycisk `Otwórz link`.
6. Sprawdź otwarcie spotkania w przeglądarce.
7. Otwórz okno ponownie i wybierz `Kopiuj link`.
8. Wklej schowek do Notatnika i porównaj adres.

## 4. Inny dostawca spotkania

Jeżeli Google Calendar przechowuje konferencję z internetowym punktem wejścia
wideo innego dostawcy, GCM powinien udostępnić ten adres w taki sam sposób.
Numer telefonu i adres SIP nie powinny być traktowane jako link przeglądarkowy.

## 5. Szczegóły wydarzenia

Dla wydarzenia ze spotkaniem szczegóły powinny podać nazwę rozwiązania i pełny
adres. Dla wydarzenia bez spotkania powinien pojawić się komunikat o braku
linku. Szczegóły powinny również informować, czy dostępna jest strona wydarzenia
w Kalendarzu Google.

## 6. Regresja

Sprawdź odczyt, wyszukiwanie, dodawanie, edycję, usuwanie i podstawową
cykliczność. Nowe funkcje nie mogą zmieniać danych wydarzenia ani konferencji.
