# Plan testów GCM by Piotrek 0.6.0

Test wykonaj osobno z NVDA, JAWS-em 2025 i Narratorem.

Przygotuj krótką serię testową, na przykład pięć codziennych wystąpień.

## 1. Okno zakresu

1. Zaznacz środkowe wystąpienie serii.
2. Naciśnij `Delete`.
3. Sprawdź trzy opcje:
   - Usuń tylko to wystąpienie;
   - Usuń to i wszystkie kolejne wystąpienia;
   - Usuń cały cykl.
4. Domyślnie powinna być zaznaczona pierwsza opcja.
5. Naciśnij Escape i sprawdź, czy nic nie zostało usunięte.

## 2. Tylko to wystąpienie

Wybierz pierwszą opcję i potwierdź. Powinien zniknąć tylko jeden termin.

## 3. To i kolejne

Na nowej serii zaznacz środkowe wystąpienie, wybierz drugą opcję
i potwierdź. Wcześniejsze terminy powinny pozostać, a zaznaczony
i wszystkie późniejsze powinny zniknąć.

## 4. To i kolejne od pierwszego terminu

Na nowej serii zaznacz pierwsze wystąpienie i wybierz drugą opcję.
Powinien zniknąć cały cykl, a komunikat powinien wyjaśnić przyczynę.

## 5. Cały cykl

Na kolejnej serii wybierz trzecią opcję. Po potwierdzeniu powinny zniknąć
wcześniejsze, zaznaczone i późniejsze wystąpienia.

## 6. Bezpieczeństwo

Dla każdego wariantu sprawdź:

- domyślną odpowiedź `Nie`;
- anulowanie klawiszem Escape;
- dokładny odczyt zakresu;
- komunikat po zakończeniu;
- fokus na liście wydarzeń;
- wynik w oficjalnym Kalendarzu Google.

## 7. Przesunięte wystąpienie

W oficjalnym Kalendarzu Google przesuń pojedynczy termin serii na inny
dzień. Następnie wybierz w GCM `Usuń to i wszystkie kolejne`.
Granica powinna zostać wyznaczona według pierwotnego terminu, nie według
dnia, na który wystąpienie przesunięto.
