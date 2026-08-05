# Plan testów PT Calendar Manager 0.14.0

Wersja obejmuje przygotowanie dokumentacji, okno „O programie” i szyfrowanie tokenu Google przez Windows DPAPI.

Testy wykonaj przede wszystkim z NVDA, JAWS-em i Narratorem. Migrację tokenu wystarczy sprawdzić raz na koncie Windows, na którym działała wersja 0.13.0.

## 1. Aktualizacja z wersji 0.13.0

1. Zamknij starszą wersję.
2. Nie usuwaj `%APPDATA%\PT Calendar Manager`.
3. Rozpakuj 0.14.0 do nowego katalogu.
4. Uruchom `uruchom_pt_calendar_manager.bat`.
5. Sprawdź, czy aplikacja nadal rozpoznaje logowanie i pobiera kalendarze.
6. Zamknij i uruchom aplikację ponownie. Logowanie powinno pozostać aktywne.

Po udanej migracji w `%APPDATA%\PT Calendar Manager` powinien istnieć `token.dat`. Dotychczasowy `token.json` w tym samym katalogu powinien zostać usunięty dopiero po poprawnym zapisaniu `token.dat`.

Starszy katalog `%APPDATA%\GCM by Piotrek`, jeśli istnieje, nie powinien zostać usunięty ani zmieniony.

## 2. Działanie po zaszyfrowaniu tokenu

Sprawdź po kolei:

- odświeżenie kalendarza klawiszem `F5`;
- przejście między miesiącami;
- dodanie testowego wydarzenia;
- edycję wydarzenia;
- usunięcie wydarzenia;
- zamknięcie i ponowne uruchomienie aplikacji.

Wszystkie operacje powinny działać tak jak w 0.13.0.

## 3. Wylogowanie

1. Wyloguj się z Google w aplikacji.
2. Zamknij PT Calendar Manager.
3. Sprawdź, czy w katalogu danych nie ma `token.dat` ani `token.json`.
4. Uruchom aplikację ponownie. Powinna informować o braku połączenia z Google, ale Ustawienia i pomoc muszą działać.
5. Zaloguj się ponownie i sprawdź, czy powstał nowy `token.dat`.

## 4. O programie

1. Otwórz Ustawienia skrótem `Ctrl+,`.
2. Przejdź do przycisku „O programie”.
3. Czytnik powinien podać krótką nazwę, rolę przycisku i literę dostępu, bez długiego opisu.
4. Otwórz okno.
5. Fokus powinien trafić do pola tekstowego tylko do odczytu.
6. Sprawdź odczyt strzałkami, zaznaczanie i kopiowanie tekstu.
7. Sprawdź przyciski:
   - Polityka prywatności;
   - Informacje prawne;
   - Zamknij.

## 5. Polityka prywatności i informacje prawne

Oba dokumenty powinny otwierać się w polu tekstowym tylko do odczytu. Sprawdź:

- czy fokus trafia do treści;
- czy tekst można czytać strzałkami;
- czy `Ctrl+A` i `Ctrl+C` pozwalają skopiować treść;
- czy po zamknięciu wraca się do okna „O programie”;
- czy po zamknięciu „O programie” wraca się do Ustawień.

## 6. Język angielski

1. Zmień język na English i uruchom aplikację ponownie.
2. Otwórz Settings, a następnie About.
3. Sprawdź angielskie tytuły i przyciski:
   - About;
   - Privacy policy;
   - Legal information;
   - Close.
4. Sprawdź, czy treści dokumentów są całkowicie angielskie.
5. Wróć do języka polskiego.

## 7. Regresja dostępności

W każdym z trzech czytników przejdź Tabulatorem przez główne okno i Ustawienia. Wersja 0.14.0 nie powinna przywrócić długich opisów przycisków usuniętych w 0.12.0.

Szczególnie sprawdź, czy „O programie” nie powoduje blokowania lub ukrywania Ustawień oraz czy kolejne okna modalne zawsze pozostają na pierwszym planie.

## 8. Test nowego komputera lub konta Windows

Na komputerze albo koncie Windows bez danych PT Calendar Manager:

- Ustawienia, O programie, polityka prywatności i informacje prawne powinny działać bez Internetu i bez logowania;
- po pierwszym logowaniu powinien powstać `token.dat`, a nie `token.json`;
- aplikacja powinna działać po ponownym uruchomieniu.

Zaszyfrowanego `token.dat` nie należy przenosić między różnymi kontami Windows. Na drugim komputerze lub koncie należy wykonać nowe logowanie Google.
