# Architektura GCM by Piotrek

## Obecny podział

### `gcm_core`

Niezależna od czytnika ekranu i wxPython warstwa odpowiedzialna za:

- ścieżki danych użytkownika;
- migrację kopii plików z dodatku NVDA;
- ustawienia aplikacji;
- OAuth i token Google;
- pobieranie kalendarzy i wydarzeń;
- model wydarzenia oraz obliczanie wystąpień na poszczególnych dniach.

### `gcm_desktop`

Warstwa aplikacji Windows:

- główne okno wxPython;
- listy dni i wydarzeń;
- standardowe przyciski i okna dialogowe;
- zarządzanie fokusem;
- wykonywanie operacji sieciowych w wątku roboczym;
- komunikaty statusu i błędów.

## Docelowy wspólny rdzeń z dodatkiem NVDA

Po ustabilizowaniu odczytu prawdziwych danych funkcje tworzenia, aktualizacji i
usuwania wydarzeń zostaną przeniesione do `gcm_core`. Następnie dodatek NVDA
będzie mógł wywoływać ten sam rdzeń przez cienką warstwę `gcm_nvda`, a aplikacja
przez `gcm_desktop`.

Nie zmieniamy teraz działającego dodatku 1.0.4. Najpierw weryfikujemy rdzeń w
samodzielnej aplikacji, aby nie ryzykować regresji w wersji publicznej.
