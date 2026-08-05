# PT Calendar Manager — dokumentacja użytkownika

Wersja 0.14.0

## 1. Przeznaczenie

PT Calendar Manager jest dostępną aplikacją dla Windows, która ułatwia codzienne zarządzanie Kalendarzem Google bez konieczności korzystania z pełnego interfejsu strony internetowej. Aplikacja nie ma zastępować wszystkich funkcji Kalendarza Google. Bardziej zaawansowane operacje można otworzyć bezpośrednio w oficjalnym interfejsie Google.

Interfejs jest przygotowany do obsługi klawiaturą i testowany z NVDA, JAWS-em oraz Narratorem.

## 2. Pierwsze uruchomienie i logowanie

Po uruchomieniu główne okno działa także bez logowania. Ustawienia języka i informacje o programie są dostępne offline.

Aby połączyć konto Google:

1. Wybierz przycisk „Zaloguj do Google” albo naciśnij `Ctrl+L`.
2. Jeśli program nie znajdzie konfiguracji OAuth, wskaż plik `client_secret.json`.
3. Zaloguj się w otwartej przeglądarce i zaakceptuj wymagane uprawnienia.
4. Wróć do PT Calendar Manager.

Token logowania jest zapisywany lokalnie jako `token.dat` i szyfrowany mechanizmem Windows DPAPI dla bieżącego użytkownika Windows.

## 3. Główne okno

W górnej części znajdują się:

- Zaloguj lub Wyloguj z Google;
- Ustawienia;
- Pomoc i skróty.

Poniżej znajdują się przyciski nawigacji po miesiącach i podstawowe operacje. Lewa lista zawiera dni bieżącego miesiąca, a prawa — wydarzenia zaznaczonego dnia.

`Enter` na liście dni przenosi fokus na listę wydarzeń. `Enter` na wydarzeniu otwiera szczegóły.

## 4. Ustawienia

Ustawienia otwiera `Ctrl+,` albo `Ctrl+K`.

Można w nich:

- wybrać język: Automatycznie, Polski albo English;
- wybrać kalendarze używane przez aplikację;
- otworzyć okno „O programie”.

Po zmianie faktycznego języka program proponuje natychmiastowe ponowne uruchomienie. Zmiana samych kalendarzy nie wymaga restartu.

Okno „O programie” zawiera numer wersji, dane autora, informację o niezależności produktu, politykę prywatności i informacje prawne.

## 5. Dodawanie i edycja wydarzeń

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

## 6. Usuwanie

Usuwanie zawsze wymaga potwierdzenia. Dla wydarzenia cyklicznego dostępne są zakresy:

- tylko to wystąpienie;
- to i wszystkie kolejne;
- cały cykl.

Domyślnie wybierana jest najbezpieczniejsza operacja dotycząca pojedynczego wystąpienia.

## 7. Wyszukiwanie

Wyszukiwanie obejmuje wybrane kalendarze, podany tekst oraz datę początkową i końcową włącznie. Po wybraniu wyniku aplikacja przechodzi do odpowiedniego dnia i ustawia fokus na wydarzeniu.

## 8. Otwieranie w Google i link spotkania

„Otwórz w Google” otwiera zaznaczone wydarzenie w oficjalnym interfejsie Kalendarza Google.

Jeżeli wydarzenie zawiera internetowy link spotkania dodany poza aplikacją, polecenie „Link spotkania” pozwala go otworzyć albo skopiować. PT Calendar Manager nie tworzy nowych spotkań Google Meet.

## 9. Skróty aplikacji

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
- `Ctrl+J` — otwórz lub skopiuj link spotkania.

Przyciski mają także standardowe klawisze dostępu Windows `Alt+litera`, odczytywane przez czytniki ekranu.

## 10. Dane użytkownika

Dane lokalne znajdują się w `%APPDATA%\PT Calendar Manager`. Szczegółowe informacje zawiera Polityka prywatności.

Wylogowanie usuwa lokalny token. Odwołanie dostępu jest możliwe również w ustawieniach bezpieczeństwa konta Google.

## 11. Świadomie nieobsługiwane funkcje

Pierwsze wydanie nie obejmuje:

- dodawania i edycji uczestników;
- tworzenia Google Meet;
- indywidualnych przypomnień;
- ręcznego wyboru strefy czasowej;
- ustawienia „wolny” lub „zajęty”;
- niestandardowych reguł cykliczności.

Do tych operacji służy polecenie otwierające wydarzenie w Kalendarzu Google.
