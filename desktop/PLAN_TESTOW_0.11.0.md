# Plan testów PT Calendar Manager 0.11.0

Testy wykonaj osobno z NVDA, JAWS-em 2025 i Narratorem. Najważniejszy jest
pełny przebieg po polsku i po angielsku, a nie tylko sprawdzenie głównego okna.

## 1. Aktualizacja ze starszej wersji

1. Uruchom 0.11.0 przy istniejącym `%APPDATA%\PT Calendar Manager`.
2. Sprawdź, czy logowanie Google i dotychczas wybrane kalendarze pozostały.
3. Otwórz Ustawienia. Starszy plik bez pola języka powinien zostać potraktowany
   jako `Automatycznie`.

## 2. Główne okno i ustawienia

1. Sprawdź, czy w głównym oknie nie ma już osobnego przycisku `Wybierz kalendarze`.
2. Powinny być: logowanie, Ustawienia i Pomoc.
3. Otwórz Ustawienia przyciskiem, `Ctrl+,` oraz `Ctrl+K`.
4. Sprawdź wybór języka oraz listę kalendarzy w jednym oknie.
5. Anulowanie nie może zmienić języka ani kalendarzy.
6. Zapis wyboru kalendarzy powinien odświeżyć wydarzenia.

## 3. Język automatyczny

Na polskim Windowsie ustaw `Automatycznie`, uruchom GCM ponownie i sprawdź
język polski. Na Windowsie z innym językiem interfejsu tryb automatyczny
powinien użyć angielskiego.

## 4. Ręczny wybór języka

1. Wybierz `English`, zapisz ustawienia i zamknij aplikację.
2. Uruchom ją ponownie. Cały interfejs powinien być angielski.
3. Wybierz `Polish`, uruchom ponownie i sprawdź język polski.
4. Sama zmiana wyboru przed ponownym uruchomieniem nie powinna częściowo
   przełączać otwartego interfejsu.

## 5. Pełny przebieg po angielsku

Sprawdź kolejno:

- główne okno, dni, miesiące i liczbę wydarzeń;
- logowanie i wylogowanie;
- Ustawienia i wybór kalendarzy;
- przejście do daty;
- wyszukiwanie oraz wyniki;
- dodawanie wydarzenia godzinowego i całodniowego;
- wszystkie podstawowe rodzaje cykliczności;
- edycję wydarzenia i całego prostego cyklu;
- usuwanie zwykłe oraz trzy zakresy usuwania cyklu;
- szczegóły wydarzenia;
- otwarcie wydarzenia w Google;
- otwarcie i kopiowanie linku spotkania;
- pomoc pod `F1`;
- komunikaty błędów i potwierdzenia.

Nie powinny pojawić się polskie etykiety, poza treścią wydarzeń, nazwami
kalendarzy i innymi danymi pochodzącymi od użytkownika albo z Google.

## 6. Pełny przebieg po polsku

Powtórz powyższy przebieg. Nie powinny pojawić się angielskie etykiety poza
nazwą wyboru języka `English`, treścią użytkownika i nazwami własnymi Google.

## 7. Daty

W obu językach sprawdź wpisywanie:

- `04.08.2026`;
- `2026-08-04`.

Oba formaty powinny działać w przejściu do daty, wyszukiwaniu, dodawaniu,
edycji i dacie zakończenia cyklu. Nieprawidłowe daty muszą dawać komunikat
w aktywnym języku.

## 8. Dostępność

Dla każdego czytnika sprawdź:

- nazwy kontrolek i okien w aktywnym języku;
- odczyt list dni i wydarzeń;
- kolejność Tabulatora w Ustawieniach;
- pola wyboru kalendarzy;
- listę wyboru języka;
- powrót fokusu po zapisaniu lub anulowaniu;
- brak podwójnego odczytu nazw lub skrótów.

Nadmiernie rozbudowane opisy przy przyciskach pozostają do osobnego etapu
końcowego dopracowania.

## 9. Regresja

Potwierdź, że język i przeniesienie wyboru kalendarzy do Ustawień nie zmieniły
logiki pobierania, tworzenia, edycji, usuwania, cykliczności, wyszukiwania,
otwierania w Google ani obsługi linków spotkań.
