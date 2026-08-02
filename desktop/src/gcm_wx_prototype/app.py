from __future__ import annotations

import datetime as dt
from dataclasses import dataclass

import wx

from .model import (
    CalendarEvent,
    EventStore,
    count_text,
    format_day_item,
    format_full_date,
    format_month,
    parse_polish_date,
    parse_time,
)


APP_TITLE = "GCM by Piotrek — prototyp dostępności"


@dataclass(slots=True)
class EventFormData:
    title: str
    date: dt.date
    all_day: bool
    start_time: dt.time | None
    end_time: dt.time | None
    calendar_name: str
    location: str
    description: str


class EventDialog(wx.Dialog):
    def __init__(
        self,
        parent: wx.Window,
        *,
        title: str,
        default_date: dt.date,
        event: CalendarEvent | None = None,
    ) -> None:
        super().__init__(
            parent,
            title=title,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
        )

        self._result: EventFormData | None = None

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        form = wx.FlexGridSizer(cols=2, vgap=8, hgap=12)
        form.AddGrowableCol(1, 1)

        self.title_ctrl = wx.TextCtrl(self, value=event.title if event else "")
        self.title_ctrl.SetName("Tytuł wydarzenia")

        event_date = event.date if event else default_date
        self.date_ctrl = wx.TextCtrl(self, value=event_date.strftime("%d.%m.%Y"))
        self.date_ctrl.SetName("Data wydarzenia, format dzień miesiąc rok")

        self.all_day_ctrl = wx.CheckBox(self, label="Wydarzenie całodniowe")
        self.all_day_ctrl.SetValue(bool(event.all_day) if event else False)
        self.all_day_ctrl.SetName("Wydarzenie całodniowe")

        start_value = (
            event.start_time.strftime("%H:%M")
            if event and event.start_time
            else "09:00"
        )
        end_value = (
            event.end_time.strftime("%H:%M")
            if event and event.end_time
            else "10:00"
        )
        self.start_ctrl = wx.TextCtrl(self, value=start_value)
        self.start_ctrl.SetName("Godzina rozpoczęcia, format godzina dwukropek minuty")
        self.end_ctrl = wx.TextCtrl(self, value=end_value)
        self.end_ctrl.SetName("Godzina zakończenia, format godzina dwukropek minuty")

        calendars = ["Mój kalendarz", "Familijne", "Praca"]
        current_calendar = event.calendar_name if event else "Mój kalendarz"
        if current_calendar not in calendars:
            calendars.append(current_calendar)
        self.calendar_ctrl = wx.Choice(self, choices=calendars)
        self.calendar_ctrl.SetSelection(calendars.index(current_calendar))
        self.calendar_ctrl.SetName("Kalendarz")

        self.location_ctrl = wx.TextCtrl(
            self,
            value=event.location if event else "",
        )
        self.location_ctrl.SetName("Lokalizacja")

        self.description_ctrl = wx.TextCtrl(
            self,
            value=event.description if event else "",
            style=wx.TE_MULTILINE,
        )
        self.description_ctrl.SetMinSize((420, 100))
        self.description_ctrl.SetName("Opis wydarzenia")

        def add_row(label: str, control: wx.Window) -> None:
            label_ctrl = wx.StaticText(self, label=label)
            label_ctrl.SetName(label)
            form.Add(label_ctrl, 0, wx.ALIGN_CENTER_VERTICAL)
            form.Add(control, 1, wx.EXPAND)

        add_row("Tytuł:", self.title_ctrl)
        add_row("Data, DD.MM.RRRR:", self.date_ctrl)

        form.Add(wx.StaticText(self, label="Typ wydarzenia:"), 0, wx.ALIGN_CENTER_VERTICAL)
        form.Add(self.all_day_ctrl, 1, wx.EXPAND)

        add_row("Godzina rozpoczęcia, GG:MM:", self.start_ctrl)
        add_row("Godzina zakończenia, GG:MM:", self.end_ctrl)
        add_row("Kalendarz:", self.calendar_ctrl)
        add_row("Lokalizacja:", self.location_ctrl)
        add_row("Opis:", self.description_ctrl)

        main_sizer.Add(form, 1, wx.ALL | wx.EXPAND, 12)

        buttons = wx.StdDialogButtonSizer()
        self.save_button = wx.Button(self, wx.ID_OK, "Zapisz")
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, "Anuluj")
        self.save_button.SetDefault()
        buttons.AddButton(self.save_button)
        buttons.AddButton(self.cancel_button)
        buttons.Realize()
        main_sizer.Add(buttons, 0, wx.ALL | wx.ALIGN_RIGHT, 12)

        self.SetSizerAndFit(main_sizer)
        self.SetMinSize((600, 500))
        self.SetSize((700, 560))
        self.CentreOnParent()

        self.all_day_ctrl.Bind(wx.EVT_CHECKBOX, self._on_all_day_changed)
        self.save_button.Bind(wx.EVT_BUTTON, self._on_save)

        self._update_time_enabled()
        wx.CallAfter(self.title_ctrl.SetFocus)

    def _on_all_day_changed(self, event: wx.CommandEvent) -> None:
        self._update_time_enabled()
        event.Skip()

    def _update_time_enabled(self) -> None:
        enabled = not self.all_day_ctrl.GetValue()
        self.start_ctrl.Enable(enabled)
        self.end_ctrl.Enable(enabled)

    def _show_error(self, message: str) -> None:
        dialog = wx.MessageDialog(
            self,
            message,
            "Nieprawidłowe dane",
            wx.OK | wx.ICON_ERROR,
        )
        try:
            dialog.ShowModal()
        finally:
            dialog.Destroy()

    def _on_save(self, event: wx.CommandEvent) -> None:
        title = self.title_ctrl.GetValue().strip()
        if not title:
            self._show_error("Wpisz tytuł wydarzenia.")
            self.title_ctrl.SetFocus()
            return

        try:
            event_date = parse_polish_date(self.date_ctrl.GetValue())
        except ValueError as error:
            self._show_error(str(error))
            self.date_ctrl.SetFocus()
            return

        all_day = self.all_day_ctrl.GetValue()
        start_time = None
        end_time = None
        if not all_day:
            try:
                start_time = parse_time(self.start_ctrl.GetValue())
                end_time = parse_time(self.end_ctrl.GetValue())
            except ValueError as error:
                self._show_error(str(error))
                return
            if end_time <= start_time:
                self._show_error("Godzina zakończenia musi być późniejsza od rozpoczęcia.")
                self.end_ctrl.SetFocus()
                return

        selection = self.calendar_ctrl.GetSelection()
        calendar_name = (
            self.calendar_ctrl.GetString(selection)
            if selection != wx.NOT_FOUND
            else "Mój kalendarz"
        )

        self._result = EventFormData(
            title=title,
            date=event_date,
            all_day=all_day,
            start_time=start_time,
            end_time=end_time,
            calendar_name=calendar_name,
            location=self.location_ctrl.GetValue().strip(),
            description=self.description_ctrl.GetValue().strip(),
        )
        self.EndModal(wx.ID_OK)

    def get_data(self) -> EventFormData | None:
        return self._result


class SearchResultsDialog(wx.Dialog):
    def __init__(
        self,
        parent: wx.Window,
        events: list[CalendarEvent],
    ) -> None:
        super().__init__(
            parent,
            title="Wyniki wyszukiwania",
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
        )
        self._events = events
        self.selected_event: CalendarEvent | None = None

        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(
            self,
            label=f"Znaleziono: {count_text(len(events))}.",
        )
        sizer.Add(label, 0, wx.ALL | wx.EXPAND, 12)

        choices = [
            f"{format_full_date(event.date)}, {event.display_text()}"
            for event in events
        ]
        self.results_list = wx.ListBox(self, choices=choices, style=wx.LB_SINGLE)
        self.results_list.SetName(
            f"Wyniki wyszukiwania, {len(events)} elementów"
        )
        self.results_list.SetMinSize((650, 260))
        if events:
            self.results_list.SetSelection(0)
        sizer.Add(self.results_list, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 12)

        buttons = wx.StdDialogButtonSizer()
        self.open_button = wx.Button(self, wx.ID_OK, "Przejdź do wydarzenia")
        self.close_button = wx.Button(self, wx.ID_CANCEL, "Zamknij")
        self.open_button.Enable(bool(events))
        self.open_button.SetDefault()
        buttons.AddButton(self.open_button)
        buttons.AddButton(self.close_button)
        buttons.Realize()
        sizer.Add(buttons, 0, wx.ALL | wx.ALIGN_RIGHT, 12)

        self.SetSizerAndFit(sizer)
        self.SetMinSize((700, 390))
        self.SetSize((760, 440))
        self.CentreOnParent()

        self.open_button.Bind(wx.EVT_BUTTON, self._on_open)
        self.results_list.Bind(wx.EVT_LISTBOX_DCLICK, self._on_open)

        wx.CallAfter(
            (self.results_list if events else self.close_button).SetFocus
        )

    def _on_open(self, event: wx.Event) -> None:
        selection = self.results_list.GetSelection()
        if 0 <= selection < len(self._events):
            self.selected_event = self._events[selection]
            self.EndModal(wx.ID_OK)


class MainFrame(wx.Frame):
    def __init__(self) -> None:
        super().__init__(
            None,
            title=APP_TITLE,
            size=(1050, 650),
            style=wx.DEFAULT_FRAME_STYLE,
        )

        self.store = EventStore()
        today = dt.date.today()
        self.current_year = today.year
        self.current_month = today.month
        self.selected_date = today
        self._day_values: list[dt.date] = []
        self._event_values: list[CalendarEvent] = []

        panel = wx.Panel(self)
        panel.SetName("Główne okno aplikacji")

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        top_buttons = wx.BoxSizer(wx.HORIZONTAL)
        self.previous_button = wx.Button(panel, label="Poprzedni miesiąc")
        self.today_button = wx.Button(panel, label="Dzisiaj")
        self.next_button = wx.Button(panel, label="Następny miesiąc")
        self.month_label = wx.StaticText(panel, label="")
        self.goto_button = wx.Button(panel, label="Przejdź do daty")
        self.search_button = wx.Button(panel, label="Wyszukaj")
        self.add_button = wx.Button(panel, label="Dodaj wydarzenie")
        self.refresh_button = wx.Button(panel, label="Odśwież")

        for button in (
            self.previous_button,
            self.today_button,
            self.next_button,
        ):
            top_buttons.Add(button, 0, wx.RIGHT, 6)

        top_buttons.Add(self.month_label, 1, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 12)

        for button in (
            self.goto_button,
            self.search_button,
            self.add_button,
            self.refresh_button,
        ):
            top_buttons.Add(button, 0, wx.LEFT, 6)

        main_sizer.Add(top_buttons, 0, wx.ALL | wx.EXPAND, 12)

        content_sizer = wx.BoxSizer(wx.HORIZONTAL)

        days_box = wx.StaticBoxSizer(wx.VERTICAL, panel, "Dni miesiąca")
        self.days_list = wx.ListBox(panel, style=wx.LB_SINGLE)
        self.days_list.SetName("Dni miesiąca")
        self.days_list.SetMinSize((420, 420))
        self.days_list.SetHelpText(
            "Strzałkami wybierz dzień. Enter przenosi do listy wydarzeń."
        )
        days_box.Add(self.days_list, 1, wx.ALL | wx.EXPAND, 8)
        content_sizer.Add(days_box, 1, wx.RIGHT | wx.EXPAND, 8)

        events_box = wx.StaticBoxSizer(wx.VERTICAL, panel, "Wydarzenia wybranego dnia")
        self.events_list = wx.ListBox(panel, style=wx.LB_SINGLE)
        self.events_list.SetName("Wydarzenia wybranego dnia")
        self.events_list.SetMinSize((520, 360))
        self.events_list.SetHelpText(
            "Strzałkami wybierz wydarzenie. Enter pokazuje szczegóły."
        )
        events_box.Add(self.events_list, 1, wx.ALL | wx.EXPAND, 8)

        event_buttons = wx.BoxSizer(wx.HORIZONTAL)
        self.details_button = wx.Button(panel, label="Pokaż szczegóły")
        self.edit_button = wx.Button(panel, label="Edytuj")
        self.delete_button = wx.Button(panel, label="Usuń")
        event_buttons.Add(self.details_button, 0, wx.RIGHT, 8)
        event_buttons.Add(self.edit_button, 0, wx.RIGHT, 8)
        event_buttons.Add(self.delete_button, 0)
        events_box.Add(event_buttons, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 8)
        content_sizer.Add(events_box, 1, wx.LEFT | wx.EXPAND, 8)

        main_sizer.Add(content_sizer, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 12)

        panel.SetSizer(main_sizer)

        self.status_bar = self.CreateStatusBar()
        self.status_bar.SetName("Stan aplikacji")

        self._bind_events()
        self._install_accelerators()
        self._load_month(select_date=today)

        self.Centre()
        wx.CallAfter(self.days_list.SetFocus)

    def _bind_events(self) -> None:
        self.previous_button.Bind(wx.EVT_BUTTON, self._on_previous_month)
        self.today_button.Bind(wx.EVT_BUTTON, self._on_today)
        self.next_button.Bind(wx.EVT_BUTTON, self._on_next_month)
        self.goto_button.Bind(wx.EVT_BUTTON, self._on_goto_date)
        self.search_button.Bind(wx.EVT_BUTTON, self._on_search)
        self.add_button.Bind(wx.EVT_BUTTON, self._on_add)
        self.refresh_button.Bind(wx.EVT_BUTTON, self._on_refresh)

        self.days_list.Bind(wx.EVT_LISTBOX, self._on_day_selected)
        self.days_list.Bind(wx.EVT_LISTBOX_DCLICK, self._focus_events)
        self.days_list.Bind(wx.EVT_KEY_DOWN, self._on_days_key)

        self.events_list.Bind(wx.EVT_LISTBOX, self._on_event_selected)
        self.events_list.Bind(wx.EVT_LISTBOX_DCLICK, self._on_details)
        self.events_list.Bind(wx.EVT_KEY_DOWN, self._on_events_key)

        self.details_button.Bind(wx.EVT_BUTTON, self._on_details)
        self.edit_button.Bind(wx.EVT_BUTTON, self._on_edit)
        self.delete_button.Bind(wx.EVT_BUTTON, self._on_delete)

    def _install_accelerators(self) -> None:
        self.id_add = wx.NewIdRef()
        self.id_edit = wx.NewIdRef()
        self.id_delete = wx.NewIdRef()
        self.id_search = wx.NewIdRef()
        self.id_goto = wx.NewIdRef()
        self.id_today = wx.NewIdRef()
        self.id_refresh = wx.NewIdRef()
        self.id_previous = wx.NewIdRef()
        self.id_next = wx.NewIdRef()

        entries = [
            (wx.ACCEL_CTRL, ord("N"), self.id_add),
            (wx.ACCEL_CTRL, ord("E"), self.id_edit),
            (wx.ACCEL_NORMAL, wx.WXK_DELETE, self.id_delete),
            (wx.ACCEL_CTRL, ord("F"), self.id_search),
            (wx.ACCEL_CTRL, ord("G"), self.id_goto),
            (wx.ACCEL_CTRL, ord("D"), self.id_today),
            (wx.ACCEL_NORMAL, wx.WXK_F5, self.id_refresh),
            (wx.ACCEL_ALT, wx.WXK_LEFT, self.id_previous),
            (wx.ACCEL_ALT, wx.WXK_RIGHT, self.id_next),
        ]
        self.SetAcceleratorTable(wx.AcceleratorTable(entries))

        self.Bind(wx.EVT_MENU, self._on_add, id=self.id_add)
        self.Bind(wx.EVT_MENU, self._on_edit, id=self.id_edit)
        self.Bind(wx.EVT_MENU, self._on_delete, id=self.id_delete)
        self.Bind(wx.EVT_MENU, self._on_search, id=self.id_search)
        self.Bind(wx.EVT_MENU, self._on_goto_date, id=self.id_goto)
        self.Bind(wx.EVT_MENU, self._on_today, id=self.id_today)
        self.Bind(wx.EVT_MENU, self._on_refresh, id=self.id_refresh)
        self.Bind(wx.EVT_MENU, self._on_previous_month, id=self.id_previous)
        self.Bind(wx.EVT_MENU, self._on_next_month, id=self.id_next)

    def _set_status(self, text: str) -> None:
        self.status_bar.SetStatusText(text)

    def _load_month(self, *, select_date: dt.date | None = None) -> None:
        first = dt.date(self.current_year, self.current_month, 1)
        self.month_label.SetLabel(format_month(first))
        self.month_label.SetName(f"Wybrany miesiąc: {format_month(first)}")

        self._day_values = self.store.month_days(
            self.current_year,
            self.current_month,
        )
        labels = [
            format_day_item(day, len(self.store.events_for_date(day)))
            for day in self._day_values
        ]
        self.days_list.Set(labels)

        if select_date and (
            select_date.year == self.current_year
            and select_date.month == self.current_month
        ):
            index = select_date.day - 1
        else:
            index = 0

        if self._day_values:
            index = max(0, min(index, len(self._day_values) - 1))
            self.days_list.SetSelection(index)
            self.selected_date = self._day_values[index]
        self._load_events_for_selected_day()
        self._set_status(
            f"Wybrano miesiąc {format_month(first)}. "
            f"Lista zawiera {len(self._day_values)} dni."
        )

    def _load_events_for_selected_day(
        self,
        *,
        select_event_id: str | None = None,
    ) -> None:
        self._event_values = self.store.events_for_date(self.selected_date)
        self.events_list.Set(
            [event.display_text() for event in self._event_values]
        )
        self.events_list.SetName(
            f"Wydarzenia dla {format_full_date(self.selected_date)}, "
            f"{count_text(len(self._event_values))}"
        )

        selection = wx.NOT_FOUND
        if select_event_id:
            for index, event in enumerate(self._event_values):
                if event.event_id == select_event_id:
                    selection = index
                    break
        if selection == wx.NOT_FOUND and self._event_values:
            selection = 0
        if selection != wx.NOT_FOUND:
            self.events_list.SetSelection(selection)

        enabled = bool(self._event_values)
        self.details_button.Enable(enabled)
        self.edit_button.Enable(enabled)
        self.delete_button.Enable(enabled)
        self._set_status(
            f"{format_full_date(self.selected_date)}: "
            f"{count_text(len(self._event_values))}."
        )

    def _selected_event(self) -> CalendarEvent | None:
        selection = self.events_list.GetSelection()
        if 0 <= selection < len(self._event_values):
            return self._event_values[selection]
        return None

    def _on_day_selected(self, event: wx.CommandEvent) -> None:
        selection = self.days_list.GetSelection()
        if 0 <= selection < len(self._day_values):
            self.selected_date = self._day_values[selection]
            self._load_events_for_selected_day()
        event.Skip()

    def _on_event_selected(self, event: wx.CommandEvent) -> None:
        selected = self._selected_event()
        if selected:
            self._set_status(f"Wybrano wydarzenie: {selected.display_text()}.")
        event.Skip()

    def _on_days_key(self, event: wx.KeyEvent) -> None:
        if event.GetKeyCode() in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            self._focus_events(event)
            return
        event.Skip()

    def _on_events_key(self, event: wx.KeyEvent) -> None:
        key = event.GetKeyCode()
        if key in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            self._on_details(event)
            return
        event.Skip()

    def _focus_events(self, event: wx.Event) -> None:
        self.events_list.SetFocus()
        if not self._event_values:
            self._set_status(
                f"{format_full_date(self.selected_date)}: brak wydarzeń."
            )

    def _change_month(self, offset: int) -> None:
        month_index = self.current_year * 12 + (self.current_month - 1) + offset
        self.current_year, zero_based_month = divmod(month_index, 12)
        self.current_month = zero_based_month + 1
        self._load_month()

    def _on_previous_month(self, event: wx.Event) -> None:
        self._change_month(-1)

    def _on_next_month(self, event: wx.Event) -> None:
        self._change_month(1)

    def _on_today(self, event: wx.Event) -> None:
        today = dt.date.today()
        self.current_year = today.year
        self.current_month = today.month
        self._load_month(select_date=today)
        self.days_list.SetFocus()

    def _on_refresh(self, event: wx.Event) -> None:
        current = self.selected_date
        selected_event = self._selected_event()
        self._load_month(select_date=current)
        if selected_event:
            self._load_events_for_selected_day(
                select_event_id=selected_event.event_id
            )
        self._set_status("Dane zostały odświeżone.")

    def _on_goto_date(self, event: wx.Event) -> None:
        dialog = wx.TextEntryDialog(
            self,
            "Wpisz datę w formacie DD.MM.RRRR.",
            "Przejdź do daty",
            self.selected_date.strftime("%d.%m.%Y"),
        )
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
        self.current_year = target.year
        self.current_month = target.month
        self._load_month(select_date=target)
        self.days_list.SetFocus()

    def _on_search(self, event: wx.Event) -> None:
        dialog = wx.TextEntryDialog(
            self,
            "Wpisz fragment tytułu, lokalizacji, opisu albo nazwy kalendarza.",
            "Wyszukaj wydarzenia",
            "",
        )
        try:
            result = dialog.ShowModal()
            query = dialog.GetValue().strip()
        finally:
            dialog.Destroy()
        if result != wx.ID_OK:
            return
        if not query:
            self._show_message(
                "Wpisz tekst do wyszukania.",
                "Wyszukiwanie",
                error=True,
            )
            return

        results = self.store.search(query)
        results_dialog = SearchResultsDialog(self, results)
        try:
            result = results_dialog.ShowModal()
            selected = results_dialog.selected_event
        finally:
            results_dialog.Destroy()
        if result == wx.ID_OK and selected:
            self.current_year = selected.date.year
            self.current_month = selected.date.month
            self._load_month(select_date=selected.date)
            self._load_events_for_selected_day(
                select_event_id=selected.event_id
            )
            self.events_list.SetFocus()

    def _on_add(self, event: wx.Event) -> None:
        dialog = EventDialog(
            self,
            title="Dodaj wydarzenie",
            default_date=self.selected_date,
        )
        try:
            result = dialog.ShowModal()
            data = dialog.get_data()
        finally:
            dialog.Destroy()
        if result != wx.ID_OK or data is None:
            return

        created = self.store.add_event(
            date=data.date,
            title=data.title,
            calendar_name=data.calendar_name,
            all_day=data.all_day,
            start_time=data.start_time,
            end_time=data.end_time,
            location=data.location,
            description=data.description,
        )
        self.current_year = created.date.year
        self.current_month = created.date.month
        self._load_month(select_date=created.date)
        self._load_events_for_selected_day(select_event_id=created.event_id)
        self.events_list.SetFocus()
        self._set_status(f"Dodano wydarzenie: {created.title}.")

    def _on_edit(self, event: wx.Event) -> None:
        selected = self._selected_event()
        if not selected:
            self._show_message(
                "Najpierw zaznacz wydarzenie.",
                "Edycja wydarzenia",
                error=True,
            )
            return

        dialog = EventDialog(
            self,
            title="Edytuj wydarzenie",
            default_date=selected.date,
            event=selected,
        )
        try:
            result = dialog.ShowModal()
            data = dialog.get_data()
        finally:
            dialog.Destroy()
        if result != wx.ID_OK or data is None:
            return

        updated = self.store.update_event(
            selected.event_id,
            title=data.title,
            date=data.date,
            calendar_name=data.calendar_name,
            all_day=data.all_day,
            start_time=None if data.all_day else data.start_time,
            end_time=None if data.all_day else data.end_time,
            location=data.location,
            description=data.description,
        )
        self.current_year = updated.date.year
        self.current_month = updated.date.month
        self._load_month(select_date=updated.date)
        self._load_events_for_selected_day(select_event_id=updated.event_id)
        self.events_list.SetFocus()
        self._set_status(f"Zapisano wydarzenie: {updated.title}.")

    def _on_delete(self, event: wx.Event) -> None:
        selected = self._selected_event()
        if not selected:
            self._show_message(
                "Najpierw zaznacz wydarzenie.",
                "Usuwanie wydarzenia",
                error=True,
            )
            return

        dialog = wx.MessageDialog(
            self,
            f"Czy usunąć wydarzenie „{selected.title}”?",
            "Potwierdź usunięcie",
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING,
        )
        try:
            result = dialog.ShowModal()
        finally:
            dialog.Destroy()
        if result != wx.ID_YES:
            return

        title = selected.title
        self.store.delete_event(selected.event_id)
        self._load_month(select_date=self.selected_date)
        self.events_list.SetFocus()
        self._set_status(f"Usunięto wydarzenie: {title}.")

    def _on_details(self, event: wx.Event) -> None:
        selected = self._selected_event()
        if not selected:
            self._show_message(
                "Dla tego dnia nie ma zaznaczonego wydarzenia.",
                "Szczegóły wydarzenia",
                error=True,
            )
            return

        dialog = wx.Dialog(
            self,
            title="Szczegóły wydarzenia",
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
        )
        sizer = wx.BoxSizer(wx.VERTICAL)
        text = wx.TextCtrl(
            dialog,
            value=selected.details_text(),
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_DONTWRAP,
        )
        text.SetName("Szczegóły wydarzenia")
        text.SetMinSize((560, 260))
        sizer.Add(text, 1, wx.ALL | wx.EXPAND, 12)
        close_button = wx.Button(dialog, wx.ID_OK, "Zamknij")
        close_button.SetDefault()
        sizer.Add(close_button, 0, wx.ALL | wx.ALIGN_RIGHT, 12)
        dialog.SetSizerAndFit(sizer)
        dialog.SetMinSize((620, 380))
        dialog.SetSize((680, 430))
        dialog.CentreOnParent()
        try:
            wx.CallAfter(text.SetFocus)
            dialog.ShowModal()
        finally:
            dialog.Destroy()

    def _show_message(
        self,
        message: str,
        title: str,
        *,
        error: bool = False,
    ) -> None:
        style = wx.OK | (wx.ICON_ERROR if error else wx.ICON_INFORMATION)
        dialog = wx.MessageDialog(self, message, title, style)
        try:
            dialog.ShowModal()
        finally:
            dialog.Destroy()


class GcmPrototypeApp(wx.App):
    def OnInit(self) -> bool:
        self.SetAppName("GCM by Piotrek")
        frame = MainFrame()
        frame.Show()
        self.SetTopWindow(frame)
        return True


def main() -> None:
    app = GcmPrototypeApp(redirect=False)
    app.MainLoop()
