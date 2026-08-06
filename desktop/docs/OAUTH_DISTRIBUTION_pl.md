# Konfiguracja OAuth w wydaniu Windows

PT Calendar Manager używa klienta OAuth typu **Desktop app**.

Oficjalny instalator i pakiet przenośny 0.16.3 zawierają konfigurację OAuth, aby
logowanie działało na czystym komputerze bez ręcznego wskazywania pliku. Podczas
budowania wydania umieść właściwy plik w
`release-secrets\\client_secret.json` i uruchom:

`tools\\build_release.ps1 -IncludeOAuthClient`

Skrypt sprawdza strukturę pliku przed budowaniem i po skopiowaniu do katalogu
programu. Katalog `release-secrets` nie trafia do repozytorium ani pakietu
źródłowego. Budowanie bez parametru `-IncludeOAuthClient` pozostaje możliwe dla
osób przygotowujących własny pakiet z własnym klientem OAuth.

Aplikacja desktopowa działa na urządzeniu użytkownika, dlatego nie może
skutecznie zachować identyfikatora ani sekretu klienta OAuth w poufności. Nie są
to zabezpieczenia danych użytkownika. Bezpieczeństwo opiera się na ograniczonych
zakresach, zgodzie użytkownika, weryfikacji projektu OAuth oraz szyfrowaniu
indywidualnego tokenu użytkownika przez Windows DPAPI.

Do publicznego wydania należy użyć klienta Desktop app należącego do projektu,
który przejdzie weryfikację Google. Osoba budująca własną wersję programu może
użyć własnego klienta OAuth.
