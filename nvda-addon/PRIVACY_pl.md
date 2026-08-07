# Polityka prywatności Google Calendar Manager

Data obowiązywania: 2026-07-09

Google Calendar Manager to dodatek do NVDA dla systemu Windows. Pozwala użytkownikowi uzyskiwać dostęp do wybranych wydarzeń Kalendarza Google i zarządzać nimi z poziomu NVDA.

Ta polityka opisuje, w jaki sposób dodatek uzyskuje dostęp do danych użytkownika Google, jak ich używa, gdzie je przechowuje i czy je udostępnia.

## Dane odczytywane z Kalendarza Google

Google Calendar Manager może uzyskiwać dostęp do następujących danych Kalendarza Google, zależnie od działań użytkownika:

- wpisów listy kalendarzy, aby użytkownik mógł wybrać kalendarze używane przez dodatek;
- ustawień kalendarza, takich jak strefa czasowa Kalendarza Google;
- danych wydarzeń w wybranych kalendarzach, w tym tytułów, dat, godzin, opisów, lokalizacji, informacji o cykliczności i identyfikatorów wydarzeń.

## Używane zakresy OAuth

Dodatek prosi o następujące zakresy Google Calendar API:

- `https://www.googleapis.com/auth/calendar.events`
  - Używany do odczytu, dodawania, edycji i usuwania wydarzeń zgodnie z działaniami użytkownika.
- `https://www.googleapis.com/auth/calendar.calendarlist.readonly`
  - Używany do odczytu listy kalendarzy, aby można było wybrać kalendarze w dodatku.
- `https://www.googleapis.com/auth/calendar.settings.readonly`
  - Używany do odczytu ustawień Kalendarza, takich jak strefa czasowa.

Dodatek nie prosi o uprawnienie do tworzenia, usuwania, udostępniania ani modyfikowania samych kalendarzy.

## Sposób użycia danych

Dane Kalendarza Google są używane wyłącznie do działania funkcji dodatku:

- odczytywania wydarzeń przez NVDA;
- pokazywania list wydarzeń w oknach dialogowych NVDA;
- wyszukiwania wydarzeń według tekstu;
- dodawania nowych wydarzeń;
- edycji istniejących wydarzeń;
- usuwania wybranych wydarzeń;
- wyboru kalendarzy używanych przez dodatek.

Dane Kalendarza Google nie są używane do reklam, analityki, profilowania ani innych niezwiązanych celów.

## Przechowywanie lokalne

Google Calendar Manager przechowuje ustawienia i token logowania Google lokalnie na komputerze użytkownika, w katalogu konfiguracji użytkownika NVDA, w podkatalogu `googleCalendarManager`.

Typowe pliki lokalne:

- `token.json`: token logowania OAuth Google;
- `settings.json`: wybrane kalendarze i ustawienia dodatku;
- `last_oauth_error.txt`: informacje diagnostyczne dotyczące błędów OAuth.

Dodatek nie przechowuje danych Kalendarza Google na serwerze kontrolowanym przez autora.

## Udostępnianie danych

Google Calendar Manager nie sprzedaje, nie wynajmuje i nie udostępnia danych Kalendarza Google osobom trzecim.

Dodatek komunikuje się z Google Calendar API w zakresie potrzebnym do wykonania działań zleconych przez użytkownika. Nie wysyła danych kalendarza na serwery kontrolowane przez autora.

## Dostęp człowieka do danych użytkownika

Autor nie ma dostępu do danych Kalendarza Google użytkownika przez dodatek.

Jeżeli użytkownik skontaktuje się z autorem w sprawie pomocy technicznej i dobrowolnie przekaże logi, zrzuty ekranu albo szczegóły kalendarza, te informacje zostaną użyte wyłącznie do diagnozy zgłoszonego problemu.

## Przechowywanie i usuwanie danych

Google Calendar Manager przechowuje token OAuth i ustawienia lokalnie do czasu ich usunięcia przez użytkownika.

Użytkownik może usunąć lokalne dane dodatku przez skasowanie folderu `googleCalendarManager` z katalogu konfiguracji użytkownika NVDA.

Użytkownik może w każdej chwili cofnąć dostęp dodatku do konta Google w ustawieniach bezpieczeństwa konta Google, w sekcji dostępu aplikacji innych firm.

## Ograniczone użycie danych

Sposób użycia i przekazywania informacji otrzymanych z interfejsów API Google przez Google Calendar Manager będzie zgodny z Google API Services User Data Policy, w tym z wymaganiami Limited Use.

## Kontakt

Autor: Piotr Tarasewicz

Kontakt: `https://ptprojects.app/contact.html`

Strona projektu: `https://ptprojects.app/projects/google-calendar-manager/`
