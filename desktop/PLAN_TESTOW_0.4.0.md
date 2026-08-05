# Plan testów PT Calendar Manager 0.4.0

Test edycji wykonaj najpierw na zwykłym wydarzeniu utworzonym specjalnie do
testów. Sprawdź osobno NVDA, JAWS i Narratora.

## Test podstawowy

1. Utwórz w GCM wydarzenie `Test edycji GCM 0.4.0`.
2. Zaznacz je na liście wydarzeń.
3. Naciśnij `Ctrl+E` albo przycisk `Edytuj`.
4. Sprawdź, czy formularz zawiera dotychczasowe:
   - tytuł;
   - kalendarz;
   - daty i godziny;
   - ustawienie wydarzenia całodniowego;
   - lokalizację;
   - opis.
5. Przejdź po formularzu Tabulatorem i sprawdź etykiety wszystkich pól.
6. Zmień tytuł, termin, lokalizację i opis.
7. Wyczyść lokalizację albo opis, aby sprawdzić możliwość usuwania zawartości.
8. Wybierz `Zapisz zmiany`, przeczytaj podsumowanie i potwierdź.
9. Sprawdź, czy aplikacja:
   - pokazuje komunikat o sukcesie;
   - przechodzi do nowej daty wydarzenia;
   - ustawia fokus na zmodyfikowanym wydarzeniu.
10. Sprawdź to samo wydarzenie w oficjalnym Kalendarzu Google.

## Rodzaje terminów

Przetestuj kolejno:

- wydarzenie godzinowe w jednym dniu;
- wydarzenie godzinowe przechodzące przez północ;
- wydarzenie jednodniowe całodniowe;
- wydarzenie wielodniowe całodniowe;
- zmianę wydarzenia godzinowego na całodniowe i odwrotnie.

## Ochrona danych

- Otwórz edycję i wybierz `Anuluj`: nic nie może zostać zapisane.
- Otwórz edycję i niczego nie zmieniaj: aplikacja powinna zgłosić brak zmian.
- Spróbuj edytować wydarzenie z kalendarza tylko do odczytu: operacja powinna być
  zablokowana.
- Przy wydarzeniu cyklicznym aplikacja powinna ostrzec, że edytowana jest tylko
  wybrana instancja.
- Przy wydarzeniu z uczestnikami aplikacja powinna uprzedzić o wysłaniu
  aktualizacji uczestnikom.
- Specjalne typy wydarzeń powinny zostać zablokowane z czytelnym wyjaśnieniem.

Usuwanie pozostaje w tej wersji wyłączone.
