# Konfiguracja OAuth w wydaniu Windows

PT Calendar Manager używa klienta OAuth typu **Desktop app**.

Domyślnie skrypt budowania nie dołącza `client_secret.json`. Aby utworzyć build
wewnętrzny zawierający konkretną konfigurację wdrożeniową, umieść plik w
`release-secrets\\client_secret.json` i uruchom:

`tools\\build_release.ps1 -IncludeOAuthClient`

Katalog `release-secrets` nie trafia do repozytorium ani pakietu źródłowego.

Aplikacja desktopowa działa na urządzeniu użytkownika, dlatego nie może
skutecznie zachować identyfikatora ani sekretu klienta OAuth w poufności. Nie są
to zabezpieczenia danych użytkownika. Bezpieczeństwo opiera się na ograniczonych
zakresach, zgodzie użytkownika, weryfikacji projektu OAuth oraz szyfrowaniu
indywidualnego tokenu użytkownika przez Windows DPAPI.

Do publicznego wydania należy użyć klienta Desktop app należącego do projektu,
który przejdzie weryfikację Google. Osoba budująca własną wersję programu może
użyć własnego klienta OAuth.
