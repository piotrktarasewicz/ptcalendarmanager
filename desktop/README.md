# GCM by Piotrek 0.10.0 — otwieranie wydarzeń i spotkań

GCM by Piotrek jest dostępnym klientem Kalendarza Google dla Windows,
testowanym z NVDA, JAWS-em i Narratorem. Aplikacja służy do szybkiej,
doraźnej obsługi kalendarza, a nie do zastępowania pełnego interfejsu Google.

## Nowości w wersji 0.10.0

- przycisk `Otwórz w Google` dla zaznaczonego wydarzenia;
- skrót `Ctrl+Shift+G` do otwierania wydarzenia w internetowym Kalendarzu Google;
- wykrywanie istniejących linków spotkań zapisanych w danych konferencji;
- okno `Link spotkania` pozwalające otworzyć albo skopiować adres;
- skrót `Ctrl+J` do okna linku spotkania;
- obsługa właściwego punktu wejścia typu wideo oraz internetowej strony
  konferencji, bez otwierania numerów telefonicznych i adresów SIP;
- kontrola, aby aplikacja otwierała wyłącznie bezwzględne adresy HTTP lub HTTPS.

GCM nie tworzy nowych spotkań Google Meet i nie zmienia istniejących danych
konferencji. Funkcje są aktywne tylko wtedy, gdy odpowiedni link znajduje się
w wydarzeniu pobranym z Google.

## Klawisze dostępu nowych przycisków

- `Alt+W` — Otwórz w Google;
- `Alt+I` — Link spotkania.

## Skróty aplikacji

- `Ctrl+Shift+G` — otwórz zaznaczone wydarzenie w Kalendarzu Google;
- `Ctrl+J` — otwórz okno istniejącego linku spotkania.

Pozostałe skróty znajdują się w pomocy otwieranej klawiszem `F1`.

## Uruchomienie

Rozpakuj archiwum do nowego katalogu i uruchom `uruchom_gcm.bat`.

Token i ustawienia pozostają w `%APPDATA%\GCM by Piotrek`.
