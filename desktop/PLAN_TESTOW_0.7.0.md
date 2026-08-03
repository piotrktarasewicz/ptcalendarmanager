# Plan testów GCM by Piotrek 0.7.0

Test wykonaj osobno z NVDA, JAWS-em 2025 i Narratorem.

## 1. Dostępność formularza

1. Naciśnij `Ctrl+F`.
2. Przechodź Tabulatorem.
3. Sprawdź odczyt pól:
   - Szukany tekst;
   - Data początkowa wyszukiwania, DD.MM.RRRR;
   - Data końcowa wyszukiwania, DD.MM.RRRR;
   - Wyszukaj;
   - Anuluj.
4. Sprawdź, czy pola dat zawierają wartości domyślne.

## 2. Walidacja

Sprawdź kolejno:

- pusty szukany tekst;
- błędną datę, na przykład `31.02.2026`;
- datę końcową wcześniejszą od początkowej.

W każdym przypadku aplikacja powinna wyjaśnić błąd i pozostawić otwarty formularz.

## 3. Wyszukiwanie w kilku miesiącach

1. Utwórz dwa wydarzenia o podobnym tytule w różnych miesiącach.
2. Podaj zakres obejmujący oba miesiące.
3. Sprawdź, czy oba wydarzenia pojawiają się w wynikach.
4. Sprawdź, czy okno wyników odczytuje użyty zakres.

## 4. Przejście do wyniku spoza bieżącego miesiąca

1. Wybierz wynik z innego miesiąca.
2. Użyj `Przejdź do wydarzenia`.
3. GCM powinien pobrać właściwy miesiąc i ustawić fokus na wydarzeniu.

## 5. Pola przeszukiwane

Przygotuj wydarzenia, które można odnaleźć osobno po:

- fragmencie tytułu;
- fragmencie opisu;
- fragmencie lokalizacji;
- nazwie kalendarza.

## 6. Kalendarze

Sprawdź, czy wyniki pochodzą wyłącznie z kalendarzy zaznaczonych w oknie
`Wybierz kalendarze`.

## 7. Anulowanie i brak wyników

- Escape w formularzu nie powinien rozpoczynać wyszukiwania.
- Escape w wynikach powinien wrócić do głównego okna.
- Brak wyników powinien zostać odczytany jako `brak wydarzeń`.
