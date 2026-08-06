# Bezpieczeństwo danych projektu

Do repozytorium nie wolno dodawać:

- tokenów dostępu lub odświeżania Google;
- plików `token.json` i `token.dat`;
- plików `.env`;
- prywatnych logów zawierających identyfikatory kalendarzy, wydarzeń lub ich treść;
- luźnego pliku `client_secret.json` używanego podczas lokalnego budowania.

Publiczne przykłady konfiguracji powinny używać wyłącznie fikcyjnych wartości. Oficjalne instalatory i paczki przenośne mogą zawierać konfigurację klienta OAuth typu Desktop wymaganą do działania wydania, ponieważ taki klient jest aplikacją publiczną i nie stanowi mechanizmu przechowywania tokenów użytkownika.

Tokeny użytkownika są danymi prywatnymi i nigdy nie mogą trafić do kodu źródłowego, artefaktów testowych ani zgłoszeń błędów.
