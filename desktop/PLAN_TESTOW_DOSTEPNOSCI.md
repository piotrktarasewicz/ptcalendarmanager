# Plan testów dostępności — prototyp wxPython

Wykonaj ten sam test osobno z NVDA, JAWS-em i Narratorem. Warto całkowicie
wyłączyć pozostałe czytniki, aby nie przechwytywały komunikatów.

## 1. Uruchomienie

Sprawdź:

- czy odczytywany jest tytuł „GCM by Piotrek — prototyp dostępności”;
- na którym elemencie znajduje się początkowy fokus;
- czy można przejść po całym oknie Tabulatorem i Shift+Tabulatorem;
- czy żaden element nie wymaga myszy.

## 2. Górne przyciski

Powinny być odczytywane kolejno:

1. Poprzedni miesiąc,
2. Dzisiaj,
3. Następny miesiąc,
4. Przejdź do daty,
5. Wyszukaj,
6. Dodaj wydarzenie,
7. Odśwież.

Sprawdź także skróty:

- Alt+Strzałka w lewo,
- Alt+Strzałka w prawo,
- Ctrl+D,
- Ctrl+G,
- Ctrl+F,
- Ctrl+N,
- F5.

## 3. Lista dni

Sprawdź:

- czy kontrolka jest nazywana „Dni miesiąca”;
- czy czytnik odczytuje zaznaczony element;
- czy strzałki zmieniają dzień;
- czy każdy element zawiera dzień tygodnia, datę i liczbę wydarzeń;
- czy klawisz Enter przenosi fokus do listy wydarzeń.

Przykładowy element:

„niedziela, 2 sierpnia 2026, 2 wydarzenia”.

## 4. Lista wydarzeń

Sprawdź:

- czy nazwa listy zawiera wybraną datę i liczbę wydarzeń;
- czy wydarzenia całodniowe i godzinowe są rozróżniane;
- czy odczytywana jest nazwa kalendarza;
- czy Enter otwiera szczegóły;
- czy przy braku wydarzeń lista nadal jest zrozumiała.

## 5. Przyciski wydarzenia

Sprawdź kolejno:

- Pokaż szczegóły,
- Edytuj,
- Usuń.

Przyciski Edytuj, Usuń i Pokaż szczegóły powinny być nieaktywne, gdy dzień nie
ma wydarzeń.

## 6. Formularz dodawania

Naciśnij Ctrl+N i sprawdź:

- tytuł okna,
- pole „Tytuł”,
- pole „Data”,
- pole wyboru „Wydarzenie całodniowe”,
- pola godziny rozpoczęcia i zakończenia,
- listę „Kalendarz”,
- pole „Lokalizacja”,
- wielowierszowe pole „Opis”,
- przyciski Zapisz i Anuluj.

Po zaznaczeniu wydarzenia całodniowego pola godzin powinny stać się nieaktywne.

## 7. Edycja i usuwanie

- zaznacz wydarzenie;
- użyj Ctrl+E;
- zmień tytuł i zapisz;
- sprawdź, czy fokus wrócił na zmienione wydarzenie;
- naciśnij Delete;
- sprawdź komunikat potwierdzający;
- anuluj, a następnie wykonaj usunięcie.

## 8. Wyszukiwanie

Naciśnij Ctrl+F, wpisz część tytułu i sprawdź:

- czy pole ma właściwą nazwę;
- czy wynik jest przedstawiony jako zwykła lista;
- czy można przejść do znalezionego wydarzenia;
- czy brak wyników jest jasno komunikowany.

## 9. Przejście do daty

Naciśnij Ctrl+G:

- wpisz poprawną datę w formacie DD.MM.RRRR;
- sprawdź zmianę miesiąca i zaznaczenia;
- sprawdź komunikat po wpisaniu błędnej daty.

## 10. Informacje, które warto zanotować

Dla każdego czytnika zapisz:

- czego dokładnie nie odczytał;
- czy podał rolę kontrolki;
- czy podał zaznaczenie i pozycję na liście;
- gdzie ginął fokus;
- czy pojawiały się podwójne komunikaty;
- czy coś było odczytywane tylko po ręcznym użyciu kursora czytnika;
- czy aplikacja pozostawała w pełni obsługiwalna klawiaturą.
