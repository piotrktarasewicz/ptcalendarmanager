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

    def test_main_button_configuration_contains_no_long_descriptions(self) -> None:
        path = ROOT / "src/gcm_desktop/app.py"
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        main_frame = next(
            node for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name == "MainFrame"
        )
        configure = next(
            node for node in main_frame.body
            if isinstance(node, ast.FunctionDef) and node.name == "_configure_button"
        )
        parameter_names = [argument.arg for argument in configure.args.args]
        keyword_only_names = [argument.arg for argument in configure.args.kwonlyargs]
        self.assertEqual(parameter_names, ["self", "control"])
        self.assertEqual(keyword_only_names, ["name", "access_key"])

        source = path.read_text(encoding="utf-8")
        start = source.index("    def _configure_button(")
        end = source.index("    def _update_button_accessible_name(", start)
        block = source[start:end]
        self.assertNotIn("action_description", block)
        self.assertNotIn("application_shortcut", block)
        self.assertNotIn("Skrót aplikacji", block)

    def test_settings_button_uses_short_accessible_name(self) -> None:
        source = (ROOT / "src/gcm_desktop/app.py").read_text(encoding="utf-8")
        self.assertIn('(self.settings_button, tr("Ustawienia"),', source)
        self.assertNotIn('tr("Ustawienia aplikacji i wybór kalendarzy")', source)


if __name__ == "__main__":
    unittest.main()
