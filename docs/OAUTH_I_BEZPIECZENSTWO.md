# OAuth i bezpieczeństwo

## Model autoryzacji

Oba produkty korzystają z OAuth 2.0 i Google Calendar API. Użytkownik wyraża zgodę w przeglądarce. Projekt nie przechowuje hasła do konta Google.

Zakresy dodatku NVDA są ograniczone do:

- `https://www.googleapis.com/auth/calendar.events`;
- `https://www.googleapis.com/auth/calendar.calendarlist.readonly`;
- `https://www.googleapis.com/auth/calendar.settings.readonly`.

## Konfiguracja klienta Desktop app

Konfiguracja klienta OAuth typu Desktop app jest elementem publicznej aplikacji, ale musi być oddzielona od publicznej historii źródeł.

- Oficjalny instalator i wersja przenośna PT Calendar Manager 0.16.3 zawierają konfigurację potrzebną do pierwszego logowania.
- Oficjalna paczka dodatku NVDA również może zawierać konfigurację wymaganą do działania.
- Repozytorium źródłowe zawiera wyłącznie przykład `client_secret.example.json`.
- Źródłowy ZIP aplikacji nie zawiera konfiguracji wdrożeniowej.

## Tokeny użytkownika

Token powstaje dopiero po udzieleniu zgody przez użytkownika.

- PT Calendar Manager zapisuje zaszyfrowany przez Windows DPAPI plik `token.dat` w `%APPDATA%\PT Calendar Manager`.
- Dodatek NVDA zapisuje swoje dane w katalogu `googleCalendarManager` konfiguracji użytkownika NVDA.

Tokenów nie wolno dodawać do repozytorium, paczek źródłowych, logów testowych ani zgłoszeń błędów.

## Logi i raporty błędów

Przed dołączeniem raportu należy usunąć:

- adresy e-mail;
- identyfikatory kalendarzy i wydarzeń;
- nazwy kalendarzy;
- tytuły, opisy i lokalizacje wydarzeń;
- tokeny i dane OAuth;
- prywatne ścieżki użytkownika, jeśli nie są potrzebne do diagnozy.

## Stan weryfikacji Google

Projekt nie przeszedł jeszcze publicznej weryfikacji Google OAuth. Do czasu jej zakończenia logowanie może działać wyłącznie dla kont wpisanych na listę użytkowników testowych. Weryfikacja OAuth jest osobnym etapem przed oznaczeniem aplikacji jako 1.0 RC.
