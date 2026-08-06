# PT Calendar Manager 0.15.5 — zmiany

## Natywna lista kalendarzy Windows

Sekcja wyboru kalendarzy nie korzysta już z `wx.CheckListBox` ani z własnej nakładki MSAA. Zastąpiła ją natywna kontrolka `wx.ListCtrl` w widoku jednego wiersza na kalendarz, z polami wyboru włączonymi przez `EnableCheckBoxes(True)`.

Dzięki temu:

- JAWS otrzymuje standardową nawigację po wierszach listy;
- Narrator otrzymuje oddzielny stan bieżącego wiersza i natywny stan pola wyboru;
- NVDA nadal odczytuje rzeczywiste zaznaczenie;
- fokus po wejściu na listę zaczyna się zawsze na pierwszym kalendarzu, niezależnie od tego, które kalendarze są zaznaczone;
- własny obiekt `wx.Accessible` nie zastępuje już systemowego dostawcy dostępności tej kontrolki.

Wygląd okna, instrukcja nad listą oraz obsługa strzałkami i Spacją pozostają bez zmian.
