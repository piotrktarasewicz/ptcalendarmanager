# PT Calendar Manager — dokumentacja użytkownika

Wersja 0.15.3

## 1. Przeznaczenie

PT Calendar Manager jest dostępną aplikacją dla Windows, która ułatwia codzienne zarządzanie Kalendarzem Google bez konieczności korzystania z pełnego interfejsu strony internetowej. Aplikacja nie ma zastępować wszystkich funkcji Kalendarza Google. Bardziej zaawansowane operacje można otworzyć bezpośrednio w oficjalnym interfejsie Google.

Interfejs jest przygotowany do obsługi klawiaturą i testowany z NVDA, JAWS-em oraz Narratorem.

## 2. Pierwsze uruchomienie i logowanie

Po uruchomieniu główne okno działa także bez logowania. Ustawienia języka, pomoc i informacje o programie są dostępne offline.

Aby połączyć konto Google:

1. Otwórz menu Konto i wybierz „Zaloguj do Google” albo naciśnij `Ctrl+L`.
2. Jeśli program nie znajdzie konfiguracji OAuth, wskaż plik `client_secret.json`.
3. Zaloguj się w otwartej przeglądarce i zaakceptuj wymagane uprawnienia.
4. Wróć do PT Calendar Manager.

Token logowania jest zapisywany lokalnie jako `token.dat` i szyfrowany mechanizmem Windows DPAPI dla bieżącego użytkownika Windows.

## 3. Główne okno

Na górze znajduje się klasyczny pasek menu Windows:

- Kalendarz;
- Wydarzenie;
- Konto;
- Ustawienia;
- Pomoc.

Lewy `Alt` przenosi fokus do paska menu. Po menu porusza się strzałkami, a polecenie wybiera Enterem. Przy pozycjach menu są wyświetlane skróty klawiaturowe.

Pod paskiem menu znajduje się nagłówek bieżącego miesiąca. Główna część okna zawiera wyłącznie dwie listy:

- po lewej — dni bieżącego miesiąca;
- po prawej — wydarzenia zaznaczonego dnia.

Tabulator przełącza tylko między tymi dwiema listami. `Enter` na liście dni przenosi fokus na wydarzenia, a `Enter` na wydarzeniu otwiera szczegóły. `Shift+F10` otwiera menu kontekstowe właściwe dla aktualnej listy.

Na pasku stanu wyświetlany jest komunikat bieżącej operacji oraz stan połączenia konta Google.

## 4. Pasek menu

### Kalendarz

Zawiera zmianę miesiąca, przejście do dzisiaj lub wskazanej daty, wyszukiwanie, dodawanie wydarzenia oraz odświeżanie danych.

### Wydarzenie

Zawiera szczegóły, edycję, usuwanie, otwieranie wydarzenia w Google i obsługę istniejącego linku spotkania. Polecenia niedostępne bez zaznaczonego wydarzenia są standardowo oznaczone jako nieaktywne.

### Konto

Zawiera polecenie „Zaloguj do Google” albo „Wyloguj z Google”, zależnie od aktualnego stanu.

### Ustawienia

Otwiera ustawienia języka i wybór kalendarzy. Dostępne są także skróty `Ctrl+,` i zachowany zgodnościowo `Ctrl+K`.

### Pomoc

Zawiera „Pomoc i skróty” oraz „O programie”. Okno „O programie” udostępnia numer wersji, dane autora, informację o niezależności produktu, politykę prywatności i informacje prawne.

## 5. Ustawienia

Można w nich:

- wybrać język: Automatycznie, Polski albo English;
- wybrać kalendarze używane przez aplikację.

Wybór kalendarzy jest pojedynczą listą z polami wyboru. Tabulator przechodzi z języka bezpośrednio do tej listy. Strzałki zmieniają bieżący kalendarz, a Spacja zaznacza go lub odznacza.

Po zmianie faktycznego języka program proponuje natychmiastowe ponowne uruchomienie. Zmiana samych kalendarzy nie wymaga restartu.

## 6. Dodawanie i edycja wydarzeń

PT Calendar Manager obsługuje wydarzenia godzinowe i całodniowe. Formularz umożliwia podanie tytułu, dat, godzin, lokalizacji, kalendarza i podstawowej cykliczności.

Obsługiwane cykle:

- codziennie;
- co tydzień;
- co miesiąc;
- co 3 miesiące;
- co 6 miesięcy;
- co rok.

Cykl może nie mieć daty zakończenia albo zakończyć się we wskazanym dniu.

Przy edycji wydarzenia cyklicznego można zmienić jedno wystąpienie albo cały prosty cykl. Złożone reguły utworzone poza PT Calendar Manager są chronione przed przypadkowym uproszczeniem.

## 7. Usuwanie

Usuwanie zawsze wymaga potwierdzenia. Dla wydarzenia cyklicznego dostępne są zakresy:

- tylko to wystąpienie;
- to i wszystkie kolejne;
- cały cykl.

Domyślnie wybierana jest najbezpieczniejsza operacja dotycząca pojedynczego wystąpienia.

## 8. Wyszukiwanie

Wyszukiwanie obejmuje wybrane kalendarze, podany tekst oraz datę początkową i końcową włącznie. Po wybraniu wyniku aplikacja przechodzi do odpowiedniego dnia i ustawia fokus na wydarzeniu.

## 9. Otwieranie w Google i link spotkania

„Otwórz w Google” otwiera zaznaczone wydarzenie w oficjalnym interfejsie Kalendarza Google.

Jeżeli wydarzenie zawiera internetowy link spotkania dodany poza aplikacją, polecenie „Link spotkania” pozwala go otworzyć albo skopiować. PT Calendar Manager nie tworzy nowych spotkań Google Meet.

## 10. Skróty aplikacji

- `Ctrl+L` — zaloguj albo wyloguj;
- `Ctrl+,` — ustawienia;
- `Ctrl+K` — ustawienia, zachowany skrót wyboru kalendarzy;
- `F1` — pomoc;
- `Alt+Strzałka w lewo` — poprzedni miesiąc;
- `Ctrl+D` — dzisiaj;
- `Alt+Strzałka w prawo` — następny miesiąc;
- `Ctrl+G` — przejdź do daty;
- `Ctrl+F` — wyszukaj;
- `Ctrl+N` — dodaj wydarzenie;
- `F5` — odśwież;
- `Ctrl+E` — edytuj;
- `Delete` — usuń;
- `Ctrl+Shift+G` — otwórz wydarzenie w Google;
- `Ctrl+J` — otwórz lub skopiuj link spotkania;
- lewy `Alt` — przejdź do paska menu;
- `Shift+F10` — menu kontekstowe aktualnej listy.

Menu i jego pozycje mają standardowe litery dostępu Windows. Ich oznaczenia są dostosowane osobno do języka polskiego i angielskiego.

## 11. Wygląd i kolory

Aplikacja korzysta z natywnych kolorów Windows. Nie ma własnej skórki ani ręcznie ustawionych barw tła. Delikatny systemowy kolor akcentu jest używany tylko dla nagłówka miesiąca oraz nazw paneli z listami. Informacja nigdy nie jest przekazywana wyłącznie kolorem.

## 12. Dane użytkownika

Dane lokalne znajdują się w `%APPDATA%\PT Calendar Manager`. Szczegółowe informacje zawiera Polityka prywatności.

Wylogowanie usuwa lokalny token. Odwołanie dostępu jest możliwe również w ustawieniach bezpieczeństwa konta Google.

## 13. Świadomie nieobsługiwane funkcje

Pierwsze wydanie nie obejmuje:

- dodawania i edycji uczestników;
- tworzenia Google Meet;
- indywidualnych przypomnień;
- ręcznego wyboru strefy czasowej;
- ustawienia „wolny” lub „zajęty”;
- niestandardowych reguł cykliczności.

Do tych operacji służy polecenie otwierające wydarzenie w Kalendarzu Google.
