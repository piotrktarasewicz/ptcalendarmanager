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

    def test_calendar_controls_use_a_real_native_group_box(self) -> None:
        self.assertIn("calendar_group = wx.StaticBox", self.dialog_source)
        self.assertIn("calendar_group,\n                style=wx.VSCROLL", self.dialog_source)
        self.assertIn("calendar_group,\n                label=instruction_text", self.dialog_source)

    def test_group_exposes_the_instruction_programmatically(self) -> None:
        self.assertIn(
            "group_accessible = apply_accessible_name(\n"
            "                calendar_group,\n"
            "                calendar_group_label,\n"
            "                instruction_text,",
            self.dialog_source,
        )
        self.assertIn(
            '"Zaznacz kalendarze, których wydarzenia mają być wyświetlane.": '
            '"Select the calendars whose events should be displayed."',
            self.i18n_source,
        )

    def test_instruction_is_compact_static_text_not_a_focus_target(self) -> None:
        settings_source = self.dialog_source.split("class SettingsDialog", 1)[1].split("class SearchDialog", 1)[0]
        self.assertNotIn("self.calendar_instruction = wx.TextCtrl", settings_source)
        self.assertNotIn("wx.TE_READONLY", settings_source)
        self.assertNotIn("SetMinSize((580, 46))", settings_source)


if __name__ == "__main__":
    unittest.main()
