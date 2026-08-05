# Plan testów PT Calendar Manager 0.15.1

Test wykonaj osobno z NVDA, JAWS-em i Narratorem.

## 1. Instrukcja wyboru kalendarzy

1. Otwórz menu Ustawienia i wybierz Ustawienia.
2. Fokus początkowo powinien znajdować się na wyborze języka.
3. Naciśnij Tab.
4. Czytnik powinien odczytać informację: „Zaznacz kalendarze, których wydarzenia mają być pokazywane.”
5. Naciśnij Tab ponownie. Fokus powinien przejść do pierwszego pola wyboru kalendarza i czytnik powinien podać jego nazwę oraz stan zaznaczenia.
6. Przy przechodzeniu przez kolejne kalendarze instrukcja nie powinna być powtarzana.

## 2. Nawigacja wstecz

1. Przejdź do pierwszego pola wyboru kalendarza.
2. Naciśnij Shift+Tab.
3. Fokus powinien wrócić na instrukcję, która powinna zostać ponownie odczytana.
4. Kolejne Shift+Tab powinno przejść do wyboru języka.

## 3. Wygląd

Instrukcja powinna wyglądać jak zwykła informacja tekstowa, bez ciężkiego obramowania i bez zmiany kolorystyki systemowej.

## 4. Regresja

- zmień zaznaczenie kalendarzy i zapisz ustawienia;
- anuluj ustawienia i sprawdź, czy wybór nie został zmieniony;
- zmień język i sprawdź dialog ponownego uruchomienia;
- sprawdź główne menu, obie listy i menu kontekstowe.
