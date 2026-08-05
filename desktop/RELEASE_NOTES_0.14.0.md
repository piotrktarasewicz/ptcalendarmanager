# PT Calendar Manager 0.14.0 — informacje o wersji

## Najważniejsze zmiany

- dodano dostępne okno „O programie” w Ustawieniach;
- dodano wbudowaną politykę prywatności po polsku i po angielsku;
- dodano wbudowane informacje prawne i jasne wskazanie niezależności od Google;
- przygotowano pełną dokumentację użytkownika w obu językach;
- token Google jest zapisywany jako `token.dat` i szyfrowany przez Windows DPAPI;
- istniejący `token.json` jest automatycznie migrowany i usuwany z bieżącego katalogu dopiero po udanym szyfrowaniu;
- wylogowanie usuwa zarówno nowy, jak i starszy format tokenu;
- przygotowano wymagania dla przyszłego instalatora.

## Zakres funkcjonalny

Funkcje kalendarza nie zostały zmienione. Wersja 0.14.0 skupia się na bezpieczeństwie danych lokalnych, przejrzystości i przygotowaniu aplikacji do wydania.

## Ważny test praktyczny

Mechanizm DPAPI musi zostać potwierdzony na Windowsie przez aktualizację z 0.13.0, ponowne uruchomienie oraz wykonanie co najmniej jednej operacji odczytu i zapisu w Kalendarzu Google.
