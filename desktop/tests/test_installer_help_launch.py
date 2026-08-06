from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class InstallerHelpLaunchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.installer = (ROOT / "installer" / "PTCalendarManager.iss").read_text(
            encoding="utf-8-sig"
        )

    def test_installer_version_is_current(self) -> None:
        self.assertIn('#define MyAppVersion "0.16.3"', self.installer)
        self.assertIn("VersionInfoVersion=0.16.3.0", self.installer)

    def test_finish_checkbox_opens_in_app_help(self) -> None:
        self.assertIn(
            "polish.OpenHelpAndShortcuts=Otwórz pomoc i skróty programu",
            self.installer,
        )
        run_section = self.installer.split("[Run]", 1)[1].split("[CustomMessages]", 1)[0]
        self.assertEqual(run_section.count("Filename:"), 1)
        self.assertIn('Parameters: "--show-help"', run_section)
        self.assertNotIn("shellexec", run_section.lower())
        self.assertNotIn("SKROTY_pl.txt", run_section)

    def test_start_menu_documentation_opens_same_help_view(self) -> None:
        icons_section = self.installer.split("[Icons]", 1)[1].split("[Run]", 1)[0]
        documentation_lines = [
            line
            for line in icons_section.splitlines()
            if "Dokumentacja" in line or "Documentation" in line
        ]
        self.assertEqual(len(documentation_lines), 2)
        self.assertTrue(all('Parameters: "--show-help"' in line for line in documentation_lines))


if __name__ == "__main__":
    unittest.main()
