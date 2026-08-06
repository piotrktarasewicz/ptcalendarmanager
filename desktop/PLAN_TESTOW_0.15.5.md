# Plan testów PT Calendar Manager 0.15.5

## Cel

Sprawdzenie natywnej listy kalendarzy Windows z polami wyboru w NVDA, JAWS-ie i Narratorze.

## Przygotowanie

1. Uruchom `uruchom_pt_calendar_manager.bat`.
2. Otwórz Ustawienia.
3. Upewnij się, że co najmniej jeden kalendarz jest zaznaczony, a jeden niezaznaczony.

## Test każdego czytnika

1. Fokus początkowo znajduje się na wyborze języka.
2. Naciśnij Tab. Fokus powinien przejść bezpośrednio na pierwszy kalendarz, nie na panel.
3. Czytnik powinien odczytać nazwę listy, pierwszy kalendarz oraz jego rzeczywisty stan pola wyboru.
4. Poruszaj się strzałkami w górę i w dół. Każdy kalendarz powinien być odczytywany.
5. Sprawdź, czy zaznaczone i niezaznaczone kalendarze są rozróżniane.
6. Naciśnij Spację. Stan bieżącego kalendarza powinien się zmienić i zostać oznajmiony.
7. Zapisz ustawienia, otwórz je ponownie i sprawdź zachowanie stanów.

## Szczególnie ważny przypadek

- kalendarz główny: niezaznaczony;
- Familijne: zaznaczone;
- Święta w Polsce: zaznaczone.

Po wejściu na listę fokus powinien być na kalendarzu głównym, ale jego stan nie może być mylony z zaznaczeniem checkboxa.
