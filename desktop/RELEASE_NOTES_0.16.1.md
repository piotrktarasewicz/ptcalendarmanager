# PT Calendar Manager 0.16.1

Wersja 0.16.1 naprawia układ dokumentów w wydaniu Windows.

- instalator poprawnie otwiera listę skrótów na ekranie końcowym;
- skróty Dokumentacja i Licencja wskazują istniejące pliki;
- wersja przenośna ma publiczny katalog `docs` obok pliku EXE;
- pełna licencja i informacje o komponentach zewnętrznych znajdują się obok EXE;
- zachowano ten sam AppId, więc 0.16.1 aktualizuje instalację 0.16.0.

Przyczyną błędu był układ PyInstallera 6: dane zostały umieszczone w `_internal`, podczas gdy instalator odwoływał się do katalogu głównego programu.
