import ast
import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from gcm_core.i18n import (
    ENGLISH_TRANSLATIONS,
    detect_system_language,
    get_language,
    language_choice_labels,
    resolve_language,
    set_language,
    tr,
)
from gcm_core.models import (
    CalendarInfo,
    RecurrenceSettings,
    count_text,
    event_from_google,
    format_full_date,
    format_month,
    parse_date_input,
    recurrence_choices,
)
from gcm_core.settings import AppSettings, load_settings, save_settings


class LanguageResolutionTests(unittest.TestCase):
    def tearDown(self) -> None:
        set_language("pl")

    def test_automatic_language_uses_polish_only_for_polish_system(self) -> None:
        self.assertEqual(detect_system_language("pl-PL"), "pl")
        self.assertEqual(detect_system_language("pl_PL.UTF-8"), "pl")
        self.assertEqual(detect_system_language("en-US"), "en")
        self.assertEqual(detect_system_language("de-DE"), "en")
        self.assertEqual(resolve_language("auto", "pl-PL"), "pl")
        self.assertEqual(resolve_language("auto", "en-US"), "en")

    def test_manual_choice_overrides_system_language(self) -> None:
        self.assertEqual(resolve_language("en", "pl-PL"), "en")
        self.assertEqual(resolve_language("pl", "en-US"), "pl")

    def test_restart_is_only_needed_when_effective_language_changes(self) -> None:
        self.assertEqual(resolve_language("auto", "pl-PL"), resolve_language("pl", "pl-PL"))
        self.assertNotEqual(resolve_language("auto", "pl-PL"), resolve_language("en", "pl-PL"))

    def test_language_labels_are_localized(self) -> None:
        set_language("pl")
        self.assertEqual(
            language_choice_labels(),
            ("Automatycznie, zgodnie z językiem systemu", "Polski", "English"),
        )
        set_language("en")
        self.assertEqual(
            language_choice_labels(),
            ("Automatic, use the system language", "Polish", "English"),
        )


class EnglishPresentationTests(unittest.TestCase):
    def setUp(self) -> None:
        set_language("en")

    def tearDown(self) -> None:
        set_language("pl")

    def test_dates_counts_and_recurrence_are_english(self) -> None:
        value = dt.date(2026, 8, 4)
        self.assertEqual(format_full_date(value), "Tuesday, 4 August 2026")
        self.assertEqual(format_month(2026, 8), "August 2026")
        self.assertEqual(count_text(0), "no events")
        self.assertEqual(count_text(1), "1 event")
        self.assertEqual(count_text(8), "8 events")
        labels = [label for _, label in recurrence_choices()]
        self.assertIn("Every 3 months", labels)
        self.assertIn("Every 6 months", labels)
        self.assertEqual(
            RecurrenceSettings("quarterly", value).display_text(),
            "Every 3 months, through 04.08.2026, inclusive",
        )

    def test_event_details_are_english(self) -> None:
        event = event_from_google(
            {
                "id": "meet-en",
                "summary": "Review",
                "htmlLink": "https://calendar.google.com/calendar/event?eid=test",
                "hangoutLink": "https://meet.google.com/abc-defg-hij",
                "conferenceData": {"conferenceSolution": {"name": "Google Meet"}},
                "start": {"date": "2026-08-04"},
                "end": {"date": "2026-08-05"},
            },
            CalendarInfo("cal", "Work", primary=True),
        )
        details = event.details_text()
        self.assertIn("Title: Review", details)
        self.assertIn("Calendar: Work", details)
        self.assertIn("Meeting link:", details)
        self.assertIn("Event page in Google Calendar: available", details)

    def test_both_date_input_formats_are_accepted(self) -> None:
        expected = dt.date(2026, 8, 4)
        self.assertEqual(parse_date_input("04.08.2026"), expected)
        self.assertEqual(parse_date_input("2026-08-04"), expected)


class SettingsMigrationTests(unittest.TestCase):
    def tearDown(self) -> None:
        set_language("pl")

    def test_old_settings_without_language_migrate_to_auto(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "settings.json"
            path.write_text(
                json.dumps({"selected_calendar_ids": ["primary"]}),
                encoding="utf-8",
            )
            with patch("gcm_core.settings.settings_path", return_value=path):
                settings = load_settings()
            self.assertEqual(settings.selected_calendar_ids, ["primary"])
            self.assertEqual(settings.language, "auto")

    def test_language_and_calendars_are_saved_together(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "settings.json"
            with patch("gcm_core.settings.settings_path", return_value=path):
                save_settings(AppSettings(["one", "two"], "en"))
                loaded = load_settings()
            self.assertEqual(loaded, AppSettings(["one", "two"], "en"))


class TranslationCoverageTests(unittest.TestCase):
    def test_every_constant_tr_key_has_an_english_translation(self) -> None:
        root = Path(__file__).resolve().parents[1] / "src"
        missing: list[str] = []
        for path in root.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                if not isinstance(node.func, ast.Name) or node.func.id != "tr":
                    continue
                if not node.args or not isinstance(node.args[0], ast.Constant):
                    continue
                key = node.args[0].value
                if isinstance(key, str) and key not in ENGLISH_TRANSLATIONS:
                    missing.append(f"{path.name}:{node.lineno}: {key}")
        self.assertEqual(missing, [])

    def test_translation_function_formats_values(self) -> None:
        set_language("en")
        self.assertEqual(
            tr("Ustawienia zostały zapisane."),
            "Settings have been saved.",
        )
        set_language("pl")
        self.assertEqual(
            tr("Ustawienia zostały zapisane."),
            "Ustawienia zostały zapisane.",
        )


if __name__ == "__main__":
    unittest.main()
