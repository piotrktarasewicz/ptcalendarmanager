# PT Calendar Manager

Repozytorium zawiera dwa aktualne, dostępne narzędzia do obsługi Kalendarza Google:

- **PT Calendar Manager 0.16.3** — samodzielną aplikację dla Windows;
- **Google Calendar Manager 1.0.4** — dodatek dla czytnika ekranu NVDA.

Oba programy są przeznaczone do obsługi klawiaturą i współpracy z czytnikami ekranu.

## Pobieranie

### PT Calendar Manager 0.16.3

- [Strona wydania 0.16.3](https://github.com/piotrktarasewicz/ptcalendarmanager/releases/tag/desktop-v0.16.3)
- [Instalator dla Windows](https://github.com/piotrktarasewicz/ptcalendarmanager/releases/download/desktop-v0.16.3/PT-Calendar-Manager-0.16.3-Setup.exe)
- [Wersja przenośna](https://github.com/piotrktarasewicz/ptcalendarmanager/releases/download/desktop-v0.16.3/pt-calendar-manager-0.16.3-portable.zip)

### Dodatek Google Calendar Manager 1.0.4 dla NVDA

- [Strona wydania 1.0.4](https://github.com/piotrktarasewicz/ptcalendarmanager/releases/tag/v1.0.4)
- [Paczka dodatku NVDA](https://github.com/piotrktarasewicz/ptcalendarmanager/releases/download/v1.0.4/googleCalendarManager-1.0.4.nvda-addon)

## Układ repozytorium

- `desktop/` — źródła PT Calendar Manager 0.16.3;
- `nvda-addon/` — źródła dodatku Google Calendar Manager 1.0.4;
- `docs/` — kontekst projektu, zasady rozwoju, wydawania oraz bezpieczeństwa OAuth;
- `AGENTS.md` — trwałe instrukcje dla narzędzi wspomagających rozwój;
- `.github/workflows/tests.yml` — automatyczna kontrola źródeł, testów i prywatnych plików.

Historia kodu pozostaje w gałęzi `main`, ponieważ zajmuje niewiele miejsca i jest przydatna przy diagnozowaniu regresji. Duże instalatory i paczki nie są przechowywane w historii Git — aktualne pliki dystrybucyjne znajdują się w GitHub Releases.

## Rozwój

Przed rozpoczęciem zmian przeczytaj:

- [Kontekst projektu](docs/KONTEKST_PROJEKTU.md);
- [Rozwój i wydania](docs/ROZWOJ_I_WYDANIA.md);
- [OAuth i bezpieczeństwo](docs/OAUTH_I_BEZPIECZENSTWO.md);
- [Zasady bezpieczeństwa repozytorium](SECURITY.md).

Instrukcje właściwe dla obu produktów znajdują się także w plikach:

- [desktop/README.md](desktop/README.md);
- [nvda-addon/README_pl.md](nvda-addon/README_pl.md);
- [nvda-addon/BUILD.md](nvda-addon/BUILD.md).

## Status Google OAuth

Aplikacja nie przeszła jeszcze publicznej weryfikacji Google. Do czasu jej zakończenia logowanie może być dostępne wyłącznie dla kont dodanych jako użytkownicy testowi projektu OAuth. Wersja 1.0 RC aplikacji samodzielnej jest planowana dopiero po zakończeniu tego etapu.

## Prywatność

Repozytorium nie zawiera tokenów użytkowników, plików `.env`, `token.json`, `token.dat` ani rzeczywistego luźnego pliku `client_secret.json`.

Oficjalny instalator i pakiet przenośny PT Calendar Manager 0.16.3 zawierają konfigurację publicznego klienta OAuth typu Desktop app, niezbędną do pierwszego logowania. Token konkretnego użytkownika powstaje dopiero po jego zgodzie i jest szyfrowany lokalnie przez Windows DPAPI.

## Licencja

Kod źródłowy jest udostępniany na warunkach GNU General Public License w wersji 3 lub nowszej (`GPL-3.0-or-later`).
