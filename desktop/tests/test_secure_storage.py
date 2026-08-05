import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from gcm_core import oauth
from gcm_core.paths import plaintext_token_path, token_path
from gcm_core.secure_storage import (
    TOKEN_FILE_MAGIC,
    read_protected_text,
    write_protected_text,
)


class ProtectedFileFormatTests(unittest.TestCase):
    def test_protected_file_has_magic_and_does_not_store_plaintext(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "token.dat"
            with patch(
                "gcm_core.secure_storage.protect_bytes",
                side_effect=lambda data, **kwargs: b"encrypted:" + data[::-1],
            ):
                write_protected_text(path, '{"token":"secret-value"}')
            payload = path.read_bytes()
            self.assertTrue(payload.startswith(TOKEN_FILE_MAGIC))
            self.assertNotIn(b"secret-value", payload)

    def test_protected_file_round_trip_uses_unprotect(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "token.dat"
            path.write_bytes(TOKEN_FILE_MAGIC + b"cipher")
            with patch(
                "gcm_core.secure_storage.unprotect_bytes",
                return_value=b'{"token":"value"}',
            ):
                self.assertEqual(read_protected_text(path), '{"token":"value"}')


class OAuthTokenMigrationTests(unittest.TestCase):
    def test_plaintext_token_is_encrypted_and_removed_after_success(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            encrypted = Path(directory) / "token.dat"
            plaintext = Path(directory) / "token.json"
            plaintext.write_text('{"token":"legacy"}', encoding="utf-8")
            credentials = Mock()
            credentials.to_json.return_value = '{"token":"legacy"}'

            def fake_write(path: Path, text: str) -> None:
                path.write_bytes(TOKEN_FILE_MAGIC + b"encrypted")

            with patch("gcm_core.oauth.token_path", return_value=encrypted), patch(
                "gcm_core.oauth.plaintext_token_path", return_value=plaintext
            ), patch(
                "gcm_core.oauth._credentials_from_json", return_value=credentials
            ), patch(
                "gcm_core.oauth.write_protected_text", side_effect=fake_write
            ):
                loaded = oauth.load_credentials()

            self.assertIs(loaded, credentials)
            self.assertTrue(encrypted.is_file())
            self.assertFalse(plaintext.exists())

    def test_plaintext_is_retained_when_encryption_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            encrypted = Path(directory) / "token.dat"
            plaintext = Path(directory) / "token.json"
            plaintext.write_text('{"token":"legacy"}', encoding="utf-8")
            credentials = Mock()
            with patch("gcm_core.oauth.token_path", return_value=encrypted), patch(
                "gcm_core.oauth.plaintext_token_path", return_value=plaintext
            ), patch(
                "gcm_core.oauth._credentials_from_json", return_value=credentials
            ), patch(
                "gcm_core.oauth.write_protected_text",
                side_effect=OSError("DPAPI unavailable"),
            ), patch("gcm_core.oauth.save_error"):
                loaded = oauth.load_credentials()

            self.assertIsNone(loaded)
            self.assertTrue(plaintext.is_file())
            self.assertFalse(encrypted.exists())

    def test_logout_removes_encrypted_and_legacy_tokens(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            encrypted = Path(directory) / "token.dat"
            plaintext = Path(directory) / "token.json"
            encrypted.write_bytes(b"encrypted")
            plaintext.write_text("legacy", encoding="utf-8")
            with patch("gcm_core.oauth.token_path", return_value=encrypted), patch(
                "gcm_core.oauth.plaintext_token_path", return_value=plaintext
            ):
                oauth.logout()
            self.assertFalse(encrypted.exists())
            self.assertFalse(plaintext.exists())


class TokenPathTests(unittest.TestCase):
    def test_primary_token_file_uses_dat_extension(self) -> None:
        with tempfile.TemporaryDirectory() as directory, patch.dict(
            "os.environ", {"APPDATA": directory}, clear=False
        ):
            self.assertEqual(token_path().name, "token.dat")
            self.assertEqual(plaintext_token_path().name, "token.json")


if __name__ == "__main__":
    unittest.main()
