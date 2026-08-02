# GCM by Piotrek 0.2.0 — pierwszy etap właściwej aplikacji

GCM by Piotrek to dostępny klient Kalendarza Google dla Windows, projektowany
od początku do obsługi klawiaturą i współpracy z NVDA, JAWS-em oraz Narratorem.

Wersja 0.2.0 jest pierwszym etapem właściwej aplikacji. Łączy sprawdzony
interfejs wxPython z nowym, niezależnym od NVDA pakietem `gcm_core`.

## Co działa w tej wersji

- logowanie do Google w domyślnej przeglądarce;
- automatyczne odświeżanie tokenu OAuth;
- próba bezpiecznego skopiowania istniejącego tokenu, ustawień i pliku
  `client_secret.json` z dodatku NVDA;
- lista kalendarzy i wybór kalendarzy używanych przez aplikację;
- pobieranie prawdziwych wydarzeń dla wybranego miesiąca;
- lista wszystkich dni miesiąca z liczbą wydarzeń;
- lista wydarzeń dla zaznaczonego dnia;
- wydarzenia godzinowe, całodniowe i wielodniowe;
- poprzedni i następny miesiąc, dzisiaj oraz przejście do daty;
- wyszukiwanie w wydarzeniach pobranych dla bieżącego miesiąca;
- dostępne okno szczegółów wydarzenia;
- operacje sieciowe wykonywane poza głównym wątkiem interfejsu.

## Czego jeszcze nie ma

Przyciski Dodaj, Edytuj i Usuń są już obecne, ale w wersji 0.2.0 nie wykonują
zmian w Google. Jest to celowy etap tylko do odczytu. Najpierw sprawdzamy
logowanie, prawdziwe dane, listy, fokus i stabilność z trzema czytnikami ekranu.

## Ochrona działającego dodatku NVDA

Aplikacja nie zmienia i nie usuwa plików dodatku NVDA. Przy pierwszym
uruchomieniu może skopiować do własnego katalogu:

- `%APPDATA%\nvda\googleCalendarManager\token.json`,
- `%APPDATA%\nvda\googleCalendarManager\settings.json`,
- `client_secret.json` z katalogu zainstalowanego dodatku.

Własne dane aplikacji są przechowywane w:

`%APPDATA%\GCM by Piotrek`

Wylogowanie w aplikacji usuwa wyłącznie jej własną kopię tokenu. Nie wylogowuje
dodatku NVDA.

## Uruchomienie

1. Rozpakuj cały katalog do nowego miejsca.
2. Uruchom `uruchom_gcm.bat`.
3. Skrypt wykryje 64-bitowy Python 3.10–3.13, utworzy `.venv`, zainstaluje
   zależności i uruchomi aplikację.
4. Pierwsza instalacja bibliotek wymaga Internetu.

Jeżeli aplikacja znajdzie token z dodatku NVDA, spróbuje od razu pobrać
kalendarze i wydarzenia. Jeżeli tokenu nie znajdzie albo jest nieważny, użyj
przycisku `Zaloguj do Google`.

## Gdy aplikacja nie znajdzie konfiguracji OAuth

Po wybraniu `Zaloguj do Google` aplikacja pozwoli wskazać plik
`client_secret.json`. Możesz wskazać plik z katalogu zainstalowanego dodatku
NVDA. Zostanie skopiowany do katalogu danych GCM by Piotrek.

Typowa lokalizacja:

`%APPDATA%\nvda\addons\googleCalendarManager\globalPlugins\googleCalendarManager\client_secret.json`

## Skróty

- `Ctrl+L` — zaloguj lub wyloguj;
- `Ctrl+K` — wybierz kalendarze;
- `Ctrl+N` — dodaj wydarzenie, w 0.2.0 pokazuje informację o następnym etapie;
- `Ctrl+E` — edytuj, w 0.2.0 tylko informacja;
- `Delete` — usuń, w 0.2.0 tylko informacja;
- `Ctrl+F` — wyszukaj w pobranym miesiącu;
- `Ctrl+G` — przejdź do daty;
- `Ctrl+D` — dzisiaj;
- `F5` — pobierz miesiąc ponownie z Google;
- `Alt+Strzałka w lewo` — poprzedni miesiąc;
- `Alt+Strzałka w prawo` — następny miesiąc;
- `Enter` na liście dni — przejdź do listy wydarzeń;
- `Enter` na wydarzeniu — pokaż szczegóły.

## Budowanie EXE

Uruchom `zbuduj_exe.bat`. Program zostanie utworzony w katalogu:

`dist\GCM by Piotrek\GCM by Piotrek.exe`

Na tym etapie używamy wariantu katalogowego `onedir`, który jest prostszy do
diagnozowania niż pojedynczy plik EXE.

## Bezpieczeństwo etapu 0.2.0

Kod interfejsu nie importuje żadnych modułów NVDA. Rdzeń Google znajduje się w
osobnym pakiecie `gcm_core`. Nie wykonujemy jeszcze operacji zapisu, dlatego
nawet błąd interfejsu nie powinien zmienić wydarzeń w kalendarzu.
