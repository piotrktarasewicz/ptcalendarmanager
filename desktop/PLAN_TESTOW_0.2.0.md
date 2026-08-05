# Plan testów PT Calendar Manager 0.2.0

Wykonaj najpierw test z NVDA, później z JAWS-em i Narratorem.

## 1. Start i migracja

- uruchom aplikację;
- sprawdź, czy fokus trafia na listę dni;
- sprawdź komunikat na pasku stanu;
- jeżeli aplikacja znalazła token dodatku NVDA, powinna samodzielnie rozpocząć
  pobieranie danych;
- sprawdź, czy dodatek NVDA nadal działa po uruchomieniu aplikacji.

## 2. Konto Google

- sprawdź nazwę przycisku `Zaloguj do Google` albo `Wyloguj z Google`;
- jeżeli potrzebne jest logowanie, przejdź pełny proces w przeglądarce;
- po powrocie sprawdź, czy aplikacja odzyskała fokus i pobrała dane;
- nie testuj jeszcze wylogowania, dopóki nie potwierdzisz poprawnego odczytu.

## 3. Wybór kalendarzy

- otwórz `Wybierz kalendarze`;
- sprawdź nazwy pól wyboru;
- zaznacz kilka kalendarzy;
- zapisz i sprawdź, czy lista dni została odświeżona;
- upewnij się, że ustawienie pozostaje po ponownym uruchomieniu aplikacji.

## 4. Prawdziwe wydarzenia

- wybierz dzień bez wydarzeń;
- wybierz dzień z jednym wydarzeniem;
- wybierz dzień z kilkoma wydarzeniami;
- sprawdź wydarzenie całodniowe;
- sprawdź wydarzenie wielodniowe;
- sprawdź wydarzenie godzinowe;
- otwórz szczegóły Enterem.

## 5. Nawigacja między miesiącami

- użyj przycisków oraz Alt+strzałek;
- sprawdź automatyczne pobieranie nowego miesiąca;
- wróć do dzisiaj przez Ctrl+D;
- użyj Ctrl+G do przejścia do konkretnej daty.

## 6. Wyszukiwanie

Wersja 0.2.0 szuka tylko w wydarzeniach aktualnie pobranego miesiąca.

- naciśnij Ctrl+F;
- wyszukaj fragment tytułu;
- wybierz wynik;
- sprawdź powrót na właściwy dzień i wydarzenie.

## 7. Co zgłosić

- dokładny tekst ostatniego komunikatu przed błędem;
- czy aplikacja się zawiesiła, czy tylko nie odświeżyła listy;
- gdzie znajdował się fokus;
- czy problem wystąpił z każdym czytnikiem;
- zawartość pliku `%APPDATA%\PT Calendar Manager\last_error.txt`, jeżeli powstał.
