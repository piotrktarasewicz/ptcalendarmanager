from __future__ import annotations

import sys

import wx



class ExplicitNameAccessible(wx.Accessible):
    """
    Expose an explicit accessible name, description and keyboard shortcut
    while allowing wxWidgets to provide the native role, state and value.
    """

    def __init__(
        self,
        window: wx.Window,
        name: str,
        description: str = "",
        keyboard_shortcut: str = "",
    ) -> None:
        super().__init__(window)
        self._explicit_name = str(name)
        self._description = str(description or "")
        self._keyboard_shortcut = str(keyboard_shortcut or "")

    def update(
        self,
        *,
        name: str | None = None,
        description: str | None = None,
        keyboard_shortcut: str | None = None,
    ) -> None:
        if name is not None:
            self._explicit_name = str(name)
        if description is not None:
            self._description = str(description)
        if keyboard_shortcut is not None:
            self._keyboard_shortcut = str(keyboard_shortcut)

    def GetName(self, childId: int):
        if childId == 0:
            return wx.ACC_OK, self._explicit_name
        return wx.ACC_NOT_IMPLEMENTED, ""

    def GetDescription(self, childId: int):
        if childId == 0 and self._description:
            return wx.ACC_OK, self._description
        return wx.ACC_NOT_IMPLEMENTED, ""

    def GetHelpText(self, childId: int):
        if childId == 0 and self._description:
            return wx.ACC_OK, self._description
        return wx.ACC_NOT_IMPLEMENTED, ""

    def GetKeyboardShortcut(self, childId: int):
        if childId == 0 and self._keyboard_shortcut:
            return wx.ACC_OK, self._keyboard_shortcut
        return wx.ACC_NOT_IMPLEMENTED, ""


class CheckListBoxAccessible(ExplicitNameAccessible):
    """
    Add the missing MSAA checked state for wx.CheckListBox items on Windows.

    Native Windows list boxes expose selection and focus, but do not know that
    wxWidgets owner-draws a check box next to every item. Child identifiers are
    one-based in MSAA, so child 1 corresponds to item index 0.
    """

    def __init__(
        self,
        window: wx.CheckListBox,
        name: str,
        description: str = "",
    ) -> None:
        super().__init__(window, name, description)
        self._check_list = window

    def GetState(self, childId: int):
        if childId <= 0:
            return wx.ACC_NOT_IMPLEMENTED, 0

        index = childId - 1
        if index < 0 or index >= self._check_list.GetCount():
            return wx.ACC_FAIL, 0

        state = 0
        state |= getattr(wx, "ACC_STATE_SYSTEM_FOCUSABLE", 0)
        state |= getattr(wx, "ACC_STATE_SYSTEM_SELECTABLE", 0)

        if not self._check_list.IsEnabled():
            state |= getattr(wx, "ACC_STATE_SYSTEM_UNAVAILABLE", 0)

        if self._check_list.GetSelection() == index:
            state |= getattr(wx, "ACC_STATE_SYSTEM_SELECTED", 0)
            if self._check_list.HasFocus():
                state |= getattr(wx, "ACC_STATE_SYSTEM_FOCUSED", 0)

        if self._check_list.IsChecked(index):
            state |= getattr(wx, "ACC_STATE_SYSTEM_CHECKED", 0)

        return wx.ACC_OK, state


def apply_check_list_box_accessibility(
    control: wx.CheckListBox,
    name: str,
    description: str = "",
) -> CheckListBoxAccessible | None:
    """Expose a checklist name and the checked state of every list item."""

    control.SetName(str(name))
    accessible_description = str(description or "")
    if accessible_description:
        control.SetHelpText(accessible_description)
        try:
            control.SetToolTip(accessible_description)
        except Exception:
            pass

    if sys.platform != "win32":
        return None

    try:
        accessible = CheckListBoxAccessible(
            control,
            name,
            accessible_description,
        )
        control.SetAccessible(accessible)
        return accessible
    except Exception:
        return None


def notify_check_list_box_state_change(
    control: wx.CheckListBox,
    item_index: int,
) -> None:
    """Notify MSAA clients after a checklist item is checked or unchecked."""

    if sys.platform != "win32" or item_index < 0:
        return

    event_type = getattr(wx, "ACC_EVENT_OBJECT_STATECHANGE", None)
    object_type = getattr(wx, "OBJID_CLIENT", None)
    if event_type is None or object_type is None:
        return

    try:
        wx.Accessible.NotifyEvent(
            event_type,
            control,
            object_type,
            item_index + 1,
        )
    except Exception:
        pass


def apply_accessible_name(
    control: wx.Window,
    name: str,
    description: str = "",
    keyboard_shortcut: str = "",
) -> ExplicitNameAccessible | None:
    """
    Give a control an explicit programmatic name and optional shortcut.

    The ordinary wx label still contains the Windows mnemonic marked by
    an ampersand. On Windows, wx.Accessible additionally exposes the same
    access key to screen readers through GetKeyboardShortcut.
    """

    control.SetName(str(name))

    # A focused button should stay concise. Its visible label, native role and
    # Windows access key already explain how to use it. Long help text and a
    # second application shortcut made NVDA, JAWS and Narrator repeat several
    # pieces of information on every Tab press.
    is_button = isinstance(control, wx.Button)
    accessible_description = "" if is_button else str(description or "")

    if accessible_description:
        control.SetHelpText(accessible_description)
        try:
            control.SetToolTip(accessible_description)
        except Exception:
            pass
    elif is_button:
        try:
            control.SetHelpText("")
            control.UnsetToolTip()
        except Exception:
            pass

    if sys.platform != "win32":
        return None

    try:
        accessible = ExplicitNameAccessible(
            control,
            name,
            accessible_description,
            keyboard_shortcut,
        )
        control.SetAccessible(accessible)
        return accessible
    except Exception:
        return None
