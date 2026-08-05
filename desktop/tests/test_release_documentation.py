import ast
import unittest
from pathlib import Path

from gcm_core.i18n import set_language
from gcm_core.legal import about_text, legal_text, privacy_text
from gcm_core.oauth import SCOPES


class LegalDocumentTests(unittest.TestCase):
    def tearDown(self) -> None:
        set_language("pl")

    def test_polish_privacy_policy_covers_scopes_storage_and_no_server(self) -> None:
        set_language("pl")
        text = privacy_text()
        for scope in SCOPES:
            self.assertIn(scope, text)
        self.assertIn("Windows DPAPI", text)
        self.assertIn("nie prowadzi własnej zewnętrznej bazy", text)
        self.assertIn("Limited Use", text)

    def test_english_privacy_policy_covers_scopes_storage_and_no_server(self) -> None:
        set_language("en")
        text = privacy_text()
        for scope in SCOPES:
            self.assertIn(scope, text)
        self.assertIn("Windows DPAPI", text)
        self.assertIn("does not maintain an external database", text)
        self.assertIn("Limited Use", text)

    def test_about_and_legal_text_identify_product_and_independence(self) -> None:
        for language in ("pl", "en"):
            set_language(language)
            self.assertIn("PT Calendar Manager", about_text())
            self.assertIn("Google LLC", legal_text())


class AboutUiTests(unittest.TestCase):
    def test_settings_contains_about_button_and_handler(self) -> None:
        path = Path(__file__).resolve().parents[1] / "src/gcm_desktop/dialogs.py"
        source = path.read_text(encoding="utf-8")
        self.assertIn("class AboutDialog", source)
        self.assertIn("self.about_button", source)
        self.assertIn("def _on_about", source)
        self.assertIn("privacy_text()", source)
        self.assertIn("legal_text()", source)

    def test_about_handler_is_part_of_settings_not_event_form(self) -> None:
        path = Path(__file__).resolve().parents[1] / "src/gcm_desktop/dialogs.py"
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        classes = {
            node.name: node
            for node in tree.body
            if isinstance(node, ast.ClassDef)
        }
        settings_methods = {
            node.name
            for node in classes["SettingsDialog"].body
            if isinstance(node, ast.FunctionDef)
        }
        event_methods = {
            node.name
            for node in classes["EventCreateDialog"].body
            if isinstance(node, ast.FunctionDef)
        }
        self.assertIn("_on_about", settings_methods)
        self.assertNotIn("_on_about", event_methods)


if __name__ == "__main__":
    unittest.main()
