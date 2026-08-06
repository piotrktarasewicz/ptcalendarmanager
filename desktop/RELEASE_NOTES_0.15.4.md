# PT Calendar Manager 0.15.4 — zmiany

## Poprawione odczytywanie zaznaczenia kalendarzy

Lista kalendarzy pozostaje jednym kompaktowym polem `wx.CheckListBox`, ale aplikacja nie polega już wyłącznie na domyślnej dostępności tej kontrolki w Windows.

Każdy element listy udostępnia teraz czytnikom ekranu jawny stan MSAA:

- zaznaczony albo niezaznaczony;
- bieżący element listy;
- element posiadający fokus.

Po naciśnięciu Spacji aplikacja wysyła do czytnika zdarzenie zmiany stanu właściwego elementu. NVDA, JAWS i Narrator powinny dzięki temu od razu poinformować o zaznaczeniu albo odznaczeniu kalendarza.

Początkowe zaznaczenia są ustawiane jednym wywołaniem na podstawie zapisanych identyfikatorów kalendarzy. Zaznaczenie kursora listy nie jest już traktowane jako zaznaczenie checkboxa. Rozwiązuje to przypadek, w którym Narrator błędnie informował, że kalendarz główny jest zaznaczony.

Układ wizualny, rozmiar okna i model klawiatury nie zostały zmienione.
