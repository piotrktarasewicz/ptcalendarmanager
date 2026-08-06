# Copyright (C) 2026 Piotr Tarasewicz
# SPDX-License-Identifier: GPL-3.0-or-later

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
