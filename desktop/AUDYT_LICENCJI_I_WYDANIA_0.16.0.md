# Audyt licencji i przygotowania wydania 0.16.0

Data audytu: 6 sierpnia 2026 r.

Ten dokument opisuje decyzje techniczne i licencyjne przyjęte dla PT Calendar
Managera 0.16.0. Nie zastępuje indywidualnej porady prawnej.

## 1. Licencja programu

PT Calendar Manager jest wydawany na licencji `GPL-3.0-or-later`.

Powody:

- aplikacja została utworzona przez adaptację i rozwinięcie kodu oraz
  architektury dodatku Google Calendar Manager dla NVDA;
- dodatek jest objęty licencją `GPL-3.0-or-later`;
- ta sama licencja zapewnia spójne i przejrzyste warunki dalszego
  rozpowszechniania programu;
- każdemu wydaniu binarnemu będzie towarzyszyć odpowiadający mu kod źródłowy,
  skrypty budowania i skrypt instalatora.

W programie dostępne są: informacja o prawach autorskich, brak gwarancji, pełny
tekst GNU GPL oraz informacje o komponentach zewnętrznych.

## 2. Kod źródłowy obok binariów

Skrypt wydania tworzy trzy główne artefakty:

- instalator EXE;
- przenośne archiwum ZIP;
- odpowiadające im archiwum źródłowe ZIP.

Pakiet źródłowy jest generowany z tego samego katalogu roboczego co binaria.
Nie zawiera tokenów użytkownika, ustawień, środowisk wirtualnych, wyników
budowania ani katalogu z konfiguracją wdrożeniową OAuth.

Przy publicznym udostępnieniu instalator, wersja przenośna i dokładny pakiet
źródłowy muszą być dostępne razem. Alternatywnie dokładne źródła mogą być
udostępnione pod jednoznacznie oznaczonym publicznym tagiem repozytorium.

## 3. Komponenty zewnętrzne

Główne komponenty to CPython, wxPython/wxWidgets, biblioteki Google API,
`tzdata` i bootloader PyInstaller. Ich główne licencje są dołączone do drzewa
źródeł.

Podczas właściwego budowania skrypt tworzy raport dokładnych wersji wszystkich
pakietów z izolowanego środowiska oraz kopiuje dostępne pliki `LICENSE`,
`COPYING`, `NOTICE` i podobne. Raport ten trafia do instalatora i wersji
przenośnej.

Inno Setup jest narzędziem kompilującym instalator i nie jest dołączane do
programu. Przed regularnym lub komercyjnym użyciem jego kompilatora należy
sprawdzić aktualne warunki licencji Inno Setup.

## 4. Konfiguracja Google OAuth

Domyślny build nie zawiera `client_secret.json`. Chroni to przed przypadkowym
rozpowszechnieniem konfiguracji projektu testowego.

Wewnętrzny lub przyszły publiczny build może dołączyć konfigurację klienta
OAuth wyłącznie przez świadomy parametr `-IncludeOAuthClient`. Konfiguracja
musi pochodzić z właściwego klienta typu Desktop app.

Aplikacje desktopowe nie mogą skutecznie zachować danych klienta OAuth w
poufności: identyfikator i ewentualny sekret klienta są obecne na urządzeniu
użytkownika i mogą zostać odczytane z dystrybucji. Nie wolno więc traktować
ich jako mechanizmu chroniącego dane użytkowników. Właściwą ochronę zapewniają
zgoda użytkownika, ograniczone zakresy, weryfikacja projektu i bezpieczne
przechowywanie tokenu użytkownika.

Każdy odbiorca źródeł może zbudować aplikację z własnym klientem Desktop app.
Dane wdrożeniowe projektu autora nie są potrzebne do studiowania, modyfikowania
ani kompilowania kodu.

## 5. Instalator

Projekt instalatora:

- instaluje program dla bieżącego użytkownika;
- nie wymaga uprawnień administratora;
- używa stałego `AppId`, który musi pozostać niezmienny w kolejnych wersjach;
- instaluje program w `%LOCALAPPDATA%\\Programs\\PT Calendar Manager`;
- zachowuje `%APPDATA%\\PT Calendar Manager` podczas aktualizacji;
- przy odinstalowaniu pyta osobno o usunięcie danych, z domyślną odpowiedzią
  „Nie”;
- oferuje opcjonalny skrót pulpitu;
- udostępnia dokumentację i licencję z menu Start;
- nie przedstawia informacji o niezależności od Google jako regulaminu
  wymagającego akceptacji.

## 6. Bezpieczeństwo wydania

- token Google pozostaje szyfrowany mechanizmem Windows DPAPI;
- tokeny i ustawienia są wykluczone ze źródeł i artefaktów;
- domyślny proces nie dołącza konfiguracji OAuth;
- skrypt oblicza SHA-256 dla wszystkich artefaktów;
- manifest żąda poziomu `asInvoker` i obsługuje skalowanie Per-Monitor V2;
- pliki nie są jeszcze podpisywane cyfrowo.

## 7. Ograniczenia obecnego audytu

W środowisku przygotowania paczki nie można było skompilować ani uruchomić
natywnego EXE i instalatora Windows. Sprawdzono kod, strukturę, dokumenty,
manifest XML, skrypty i testy automatyczne. Ostateczne potwierdzenie wymaga
budowania oraz testów na 64-bitowym Windowsie.

Wersja 0.16.0 nie jest kandydatem 1.0 RC. Weryfikacja Google OAuth, film
weryfikacyjny i publiczny test logowania są odrębnym etapem przed oznaczeniem
wersji RC.
