# PT Calendar Manager — wymagania instalatora

Dokument roboczy dla etapu po zatwierdzeniu wersji 0.15.5.

## Pakiety

- instalator EXE dla Windows;
- wersja przenośna ZIP;
- wbudowany interpreter Python i wszystkie zależności;
- brak wymogu instalowania Pythona przez użytkownika.

## Identyfikacja

- nazwa produktu: PT Calendar Manager;
- opis: Dostępna aplikacja do obsługi Kalendarza Google;
- angielski opis: Accessible desktop application for Google Calendar;
- plik wykonywalny: `PT Calendar Manager.exe`;
- katalog programu i wpis odinstalowania pod oficjalną nazwą.

## Strony instalatora

1. wybór języka instalatora;
2. opis aplikacji i informacja, że nie jest to oficjalny produkt Google;
3. polityka prywatności i informacje o lokalnym szyfrowaniu tokenu;
4. wybór katalogu;
5. opcjonalny skrót na pulpicie;
6. instalacja;
7. ekran końcowy z polami:
   - „Zapoznaj się ze skrótami aplikacji”;
   - „Uruchom aplikację”.

Informacja o niezależności produktu jest komunikatem informacyjnym, a nie polem wymuszającym akceptację fikcyjnego regulaminu.

## Aktualizacja i odinstalowanie

- aktualizacja nie usuwa `%APPDATA%\PT Calendar Manager`;
- odinstalator pyta osobno, czy usunąć token, ustawienia i raport błędu;
- domyślnie dane użytkownika są zachowywane;
- usunięcie danych musi obejmować `token.dat`, ewentualny starszy `token.json`, `settings.json`, `client_secret.json` i `last_error.txt`;
- instalator nie może usuwać starszych katalogów bez osobnej, świadomej decyzji użytkownika.

## Dostępność

- wszystkie strony dostępne klawiaturą;
- standardowe przyciski i pola wyboru Windows;
- poprawne etykiety dla NVDA, JAWS-a i Narratora;
- brak automatycznego przechodzenia fokusu bez komunikatu;
- ekran końcowy zaczyna fokus na przycisku Zakończ albo pierwszym polu wyboru, zależnie od wyników testów.
