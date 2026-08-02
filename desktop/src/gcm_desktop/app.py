from __future__ import annotations

import datetime as dt
import threading
from pathlib import Path
from typing import Callable, TypeVar

import wx

from gcm_core import oauth
from gcm_core.calendar_api import CalendarGateway
from gcm_core.errors import get_error_text, save_error
from gcm_core.models import (
    CalendarEvent,
    CalendarInfo,
    EventCollection,
    EventDraft,
    count_text,
    format_full_date,
    format_month,
    format_short_date,
    month_days,
    month_range,
    parse_polish_date,
)
from gcm_core.paths import copy_client_secret, find_client_secret, migrate_from_nvda
from gcm_core.settings import AppSettings, load_settings, save_settings
from .dialogs import CalendarSelectionDialog, EventCreateDialog, SearchResultsDialog

APP_TITLE = "GCM by Piotrek 0.3.1 — odczyt i dodawanie wydarzeń"
T = TypeVar("T")


class MainFrame(wx.Frame):
    def __init__(self) -> None:
        super().__init__(None, title=APP_TITLE, size=(1120, 700))
        self.settings: AppSettings = load_settings()
        self.calendars: list[CalendarInfo] = []
        self.events = EventCollection()
        today = dt.date.today()
        self.current_year = today.year
        self.current_month = today.month
        self.selected_date = today
        self._day_values: list[dt.date] = []
        self._event_values: list[CalendarEvent] = []
        self._busy = False
        self._focus_event_after_refresh: str | None = None

        panel = wx.Panel(self)
        panel.SetName("Główne okno GCM by Piotrek")
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        account_row = wx.BoxSizer(wx.HORIZONTAL)
        self.login_button = wx.Button(panel, label="Zaloguj do Google")
        self.calendar_button = wx.Button(panel, label="Wybierz kalendarze")
        self.account_label = wx.StaticText(panel, label="Konto Google: sprawdzanie stanu")
        account_row.Add(self.login_button, 0, wx.RIGHT, 8)
        account_row.Add(self.calendar_button, 0, wx.RIGHT, 12)
        account_row.Add(self.account_label, 1, wx.ALIGN_CENTER_VERTICAL)
        main_sizer.Add(account_row, 0, wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, 12)

        nav_row = wx.BoxSizer(wx.HORIZONTAL)
        self.previous_button = wx.Button(panel, label="Poprzedni miesiąc")
        self.today_button = wx.Button(panel, label="Dzisiaj")
        self.next_button = wx.Button(panel, label="Następny miesiąc")
        self.month_label = wx.StaticText(panel, label="")
        self.goto_button = wx.Button(panel, label="Przejdź do daty")
        self.search_button = wx.Button(panel, label="Wyszukaj")
        self.add_button = wx.Button(panel, label="Dodaj wydarzenie")
        self.refresh_button = wx.Button(panel, label="Odśwież")
        for button in (self.previous_button, self.today_button, self.next_button):
            nav_row.Add(button, 0, wx.RIGHT, 6)
        nav_row.Add(self.month_label, 1, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 12)
        for button in (self.goto_button, self.search_button, self.add_button, self.refresh_button):
            nav_row.Add(button, 0, wx.LEFT, 6)
        main_sizer.Add(nav_row, 0, wx.ALL | wx.EXPAND, 12)

        content = wx.BoxSizer(wx.HORIZONTAL)
        days_box = wx.StaticBoxSizer(wx.VERTICAL, panel, "Dni miesiąca")
        self.days_list = wx.ListBox(panel, style=wx.LB_SINGLE)
        self.days_list.SetName("Dni miesiąca")
        self.days_list.SetMinSize((440, 440))
        days_box.Add(self.days_list, 1, wx.ALL | wx.EXPAND, 8)
        content.Add(days_box, 1, wx.RIGHT | wx.EXPAND, 8)

        events_box = wx.StaticBoxSizer(wx.VERTICAL, panel, "Wydarzenia wybranego dnia")
        self.events_list = wx.ListBox(panel, style=wx.LB_SINGLE)
        self.events_list.SetName("Wydarzenia wybranego dnia")
        self.events_list.SetMinSize((540, 380))
        events_box.Add(self.events_list, 1, wx.ALL | wx.EXPAND, 8)
        event_buttons = wx.BoxSizer(wx.HORIZONTAL)
        self.details_button = wx.Button(panel, label="Pokaż szczegóły")
        self.edit_button = wx.Button(panel, label="Edytuj")
        self.delete_button = wx.Button(panel, label="Usuń")
        event_buttons.Add(self.details_button, 0, wx.RIGHT, 8)
        event_buttons.Add(self.edit_button, 0, wx.RIGHT, 8)
        event_buttons.Add(self.delete_button, 0)
        events_box.Add(event_buttons, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 8)
        content.Add(events_box, 1, wx.LEFT | wx.EXPAND, 8)
        main_sizer.Add(content, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 12)

        panel.SetSizer(main_sizer)
        self.status_bar = self.CreateStatusBar()
        self.status_bar.SetName("Stan aplikacji")

        self._bind_events()
        self._install_accelerators()
        self._render_month(select_date=today)
        self.Centre()
        wx.CallAfter(self.days_list.SetFocus)
        wx.CallAfter(self._initialize)

    def _bind_events(self) -> None:
        self.login_button.Bind(wx.EVT_BUTTON, self._on_login)
        self.calendar_button.Bind(wx.EVT_BUTTON, self._on_calendars)
        self.previous_button.Bind(wx.EVT_BUTTON, lambda event: self._change_month(-1))
        self.next_button.Bind(wx.EVT_BUTTON, lambda event: self._change_month(1))
        self.today_button.Bind(wx.EVT_BUTTON, self._on_today)
        self.goto_button.Bind(wx.EVT_BUTTON, self._on_goto)
        self.search_button.Bind(wx.EVT_BUTTON, self._on_search)
        self.add_button.Bind(wx.EVT_BUTTON, self._on_add)
        self.refresh_button.Bind(wx.EVT_BUTTON, lambda event: self._refresh_google())
        self.days_list.Bind(wx.EVT_LISTBOX, self._on_day_selected)
        self.days_list.Bind(wx.EVT_KEY_DOWN, self._on_days_key)
        self.events_list.Bind(wx.EVT_KEY_DOWN, self._on_events_key)
        self.events_list.Bind(wx.EVT_LISTBOX_DCLICK, self._on_details)
        self.details_button.Bind(wx.EVT_BUTTON, self._on_details)
        self.edit_button.Bind(wx.EVT_BUTTON, self._on_write_not_ready)
        self.delete_button.Bind(wx.EVT_BUTTON, self._on_write_not_ready)

    def _install_accelerators(self) -> None:
        ids = {name: wx.NewIdRef() for name in (
            "login", "calendars", "add", "edit", "delete", "search", "goto",
            "today", "refresh", "previous", "next",
        )}
        entries = [
            (wx.ACCEL_CTRL, ord("L"), ids["login"]),
            (wx.ACCEL_CTRL, ord("K"), ids["calendars"]),
            (wx.ACCEL_CTRL, ord("N"), ids["add"]),
            (wx.ACCEL_CTRL, ord("E"), ids["edit"]),
            (wx.ACCEL_NORMAL, wx.WXK_DELETE, ids["delete"]),
            (wx.ACCEL_CTRL, ord("F"), ids["search"]),
            (wx.ACCEL_CTRL, ord("G"), ids["goto"]),
            (wx.ACCEL_CTRL, ord("D"), ids["today"]),
            (wx.ACCEL_NORMAL, wx.WXK_F5, ids["refresh"]),
            (wx.ACCEL_ALT, wx.WXK_LEFT, ids["previous"]),
            (wx.ACCEL_ALT, wx.WXK_RIGHT, ids["next"]),
        ]
        self.SetAcceleratorTable(wx.AcceleratorTable(entries))
        self.Bind(wx.EVT_MENU, self._on_login, id=ids["login"])
        self.Bind(wx.EVT_MENU, self._on_calendars, id=ids["calendars"])
        self.Bind(wx.EVT_MENU, self._on_add, id=ids["add"])
        self.Bind(wx.EVT_MENU, self._on_write_not_ready, id=ids["edit"])
        self.Bind(wx.EVT_MENU, self._on_write_not_ready, id=ids["delete"])
        self.Bind(wx.EVT_MENU, self._on_search, id=ids["search"])
        self.Bind(wx.EVT_MENU, self._on_goto, id=ids["goto"])
        self.Bind(wx.EVT_MENU, self._on_today, id=ids["today"])
        self.Bind(wx.EVT_MENU, lambda event: self._refresh_google(), id=ids["refresh"])
        self.Bind(wx.EVT_MENU, lambda event: self._change_month(-1), id=ids["previous"])
        self.Bind(wx.EVT_MENU, lambda event: self._change_month(1), id=ids["next"])

    def _initialize(self) -> None:
        migrated = migrate_from_nvda()
        self.settings = load_settings()
        if any(migrated.values()):
            copied = ", ".join(key for key, value in migrated.items() if value)
            self._set_status(f"Skopiowano z dodatku NVDA: {copied}.")
        self._update_account_state()
        if oauth.is_logged_in():
            self._refresh_google()
        else:
            self._set_status("Brak aktywnego logowania Google. Użyj przycisku Zaloguj do Google.")

    def _set_status(self, text: str) -> None:
        self.status_bar.SetStatusText(text)

    def _set_busy(self, busy: bool, message: str = "") -> None:
        self._busy = busy
        for control in (
            self.login_button, self.calendar_button, self.previous_button,
            self.today_button, self.next_button, self.goto_button,
            self.search_button, self.add_button, self.refresh_button,
        ):
            control.Enable(not busy)
        if message:
            self._set_status(message)

    def _run_task(
        self,
        *,
        busy_message: str,
        target: Callable[[], T],
        on_success: Callable[[T], None],
    ) -> None:
        if self._busy:
            self._set_status("Inna operacja jest już wykonywana.")
            return
        self._set_busy(True, busy_message)

        def runner() -> None:
            try:
                result = target()
            except Exception as error:
                save_error(busy_message, error)
                wx.CallAfter(self._task_failed, error)
                return
            wx.CallAfter(self._task_succeeded, result, on_success)

        threading.Thread(target=runner, name="GCMNetworkTask", daemon=True).start()

    def _task_succeeded(self, result: T, callback: Callable[[T], None]) -> None:
        self._set_busy(False)
        callback(result)

    def _task_failed(self, error: BaseException) -> None:
        self._set_busy(False)
        details = get_error_text()
        message = f"Operacja nie powiodła się.\n\n{error}"
        if details:
            message += "\n\nSzczegóły zapisano w pliku last_error.txt w katalogu danych aplikacji."
        self._show_message(message, "Błąd GCM by Piotrek", error=True)
        self._set_status(f"Błąd: {error}")

    def _update_account_state(self) -> None:
        logged_in = oauth.is_logged_in()
        self.login_button.SetLabel("Wyloguj z Google" if logged_in else "Zaloguj do Google")
        self.account_label.SetLabel("Konto Google: połączone" if logged_in else "Konto Google: niepołączone")
        self.calendar_button.Enable(logged_in and not self._busy)

    def _selected_calendars(self) -> list[CalendarInfo]:
        selected = set(self.settings.selected_calendar_ids)
        return [calendar for calendar in self.calendars if calendar.calendar_id in selected]

    def _writable_selected_calendars(self) -> list[CalendarInfo]:
        selected = [calendar for calendar in self._selected_calendars() if calendar.can_write]
        if selected:
            return selected
        return [calendar for calendar in self.calendars if calendar.can_write]

    def _load_gateway_and_calendars(self) -> tuple[list[CalendarInfo], list[CalendarEvent]]:
        credentials = oauth.ensure_valid_credentials()
        if credentials is None:
            raise RuntimeError("Logowanie Google wygasło albo nie zostało wykonane.")
        gateway = CalendarGateway(credentials)
        calendars = gateway.list_calendars()
        selected_ids = set(self.settings.selected_calendar_ids)
        if not selected_ids:
            defaults = [calendar for calendar in calendars if calendar.selected or calendar.primary]
            if not defaults:
                defaults = calendars
            self.settings = AppSettings(selected_calendar_ids=[calendar.calendar_id for calendar in defaults])
            save_settings(self.settings)
        chosen = [calendar for calendar in calendars if calendar.calendar_id in set(self.settings.selected_calendar_ids)]
        if not chosen:
            chosen = [calendar for calendar in calendars if calendar.primary] or calendars
            self.settings = AppSettings(selected_calendar_ids=[calendar.calendar_id for calendar in chosen])
            save_settings(self.settings)
        start, end = month_range(self.current_year, self.current_month)
        events = gateway.list_events(chosen, start, end)
        return calendars, events

    def _refresh_google(self) -> None:
        if not oauth.is_logged_in():
            self._show_message("Najpierw zaloguj się do Google.", "Logowanie wymagane", error=True)
            return
        month_name = format_month(self.current_year, self.current_month)
        self._run_task(
            busy_message=f"Pobieranie wydarzeń: {month_name}...",
            target=self._load_gateway_and_calendars,
            on_success=self._after_refresh,
        )

    def _after_refresh(self, result: tuple[list[CalendarInfo], list[CalendarEvent]]) -> None:
        self.calendars, events = result
        self.events.replace(events)
        selected = self.selected_date
        self._render_month(select_date=selected)
        if self._focus_event_after_refresh:
            self._render_events(self._focus_event_after_refresh)
            self._focus_event_after_refresh = None
            self.events_list.SetFocus()
        else:
            self.days_list.SetFocus()
        self._update_account_state()
        self._set_status(
            f"Pobrano {count_text(len(events))} z {len(self._selected_calendars())} kalendarzy."
        )

    def _render_month(self, select_date: dt.date | None = None) -> None:
        self.month_label.SetLabel(format_month(self.current_year, self.current_month))
        self.month_label.SetName(f"Wybrany miesiąc: {format_month(self.current_year, self.current_month)}")
        self._day_values = month_days(self.current_year, self.current_month)
        labels = [
            f"{format_full_date(day)}, {count_text(len(self.events.for_date(day)))}"
            for day in self._day_values
        ]
        self.days_list.Set(labels)
        index = 0
        if select_date and select_date.year == self.current_year and select_date.month == self.current_month:
            index = select_date.day - 1
        if self._day_values:
            index = max(0, min(index, len(self._day_values) - 1))
            self.days_list.SetSelection(index)
            self.selected_date = self._day_values[index]
        self._render_events()

    def _render_events(self, selected_event_id: str | None = None) -> None:
        self._event_values = self.events.for_date(self.selected_date)
        self.events_list.Set([event.display_text(self.selected_date) for event in self._event_values])
        self.events_list.SetName(
            f"Wydarzenia dla {format_full_date(self.selected_date)}, "
            f"{count_text(len(self._event_values))}"
        )
        index = wx.NOT_FOUND
        if selected_event_id:
            for position, event in enumerate(self._event_values):
                if event.event_id == selected_event_id:
                    index = position
                    break
        if index == wx.NOT_FOUND and self._event_values:
            index = 0
        if index != wx.NOT_FOUND:
            self.events_list.SetSelection(index)
        self.details_button.Enable(bool(self._event_values))
        self.edit_button.Enable(bool(self._event_values) and not self._busy)
        self.delete_button.Enable(bool(self._event_values) and not self._busy)
        self._set_status(f"{format_full_date(self.selected_date)}: {count_text(len(self._event_values))}.")

    def _selected_event(self) -> CalendarEvent | None:
        index = self.events_list.GetSelection()
        return self._event_values[index] if 0 <= index < len(self._event_values) else None

    def _on_day_selected(self, event: wx.CommandEvent) -> None:
        index = self.days_list.GetSelection()
        if 0 <= index < len(self._day_values):
            self.selected_date = self._day_values[index]
            self._render_events()
        event.Skip()

    def _on_days_key(self, event: wx.KeyEvent) -> None:
        if event.GetKeyCode() in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            self.events_list.SetFocus()
            return
        event.Skip()

    def _on_events_key(self, event: wx.KeyEvent) -> None:
        if event.GetKeyCode() in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            self._on_details(event)
            return
        event.Skip()

    def _change_month(self, offset: int) -> None:
        if self._busy:
            return
        month_index = self.current_year * 12 + self.current_month - 1 + offset
        self.current_year, zero_month = divmod(month_index, 12)
        self.current_month = zero_month + 1
        self.selected_date = dt.date(self.current_year, self.current_month, 1)
        self.events.replace([])
        self._render_month(select_date=self.selected_date)
        if oauth.is_logged_in():
            self._refresh_google()

    def _on_today(self, event: wx.Event) -> None:
        today = dt.date.today()
        changed_month = (today.year, today.month) != (self.current_year, self.current_month)
        self.current_year, self.current_month = today.year, today.month
        self.selected_date = today
        if changed_month:
            self.events.replace([])
        self._render_month(select_date=today)
        if changed_month and oauth.is_logged_in():
            self._refresh_google()
        else:
            self.days_list.SetFocus()

    def _on_goto(self, event: wx.Event) -> None:
        dialog = wx.TextEntryDialog(self, "Wpisz datę w formacie DD.MM.RRRR.", "Przejdź do daty", self.selected_date.strftime("%d.%m.%Y"))
        try:
            result = dialog.ShowModal()
            value = dialog.GetValue()
        finally:
            dialog.Destroy()
        if result != wx.ID_OK:
            return
        try:
            target = parse_polish_date(value)
        except ValueError as error:
            self._show_message(str(error), "Nieprawidłowa data", error=True)
            return
        changed_month = (target.year, target.month) != (self.current_year, self.current_month)
        self.current_year, self.current_month = target.year, target.month
        self.selected_date = target
        if changed_month:
            self.events.replace([])
        self._render_month(select_date=target)
        if changed_month and oauth.is_logged_in():
            self._refresh_google()
        else:
            self.days_list.SetFocus()

    def _on_search(self, event: wx.Event) -> None:
        dialog = wx.TextEntryDialog(self, "Wpisz fragment tytułu, opisu, lokalizacji albo nazwy kalendarza. Wersja 0.3.1 szuka w bieżącym miesiącu.", "Wyszukaj wydarzenia", "")
        try:
            result = dialog.ShowModal()
            query = dialog.GetValue().strip()
        finally:
            dialog.Destroy()
        if result != wx.ID_OK:
            return
        if not query:
            self._show_message("Wpisz tekst do wyszukania.", "Wyszukiwanie", error=True)
            return
        results = self.events.search(query)
        result_dialog = SearchResultsDialog(self, results)
        try:
            result = result_dialog.ShowModal()
            selected = result_dialog.selected_event
        finally:
            result_dialog.Destroy()
        if result == wx.ID_OK and selected:
            self.selected_date = selected.start_date
            self._render_month(select_date=selected.start_date)
            self._render_events(selected.event_id)
            self.events_list.SetFocus()

    def _on_login(self, event: wx.Event) -> None:
        if oauth.is_logged_in():
            dialog = wx.MessageDialog(
                self,
                "Czy wylogować aplikację GCM by Piotrek? Token dodatku NVDA nie zostanie zmieniony.",
                "Wyloguj z Google",
                wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION,
            )
            try:
                result = dialog.ShowModal()
            finally:
                dialog.Destroy()
            if result == wx.ID_YES:
                oauth.logout()
                self.calendars = []
                self.events.replace([])
                self._render_month(select_date=self.selected_date)
                self._update_account_state()
                self._set_status("Aplikacja została wylogowana. Dodatek NVDA pozostał bez zmian.")
            return

        if find_client_secret() is None:
            picker = wx.FileDialog(
                self,
                "Wskaż plik client_secret.json",
                wildcard="Pliki JSON (*.json)|*.json|Wszystkie pliki|*.*",
                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
            )
            try:
                result = picker.ShowModal()
                chosen = picker.GetPath()
            finally:
                picker.Destroy()
            if result != wx.ID_OK:
                return
            try:
                copy_client_secret(Path(chosen))
            except Exception as error:
                self._show_message(str(error), "Nie można skopiować konfiguracji OAuth", error=True)
                return

        self._run_task(
            busy_message="Logowanie do Google. Dokończ operację w przeglądarce...",
            target=oauth.login,
            on_success=lambda credentials: self._after_login(),
        )

    def _after_login(self) -> None:
        self._update_account_state()
        self._set_status("Logowanie zakończone. Pobieranie kalendarzy...")
        self._refresh_google()

    def _on_calendars(self, event: wx.Event) -> None:
        if not oauth.is_logged_in():
            self._show_message("Najpierw zaloguj się do Google.", "Logowanie wymagane", error=True)
            return

        def load() -> list[CalendarInfo]:
            credentials = oauth.ensure_valid_credentials()
            if credentials is None:
                raise RuntimeError("Brak ważnego logowania Google.")
            return CalendarGateway(credentials).list_calendars()

        self._run_task(
            busy_message="Pobieranie listy kalendarzy...",
            target=load,
            on_success=self._show_calendar_dialog,
        )

    def _show_calendar_dialog(self, calendars: list[CalendarInfo]) -> None:
        self.calendars = calendars
        selected = set(self.settings.selected_calendar_ids)
        if not selected:
            selected = {calendar.calendar_id for calendar in calendars if calendar.selected or calendar.primary}
        dialog = CalendarSelectionDialog(self, calendars, selected)
        try:
            result = dialog.ShowModal()
            ids = dialog.selected_ids()
        finally:
            dialog.Destroy()
        if result != wx.ID_OK:
            return
        if not ids:
            self._show_message("Zaznacz co najmniej jeden kalendarz.", "Wybór kalendarzy", error=True)
            return
        self.settings = AppSettings(selected_calendar_ids=ids)
        save_settings(self.settings)
        self._refresh_google()

    def _on_add(self, event: wx.Event) -> None:
        if not oauth.is_logged_in():
            self._show_message(
                "Najpierw zaloguj się do Google.",
                "Logowanie wymagane",
                error=True,
            )
            return
        writable = self._writable_selected_calendars()
        if not writable:
            self._show_message(
                "Nie znaleziono kalendarza, do którego to konto może dodawać wydarzenia. "
                "Sprawdź wybór kalendarzy i uprawnienia konta.",
                "Brak kalendarza do zapisu",
                error=True,
            )
            return

        dialog = EventCreateDialog(self, writable, self.selected_date)
        try:
            result = dialog.ShowModal()
            draft = dialog.get_draft()
        finally:
            dialog.Destroy()
        if result != wx.ID_OK or draft is None:
            return

        calendar = next(
            (item for item in writable if item.calendar_id == draft.calendar_id),
            None,
        )
        if calendar is None:
            self._show_message(
                "Wybrany kalendarz nie jest już dostępny do zapisu.",
                "Nie można dodać wydarzenia",
                error=True,
            )
            return

        if draft.all_day:
            when = (
                format_short_date(draft.start_date)
                if draft.start_date == draft.end_date_inclusive
                else f"od {format_short_date(draft.start_date)} do "
                     f"{format_short_date(draft.end_date_inclusive)} włącznie"
            )
        else:
            when = (
                f"{format_short_date(draft.start_date)}, {draft.start_time:%H:%M} — "
                f"{format_short_date(draft.end_date_inclusive)}, {draft.end_time:%H:%M}"
            )
        confirm = wx.MessageDialog(
            self,
            f"Czy utworzyć wydarzenie?\n\n"
            f"Tytuł: {draft.title}\n"
            f"Kalendarz: {calendar.name}\n"
            f"Termin: {when}",
            "Potwierdź utworzenie wydarzenia",
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION,
        )
        try:
            confirmed = confirm.ShowModal()
        finally:
            confirm.Destroy()
        if confirmed != wx.ID_YES:
            return

        def create() -> CalendarEvent:
            credentials = oauth.ensure_valid_credentials()
            if credentials is None:
                raise RuntimeError("Brak ważnego logowania Google.")
            return CalendarGateway(credentials).create_event(calendar, draft)

        self._run_task(
            busy_message=f"Tworzenie wydarzenia: {draft.title}...",
            target=create,
            on_success=self._after_create,
        )

    def _after_create(self, created: CalendarEvent) -> None:
        self.current_year = created.start_date.year
        self.current_month = created.start_date.month
        self.selected_date = created.start_date
        self._focus_event_after_refresh = created.event_id
        self._show_message(
            f"Wydarzenie „{created.title}” zostało utworzone w kalendarzu "
            f"{created.calendar_name}.",
            "Wydarzenie utworzone",
        )
        self._refresh_google()

    def _on_details(self, event: wx.Event) -> None:
        selected = self._selected_event()
        if selected is None:
            self._show_message("Dla tego dnia nie ma zaznaczonego wydarzenia.", "Szczegóły", error=True)
            return
        dialog = wx.Dialog(self, title="Szczegóły wydarzenia", style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        sizer = wx.BoxSizer(wx.VERTICAL)
        text = wx.TextCtrl(dialog, value=selected.details_text(), style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_DONTWRAP)
        text.SetName("Szczegóły wydarzenia")
        text.SetMinSize((620, 300))
        sizer.Add(text, 1, wx.ALL | wx.EXPAND, 12)
        close = wx.Button(dialog, wx.ID_OK, "Zamknij")
        close.SetDefault()
        sizer.Add(close, 0, wx.ALL | wx.ALIGN_RIGHT, 12)
        dialog.SetSizerAndFit(sizer)
        dialog.SetSize((720, 460))
        dialog.CentreOnParent()
        try:
            wx.CallAfter(text.SetFocus)
            dialog.ShowModal()
        finally:
            dialog.Destroy()

    def _on_write_not_ready(self, event: wx.Event) -> None:
        self._show_message(
            "Dodawanie wydarzeń jest już aktywne. Edycja i usuwanie zostaną podłączone w następnym, osobno testowanym etapie.",
            "Funkcja jeszcze niedostępna",
        )

    def _show_message(self, message: str, title: str, *, error: bool = False) -> None:
        style = wx.OK | (wx.ICON_ERROR if error else wx.ICON_INFORMATION)
        dialog = wx.MessageDialog(self, message, title, style)
        try:
            dialog.ShowModal()
        finally:
            dialog.Destroy()


class GcmApp(wx.App):
    def OnInit(self) -> bool:
        self.SetAppName("GCM by Piotrek")
        frame = MainFrame()
        frame.Show()
        self.SetTopWindow(frame)
        return True


def main() -> None:
    app = GcmApp(redirect=False)
    app.MainLoop()
