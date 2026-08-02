from __future__ import annotations

import sys

import wx


class ExplicitNameAccessible(wx.Accessible):
    """Expose an explicit accessible name while retaining native behaviour."""

    def __init__(
        self,
        window: wx.Window,
        name: str,
        description: str = "",
    ) -> None:
        super().__init__(window)
        self._explicit_name = str(name)
        self._description = str(description or "")

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


def apply_accessible_name(
    control: wx.Window,
    name: str,
    description: str = "",
) -> wx.Accessible | None:
    """
    Give a control an explicit programmatic name.

    SetName is used as the first layer. On Windows, wx.Accessible
    supplies the same name directly through Microsoft Active
    Accessibility for screen readers.
    """

    control.SetName(str(name))
    if description:
        control.SetHelpText(str(description))

    if sys.platform != "win32":
        return None

    try:
        accessible = ExplicitNameAccessible(control, name, description)
        control.SetAccessible(accessible)
        return accessible
    except Exception:
        return None
