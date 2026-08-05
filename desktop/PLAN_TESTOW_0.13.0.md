# Plan testów PT Calendar Manager 0.13.0

Testy wykonaj przynajmniej z NVDA, JAWS-em i Narratorem. Najważniejszy zakres tej wersji to zmiana nazwy i bezpieczna migracja danych.

## 1. Nazwa aplikacji

1. Uruchom `uruchom_pt_calendar_manager.bat`.
2. Sprawdź tytuł głównego okna: `PT Calendar Manager 0.13.0`.
3. Sprawdź nazwę głównego okna odczytywaną przez czytnik.
4. Otwórz pomoc klawiszem `F1` i sprawdź, czy używa nazwy `PT Calendar Manager`.
5. Sprawdź, czy w komunikatach logowania, błędach, edycji i usuwaniu nie pojawia się dawna nazwa robocza.

## 2. Migracja istniejącej konfiguracji

Na komputerze używanym wcześniej z wersją 0.12.0:

1. Potwierdź istnienie katalogu `%APPDATA%\GCM by Piotrek`.
2. Uruchom wersję 0.13.0.
3. Sprawdź, czy powstał katalog `%APPDATA%\PT Calendar Manager`.
4. Potwierdź skopiowanie `token.json`, `settings.json` i `client_secret.json`, jeżeli były dostępne.
5. Sprawdź, czy program zachował zalogowanie, wybrany język i wybrane kalendarze.
6. Potwierdź, że stary katalog i jego pliki nadal istnieją.

## 3. Ochrona nowych danych

1. Umieść różne wersje `settings.json` w starym i nowym katalogu danych.
2. Uruchom PT Calendar Manager.
3. Program powinien zachować plik z nowego katalogu i nie nadpisywać go starszym.

## 4. Czyste uruchomienie

1. Na komputerze bez obu katalogów danych uruchom program.
2. Powinien utworzyć `%APPDATA%\PT Calendar Manager`.
3. Ustawienia języka powinny działać bez logowania.
4. Logowanie powinno poprosić o `client_secret.json`, jeżeli pliku nie znaleziono.

## 5. Ponowne uruchomienie po zmianie języka

1. Zmień język w Ustawieniach.
2. Wybierz `Uruchom ponownie teraz`.
3. Sprawdź, czy nowa instancja nazywa się PT Calendar Manager i uruchamia się w wybranym języku.
4. Potwierdź zachowanie tokenu oraz kalendarzy po restarcie.

## 6. Informacja o niezależności

1. Otwórz pomoc `F1` w języku polskim i angielskim.
2. Sprawdź końcową informację, że aplikacja jest niezależna i nie jest produktem, projektem sponsorowanym ani zatwierdzonym przez Google.

## 7. Regresja funkcjonalna

Sprawdź kolejno:

- pobranie wydarzeń;
- dodanie wydarzenia jednorazowego;
- dodanie wydarzenia cyklicznego;
- edycję pojedynczego wydarzenia i cyklu;
- usuwanie;
- wyszukiwanie;
- otwieranie wydarzenia w Google;
- otwieranie i kopiowanie linku spotkania;
- działanie skrótów klawiaturowych;
- zwięzły odczyt przycisków.
