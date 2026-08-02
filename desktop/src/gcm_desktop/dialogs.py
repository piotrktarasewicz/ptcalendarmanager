from __future__ import annotations

import wx

from gcm_core.models import CalendarEvent, CalendarInfo, count_text, format_full_date


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
