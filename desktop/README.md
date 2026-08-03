# GCM by Piotrek 0.8.0 — pomoc i standardowe klawisze dostępu

GCM by Piotrek jest dostępnym klientem Kalendarza Google dla Windows,
testowanym z NVDA, JAWS-em i Narratorem.

## Nowości w wersji 0.8.0

- przycisk `Pomoc i skróty`;
- otwieranie pomocy klawiszem `F1`;
- standardowe klawisze dostępu Windows `Alt+litera`;
- programowe przekazywanie klawisza dostępu czytnikom ekranu;
- podpowiedzi zawierające dodatkowe skróty aplikacji;
- litery dostępu również na przyciskach formularzy i okien wynikowych.

## Dwa rodzaje skrótów

Klawisz dostępu, na przykład `Alt+N`, aktywuje konkretny przycisk zgodnie
ze standardem Windows. Litera jest oznaczona w etykiecie przycisku znakiem
`&` i jest dodatkowo udostępniana przez `wx.Accessible`.

Skrót aplikacji, na przykład `Ctrl+N`, wykonuje polecenie bezpośrednio,
niezależnie od miejsca fokusu.

## Najważniejsze skróty aplikacji

- `Ctrl+L` — zaloguj albo wyloguj;
- `Ctrl+K` — wybierz kalendarze;
- `F1` — pomoc i skróty;
- `Alt+Strzałka w lewo` i `Alt+Strzałka w prawo` — zmiana miesiąca;
- `Ctrl+D` — dzisiaj;
- `Ctrl+G` — przejdź do daty;
- `Ctrl+F` — wyszukiwanie;
- `Ctrl+N` — dodaj wydarzenie;
- `F5` — odśwież;
- `Ctrl+E` — edytuj;
- `Delete` — usuń.

Pełna lista liter `Alt+litera` znajduje się w oknie pomocy.

## Uruchomienie

Rozpakuj archiwum do nowego katalogu i uruchom `uruchom_gcm.bat`.

Token i ustawienia pozostają w `%APPDATA%\GCM by Piotrek`.
