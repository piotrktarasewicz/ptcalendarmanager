from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DIALOGS = ROOT / "src" / "gcm_desktop" / "dialogs.py"
ACCESSIBILITY = ROOT / "src" / "gcm_desktop" / "accessibility.py"


class NativeCalendarListAccessibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        source = DIALOGS.read_text(encoding="utf-8")
        cls.settings_source = source.split("class SettingsDialog", 1)[1].split(
            "class SearchDialog", 1
        )[0]
        cls.accessibility_source = ACCESSIBILITY.read_text(encoding="utf-8")

    def test_uses_native_windows_list_view_with_checkboxes(self) -> None:
        self.assertIn("self.calendar_list_ctrl = wx.ListCtrl", self.settings_source)
        self.assertIn("wx.LC_REPORT", self.settings_source)
        self.assertIn("wx.LC_SINGLE_SEL", self.settings_source)
        self.assertIn("wx.LC_NO_HEADER", self.settings_source)
        self.assertIn("EnableCheckBoxes(True)", self.settings_source)

    def test_native_accessibility_provider_is_not_replaced(self) -> None:
        self.assertIn("SetAccessible() is intentionally not", self.settings_source)
        self.assertNotIn("apply_check_list_box_accessibility", self.settings_source)
        self.assertNotIn("CheckListBoxAccessible", self.accessibility_source)
        self.assertNotIn("notify_check_list_box_state_change", self.accessibility_source)

    def test_focus_and_check_state_are_initialized_independently(self) -> None:
        self.assertIn("self.calendar_list_ctrl.CheckItem(index, True)", self.settings_source)
        self.assertIn("self.calendar_list_ctrl.Select(0)", self.settings_source)
        self.assertIn("self.calendar_list_ctrl.Focus(0)", self.settings_source)
        self.assertNotIn("selected_index = checked_indexes[0]", self.settings_source)

    def test_saved_calendars_are_read_from_native_checkbox_state(self) -> None:
        self.assertIn("self.calendar_list_ctrl.IsItemChecked(index)", self.settings_source)

    def test_list_column_tracks_available_width(self) -> None:
        self.assertIn("def _on_calendar_list_size", self.settings_source)
        self.assertIn("SetColumnWidth(0, width)", self.settings_source)


if __name__ == "__main__":
    unittest.main()
