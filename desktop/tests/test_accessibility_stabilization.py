import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class QuietButtonAccessibilityTests(unittest.TestCase):
    def test_accessibility_layer_suppresses_descriptions_for_buttons(self) -> None:
        source = (ROOT / "src/gcm_desktop/accessibility.py").read_text(encoding="utf-8")
        self.assertIn("is_button = isinstance(control, wx.Button)", source)
        self.assertIn('accessible_description = "" if is_button', source)
        self.assertNotIn('tr("Klawisz dostępu:', source)

    def test_main_window_contains_no_command_buttons(self) -> None:
        path = ROOT / "src/gcm_desktop/app.py"
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        main_frame = next(
            node for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name == "MainFrame"
        )
        initializer = next(
            node for node in main_frame.body
            if isinstance(node, ast.FunctionDef) and node.name == "__init__"
        )
        button_calls = [
            node
            for node in ast.walk(initializer)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "wx"
            and node.func.attr == "Button"
        ]
        self.assertEqual(button_calls, [])

    def test_settings_is_a_short_native_menu_command(self) -> None:
        source = (ROOT / "src/gcm_desktop/app.py").read_text(encoding="utf-8")
        self.assertIn('menu_bar.Append(settings_menu, tr("&Ustawienia"))', source)
        self.assertIn('tr("Us&tawienia")', source)
        self.assertNotIn("self.settings_button", source)


if __name__ == "__main__":
    unittest.main()
