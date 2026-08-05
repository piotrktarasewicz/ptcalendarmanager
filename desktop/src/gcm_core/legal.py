from __future__ import annotations

from .branding import (
    INDEPENDENCE_NOTICE_EN,
    INDEPENDENCE_NOTICE_PL,
    PRODUCT_DESCRIPTION_EN,
    PRODUCT_DESCRIPTION_PL,
    PRODUCT_NAME,
    PRODUCT_VERSION,
)
from .i18n import get_language
from .oauth import SCOPES

PROJECT_WEBSITE = "https://ptprojects.app/"
LAST_UPDATED_PL = "5 sierpnia 2026"
LAST_UPDATED_EN = "5 August 2026"


def about_text() -> str:
    if get_language() == "pl":
        return (
            f"{PRODUCT_NAME}\n"
            f"Wersja {PRODUCT_VERSION}\n\n"
            f"{PRODUCT_DESCRIPTION_PL}.\n\n"
            "Autor: Piotr Tarasewicz\n"
            "Projekt: PT Projects\n"
            f"Strona: {PROJECT_WEBSITE}\n\n"
            "Aplikacja została zaprojektowana do obsługi klawiaturą i jest "
            "testowana z NVDA, JAWS-em oraz Narratorem.\n\n"
            + INDEPENDENCE_NOTICE_PL
        )
    return (
        f"{PRODUCT_NAME}\n"
        f"Version {PRODUCT_VERSION}\n\n"
        f"{PRODUCT_DESCRIPTION_EN}.\n\n"
        "Author: Piotr Tarasewicz\n"
        "Project: PT Projects\n"
        f"Website: {PROJECT_WEBSITE}\n\n"
        "The application is designed for keyboard use and is tested with "
        "NVDA, JAWS and Narrator.\n\n"
        + INDEPENDENCE_NOTICE_EN
    )


def privacy_text() -> str:
    scope_lines = "\n".join(f"- {scope}" for scope in SCOPES)
    if get_language() == "pl":
        return f"""POLITYKA PRYWATNOŚCI PT CALENDAR MANAGER

Ostatnia aktualizacja: {LAST_UPDATED_PL}

1. Zakres dokumentu

Niniejsza polityka opisuje sposób, w jaki {PRODUCT_NAME} uzyskuje dostęp do danych Kalendarza Google, wykorzystuje je i przechowuje. Autorem aplikacji jest Piotr Tarasewicz, działający pod nazwą PT Projects.

2. Logowanie i zakres dostępu Google

Logowanie odbywa się w przeglądarce za pośrednictwem mechanizmu Google OAuth 2.0. Użytkownik sam przyznaje aplikacji uprawnienia. Aplikacja używa następujących zakresów:

{scope_lines}

Zakresy te służą do odczytywania listy kalendarzy i ustawień strefy czasowej oraz do odczytywania, wyszukiwania, tworzenia, edytowania i usuwania wydarzeń na wyraźne polecenie użytkownika.

3. Dane odczytywane z Google

Aplikacja może przetwarzać dane kalendarzy i wydarzeń, w szczególności ich nazwy, tytuły, opisy, lokalizacje, daty, godziny, reguły cykliczności, identyfikatory techniczne, informacje o uczestnikach oraz istniejące linki do spotkań. Dane te są używane wyłącznie do funkcji widocznych w interfejsie aplikacji.

4. Przechowywanie lokalne

{PRODUCT_NAME} nie prowadzi własnej zewnętrznej bazy danych z wydarzeniami użytkownika. Pobrane wydarzenia są przechowywane w pamięci programu podczas działania aplikacji i nie są zapisywane w osobnej lokalnej bazie.

W katalogu %APPDATA%\\{PRODUCT_NAME} mogą znajdować się:

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

Wylogowanie w aplikacji usuwa lokalny token Google. Dostęp aplikacji można także odwołać w ustawieniach bezpieczeństwa konta Google. Pozostałe dane lokalne można usunąć przez skasowanie katalogu %APPDATA%\\{PRODUCT_NAME}. Przed usunięciem warto zamknąć aplikację.

Odinstalowanie przyszłej wersji instalacyjnej może pozostawiać ustawienia użytkownika, jeżeli użytkownik zdecyduje się je zachować. Instalator powinien jasno informować o tej możliwości.

7. Bezpieczeństwo

Token jest chroniony przez Windows DPAPI, co ogranicza możliwość użycia go przez inne konto Windows na tym samym komputerze. Żadne rozwiązanie techniczne nie zapewnia jednak absolutnego bezpieczeństwa. Użytkownik powinien chronić swoje konto Windows i urządzenie.

8. Zmiany i kontakt

Polityka może być aktualizowana, gdy zmieni się sposób działania aplikacji, zakres dostępu Google albo sposób przechowywania danych. Aktualna wersja będzie publikowana na stronie PT Projects. Pytania można kierować przez stronę {PROJECT_WEBSITE}.
"""
    return f"""PT CALENDAR MANAGER PRIVACY POLICY

Last updated: {LAST_UPDATED_EN}

1. Scope

This policy explains how {PRODUCT_NAME} accesses, uses and stores Google Calendar data. The application is developed by Piotr Tarasewicz under the PT Projects name.

2. Google sign-in and access scopes

Sign-in takes place in the user's browser through Google OAuth 2.0. The user grants the requested permissions. The application uses these scopes:

{scope_lines}

They are used to read the calendar list and time-zone settings and to read, search, create, edit and delete events when the user explicitly requests an action.

3. Google data accessed

The application may process calendar and event data, including names, titles, descriptions, locations, dates, times, recurrence rules, technical identifiers, attendee information and existing meeting links. This data is used only for features visible in the application interface.

4. Local storage

{PRODUCT_NAME} does not maintain an external database of users' events. Downloaded events are held in application memory while the program is running and are not written to a separate local event database.

The %APPDATA%\\{PRODUCT_NAME} folder may contain:

- token.dat — the Google token encrypted with Windows DPAPI and tied to the current Windows user account;
- settings.json — the selected language and selected calendar identifiers;
- client_secret.json — the application's OAuth client configuration;
- last_error.txt — a local technical report for the most recent error.

An error report may contain technical identifiers, calendar names or fragments of data related to the operation that failed. It is not automatically sent to the developer or to another server.

When upgrading from an earlier version, a previous token.json file may temporarily remain in the current data folder. After successful encryption, the application removes the current-folder plaintext copy. Data folders from older application versions are not removed automatically so that rollback remains possible.

5. Data transmission and sharing

Calendar data is transmitted directly between the application and the Google services required for sign-in and the Google Calendar API. PT Projects does not receive copies of users' calendars, events or tokens and does not use them for advertising, profiling or analytics.

The application does not sell or disclose user data to other parties. Its use of information received from Google APIs is limited to the application's user-facing features and complies with the Google API Services User Data Policy, including the Limited Use requirements.

6. User control and deletion

Signing out in the application removes the local Google token. Access can also be revoked in the security settings of the user's Google Account. Other local data can be removed by deleting the %APPDATA%\\{PRODUCT_NAME} folder after closing the application.

A future installed version may preserve user settings during uninstall when the user chooses to keep them. The installer should clearly explain that choice.

7. Security

The token is protected by Windows DPAPI, which limits its use by another Windows account on the same computer. No technical measure can provide absolute security, so users should protect their Windows account and device.

8. Changes and contact

This policy may be updated when the application, Google access scopes or data storage practices change. The current version will be published on the PT Projects website. Questions can be submitted through {PROJECT_WEBSITE}.
"""


def legal_text() -> str:
    if get_language() == "pl":
        return f"""INFORMACJE PRAWNE I STATUS PROJEKTU

Ostatnia aktualizacja: {LAST_UPDATED_PL}

1. Niezależność produktu

{INDEPENDENCE_NOTICE_PL}

Nazwa Google i nazwa Google Calendar są używane wyłącznie opisowo, aby wskazać usługę, z którą współpracuje aplikacja. Aplikacja nie używa logo Google ani nie sugeruje partnerstwa z Google.

2. Status wersji

Wersja {PRODUCT_VERSION} jest wersją testową przygotowywaną do pierwszego wydania publicznego. Przed wykonaniem ważnej operacji użytkownik powinien sprawdzić jej wynik w Kalendarzu Google. Operacje usuwania i edycji wymagają potwierdzenia w aplikacji, lecz użytkownik nadal odpowiada za wybór właściwego wydarzenia i zakresu operacji.

3. Zależność od usług zewnętrznych

Działanie logowania i funkcji kalendarza zależy od usług Google, połączenia z Internetem oraz dostępności Google Calendar API. Zmiana zasad, interfejsów lub dostępności usług Google może wpłynąć na działanie aplikacji.

4. Prywatność

Szczegółowe informacje o dostępie do danych, ich wykorzystaniu, przechowywaniu i usuwaniu znajdują się w Polityce prywatności dostępnej z okna O programie.

5. Oprogramowanie zewnętrzne

Aplikacja korzysta z Pythona, wxPython oraz oficjalnych bibliotek klienta i uwierzytelniania Google. Informacje o licencjach komponentów zewnętrznych zostaną dołączone do instalatora i publicznego repozytorium przed wydaniem 1.0.
"""
    return f"""LEGAL INFORMATION AND PROJECT STATUS

Last updated: {LAST_UPDATED_EN}

1. Independent product

{INDEPENDENCE_NOTICE_EN}

The Google and Google Calendar names are used only descriptively to identify the service supported by the application. The application does not use the Google logo and does not imply a partnership with Google.

2. Version status

Version {PRODUCT_VERSION} is a test release being prepared for the first public release. Users should verify the result of important operations in Google Calendar. Editing and deletion operations require confirmation in the application, but the user remains responsible for selecting the correct event and operation scope.

3. Dependence on external services

Google sign-in and calendar features depend on Google services, an Internet connection and the availability of the Google Calendar API. Changes to Google's policies, interfaces or service availability may affect the application.

4. Privacy

Detailed information about data access, use, storage and deletion is provided in the Privacy Policy available from the About dialog.

5. Third-party software

The application uses Python, wxPython and official Google client and authentication libraries. License information for third-party components will be bundled with the installer and public repository before version 1.0 is released.
"""
