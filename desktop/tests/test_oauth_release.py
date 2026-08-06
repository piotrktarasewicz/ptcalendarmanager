from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate_oauth_client.py"


def valid_payload() -> dict[str, object]:
    return {
        "installed": {
            "client_id": "123456789-example.apps.googleusercontent.com",
            "project_id": "example-project",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": "example-not-a-real-secret",
            "redirect_uris": ["http://localhost"],
        }
    }


class OAuthReleaseTests(unittest.TestCase):
    def run_validator(self, payload: object) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "client_secret.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(VALIDATOR), str(path)],
                text=True,
                capture_output=True,
                check=False,
            )

    def test_valid_desktop_client_is_accepted(self) -> None:
        result = self.run_validator(valid_payload())
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_web_client_is_rejected(self) -> None:
        result = self.run_validator({"web": valid_payload()["installed"]})
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("example-not-a-real-secret", result.stderr)

    def test_missing_secret_is_rejected(self) -> None:
        payload = valid_payload()
        del payload["installed"]["client_secret"]  # type: ignore[index]
        result = self.run_validator(payload)
        self.assertEqual(result.returncode, 1)

    def test_release_build_copies_and_validates_oauth_client(self) -> None:
        script = (ROOT / "tools" / "build_release.ps1").read_text(
            encoding="utf-8-sig"
        )
        self.assertIn("[switch]$IncludeOAuthClient", script)
        self.assertGreaterEqual(script.count("validate_oauth_client.py"), 2)
        self.assertIn('$BundledOAuthFile = Join-Path $DistDir "client_secret.json"', script)
        self.assertIn("$SourceOAuthHash", script)
        self.assertIn("$BundledOAuthHash", script)

    def test_source_package_excludes_oauth_client(self) -> None:
        script = (ROOT / "tools" / "build_release.ps1").read_text(
            encoding="utf-8-sig"
        )
        self.assertIn('"release-secrets"', script)
        self.assertIn('$_.Name -eq "client_secret.json"', script)

    def test_pyinstaller_spec_never_reads_release_secret(self) -> None:
        spec = (ROOT / "PTCalendarManager.spec").read_text(encoding="utf-8")
        self.assertNotIn("release-secrets", spec)
        self.assertNotIn("client_secret.json", spec)


if __name__ == "__main__":
    unittest.main()
