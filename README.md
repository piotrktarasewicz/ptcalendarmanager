# PT Calendar Manager

To repozytorium łączy pełną historię trzech kolejnych nazw i dwóch form programu:

- Google Calendar Reader — pierwotna nazwa dodatku NVDA;
- Google Calendar Manager — późniejsza nazwa dodatku NVDA;
- PT Calendar Manager — samodzielna aplikacja dla systemu Windows.

Aktualna wersja samodzielnej aplikacji to 0.16.3.

## Układ repozytorium

- `desktop/` — aktualne źródła PT Calendar Manager 0.16.3;
- `legacy/nvda-addon/` — ostatnie źródła dodatku NVDA Google Calendar Manager 1.0.4;
- `docs/` — opis migracji, historii i archiwum;
- gałąź `archive/all-project-files` — archiwalne paczki, instalatory, prototypy, logi robocze i plany testów;
- gałęzie `history/google-calendar-manager-site` i `history/google-calendar-reader-redirect` — odfiltrowana historia dawnych stron projektu;
- gałęzie `legacy/nvda-fix-event-editing-1.0.4` i `legacy/nvda-inline-custom-search-range` — zachowane gałęzie robocze dodatku NVDA.

## Historia wersji

Tagi `v1.0.2`, `v1.0.3` i `v1.0.4` dotyczą dodatku NVDA.

Tagi od `desktop-v0.1.0` do `desktop-v0.16.3` oznaczają odtworzone z zachowanych paczek źródłowych wersje aplikacji samodzielnej. Każda wersja ma osobny commit, dzięki czemu można porównywać rozwój projektu od prototypu wxPython.

## Uruchamianie i budowanie

Instrukcje aktualnej wersji znajdują się w `desktop/README.md`. Kompletne wydania Windows są przechowywane na gałęzi archiwalnej.

## Dane OAuth i prywatność

Prawdziwe tokeny użytkownika, pliki `.env`, `token.json`, `token.dat` i luźne pliki `client_secret.json` nie są przechowywane w historii źródeł. Repozytorium zawiera wyłącznie przykładową konfigurację dodatku NVDA oraz oficjalne paczki binarne przeznaczone do dystrybucji.

Prywatne identyfikatory wydarzeń, nazwy kalendarzy i treść wydarzeń zostały usunięte z kopii historycznych logów diagnostycznych.

## Licencja

Kod źródłowy jest udostępniany na warunkach GPL-3.0-or-later. Szczegóły i informacje o składnikach zewnętrznych znajdują się również w katalogach `desktop/` oraz `legacy/nvda-addon/`.
