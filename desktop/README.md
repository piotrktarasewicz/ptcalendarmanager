# GCM by Piotrek 0.3.1 — poprawione etykiety formularza

GCM by Piotrek to dostępny klient Kalendarza Google dla Windows.
Interfejs jest rozwijany i testowany z NVDA, JAWS-em i Narratorem.

## Poprawka w wersji 0.3.1

W formularzu dodawania wydarzenia widoczne napisy nie były programowo
powiązane z polami. Czytniki odczytywały więc jedynie „pole edycyjne”.

Wersja 0.3.1 nadaje każdej kontrolce jednoznaczną nazwę przez
`wx.Accessible`, a `SetName()` pozostawia jako drugą warstwę
zabezpieczenia.

Poprawka obejmuje:

- Tytuł wydarzenia;
- Kalendarz docelowy;
- Datę rozpoczęcia;
- Wydarzenie całodniowe;
- Godzinę rozpoczęcia;
- Datę zakończenia włącznie;
- Godzinę zakończenia;
- Lokalizację;
- Opis wydarzenia.

Funkcje odczytu i dodawania wydarzeń pozostają bez zmian.

## Uruchomienie

Rozpakuj wersję 0.3.1 do nowego katalogu i uruchom `uruchom_gcm.bat`.

Token i ustawienia pozostają w:

`%APPDATA%\GCM by Piotrek`

Dlatego aplikacja powinna zachować logowanie i wybór kalendarzy.

## Najważniejszy test

Naciśnij `Ctrl+N` i przejdź Tabulatorem po wszystkich kontrolkach.
Czytnik powinien podawać nazwę, rolę i aktualną wartość każdego pola.
