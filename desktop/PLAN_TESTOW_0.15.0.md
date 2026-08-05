# Plan testów PT Calendar Manager 0.15.0

Test należy wykonać osobno z NVDA, JAWS-em i Narratorem, po polsku oraz po angielsku.

## 1. Pierwsze uruchomienie i fokus

1. Uruchom `uruchom_pt_calendar_manager.bat`.
2. Fokus powinien trafić bezpośrednio na listę dni miesiąca.
3. Naciśnij Tab. Fokus powinien przejść na listę wydarzeń.
4. Naciśnij Tab ponownie. Fokus powinien wrócić na listę dni.
5. Sprawdź także `Shift+Tab`; przy dwóch listach fokus powinien pozostać w tym samym prostym cyklu.

## 2. Pasek menu

1. Naciśnij lewy Alt.
2. Czytnik powinien ogłosić pasek menu i pierwsze menu.
3. Strzałkami w lewo i w prawo sprawdź menu:
   - Kalendarz / Calendar;
   - Wydarzenie / Event;
   - Konto / Account;
   - Ustawienia / Settings;
   - Pomoc / Help.
4. Strzałkami w dół przejrzyj wszystkie polecenia.
5. Sprawdź, czy obok nazw odczytywane są przypisane skróty.
6. Sprawdź standardowe litery dostępu menu w obu językach.

## 3. Menu Kalendarz

Sprawdź kolejno:

- Poprzedni miesiąc;
- Dzisiaj;
- Następny miesiąc;
- Przejdź do daty;
- Wyszukaj;
- Dodaj wydarzenie;
- Odśwież.

Każde polecenie powinno działać tak samo jak w 0.14.0. Dotychczasowe skróty muszą pozostać aktywne.

## 4. Menu Wydarzenie

Bez wydarzenia polecenia wymagające zaznaczenia powinny być nieaktywne. Po zaznaczeniu wydarzenia sprawdź:

- Pokaż szczegóły;
- Edytuj;
- Usuń;
- Otwórz w Google;
- Link spotkania.

„Otwórz w Google” i „Link spotkania” powinny być aktywne tylko wtedy, gdy zaznaczone wydarzenie zawiera odpowiednie dane.

## 5. Menu Konto

1. Bez aktywnego logowania pozycja powinna nazywać się „Zaloguj do Google”.
2. Po zalogowaniu powinna zmienić nazwę na „Wyloguj z Google”.
3. Sprawdź `Ctrl+L` w obu stanach.
4. Sprawdź, czy prawa część paska stanu podaje stan konta.

## 6. Ustawienia i Pomoc

1. Ustawienia powinny zawierać tylko język i wybór kalendarzy.
2. Zmiana języka i restart powinny działać jak w 0.14.0.
3. „O programie” powinno znajdować się w menu Pomoc, nie w Ustawieniach.
4. Sprawdź Politykę prywatności i Informacje prawne.
5. `F1` powinien otwierać pomoc.

## 7. Menu kontekstowe listy dni

1. Ustaw fokus na liście dni.
2. Naciśnij `Shift+F10` albo klawisz aplikacji.
3. Sprawdź polecenia:
   - Dodaj wydarzenie;
   - Dzisiaj;
   - Przejdź do daty;
   - Wyszukaj;
   - Odśwież.
4. Po zamknięciu menu fokus powinien pozostać na liście dni.

## 8. Menu kontekstowe listy wydarzeń

1. Ustaw fokus na liście wydarzeń.
2. Naciśnij `Shift+F10` albo klawisz aplikacji.
3. Sprawdź polecenia:
   - Pokaż szczegóły;
   - Edytuj;
   - Usuń;
   - Otwórz w Google;
   - Link spotkania.
4. Sprawdź stany aktywne i nieaktywne.
5. Po zamknięciu menu fokus powinien pozostać na liście wydarzeń.

## 9. Skróty regresyjne

Potwierdź działanie:

- `Ctrl+L`;
- `Ctrl+,`;
- `Ctrl+K`;
- `Ctrl+N`;
- `Ctrl+E`;
- `Delete`;
- `Ctrl+F`;
- `Ctrl+G`;
- `Ctrl+D`;
- `F5`;
- `F1`;
- `Ctrl+Shift+G`;
- `Ctrl+J`;
- `Alt+Strzałka w lewo`;
- `Alt+Strzałka w prawo`.

## 10. Operacja sieciowa w toku

Podczas pobierania danych:

- polecenia zmieniające kalendarz lub wydarzenia powinny być nieaktywne;
- Ustawienia, Pomoc i O programie powinny pozostać dostępne;
- lista dni i lista wydarzeń nie powinny przestać reagować;
- po zakończeniu lub przekroczeniu czasu polecenia powinny zostać ponownie uaktywnione.

## 11. Wygląd

Test wzrokowy należy wykonać w:

- jasnym motywie Windows;
- ciemnym motywie, o ile kontrolki wxPython przejmują go z systemu;
- trybie wysokiego kontrastu.

Sprawdź:

- czy nagłówek miesiąca jest czytelny i wyraźny;
- czy nazwy paneli mają subtelny akcent, ale pozostają czytelne;
- czy tła i teksty są nadal kolorami systemowymi;
- czy żadna informacja nie jest przekazywana wyłącznie kolorem;
- czy nie pojawiły się obcięte teksty przy powiększeniu systemowym.

## 12. Pełna regresja

Sprawdź odczyt, wyszukiwanie, dodawanie, edycję, cykliczność, usuwanie, ustawienia, zmianę języka, otwieranie w Google, link spotkania, DPAPI i ponowne uruchomienie aplikacji.
