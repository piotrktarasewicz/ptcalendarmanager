# GCM by Piotrek 0.9.0 — podstawowe wydarzenia cykliczne

GCM by Piotrek jest dostępnym klientem Kalendarza Google dla Windows,
testowanym z NVDA, JAWS-em i Narratorem.

## Nowości w wersji 0.9.0

Podczas dodawania wydarzenia można wybrać:

- Nie powtarza się;
- Codziennie;
- Co tydzień;
- Co miesiąc;
- Co 3 miesiące;
- Co 6 miesięcy;
- Co rok.

Cykl może działać bez daty zakończenia albo kończyć się we wskazanym dniu.
Data zakończenia cyklu jest wliczana do zakresu.

Przy nowym wydarzeniu cyklicznym aplikacja domyślnie proponuje datę końcową
oddaloną o rok od daty rozpoczęcia. Zaznaczenie pola „Bez daty zakończenia
cyklu” wyłącza to ograniczenie.

## Edycja

Zwykłe wydarzenie można zamienić w jeden z obsługiwanych prostych cykli.

Przy edycji wystąpienia istniejącego cyklu aplikacja pyta, czy zmiana ma objąć:

1. tylko zaznaczone wystąpienie;
2. cały cykl.

Edycja pojedynczego wystąpienia nie pozwala zmienić reguły powtarzania.
Edycja całego cyklu pozwala zmienić jego termin oraz jeden z podstawowych
rodzajów powtarzania.

Wybranie „Nie powtarza się” podczas edycji całego cyklu zamienia serię w jedno
wydarzenie w dacie początku serii. Aplikacja wyraźnie ostrzega o tym przed
zapisaniem.

## Ochrona złożonych cykli

GCM rozpoznaje wyłącznie proste reguły należące do obsługiwanego zestawu.
Nie upraszcza automatycznie serii zawierających między innymi:

- kilka dni tygodnia;
- nietypowy odstęp;
- liczbę wystąpień `COUNT`;
- reguły pozycyjne;
- dodatkowe `RDATE` albo `EXDATE`.

Taką serię można nadal odczytać, edytować jako pojedyncze wystąpienie i usuwać
zgodnie z dotychczasowym zakresem. Edycja całego cyklu wymaga oficjalnego
Kalendarza Google.

## Miesiące bez wybranego dnia

Dla cykli miesięcznych, kwartalnych i półrocznych rozpoczętych 29., 30. albo
31. dnia miesiąca Google może pominąć miesiąc, w którym taki dzień nie
występuje. GCM nie próbuje samodzielnie przesuwać terminu na ostatni dzień
miesiąca.

## Strefa czasowa

Użytkownik nie wybiera ręcznie strefy w formularzu. GCM korzysta ze strefy
wybranego kalendarza. Pakiet `tzdata` został dodany, aby obliczenia daty końca
cyklu działały prawidłowo również w systemie Windows.

## Uruchomienie

Rozpakuj archiwum do nowego katalogu i uruchom `uruchom_gcm.bat`.

Token i ustawienia pozostają w `%APPDATA%\GCM by Piotrek`.
