# Plan testów PT Calendar Manager 0.15.4

## Cel

Sprawdzenie, czy NVDA, JAWS i Narrator prawidłowo rozróżniają stan zaznaczenia elementów listy kalendarzy.

## Przygotowanie

Przed uruchomieniem pozostaw zaznaczone tylko:

- Familijne;
- Święta w Polsce.

Kalendarz główny powinien pozostać niezaznaczony.

## Test w każdym czytniku ekranu

1. Uruchom aplikację.
2. Otwórz Ustawienia.
3. Naciśnij Tab, aby przejść z wyboru języka na listę kalendarzy.
4. Sprawdź odczyt kalendarza Familijne. Powinien być ogłoszony jako zaznaczony.
5. Strzałkami przejdź na Święta w Polsce. Powinien być ogłoszony jako zaznaczony.
6. Przejdź na kalendarz główny. Powinien być ogłoszony jako niezaznaczony.
7. Naciśnij Spację na kalendarzu głównym. Czytnik powinien od razu ogłosić zmianę na zaznaczony.
8. Naciśnij Spację ponownie. Czytnik powinien ogłosić zmianę na niezaznaczony.
9. Zapisz ustawienia, zamknij je i otwórz ponownie.
10. Potwierdź, że zapisane stany są zgodne z dokonanym wyborem.

## Oczekiwany model klawiatury

- Tab wchodzi na jedną listę kalendarzy;
- strzałki zmieniają bieżący kalendarz;
- Spacja zaznacza albo odznacza;
- Tab wychodzi z listy do przycisków okna;
- lista nie dodaje nowych przystanków Tabulatora.

## Kontrola wizualna

- okno ma taki sam rozmiar jak w 0.15.3;
- pozostaje grupa „Wybór kalendarzy”;
- nad listą pozostaje jednowierszowa instrukcja;
- nie ma dodatkowego pola tekstowego ani widocznych dopisków „zaznaczony/niezaznaczony”.
