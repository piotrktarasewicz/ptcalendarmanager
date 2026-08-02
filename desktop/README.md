# GCM by Piotrek — prototyp dostępności wxPython

To jest pierwszy, całkowicie niezależny od NVDA prototyp interfejsu aplikacji
GCM by Piotrek.

## Cel tej wersji

Ta wersja nie łączy się jeszcze z Kalendarzem Google. Jej jedynym celem jest
sprawdzenie, czy prosty interfejs zbudowany ze standardowych kontrolek wxPython
jest wygodny i poprawnie odczytywany przez:

- NVDA,
- JAWS,
- Narrator systemu Windows,
- inne czytniki ekranu.

Prototyp zawiera:

- listę wszystkich dni wybranego miesiąca,
- listę wydarzeń dla zaznaczonego dnia,
- przechodzenie do poprzedniego i następnego miesiąca,
- przejście do konkretnej daty,
- wyszukiwanie przykładowych wydarzeń,
- dodawanie, edycję i usuwanie wydarzeń w pamięci,
- szczegóły wydarzenia,
- przycisk odświeżania,
- skróty klawiaturowe.

Dane są przykładowe. Po zamknięciu aplikacji wszystkie zmiany przepadają.

## Dlaczego nie ma graficznej siatki kalendarza

Dni miesiąca są pokazane jako zwykła lista. Jest to celowe. Standardowe listy,
przyciski, pola tekstowe i pola wyboru mają znacznie większą szansę działać
poprawnie z wieloma czytnikami ekranu niż własnoręcznie rysowane kafelki lub
kontrolki kalendarza.

## Zalecane środowisko

- Windows 10 albo Windows 11,
- 64-bitowy Python 3.12,
- wxPython 4.2.5.

## Najprostsze uruchomienie

1. Rozpakuj cały katalog.
2. Uruchom plik `uruchom_prototyp.bat`.
3. Przy pierwszym uruchomieniu zostanie utworzone środowisko `.venv` i pobrany
   wxPython.
4. Po instalacji otworzy się aplikacja.

Możesz też uruchomić ręcznie:

```bat
py -3.12 -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
set PYTHONPATH=%CD%\src
python launcher.py
```

## Budowanie pliku EXE

Na Windows uruchom:

```bat
zbuduj_exe.bat
```

Po poprawnym zbudowaniu aplikacja znajdzie się w katalogu:

```text
dist\GCM by Piotrek - prototyp\GCM by Piotrek - prototyp.exe
```

Zastosowany jest wariant katalogowy, a nie pojedynczy plik EXE. Na pierwszym
etapie jest on łatwiejszy do diagnozowania i zwykle uruchamia się szybciej.

## Skróty

- `Ctrl+N` — dodaj wydarzenie,
- `Ctrl+E` — edytuj zaznaczone wydarzenie,
- `Delete` — usuń zaznaczone wydarzenie,
- `Ctrl+F` — wyszukaj,
- `Ctrl+G` — przejdź do daty,
- `Ctrl+D` — przejdź do dzisiaj,
- `Alt+Strzałka w lewo` — poprzedni miesiąc,
- `Alt+Strzałka w prawo` — następny miesiąc,
- `F5` — odśwież,
- `Enter` na liście dni — przejdź do listy wydarzeń,
- `Enter` na liście wydarzeń — pokaż szczegóły,
- `Alt+F4` — zamknij aplikację.

## Ważne

Nie oceniamy jeszcze wyglądu ani integracji z Google. Najpierw sprawdzamy:

- czy wszystkie kontrolki mają poprawne nazwy,
- czy listy są odczytywane,
- czy kolejność Tabulatora jest logiczna,
- czy fokus trafia we właściwe miejsca,
- czy formularze są wygodne,
- czy aplikacja działa podobnie z NVDA, JAWS-em i Narratorem.

Dokładny scenariusz znajduje się w pliku `PLAN_TESTOW_DOSTEPNOSCI.md`.
