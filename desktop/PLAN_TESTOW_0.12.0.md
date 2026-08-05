# Plan testów GCM by Piotrek 0.12.0

Test wykonaj osobno z NVDA, JAWS-em i Narratorem.

## 1. Zwięzły odczyt głównych przycisków

Przejdź Tabulatorem przez całe główne okno. Każdy przycisk powinien podawać
krótką nazwę, rolę i literę dostępu Windows. Nie powinien automatycznie czytać
długiego opisu działania ani skrótu aplikacji.

Przykładowo przycisk dodawania powinien zostać odczytany w rodzaju:

`Dodaj wydarzenie, N, przycisk`

Dopuszczalna jest inna kolejność słów zależna od czytnika. Nie powinny jednak
pojawiać się komunikaty „Otwiera formularz dodawania wydarzenia” ani
„Skrót aplikacji: Ctrl+N”.

Sprawdź szczególnie: Zaloguj, Ustawienia, Pomoc, Poprzedni miesiąc, Dzisiaj,
Następny miesiąc, Przejdź do daty, Wyszukaj, Dodaj wydarzenie, Odśwież,
Pokaż szczegóły, Edytuj, Usuń, Otwórz w Google i Link spotkania.

## 2. Klawisze dostępu

Potwierdź działanie wszystkich liter `Alt+litera`. Litera powinna być nadal
odczytywana przez czytnik i aktywować właściwy przycisk.

## 3. Skróty aplikacji

Potwierdź, że nadal działają skróty opisane pod `F1`, w szczególności:

- `Ctrl+N`, `Ctrl+E`, `Ctrl+F`, `Ctrl+G`;
- `Ctrl+,` i `Ctrl+K`;
- `Ctrl+L`, `Ctrl+D`, `Ctrl+J`, `Ctrl+Shift+G`;
- `F1`, `F5`, `Delete`;
- `Alt+Strzałka w lewo` i `Alt+Strzałka w prawo`.

## 4. Okna dialogowe

Sprawdź przyciski w dodawaniu, edycji, wyszukiwaniu, Ustawieniach, linku
spotkania, pomocy i pytaniu o ponowne uruchomienie. Odczyt przycisków powinien
być równie krótki. Opisy pól tekstowych mogą pozostać, gdy wyjaśniają format
lub przeznaczenie pola.

## 5. Regresja

W obu językach sprawdź logowanie, Ustawienia, zmianę języka, wybór kalendarzy,
odczyt, wyszukiwanie, dodawanie, edycję, usuwanie, cykliczność, otwieranie w
Google oraz link spotkania. Funkcjonalność powinna być identyczna jak w 0.11.2.
