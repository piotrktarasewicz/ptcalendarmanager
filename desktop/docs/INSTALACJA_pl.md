# Instalacja i aktualizacja PT Calendar Manager

## Instalator

1. Uruchom plik instalatora.
2. Wybierz język.
3. Zapoznaj się z informacją o licencji, prywatności i niezależności od Google.
4. Zmień katalog tylko wtedy, gdy jest to potrzebne.
5. Opcjonalnie wybierz skrót na pulpicie.
6. Wybierz „Instaluj”.
7. Na ostatniej stronie można otworzyć listę skrótów i uruchomić program.

Instalator nie wymaga praw administratora. Program jest instalowany dla
bieżącego konta Windows.

## Aktualizacja

Nowszy instalator można uruchomić bez wcześniejszego odinstalowania aplikacji.
Zachowany AppId powoduje aktualizację tego samego programu. Token Google i
ustawienia w `%APPDATA%\PT Calendar Manager` nie są usuwane.

## Odinstalowanie

Odinstalator pyta, czy usunąć dane użytkownika. Domyślna odpowiedź „Nie”
zachowuje logowanie i ustawienia na potrzeby późniejszej instalacji.

Odpowiedź „Tak” usuwa cały katalog `%APPDATA%\PT Calendar Manager`, w tym
token, konfigurację OAuth, ustawienia i raport ostatniego błędu.

## Wersja przenośna

Rozpakuj całe archiwum do zwykłego katalogu i uruchom
`PT Calendar Manager.exe`. Nazwa „przenośna” dotyczy braku instalatora;
dane użytkownika nadal są przechowywane w `%APPDATA%\PT Calendar Manager`,
a token DPAPI pozostaje związany z kontem Windows.
