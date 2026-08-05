import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "src/gcm_desktop/app.py"


class NativeMenuLayoutTests(unittest.TestCase):
    def test_main_window_uses_five_native_menus(self) -> None:
        source = APP_PATH.read_text(encoding="utf-8")
        self.assertIn("menu_bar = wx.MenuBar()", source)
        for label in ("&Kalendarz", "&Wydarzenie", "Ko&nto", "&Ustawienia", "&Pomoc"):
            self.assertIn(f'tr("{label}")', source)

    def test_shortcuts_are_displayed_next_to_menu_commands(self) -> None:
        source = APP_PATH.read_text(encoding="utf-8")
        for shortcut in (
            "Ctrl+N", "Ctrl+E", "Delete", "Ctrl+F", "Ctrl+G", "Ctrl+D",
            "F5", "F1", "Ctrl+Shift+G", "Ctrl+J", "Ctrl+L", "Ctrl+,",
        ):
            self.assertIn(f'"{shortcut}"', source)

    def test_both_lists_have_context_menus(self) -> None:
        source = APP_PATH.read_text(encoding="utf-8")
        self.assertIn("self.days_list.Bind(wx.EVT_CONTEXT_MENU", source)
        self.assertIn("self.events_list.Bind(wx.EVT_CONTEXT_MENU", source)
        self.assertIn("def _on_days_context_menu", source)
        self.assertIn("def _on_events_context_menu", source)

    def test_tab_cycles_only_between_the_two_lists(self) -> None:
        source = APP_PATH.read_text(encoding="utf-8")
        self.assertIn("if event.GetKeyCode() == wx.WXK_TAB", source)
        self.assertIn("self.events_list.SetFocus()", source)
        self.assertIn("self.days_list.SetFocus()", source)

    def test_visual_accent_uses_windows_system_colours(self) -> None:
        source = APP_PATH.read_text(encoding="utf-8")
        self.assertIn("wx.SystemSettings.GetColour(wx.SYS_COLOUR_HOTLIGHT)", source)
        self.assertNotIn("wx.Colour(", source)
        self.assertNotIn("SetBackgroundColour", source)

    def test_status_bar_separates_operation_and_account_state(self) -> None:
        source = APP_PATH.read_text(encoding="utf-8")
        self.assertIn("self.CreateStatusBar(2)", source)
        self.assertIn("self.status_bar.SetStatusText(text, 0)", source)
        self.assertIn("self.status_bar.SetStatusText(", source)
        self.assertIn("Konto Google: połączone", source)


if __name__ == "__main__":
    unittest.main()
