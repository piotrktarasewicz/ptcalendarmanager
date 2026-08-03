# GCM by Piotrek 0.6.0 — pełne usuwanie wydarzeń cyklicznych

GCM by Piotrek jest dostępnym klientem Kalendarza Google dla Windows,
testowanym z NVDA, JAWS-em i Narratorem.

Wersja 0.6.0 rozszerza usuwanie wydarzeń cyklicznych o trzy zakresy:

1. Usuń tylko to wystąpienie.
2. Usuń to i wszystkie kolejne wystąpienia.
3. Usuń cały cykl.

## Bezpieczny wybór

Po naciśnięciu `Delete` na wydarzeniu cyklicznym pojawia się standardowe
okno wyboru. Domyślnie zaznaczony jest najbezpieczniejszy wariant:
`Usuń tylko to wystąpienie`.

Po wyborze zakresu pojawia się osobne potwierdzenie. Domyślną odpowiedzią
jest `Nie`.

## Tylko to wystąpienie

Google otrzymuje identyfikator wybranego wystąpienia. Pozostałe terminy
serii nie są zmieniane.

## To i kolejne

Aplikacja pobiera wydarzenie nadrzędne i kończy jego regułę RRULE tuż
przed pierwotnym czasem rozpoczęcia wybranego wystąpienia. Nie usuwa
kolejnych terminów jeden po drugim i nie tworzy wielu wyjątków.

Jeżeli wybrane wystąpienie jest pierwszym terminem serii, operacja ma
taki sam skutek jak usunięcie całego cyklu.

Program wykorzystuje `originalStartTime`, a nie aktualny czas początku.
Dzięki temu prawidłowo rozpoznaje pozycję wystąpienia nawet po ręcznym
przesunięciu pojedynczego terminu.

## Cały cykl

Aplikacja usuwa wydarzenie nadrzędne na podstawie `recurringEventId`.
Znikają wystąpienia wcześniejsze, zaznaczone i późniejsze.

## Uczestnicy

Jeśli wydarzenie ma uczestników, aplikacja ostrzega przed operacją,
a Google otrzymuje polecenie wysłania informacji o anulowaniu.

## Po operacji

Aplikacja pozostaje na wybranym dniu, pobiera dane ponownie z Google
i ustawia fokus na liście wydarzeń tego dnia.

## Uruchomienie

Rozpakuj archiwum do nowego katalogu i uruchom `uruchom_gcm.bat`.

Token i ustawienia pozostają w `%APPDATA%\GCM by Piotrek`.
