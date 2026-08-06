from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DIALOGS = ROOT / "src" / "gcm_desktop" / "dialogs.py"
I18N = ROOT / "src" / "gcm_core" / "i18n.py"


class SettingsInstructionAccessibilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.dialog_source = DIALOGS.read_text(encoding="utf-8")
        self.i18n_source = I18N.read_text(encoding="utf-8")
        self.settings_source = self.dialog_source.split(
            "class SettingsDialog", 1
        )[1].split("class SearchDialog", 1)[0]

    def test_calendar_selection_is_one_native_check_list(self) -> None:
        self.assertIn("self.calendar_list_ctrl = wx.CheckListBox", self.settings_source)
        self.assertNotIn("wx.ScrolledWindow", self.settings_source)
        self.assertNotIn("self._checkboxes", self.settings_source)

    def test_accessible_name_is_attached_to_the_focused_control(self) -> None:
        self.assertIn(
            "calendar_list_accessible = apply_accessible_name(\n"
            "                self.calendar_list_ctrl,\n"
            "                accessible_name,\n"
            "                accessible_description,",
            self.settings_source,
        )
        self.assertIn(
            '"Kalendarze do wyświetlania": "Calendars to display"',
            self.i18n_source,
        )

    def test_check_list_has_compact_keyboard_model(self) -> None:
        self.assertIn("style=wx.LB_SINGLE", self.settings_source)
        self.assertIn("self.calendar_list_ctrl.IsChecked(index)", self.settings_source)
        self.assertIn("self.calendar_list_ctrl.Check(", self.settings_source)
        self.assertIn("Naciśnij spację", self.settings_source)

    def test_dialog_does_not_use_the_old_tall_panel(self) -> None:
        self.assertNotIn("SetMinSize((580, 280))", self.settings_source)
        self.assertIn("SetMinSize((580, 220))", self.settings_source)
        self.assertIn("self.SetSize((700, 470))", self.settings_source)


if __name__ == "__main__":
    unittest.main()
