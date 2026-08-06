# Historia migracji projektu

## Google Calendar Reader i Google Calendar Manager

Pierwszy program działał jako dodatek NVDA pod nazwą Google Calendar Reader. Nazwa techniczna została następnie zmieniona z `googleCalendarReader` na `googleCalendarManager`, a nazwa widoczna dla użytkownika na Google Calendar Manager. Mechanizm migracji zachowywał możliwość odczytania danych dawnej wersji.

Repozytorium `piotrktarasewicz/nvda-google-calendar-reader` zostało przemianowane na `piotrktarasewicz/nvda-google-calendar-manager`. Oba adresy wskazywały więc na tę samą historię. Odfiltrowana historia dodatku zaczyna się od commitu źródłowego 1.0.2 i zawiera 29 commitów, tagi 1.0.2–1.0.4 oraz dwie zachowane gałęzie robocze.

## Samodzielna aplikacja

Samodzielna aplikacja wxPython powstała początkowo jako prototyp i była rozwijana pod nazwą GCM by Piotrek. Od wersji 0.13.0 jej oficjalna nazwa brzmi PT Calendar Manager. Migracja danych przenosi ustawienia z `%APPDATA%\GCM by Piotrek` do `%APPDATA%\PT Calendar Manager`, nie niszcząc istniejących danych.

Historia samodzielnej aplikacji została odtworzona z 28 zachowanych paczek źródłowych:

- prototypy 0.1.0 i 0.1.1;
- GCM by Piotrek 0.2.0–0.12.0;
- PT Calendar Manager 0.13.0–0.16.3.

Każda paczka tworzy osobny commit i tag `desktop-v...`. Commity są oznaczone jako import zachowanego obrazu wersji, aby nie udawać nieistniejącej wcześniej historii Git.

## Dawne strony projektu

Z repozytorium `ptprojects` odfiltrowano wyłącznie commity dotyczące:

- bieżącej strony Google Calendar Manager;
- przekierowania ze starej strony Google Calendar Reader.

Nie przeniesiono pozostałej historii strony ani projektów WOMAI.

## Tymczasowe buildy Windows

Wydania 0.16.1–0.16.3 były tymczasowo budowane przez prywatne repozytorium `womaiowe-terminy`. Kod WOMAI nie należy do projektu kalendarza i nie został przeniesiony. Identyfikatory technicznych commitów budowania zostały zachowane w osobnym dokumencie, a właściwy kod każdej wersji znajduje się w historii `desktop/`.
