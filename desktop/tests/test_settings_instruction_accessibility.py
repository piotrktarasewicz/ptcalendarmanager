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

    def test_calendar_instruction_is_focusable_read_only_text(self) -> None:
        self.assertIn("self.calendar_instruction = wx.TextCtrl", self.dialog_source)
        self.assertIn("wx.TE_READONLY", self.dialog_source)
        self.assertIn("wx.BORDER_NONE", self.dialog_source)
        self.assertIn("wx.TE_NO_VSCROLL", self.dialog_source)

    def test_instruction_has_programmatic_name_and_translation(self) -> None:
        self.assertIn('tr("Instrukcja wyboru kalendarzy")', self.dialog_source)
        self.assertIn(
            '"Instrukcja wyboru kalendarzy": "Calendar selection instructions"',
            self.i18n_source,
        )

    def test_old_non_focusable_static_text_is_not_used_for_instruction(self) -> None:
        old_fragment = "info = wx.StaticText(\\n                self,\\n                label=tr(\\n                    \\\"Zaznacz kalendarze"
        self.assertNotIn(old_fragment, self.dialog_source)


if __name__ == "__main__":
    unittest.main()
