# Google Calendar Manager

[English version of this description](README.md)

[Pobierz Google Calendar Manager 1.0.3](https://github.com/piotrktarasewicz/nvda-google-calendar-manager/releases/download/v1.0.3/googleCalendarManager-1.0.3.nvda-addon)

Google Calendar Manager to dodatek do NVDA dla systemu Windows. Pozwala użytkownikom NVDA zalogować się do Kalendarza Google, wybrać kalendarze, odczytywać wydarzenia, wyszukiwać wydarzenia oraz wykonywać podstawowe operacje na wydarzeniach z klawiatury.

Dodatek jest przeznaczony do bezpośredniej obsługi z poziomu NVDA. Nie zastępuje pełnego interfejsu webowego Kalendarza Google.

## Aktualny status

Wersja 1.0.3 jest najnowszą publiczną wersją testową.

Paczkę dodatku można pobrać i zainstalować, ale logowanie do Google działa obecnie tylko dla kont Google dodanych przez autora jako zatwierdzeni użytkownicy testowi OAuth. Pełne publiczne logowanie wymaga weryfikacji aplikacji OAuth przez Google.

## Funkcje

- Logowanie do Kalendarza Google przez przeglądarkę.
- Sprawdzanie stanu logowania.
- Wybór kalendarzy używanych przez dodatek.
- Odczyt wydarzeń na dziś i następne sześć dni.
- Odczyt wydarzeń dla wybranego dnia.
- Dodawanie wydarzenia bezpośrednio z okna wydarzeń wybranego dnia.
- Wyszukiwanie wydarzeń według tekstu w wybranym zakresie czasu.
- Wybór gotowego zakresu jednego, trzech, sześciu albo dwunastu miesięcy.
- Ustawienie własnego zakresu bezpośrednio w głównym oknie wyszukiwania.
- Dodawanie nowych wydarzeń, także cyklicznych.
- Edycja istniejących wydarzeń.
- Usuwanie jednego albo wielu zaznaczonych wydarzeń.
- Wybór, czy operacja na wydarzeniu cyklicznym dotyczy tylko wybranego wystąpienia, czy całego cyklu.
- Zbiorcza obsługa zakresu wydarzeń cyklicznych przy usuwaniu wielu zaznaczonych wydarzeń.
- Przełączanie prostego i rozszerzonego trybu odczytu.
- Komunikaty interfejsu po angielsku i po polsku.

## Czego dodatek nie obsługuje

Google Calendar Manager nie obsługuje:

- uczestników spotkań,
- linków Google Meet,
- dostępności sal lub uczestników,
- wyszukiwania miejsc w Mapach Google,
- załączników,
- przypomnień kalendarza.

Pole lokalizacji jest zwykłym tekstem wydarzenia. Dodatek nie wyszukuje miejsc w Mapach Google i nie weryfikuje adresów.

## Wymagania

- Windows.
- NVDA 2026.1 lub nowszy.
- Dostęp do Internetu.
- Konto Google z włączonym Kalendarzem Google.

Osobna instalacja Pythona w systemie nie jest wymagana. Dodatek korzysta ze środowiska Pythona dostarczanego przez NVDA i zawiera potrzebne biblioteki Pythona.

## Instalacja

1. Pobierz plik `.nvda-addon` ze strony wydania.
2. Otwórz go i potwierdź instalację w NVDA.
3. Uruchom ponownie NVDA, jeśli będzie to wymagane.
4. Naciśnij `NVDA+Shift+G`, a następnie `0`, aby zalogować się do Kalendarza Google albo sprawdzić stan logowania.

Jeśli logowanie Google nie jest jeszcze dostępne dla Twojego konta, skontaktuj się z autorem i poproś o dodanie jako użytkownika testowego.

## Główna warstwa skrótów

Najpierw naciśnij `NVDA+Shift+G`. Następnie naciśnij jeden z poniższych klawiszy:

| Klawisz | Działanie |
| --- | --- |
| `0` | Rozpoczęcie logowania do Google albo sprawdzenie stanu logowania. |
| `1` | Odczyt wydarzeń na dziś. |
| `2` | Odczyt wydarzeń na jutro. |
| `3` | Odczyt wydarzeń na pojutrze. |
| `4` | Odczyt wydarzeń za trzy dni. |
| `5` | Odczyt wydarzeń za cztery dni. |
| `6` | Odczyt wydarzeń za pięć dni. |
| `7` | Odczyt wydarzeń za sześć dni. |
| `8` | Przełączenie prostego i rozszerzonego trybu odczytu. |
| `9` | Wybór kalendarzy. |
| `P` | Wybór dnia i otwarcie działań na wydarzeniach z tego dnia. |
| `S` | Wyszukiwanie wydarzeń według tekstu. |
| `N` | Dodanie wydarzenia. |
| `E` | Edycja wydarzenia. |
| `U` | Usuwanie wydarzeń. |
| `H` | Pokazanie pomocy ze skrótami. |

Dostępne są też skróty bezpośrednie:

- `NVDA+Control+Shift+N`: dodanie wydarzenia.
- `NVDA+Control+Shift+E`: edycja wydarzenia.
- `NVDA+Control+Shift+U`: usuwanie wydarzeń.

## Wydarzenia cykliczne

Przy edycji lub usuwaniu wydarzenia cyklicznego dodatek pyta, czy operacja ma dotyczyć tylko wybranego wystąpienia, czy całego cyklu.

Przy usuwaniu wielu zaznaczonych wydarzeń cyklicznych zakres operacji jest wybierany raz i stosowany do zaznaczonych wydarzeń cyklicznych w tej operacji.

Opcja edycji albo usuwania „tego i następnych wystąpień” nie jest dostępna.

## Wydarzenia całodniowe

Całodniowe wydarzenia niecykliczne mogą być jednodniowe albo wielodniowe.

W przypadku cyklicznych wydarzeń całodniowych każde wystąpienie jest traktowane jako pojedyncze wydarzenie całodniowe. Jeśli cykl ma datę końca, data końca cyklu jest ustawiana osobno przez dzień, miesiąc i rok.

## Język

Dodatek używa języka NVDA dla własnych komunikatów i okien dialogowych.

Obecnie dołączone języki:

- angielski,
- polski.

Jeżeli aktualny język NVDA nie jest dołączony, dodatek używa języka angielskiego. Tytuły, opisy i lokalizacje wydarzeń są treścią użytkownika z Kalendarza Google i nie są tłumaczone.

## Dostęp do Kalendarza Google

Dodatek używa OAuth 2.0 i Google Calendar API. Prosi wyłącznie o zakresy potrzebne do obecnych funkcji:

- `https://www.googleapis.com/auth/calendar.events`
- `https://www.googleapis.com/auth/calendar.calendarlist.readonly`
- `https://www.googleapis.com/auth/calendar.settings.readonly`

Dodatek nie prosi o uprawnienie do tworzenia, usuwania, udostępniania ani zmieniania samych kalendarzy.

## Pliki użytkownika

Dodatek przechowuje ustawienia i token logowania Google lokalnie w katalogu konfiguracji użytkownika NVDA, w podkatalogu `googleCalendarManager`.

Typowe pliki lokalne:

- `token.json`: lokalny token logowania Google,
- `settings.json`: wybrane kalendarze i tryb odczytu,
- `last_oauth_error.txt`: plik pomocniczy przy diagnostyce błędów OAuth.

Te pliki nie są częścią paczki dodatku i nie powinny być dodawane do repozytorium.

## Prywatność

Zobacz [PRIVACY_pl.md](PRIVACY_pl.md).

## Instrukcja obsługi

Paczka dodatku zawiera szczegółową instrukcję:

- `docs/readme.html` — angielski,
- `docs/readme_pl.html` — polski.

## Licencja

Google Calendar Manager jest udostępniany na warunkach GNU General Public License w wersji 3 lub dowolnej późniejszej (`GPL-3.0-or-later`). Zobacz [LICENSE](LICENSE) oraz [LICENSE-NOTICE.md](LICENSE-NOTICE.md).

## Autor

Piotr Tarasewicz

Kontakt: `https://ptprojects.app/contact.html`

Strona projektu: `https://ptprojects.app/projects/google-calendar-manager/`
