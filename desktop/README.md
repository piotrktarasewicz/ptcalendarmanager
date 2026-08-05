# PT Calendar Manager 0.13.0

**Dostępna aplikacja do obsługi Kalendarza Google**  
**Accessible desktop application for Google Calendar**

PT Calendar Manager jest samodzielną aplikacją dla systemu Windows, przeznaczoną do szybkiego i dostępnego zarządzania wydarzeniami Kalendarza Google. Interfejs został przygotowany do obsługi klawiaturą i jest testowany z NVDA, JAWS-em oraz Narratorem.

## Ważna informacja

PT Calendar Manager jest niezależną aplikacją do obsługi Kalendarza Google. Program nie jest produktem Google LLC, nie jest przez Google sponsorowany ani oficjalnie zatwierdzony. Google Calendar jest znakiem towarowym Google LLC.

PT Calendar Manager is an independent application for accessing Google Calendar. It is not a Google LLC product and is not sponsored or endorsed by Google. Google Calendar is a trademark of Google LLC.

## Zmiana nazwy w wersji 0.13.0

Dotychczasowa nazwa robocza **GCM by Piotrek** została zastąpiona oficjalną nazwą **PT Calendar Manager**.

Przy pierwszym uruchomieniu program kopiuje zgodne pliki użytkownika z:

`%APPDATA%\GCM by Piotrek`

do:

`%APPDATA%\PT Calendar Manager`

Migracja obejmuje, jeśli pliki istnieją:

- `token.json`;
- `settings.json`;
- `client_secret.json`;
- `last_error.txt`.

Pliki w starym katalogu nie są usuwane. Jeżeli w nowym katalogu istnieje już plik o tej samej nazwie, nie zostanie nadpisany.

## Uruchomienie wersji rozwojowej

1. Rozpakuj archiwum do nowego katalogu.
2. Uruchom `uruchom_pt_calendar_manager.bat`.
3. Starszy plik `uruchom_gcm.bat` pozostaje jako zgodnościowy skrót i uruchamia ten sam program.

## Najważniejsze funkcje

- logowanie do Kalendarza Google przez OAuth;
- wybór kalendarzy w Ustawieniach;
- polski i angielski interfejs;
- odczyt miesiąca i wydarzeń wybranego dnia;
- dodawanie oraz edycja wydarzeń;
- podstawowe cykle: codziennie, co tydzień, co miesiąc, co 3 miesiące, co 6 miesięcy i co rok;
- bezpieczne usuwanie pojedynczego wystąpienia, przyszłych wystąpień albo całego cyklu;
- wyszukiwanie w podanym zakresie dat;
- otwieranie wydarzenia w oficjalnym Kalendarzu Google;
- otwieranie i kopiowanie istniejącego linku spotkania;
- pomoc i komplet skrótów pod `F1`.

## Granice aplikacji

PT Calendar Manager nie zastępuje pełnego interfejsu Kalendarza Google. Zaawansowane reguły cykliczności, uczestnicy, tworzenie spotkań Google Meet, indywidualne przypomnienia, ręczny wybór strefy czasowej oraz pozostałe funkcje specjalistyczne pozostają w oficjalnym interfejsie Google.

## Budowanie EXE

Uruchom `zbuduj_exe.bat`. Katalog wynikowy będzie miał nazwę:

`dist\PT Calendar Manager`
