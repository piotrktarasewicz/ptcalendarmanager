# GCM by Piotrek 0.7.0 — wyszukiwanie w zakresie dat

GCM by Piotrek jest dostępnym klientem Kalendarza Google dla Windows,
testowanym z NVDA, JAWS-em i Narratorem.

Wersja 0.7.0 zastępuje wyszukiwanie ograniczone do wyświetlanego miesiąca
wyszukiwaniem w samodzielnie określonym zakresie dat.

## Formularz wyszukiwania

Po użyciu przycisku `Wyszukaj` albo skrótu `Ctrl+F` aplikacja pyta o:

- szukany tekst;
- datę początkową w formacie `DD.MM.RRRR`;
- datę końcową w formacie `DD.MM.RRRR`.

Obie daty należą do zakresu. Domyślnie formularz proponuje okres od dzisiaj
do dnia przypadającego 365 dni później.

Pola mają jawne nazwy dostępności przekazywane przez `wx.Accessible`.

## Zakres danych

Wyszukiwanie pobiera wydarzenia bezpośrednio z Google ze wszystkich kalendarzy
zaznaczonych w ustawieniach aplikacji. Nie jest ograniczone do wydarzeń
aktualnie widocznego miesiąca.

Tekst jest wyszukiwany w:

- tytule;
- opisie;
- lokalizacji;
- nazwie kalendarza.

Operacja działa w wątku roboczym i nie blokuje głównego okna.

## Wyniki

Okno wyników podaje liczbę znalezionych wydarzeń oraz użyty zakres dat.
Po wybraniu wydarzenia GCM:

1. przechodzi do miesiąca wydarzenia;
2. pobiera ten miesiąc ponownie z Google;
3. wybiera właściwy dzień;
4. ustawia fokus na znalezionym wydarzeniu.

## Uruchomienie

Rozpakuj archiwum do nowego katalogu i uruchom `uruchom_gcm.bat`.

Token i ustawienia pozostają w `%APPDATA%\\GCM by Piotrek`.
