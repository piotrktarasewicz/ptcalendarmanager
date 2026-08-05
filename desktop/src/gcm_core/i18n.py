from __future__ import annotations

import ctypes
import locale
import os
import sys
from typing import Final

LANGUAGE_AUTO: Final = "auto"
LANGUAGE_POLISH: Final = "pl"
LANGUAGE_ENGLISH: Final = "en"
SUPPORTED_LANGUAGE_PREFERENCES: Final = (
    LANGUAGE_AUTO,
    LANGUAGE_POLISH,
    LANGUAGE_ENGLISH,
)

_current_language = LANGUAGE_ENGLISH
_current_preference = LANGUAGE_AUTO

MONTHS_GENITIVE = {
    "pl": (
        "", "stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca",
        "lipca", "sierpnia", "września", "października", "listopada", "grudnia",
    ),
    "en": (
        "", "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ),
}
MONTHS_NOMINATIVE = {
    "pl": (
        "", "styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec",
        "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień",
    ),
    "en": MONTHS_GENITIVE["en"],
}
WEEKDAYS = {
    "pl": (
        "poniedziałek", "wtorek", "środa", "czwartek", "piątek", "sobota", "niedziela",
    ),
    "en": (
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
    ),
}

# Polish source strings are stable message identifiers, in the same spirit as
# gettext msgid values. English translations live in one place and are checked
# by automated tests.
ENGLISH_TRANSLATIONS: dict[str, str] = {
    # Generic and language settings.
    "Automatycznie, zgodnie z językiem systemu": "Automatic, use the system language",
    "Polski": "Polish",
    "Angielski": "English",
    "Język aplikacji": "Application language",
    "Ustawienia": "Settings",
    "Ustawienia aplikacji": "Application settings",
    "Język zostanie zmieniony po ponownym uruchomieniu aplikacji.": "The language will change after the application is restarted.",
    "Język aplikacji zostanie zmieniony. Aby zastosować nowe ustawienie, GCM musi zostać uruchomiony ponownie.\n\nWybierz „Uruchom ponownie teraz”, aby zamknąć i ponownie uruchomić aplikację, albo „Później”, aby zastosować zmianę przy następnym uruchomieniu.": "The application language has been changed. GCM must be restarted to apply the new setting.\n\nChoose ‘Restart now’ to close and restart the application, or ‘Later’ to apply the change the next time GCM starts.",
    "Ponowne uruchomienie GCM": "Restart GCM",
    "Uruchom ponownie teraz": "Restart now",
    "Zamyka bieżącą instancję i uruchamia GCM ponownie w wybranym języku.": "Closes the current instance and restarts GCM in the selected language.",
    "Później": "Later",
    "Pozostawia aplikację otwartą. Nowy język zostanie zastosowany przy następnym uruchomieniu.": "Keeps the application open. The new language will be applied the next time GCM starts.",
    "Zmiana języka zostanie zastosowana przy następnym uruchomieniu.": "The language change will be applied the next time GCM starts.",
    "Nie udało się ponownie uruchomić aplikacji. Ustawienie języka zostało zapisane i będzie użyte przy następnym ręcznym uruchomieniu.\n\n{error}": "GCM could not be restarted. The language setting has been saved and will be used the next time you start the application manually.\n\n{error}",
    "Nie można ponownie uruchomić GCM": "Could not restart GCM",
    "Ustawienia zostały zapisane.": "Settings have been saved.",
    "Wybór kalendarzy": "Calendar selection",
    "Kalendarze": "Calendars",
    "Zaznacz kalendarze, których wydarzenia mają być pokazywane.": "Select the calendars whose events should be shown.",
    "Zaloguj się do Google, aby wybrać kalendarze. Ustawienie języka jest dostępne bez logowania.": "Sign in to Google to select calendars. The language setting is available without signing in.",
    "Zaznacz co najmniej jeden kalendarz.": "Select at least one calendar.",
    "kalendarz główny": "primary calendar",
    "Bez nazwy": "Untitled calendar",

    # Main window and controls.
    "GCM by Piotrek 0.11.1 — ponowne uruchamianie po zmianie języka": "GCM by Piotrek 0.11.1 — restart after changing language",
    "Główne okno GCM by Piotrek": "GCM by Piotrek main window",
    "Za&loguj do Google": "Sign in (&L)",
    "Wy&loguj z Google": "Sign out (&L)",
    "Us&tawienia": "Se&ttings",
    "Pomoc i skróty (&H)": "&Help and shortcuts",
    "Konto Google: sprawdzanie stanu": "Google account: checking status",
    "&Poprzedni miesiąc": "&Previous month",
    "&Dzisiaj": "Toda&y",
    "Następny &miesiąc": "&Next month",
    "Przejdź do daty (&G)": "&Go to date",
    "Wy&szukaj": "&Search",
    "Dodaj wydarze&nie": "&Add event",
    "&Odśwież": "&Refresh",
    "Dni miesiąca": "Days of the month",
    "Wydarzenia wybranego dnia": "Events on the selected day",
    "Pokaż s&zczegóły": "&View details",
    "&Edytuj": "&Edit",
    "&Usuń": "&Delete",
    "Otwórz &w Google": "&Open in Google",
    "Link spotkan&ia": "&Meeting link",
    "Stan aplikacji": "Application status",
    "Zaloguj do Google": "Sign in to Google",
    "Wyloguj z Google": "Sign out of Google",
    "Łączy konto Google albo wylogowuje bieżące konto.": "Signs in to Google or signs out the current account.",
    "Ustawienia aplikacji i wybór kalendarzy": "Application settings and calendar selection",
    "Otwiera ustawienia języka i kalendarzy.": "Opens language and calendar settings.",
    "Pomoc i skróty": "Help and shortcuts",
    "Otwiera opis aplikacji i pełną listę skrótów.": "Opens the application guide and complete shortcut list.",
    "Poprzedni miesiąc": "Previous month",
    "Przechodzi do poprzedniego miesiąca.": "Moves to the previous month.",
    "Alt+Strzałka w lewo": "Alt+Left Arrow",
    "Dzisiaj": "Today",
    "Przechodzi do dzisiejszej daty.": "Moves to today's date.",
    "Następny miesiąc": "Next month",
    "Przechodzi do następnego miesiąca.": "Moves to the next month.",
    "Alt+Strzałka w prawo": "Alt+Right Arrow",
    "Przejdź do daty": "Go to date",
    "Otwiera pole do podania konkretnej daty.": "Opens a field for entering a specific date.",
    "Wyszukaj": "Search",
    "Otwiera wyszukiwanie wydarzeń w zakresie dat.": "Opens event search for a date range.",
    "Dodaj wydarzenie": "Add event",
    "Otwiera formularz dodawania wydarzenia.": "Opens the add event form.",
    "Odśwież": "Refresh",
    "Pobiera ponownie wydarzenia z Google.": "Downloads events from Google again.",
    "Pokaż szczegóły": "View details",
    "Pokazuje wszystkie dane zaznaczonego wydarzenia.": "Shows all available details of the selected event.",
    "Enter na liście wydarzeń": "Enter on the event list",
    "Edytuj": "Edit",
    "Otwiera formularz edycji zaznaczonego wydarzenia.": "Opens the selected event for editing.",
    "Usuń": "Delete",
    "Usuwa zaznaczone wydarzenie po potwierdzeniu.": "Deletes the selected event after confirmation.",
    "Otwórz w Google": "Open in Google",
    "Otwiera zaznaczone wydarzenie w internetowym Kalendarzu Google.": "Opens the selected event in Google Calendar on the web.",
    "Link spotkania": "Meeting link",
    "Pozwala otworzyć albo skopiować istniejący link spotkania.": "Lets you open or copy an existing meeting link.",
    "Skrót aplikacji: {shortcut}.": "Application shortcut: {shortcut}.",
    "Klawisz dostępu: {shortcut}.": "Access key: {shortcut}.",
    "Wybrany miesiąc: {month}": "Selected month: {month}",
    "Wydarzenia dla {date}, {count}": "Events for {date}, {count}",
    "Konto Google: połączone": "Google account: connected",
    "Konto Google: niepołączone": "Google account: not connected",

    # Status, background work, errors and login.
    "Skopiowano z dodatku NVDA: {items}": "Copied from the NVDA add-on: {items}",
    "Brak aktywnego logowania Google. Użyj przycisku Zaloguj do Google.": "No active Google sign-in. Use the Sign in to Google button.",
    "Inna operacja jest już wykonywana.": "Another operation is already in progress.",
    "Operacja nie powiodła się.\n\n{error}": "The operation failed.\n\n{error}",
    "Szczegóły zapisano w pliku last_error.txt w katalogu danych aplikacji.": "Details were saved in last_error.txt in the application data folder.",
    "Błąd GCM by Piotrek": "GCM by Piotrek error",
    "Błąd: {error}": "Error: {error}",
    "Logowanie Google wygasło albo nie zostało wykonane.": "Google sign-in has expired or has not been completed.",
    "Najpierw zaloguj się do Google.": "Sign in to Google first.",
    "Logowanie wymagane": "Sign-in required",
    "Pobieranie wydarzeń: {month}...": "Downloading events: {month}...",
    "Pobrano {events} z {calendars} kalendarzy.": "Downloaded {events} from {calendars} calendars.",
    "Brak ważnego logowania Google.": "There is no valid Google sign-in.",
    "Czy wylogować aplikację GCM by Piotrek? Token dodatku NVDA nie zostanie zmieniony.": "Sign GCM by Piotrek out? The NVDA add-on token will not be changed.",
    "Aplikacja została wylogowana. Dodatek NVDA pozostał bez zmian.": "The application has been signed out. The NVDA add-on was not changed.",
    "Wskaż plik client_secret.json": "Select the client_secret.json file",
    "Pliki JSON (*.json)|*.json|Wszystkie pliki|*.*": "JSON files (*.json)|*.json|All files|*.*",
    "Nie można skopiować konfiguracji OAuth": "Could not copy the OAuth configuration",
    "Logowanie do Google. Dokończ operację w przeglądarce...": "Signing in to Google. Complete the operation in your browser...",
    "Logowanie zakończone. Pobieranie kalendarzy...": "Sign-in complete. Downloading calendars...",
    "Pobieranie listy kalendarzy...": "Downloading the calendar list...",
    "Pobieranie ustawień i kalendarzy...": "Loading settings and calendars...",

    # Dates, month rendering and search.
    "{date}, cały dzień": "{date}, all day",
    "od {start} do {end} włącznie, cały dzień": "from {start} through {end}, inclusive, all day",
    "Wpisz datę w formacie DD.MM.RRRR lub RRRR-MM-DD.": "Enter a date in DD.MM.YYYY or YYYY-MM-DD format.",
    "Nieprawidłowa data": "Invalid date",
    "Wyszukaj wydarzenia": "Search events",
    "Wyszukiwanie obejmuje wybrane kalendarze Google. Data początkowa i końcowa należą do zakresu.": "The search covers the selected Google calendars. The start and end dates are both included.",
    "Szukany tekst": "Search text",
    "Wpisz fragment tytułu, opisu, lokalizacji albo nazwy kalendarza.": "Enter part of a title, description, location or calendar name.",
    "Data początkowa wyszukiwania, DD.MM.RRRR lub RRRR-MM-DD": "Search start date, DD.MM.YYYY or YYYY-MM-DD",
    "Pierwszy dzień zakresu wyszukiwania, podawany włącznie.": "The first day of the search range, included.",
    "Data końcowa wyszukiwania, DD.MM.RRRR lub RRRR-MM-DD": "Search end date, DD.MM.YYYY or YYYY-MM-DD",
    "Ostatni dzień zakresu wyszukiwania, podawany włącznie.": "The last day of the search range, included.",
    "Szukany tekst:": "Search text:",
    "Data początkowa, DD.MM.RRRR lub RRRR-MM-DD:": "Start date, DD.MM.YYYY or YYYY-MM-DD:",
    "Data końcowa, DD.MM.RRRR lub RRRR-MM-DD:": "End date, DD.MM.YYYY or YYYY-MM-DD:",
    "Duży zakres może zawierać wiele wydarzeń, ale wyszukiwanie nie blokuje głównego okna.": "A large range may contain many events, but the search does not block the main window.",
    "Rozpoczyna wyszukiwanie w podanym zakresie.": "Starts the search in the specified range.",
    "Zamyka formularz wyszukiwania.": "Closes the search form.",
    "Nieprawidłowe dane wyszukiwania": "Invalid search data",
    "Wyniki wyszukiwania": "Search results",
    "Znaleziono: {count}. Zakres od {start} do {end} włącznie.": "Found: {count}. Range from {start} through {end}, inclusive.",
    "Wyniki wyszukiwania, {count} elementów": "Search results, {count} items",
    "Przejdź do wydarzenia": "Go to event",
    "Przechodzi do zaznaczonego wyniku w głównym oknie.": "Moves to the selected result in the main window.",
    "Zamknij": "Close",
    "Zamyka wyniki wyszukiwania.": "Closes the search results.",
    "Wyszukiwanie od {start} do {end}...": "Searching from {start} through {end}...",
    "Wyszukiwanie zakończone: {count}.": "Search complete: {count}.",

    # Event form.
    "Utwórz wydarzenie": "Create event",
    "Edytuj wydarzenie": "Edit event",
    "Zapisz zmiany": "Save changes",
    "Tytuł wydarzenia": "Event title",
    "Wpisz nazwę wydarzenia.": "Enter the event name.",
    "Kalendarz wydarzenia": "Event calendar",
    "Kalendarz docelowy": "Destination calendar",
    "Kalendarz tego wydarzenia. Przenoszenie między kalendarzami nie jest jeszcze dostępne.": "This event's calendar. Moving events between calendars is not currently supported.",
    "Wybierz kalendarz, w którym wydarzenie zostanie zapisane.": "Select the calendar in which the event will be saved.",
    "Data rozpoczęcia, DD.MM.RRRR lub RRRR-MM-DD": "Start date, DD.MM.YYYY or YYYY-MM-DD",
    "Wpisz datę rozpoczęcia w formacie dzień, miesiąc, rok albo w formacie ISO.": "Enter the start date as day, month, year or in ISO format.",
    "Wydarzenie całodniowe": "All-day event",
    "Zaznacz, aby pominąć godziny rozpoczęcia i zakończenia.": "Select to omit start and end times.",
    "Godzina rozpoczęcia, GG:MM": "Start time, HH:MM",
    "Wpisz godzinę rozpoczęcia w formacie godzina, dwukropek, minuty.": "Enter the start time as hour, colon, minutes.",
    "Data zakończenia włącznie, DD.MM.RRRR lub RRRR-MM-DD": "End date inclusive, DD.MM.YYYY or YYYY-MM-DD",
    "Wpisz ostatni dzień wydarzenia.": "Enter the last day of the event.",
    "Godzina zakończenia, GG:MM": "End time, HH:MM",
    "Wpisz godzinę zakończenia w formacie godzina, dwukropek, minuty.": "Enter the end time as hour, colon, minutes.",
    "Powtarzanie wydarzenia": "Event recurrence",
    "Wybierz prosty rodzaj cyklu albo wydarzenie jednorazowe.": "Select a basic recurrence or a one-time event.",
    "Bez daty zakończenia cyklu": "No recurrence end date",
    "Zaznacz, aby cykl nie miał określonej daty końcowej.": "Select for a recurrence with no specified end date.",
    "Data zakończenia cyklu włącznie, DD.MM.RRRR lub RRRR-MM-DD": "Recurrence end date inclusive, DD.MM.YYYY or YYYY-MM-DD",
    "Wpisz ostatni dzień, w którym cykl może utworzyć wystąpienie.": "Enter the last date on which the recurrence may create an occurrence.",
    "Lokalizacja": "Location",
    "Wpisz miejsce wydarzenia albo pozostaw pole puste.": "Enter the event location or leave the field blank.",
    "Opis wydarzenia": "Event description",
    "Wpisz dodatkowy opis albo pozostaw pole puste.": "Enter an additional description or leave the field blank.",
    "Tytuł:": "Title:",
    "Kalendarz:": "Calendar:",
    "Data rozpoczęcia, DD.MM.RRRR lub RRRR-MM-DD:": "Start date, DD.MM.YYYY or YYYY-MM-DD:",
    "Typ wydarzenia:": "Event type:",
    "Godzina rozpoczęcia, GG:MM:": "Start time, HH:MM:",
    "Data zakończenia włącznie, DD.MM.RRRR lub RRRR-MM-DD:": "End date inclusive, DD.MM.YYYY or YYYY-MM-DD:",
    "Godzina zakończenia, GG:MM:": "End time, HH:MM:",
    "Powtarzanie:": "Recurrence:",
    "Zakończenie cyklu:": "Recurrence ending:",
    "Data zakończenia cyklu włącznie, DD.MM.RRRR lub RRRR-MM-DD:": "Recurrence end date inclusive, DD.MM.YYYY or YYYY-MM-DD:",
    "Lokalizacja:": "Location:",
    "Opis:": "Description:",
    "Zatwierdza dane w formularzu.": "Confirms the form data.",
    "Anuluj": "Cancel",
    "Zamyka formularz bez zapisywania zmian.": "Closes the form without saving changes.",
    "Nieprawidłowe dane": "Invalid data",
    "Wybierz kalendarz.": "Select a calendar.",
    "Wpisz tytuł wydarzenia.": "Enter the event title.",
    "Data zakończenia nie może być wcześniejsza od daty rozpoczęcia.": "The end date cannot be earlier than the start date.",
    "Podaj godzinę rozpoczęcia.": "Enter the start time.",
    "Podaj godzinę zakończenia.": "Enter the end time.",
    "Koniec wydarzenia musi być późniejszy od początku.": "The event must end after it starts.",
    "Wydarzenie godzinowe nie ma pełnych danych czasu.": "The timed event does not have complete time data.",

    # Recurrence.
    "Nie powtarza się": "Does not repeat",
    "Codziennie": "Daily",
    "Co tydzień": "Weekly",
    "Co miesiąc": "Monthly",
    "Co 3 miesiące": "Every 3 months",
    "Co 6 miesięcy": "Every 6 months",
    "Co rok": "Yearly",
    "zaawansowany cykl": "advanced recurrence",
    "Wybrany rodzaj powtarzania nie jest obsługiwany.": "The selected recurrence type is not supported.",
    "Data zakończenia cyklu nie może być wcześniejsza od daty rozpoczęcia.": "The recurrence end date cannot be earlier than the start date.",
    "zaawansowany cykl utworzony poza GCM": "advanced recurrence created outside GCM",
    "{label}, bez daty zakończenia": "{label}, with no end date",
    "{label}, do {date} włącznie": "{label}, through {date}, inclusive",
    "Edytuj tylko to wystąpienie": "Edit only this occurrence",
    "Edytuj cały cykl": "Edit the entire series",
    "Wybierz zakres edycji wydarzenia cyklicznego. Domyślnie zaznaczone jest najbezpieczniejsze zmienienie jednego terminu.": "Choose the scope for editing the recurring event. The safest option, changing one occurrence, is selected by default.",
    "Zakres edycji cyklu": "Recurrence edit scope",
    "Zakres edycji wydarzenia cyklicznego": "Recurring event edit scope",
    "Ten cykl ma zaawansowaną regułę powtarzania. GCM może edytować pojedyncze wystąpienie, ale cały cykl trzeba zmienić w oficjalnym Kalendarzu Google.": "This series has an advanced recurrence rule. GCM can edit one occurrence, but the entire series must be changed in the official Google Calendar interface.",
    "Ten cykl ma zaawansowaną regułę powtarzania i nie może być bezpiecznie uproszczony przez GCM.": "This series has an advanced recurrence rule and cannot be safely simplified by GCM.",
    "Wydarzenie nadrzędne nie zawiera reguły RRULE.": "The parent event does not contain an RRULE recurrence rule.",
    "To wydarzenie nie jest wystąpieniem cyklu.": "This event is not an occurrence of a recurring series.",
    "Brak pierwotnego czasu rozpoczęcia wystąpienia cyklu.": "The original start time of the recurring occurrence is missing.",
    "Wydarzenie nadrzędne nie ma daty rozpoczęcia.": "The parent event has no start date.",
    "Typ daty wystąpienia nie odpowiada typowi całego cyklu.": "The occurrence date type does not match the series date type.",
    "Wydarzenie nadrzędne nie zawiera reguły powtarzania.": "The parent event does not contain a recurrence rule.",

    # Creating and editing events.
    "Nie znaleziono kalendarza, do którego to konto może dodawać wydarzenia. Sprawdź wybór kalendarzy i uprawnienia konta.": "No calendar was found in which this account may create events. Check calendar selection and account permissions.",
    "Brak kalendarza do zapisu": "No writable calendar",
    "Wybrany kalendarz nie jest już dostępny do zapisu.": "The selected calendar is no longer writable.",
    "Nie można dodać wydarzenia": "Cannot add event",
    "Czy utworzyć wydarzenie?\n\nTytuł: {title}\nKalendarz: {calendar}\nTermin: {when}\nPowtarzanie: {recurrence}": "Create this event?\n\nTitle: {title}\nCalendar: {calendar}\nTime: {when}\nRecurrence: {recurrence}",
    "Potwierdź utworzenie wydarzenia": "Confirm event creation",
    "Tworzenie wydarzenia: {title}...": "Creating event: {title}...",
    "Wydarzenie „{title}” zostało utworzone w kalendarzu {calendar}.": "The event “{title}” was created in {calendar}.",
    "Wydarzenie utworzone": "Event created",
    "Dla tego dnia nie ma zaznaczonego wydarzenia.": "No event is selected for this day.",
    "Nie można edytować wydarzenia": "Cannot edit event",
    "Nie znaleziono kalendarza tego wydarzenia. Odśwież dane i spróbuj ponownie.": "The calendar for this event was not found. Refresh the data and try again.",
    "Kalendarz {calendar} jest dostępny tylko do odczytu.": "The calendar {calendar} is read-only.",
    "Brak uprawnień do edycji": "No permission to edit",
    "Google oznaczył to wydarzenie jako zablokowane i nie pozwala na zwykłą edycję jego pól.": "Google marked this event as locked and does not allow ordinary editing of its fields.",
    "To jest specjalny typ wydarzenia: {kind}. GCM edytuje obecnie zwykłe wydarzenia kalendarza.": "This is a special event type: {kind}. GCM currently edits standard calendar events.",
    "Tego wydarzenia nie można jeszcze edytować": "This event cannot currently be edited",
    "urodziny": "birthday",
    "czas skupienia": "focus time",
    "wydarzenie utworzone z Gmaila": "event created from Gmail",
    "poza biurem": "out of office",
    "miejsce pracy": "working location",
    "Pobieranie całego cyklu: {title}...": "Downloading the entire series: {title}...",
    "Nie wprowadzono żadnych zmian.": "No changes were made.",
    "Nie dotyczy": "Not applicable",
    "Edycja wydarzenia": "Event editing",
    "Zmiana obejmie tylko wybrane wystąpienie. Pozostałe terminy cyklu i reguła powtarzania pozostaną bez zmian.": "Only the selected occurrence will be changed. Other occurrences and the recurrence rule will remain unchanged.",
    "To pojedyncze wydarzenie zostanie zamienione w cykl zgodnie z wybraną regułą powtarzania.": "This one-time event will be converted into a recurring series using the selected recurrence rule.",
    "Zmiana obejmie cały cykl, w tym jego tytuł, termin i podstawową regułę powtarzania.": "The change will affect the entire series, including its title, time and basic recurrence rule.",
    "Wybrano opcję „Nie powtarza się”. Cały cykl zostanie zamieniony w jedno wydarzenie w dacie początku serii.": "Does not repeat was selected. The entire series will be converted into one event on the series start date.",
    "Wydarzenie ma uczestników. Google wyśle im aktualizację po zapisaniu zmian.": "The event has attendees. Google will send them an update after the changes are saved.",
    "Czy zapisać zmiany w wydarzeniu?\n\nTytuł: {title}\nKalendarz: {calendar}\nNowy termin: {when}\nPowtarzanie: {recurrence}\n\n{notice}": "Save the changes to this event?\n\nTitle: {title}\nCalendar: {calendar}\nNew time: {when}\nRecurrence: {recurrence}\n\n{notice}",
    "Potwierdź edycję wydarzenia": "Confirm event changes",
    "Zapisywanie zmian w całym cyklu: {title}...": "Saving changes to the entire series: {title}...",
    "Zapisywanie zmian w wydarzeniu: {title}...": "Saving event changes: {title}...",
    "Wydarzenie „{title}” zostało zamienione w cykl.": "The event “{title}” was converted into a recurring series.",
    "Zmiany w całym cyklu „{title}” zostały zapisane.": "Changes to the entire “{title}” series were saved.",
    "Zmiany w wydarzeniu „{title}” zostały zapisane.": "Changes to the event “{title}” were saved.",
    "Edycja zakończona": "Editing complete",

    # Delete flow.
    "Usuń tylko to wystąpienie": "Delete only this occurrence",
    "Usuń to i wszystkie kolejne wystąpienia": "Delete this and all following occurrences",
    "Usuń cały cykl": "Delete the entire series",
    "Wybierz zakres usuwania wydarzenia cyklicznego. Domyślnie zaznaczone jest najbezpieczniejsze usunięcie jednego terminu.": "Choose the scope for deleting the recurring event. The safest option, deleting one occurrence, is selected by default.",
    "Zakres usuwania cyklu": "Recurrence deletion scope",
    "Zakres usuwania wydarzenia cyklicznego": "Recurring event deletion scope",
    "Nie można usunąć wydarzenia": "Cannot delete event",
    "Kalendarz {calendar} jest dostępny tylko do odczytu i nie pozwala usuwać wydarzeń.": "The calendar {calendar} is read-only and does not allow deleting events.",
    "Brak uprawnień do usuwania": "No permission to delete",
    "Google oznaczył to wydarzenie jako zablokowane i nie pozwala go usunąć.": "Google marked this event as locked and does not allow it to be deleted.",
    "Usunięte zostanie tylko zaznaczone wystąpienie. Pozostałe terminy cyklu pozostaną bez zmian.": "Only the selected occurrence will be deleted. Other occurrences in the series will remain unchanged.",
    "Usunięte zostanie to wydarzenie.": "This event will be deleted.",
    "Usunięte zostanie zaznaczone wystąpienie oraz wszystkie późniejsze terminy tej serii. Wcześniejsze wystąpienia pozostaną. Jeżeli zaznaczony termin jest pierwszym wystąpieniem, skutek będzie równy usunięciu całego cyklu.": "The selected occurrence and all later occurrences in this series will be deleted. Earlier occurrences will remain. If the selected occurrence is the first one, the entire series will be deleted.",
    "Usunięty zostanie cały cykl: wcześniejsze, zaznaczone i wszystkie późniejsze wystąpienia.": "The entire series will be deleted: earlier, selected and all later occurrences.",
    "Wydarzenie ma uczestników. Google wyśle im informację o anulowaniu.": "The event has attendees. Google will notify them about the cancellation.",
    "To jest specjalny typ wydarzenia: {kind}.": "This is a special event type: {kind}.",
    "Potwierdź usunięcie wydarzenia": "Confirm event deletion",
    "Potwierdź usunięcie tego i kolejnych wystąpień": "Confirm deletion of this and following occurrences",
    "Potwierdź usunięcie całego cyklu": "Confirm deletion of the entire series",
    "Czy na pewno wykonać tę operację?\n\n{details}\n\n{notices}\n\nTej operacji nie można cofnąć w aplikacji GCM.": "Are you sure you want to perform this operation?\n\n{details}\n\n{notices}\n\nThis operation cannot be undone in GCM.",
    "Usuwanie wydarzenia: {title}...": "Deleting event: {title}...",
    "Usuwanie tego i kolejnych wystąpień: {title}...": "Deleting this and following occurrences: {title}...",
    "Usuwanie całego cyklu: {title}...": "Deleting the entire series: {title}...",
    "Cały cykl „{title}” został usunięty z kalendarza {calendar}.": "The entire “{title}” series was deleted from {calendar}.",
    "Zaznaczony termin był pierwszym wystąpieniem. Cały cykl „{title}” został usunięty z kalendarza {calendar}.": "The selected occurrence was the first one. The entire “{title}” series was deleted from {calendar}.",
    "Zaznaczone i wszystkie kolejne wystąpienia „{title}” zostały usunięte z kalendarza {calendar}.": "The selected and all following occurrences of “{title}” were deleted from {calendar}.",
    "Wybrane wydarzenie „{title}” zostało usunięte z kalendarza {calendar}.": "The selected event “{title}” was deleted from {calendar}.",
    "Usuwanie zakończone": "Deletion complete",

    # Event model presentation.
    "Spotkanie online": "Online meeting",
    "cały dzień, wydarzenie wielodniowe od {start} do {end}": "all day, multi-day event from {start} through {end}",
    "cały dzień": "all day",
    "trwa od {start}": "in progress since {start}",
    "bez określonej godziny": "no specified time",
    "{timing}, {title}, kalendarz {calendar}": "{timing}, {title}, calendar {calendar}",
    "Tytuł: {title}": "Title: {title}",
    "Kalendarz: {calendar}": "Calendar: {calendar}",
    "Data: {date}": "Date: {date}",
    "Czas: wydarzenie całodniowe": "Time: all-day event",
    "Zakres: {start} — {end}": "Range: {start} — {end}",
    "Czas: wydarzenie całodniowe, wielodniowe": "Time: multi-day all-day event",
    "Początek: {start}": "Start: {start}",
    "Koniec: {end}": "End: {end}",
    "Powtarzanie: wydarzenie należy do cyklu": "Recurrence: the event is part of a series",
    "Powtarzanie: {recurrence}": "Recurrence: {recurrence}",
    "Lokalizacja: {location}": "Location: {location}",
    "Opis: {description}": "Description: {description}",
    "brak": "none",
    "dostępne": "available",
    "Spotkanie online: {meeting}": "Online meeting: {meeting}",
    "Link spotkania: {url}": "Meeting link: {url}",
    "Spotkanie online: brak linku": "Online meeting: no link",
    "Strona wydarzenia w Kalendarzu Google: dostępna": "Event page in Google Calendar: available",
    "Strona wydarzenia w Kalendarzu Google: niedostępna": "Event page in Google Calendar: unavailable",
    "Bez tytułu": "Untitled",
    "brak wydarzeń": "no events",
    "1 wydarzenie": "1 event",
    "{count} wydarzenia": "{count} events",
    "{count} wydarzeń": "{count} events",
    "Podaj datę w formacie DD.MM.RRRR lub RRRR-MM-DD.": "Enter a date in DD.MM.YYYY or YYYY-MM-DD format.",
    "Podana data jest nieprawidłowa.": "The date is invalid.",
    "Podaj godzinę w formacie GG:MM.": "Enter a time in HH:MM format.",
    "Podana godzina jest nieprawidłowa.": "The time is invalid.",
    "Wpisz tekst do wyszukania.": "Enter text to search for.",
    "Data końcowa wyszukiwania nie może być wcześniejsza niż początkowa.": "The search end date cannot be earlier than the start date.",

    # Meeting link, details and web links.
    "Rodzaj spotkania: {meeting}": "Meeting type: {meeting}",
    "spotkanie online": "online meeting",
    "Adres spotkania": "Meeting address",
    "Adres można zaznaczyć i skopiować ręcznie.": "The address can be selected and copied manually.",
    "Otwórz link": "Open link",
    "Kopiuj link": "Copy link",
    "Otwiera spotkanie w domyślnej przeglądarce.": "Opens the meeting in the default browser.",
    "Kopiuje adres spotkania do schowka.": "Copies the meeting address to the clipboard.",
    "Zamyka okno bez wykonywania działania.": "Closes the window without taking action.",
    "Nie udało się otworzyć {description}.\n\n{error}": "Could not open {description}.\n\n{error}",
    "System nie potwierdził otwarcia {description}.": "The system did not confirm that {description} was opened.",
    "Otwieranie linku": "Opening link",
    "Otwarto {description} w domyślnej przeglądarce.": "Opened {description} in the default browser.",
    "Dla zaznaczonego wydarzenia nie ma dostępnego odnośnika do Kalendarza Google.": "There is no Google Calendar link available for the selected event.",
    "wydarzenie w Kalendarzu Google": "the event in Google Calendar",
    "Zaznaczone wydarzenie nie zawiera obsługiwanego linku spotkania.": "The selected event does not contain a supported meeting link.",
    "link spotkania": "the meeting link",
    "Link spotkania został skopiowany do schowka.": "The meeting link was copied to the clipboard.",
    "Nie udało się skopiować linku spotkania do schowka.": "Could not copy the meeting link to the clipboard.",
    "Szczegóły": "Details",
    "Szczegóły wydarzenia": "Event details",
    "Zamyka szczegóły wydarzenia.": "Closes the event details.",

    # Help.
    "Pomoc i skróty klawiaturowe": "Help and keyboard shortcuts",
    "Treść pomocy i lista skrótów": "Help content and shortcut list",
    "Czytaj strzałkami. Tekst można zaznaczać i kopiować.": "Read with the arrow keys. The text can be selected and copied.",
    "Zamyka pomoc i wraca do głównego okna.": "Closes help and returns to the main window.",
    "Zapisz": "Save",
    "Zapisuje ustawienia aplikacji.": "Saves the application settings.",
    "Zamyka ustawienia bez zapisywania zmian.": "Closes settings without saving changes.",

    # API and OAuth errors.
    "Kalendarz {calendar} nie pozwala temu kontu edytować wydarzeń.": "The calendar {calendar} does not allow this account to edit events.",
    "Wydarzenie nie ma identyfikatora Google.": "The event has no Google identifier.",
    "Wydarzenie nie należy do wskazanego kalendarza.": "The event does not belong to the specified calendar.",
    "Edycja nie może przenieść wydarzenia do innego kalendarza.": "Editing cannot move the event to another calendar.",
    "Ten rodzaj wydarzenia nie jest jeszcze obsługiwany przez edycję GCM.": "This event type is not currently supported by GCM editing.",
    "Kalendarz {calendar} nie pozwala temu kontu usuwać wydarzeń.": "The calendar {calendar} does not allow this account to delete events.",
    "Wydarzenie nie ma identyfikatora Google.": "The event has no Google identifier.",
    "Kalendarz {calendar} nie pozwala temu kontu dodawać wydarzeń.": "The calendar {calendar} does not allow this account to create events.",
    "Wybrany kalendarz nie odpowiada danym wydarzenia.": "The selected calendar does not match the event data.",
    "Nie znaleziono pliku client_secret.json.": "The client_secret.json file was not found.",
    "Otwieranie przeglądarki do logowania Google. Po zakończeniu wróć do aplikacji GCM by Piotrek.": "Opening the browser for Google sign-in. When finished, return to GCM by Piotrek.",
    "Logowanie zakończone. Możesz zamknąć tę kartę i wrócić do GCM by Piotrek.": "Sign-in complete. You can close this tab and return to GCM by Piotrek.",
    "Odczyt tokenu OAuth": "Reading the OAuth token",
    "Odświeżanie tokenu OAuth": "Refreshing the OAuth token",
    "Logowanie OAuth": "OAuth sign-in",
    "Kontekst: {context}\nTyp: {type}\nTreść: {message}\n\n{traceback}": "Context: {context}\nType: {type}\nMessage: {message}\n\n{traceback}",
}


def _windows_locale_name() -> str:
    if sys.platform != "win32":
        return ""
    kernel32 = ctypes.windll.kernel32
    try:
        # Prefer the Windows display language rather than regional formatting.
        language_id = kernel32.GetUserDefaultUILanguage()
        if language_id:
            buffer = ctypes.create_unicode_buffer(85)
            length = kernel32.LCIDToLocaleName(
                language_id,
                buffer,
                len(buffer),
                0,
            )
            if length:
                return buffer.value
    except Exception:
        pass
    try:
        buffer = ctypes.create_unicode_buffer(85)
        length = kernel32.GetUserDefaultLocaleName(buffer, len(buffer))
        if length:
            return buffer.value
    except Exception:
        pass
    return ""


def detect_system_language(system_locale: str | None = None) -> str:
    candidates: list[str] = []
    if system_locale:
        candidates.append(system_locale)
    windows_name = _windows_locale_name()
    if windows_name:
        candidates.append(windows_name)
    try:
        locale_name = locale.getlocale()[0]
        if locale_name:
            candidates.append(locale_name)
    except Exception:
        pass
    for env_name in ("LC_ALL", "LC_MESSAGES", "LANG"):
        value = os.environ.get(env_name, "")
        if value:
            candidates.append(value)

    for value in candidates:
        normalized = str(value).strip().lower().replace("-", "_")
        if normalized == "pl" or normalized.startswith("pl_"):
            return LANGUAGE_POLISH
    return LANGUAGE_ENGLISH


def normalize_language_preference(value: object) -> str:
    normalized = str(value or LANGUAGE_AUTO).strip().lower().replace("-", "_")
    aliases = {
        "automatic": LANGUAGE_AUTO,
        "system": LANGUAGE_AUTO,
        "polish": LANGUAGE_POLISH,
        "pl_pl": LANGUAGE_POLISH,
        "english": LANGUAGE_ENGLISH,
        "en_us": LANGUAGE_ENGLISH,
        "en_gb": LANGUAGE_ENGLISH,
    }
    normalized = aliases.get(normalized, normalized)
    if normalized not in SUPPORTED_LANGUAGE_PREFERENCES:
        return LANGUAGE_AUTO
    return normalized


def resolve_language(preference: object, system_locale: str | None = None) -> str:
    normalized = normalize_language_preference(preference)
    if normalized == LANGUAGE_AUTO:
        return detect_system_language(system_locale)
    return normalized


def set_language(preference: object, system_locale: str | None = None) -> str:
    global _current_language, _current_preference
    _current_preference = normalize_language_preference(preference)
    _current_language = resolve_language(_current_preference, system_locale)
    return _current_language


def get_language() -> str:
    return _current_language


def get_language_preference() -> str:
    return _current_preference


def tr(message: str, **values: object) -> str:
    text = str(message)
    if _current_language == LANGUAGE_ENGLISH:
        text = ENGLISH_TRANSLATIONS.get(text, text)
    if values:
        try:
            return text.format(**values)
        except (KeyError, ValueError, IndexError):
            return text
    return text


def language_choice_values() -> tuple[str, ...]:
    return SUPPORTED_LANGUAGE_PREFERENCES


def language_choice_labels() -> tuple[str, ...]:
    return (
        tr("Automatycznie, zgodnie z językiem systemu"),
        tr("Polski"),
        "English",
    )


def language_label(preference: object) -> str:
    normalized = normalize_language_preference(preference)
    mapping = dict(zip(language_choice_values(), language_choice_labels()))
    return mapping.get(normalized, mapping[LANGUAGE_AUTO])


def localized(polish: str, english: str) -> str:
    return polish if _current_language == LANGUAGE_POLISH else english
