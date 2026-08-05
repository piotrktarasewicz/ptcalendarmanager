import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from gcm_core.branding import DATA_DIR_NAME, PRODUCT_NAME, PRODUCT_VERSION
from gcm_core.paths import app_data_dir, legacy_app_data_dirs, migrate_legacy_app_data


class ProductBrandingTests(unittest.TestCase):
    def test_official_product_name_and_version(self) -> None:
        self.assertEqual(PRODUCT_NAME, "PT Calendar Manager")
        self.assertEqual(PRODUCT_VERSION, "0.15.0")
        self.assertEqual(DATA_DIR_NAME, PRODUCT_NAME)

    def test_windows_data_directory_uses_official_name(self) -> None:
        with tempfile.TemporaryDirectory() as directory, patch.dict(
            os.environ, {"APPDATA": directory}, clear=False
        ):
            self.assertEqual(app_data_dir(), Path(directory) / "PT Calendar Manager")
            self.assertEqual(
                legacy_app_data_dirs(),
                [Path(directory) / "GCM by Piotrek"],
            )


class LegacyApplicationDataMigrationTests(unittest.TestCase):
    def test_files_are_copied_without_deleting_legacy_data(self) -> None:
        with tempfile.TemporaryDirectory() as directory, patch.dict(
            os.environ, {"APPDATA": directory}, clear=False
        ):
            legacy = Path(directory) / "GCM by Piotrek"
            legacy.mkdir()
            (legacy / "token.json").write_text('{"token": "old"}', encoding="utf-8")
            (legacy / "settings.json").write_text(
                json.dumps({"selected_calendar_ids": ["primary"], "language": "en"}),
                encoding="utf-8",
            )
            (legacy / "client_secret.json").write_text('{"installed": {}}', encoding="utf-8")

            result = migrate_legacy_app_data()
            current = Path(directory) / "PT Calendar Manager"

            self.assertTrue(result["token.json"])
            self.assertTrue(result["settings.json"])
            self.assertTrue(result["client_secret.json"])
            self.assertEqual(
                (current / "token.json").read_text(encoding="utf-8"),
                '{"token": "old"}',
            )
            self.assertTrue((legacy / "token.json").is_file())

    def test_existing_new_files_are_never_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as directory, patch.dict(
            os.environ, {"APPDATA": directory}, clear=False
        ):
            legacy = Path(directory) / "GCM by Piotrek"
            current = Path(directory) / "PT Calendar Manager"
            legacy.mkdir()
            current.mkdir()
            (legacy / "settings.json").write_text('{"language": "pl"}', encoding="utf-8")
            (current / "settings.json").write_text('{"language": "en"}', encoding="utf-8")

            result = migrate_legacy_app_data()

            self.assertFalse(result["settings.json"])
            self.assertEqual(
                (current / "settings.json").read_text(encoding="utf-8"),
                '{"language": "en"}',
            )

    def test_repeated_migration_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as directory, patch.dict(
            os.environ, {"APPDATA": directory}, clear=False
        ):
            legacy = Path(directory) / "GCM by Piotrek"
            legacy.mkdir()
            (legacy / "token.json").write_text("token", encoding="utf-8")

            first = migrate_legacy_app_data()
            second = migrate_legacy_app_data()

            self.assertTrue(first["token.json"])
            self.assertFalse(second["token.json"])


if __name__ == "__main__":
    unittest.main()
