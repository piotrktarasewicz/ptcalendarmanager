from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import types
import unittest


ROOT = Path(__file__).resolve().parents[1]
ACCESSIBILITY = ROOT / "src" / "gcm_desktop" / "accessibility.py"
DIALOGS = ROOT / "src" / "gcm_desktop" / "dialogs.py"


class _FakeAccessible:
    notifications: list[tuple[object, ...]] = []

    def __init__(self, window=None) -> None:
        self.window = window

    @staticmethod
    def NotifyEvent(*args) -> None:
        _FakeAccessible.notifications.append(args)


class _FakeWindow:
    pass


class _FakeButton(_FakeWindow):
    pass


class _FakeCheckListBox(_FakeWindow):
    def __init__(
        self,
        *,
        count: int,
        checked: set[int],
        selection: int,
        focused: bool = True,
        enabled: bool = True,
    ) -> None:
        self._count = count
        self._checked = set(checked)
        self._selection = selection
        self._focused = focused
        self._enabled = enabled

    def GetCount(self) -> int:
        return self._count

    def IsChecked(self, index: int) -> bool:
        return index in self._checked

    def GetSelection(self) -> int:
        return self._selection

    def HasFocus(self) -> bool:
        return self._focused

    def IsEnabled(self) -> bool:
        return self._enabled


class ChecklistAccessibleStateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        fake_wx = types.ModuleType("wx")
        fake_wx.Accessible = _FakeAccessible
        fake_wx.Window = _FakeWindow
        fake_wx.Button = _FakeButton
        fake_wx.CheckListBox = _FakeCheckListBox
        fake_wx.ACC_OK = 0
        fake_wx.ACC_FAIL = 1
        fake_wx.ACC_NOT_IMPLEMENTED = 2
        fake_wx.ACC_STATE_SYSTEM_FOCUSABLE = 0x00100000
        fake_wx.ACC_STATE_SYSTEM_SELECTABLE = 0x00200000
        fake_wx.ACC_STATE_SYSTEM_UNAVAILABLE = 0x00000001
        fake_wx.ACC_STATE_SYSTEM_SELECTED = 0x00000002
        fake_wx.ACC_STATE_SYSTEM_FOCUSED = 0x00000004
        fake_wx.ACC_STATE_SYSTEM_CHECKED = 0x00000020
        fake_wx.ACC_EVENT_OBJECT_STATECHANGE = 0x800A
        fake_wx.OBJID_CLIENT = -4

        cls._old_wx = sys.modules.get("wx")
        sys.modules["wx"] = fake_wx
        spec = importlib.util.spec_from_file_location(
            "testable_gcm_accessibility",
            ACCESSIBILITY,
        )
        assert spec is not None and spec.loader is not None
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)
        cls.fake_wx = fake_wx

    @classmethod
    def tearDownClass(cls) -> None:
        if cls._old_wx is None:
            sys.modules.pop("wx", None)
        else:
            sys.modules["wx"] = cls._old_wx

    def test_checked_state_is_independent_from_list_selection(self) -> None:
        control = _FakeCheckListBox(
            count=3,
            checked={1, 2},
            selection=1,
        )
        accessible = self.module.CheckListBoxAccessible(
            control,
            "Calendars",
        )

        _, primary_state = accessible.GetState(1)
        _, family_state = accessible.GetState(2)
        _, holidays_state = accessible.GetState(3)

        checked = self.fake_wx.ACC_STATE_SYSTEM_CHECKED
        selected = self.fake_wx.ACC_STATE_SYSTEM_SELECTED
        focused = self.fake_wx.ACC_STATE_SYSTEM_FOCUSED

        self.assertFalse(primary_state & checked)
        self.assertTrue(family_state & checked)
        self.assertTrue(holidays_state & checked)
        self.assertTrue(family_state & selected)
        self.assertTrue(family_state & focused)
        self.assertFalse(primary_state & selected)

    def test_state_change_notification_uses_one_based_child_id(self) -> None:
        _FakeAccessible.notifications.clear()
        self.module.sys = types.SimpleNamespace(platform="win32")
        control = _FakeCheckListBox(
            count=3,
            checked={2},
            selection=2,
        )

        self.module.notify_check_list_box_state_change(control, 2)

        self.assertEqual(len(_FakeAccessible.notifications), 1)
        event_type, notified_control, object_type, child_id = (
            _FakeAccessible.notifications[0]
        )
        self.assertEqual(event_type, self.fake_wx.ACC_EVENT_OBJECT_STATECHANGE)
        self.assertIs(notified_control, control)
        self.assertEqual(object_type, self.fake_wx.OBJID_CLIENT)
        self.assertEqual(child_id, 3)

    def test_dialog_initializes_only_saved_checked_items(self) -> None:
        source = DIALOGS.read_text(encoding="utf-8")
        settings_source = source.split("class SettingsDialog", 1)[1].split(
            "class SearchDialog", 1
        )[0]
        self.assertIn("self.calendar_list_ctrl.SetCheckedItems(checked_indexes)", settings_source)
        self.assertIn("selected_index = checked_indexes[0] if checked_indexes else 0", settings_source)
        self.assertIn("wx.EVT_CHECKLISTBOX", settings_source)
        self.assertIn("notify_check_list_box_state_change", settings_source)


if __name__ == "__main__":
    unittest.main()
