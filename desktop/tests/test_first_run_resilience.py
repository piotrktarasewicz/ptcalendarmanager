import ast
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from gcm_core import oauth


class OAuthUiStateTests(unittest.TestCase):
    def test_is_logged_in_does_not_refresh_token_or_use_network(self) -> None:
        credentials = Mock(valid=False, refresh_token="refresh-token")
        with patch("gcm_core.oauth.load_credentials", return_value=credentials), patch(
            "gcm_core.oauth.ensure_valid_credentials",
            side_effect=AssertionError("network refresh must not run"),
        ):
            self.assertTrue(oauth.is_logged_in())

    def test_is_logged_in_is_false_without_saved_credentials(self) -> None:
        with patch("gcm_core.oauth.load_credentials", return_value=None):
            self.assertFalse(oauth.is_logged_in())

    def test_valid_saved_credentials_are_recognized_locally(self) -> None:
        credentials = Mock(valid=True, refresh_token=None)
        with patch("gcm_core.oauth.load_credentials", return_value=credentials):
            self.assertTrue(oauth.is_logged_in())


class SettingsIndependenceTests(unittest.TestCase):
    def test_settings_handler_does_not_start_google_task(self) -> None:
        path = Path(__file__).resolve().parents[1] / "src/gcm_desktop/app.py"
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        main_frame = next(
            node for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name == "MainFrame"
        )
        handler = next(
            node for node in main_frame.body
            if isinstance(node, ast.FunctionDef) and node.name == "_on_settings"
        )
        calls = [
            node.func.attr
            for node in ast.walk(handler)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        ]
        self.assertIn("_show_settings_dialog", calls)
        self.assertNotIn("_run_task", calls)

    def test_settings_button_is_not_disabled_by_google_busy_state(self) -> None:
        path = Path(__file__).resolve().parents[1] / "src/gcm_desktop/app.py"
        source = path.read_text(encoding="utf-8")
        start = source.index("    def _set_busy(")
        end = source.index("    def _run_task(", start)
        block = source[start:end]
        self.assertNotIn("self.settings_button,", block)


if __name__ == "__main__":
    unittest.main()
