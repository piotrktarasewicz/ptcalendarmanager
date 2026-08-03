# GCM by Piotrek 0.5.0 — pełny podstawowy przepływ wydarzeń

GCM by Piotrek to dostępny klient Kalendarza Google dla Windows,
rozwijany i praktycznie testowany z NVDA, JAWS-em i Narratorem.

Wersja 0.5.0 domyka podstawową obsługę wydarzeń:

- odczyt;
- dodawanie;
- edycję;
- usuwanie.

## Usuwanie wydarzeń

Zaznacz wydarzenie i użyj przycisku `Usuń` albo klawisza `Delete`.

Przed wykonaniem operacji aplikacja pokazuje:

- tytuł;
- kalendarz;
- termin;
- lokalizację i opis;
- ostrzeżenie, że operacji nie można cofnąć w GCM.

Przycisk `Nie` jest domyślnym wyborem.

## Wydarzenia cykliczne

Wersja 0.5.0 usuwa wyłącznie zaznaczone wystąpienie wydarzenia cyklicznego.
Nie oferuje usuwania całej serii, dzięki czemu nie można wybrać tej
operacji przypadkowo.

## Uczestnicy

Jeżeli wydarzenie ma rzeczywistych uczestników, aplikacja ostrzega o tym
przed usunięciem, a Google otrzymuje polecenie wysłania im informacji
o anulowaniu.

## Specjalne typy wydarzeń

Usunięcie jest dostępne dla zwykłych i specjalnych typów wydarzeń, o ile:

- kalendarz pozwala na zapis;
- wydarzenie ma identyfikator Google;
- Google nie oznaczył go jako zablokowane.

Typ specjalny jest jawnie podany w oknie potwierdzenia.

## Po prawidłowym usunięciu

Aplikacja:

1. pokazuje potwierdzenie;
2. ponownie pobiera wydarzenia z Google;
3. pozostaje na tym samym dniu;
4. ustawia fokus na liście wydarzeń tego dnia.

## Uruchomienie

Rozpakuj archiwum do nowego katalogu i uruchom `uruchom_gcm.bat`.

Logowanie i ustawienia są przechowywane w:

`%APPDATA%\GCM by Piotrek`

dlatego powinny pozostać zachowane między wersjami.
