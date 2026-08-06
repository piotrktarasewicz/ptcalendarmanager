# PT Calendar Manager 0.16.3

Wersja 0.16.3 upraszcza pierwsze logowanie na nowym komputerze.

Najważniejsze zmiany:

- oficjalny instalator i pakiet przenośny zawierają konfigurację klienta OAuth typu Desktop app;
- użytkownik czystego komputera nie musi ręcznie wskazywać pliku `client_secret.json`;
- proces wydania sprawdza strukturę konfiguracji OAuth przed zbudowaniem programu i po skopiowaniu jej do pakietu;
- pakiet źródłowy nadal nie zawiera konfiguracji wdrożeniowej ani tokenów użytkowników;
- token konta Google nadal powstaje dopiero po zgodzie użytkownika i jest szyfrowany lokalnie przez Windows DPAPI.

Pozostałe funkcje i dostępny układ pomocy z wersji 0.16.2 pozostają bez zmian.
