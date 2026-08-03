# Plan testów GCM by Piotrek 0.9.0

Test wykonaj osobno z NVDA, JAWS-em 2025 i Narratorem.

Najbezpieczniej przygotować osobny kalendarz testowy i krótkie cykle z datą
zakończenia, aby łatwo zweryfikować wynik w oficjalnym Kalendarzu Google.

## 1. Formularz dodawania

1. Naciśnij `Ctrl+N`.
2. Przejdź Tabulatorem do pola „Powtarzanie wydarzenia”.
3. Sprawdź kolejno opcje:
   - Nie powtarza się;
   - Codziennie;
   - Co tydzień;
   - Co miesiąc;
   - Co 3 miesiące;
   - Co 6 miesięcy;
   - Co rok.
4. Dla wydarzenia jednorazowego pole końca cyklu i pole „Bez daty zakończenia”
   powinny być nieaktywne.
5. Po wybraniu cyklu pole końca powinno być aktywne.
6. Po zaznaczeniu „Bez daty zakończenia cyklu” pole daty powinno zostać
   wyłączone i pominięte przy przechodzeniu Tabulatorem.

## 2. Tworzenie wszystkich cykli

Utwórz po jednym krótkim wydarzeniu każdego rodzaju. Po każdej operacji sprawdź:

- dokładny komunikat potwierdzający;
- datę końca cyklu;
- wystąpienia w GCM po odświeżeniu;
- zgodność z oficjalnym Kalendarzem Google.

Dla „Co 3 miesiące” i „Co 6 miesięcy” sprawdź co najmniej dwa wystąpienia.

## 3. Cykl bez końca

Utwórz cykl z zaznaczonym polem „Bez daty zakończenia cyklu”. Sprawdź, czy
Google nie ustawił daty końca i czy komunikat GCM mówi o cyklu bezterminowym.

## 4. Walidacja

Sprawdź następujące błędy:

- data końca cyklu wcześniejsza niż początek;
- nieprawidłowy format daty;
- brak tytułu;
- zakończenie wydarzenia wcześniejsze niż początek.

Po błędzie fokus powinien wrócić do właściwego pola albo pozostać w formularzu.

## 5. Zamiana wydarzenia jednorazowego w cykl

1. Utwórz zwykłe wydarzenie.
2. Wybierz je i naciśnij `Ctrl+E`.
3. Ustaw powtarzanie, na przykład „Co miesiąc”.
4. Zapisz i potwierdź.
5. Sprawdź, czy wydarzenie stało się cyklem i czy GCM pozostał na właściwym dniu.

## 6. Edycja pojedynczego wystąpienia

1. Wybierz środkowe wystąpienie cyklu.
2. Naciśnij `Ctrl+E`.
3. Wybierz „Edytuj tylko to wystąpienie”.
4. Sprawdź, czy pole powtarzania jest wyłączone.
5. Zmień tytuł albo godzinę.
6. Potwierdź, że zmienił się tylko wybrany termin.

## 7. Edycja całego cyklu

1. Wybierz wystąpienie prostego cyklu.
2. Naciśnij `Ctrl+E` i wybierz „Edytuj cały cykl”.
3. Sprawdź, czy formularz pokazuje datę początku całej serii, a nie tylko
   zaznaczonego wystąpienia.
4. Zmień częstotliwość, na przykład z miesięcznej na kwartalną.
5. Zmień datę końca.
6. Potwierdź wynik w GCM i Google.

## 8. Zamiana cyklu w wydarzenie jednorazowe

W edycji całego cyklu wybierz „Nie powtarza się”. Potwierdzenie musi wyraźnie
powiedzieć, że seria zostanie zamieniona w jedno wydarzenie w dacie jej
początku. Najpierw sprawdź anulowanie, a następnie wykonaj operację na cyklu
testowym.

## 9. Złożony cykl utworzony poza GCM

W oficjalnym Kalendarzu Google utwórz serię powtarzaną na przykład w poniedziałki
i środy. W GCM:

- edycja pojedynczego wystąpienia powinna działać;
- próba edycji całego cyklu powinna zostać zablokowana czytelnym komunikatem;
- istniejąca reguła w Google nie może zostać zmieniona ani uproszczona.

## 10. Regresja

Sprawdź odczyt, wyszukiwanie, dodawanie jednorazowe, edycję, wszystkie trzy
zakresy usuwania cyklu, pomoc, skróty i wybór kalendarzy.
