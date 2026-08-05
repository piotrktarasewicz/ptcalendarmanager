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
    def test_about_dialog_and_documents_remain_available(self) -> None:
        path = Path(__file__).resolve().parents[1] / "src/gcm_desktop/dialogs.py"
        source = path.read_text(encoding="utf-8")
        self.assertIn("class AboutDialog", source)
        self.assertIn("privacy_text()", source)
        self.assertIn("legal_text()", source)

    def test_about_is_opened_from_help_menu_not_settings(self) -> None:
        root = Path(__file__).resolve().parents[1]
        app_path = root / "src/gcm_desktop/app.py"
        app_source = app_path.read_text(encoding="utf-8")
        self.assertIn('self._append_menu_item(help_menu, "about"', app_source)
        self.assertIn("def _on_about", app_source)
        self.assertIn("AboutDialog(self)", app_source)

        dialogs_path = root / "src/gcm_desktop/dialogs.py"
        tree = ast.parse(dialogs_path.read_text(encoding="utf-8"), filename=str(dialogs_path))
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
        self.assertNotIn("_on_about", settings_methods)
        settings_source = ast.get_source_segment(
            dialogs_path.read_text(encoding="utf-8"),
            classes["SettingsDialog"],
        ) or ""
        self.assertNotIn("about_button", settings_source)


if __name__ == "__main__":
    unittest.main()
