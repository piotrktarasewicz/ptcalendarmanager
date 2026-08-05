# Plan testów PT Calendar Manager 0.3.1

Wykonaj test osobno z NVDA, JAWS-em i Narratorem.

1. Uruchom aplikację.
2. Naciśnij `Ctrl+N`.
3. Przechodź Tabulatorem po formularzu.
4. Sprawdź kolejno nazwy:

   - Tytuł wydarzenia;
   - Kalendarz docelowy;
   - Data rozpoczęcia, DD.MM.RRRR;
   - Wydarzenie całodniowe;
   - Godzina rozpoczęcia, GG:MM;
   - Data zakończenia włącznie, DD.MM.RRRR;
   - Godzina zakończenia, GG:MM;
   - Lokalizacja;
   - Opis wydarzenia;
   - Utwórz wydarzenie;
   - Anuluj.

5. Sprawdź, czy wraz z nazwą odczytywana jest rola i bieżąca wartość.
6. Zaznacz wydarzenie całodniowe i sprawdź stan pól godzin.
7. Utwórz jedno wydarzenie testowe, aby potwierdzić brak regresji zapisu.

Zwróć uwagę, czy któryś czytnik:

- nadal mówi wyłącznie „pole edycyjne”;
- odczytuje nazwę dwa razy;
- pomija wartość;
- nie informuje o stanie nieaktywnym.
