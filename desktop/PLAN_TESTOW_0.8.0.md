# Plan testów PT Calendar Manager 0.8.0

Test wykonaj osobno z NVDA, JAWS-em 2025 i Narratorem.

## 1. Odczyt głównych przycisków

Przejdź Tabulatorem po wszystkich przyciskach. Sprawdź, czy czytnik
podaje nazwę przycisku oraz klawisz dostępu `Alt+litera`.

Oczekiwane litery:

- Zaloguj lub Wyloguj z Google — `Alt+L`;
- Wybierz kalendarze — `Alt+K`;
- Pomoc i skróty — `Alt+H`;
- Poprzedni miesiąc — `Alt+P`;
- Dzisiaj — `Alt+D`;
- Następny miesiąc — `Alt+M`;
- Przejdź do daty — `Alt+G`;
- Wyszukaj — `Alt+S`;
- Dodaj wydarzenie — `Alt+N`;
- Odśwież — `Alt+O`;
- Pokaż szczegóły — `Alt+Z`;
- Edytuj — `Alt+E`;
- Usuń — `Alt+U`.

Zwróć uwagę, czy nazwa lub skrót nie są odczytywane podwójnie.

## 2. Działanie liter dostępu

Uruchom każdy przycisk przez `Alt+litera`. Sprawdź szczególnie:

- `Alt+H` otwiera pomoc;
- `Alt+N` otwiera dodawanie;
- `Alt+S` otwiera wyszukiwanie;
- `Alt+Z` pokazuje szczegóły zaznaczonego wydarzenia;
- `Alt+U` otwiera bezpieczny przepływ usuwania.

## 3. Pomoc

1. Naciśnij `F1`.
2. Fokus powinien trafić do pola tekstowego tylko do odczytu.
3. Sprawdź nawigację strzałkami, zaznaczanie i kopiowanie tekstu.
4. Przejdź do przycisku `Zamknij`, który powinien mieć `Alt+Z`.
5. Zamknij pomoc i sprawdź powrót fokusu do listy dni.

## 4. Skróty aplikacji

Potwierdź, że nadal działają:

- `Ctrl+L`;
- `Ctrl+K`;
- `Ctrl+N`;
- `Ctrl+E`;
- `Delete`;
- `Ctrl+F`;
- `Ctrl+G`;
- `Ctrl+D`;
- `F5`;
- `Alt+Strzałka w lewo`;
- `Alt+Strzałka w prawo`.

Skrót aplikacji powinien wykonywać polecenie od razu, a nie tylko
przenosić fokus na przycisk.

## 5. Przyciski w oknach dialogowych

Sprawdź litery dostępu dla przycisków:

- Utwórz wydarzenie — `Alt+U`;
- Zapisz zmiany — `Alt+Z`;
- Anuluj — `Alt+A`;
- Wyszukaj — `Alt+S`;
- Przejdź do wydarzenia — `Alt+P`;
- Zamknij — `Alt+Z`.

## 6. Regresja

Sprawdź odczyt, dodawanie, edycję, usuwanie, wyszukiwanie i wybór
kalendarzy. Dodanie klawiszy dostępu nie powinno zmienić działania
dotychczasowych funkcji.
