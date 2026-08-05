# Plan testów PT Calendar Manager 0.11.2

## 1. Start z wygasłym lub przeniesionym tokenem

1. Uruchom aplikację na drugim komputerze albo z wcześniej zapisanym tokenem.
2. Główne okno powinno reagować natychmiast na Tabulator i skróty.
3. Ewentualne odświeżanie tokenu powinno odbywać się w tle.
4. Ustawienia i Pomoc muszą pozostać dostępne.

## 2. Ustawienia bez Google

1. Odłącz Internet albo uruchom GCM bez tokenu.
2. Otwórz Ustawienia przyciskiem, `Ctrl+,` i `Ctrl+K`.
3. Zmiana języka powinna być dostępna.
4. Brak listy kalendarzy nie może blokować ani zamykać okna.

## 3. Brak client_secret.json

1. Tymczasowo usuń lub przenieś `client_secret.json` z katalogu danych GCM.
2. Wybierz Zaloguj do Google.
3. Program powinien wyjaśnić, do czego potrzebny jest plik i skąd można go skopiować.
4. Po wybraniu OK powinno otworzyć się modalne okno wyboru pliku.
5. Anulowanie powinno zostać odnotowane na pasku stanu.

## 4. Limit czasu Google

1. Zablokuj połączenie do Google lub odłącz sieć w trakcie pobierania.
2. Ustawienia powinny przez cały czas działać.
3. Po najwyżej 45 sekundach pozostałe kontrolki powinny zostać odblokowane.
4. Powinien pojawić się dostępny komunikat o przekroczeniu czasu.

## 5. Regresja

Po przywróceniu połączenia sprawdź logowanie, pobranie kalendarzy, odczyt wydarzeń, tworzenie, edycję, usuwanie, wyszukiwanie, link Google i link spotkania w NVDA, JAWS-ie i Narratorze.
