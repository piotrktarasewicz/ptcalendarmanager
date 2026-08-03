from __future__ import annotations

import datetime as dt

import wx

from .accessibility import apply_accessible_name

from gcm_core.models import (
    CalendarEvent,
    CalendarInfo,
    EventDraft,
    count_text,
    format_full_date,
    parse_polish_date,
    parse_polish_time,
)


class EventCreateDialog(wx.Dialog):
    def __init__(
        self,
        parent: wx.Window,
        calendars: list[CalendarInfo],
        default_date: dt.date,
        *,
        initial_event: CalendarEvent | None = None,
        title: str = "Dodaj wydarzenie",
        save_label: str = "Utwórz wydarzenie",
    ) -> None:
        super().__init__(
            parent,
            title=title,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
        )
        self._calendars = calendars
        self._draft: EventDraft | None = None
        self._accessible_objects: list[wx.Accessible] = []
        self._initial_event = initial_event

        initial_draft = initial_event.to_draft() if initial_event else None
        form_date = initial_draft.start_date if initial_draft else default_date
        end_date = initial_draft.end_date_inclusive if initial_draft else default_date

        sizer = wx.BoxSizer(wx.VERTICAL)
        form = wx.FlexGridSizer(cols=2, vgap=8, hgap=12)
        form.AddGrowableCol(1, 1)

        self.title_ctrl = wx.TextCtrl(
            self,
            value=initial_draft.title if initial_draft else "",
        )

        labels = [
            calendar.name + (", kalendarz główny" if calendar.primary else "")
            for calendar in calendars
        ]
        self.calendar_ctrl = wx.Choice(self, choices=labels)
        default_index = 0
        if initial_draft:
            default_index = next(
                (
                    index
                    for index, calendar in enumerate(calendars)
                    if calendar.calendar_id == initial_draft.calendar_id
                ),
                0,
            )
        else:
            default_index = next(
                (index for index, calendar in enumerate(calendars) if calendar.primary),
                0,
            )
        if calendars:
            self.calendar_ctrl.SetSelection(default_index)

        self.start_date_ctrl = wx.TextCtrl(
            self,
            value=form_date.strftime("%d.%m.%Y"),
        )

        self.all_day_ctrl = wx.CheckBox(self, label="Wydarzenie całodniowe")
        self.all_day_ctrl.SetValue(initial_draft.all_day if initial_draft else False)

        start_time = (
            initial_draft.start_time.strftime("%H:%M")
            if initial_draft and initial_draft.start_time
            else "09:00"
        )
        self.start_time_ctrl = wx.TextCtrl(self, value=start_time)

        self.end_date_ctrl = wx.TextCtrl(
            self,
            value=end_date.strftime("%d.%m.%Y"),
        )

        end_time = (
            initial_draft.end_time.strftime("%H:%M")
            if initial_draft and initial_draft.end_time
            else "10:00"
        )
        self.end_time_ctrl = wx.TextCtrl(self, value=end_time)

        self.location_ctrl = wx.TextCtrl(
            self,
            value=initial_draft.location if initial_draft else "",
        )

        self.description_ctrl = wx.TextCtrl(
            self,
            value=initial_draft.description if initial_draft else "",
            style=wx.TE_MULTILINE,
        )
        self.description_ctrl.SetMinSize((460, 110))

        calendar_help = (
            "Kalendarz tego wydarzenia. Przenoszenie między kalendarzami nie jest jeszcze dostępne."
            if initial_event
            else "Wybierz kalendarz, w którym wydarzenie zostanie zapisane."
        )
        self._name_control(self.title_ctrl, "Tytuł wydarzenia", "Wpisz nazwę wydarzenia.")
        self._name_control(
            self.calendar_ctrl,
            "Kalendarz wydarzenia" if initial_event else "Kalendarz docelowy",
            calendar_help,
        )
        self._name_control(
            self.start_date_ctrl,
            "Data rozpoczęcia, DD.MM.RRRR",
            "Wpisz datę rozpoczęcia w formacie dzień, miesiąc, rok.",
        )
        self._name_control(
            self.all_day_ctrl,
            "Wydarzenie całodniowe",
            "Zaznacz, aby pominąć godziny rozpoczęcia i zakończenia.",
        )
        self._name_control(
            self.start_time_ctrl,
            "Godzina rozpoczęcia, GG:MM",
            "Wpisz godzinę rozpoczęcia w formacie godzina, dwukropek, minuty.",
        )
        self._name_control(
            self.end_date_ctrl,
            "Data zakończenia włącznie, DD.MM.RRRR",
            "Wpisz ostatni dzień wydarzenia.",
        )
        self._name_control(
            self.end_time_ctrl,
            "Godzina zakończenia, GG:MM",
            "Wpisz godzinę zakończenia w formacie godzina, dwukropek, minuty.",
        )
        self._name_control(
            self.location_ctrl,
            "Lokalizacja",
            "Wpisz miejsce wydarzenia albo pozostaw pole puste.",
        )
        self._name_control(
            self.description_ctrl,
            "Opis wydarzenia",
            "Wpisz dodatkowy opis albo pozostaw pole puste.",
        )

        def add_row(label: str, control: wx.Window) -> None:
            form.Add(wx.StaticText(self, label=label), 0, wx.ALIGN_CENTER_VERTICAL)
            form.Add(control, 1, wx.EXPAND)

        add_row("Tytuł:", self.title_ctrl)
        add_row("Kalendarz:", self.calendar_ctrl)
        add_row("Data rozpoczęcia, DD.MM.RRRR:", self.start_date_ctrl)
        form.Add(wx.StaticText(self, label="Typ wydarzenia:"), 0, wx.ALIGN_CENTER_VERTICAL)
        form.Add(self.all_day_ctrl, 1, wx.EXPAND)
        add_row("Godzina rozpoczęcia, GG:MM:", self.start_time_ctrl)
        add_row("Data zakończenia włącznie, DD.MM.RRRR:", self.end_date_ctrl)
        add_row("Godzina zakończenia, GG:MM:", self.end_time_ctrl)
        add_row("Lokalizacja:", self.location_ctrl)
        add_row("Opis:", self.description_ctrl)
        sizer.Add(form, 1, wx.ALL | wx.EXPAND, 12)

        buttons = wx.StdDialogButtonSizer()
        self.save_button = wx.Button(self, wx.ID_OK, save_label)
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, "Anuluj")
        self.save_button.SetDefault()
        buttons.AddButton(self.save_button)
        buttons.AddButton(self.cancel_button)
        buttons.Realize()
        sizer.Add(buttons, 0, wx.ALL | wx.ALIGN_RIGHT, 12)

        self.SetSizerAndFit(sizer)
        self.SetMinSize((680, 560))
        self.SetSize((760, 640))
        self.CentreOnParent()

        self.all_day_ctrl.Bind(wx.EVT_CHECKBOX, self._on_all_day)
        self.save_button.Bind(wx.EVT_BUTTON, self._on_save)
        self._apply_all_day_state()
        wx.CallAfter(self.title_ctrl.SetFocus)

    def _name_control(
        self,
        control: wx.Window,
        name: str,
        description: str = "",
    ) -> None:
        accessible = apply_accessible_name(control, name, description)
        if accessible is not None:
            self._accessible_objects.append(accessible)

    def _apply_all_day_state(self) -> None:
        enabled = not self.all_day_ctrl.GetValue()
        self.start_time_ctrl.Enable(enabled)
        self.end_time_ctrl.Enable(enabled)

    def _on_all_day(self, event: wx.CommandEvent) -> None:
        self._apply_all_day_state()
        event.Skip()

    def _show_error(self, text: str, control: wx.Window | None = None) -> None:
        dialog = wx.MessageDialog(
            self,
            text,
            "Nieprawidłowe dane wydarzenia",
            wx.OK | wx.ICON_ERROR,
        )
        try:
            dialog.ShowModal()
        finally:
            dialog.Destroy()
        if control is not None:
            control.SetFocus()

    def _on_save(self, event: wx.CommandEvent) -> None:
        title = self.title_ctrl.GetValue().strip()
        if not title:
            self._show_error("Wpisz tytuł wydarzenia.", self.title_ctrl)
            return

        calendar_index = self.calendar_ctrl.GetSelection()
        if not 0 <= calendar_index < len(self._calendars):
            self._show_error("Wybierz kalendarz.", self.calendar_ctrl)
            return

        try:
            start_date = parse_polish_date(self.start_date_ctrl.GetValue())
        except ValueError as error:
            self._show_error(str(error), self.start_date_ctrl)
            return
        try:
            end_date = parse_polish_date(self.end_date_ctrl.GetValue())
        except ValueError as error:
            self._show_error(str(error), self.end_date_ctrl)
            return

        all_day = self.all_day_ctrl.GetValue()
        start_time = None
        end_time = None
        if not all_day:
            try:
                start_time = parse_polish_time(self.start_time_ctrl.GetValue())
            except ValueError as error:
                self._show_error(str(error), self.start_time_ctrl)
                return
            try:
                end_time = parse_polish_time(self.end_time_ctrl.GetValue())
            except ValueError as error:
                self._show_error(str(error), self.end_time_ctrl)
                return

        calendar = self._calendars[calendar_index]
        draft = EventDraft(
            calendar_id=calendar.calendar_id,
            title=title,
            all_day=all_day,
            start_date=start_date,
            end_date_inclusive=end_date,
            start_time=start_time,
            end_time=end_time,
            location=self.location_ctrl.GetValue().strip(),
            description=self.description_ctrl.GetValue().strip(),
        )
        try:
            draft.validate()
        except ValueError as error:
            self._show_error(str(error))
            return

        self._draft = draft
        self.EndModal(wx.ID_OK)

    def get_draft(self) -> EventDraft | None:
        return self._draft


class EventEditDialog(EventCreateDialog):
    def __init__(
        self,
        parent: wx.Window,
        calendar: CalendarInfo,
        event: CalendarEvent,
    ) -> None:
        super().__init__(
            parent,
            [calendar],
            event.start_date,
            initial_event=event,
            title="Edytuj wydarzenie",
            save_label="Zapisz zmiany",
        )


class CalendarSelectionDialog(wx.Dialog):
    def __init__(
        self,
        parent: wx.Window,
        calendars: list[CalendarInfo],
        selected_ids: set[str],
    ) -> None:
        super().__init__(parent, title="Wybierz kalendarze", style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self._calendars = calendars
        self._checkboxes: list[wx.CheckBox] = []

        sizer = wx.BoxSizer(wx.VERTICAL)
        info = wx.StaticText(self, label="Zaznacz kalendarze, których wydarzenia mają być pokazywane.")
        info.Wrap(560)
        sizer.Add(info, 0, wx.ALL | wx.EXPAND, 12)

        panel = wx.ScrolledWindow(self, style=wx.VSCROLL | wx.TAB_TRAVERSAL)
        panel.SetScrollRate(0, 20)
        panel_sizer = wx.BoxSizer(wx.VERTICAL)
        for calendar in calendars:
            label = calendar.name + (", kalendarz główny" if calendar.primary else "")
            checkbox = wx.CheckBox(panel, label=label)
            checkbox.SetName(label)
            checkbox.SetValue(calendar.calendar_id in selected_ids)
            self._checkboxes.append(checkbox)
            panel_sizer.Add(checkbox, 0, wx.ALL | wx.EXPAND, 6)
        panel.SetSizer(panel_sizer)
        panel.SetMinSize((580, 300))
        sizer.Add(panel, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 12)

        buttons = wx.StdDialogButtonSizer()
        self.ok_button = wx.Button(self, wx.ID_OK, "Zapisz")
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, "Anuluj")
        self.ok_button.SetDefault()
        buttons.AddButton(self.ok_button)
        buttons.AddButton(self.cancel_button)
        buttons.Realize()
        sizer.Add(buttons, 0, wx.ALL | wx.ALIGN_RIGHT, 12)

        self.SetSizerAndFit(sizer)
        self.SetMinSize((650, 450))
        self.SetSize((700, 520))
        self.CentreOnParent()
        wx.CallAfter((self._checkboxes[0] if self._checkboxes else self.cancel_button).SetFocus)

    def selected_ids(self) -> list[str]:
        return [
            calendar.calendar_id
            for calendar, checkbox in zip(self._calendars, self._checkboxes)
            if checkbox.GetValue()
        ]


class SearchResultsDialog(wx.Dialog):
    def __init__(self, parent: wx.Window, events: list[CalendarEvent]) -> None:
        super().__init__(parent, title="Wyniki wyszukiwania", style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self._events = events
        self.selected_event: CalendarEvent | None = None
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(self, label=f"Znaleziono: {count_text(len(events))}."), 0, wx.ALL, 12)
        choices = [f"{format_full_date(event.start_date)}, {event.display_text(event.start_date)}" for event in events]
        self.results = wx.ListBox(self, choices=choices, style=wx.LB_SINGLE)
        self.results.SetName(f"Wyniki wyszukiwania, {len(events)} elementów")
        self.results.SetMinSize((680, 300))
        if events:
            self.results.SetSelection(0)
        sizer.Add(self.results, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 12)
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
        self.SetSize((760, 460))
        self.CentreOnParent()
        self.open_button.Bind(wx.EVT_BUTTON, self._on_open)
        self.results.Bind(wx.EVT_LISTBOX_DCLICK, self._on_open)
        wx.CallAfter((self.results if events else self.close_button).SetFocus)

    def _on_open(self, event: wx.Event) -> None:
        index = self.results.GetSelection()
        if 0 <= index < len(self._events):
            self.selected_event = self._events[index]
            self.EndModal(wx.ID_OK)
