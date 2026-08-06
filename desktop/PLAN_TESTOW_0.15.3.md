# Plan testów PT Calendar Manager 0.15.3

## Cel

Sprawdzenie dostępności pojedynczej listy kontrolnej kalendarzy w NVDA, JAWS-ie i Narratorze.

## Ustawienia

1. Otwórz menu Ustawienia i wybierz Ustawienia.
2. Sprawdź, czy fokus początkowy znajduje się na polu wyboru języka.
3. Naciśnij Tab jeden raz.
4. Czytnik powinien przejść bezpośrednio do listy kalendarzy. Nie powinien zatrzymać się na elemencie odczytywanym jako „panel, okienko”.
5. Przy wejściu na listę powinien zostać odczytany jej cel: kalendarze do wyświetlania oraz instrukcja zaznaczania.
6. Użyj strzałek w górę i w dół. Czytnik powinien odczytywać nazwy kolejnych kalendarzy.
7. Naciśnij Spację. Stan bieżącego kalendarza powinien się zmienić i zostać odczytany.
8. Naciśnij Tab. Fokus powinien przejść do przycisku Zapisz.
9. Zapisz ustawienia, ponownie otwórz okno i potwierdź zachowanie zaznaczeń.

## Kontrola wizualna

- grupa ma nazwę „Wybór kalendarzy”;
- instrukcja znajduje się nad listą;
- lista pokazuje checkboxy i przewija się przy większej liczbie kalendarzy;
- okno nie jest wyższe niż w wersji 0.15.2 i nie zawiera dodatkowego pola tekstowego.

## Regresja

- zmiana języka nadal wymaga restartu;
- nie można zapisać ustawień bez zaznaczenia przynajmniej jednego kalendarza;
- główne okno, menu, wyszukiwanie, dodawanie, edycja i usuwanie wydarzeń działają bez zmian.
