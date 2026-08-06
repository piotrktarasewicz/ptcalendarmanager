# Plan testów PT Calendar Manager 0.15.2

## Cel

Sprawdzenie semantycznej grupy wyboru kalendarzy bez dodatkowego pola tekstowego i bez powiększenia okna Ustawień.

## Test w NVDA, JAWS-ie i Narratorze

1. Otwórz Ustawienia skrótem `Ctrl+,`.
2. Przejdź Tabulatorem z pola „Język aplikacji” do pierwszego kalendarza.
3. Czytnik powinien przekazać kontekst grupy „Wybór kalendarzy” oraz instrukcję: „Zaznacz kalendarze, których wydarzenia mają być wyświetlane.”
4. Następnie powinien odczytać nazwę i stan pierwszego kalendarza.
5. Przy kolejnych kalendarzach instrukcja nie powinna być powtarzana.
6. W oknie nie powinno być dodatkowego pola tylko do odczytu.
7. Rozmiar okna powinien odpowiadać wersji 0.15.0 i nie powinien być zwiększony przez instrukcję.
8. Sprawdź zmianę zaznaczenia spacją, zapis i anulowanie ustawień.

## Regresja

Sprawdź otwieranie menu głównego lewym Altem, oba menu kontekstowe, logowanie, odświeżanie oraz zmianę języka z ponownym uruchomieniem.
