from __future__ import annotations

import sys

import wx

from gcm_core.i18n import tr


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

    help_parts = []
    if description:
        help_parts.append(str(description))
    if keyboard_shortcut:
        help_parts.append(tr("Klawisz dostępu: {shortcut}.", shortcut=keyboard_shortcut))
    help_text = " ".join(help_parts)

    if help_text:
        control.SetHelpText(help_text)
        try:
            control.SetToolTip(help_text)
        except Exception:
            pass

    if sys.platform != "win32":
        return None

    try:
        accessible = ExplicitNameAccessible(
            control,
            name,
            help_text,
            keyboard_shortcut,
        )
        control.SetAccessible(accessible)
        return accessible
    except Exception:
        return None
