from __future__ import annotations

import re
import unittest

from gcm_core.help_content import get_help_html


class HelpContentTests(unittest.TestCase):
    def test_polish_help_has_semantic_heading_hierarchy(self) -> None:
        document = get_help_html("pl")
        self.assertEqual(len(re.findall(r"<h1(?:\s|>)", document)), 1)
        self.assertEqual(len(re.findall(r"<h2(?:\s|>)", document)), 8)
        self.assertIn('<html lang="pl">', document)
        self.assertIn("<h2>Skróty aplikacji</h2>", document)
        self.assertLess(
            document.index("<h2>Skróty aplikacji</h2>"),
            document.index("<h2>Język aplikacji</h2>"),
        )

    def test_english_help_has_matching_semantic_structure(self) -> None:
        document = get_help_html("en")
        self.assertEqual(len(re.findall(r"<h1(?:\s|>)", document)), 1)
        self.assertEqual(len(re.findall(r"<h2(?:\s|>)", document)), 8)
        self.assertIn('<html lang="en">', document)
        self.assertIn("<h2>Application shortcuts</h2>", document)

    def test_help_is_self_contained_and_non_editable(self) -> None:
        for language in ("pl", "en"):
            document = get_help_html(language)
            self.assertIn("<main", document)
            self.assertNotIn("<script", document.lower())
            self.assertNotIn("contenteditable", document.lower())


if __name__ == "__main__":
    unittest.main()
