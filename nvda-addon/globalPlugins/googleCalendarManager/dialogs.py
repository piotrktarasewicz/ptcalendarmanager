import datetime
import wx
import ui


def _safe_focus(control):
    try:
        wx.CallAfter(control.SetFocus)
    except Exception:
        pass


def _safe_select_all(control):
    try:
        wx.CallAfter(control.SetSelection, -1, -1)
    except Exception:
        pass


def _focus_control_now(control):
    try:
        control.SetFocus()
    except Exception:
        pass


def _select_all_now(control):
    try:
        control.SetSelection(-1, -1)
    except Exception:
        pass


class ReadOnlyMessageDialog(wx.Dialog):
    def __init__(self, parent, title, message, ok_label="OK", checkbox_label=None, checkbox_checked=False):
        super().__init__(parent, title=title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.checkbox = None

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        text_ctrl = wx.TextCtrl(
            self,
            value=str(message or ""),
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_DONTWRAP
        )
        text_ctrl.SetMinSize((520, 140))
        main_sizer.Add(text_ctrl, 1, wx.ALL | wx.EXPAND, 12)

        if checkbox_label:
            self.checkbox = wx.CheckBox(self, label=checkbox_label)
            self.checkbox.SetValue(bool(checkbox_checked))
            main_sizer.Add(self.checkbox, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)

        button_sizer = wx.StdDialogButtonSizer()
        self.ok_button = wx.Button(self, wx.ID_OK, ok_label)
        self.ok_button.SetDefault()
        button_sizer.AddButton(self.ok_button)
        button_sizer.Realize()

        main_sizer.Add(button_sizer, 0, wx.ALL | wx.ALIGN_RIGHT, 12)

        self.SetSizerAndFit(main_sizer)
        self.SetMinSize((560, 260))
        self.SetSize((620, 300))
        self.CentreOnScreen()

        self.Bind(wx.EVT_CHAR_HOOK, self._on_char_hook)

        self._initial_focus_control = text_ctrl
        _safe_focus(text_ctrl)

    def focus_initial_control(self):
        _focus_control_now(self._initial_focus_control)

    def _on_char_hook(self, event):
        key = event.GetKeyCode()

        if key in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            self.EndModal(wx.ID_OK)
            return

        if key == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_OK)
            return

        event.Skip()

    def is_checkbox_checked(self):
        if self.checkbox is None:
            return False
        return self.checkbox.GetValue()


class ConfirmDialog(wx.Dialog):
    def __init__(self, parent, title, message, ok_label="OK", cancel_label="Cancel"):
        super().__init__(parent, title=title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        text_ctrl = wx.TextCtrl(
            self,
            value=str(message or ""),
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_DONTWRAP
        )
        text_ctrl.SetMinSize((520, 120))
        main_sizer.Add(text_ctrl, 1, wx.ALL | wx.EXPAND, 12)

        button_sizer = wx.StdDialogButtonSizer()

        self.ok_button = wx.Button(self, wx.ID_OK, ok_label)
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, cancel_label)

        self.ok_button.SetDefault()

        button_sizer.AddButton(self.ok_button)
        button_sizer.AddButton(self.cancel_button)
        button_sizer.Realize()

        main_sizer.Add(button_sizer, 0, wx.ALL | wx.ALIGN_RIGHT, 12)

        self.SetSizerAndFit(main_sizer)
        self.SetMinSize((560, 240))
        self.SetSize((620, 280))
        self.CentreOnScreen()

        self._initial_focus_control = text_ctrl
        _safe_focus(text_ctrl)

    def focus_initial_control(self):
        _focus_control_now(self._initial_focus_control)


class CalendarSelectionDialog(wx.Dialog):
    def __init__(self, parent, title, info_text, labels, checked_indexes, ok_label="OK", cancel_label="Cancel"):
        super().__init__(parent, title=title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self._checkboxes = []

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        info = wx.StaticText(self, label=info_text)
        info.Wrap(520)
        main_sizer.Add(info, 0, wx.ALL | wx.EXPAND, 12)

        container = wx.ScrolledWindow(self, style=wx.VSCROLL | wx.TAB_TRAVERSAL)
        container.SetScrollRate(0, 20)
        container_sizer = wx.BoxSizer(wx.VERTICAL)

        for index, label in enumerate(labels):
            cb = wx.CheckBox(container, label=label)
            cb.SetValue(index in checked_indexes)
            self._checkboxes.append(cb)
            container_sizer.Add(cb, 0, wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, 10)

        if self._checkboxes:
            container_sizer.AddSpacer(8)

        container.SetSizer(container_sizer)
        main_sizer.Add(container, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 12)

        button_sizer = wx.StdDialogButtonSizer()

        self.ok_button = wx.Button(self, wx.ID_OK, ok_label)
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, cancel_label)

        self.ok_button.SetDefault()

        button_sizer.AddButton(self.ok_button)
        button_sizer.AddButton(self.cancel_button)
        button_sizer.Realize()

        main_sizer.Add(button_sizer, 0, wx.ALL | wx.ALIGN_RIGHT, 12)

        self.SetSizerAndFit(main_sizer)
        self.SetMinSize((560, 320))
        self.SetSize((620, 420))
        self.CentreOnScreen()

        self.Bind(wx.EVT_CHAR_HOOK, self._on_char_hook)

        self._initial_focus_control = self._checkboxes[0] if self._checkboxes else self.ok_button
        if self._checkboxes:
            _safe_focus(self._checkboxes[0])

    def focus_initial_control(self):
        _focus_control_now(self._initial_focus_control)

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

    def get_selected_indexes(self):
        result = []
        for index, checkbox in enumerate(self._checkboxes):
            if checkbox.GetValue():
                result.append(index)
        return result


class ErrorDetailsDialog(wx.Dialog):
    def __init__(self, parent, title, message, details_label="Details", close_label="Close"):
        super().__init__(parent, title=title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        text_ctrl = wx.TextCtrl(
            self,
            value=str(message or ""),
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_DONTWRAP
        )
        text_ctrl.SetMinSize((520, 120))
        main_sizer.Add(text_ctrl, 1, wx.ALL | wx.EXPAND, 12)

        button_sizer = wx.StdDialogButtonSizer()

        self.details_button = wx.Button(self, wx.ID_MORE, details_label)
        self.close_button = wx.Button(self, wx.ID_CLOSE, close_label)

        self.details_button.SetDefault()

        button_sizer.AddButton(self.details_button)
        button_sizer.AddButton(self.close_button)
        button_sizer.Realize()

        main_sizer.Add(button_sizer, 0, wx.ALL | wx.ALIGN_RIGHT, 12)

        self.SetSizerAndFit(main_sizer)
        self.SetMinSize((560, 240))
        self.SetSize((660, 280))
        self.CentreOnScreen()

        self.Bind(wx.EVT_BUTTON, self._on_details, self.details_button)
        self.Bind(wx.EVT_BUTTON, self._on_close, self.close_button)
        self.Bind(wx.EVT_CHAR_HOOK, self._on_char_hook)

        self._initial_focus_control = self.details_button
        _safe_focus(self.details_button)

    def focus_initial_control(self):
        _focus_control_now(self._initial_focus_control)

    def _on_details(self, event):
        self.EndModal(wx.ID_MORE)

    def _on_close(self, event):
        self.EndModal(wx.ID_CLOSE)

    def _on_char_hook(self, event):
        key = event.GetKeyCode()
        focus = self.FindFocus()

        if key == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_CLOSE)
            return

        if key in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            if focus is self.close_button:
                self.EndModal(wx.ID_CLOSE)
            else:
                self.EndModal(wx.ID_MORE)
            return

        event.Skip()


class EventDayDialog(wx.Dialog):
    def __init__(self, parent, title, day_label, month_label, ok_label="OK", cancel_label="Cancel", default_day="", default_month=""):
        super().__init__(parent, title=title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self._focus_labels = {}

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.FlexGridSizer(cols=2, vgap=8, hgap=12)
        grid.AddGrowableCol(1, 1)

        self.day_ctrl = wx.TextCtrl(self, value=str(default_day))
        self.month_ctrl = wx.TextCtrl(self, value=str(default_month))

        self.day_ctrl.SetName(day_label)
        self.month_ctrl.SetName(month_label)

        self._bind_focus_announcement(self.day_ctrl, day_label)
        self._bind_focus_announcement(self.month_ctrl, month_label)

        grid.Add(wx.StaticText(self, label=day_label), 0, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self.day_ctrl, 1, wx.EXPAND)

        grid.Add(wx.StaticText(self, label=month_label), 0, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self.month_ctrl, 1, wx.EXPAND)

        main_sizer.Add(grid, 1, wx.ALL | wx.EXPAND, 12)

        button_sizer = wx.StdDialogButtonSizer()
        self.ok_button = wx.Button(self, wx.ID_OK, ok_label)
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, cancel_label)
        self.ok_button.SetDefault()
        button_sizer.AddButton(self.ok_button)
        button_sizer.AddButton(self.cancel_button)
        button_sizer.Realize()

        main_sizer.Add(button_sizer, 0, wx.ALL | wx.ALIGN_RIGHT, 12)

        self.SetSizerAndFit(main_sizer)
        self.SetMinSize((460, 220))
        self.SetSize((520, 240))
        self.CentreOnScreen()

        self.Bind(wx.EVT_CHAR_HOOK, self._on_char_hook)

        self._initial_focus_control = self.day_ctrl
        _safe_focus(self.day_ctrl)

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
            "day": self.day_ctrl.GetValue().strip(),
            "month": self.month_ctrl.GetValue().strip(),
        }


class EventSelectionDialog(wx.Dialog):
    def __init__(
        self,
        parent,
        title,
        label_text,
        choices,
        ok_label="OK",
        cancel_label="Cancel",
        multi_select=False,
        select_all_label="Select all",
        deselect_all_label="Deselect all",
        checked_state_label="selected",
        unchecked_state_label="not selected",
        selection_all_selected_message="All events selected.",
        selection_all_cleared_message="All events deselected.",
    ):
        super().__init__(parent, title=title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.multi_select = bool(multi_select)
        self._choices = list(choices)
        self._checkboxes = []
        self._checked_state_label = str(checked_state_label)
        self._unchecked_state_label = str(unchecked_state_label)
        self._selection_all_selected_message = str(selection_all_selected_message)
        self._selection_all_cleared_message = str(selection_all_cleared_message)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, label=label_text)
        label.Wrap(520)
        main_sizer.Add(label, 0, wx.ALL | wx.EXPAND, 12)

        if self.multi_select:
            self.scroll_panel = wx.ScrolledWindow(self, style=wx.VSCROLL | wx.TAB_TRAVERSAL)
            self.scroll_panel.SetScrollRate(0, 20)
            self.scroll_panel.SetMinSize((560, 260))
            list_sizer = wx.BoxSizer(wx.VERTICAL)

            for choice_text in self._choices:
                checkbox = wx.CheckBox(self.scroll_panel, label=choice_text)
                checkbox.Bind(wx.EVT_SET_FOCUS, self._on_checkbox_focus)
                checkbox.Bind(wx.EVT_CHECKBOX, self._on_checkbox_toggled)
                self._checkboxes.append(checkbox)
                list_sizer.Add(checkbox, 0, wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, 8)

            if self._checkboxes:
                list_sizer.AddSpacer(8)

            self.scroll_panel.SetSizer(list_sizer)
            main_sizer.Add(self.scroll_panel, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 12)

            action_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.select_all_button = wx.Button(self, wx.ID_ANY, select_all_label)
            self.deselect_all_button = wx.Button(self, wx.ID_ANY, deselect_all_label)
            action_sizer.Add(self.select_all_button, 0, wx.RIGHT, 8)
            action_sizer.Add(self.deselect_all_button, 0)
            main_sizer.Add(action_sizer, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)

            self.select_all_button.Bind(wx.EVT_BUTTON, self._on_select_all)
            self.deselect_all_button.Bind(wx.EVT_BUTTON, self._on_deselect_all)
        else:
            self.choice = wx.ListBox(self, choices=self._choices)
            self.choice.SetMinSize((520, 220))
            if self._choices:
                self.choice.SetSelection(0)
            main_sizer.Add(self.choice, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 12)

        button_sizer = wx.StdDialogButtonSizer()
        self.ok_button = wx.Button(self, wx.ID_OK, ok_label)
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, cancel_label)
        self.ok_button.SetDefault()
        button_sizer.AddButton(self.ok_button)
        button_sizer.AddButton(self.cancel_button)
        button_sizer.Realize()

        main_sizer.Add(button_sizer, 0, wx.ALL | wx.ALIGN_RIGHT, 12)

        self.SetSizerAndFit(main_sizer)
        self.SetMinSize((600, 420))
        self.SetSize((760, 560))
        self.CentreOnScreen()

        self.Bind(wx.EVT_CHAR_HOOK, self._on_char_hook)

        if self.multi_select:
            if self._checkboxes:
                wx.CallAfter(self._focus_first_checkbox)
        else:
            _safe_focus(self.choice)

    def focus_initial_control(self):
        if self.multi_select:
            self._focus_first_checkbox()
            return
        _focus_control_now(self.choice)

    def _focus_first_checkbox(self):
        if self._checkboxes:
            self._checkboxes[0].SetFocus()
            self._announce_checkbox(self._checkboxes[0])

    def _announce_checkbox(self, checkbox):
        label = checkbox.GetLabel()
        state = self._checked_state_label if checkbox.GetValue() else self._unchecked_state_label
        ui.message(f"{label}, {state}")
        try:
            self.scroll_panel.ScrollChildIntoView(checkbox)
        except Exception:
            pass

    def _announce_checkbox_state(self, checkbox):
        state = self._checked_state_label if checkbox.GetValue() else self._unchecked_state_label
        ui.message(state)
        try:
            self.scroll_panel.ScrollChildIntoView(checkbox)
        except Exception:
            pass

    def _on_checkbox_focus(self, event):
        checkbox = event.GetEventObject()
        wx.CallAfter(self._announce_checkbox, checkbox)
        event.Skip()

    def _on_checkbox_toggled(self, event):
        checkbox = event.GetEventObject()
        wx.CallAfter(self._announce_checkbox_state, checkbox)
        event.Skip()

    def _on_select_all(self, event):
        for checkbox in self._checkboxes:
            checkbox.SetValue(True)
        if self._checkboxes:
            self._checkboxes[0].SetFocus()
        ui.message(self._selection_all_selected_message)

    def _on_deselect_all(self, event):
        for checkbox in self._checkboxes:
            checkbox.SetValue(False)
        if self._checkboxes:
            self._checkboxes[0].SetFocus()
        ui.message(self._selection_all_cleared_message)

    def _on_char_hook(self, event):
        key = event.GetKeyCode()
        focus = self.FindFocus()

        if key == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_CANCEL)
            return

        if key in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            if focus is self.cancel_button:
                self.EndModal(wx.ID_CANCEL)
                return
            if self.multi_select and focus is getattr(self, "select_all_button", None):
                self._on_select_all(None)
                return
            if self.multi_select and focus is getattr(self, "deselect_all_button", None):
                self._on_deselect_all(None)
                return
            self.EndModal(wx.ID_OK)
            return

        event.Skip()

    def get_selected_index(self):
        if self.multi_select:
            selected = self.get_selected_indices()
            return selected[0] if selected else wx.NOT_FOUND
        return self.choice.GetSelection()

    def get_selected_indices(self):
        if self.multi_select:
            return [index for index, checkbox in enumerate(self._checkboxes) if checkbox.GetValue()]
        index = self.choice.GetSelection()
        return [index] if index != wx.NOT_FOUND else []

    def get_selected_indexes(self):
        return self.get_selected_indices()


class SearchEventsDialog(wx.Dialog):
    def __init__(
        self,
        parent,
        title,
        query_label,
        range_label,
        range_choices,
        ok_label="OK",
        cancel_label="Cancel",
        default_range_index=0,
    ):
        super().__init__(parent, title=title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self._focus_labels = {}

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.FlexGridSizer(cols=2, vgap=8, hgap=12)
        grid.AddGrowableCol(1, 1)

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

        grid.Add(wx.StaticText(self, label=query_label), 0, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self.query_ctrl, 1, wx.EXPAND)

        grid.Add(wx.StaticText(self, label=range_label), 0, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self.range_choice, 1, wx.EXPAND)

        main_sizer.Add(grid, 1, wx.ALL | wx.EXPAND, 12)

        button_sizer = wx.StdDialogButtonSizer()
        self.ok_button = wx.Button(self, wx.ID_OK, ok_label)
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, cancel_label)
        self.ok_button.SetDefault()
        button_sizer.AddButton(self.ok_button)
        button_sizer.AddButton(self.cancel_button)
        button_sizer.Realize()

        main_sizer.Add(button_sizer, 0, wx.ALL | wx.ALIGN_RIGHT, 12)

        self.SetSizerAndFit(main_sizer)
        self.SetMinSize((560, 240))
        self.SetSize((640, 270))
        self.CentreOnScreen()

        self.Bind(wx.EVT_CHAR_HOOK, self._on_char_hook)

        self._initial_focus_control = self.query_ctrl
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
        }


class SearchDateRangeDialog(wx.Dialog):
    def __init__(
        self,
        parent,
        title,
        start_day_label,
        start_month_label,
        end_day_label,
        end_month_label,
        ok_label="OK",
        cancel_label="Cancel",
        default_start_day="",
        default_start_month="",
        default_end_day="",
        default_end_month="",
    ):
        super().__init__(parent, title=title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self._focus_labels = {}

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.FlexGridSizer(cols=2, vgap=8, hgap=12)
        grid.AddGrowableCol(1, 1)

        self.start_day_ctrl = wx.TextCtrl(self, value=str(default_start_day))
        self.start_month_ctrl = wx.TextCtrl(self, value=str(default_start_month))
        self.end_day_ctrl = wx.TextCtrl(self, value=str(default_end_day))
        self.end_month_ctrl = wx.TextCtrl(self, value=str(default_end_month))

        controls = [
            (self.start_day_ctrl, start_day_label),
            (self.start_month_ctrl, start_month_label),
            (self.end_day_ctrl, end_day_label),
            (self.end_month_ctrl, end_month_label),
        ]

        for control, label in controls:
            control.SetName(label)
            self._bind_focus_announcement(control, label)
            grid.Add(wx.StaticText(self, label=label), 0, wx.ALIGN_CENTER_VERTICAL)
            grid.Add(control, 1, wx.EXPAND)

        main_sizer.Add(grid, 1, wx.ALL | wx.EXPAND, 12)

        button_sizer = wx.StdDialogButtonSizer()
        self.ok_button = wx.Button(self, wx.ID_OK, ok_label)
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, cancel_label)
        self.ok_button.SetDefault()
        button_sizer.AddButton(self.ok_button)
        button_sizer.AddButton(self.cancel_button)
        button_sizer.Realize()

        main_sizer.Add(button_sizer, 0, wx.ALL | wx.ALIGN_RIGHT, 12)

        self.SetSizerAndFit(main_sizer)
        self.SetMinSize((520, 280))
        self.SetSize((620, 320))
        self.CentreOnScreen()

        self.Bind(wx.EVT_CHAR_HOOK, self._on_char_hook)

        self._initial_focus_control = self.start_day_ctrl
        _safe_focus(self.start_day_ctrl)

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
            "start_day": self.start_day_ctrl.GetValue().strip(),
            "start_month": self.start_month_ctrl.GetValue().strip(),
            "end_day": self.end_day_ctrl.GetValue().strip(),
            "end_month": self.end_month_ctrl.GetValue().strip(),
        }


class DeleteEventConfirmDialog(wx.Dialog):
    def __init__(self, parent, title, message, delete_label="Delete", cancel_label="Cancel"):
        super().__init__(parent, title=title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.text_ctrl = wx.TextCtrl(
            self,
            value=str(message or ""),
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_DONTWRAP
        )
        self.text_ctrl.SetMinSize((520, 120))
        main_sizer.Add(self.text_ctrl, 1, wx.ALL | wx.EXPAND, 12)

        button_sizer = wx.StdDialogButtonSizer()

        self.delete_button = wx.Button(self, wx.ID_OK, delete_label)
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, cancel_label)

        self.delete_button.SetDefault()

        button_sizer.AddButton(self.delete_button)
        button_sizer.AddButton(self.cancel_button)
        button_sizer.Realize()

        main_sizer.Add(button_sizer, 0, wx.ALL | wx.ALIGN_RIGHT, 12)

        self.SetSizerAndFit(main_sizer)
        self.SetMinSize((560, 240))
        self.SetSize((680, 300))
        self.CentreOnScreen()

        self.Bind(wx.EVT_CHAR_HOOK, self._on_char_hook)

        self._initial_focus_control = self.text_ctrl
        _safe_focus(self.text_ctrl)

    def focus_initial_control(self):
        _focus_control_now(self._initial_focus_control)

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


class DailyEventsResultDialog(wx.Dialog):
    RESULT_EDIT = 5101
    RESULT_DELETE = 5102
    RESULT_ADD = 5103
    RESULT_OTHER_DAY = wx.ID_MORE

    def __init__(
        self,
        parent,
        title,
        message,
        ok_label="OK",
        other_day_label="Choose another day",
        edit_label="Edit",
        delete_label="Delete",
        add_label=None,
        add_enabled=False,
        management_enabled=True,
    ):
        super().__init__(parent, title=title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.text_ctrl = wx.TextCtrl(
            self,
            value=str(message or ""),
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_DONTWRAP
        )
        self.text_ctrl.SetMinSize((560, 220))
        main_sizer.Add(self.text_ctrl, 1, wx.ALL | wx.EXPAND, 12)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.add_button = None
        if add_label:
            self.add_button = wx.Button(self, wx.ID_ANY, add_label)
            self.add_button.Enable(bool(add_enabled))
        self.edit_button = wx.Button(self, wx.ID_ANY, edit_label)
        self.delete_button = wx.Button(self, wx.ID_ANY, delete_label)
        self.other_day_button = wx.Button(self, wx.ID_ANY, other_day_label)
        self.ok_button = wx.Button(self, wx.ID_OK, ok_label)

        self.ok_button.SetDefault()
        self.edit_button.Enable(bool(management_enabled))
        self.delete_button.Enable(bool(management_enabled))

        if self.add_button is not None:
            button_sizer.Add(self.add_button, 0, wx.RIGHT, 8)
        button_sizer.Add(self.edit_button, 0, wx.RIGHT, 8)
        button_sizer.Add(self.delete_button, 0, wx.RIGHT, 8)
        button_sizer.Add(self.other_day_button, 0, wx.RIGHT, 8)
        button_sizer.Add(self.ok_button, 0)

        main_sizer.Add(button_sizer, 0, wx.ALL | wx.ALIGN_RIGHT, 12)

        self.SetSizerAndFit(main_sizer)
        self.SetMinSize((660, 340))
        self.SetSize((820, 440))
        self.CentreOnScreen()

        if self.add_button is not None:
            self.Bind(wx.EVT_BUTTON, self._on_add, self.add_button)
        self.Bind(wx.EVT_BUTTON, self._on_edit, self.edit_button)
        self.Bind(wx.EVT_BUTTON, self._on_delete, self.delete_button)
        self.Bind(wx.EVT_BUTTON, self._on_other_day, self.other_day_button)
        self.Bind(wx.EVT_BUTTON, self._on_ok, self.ok_button)
        self.Bind(wx.EVT_CHAR_HOOK, self._on_char_hook)

        self._initial_focus_control = self.text_ctrl
        _safe_focus(self.text_ctrl)

    def focus_initial_control(self):
        _focus_control_now(self._initial_focus_control)

    def _on_add(self, event):
        self.EndModal(self.RESULT_ADD)

    def _on_edit(self, event):
        self.EndModal(self.RESULT_EDIT)

    def _on_delete(self, event):
        self.EndModal(self.RESULT_DELETE)

    def _on_other_day(self, event):
        self.EndModal(self.RESULT_OTHER_DAY)

    def _on_ok(self, event):
        self.EndModal(wx.ID_OK)

    def _on_char_hook(self, event):
        key = event.GetKeyCode()
        focus = self.FindFocus()

        if key == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_OK)
            return

        if key in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            if focus is self.edit_button:
                self.EndModal(self.RESULT_EDIT)
                return
            if focus is self.delete_button:
                self.EndModal(self.RESULT_DELETE)
                return
            if focus is self.other_day_button:
                self.EndModal(self.RESULT_OTHER_DAY)
                return
            self.EndModal(wx.ID_OK)
            return

        event.Skip()


class AddEventDialog(wx.Dialog):
    def __init__(
        self,
        parent,
        title,
        labels,
        calendar_names,
        recurrence_labels,
        selected_calendar_index=0,
        selected_recurrence_index=0,
        ok_label="OK",
        cancel_label="Cancel",
        default_title="",
        default_day="",
        default_month="",
        default_end_day="",
        default_end_month="",
        default_recurrence_end_day="",
        default_recurrence_end_month="",
        default_recurrence_end_year="",
        default_start_hour="09",
        default_start_minute="00",
        default_end_hour="10",
        default_end_minute="00",
        default_location="",
        default_all_day=False,
        default_recurrence_no_end=False,
        enable_calendar_choice=True,
        enable_recurrence_choice=True,
    ):
        super().__init__(parent, title=title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.labels = dict(labels)
        self._focus_labels = {}
        self._enable_recurrence_choice = bool(enable_recurrence_choice)

        self._initial_default_end_day = str(default_end_day).strip()
        self._initial_default_end_month = str(default_end_month).strip()
        self._initial_default_recurrence_end_day = str(default_recurrence_end_day).strip()
        self._initial_default_recurrence_end_month = str(default_recurrence_end_month).strip()
        self._initial_default_recurrence_end_year = str(default_recurrence_end_year).strip()

        self._user_changed_end_date = False
        self._user_changed_recurrence_end_date = False
        self._syncing_default_dates = False

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.scroller = wx.ScrolledWindow(self, style=wx.VSCROLL | wx.TAB_TRAVERSAL)
        self.scroller.SetScrollRate(0, 20)
        scroller_sizer = wx.BoxSizer(wx.VERTICAL)

        form_panel = wx.Panel(self.scroller)
        form_sizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.FlexGridSizer(cols=2, vgap=8, hgap=12)
        grid.AddGrowableCol(1, 1)

        self.title_ctrl = wx.TextCtrl(form_panel, value=str(default_title))
        self.day_ctrl = wx.TextCtrl(form_panel, value=str(default_day))
        self.month_ctrl = wx.TextCtrl(form_panel, value=str(default_month))
        self.all_day_checkbox = wx.CheckBox(form_panel, label=labels["all_day"])
        self.all_day_checkbox.SetValue(bool(default_all_day))

        self.recurrence_choice = wx.Choice(form_panel, choices=recurrence_labels)
        if recurrence_labels:
            if 0 <= selected_recurrence_index < len(recurrence_labels):
                self.recurrence_choice.SetSelection(selected_recurrence_index)
            else:
                self.recurrence_choice.SetSelection(0)
        if not self._enable_recurrence_choice and recurrence_labels:
            self.recurrence_choice.SetSelection(0)

        self.recurrence_no_end_checkbox = wx.CheckBox(form_panel, label=labels["recurrence_no_end"])
        self.recurrence_no_end_checkbox.SetValue(bool(default_recurrence_no_end))
        self.recurrence_end_day_ctrl = wx.TextCtrl(form_panel, value=str(default_recurrence_end_day))
        self.recurrence_end_month_ctrl = wx.TextCtrl(form_panel, value=str(default_recurrence_end_month))
        self.recurrence_end_year_ctrl = wx.TextCtrl(form_panel, value=str(default_recurrence_end_year))

        self.start_hour_ctrl = wx.TextCtrl(form_panel, value=str(default_start_hour))
        self.start_minute_ctrl = wx.TextCtrl(form_panel, value=str(default_start_minute))
        self.end_day_ctrl = wx.TextCtrl(form_panel, value=str(default_end_day))
        self.end_month_ctrl = wx.TextCtrl(form_panel, value=str(default_end_month))
        self.end_hour_ctrl = wx.TextCtrl(form_panel, value=str(default_end_hour))
        self.end_minute_ctrl = wx.TextCtrl(form_panel, value=str(default_end_minute))

        self.location_ctrl = wx.TextCtrl(form_panel, value=str(default_location))
        self.calendar_choice = wx.Choice(form_panel, choices=calendar_names)
        if calendar_names:
            if 0 <= selected_calendar_index < len(calendar_names):
                self.calendar_choice.SetSelection(selected_calendar_index)
            else:
                self.calendar_choice.SetSelection(0)
        self.calendar_choice.Enable(bool(enable_calendar_choice))

        self.title_label_ctrl = wx.StaticText(form_panel, label=labels["title"])
        self.day_label_ctrl = wx.StaticText(form_panel, label=labels["day"])
        self.month_label_ctrl = wx.StaticText(form_panel, label=labels["month"])
        self.start_hour_label_ctrl = wx.StaticText(form_panel, label=labels["start_hour"])
        self.start_minute_label_ctrl = wx.StaticText(form_panel, label=labels["start_minute"])
        self.end_day_label_ctrl = wx.StaticText(form_panel, label=labels["end_day"])
        self.end_month_label_ctrl = wx.StaticText(form_panel, label=labels["end_month"])
        self.end_hour_label_ctrl = wx.StaticText(form_panel, label=labels["end_hour"])
        self.end_minute_label_ctrl = wx.StaticText(form_panel, label=labels["end_minute"])
        self.recurrence_label_ctrl = wx.StaticText(form_panel, label=labels["recurrence"])
        self.recurrence_end_day_label_ctrl = wx.StaticText(form_panel, label=labels["recurrence_end_day"])
        self.recurrence_end_month_label_ctrl = wx.StaticText(form_panel, label=labels["recurrence_end_month"])
        self.recurrence_end_year_label_ctrl = wx.StaticText(form_panel, label=labels["recurrence_end_year"])
        self.location_label_ctrl = wx.StaticText(form_panel, label=labels["location"])
        self.calendar_label_ctrl = wx.StaticText(form_panel, label=labels["calendar"])

        rows = [
            (self.title_label_ctrl, self.title_ctrl),
            (self.day_label_ctrl, self.day_ctrl),
            (self.month_label_ctrl, self.month_ctrl),
            (wx.StaticText(form_panel, label=""), self.all_day_checkbox),
            (self.start_hour_label_ctrl, self.start_hour_ctrl),
            (self.start_minute_label_ctrl, self.start_minute_ctrl),
            (self.end_hour_label_ctrl, self.end_hour_ctrl),
            (self.end_minute_label_ctrl, self.end_minute_ctrl),
            (self.end_day_label_ctrl, self.end_day_ctrl),
            (self.end_month_label_ctrl, self.end_month_ctrl),
            (self.recurrence_label_ctrl, self.recurrence_choice),
            (wx.StaticText(form_panel, label=""), self.recurrence_no_end_checkbox),
            (self.recurrence_end_day_label_ctrl, self.recurrence_end_day_ctrl),
            (self.recurrence_end_month_label_ctrl, self.recurrence_end_month_ctrl),
            (self.recurrence_end_year_label_ctrl, self.recurrence_end_year_ctrl),
            (self.location_label_ctrl, self.location_ctrl),
            (self.calendar_label_ctrl, self.calendar_choice),
        ]

        for label_ctrl, control in rows:
            grid.Add(label_ctrl, 0, wx.ALIGN_CENTER_VERTICAL)
            grid.Add(control, 1, wx.EXPAND)

        form_sizer.Add(grid, 1, wx.EXPAND | wx.ALL, 12)
        form_panel.SetSizer(form_sizer)

        self.scroller.SetSizer(wx.BoxSizer(wx.VERTICAL))
        self.scroller.GetSizer().Add(form_panel, 1, wx.EXPAND)
        scroller_sizer.Add(self.scroller, 1, wx.EXPAND)
        main_sizer.Add(scroller_sizer, 1, wx.EXPAND)

        button_sizer = wx.StdDialogButtonSizer()
        self.ok_button = wx.Button(self, wx.ID_OK, ok_label)
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, cancel_label)
        self.ok_button.SetDefault()
        button_sizer.AddButton(self.ok_button)
        button_sizer.AddButton(self.cancel_button)
        button_sizer.Realize()
        main_sizer.Add(button_sizer, 0, wx.ALL | wx.ALIGN_RIGHT, 12)

        self.SetSizer(main_sizer)
        self.SetMinSize((700, 520))
        self.SetSize((820, 640))
        self.CentreOnScreen()

        control_labels = [
            (self.title_ctrl, labels["title"]),
            (self.day_ctrl, labels["day"]),
            (self.month_ctrl, labels["month"]),
            (self.all_day_checkbox, labels["all_day"]),
            (self.start_hour_ctrl, labels["start_hour"]),
            (self.start_minute_ctrl, labels["start_minute"]),
            (self.end_hour_ctrl, labels["end_hour"]),
            (self.end_minute_ctrl, labels["end_minute"]),
            (self.end_day_ctrl, labels["end_day"]),
            (self.end_month_ctrl, labels["end_month"]),
            (self.recurrence_choice, labels["recurrence"]),
            (self.recurrence_no_end_checkbox, labels["recurrence_no_end"]),
            (self.recurrence_end_day_ctrl, labels["recurrence_end_day"]),
            (self.recurrence_end_month_ctrl, labels["recurrence_end_month"]),
            (self.recurrence_end_year_ctrl, labels["recurrence_end_year"]),
            (self.location_ctrl, labels["location"]),
            (self.calendar_choice, labels["calendar"]),
        ]
        for control, label in control_labels:
            control.SetName(label)
            self._bind_focus_announcement(control, label)

        self.Bind(wx.EVT_CHAR_HOOK, self._on_char_hook)
        self.all_day_checkbox.Bind(wx.EVT_CHECKBOX, self._on_all_day_changed)
        self.recurrence_choice.Bind(wx.EVT_CHOICE, self._on_recurrence_changed)
        self.recurrence_no_end_checkbox.Bind(wx.EVT_CHECKBOX, self._on_recurrence_no_end_changed)
        self.day_ctrl.Bind(wx.EVT_TEXT, self._on_start_date_changed)
        self.month_ctrl.Bind(wx.EVT_TEXT, self._on_start_date_changed)
        self.end_day_ctrl.Bind(wx.EVT_TEXT, self._on_end_date_changed)
        self.end_month_ctrl.Bind(wx.EVT_TEXT, self._on_end_date_changed)
        self.recurrence_end_day_ctrl.Bind(wx.EVT_TEXT, self._on_recurrence_end_date_changed)
        self.recurrence_end_month_ctrl.Bind(wx.EVT_TEXT, self._on_recurrence_end_date_changed)
        self.recurrence_end_year_ctrl.Bind(wx.EVT_TEXT, self._on_recurrence_end_date_changed)

        self._sync_own_end_with_start = self._should_sync_own_end_with_start()
        self._sync_recurrence_end_with_start = self._should_sync_recurrence_end_with_start()
        self._set_tab_order()

        self._update_time_controls()
        self._update_recurrence_controls()

        self._initial_focus_control = self.title_ctrl
        _safe_focus(self.title_ctrl)
        _safe_select_all(self.title_ctrl)

    def focus_initial_control(self):
        _focus_control_now(self._initial_focus_control)
        _select_all_now(self._initial_focus_control)

    def _bind_focus_announcement(self, control, label):
        self._focus_labels[control.GetId()] = label
        control.Bind(wx.EVT_SET_FOCUS, self._on_control_focus)

    def _on_control_focus(self, event):
        control = event.GetEventObject()
        label = self._focus_labels.get(control.GetId(), "")
        if label:
            wx.CallAfter(ui.message, label)
        event.Skip()

    def _set_visible(self, label_ctrl, control, visible):
        label_ctrl.Show(visible)
        label_ctrl.Enable(visible)
        control.Show(visible)
        control.Enable(visible)

    def _set_tab_order(self):
        controls = [
            self.title_ctrl,
            self.day_ctrl,
            self.month_ctrl,
            self.all_day_checkbox,
            self.start_hour_ctrl,
            self.start_minute_ctrl,
            self.end_hour_ctrl,
            self.end_minute_ctrl,
            self.end_day_ctrl,
            self.end_month_ctrl,
            self.recurrence_choice,
            self.recurrence_no_end_checkbox,
            self.recurrence_end_day_ctrl,
            self.recurrence_end_month_ctrl,
            self.recurrence_end_year_ctrl,
            self.location_ctrl,
            self.calendar_choice,
            self.ok_button,
            self.cancel_button,
        ]
        previous = None
        for control in controls:
            if previous is not None:
                try:
                    control.MoveAfterInTabOrder(previous)
                except Exception:
                    pass
            previous = control

    @staticmethod
    def _same_text(left, right):
        return str(left).strip() == str(right).strip()

    def _current_start_year_text(self):
        try:
            day = int(self.day_ctrl.GetValue().strip())
            month = int(self.month_ctrl.GetValue().strip())
            today = datetime.date.today()
            candidate = datetime.date(today.year, month, day)
            if candidate < today:
                candidate = datetime.date(today.year + 1, month, day)
            return str(candidate.year)
        except Exception:
            return str(datetime.date.today().year)

    def _should_sync_own_end_with_start(self):
        return (
            (not self._initial_default_end_day or self._same_text(self._initial_default_end_day, self.day_ctrl.GetValue()))
            and (not self._initial_default_end_month or self._same_text(self._initial_default_end_month, self.month_ctrl.GetValue()))
        )

    def _should_sync_recurrence_end_with_start(self):
        return (
            (not self._initial_default_recurrence_end_day or self._same_text(self._initial_default_recurrence_end_day, self.day_ctrl.GetValue()))
            and (not self._initial_default_recurrence_end_month or self._same_text(self._initial_default_recurrence_end_month, self.month_ctrl.GetValue()))
            and (not self._initial_default_recurrence_end_year or self._same_text(self._initial_default_recurrence_end_year, self._current_start_year_text()))
        )

    def _copy_default_dates_from_start_if_unchanged(self):
        try:
            self._syncing_default_dates = True

            if self._sync_own_end_with_start and not self._user_changed_end_date:
                self.end_day_ctrl.ChangeValue(self.day_ctrl.GetValue().strip())
                self.end_month_ctrl.ChangeValue(self.month_ctrl.GetValue().strip())

            if self._sync_recurrence_end_with_start and not self._user_changed_recurrence_end_date:
                self.recurrence_end_day_ctrl.ChangeValue(self.day_ctrl.GetValue().strip())
                self.recurrence_end_month_ctrl.ChangeValue(self.month_ctrl.GetValue().strip())
                self.recurrence_end_year_ctrl.ChangeValue(self._current_start_year_text())
        finally:
            self._syncing_default_dates = False

    def _on_start_date_changed(self, event):
        self._copy_default_dates_from_start_if_unchanged()
        event.Skip()

    def _on_end_date_changed(self, event):
        if not self._syncing_default_dates:
            self._user_changed_end_date = True
        event.Skip()

    def _on_recurrence_end_date_changed(self, event):
        if not self._syncing_default_dates:
            self._user_changed_recurrence_end_date = True
        event.Skip()

    def _is_recurring(self):
        if not self._enable_recurrence_choice:
            return False
        return self.recurrence_choice.GetSelection() > 0

    def _update_time_controls(self):
        is_all_day = self.all_day_checkbox.GetValue()
        is_recurring = self._is_recurring()
        show_own_end = is_all_day and not is_recurring
        self._set_visible(self.end_day_label_ctrl, self.end_day_ctrl, show_own_end)
        self._set_visible(self.end_month_label_ctrl, self.end_month_ctrl, show_own_end)
        self._set_visible(self.start_hour_label_ctrl, self.start_hour_ctrl, not is_all_day)
        self._set_visible(self.start_minute_label_ctrl, self.start_minute_ctrl, not is_all_day)
        self._set_visible(self.end_hour_label_ctrl, self.end_hour_ctrl, not is_all_day)
        self._set_visible(self.end_minute_label_ctrl, self.end_minute_ctrl, not is_all_day)
        self.Layout()
        self.scroller.FitInside()

    def _update_recurrence_controls(self):
        if not self._enable_recurrence_choice:
            if self.recurrence_choice.GetCount() > 0:
                self.recurrence_choice.SetSelection(0)
            self.recurrence_choice.Enable(False)
            self.recurrence_no_end_checkbox.SetValue(False)
            self.recurrence_no_end_checkbox.Enable(False)
            self._set_visible(self.recurrence_end_day_label_ctrl, self.recurrence_end_day_ctrl, False)
            self._set_visible(self.recurrence_end_month_label_ctrl, self.recurrence_end_month_ctrl, False)
            self._set_visible(self.recurrence_end_year_label_ctrl, self.recurrence_end_year_ctrl, False)
            self.Layout()
            self.scroller.FitInside()
            return

        recurrence_index = self.recurrence_choice.GetSelection()
        is_recurring = recurrence_index > 0
        self.recurrence_choice.Enable(True)
        self.recurrence_no_end_checkbox.Enable(is_recurring)
        if not is_recurring:
            self.recurrence_no_end_checkbox.SetValue(False)
        show_end = is_recurring and not self.recurrence_no_end_checkbox.GetValue()
        self._set_visible(self.recurrence_end_day_label_ctrl, self.recurrence_end_day_ctrl, show_end)
        self._set_visible(self.recurrence_end_month_label_ctrl, self.recurrence_end_month_ctrl, show_end)
        self._set_visible(self.recurrence_end_year_label_ctrl, self.recurrence_end_year_ctrl, show_end)
        self.Layout()
        self.scroller.FitInside()

    def _on_all_day_changed(self, event):
        self._update_time_controls()
        event.Skip()

    def _on_recurrence_changed(self, event):
        self._update_recurrence_controls()
        self._copy_default_dates_from_start_if_unchanged()
        self._update_time_controls()
        event.Skip()

    def _on_recurrence_no_end_changed(self, event):
        self._update_recurrence_controls()
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
                return

        event.Skip()

    def get_data(self):
        calendar_index = self.calendar_choice.GetSelection()
        if calendar_index == wx.NOT_FOUND:
            calendar_index = -1

        recurrence_index = self.recurrence_choice.GetSelection()
        if recurrence_index == wx.NOT_FOUND:
            recurrence_index = 0

        return {
            "title": self.title_ctrl.GetValue().strip(),
            "day": self.day_ctrl.GetValue().strip(),
            "month": self.month_ctrl.GetValue().strip(),
            "start_hour": self.start_hour_ctrl.GetValue().strip(),
            "start_minute": self.start_minute_ctrl.GetValue().strip(),
            "end_day": self.end_day_ctrl.GetValue().strip(),
            "end_month": self.end_month_ctrl.GetValue().strip(),
            "end_hour": self.end_hour_ctrl.GetValue().strip(),
            "end_minute": self.end_minute_ctrl.GetValue().strip(),
            "location": self.location_ctrl.GetValue().strip(),
            "all_day": self.all_day_checkbox.GetValue(),
            "calendar_index": calendar_index,
            "recurrence_index": recurrence_index,
            "recurrence_no_end": self.recurrence_no_end_checkbox.GetValue(),
            "recurrence_end_day": self.recurrence_end_day_ctrl.GetValue().strip(),
            "recurrence_end_month": self.recurrence_end_month_ctrl.GetValue().strip(),
            "recurrence_end_year": self.recurrence_end_year_ctrl.GetValue().strip(),
        }
