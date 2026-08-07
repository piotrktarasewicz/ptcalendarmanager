# Kontekst projektu

## Cel

PT Calendar Manager zapewnia szybką i dostępną obsługę Kalendarza Google osobom korzystającym z klawiatury i czytników ekranu. Projekt rozwija dwa produkty o wspólnym pochodzeniu, ale niezależnych numerach wersji.

## Aktualne produkty

### PT Calendar Manager 0.16.3

Samodzielna aplikacja dla Windows znajduje się w katalogu `desktop/`.

Najważniejsze elementy:

- `desktop/src/gcm_core/` — modele, komunikacja z Google Calendar API, logika kalendarzy, internacjonalizacja i wspólne mechanizmy;
- `desktop/src/gcm_desktop/` — interfejs wxPython i integracja z systemem Windows;
- `desktop/tests/` — testy pomocy, instalatora i procesu wydania OAuth;
- `desktop/tools/` — budowanie wydania, walidacja OAuth i zestawianie informacji licencyjnych;
- `desktop/installer/` — definicja instalatora Inno Setup.

Dane użytkownika są przechowywane w `%APPDATA%\PT Calendar Manager`. Token Google znajduje się w `token.dat` i jest szyfrowany przez Windows DPAPI.

### Google Calendar Manager 1.0.4 dla NVDA

Źródła dodatku znajdują się w katalogu `nvda-addon/`.

Najważniejsze elementy:

- `nvda-addon/globalPlugins/googleCalendarManager/` — globalna wtyczka NVDA, logowanie, operacje kalendarza, okna i ustawienia;
- `nvda-addon/locale/` — tłumaczenia;
- `nvda-addon/docs/` — instrukcja dołączana do paczki;
- `nvda-addon/BUILD.md` — proces przygotowania paczki `.nvda-addon`.

Dodatek wymaga NVDA 2026.1 lub nowszego. Jego dane znajdują się w podkatalogu `googleCalendarManager` konfiguracji użytkownika NVDA.

## Pochodzenie

Projekt rozpoczął się jako dodatek Google Calendar Reader dla NVDA. Następnie otrzymał nazwę Google Calendar Manager, a jego koncepcja i część kodu zostały rozwinięte w samodzielną aplikację PT Calendar Manager. Historia tekstowego kodu pozostaje w `main`, aby ułatwiać porównywanie zmian i diagnozowanie regresji.

## Trwałe decyzje projektowe

- Dostępność klawiaturowa i czytniki ekranu mają pierwszeństwo przy projektowaniu interfejsu.
- Nazwa dnia tygodnia jest wypowiadana i wyświetlana przed datą.
- Pomoc zachowuje semantyczną hierarchię nagłówków i zawiera skróty blisko początku dokumentu.
- Opcja instalatora dotycząca pomocy otwiera wspólną pomoc i skróty programu.
- Interfejs i dokumentacja użytkowa pozostają po polsku i angielsku.
- Program nie zarządza uczestnikami spotkań, Google Meet, dostępnością sal, załącznikami ani wyszukiwaniem miejsc w Google Maps, dopóki nie zostanie podjęta osobna decyzja projektowa.
- Outlook i Apple Calendar nie są obecnie częścią projektu. Ewentualne integracje wymagają osobnych modułów dostawców i nie mogą komplikować obsługi Google Calendar.

## Stan wydania 0.16.3

Wydanie Windows 0.16.3 przeszło 12 testów procesu wydania. Zachowano także wcześniejszy wynik 123 testów regresyjnych funkcji aplikacji. Wydanie zweryfikowano pod kątem architektury x64, instalacji cichej, zawartości konfiguracji OAuth oraz braku konfiguracji wdrożeniowej i tokenów w paczce źródłowej.

Nadal wymagane są ręczne testy z NVDA i Narratorem, szczególnie na czystym koncie Windows oraz przy aktualizacji z poprzedniej wersji.

## Kontynuacja w nowej rozmowie

Pamięć rozmowy nie jest źródłem prawdy. Przy rozpoczynaniu kolejnej sesji należy wskazać repozytorium `piotrktarasewicz/ptcalendarmanager` i polecić odczytanie `AGENTS.md` oraz dokumentów z katalogu `docs/`. Pozwala to odtworzyć architekturę, ograniczenia, decyzje dostępnościowe, proces testowania i zasady OAuth bez dostępu do wcześniejszego czatu.
