from __future__ import annotations

import datetime as dt
import threading
import webbrowser
from pathlib import Path
from typing import Callable, TypeVar

import wx

from gcm_core import oauth
from gcm_core.calendar_api import CalendarGateway
from gcm_core.i18n import (
    get_language,
    localized,
    resolve_language,
    set_language,
    tr,
)
from gcm_core.errors import get_error_text, save_error
from gcm_core.models import (
    CalendarEvent,
    CalendarInfo,
    EventCollection,
    EventDraft,
    SearchCriteria,
    count_text,
    format_full_date,
    format_month,
    format_short_date,
    month_days,
    month_range,
    parse_date_input,
)
from gcm_core.paths import (
    copy_client_secret,
    find_client_secret,
    migrate_from_nvda,
    migrate_legacy_app_data,
)
from gcm_core.settings import AppSettings, load_settings, save_settings
from gcm_core.restart import launch_current_application
from gcm_core.branding import (
    INDEPENDENCE_NOTICE_EN,
    INDEPENDENCE_NOTICE_PL,
    PRODUCT_NAME,
    PRODUCT_VERSION,
)
from .accessibility import ExplicitNameAccessible, apply_accessible_name
from .dialogs import (
    SettingsDialog,
    EventCreateDialog,
    EventEditDialog,
    HelpDialog,
    MeetingLinkDialog,
    RestartRequiredDialog,
    SearchDialog,
    SearchResultsDialog,
)

T = TypeVar("T")


class MainFrame(wx.Frame):
    def __init__(self) -> None:
        self._legacy_migration = migrate_legacy_app_data()
        self.settings: AppSettings = load_settings()
        set_language(self.settings.language)
        super().__init__(
            None,
            title=f"{PRODUCT_NAME} {PRODUCT_VERSION}",
            size=(1120, 700),
        )
        self.calendars: list[CalendarInfo] = []
        self.events = EventCollection()
        today = dt.date.today()
        self.current_year = today.year
        self.current_month = today.month
        self.selected_date = today
        self._day_values: list[dt.date] = []
        self._event_values: list[CalendarEvent] = []
        self._busy = False
        self._active_task_id = 0
        self._task_timeout_call: wx.CallLater | None = None
        self._focus_event_after_refresh: str | None = None
        self._focus_events_after_refresh = False
        self._accessible_objects: list[wx.Accessible] = []
        self._button_accessibility: dict[wx.Button, ExplicitNameAccessible] = {}

        panel = wx.Panel(self)
        panel.SetName(tr("Główne okno PT Calendar Manager"))
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        account_row = wx.BoxSizer(wx.HORIZONTAL)
        self.login_button = wx.Button(panel, label=tr("Za&loguj do Google"))
        self.settings_button = wx.Button(panel, label=tr("Us&tawienia"))
        self.help_button = wx.Button(panel, label=tr("Pomoc i skróty (&H)"))
        self.account_label = wx.StaticText(
            panel,
            label=tr("Konto Google: sprawdzanie stanu"),
        )
        account_row.Add(self.login_button, 0, wx.RIGHT, 8)
        account_row.Add(self.settings_button, 0, wx.RIGHT, 8)
        account_row.Add(self.help_button, 0, wx.RIGHT, 12)
        account_row.Add(self.account_label, 1, wx.ALIGN_CENTER_VERTICAL)
        main_sizer.Add(account_row, 0, wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, 12)

        nav_row = wx.BoxSizer(wx.HORIZONTAL)
        self.previous_button = wx.Button(panel, label=tr("&Poprzedni miesiąc"))
        self.today_button = wx.Button(panel, label=tr("&Dzisiaj"))
        self.next_button = wx.Button(panel, label=tr("Następny &miesiąc"))
        self.month_label = wx.StaticText(panel, label="")
        self.goto_button = wx.Button(panel, label=tr("Przejdź do daty (&G)"))
        self.search_button = wx.Button(panel, label=tr("Wy&szukaj"))
        self.add_button = wx.Button(panel, label=tr("Dodaj wydarze&nie"))
        self.refresh_button = wx.Button(panel, label=tr("&Odśwież"))
        for button in (self.previous_button, self.today_button, self.next_button):
            nav_row.Add(button, 0, wx.RIGHT, 6)
        nav_row.Add(self.month_label, 1, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 12)
        for button in (self.goto_button, self.search_button, self.add_button, self.refresh_button):
            nav_row.Add(button, 0, wx.LEFT, 6)
        main_sizer.Add(nav_row, 0, wx.ALL | wx.EXPAND, 12)

        content = wx.BoxSizer(wx.HORIZONTAL)
        days_box = wx.StaticBoxSizer(wx.VERTICAL, panel, tr("Dni miesiąca"))
        self.days_list = wx.ListBox(panel, style=wx.LB_SINGLE)
        self.days_list.SetName(tr("Dni miesiąca"))
        self.days_list.SetMinSize((440, 440))
        days_box.Add(self.days_list, 1, wx.ALL | wx.EXPAND, 8)
        content.Add(days_box, 1, wx.RIGHT | wx.EXPAND, 8)

        events_box = wx.StaticBoxSizer(wx.VERTICAL, panel, tr("Wydarzenia wybranego dnia"))
        self.events_list = wx.ListBox(panel, style=wx.LB_SINGLE)
        self.events_list.SetName(tr("Wydarzenia wybranego dnia"))
        self.events_list.SetMinSize((540, 380))
        events_box.Add(self.events_list, 1, wx.ALL | wx.EXPAND, 8)
        event_buttons = wx.BoxSizer(wx.VERTICAL)
        primary_event_buttons = wx.BoxSizer(wx.HORIZONTAL)
        self.details_button = wx.Button(panel, label=tr("Pokaż s&zczegóły"))
        self.edit_button = wx.Button(panel, label=tr("&Edytuj"))
        self.delete_button = wx.Button(panel, label=tr("&Usuń"))
        primary_event_buttons.Add(self.details_button, 0, wx.RIGHT, 8)
        primary_event_buttons.Add(self.edit_button, 0, wx.RIGHT, 8)
        primary_event_buttons.Add(self.delete_button, 0)
        event_buttons.Add(primary_event_buttons, 0, wx.BOTTOM, 6)

        link_event_buttons = wx.BoxSizer(wx.HORIZONTAL)
        self.open_google_button = wx.Button(panel, label=tr("Otwórz &w Google"))
        self.meeting_button = wx.Button(panel, label=tr("Link spotkan&ia"))
        link_event_buttons.Add(self.open_google_button, 0, wx.RIGHT, 8)
        link_event_buttons.Add(self.meeting_button, 0)
        event_buttons.Add(link_event_buttons, 0)
        events_box.Add(event_buttons, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 8)
        content.Add(events_box, 1, wx.LEFT | wx.EXPAND, 8)
        main_sizer.Add(content, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 12)

        panel.SetSizer(main_sizer)
        self.status_bar = self.CreateStatusBar()
        self.status_bar.SetName(tr("Stan aplikacji"))

        self._configure_main_buttons()
        self._bind_events()
        self._install_accelerators()
        self._render_month(select_date=today)
        self.Centre()
        wx.CallAfter(self.days_list.SetFocus)
        wx.CallAfter(self._initialize)


    @staticmethod
    def _access_key(polish: str, english: str) -> str:
        return polish if get_language() == "pl" else english

    def _configure_button(
        self,
        control: wx.Button,
        *,
        name: str,
        access_key: str,
    ) -> None:
        accessible = apply_accessible_name(
            control,
            name,
            keyboard_shortcut=f"Alt+{access_key}",
        )
        if accessible is not None:
            self._accessible_objects.append(accessible)
            self._button_accessibility[control] = accessible

    def _configure_main_buttons(self) -> None:
        definitions = (
            (self.login_button, tr("Zaloguj do Google"), self._access_key("L", "L")),
            (self.settings_button, tr("Ustawienia"), self._access_key("T", "T")),
            (self.help_button, tr("Pomoc i skróty"), self._access_key("H", "H")),
            (self.previous_button, tr("Poprzedni miesiąc"), self._access_key("P", "P")),
            (self.today_button, tr("Dzisiaj"), self._access_key("D", "Y")),
            (self.next_button, tr("Następny miesiąc"), self._access_key("M", "N")),
            (self.goto_button, tr("Przejdź do daty"), self._access_key("G", "G")),
            (self.search_button, tr("Wyszukaj"), self._access_key("S", "S")),
            (self.add_button, tr("Dodaj wydarzenie"), self._access_key("N", "A")),
            (self.refresh_button, tr("Odśwież"), self._access_key("O", "R")),
            (self.details_button, tr("Pokaż szczegóły"), self._access_key("Z", "V")),
            (self.edit_button, tr("Edytuj"), self._access_key("E", "E")),
            (self.delete_button, tr("Usuń"), self._access_key("U", "D")),
            (self.open_google_button, tr("Otwórz w Google"), self._access_key("W", "O")),
            (self.meeting_button, tr("Link spotkania"), self._access_key("I", "M")),
        )
        for control, name, access_key in definitions:
            self._configure_button(
                control,
                name=name,
                access_key=access_key,
            )

    def _update_button_accessible_name(
        self,
        control: wx.Button,
        name: str,
    ) -> None:
        control.SetName(name)
        accessible = self._button_accessibility.get(control)
        if accessible is not None:
            accessible.update(name=name)

    def _bind_events(self) -> None:
        self.login_button.Bind(wx.EVT_BUTTON, self._on_login)
        self.settings_button.Bind(wx.EVT_BUTTON, self._on_settings)
        self.help_button.Bind(wx.EVT_BUTTON, self._on_help)
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
        self.edit_button.Bind(wx.EVT_BUTTON, self._on_edit)
        self.delete_button.Bind(wx.EVT_BUTTON, self._on_delete)
        self.open_google_button.Bind(wx.EVT_BUTTON, self._on_open_google)
        self.meeting_button.Bind(wx.EVT_BUTTON, self._on_meeting_link)
        self.events_list.Bind(wx.EVT_LISTBOX, self._on_event_selected)

    def _install_accelerators(self) -> None:
        ids = {name: wx.NewIdRef() for name in (
            "login", "settings", "add", "edit", "delete", "search", "goto",
            "today", "refresh", "previous", "next", "help", "open_google", "meeting",
        )}
        entries = [
            (wx.ACCEL_CTRL, ord("L"), ids["login"]),
            (wx.ACCEL_CTRL, ord(","), ids["settings"]),
            (wx.ACCEL_CTRL, ord("K"), ids["settings"]),
            (wx.ACCEL_CTRL, ord("N"), ids["add"]),
            (wx.ACCEL_CTRL, ord("E"), ids["edit"]),
            (wx.ACCEL_NORMAL, wx.WXK_DELETE, ids["delete"]),
            (wx.ACCEL_CTRL, ord("F"), ids["search"]),
            (wx.ACCEL_CTRL, ord("G"), ids["goto"]),
            (wx.ACCEL_CTRL, ord("D"), ids["today"]),
            (wx.ACCEL_NORMAL, wx.WXK_F5, ids["refresh"]),
            (wx.ACCEL_NORMAL, wx.WXK_F1, ids["help"]),
            (wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord("G"), ids["open_google"]),
            (wx.ACCEL_CTRL, ord("J"), ids["meeting"]),
            (wx.ACCEL_ALT, wx.WXK_LEFT, ids["previous"]),
            (wx.ACCEL_ALT, wx.WXK_RIGHT, ids["next"]),
        ]
        self.SetAcceleratorTable(wx.AcceleratorTable(entries))
        self.Bind(wx.EVT_MENU, self._on_login, id=ids["login"])
        self.Bind(wx.EVT_MENU, self._on_settings, id=ids["settings"])
        self.Bind(wx.EVT_MENU, self._on_add, id=ids["add"])
        self.Bind(wx.EVT_MENU, self._on_edit, id=ids["edit"])
        self.Bind(wx.EVT_MENU, self._on_delete, id=ids["delete"])
        self.Bind(wx.EVT_MENU, self._on_search, id=ids["search"])
        self.Bind(wx.EVT_MENU, self._on_goto, id=ids["goto"])
        self.Bind(wx.EVT_MENU, self._on_today, id=ids["today"])
        self.Bind(wx.EVT_MENU, lambda event: self._refresh_google(), id=ids["refresh"])
        self.Bind(wx.EVT_MENU, self._on_help, id=ids["help"])
        self.Bind(wx.EVT_MENU, self._on_open_google, id=ids["open_google"])
        self.Bind(wx.EVT_MENU, self._on_meeting_link, id=ids["meeting"])
        self.Bind(wx.EVT_MENU, lambda event: self._change_month(-1), id=ids["previous"])
        self.Bind(wx.EVT_MENU, lambda event: self._change_month(1), id=ids["next"])


    @staticmethod
    def _help_text() -> str:
        if get_language() == "pl":
            return (
                "PT Calendar Manager — pomoc i skróty klawiaturowe\n\n"
                "PRZEZNACZENIE APLIKACJI\n"
                "PT Calendar Manager służy do szybkiego, dostępnego zarządzania Kalendarzem Google. "
                "Bardziej zaawansowane funkcje pozostają w oficjalnym interfejsie Google.\n\n"
                "UKŁAD GŁÓWNEGO OKNA\n"
                "W górnej części znajdują się logowanie, ustawienia i pomoc. "
                "W ustawieniach wybiera się język aplikacji oraz kalendarze. "
                "Po lewej znajduje się lista dni bieżącego miesiąca, a po prawej "
                "lista wydarzeń zaznaczonego dnia. Enter na liście dni przenosi "
                "fokus na wydarzenia. Enter na wydarzeniu otwiera szczegóły.\n\n"
                "SKRÓTY APLIKACJI\n"
                "Ctrl+L — zaloguj do Google albo wyloguj.\n"
                "Ctrl+, — otwórz ustawienia.\n"
                "Ctrl+K — otwórz ustawienia, zachowany skrót wyboru kalendarzy.\n"
                "F1 — otwórz pomoc.\n"
                "Alt+Strzałka w lewo — poprzedni miesiąc.\n"
                "Ctrl+D — dzisiaj.\n"
                "Alt+Strzałka w prawo — następny miesiąc.\n"
                "Ctrl+G — przejdź do daty.\n"
                "Ctrl+F — wyszukaj wydarzenia.\n"
                "Ctrl+N — dodaj wydarzenie.\n"
                "F5 — odśwież dane.\n"
                "Ctrl+E — edytuj wydarzenie.\n"
                "Delete — usuń wydarzenie.\n"
                "Ctrl+Shift+G — otwórz wydarzenie w Kalendarzu Google.\n"
                "Ctrl+J — otwórz lub skopiuj link spotkania.\n\n"
                "JĘZYK APLIKACJI\n"
                "Dostępne są ustawienia Automatycznie, Polski i English. "
                "Tryb automatyczny używa języka Windows: polskiego dla polskiego "
                "systemu, a angielskiego dla pozostałych. Ręczna zmiana języka "
                "zaczyna działać po ponownym uruchomieniu PT Calendar Manager.\n\n"
                "WYDARZENIA CYKLICZNE\n"
                "PT Calendar Manager tworzy i edytuje podstawowe cykle: codzienne, tygodniowe, "
                "miesięczne, kwartalne, półroczne i roczne. Zaawansowane reguły "
                "utworzone poza PT Calendar Manager można edytować tylko jako pojedyncze wystąpienia.\n\n"
                "OTWIERANIE W GOOGLE I LINK SPOTKANIA\n"
                "Otwórz w Google przechodzi do wybranego wydarzenia w przeglądarce. "
                "Link spotkania można otworzyć albo skopiować, jeżeli został dodany "
                "do wydarzenia poza PT Calendar Manager.\n\n"
                "INFORMACJA O NIEZALEŻNOŚCI\n"
                + INDEPENDENCE_NOTICE_PL
            )
        return (
            "PT Calendar Manager — help and keyboard shortcuts\n\n"
            "PURPOSE\n"
            "PT Calendar Manager provides quick, accessible management of Google Calendar. "
            "More advanced features remain available in Google's official interface.\n\n"
            "MAIN WINDOW\n"
            "Sign-in, Settings and Help are at the top. Settings contains the "
            "application language and calendar selection. The days of the current "
            "month are listed on the left and events for the selected day are on "
            "the right. Enter on the day list moves focus to events. Enter on an "
            "event opens its details.\n\n"
            "APPLICATION SHORTCUTS\n"
            "Ctrl+L — sign in to or sign out of Google.\n"
            "Ctrl+, — open Settings.\n"
            "Ctrl+K — open Settings; retained as the former calendar shortcut.\n"
            "F1 — open Help.\n"
            "Alt+Left Arrow — previous month.\n"
            "Ctrl+D — today.\n"
            "Alt+Right Arrow — next month.\n"
            "Ctrl+G — go to date.\n"
            "Ctrl+F — search events.\n"
            "Ctrl+N — add an event.\n"
            "F5 — refresh data.\n"
            "Ctrl+E — edit an event.\n"
            "Delete — delete an event.\n"
            "Ctrl+Shift+G — open the event in Google Calendar.\n"
            "Ctrl+J — open or copy a meeting link.\n\n"
            "APPLICATION LANGUAGE\n"
            "The available choices are Automatic, Polish and English. Automatic "
            "uses the Windows language: Polish on a Polish system and English for "
            "other systems. A manual language change takes effect after PT Calendar Manager is restarted.\n\n"
            "RECURRING EVENTS\n"
            "PT Calendar Manager creates and edits basic daily, weekly, monthly, quarterly, "
            "semiannual and yearly recurrences. Advanced rules created outside "
            "PT Calendar Manager can only be edited as individual occurrences.\n\n"
            "OPENING IN GOOGLE AND MEETING LINKS\n"
            "Open in Google opens the selected event in a browser. A meeting link "
            "can be opened or copied when it was added to the event outside PT Calendar Manager.\n\n"
            "INDEPENDENCE NOTICE\n"
            + INDEPENDENCE_NOTICE_EN
        )

    def _on_help(self, event: wx.Event) -> None:
        dialog = HelpDialog(self, self._help_text())
        try:
            dialog.ShowModal()
        finally:
            dialog.Destroy()
        self.days_list.SetFocus()

    def _initialize(self) -> None:
        migrated = migrate_from_nvda()
        self.settings = load_settings()
        if any(self._legacy_migration.values()):
            copied = ", ".join(
                name for name, value in self._legacy_migration.items() if value
            )
            self._set_status(
                tr("Skopiowano dane z wcześniejszej nazwy aplikacji: {items}", items=copied)
            )
        elif any(migrated.values()):
            copied = ", ".join(key for key, value in migrated.items() if value)
            self._set_status(tr("Skopiowano z dodatku NVDA: {items}", items=copied))
        self._update_account_state()
        if oauth.is_logged_in():
            self._refresh_google()
        else:
            self._set_status(tr("Brak aktywnego logowania Google. Użyj przycisku Zaloguj do Google."))

    def _set_status(self, text: str) -> None:
        self.status_bar.SetStatusText(text)

    def _set_busy(self, busy: bool, message: str = "") -> None:
        self._busy = busy
        # Settings and Help deliberately remain available while Google is busy.
        # Language selection and diagnostics must never depend on the network.
        for control in (
            self.login_button, self.previous_button,
            self.today_button, self.next_button, self.goto_button,
            self.search_button, self.add_button, self.refresh_button,
            self.edit_button, self.delete_button,
        ):
            control.Enable(not busy)
        if message:
            self._set_status(message)

    def _cancel_task_timeout(self) -> None:
        call = self._task_timeout_call
        self._task_timeout_call = None
        if call is not None:
            try:
                if call.IsRunning():
                    call.Stop()
            except Exception:
                pass

    def _run_task(
        self,
        *,
        busy_message: str,
        target: Callable[[], T],
        on_success: Callable[[T], None],
        timeout_seconds: int = 45,
    ) -> None:
        if self._busy:
            self._set_status(tr("Inna operacja jest już wykonywana."))
            return
        self._active_task_id += 1
        task_id = self._active_task_id
        self._set_busy(True, busy_message)
        self._cancel_task_timeout()
        self._task_timeout_call = wx.CallLater(
            max(1, int(timeout_seconds)) * 1000,
            self._task_timed_out,
            task_id,
        )

        def runner() -> None:
            try:
                result = target()
            except Exception as error:
                save_error(busy_message, error)
                wx.CallAfter(self._task_failed, task_id, error)
                return
            wx.CallAfter(self._task_succeeded, task_id, result, on_success)

        threading.Thread(target=runner, name="PTCalendarManagerNetworkTask", daemon=True).start()

    def _task_succeeded(
        self,
        task_id: int,
        result: T,
        callback: Callable[[T], None],
    ) -> None:
        if task_id != self._active_task_id or not self._busy:
            return
        self._cancel_task_timeout()
        self._set_busy(False)
        callback(result)

    def _task_failed(self, task_id: int, error: BaseException) -> None:
        if task_id != self._active_task_id or not self._busy:
            return
        self._cancel_task_timeout()
        self._set_busy(False)
        details = get_error_text()
        message = tr("Operacja nie powiodła się.\n\n{error}", error=error)
        if details:
            message += "\n\n" + tr("Szczegóły zapisano w pliku last_error.txt w katalogu danych aplikacji.")
        self._show_message(message, tr("Błąd PT Calendar Manager"), error=True)
        self._set_status(tr("Błąd: {error}", error=error))

    def _task_timed_out(self, task_id: int) -> None:
        if task_id != self._active_task_id or not self._busy:
            return
        self._task_timeout_call = None
        self._set_busy(False)
        message = tr(
            "Google nie odpowiedział w wymaganym czasie. Interfejs został odblokowany. Sprawdź połączenie z Internetem, zaporę sieciową albo zaloguj się ponownie. Ustawienia języka pozostają dostępne bez połączenia z Google."
        )
        self._show_message(
            message,
            tr("Przekroczono czas oczekiwania na Google"),
            error=True,
        )
        self._set_status(message)

    def _update_account_state(self) -> None:
        logged_in = oauth.is_logged_in()
        login_name = (
            tr("Wyloguj z Google") if logged_in else tr("Zaloguj do Google")
        )
        self.login_button.SetLabel(
            tr("Wy&loguj z Google") if logged_in else tr("Za&loguj do Google")
        )
        self._update_button_accessible_name(self.login_button, login_name)
        self.account_label.SetLabel(
            tr("Konto Google: połączone")
            if logged_in
            else tr("Konto Google: niepołączone")
        )
        self.settings_button.Enable(not self._busy)

    def _selected_calendars(self) -> list[CalendarInfo]:
        selected = set(self.settings.selected_calendar_ids)
        return [calendar for calendar in self.calendars if calendar.calendar_id in selected]

    def _writable_selected_calendars(self) -> list[CalendarInfo]:
        selected = [calendar for calendar in self._selected_calendars() if calendar.can_write]
        if selected:
            return selected
        return [calendar for calendar in self.calendars if calendar.can_write]

    def _calendar_for_event(self, event: CalendarEvent) -> CalendarInfo | None:
        return next(
            (calendar for calendar in self.calendars if calendar.calendar_id == event.calendar_id),
            None,
        )

    @staticmethod
    def _draft_when_text(draft: EventDraft) -> str:
        if draft.all_day:
            if draft.start_date == draft.end_date_inclusive:
                return tr(
                    "{date}, cały dzień",
                    date=format_short_date(draft.start_date),
                )
            return tr(
                "od {start} do {end} włącznie, cały dzień",
                start=format_short_date(draft.start_date),
                end=format_short_date(draft.end_date_inclusive),
            )
        return (
            f"{format_short_date(draft.start_date)}, {draft.start_time:%H:%M} — "
            f"{format_short_date(draft.end_date_inclusive)}, {draft.end_time:%H:%M}"
        )

    def _load_gateway_and_calendars(
        self,
    ) -> tuple[list[CalendarInfo], list[CalendarEvent]]:
        credentials = oauth.ensure_valid_credentials()
        if credentials is None:
            raise RuntimeError(
                tr("Logowanie Google wygasło albo nie zostało wykonane.")
            )
        gateway = CalendarGateway(credentials)
        calendars = gateway.list_calendars()
        selected_ids = set(self.settings.selected_calendar_ids)
        if not selected_ids:
            defaults = [
                calendar
                for calendar in calendars
                if calendar.selected or calendar.primary
            ]
            if not defaults:
                defaults = calendars
            self.settings = AppSettings(
                selected_calendar_ids=[
                    calendar.calendar_id for calendar in defaults
                ],
                language=self.settings.language,
            )
            save_settings(self.settings)
        chosen = [
            calendar
            for calendar in calendars
            if calendar.calendar_id in set(self.settings.selected_calendar_ids)
        ]
        if not chosen:
            chosen = [calendar for calendar in calendars if calendar.primary] or calendars
            self.settings = AppSettings(
                selected_calendar_ids=[
                    calendar.calendar_id for calendar in chosen
                ],
                language=self.settings.language,
            )
            save_settings(self.settings)
        start, end = month_range(self.current_year, self.current_month)
        events = gateway.list_events(chosen, start, end)
        return calendars, events

    def _refresh_google(self) -> None:
        if not oauth.is_logged_in():
            self._show_message(
                tr("Najpierw zaloguj się do Google."),
                tr("Logowanie wymagane"),
                error=True,
            )
            return
        month_name = format_month(self.current_year, self.current_month)
        self._run_task(
            busy_message=tr(
                "Pobieranie wydarzeń: {month}...",
                month=month_name,
            ),
            target=self._load_gateway_and_calendars,
            on_success=self._after_refresh,
        )

    def _after_refresh(
        self,
        result: tuple[list[CalendarInfo], list[CalendarEvent]],
    ) -> None:
        self.calendars, events = result
        self.events.replace(events)
        selected = self.selected_date
        self._render_month(select_date=selected)
        if self._focus_event_after_refresh:
            self._render_events(self._focus_event_after_refresh)
            self._focus_event_after_refresh = None
            self._focus_events_after_refresh = False
            self.events_list.SetFocus()
        elif self._focus_events_after_refresh:
            self._focus_events_after_refresh = False
            self.events_list.SetFocus()
        else:
            self.days_list.SetFocus()
        self._update_account_state()
        self._set_status(
            tr(
                "Pobrano {events} z {calendars} kalendarzy.",
                events=count_text(len(events)),
                calendars=len(self._selected_calendars()),
            )
        )

    def _render_month(self, select_date: dt.date | None = None) -> None:
        month_text = format_month(self.current_year, self.current_month)
        self.month_label.SetLabel(month_text)
        self.month_label.SetName(
            tr("Wybrany miesiąc: {month}", month=month_text)
        )
        self._day_values = month_days(self.current_year, self.current_month)
        labels = [
            f"{format_full_date(day)}, "
            f"{count_text(len(self.events.for_date(day)))}"
            for day in self._day_values
        ]
        self.days_list.Set(labels)
        index = 0
        if (
            select_date
            and select_date.year == self.current_year
            and select_date.month == self.current_month
        ):
            index = select_date.day - 1
        if self._day_values:
            index = max(0, min(index, len(self._day_values) - 1))
            self.days_list.SetSelection(index)
            self.selected_date = self._day_values[index]
        self._render_events()

    def _render_events(self, selected_event_id: str | None = None) -> None:
        self._event_values = self.events.for_date(self.selected_date)
        self.events_list.Set(
            [event.display_text(self.selected_date) for event in self._event_values]
        )
        self.events_list.SetName(
            tr(
                "Wydarzenia dla {date}, {count}",
                date=format_full_date(self.selected_date),
                count=count_text(len(self._event_values)),
            )
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
        self._update_event_action_buttons()
        self._set_status(
            f"{format_full_date(self.selected_date)}: "
            f"{count_text(len(self._event_values))}."
        )

    def _selected_event(self) -> CalendarEvent | None:
        index = self.events_list.GetSelection()
        return self._event_values[index] if 0 <= index < len(self._event_values) else None

    def _update_event_action_buttons(self) -> None:
        selected = self._selected_event()
        has_selection = selected is not None
        self.details_button.Enable(has_selection)
        self.edit_button.Enable(has_selection and not self._busy)
        self.delete_button.Enable(has_selection and not self._busy)
        self.open_google_button.Enable(
            bool(selected and selected.can_open_in_google)
        )
        self.meeting_button.Enable(
            bool(selected and selected.has_meeting_link)
        )

    def _on_event_selected(self, event: wx.CommandEvent) -> None:
        self._update_event_action_buttons()
        event.Skip()

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
        dialog = wx.TextEntryDialog(
            self,
            tr("Wpisz datę w formacie DD.MM.RRRR lub RRRR-MM-DD."),
            tr("Przejdź do daty"),
            format_short_date(self.selected_date),
        )
        try:
            result = dialog.ShowModal()
            value = dialog.GetValue()
        finally:
            dialog.Destroy()
        if result != wx.ID_OK:
            return
        try:
            target = parse_date_input(value)
        except ValueError as error:
            self._show_message(str(error), tr("Nieprawidłowa data"), error=True)
            return
        changed_month = (target.year, target.month) != (
            self.current_year,
            self.current_month,
        )
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
        if not oauth.is_logged_in():
            self._show_message(
                tr("Najpierw zaloguj się do Google."),
                tr("Logowanie wymagane"),
                error=True,
            )
            return

        today = dt.date.today()
        dialog = SearchDialog(
            self,
            default_start=today,
            default_end=today + dt.timedelta(days=365),
        )
        try:
            result = dialog.ShowModal()
            criteria = dialog.get_criteria()
        finally:
            dialog.Destroy()
        if result != wx.ID_OK or criteria is None:
            return

        def search() -> tuple[list[CalendarInfo], SearchCriteria, list[CalendarEvent]]:
            credentials = oauth.ensure_valid_credentials()
            if credentials is None:
                raise RuntimeError(tr("Brak ważnego logowania Google."))
            gateway = CalendarGateway(credentials)
            calendars = self.calendars or gateway.list_calendars()
            selected_ids = set(self.settings.selected_calendar_ids)
            chosen = [
                calendar
                for calendar in calendars
                if calendar.calendar_id in selected_ids
            ]
            if not chosen:
                chosen = [calendar for calendar in calendars if calendar.primary] or calendars
            results = gateway.search_events(chosen, criteria)
            return calendars, criteria, results

        self._run_task(
            busy_message=tr(
                "Wyszukiwanie od {start} do {end}...",
                start=format_short_date(criteria.start_date),
                end=format_short_date(criteria.end_date_inclusive),
            ),
            target=search,
            on_success=self._after_search,
        )

    def _after_search(
        self,
        result: tuple[list[CalendarInfo], SearchCriteria, list[CalendarEvent]],
    ) -> None:
        calendars, criteria, events = result
        self.calendars = calendars
        self._update_account_state()
        self._set_status(
            tr("Wyszukiwanie zakończone: {count}.", count=count_text(len(events)))
        )

        result_dialog = SearchResultsDialog(self, events, criteria)
        try:
            dialog_result = result_dialog.ShowModal()
            selected = result_dialog.selected_event
        finally:
            result_dialog.Destroy()

        if dialog_result != wx.ID_OK or selected is None:
            self.search_button.SetFocus()
            return

        self.current_year = selected.start_date.year
        self.current_month = selected.start_date.month
        self.selected_date = selected.start_date
        self._focus_event_after_refresh = selected.event_id
        self.events.replace([])
        self._render_month(select_date=selected.start_date)
        self._refresh_google()

    def _on_login(self, event: wx.Event) -> None:
        if oauth.is_logged_in():
            dialog = wx.MessageDialog(
                self,
                tr(
                    "Czy wylogować aplikację PT Calendar Manager? Token dodatku NVDA nie zostanie zmieniony."
                ),
                tr("Wyloguj z Google"),
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
                self._set_status(
                    tr(
                        "Aplikacja została wylogowana. Dodatek NVDA pozostał bez zmian."
                    )
                )
            return

        if find_client_secret() is None:
            explanation = wx.MessageDialog(
                self,
                tr(
                    "Na tym komputerze nie znaleziono konfiguracji logowania Google client_secret.json. Jest ona potrzebna do rozpoczęcia logowania.\n\nSkopiuj ten plik z poprzedniego komputera z katalogu %APPDATA%\\PT Calendar Manager albo wskaż plik używany przez wtyczkę NVDA. Po wybraniu OK otworzy się okno wyboru pliku."
                ),
                tr("Brak konfiguracji logowania Google"),
                wx.OK | wx.CANCEL | wx.ICON_INFORMATION,
            )
            try:
                explanation_result = explanation.ShowModal()
            finally:
                explanation.Destroy()
            if explanation_result != wx.ID_OK:
                self._set_status(tr("Logowanie anulowane: nie wskazano konfiguracji OAuth."))
                return

            picker = wx.FileDialog(
                self,
                tr("Wskaż plik client_secret.json"),
                wildcard=tr("Pliki JSON (*.json)|*.json|Wszystkie pliki|*.*"),
                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
            )
            try:
                result = picker.ShowModal()
                chosen = picker.GetPath()
            finally:
                picker.Destroy()
            if result != wx.ID_OK:
                self._set_status(tr("Logowanie anulowane: nie wskazano konfiguracji OAuth."))
                return
            try:
                copy_client_secret(Path(chosen))
            except Exception as error:
                self._show_message(
                    str(error),
                    tr("Nie można skopiować konfiguracji OAuth"),
                    error=True,
                )
                return

        self._run_task(
            busy_message=tr(
                "Logowanie do Google. Dokończ operację w przeglądarce..."
            ),
            target=oauth.login,
            on_success=lambda credentials: self._after_login(),
        )

    def _after_login(self) -> None:
        self._update_account_state()
        self._set_status(
            tr("Logowanie zakończone. Pobieranie kalendarzy...")
        )
        self._refresh_google()

    def _on_settings(self, event: wx.Event) -> None:
        # Opening Settings must never require a successful Google request.
        # When calendars are unavailable, the dialog still exposes language
        # selection and explains how to retry calendar loading.
        logged_in = oauth.is_logged_in()
        try:
            self._show_settings_dialog(
                self.calendars if logged_in else [],
                google_logged_in=logged_in,
            )
        except Exception as error:
            save_error(tr("Otwieranie ustawień"), error)
            self._show_message(
                tr("Nie udało się otworzyć Ustawień.\n\n{error}", error=error),
                tr("Błąd Ustawień"),
                error=True,
            )

    def _show_settings_dialog(
        self,
        calendars: list[CalendarInfo],
        *,
        google_logged_in: bool | None = None,
    ) -> None:
        if calendars:
            self.calendars = calendars
        selected = set(self.settings.selected_calendar_ids)
        if calendars and not selected:
            selected = {
                calendar.calendar_id
                for calendar in calendars
                if calendar.selected or calendar.primary
            }
        old_ids = list(self.settings.selected_calendar_ids)
        old_language = self.settings.language
        old_effective_language = get_language()
        if google_logged_in is None:
            google_logged_in = oauth.is_logged_in()
        dialog = SettingsDialog(
            self,
            calendars,
            selected,
            old_language,
            google_logged_in=google_logged_in,
        )
        try:
            result = dialog.ShowModal()
            ids = dialog.selected_ids()
            language = dialog.language_preference()
        finally:
            dialog.Destroy()
        if result != wx.ID_OK:
            return

        self.settings = AppSettings(
            selected_calendar_ids=ids,
            language=language,
        )
        save_settings(self.settings)
        preference_changed = language != old_language
        effective_language_changed = (
            preference_changed
            and resolve_language(language) != old_effective_language
        )
        calendar_changed = set(ids) != set(old_ids)

        if effective_language_changed:
            restart_dialog = RestartRequiredDialog(self)
            try:
                restart_result = restart_dialog.ShowModal()
            finally:
                restart_dialog.Destroy()

            if restart_result == wx.ID_OK:
                try:
                    launch_current_application()
                except Exception as error:
                    self._show_message(
                        tr(
                            "Nie udało się ponownie uruchomić aplikacji. Ustawienie języka zostało zapisane i będzie użyte przy następnym ręcznym uruchomieniu.\n\n{error}",
                            error=error,
                        ),
                        tr("Nie można ponownie uruchomić PT Calendar Manager"),
                        error=True,
                    )
                else:
                    self.Close()
                    return
            else:
                self._set_status(
                    tr(
                        "Zmiana języka zostanie zastosowana przy następnym uruchomieniu."
                    )
                )
        else:
            self._set_status(tr("Ustawienia zostały zapisane."))

        if calendar_changed and oauth.is_logged_in():
            self._refresh_google()
        else:
            self.settings_button.SetFocus()

    def _on_add(self, event: wx.Event) -> None:
        if not oauth.is_logged_in():
            self._show_message(
                tr("Najpierw zaloguj się do Google."),
                tr("Logowanie wymagane"),
                error=True,
            )
            return
        writable = self._writable_selected_calendars()
        if not writable:
            self._show_message(
                tr(
                    "Nie znaleziono kalendarza, do którego to konto może dodawać wydarzenia. Sprawdź wybór kalendarzy i uprawnienia konta."
                ),
                tr("Brak kalendarza do zapisu"),
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
                tr("Wybrany kalendarz nie jest już dostępny do zapisu."),
                tr("Nie można dodać wydarzenia"),
                error=True,
            )
            return

        confirm = wx.MessageDialog(
            self,
            tr(
                "Czy utworzyć wydarzenie?\n\nTytuł: {title}\nKalendarz: {calendar}\nTermin: {when}\nPowtarzanie: {recurrence}",
                title=draft.title,
                calendar=calendar.name,
                when=self._draft_when_text(draft),
                recurrence=draft.recurrence.display_text(),
            ),
            tr("Potwierdź utworzenie wydarzenia"),
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
                raise RuntimeError(tr("Brak ważnego logowania Google."))
            return CalendarGateway(credentials).create_event(calendar, draft)

        self._run_task(
            busy_message=tr("Tworzenie wydarzenia: {title}...", title=draft.title),
            target=create,
            on_success=self._after_create,
        )

    def _after_create(self, created: CalendarEvent) -> None:
        self.current_year = created.start_date.year
        self.current_month = created.start_date.month
        self.selected_date = created.start_date
        self._focus_event_after_refresh = created.event_id
        self._show_message(
            tr(
                "Wydarzenie „{title}” zostało utworzone w kalendarzu {calendar}.",
                title=created.title,
                calendar=created.calendar_name,
            ),
            tr("Wydarzenie utworzone"),
        )
        self._refresh_google()

    def _choose_recurring_edit_scope(self) -> str | None:
        choices = [
            tr("Edytuj tylko to wystąpienie"),
            tr("Edytuj cały cykl"),
        ]
        dialog = wx.SingleChoiceDialog(
            self,
            tr(
                "Wybierz zakres edycji wydarzenia cyklicznego. Domyślnie zaznaczone jest najbezpieczniejsze zmienienie jednego terminu."
            ),
            tr("Zakres edycji cyklu"),
            choices,
        )
        dialog.SetName(tr("Zakres edycji wydarzenia cyklicznego"))
        dialog.SetSelection(0)
        try:
            result = dialog.ShowModal()
            selection = dialog.GetSelection()
        finally:
            dialog.Destroy()
        if result != wx.ID_OK or selection < 0:
            return None
        return ("instance", "series")[selection]

    def _on_edit(self, event: wx.Event) -> None:
        if not oauth.is_logged_in():
            self._show_message(
                tr("Najpierw zaloguj się do Google."),
                tr("Logowanie wymagane"),
                error=True,
            )
            return
        selected = self._selected_event()
        if selected is None:
            self._show_message(
                tr("Dla tego dnia nie ma zaznaczonego wydarzenia."),
                tr("Nie można edytować wydarzenia"),
                error=True,
            )
            return
        calendar = self._calendar_for_event(selected)
        if calendar is None:
            self._show_message(
                tr(
                    "Nie znaleziono kalendarza tego wydarzenia. Odśwież dane i spróbuj ponownie."
                ),
                tr("Nie można edytować wydarzenia"),
                error=True,
            )
            return
        if not calendar.can_write:
            self._show_message(
                tr(
                    "Kalendarz {calendar} jest dostępny tylko do odczytu.",
                    calendar=calendar.name,
                ),
                tr("Brak uprawnień do edycji"),
                error=True,
            )
            return
        if not selected.supports_basic_edit:
            if selected.locked:
                reason = tr(
                    "Google oznaczył to wydarzenie jako zablokowane i nie pozwala na zwykłą edycję jego pól."
                )
            else:
                event_type_labels = {
                    "birthday": tr("urodziny"),
                    "focusTime": tr("czas skupienia"),
                    "fromGmail": tr("wydarzenie utworzone z Gmaila"),
                    "outOfOffice": tr("poza biurem"),
                    "workingLocation": tr("miejsce pracy"),
                }
                kind = event_type_labels.get(selected.event_type, selected.event_type)
                reason = tr(
                    "To jest specjalny typ wydarzenia: {kind}. PT Calendar Manager edytuje obecnie zwykłe wydarzenia kalendarza.",
                    kind=kind,
                )
            self._show_message(
                reason,
                tr("Tego wydarzenia nie można jeszcze edytować"),
                error=True,
            )
            return

        if selected.is_recurring_instance:
            scope = self._choose_recurring_edit_scope()
            if scope is None:
                self.events_list.SetFocus()
                return
            if scope == "series":
                self._load_series_for_edit(calendar, selected)
                return
        self._show_edit_dialog(
            calendar,
            selected,
            selected,
            "instance" if selected.is_recurring_instance else "single",
        )

    def _load_series_for_edit(
        self,
        calendar: CalendarInfo,
        instance: CalendarEvent,
    ) -> None:
        def load() -> CalendarEvent:
            credentials = oauth.ensure_valid_credentials()
            if credentials is None:
                raise RuntimeError(tr("Brak ważnego logowania Google."))
            return CalendarGateway(credentials).get_recurring_series(calendar, instance)

        self._run_task(
            busy_message=tr(
                "Pobieranie całego cyklu: {title}...",
                title=instance.title,
            ),
            target=load,
            on_success=lambda parent: self._show_edit_dialog(
                calendar,
                instance,
                parent,
                "series",
            ),
        )

    def _show_edit_dialog(
        self,
        calendar: CalendarInfo,
        selected_instance: CalendarEvent,
        form_event: CalendarEvent,
        scope: str,
    ) -> None:
        original_draft = form_event.to_draft()
        dialog = EventEditDialog(
            self,
            calendar,
            form_event,
            allow_recurrence_edit=scope in {"single", "series"},
        )
        try:
            result = dialog.ShowModal()
            draft = dialog.get_draft()
        finally:
            dialog.Destroy()
        if result != wx.ID_OK or draft is None:
            return
        if draft == original_draft:
            self._show_message(
                tr("Nie wprowadzono żadnych zmian."),
                tr("Edycja wydarzenia"),
            )
            return

        notices: list[str] = []
        if scope == "instance":
            notices.append(
                tr(
                    "Zmiana obejmie tylko wybrane wystąpienie. Pozostałe terminy cyklu i reguła powtarzania pozostaną bez zmian."
                )
            )
        elif scope == "single" and draft.recurrence.is_recurring:
            notices.append(
                tr(
                    "To pojedyncze wydarzenie zostanie zamienione w cykl zgodnie z wybraną regułą powtarzania."
                )
            )
        elif scope == "series":
            notices.append(
                tr(
                    "Zmiana obejmie cały cykl, w tym jego tytuł, termin i podstawową regułę powtarzania."
                )
            )
            if not draft.recurrence.is_recurring:
                notices.append(
                    tr(
                        "Wybrano opcję „Nie powtarza się”. Cały cykl zostanie zamieniony w jedno wydarzenie w dacie początku serii."
                    )
                )
        if selected_instance.has_attendees:
            notices.append(
                tr(
                    "Wydarzenie ma uczestników. Google wyśle im aktualizację po zapisaniu zmian."
                )
            )
        recurrence = (
            draft.recurrence.display_text()
            if scope == "series" or (scope == "single" and draft.recurrence.is_recurring)
            else tr("Nie dotyczy")
        )
        confirm = wx.MessageDialog(
            self,
            tr(
                "Czy zapisać zmiany w wydarzeniu?\n\nTytuł: {title}\nKalendarz: {calendar}\nNowy termin: {when}\nPowtarzanie: {recurrence}\n\n{notice}",
                title=draft.title,
                calendar=calendar.name,
                when=self._draft_when_text(draft),
                recurrence=recurrence,
                notice="\n\n".join(notices),
            ).rstrip(),
            tr("Potwierdź edycję wydarzenia"),
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION,
        )
        try:
            confirmed = confirm.ShowModal()
        finally:
            confirm.Destroy()
        if confirmed != wx.ID_YES:
            return

        selected_day = self.selected_date

        def update() -> tuple[CalendarEvent, str, dt.date]:
            credentials = oauth.ensure_valid_credentials()
            if credentials is None:
                raise RuntimeError(tr("Brak ważnego logowania Google."))
            gateway = CalendarGateway(credentials)
            if scope == "series":
                updated = gateway.update_recurring_series(
                    calendar,
                    selected_instance,
                    draft,
                )
            else:
                updated = gateway.update_event(calendar, selected_instance, draft)
            result_scope = (
                "converted"
                if scope == "single" and draft.recurrence.is_recurring
                else scope
            )
            return updated, result_scope, selected_day

        busy = (
            tr("Zapisywanie zmian w całym cyklu: {title}...", title=draft.title)
            if scope == "series"
            else tr("Zapisywanie zmian w wydarzeniu: {title}...", title=draft.title)
        )
        self._run_task(
            busy_message=busy,
            target=update,
            on_success=self._after_update,
        )

    def _after_update(
        self,
        result: tuple[CalendarEvent, str, dt.date],
    ) -> None:
        updated, scope, selected_day = result
        if scope in {"series", "converted"}:
            self.current_year = selected_day.year
            self.current_month = selected_day.month
            self.selected_date = selected_day
            self._focus_event_after_refresh = None
            self._focus_events_after_refresh = True
            if scope == "converted":
                message = tr(
                    "Wydarzenie „{title}” zostało zamienione w cykl.",
                    title=updated.title,
                )
            else:
                message = tr(
                    "Zmiany w całym cyklu „{title}” zostały zapisane.",
                    title=updated.title,
                )
        else:
            self.current_year = updated.start_date.year
            self.current_month = updated.start_date.month
            self.selected_date = updated.start_date
            self._focus_event_after_refresh = updated.event_id
            message = tr(
                "Zmiany w wydarzeniu „{title}” zostały zapisane.",
                title=updated.title,
            )
        self._show_message(message, tr("Edycja zakończona"))
        self._refresh_google()

    def _choose_recurring_delete_scope(self) -> str | None:
        choices = [
            tr("Usuń tylko to wystąpienie"),
            tr("Usuń to i wszystkie kolejne wystąpienia"),
            tr("Usuń cały cykl"),
        ]
        dialog = wx.SingleChoiceDialog(
            self,
            tr(
                "Wybierz zakres usuwania wydarzenia cyklicznego. Domyślnie zaznaczone jest najbezpieczniejsze usunięcie jednego terminu."
            ),
            tr("Zakres usuwania cyklu"),
            choices,
        )
        dialog.SetName(tr("Zakres usuwania wydarzenia cyklicznego"))
        dialog.SetSelection(0)
        try:
            result = dialog.ShowModal()
            selection = dialog.GetSelection()
        finally:
            dialog.Destroy()
        if result != wx.ID_OK or selection < 0:
            return None
        return ("single", "following", "series")[selection]

    def _on_delete(self, event: wx.Event) -> None:
        if not oauth.is_logged_in():
            self._show_message(
                tr("Najpierw zaloguj się do Google."),
                tr("Logowanie wymagane"),
                error=True,
            )
            return

        selected = self._selected_event()
        if selected is None:
            self._show_message(
                tr("Dla tego dnia nie ma zaznaczonego wydarzenia."),
                tr("Nie można usunąć wydarzenia"),
                error=True,
            )
            return

        calendar = self._calendar_for_event(selected)
        if calendar is None:
            self._show_message(
                tr(
                    "Nie znaleziono kalendarza tego wydarzenia. Odśwież dane i spróbuj ponownie."
                ),
                tr("Nie można usunąć wydarzenia"),
                error=True,
            )
            return

        if not calendar.can_write:
            self._show_message(
                tr(
                    "Kalendarz {calendar} jest dostępny tylko do odczytu i nie pozwala usuwać wydarzeń.",
                    calendar=calendar.name,
                ),
                tr("Brak uprawnień do usuwania"),
                error=True,
            )
            return

        if not selected.supports_delete:
            self._show_message(
                tr(
                    "Google oznaczył to wydarzenie jako zablokowane i nie pozwala go usunąć."
                ),
                tr("Nie można usunąć wydarzenia"),
                error=True,
            )
            return

        scope = "single"
        if selected.is_recurring_instance:
            scope = self._choose_recurring_delete_scope()
            if scope is None:
                self.events_list.SetFocus()
                return

        scope_text = {
            "single": (
                tr(
                    "Usunięte zostanie tylko zaznaczone wystąpienie. Pozostałe terminy cyklu pozostaną bez zmian."
                )
                if selected.is_recurring_instance
                else tr("Usunięte zostanie to wydarzenie.")
            ),
            "following": tr(
                "Usunięte zostanie zaznaczone wystąpienie oraz wszystkie późniejsze terminy tej serii. Wcześniejsze wystąpienia pozostaną. Jeżeli zaznaczony termin jest pierwszym wystąpieniem, skutek będzie równy usunięciu całego cyklu."
            ),
            "series": tr(
                "Usunięty zostanie cały cykl: wcześniejsze, zaznaczone i wszystkie późniejsze wystąpienia."
            ),
        }[scope]

        notices: list[str] = [scope_text]
        if selected.has_attendees:
            notices.append(
                tr(
                    "Wydarzenie ma uczestników. Google wyśle im informację o anulowaniu."
                )
            )
        if selected.event_type != "default":
            event_type_labels = {
                "birthday": tr("urodziny"),
                "focusTime": tr("czas skupienia"),
                "fromGmail": tr("wydarzenie utworzone z Gmaila"),
                "outOfOffice": tr("poza biurem"),
                "workingLocation": tr("miejsce pracy"),
            }
            kind = event_type_labels.get(selected.event_type, selected.event_type)
            notices.append(
                tr("To jest specjalny typ wydarzenia: {kind}.", kind=kind)
            )

        confirm_title = {
            "single": tr("Potwierdź usunięcie wydarzenia"),
            "following": tr("Potwierdź usunięcie tego i kolejnych wystąpień"),
            "series": tr("Potwierdź usunięcie całego cyklu"),
        }[scope]
        confirm = wx.MessageDialog(
            self,
            tr(
                "Czy na pewno wykonać tę operację?\n\n{details}\n\n{notices}\n\nTej operacji nie można cofnąć w aplikacji PT Calendar Manager.",
                details=selected.details_text(),
                notices="\n".join(notices),
            ),
            confirm_title,
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING,
        )
        try:
            confirmed = confirm.ShowModal()
        finally:
            confirm.Destroy()

        if confirmed != wx.ID_YES:
            self.events_list.SetFocus()
            return

        deleted_title = selected.title
        deleted_calendar_name = calendar.name
        deleted_date = self.selected_date

        def delete() -> tuple[str, str, dt.date, str, bool]:
            credentials = oauth.ensure_valid_credentials()
            if credentials is None:
                raise RuntimeError(tr("Brak ważnego logowania Google."))
            gateway = CalendarGateway(credentials)
            parent_deleted = False
            if scope == "series":
                gateway.delete_recurring_series(calendar, selected)
            elif scope == "following":
                parent_deleted = gateway.delete_recurring_from(calendar, selected)
            else:
                gateway.delete_event(calendar, selected)
            return (
                deleted_title,
                deleted_calendar_name,
                deleted_date,
                scope,
                parent_deleted,
            )

        busy_text = {
            "single": tr("Usuwanie wydarzenia: {title}...", title=selected.title),
            "following": tr(
                "Usuwanie tego i kolejnych wystąpień: {title}...",
                title=selected.title,
            ),
            "series": tr("Usuwanie całego cyklu: {title}...", title=selected.title),
        }[scope]
        self._run_task(
            busy_message=busy_text,
            target=delete,
            on_success=self._after_delete,
        )

    def _after_delete(
        self,
        result: tuple[str, str, dt.date, str, bool],
    ) -> None:
        title, calendar_name, selected_date, scope, parent_deleted = result
        self.selected_date = selected_date
        self.current_year = selected_date.year
        self.current_month = selected_date.month
        self._focus_event_after_refresh = None
        self._focus_events_after_refresh = True

        if scope == "series":
            message = tr(
                "Cały cykl „{title}” został usunięty z kalendarza {calendar}.",
                title=title,
                calendar=calendar_name,
            )
        elif scope == "following":
            if parent_deleted:
                message = tr(
                    "Zaznaczony termin był pierwszym wystąpieniem. Cały cykl „{title}” został usunięty z kalendarza {calendar}.",
                    title=title,
                    calendar=calendar_name,
                )
            else:
                message = tr(
                    "Zaznaczone i wszystkie kolejne wystąpienia „{title}” zostały usunięte z kalendarza {calendar}.",
                    title=title,
                    calendar=calendar_name,
                )
        else:
            message = tr(
                "Wybrane wydarzenie „{title}” zostało usunięte z kalendarza {calendar}.",
                title=title,
                calendar=calendar_name,
            )

        self._show_message(message, tr("Usuwanie zakończone"))
        self._refresh_google()

    @staticmethod
    def _copy_to_clipboard(text: str) -> bool:
        if not text:
            return False
        try:
            if not wx.TheClipboard.Open():
                return False
            try:
                copied = bool(wx.TheClipboard.SetData(wx.TextDataObject(text)))
                if copied:
                    wx.TheClipboard.Flush()
                return copied
            finally:
                wx.TheClipboard.Close()
        except Exception:
            return False

    def _open_web_link(self, url: str, description: str) -> None:
        try:
            opened = webbrowser.open_new_tab(url)
        except Exception as error:
            self._show_message(
                tr(
                    "Nie udało się otworzyć {description}.\n\n{error}",
                    description=description,
                    error=error,
                ),
                tr("Otwieranie linku"),
                error=True,
            )
            return
        if not opened:
            self._show_message(
                tr(
                    "System nie potwierdził otwarcia {description}.",
                    description=description,
                ),
                tr("Otwieranie linku"),
                error=True,
            )
            return
        self._set_status(
            tr(
                "Otwarto {description} w domyślnej przeglądarce.",
                description=description,
            )
        )

    def _on_open_google(self, event: wx.Event) -> None:
        selected = self._selected_event()
        if selected is None or not selected.can_open_in_google:
            self._show_message(
                tr(
                    "Dla zaznaczonego wydarzenia nie ma dostępnego odnośnika do Kalendarza Google."
                ),
                tr("Otwórz w Google"),
                error=True,
            )
            return
        self._open_web_link(
            selected.html_link,
            tr("wydarzenie w Kalendarzu Google"),
        )

    def _on_meeting_link(self, event: wx.Event) -> None:
        selected = self._selected_event()
        if selected is None or not selected.has_meeting_link:
            self._show_message(
                tr(
                    "Zaznaczone wydarzenie nie zawiera obsługiwanego linku spotkania."
                ),
                tr("Link spotkania"),
                error=True,
            )
            return

        dialog = MeetingLinkDialog(
            self,
            selected.meeting_label,
            selected.meeting_url,
        )
        try:
            result = dialog.ShowModal()
            action = dialog.action
        finally:
            dialog.Destroy()

        if result != wx.ID_OK:
            self.events_list.SetFocus()
            return
        if action == "open":
            self._open_web_link(selected.meeting_url, tr("link spotkania"))
        elif action == "copy":
            if self._copy_to_clipboard(selected.meeting_url):
                self._show_message(
                    tr("Link spotkania został skopiowany do schowka."),
                    tr("Link spotkania"),
                )
            else:
                self._show_message(
                    tr("Nie udało się skopiować linku spotkania do schowka."),
                    tr("Link spotkania"),
                    error=True,
                )
        self.events_list.SetFocus()

    def _on_details(self, event: wx.Event) -> None:
        selected = self._selected_event()
        if selected is None:
            self._show_message(
                tr("Dla tego dnia nie ma zaznaczonego wydarzenia."),
                tr("Szczegóły"),
                error=True,
            )
            return
        dialog = wx.Dialog(
            self,
            title=tr("Szczegóły wydarzenia"),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
        )
        sizer = wx.BoxSizer(wx.VERTICAL)
        text = wx.TextCtrl(
            dialog,
            value=selected.details_text(),
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_DONTWRAP,
        )
        text.SetName(tr("Szczegóły wydarzenia"))
        text.SetMinSize((620, 300))
        sizer.Add(text, 1, wx.ALL | wx.EXPAND, 12)
        close = wx.Button(dialog, wx.ID_OK, localized("&Zamknij", "&Close"))
        close_accessible = apply_accessible_name(
            close,
            tr("Zamknij"),
            tr("Zamyka szczegóły wydarzenia."),
            self._access_key("Alt+Z", "Alt+C"),
        )
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

    def _show_message(self, message: str, title: str, *, error: bool = False) -> None:
        style = wx.OK | (wx.ICON_ERROR if error else wx.ICON_INFORMATION)
        dialog = wx.MessageDialog(self, message, title, style)
        try:
            dialog.ShowModal()
        finally:
            dialog.Destroy()


class PTCalendarManagerApp(wx.App):
    def OnInit(self) -> bool:
        self.SetAppName(PRODUCT_NAME)
        frame = MainFrame()
        frame.Show()
        self.SetTopWindow(frame)
        return True


def main() -> None:
    app = PTCalendarManagerApp(redirect=False)
    app.MainLoop()
