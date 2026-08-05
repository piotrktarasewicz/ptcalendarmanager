# Polityka prywatności

POLITYKA PRYWATNOŚCI PT CALENDAR MANAGER

Ostatnia aktualizacja: 5 sierpnia 2026

1. Zakres dokumentu

Niniejsza polityka opisuje sposób, w jaki PT Calendar Manager uzyskuje dostęp do danych Kalendarza Google, wykorzystuje je i przechowuje. Autorem aplikacji jest Piotr Tarasewicz, działający pod nazwą PT Projects.

2. Logowanie i zakres dostępu Google

Logowanie odbywa się w przeglądarce za pośrednictwem mechanizmu Google OAuth 2.0. Użytkownik sam przyznaje aplikacji uprawnienia. Aplikacja używa następujących zakresów:

- https://www.googleapis.com/auth/calendar.events
- https://www.googleapis.com/auth/calendar.calendarlist.readonly
- https://www.googleapis.com/auth/calendar.settings.readonly

Zakresy te służą do odczytywania listy kalendarzy i ustawień strefy czasowej oraz do odczytywania, wyszukiwania, tworzenia, edytowania i usuwania wydarzeń na wyraźne polecenie użytkownika.

3. Dane odczytywane z Google

Aplikacja może przetwarzać dane kalendarzy i wydarzeń, w szczególności ich nazwy, tytuły, opisy, lokalizacje, daty, godziny, reguły cykliczności, identyfikatory techniczne, informacje o uczestnikach oraz istniejące linki do spotkań. Dane te są używane wyłącznie do funkcji widocznych w interfejsie aplikacji.

4. Przechowywanie lokalne

PT Calendar Manager nie prowadzi własnej zewnętrznej bazy danych z wydarzeniami użytkownika. Pobrane wydarzenia są przechowywane w pamięci programu podczas działania aplikacji i nie są zapisywane w osobnej lokalnej bazie.

W katalogu %APPDATA%\PT Calendar Manager mogą znajdować się:

- token.dat — token Google zaszyfrowany mechanizmem Windows DPAPI i powiązany z bieżącym kontem użytkownika Windows;
- settings.json — wybrany język i identyfikatory wybranych kalendarzy;
- client_secret.json — konfiguracja klienta OAuth aplikacji;
- last_error.txt — lokalny raport techniczny ostatniego błędu.

Raport błędu może zawierać techniczne identyfikatory, nazwy kalendarzy lub fragmenty danych związanych z operacją, podczas której wystąpił błąd. Plik nie jest automatycznie wysyłany autorowi ani do innego serwera.

Przy aktualizacji ze starszej wersji w katalogu danych może pozostać wcześniejszy plik token.json. Po udanym zaszyfrowaniu aplikacja usuwa jego kopię z bieżącego katalogu. Starsze katalogi poprzednich wersji nie są usuwane automatycznie, aby nie utrudniać powrotu do wcześniejszej wersji.

5. Przesyłanie i udostępnianie danych

Dane kalendarza są przesyłane bezpośrednio między aplikacją a usługami Google wymaganymi do logowania i obsługi Google Calendar API. PT Projects nie otrzymuje kopii kalendarzy, wydarzeń ani tokenu użytkownika i nie wykorzystuje ich do reklam, profilowania ani analityki.

Aplikacja nie sprzedaje ani nie przekazuje danych użytkownika innym podmiotom. Korzystanie z danych otrzymanych z interfejsów Google jest ograniczone do funkcji aplikacji i odbywa się zgodnie z Google API Services User Data Policy, w tym z wymaganiami Limited Use.

6. Kontrola użytkownika i usuwanie danych

Wylogowanie w aplikacji usuwa lokalny token Google. Dostęp aplikacji można także odwołać w ustawieniach bezpieczeństwa konta Google. Pozostałe dane lokalne można usunąć przez skasowanie katalogu %APPDATA%\PT Calendar Manager. Przed usunięciem warto zamknąć aplikację.

Odinstalowanie przyszłej wersji instalacyjnej może pozostawiać ustawienia użytkownika, jeżeli użytkownik zdecyduje się je zachować. Instalator powinien jasno informować o tej możliwości.

7. Bezpieczeństwo

Token jest chroniony przez Windows DPAPI, co ogranicza możliwość użycia go przez inne konto Windows na tym samym komputerze. Żadne rozwiązanie techniczne nie zapewnia jednak absolutnego bezpieczeństwa. Użytkownik powinien chronić swoje konto Windows i urządzenie.

8. Zmiany i kontakt

Polityka może być aktualizowana, gdy zmieni się sposób działania aplikacji, zakres dostępu Google albo sposób przechowywania danych. Aktualna wersja będzie publikowana na stronie PT Projects. Pytania można kierować przez stronę https://ptprojects.app/.
