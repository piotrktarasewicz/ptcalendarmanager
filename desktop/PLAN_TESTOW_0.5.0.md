# Plan testów GCM by Piotrek 0.5.0

Test wykonaj osobno z NVDA, JAWS-em i Narratorem.

## 1. Anulowanie operacji

1. Utwórz wydarzenie testowe.
2. Zaznacz je i naciśnij `Delete`.
3. Sprawdź, czy okno podaje tytuł, kalendarz i termin.
4. Naciśnij Enter bez zmieniania wyboru.
5. Ponieważ domyślne jest `Nie`, wydarzenie powinno pozostać.

## 2. Usunięcie zwykłego wydarzenia

1. Ponownie naciśnij `Delete`.
2. Wybierz `Tak`.
3. Sprawdź komunikat o usunięciu.
4. Po odświeżeniu fokus powinien znaleźć się na liście wydarzeń tego dnia.
5. Potwierdź w oficjalnym Kalendarzu Google, że wydarzenie zniknęło.

## 3. Wydarzenie z uczestnikiem

1. Przygotuj wydarzenie testowe z uczestnikiem, którego możesz bezpiecznie
   powiadomić.
2. Sprawdź, czy potwierdzenie zapowiada wysłanie informacji o anulowaniu.
3. Usuń wydarzenie i zweryfikuj wynik w Google.

## 4. Pojedyncze wystąpienie cyklu

1. Utwórz krótką serię testową w Kalendarzu Google.
2. W GCM wybierz jedno wystąpienie i naciśnij `Delete`.
3. Sprawdź ostrzeżenie, że usunięty zostanie tylko wybrany termin.
4. Potwierdź operację.
5. Sprawdź, czy pozostałe terminy serii nadal istnieją.

## 5. Kalendarz tylko do odczytu

Jeżeli masz taki kalendarz, spróbuj usunąć jego wydarzenie. Program powinien
odmówić przed wysłaniem żądania do Google.

## 6. Obsługa klawiatury i czytników

Sprawdź:

- przycisk `Usuń`;
- skrót `Delete`;
- domyślny wybór `Nie`;
- odczyt ostrzeżeń;
- fokus po anulowaniu;
- fokus po prawidłowym usunięciu;
- zachowanie pustej listy, gdy usunięto ostatnie wydarzenie dnia.
