# Instrukcje pracy nad PT Calendar Manager

## Źródło prawdy

Przed zmianą kodu przeczytaj:

1. `README.md`;
2. `docs/KONTEKST_PROJEKTU.md`;
3. `docs/ROZWOJ_I_WYDANIA.md`;
4. `docs/OAUTH_I_BEZPIECZENSTWO.md`;
5. `SECURITY.md`.

Aktualne produkty to wyłącznie:

- PT Calendar Manager 0.16.3 w katalogu `desktop/`;
- Google Calendar Manager 1.0.4 dla NVDA w katalogu `nvda-addon/`.

Wersje obu produktów są niezależne. Nie zmieniaj numeru wersji bez wyraźnego polecenia.

## Dostępność

Dostępność jest wymaganiem podstawowym, a nie dodatkiem. Każda zmiana interfejsu musi zachować:

- pełną obsługę klawiaturą;
- logiczną kolejność fokusu;
- jednoznaczne etykiety kontrolek;
- prawidłowe komunikaty dla NVDA, JAWS-a i Narratora;
- semantyczne nagłówki w pomocy;
- brak informacji przekazywanej wyłącznie kolorem lub położeniem wizualnym.

W datach nazwa dnia tygodnia pozostaje przed datą. Polecenie instalatora otwierające dokumentację ma prowadzić do pomocy zawierającej skróty, a nie do osobnego pliku tekstowego ze skrótami.

## Bezpieczeństwo

Nigdy nie dodawaj do źródeł:

- `client_secret.json` z rzeczywistą konfiguracją;
- `token.json`, `token.dat` ani innych tokenów Google;
- plików `.env`;
- prywatnych logów zawierających treść wydarzeń, nazwy kalendarzy, adresy e-mail lub identyfikatory API.

Konfiguracja klienta OAuth typu Desktop app może występować wyłącznie w oficjalnych artefaktach wydania. Publiczny kod zawiera tylko przykład konfiguracji.

## Kontrola zmian

Po zmianach co najmniej:

1. skompiluj składnię źródeł aplikacji i dodatku;
2. uruchom testy z `desktop/tests`;
3. sprawdź brak prywatnych plików;
4. zaktualizuj dokumentację i informacje o wydaniu, jeśli zachowanie użytkowe się zmieniło.

Nie umieszczaj instalatorów, paczek portable ani plików `.nvda-addon` w historii Git. Publikuj je jako zasoby GitHub Releases.
