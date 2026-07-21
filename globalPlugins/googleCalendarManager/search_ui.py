import datetime

import ui
import wx


CUSTOM_RANGE_INDEX = 4


def _safe_focus(control):
    try:
        wx.CallAfter(control.SetFocus)
    except Exception:
        pass


def _focus_control_now(control):
    try:
        control.SetFocus()
    except Exception:
        pass


class InlineSearchEventsDialog(wx.Dialog):
    def __init__(
        self,
        parent,
        title,
        query_label,
        range_label,
        range_choices,
        start_day_label,
        start_month_label,
        end_day_label,
        end_month_label,
        ok_label="OK",
        cancel_label="Cancel",
        default_range_index=0,
        default_start_day="",
        default_start_month="",
        default_end_day="",
        default_end_month="",
    ):
        super().__init__(parent, title=title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self._focus_labels = {}
        self._custom_controls = []

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_grid = wx.FlexGridSizer(cols=2, vgap=8, hgap=12)
        main_grid.AddGrowableCol(1, 1)

        self.query_ctrl = wx.TextCtrl(self, value="")
        self.range_choice = wx.Choice(self, choices=list(range_choices))
        if range_choices:
            if not (0 <= default_range_index < len(range_choices)):
                default_range_index = 0
            self.range_choice.SetSelection(default_range_index)

        self.query_ctrl.SetName(query_label)
        self.range_choice.SetName(range_label)
        self._bind_focus_announcement(self.query_ctrl, query_label)
        self._bind_focus_announcement(self.range_choice, range_label)

        main_grid.Add(wx.StaticText(self, label=query_label), 0, wx.ALIGN_CENTER_VERTICAL)
        main_grid.Add(self.query_ctrl, 1, wx.EXPAND)
        main_grid.Add(wx.StaticText(self, label=range_label), 0, wx.ALIGN_CENTER_VERTICAL)
        main_grid.Add(self.range_choice, 1, wx.EXPAND)
        main_sizer.Add(main_grid, 0, wx.ALL | wx.EXPAND, 12)

        self.custom_panel = wx.Panel(self, style=wx.TAB_TRAVERSAL)
        custom_grid = wx.FlexGridSizer(cols=2, vgap=8, hgap=12)
        custom_grid.AddGrowableCol(1, 1)

        self.start_day_ctrl = wx.TextCtrl(self.custom_panel, value=str(default_start_day))
        self.start_month_ctrl = wx.TextCtrl(self.custom_panel, value=str(default_start_month))
        self.end_day_ctrl = wx.TextCtrl(self.custom_panel, value=str(default_end_day))
        self.end_month_ctrl = wx.TextCtrl(self.custom_panel, value=str(default_end_month))

        custom_fields = [
            (self.start_day_ctrl, start_day_label),
            (self.start_month_ctrl, start_month_label),
            (self.end_day_ctrl, end_day_label),
            (self.end_month_ctrl, end_month_label),
        ]
        for control, label in custom_fields:
            control.SetName(label)
            self._bind_focus_announcement(control, label)
            self._custom_controls.append(control)
            custom_grid.Add(wx.StaticText(self.custom_panel, label=label), 0, wx.ALIGN_CENTER_VERTICAL)
            custom_grid.Add(control, 1, wx.EXPAND)

        self.custom_panel.SetSizer(custom_grid)
        main_sizer.Add(self.custom_panel, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 12)

        button_sizer = wx.StdDialogButtonSizer()
        self.ok_button = wx.Button(self, wx.ID_OK, ok_label)
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, cancel_label)
        self.ok_button.SetDefault()
        button_sizer.AddButton(self.ok_button)
        button_sizer.AddButton(self.cancel_button)
        button_sizer.Realize()
        main_sizer.Add(button_sizer, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.ALIGN_RIGHT, 12)

        self.SetSizer(main_sizer)
        self.SetMinSize((560, 260))
        self.SetSize((640, 360))
        self.CentreOnScreen()

        self.range_choice.Bind(wx.EVT_CHOICE, self._on_range_changed)
        self.Bind(wx.EVT_CHAR_HOOK, self._on_char_hook)

        self._initial_focus_control = self.query_ctrl
        self._update_custom_range_visibility()
        _safe_focus(self.query_ctrl)

    def focus_initial_control(self):
        _focus_control_now(self._initial_focus_control)

    def _bind_focus_announcement(self, control, label):
        self._focus_labels[control.GetId()] = label
        control.Bind(wx.EVT_SET_FOCUS, self._on_control_focus)

    def _on_control_focus(self, event):
        control = event.GetEventObject()
        label = self._focus_labels.get(control.GetId(), "")
        if label:
            wx.CallAfter(ui.message, label)
        event.Skip()

    def _is_custom_range_selected(self):
        return self.range_choice.GetSelection() == CUSTOM_RANGE_INDEX

    def _update_custom_range_visibility(self):
        show_custom = self._is_custom_range_selected()
        self.custom_panel.Show(show_custom)
        for control in self._custom_controls:
            control.Enable(show_custom)

        self.Layout()
        try:
            self.Fit()
            width = max(self.GetSize().GetWidth(), 640)
            height = max(self.GetSize().GetHeight(), 280 if not show_custom else 360)
            self.SetSize((width, height))
        except Exception:
            pass
        self.CentreOnScreen()

    def _on_range_changed(self, event):
        self._update_custom_range_visibility()
        event.Skip()

    def _on_char_hook(self, event):
        key = event.GetKeyCode()
        focus = self.FindFocus()

        if key == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_CANCEL)
            return

        if key in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            if focus is self.cancel_button:
                self.EndModal(wx.ID_CANCEL)
            else:
                self.EndModal(wx.ID_OK)
            return

        event.Skip()

    def get_data(self):
        return {
            "query": self.query_ctrl.GetValue().strip(),
            "range_index": self.range_choice.GetSelection(),
            "start_day": self.start_day_ctrl.GetValue().strip(),
            "start_month": self.start_month_ctrl.GetValue().strip(),
            "end_day": self.end_day_ctrl.GetValue().strip(),
            "end_month": self.end_month_ctrl.GetValue().strip(),
        }


class InlineSearchMixin:
    def _show_search_events_dialog(self):
        today = datetime.date.today()
        default_end = self._add_months_to_date(today, 1)
        range_labels = self._get_search_range_labels()

        dialog = InlineSearchEventsDialog(
            self._get_dialog_parent(),
            title=self._t("search_events_dialog_title"),
            query_label=self._t("search_events_query_label"),
            range_label=self._t("search_events_range_label"),
            range_choices=range_labels,
            start_day_label=self._t("search_events_start_day_label"),
            start_month_label=self._t("search_events_start_month_label"),
            end_day_label=self._t("search_events_end_day_label"),
            end_month_label=self._t("search_events_end_month_label"),
            ok_label=self._t("search_events_open_label"),
            cancel_label=self._t("dialog_cancel"),
            default_range_index=0,
            default_start_day=str(today.day),
            default_start_month=str(today.month),
            default_end_day=str(default_end.day),
            default_end_month=str(default_end.month),
        )

        try:
            result = self._show_modal_dialog(dialog)
            if result != wx.ID_OK:
                return
            raw_data = dialog.get_data()
        finally:
            dialog.Destroy()

        query = str(raw_data.get("query", "")).strip()
        if not query:
            self._show_message(
                self._t("search_events_error_query_required"),
                self._t("search_events_dialog_title"),
            )
            return

        range_index = raw_data.get("range_index", 0)
        if range_index == CUSTOM_RANGE_INDEX:
            is_valid, error_text, start_date = self._parse_single_date(
                raw_data.get("start_day", ""),
                raw_data.get("start_month", ""),
                "search_events_error_start_day_required",
                "search_events_error_start_month_required",
                "search_events_error_invalid_start_date",
                reference_date=today,
            )
            if not is_valid:
                self._show_message(error_text, self._t("search_events_dialog_title"))
                return

            is_valid, error_text, end_date = self._parse_single_date(
                raw_data.get("end_day", ""),
                raw_data.get("end_month", ""),
                "search_events_error_end_day_required",
                "search_events_error_end_month_required",
                "search_events_error_invalid_end_date",
                reference_date=start_date,
            )
            if not is_valid:
                self._show_message(error_text, self._t("search_events_dialog_title"))
                return

            if end_date < start_date:
                self._show_message(
                    self._t("search_events_error_end_before_start"),
                    self._t("search_events_dialog_title"),
                )
                return
        else:
            months_by_index = {
                0: 1,
                1: 3,
                2: 6,
                3: 12,
            }
            months = months_by_index.get(range_index, 1)
            start_date = today
            end_date = self._add_months_to_date(today, months)

        self._search_events_async(query, start_date, end_date)
