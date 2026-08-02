import datetime as dt
import unittest

from gcm_core.models import (
    CalendarInfo,
    EventCollection,
    count_text,
    event_from_google,
    month_days,
    month_range,
    parse_polish_date,
)


class ModelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.calendar = CalendarInfo("cal-1", "Familijne", primary=True)

    def test_month_range(self) -> None:
        self.assertEqual(month_range(2026, 12), (dt.date(2026, 12, 1), dt.date(2027, 1, 1)))
        self.assertEqual(len(month_days(2026, 8)), 31)

    def test_count_text(self) -> None:
        self.assertEqual(count_text(0), "brak wydarzeń")
        self.assertEqual(count_text(1), "1 wydarzenie")
        self.assertEqual(count_text(3), "3 wydarzenia")
        self.assertEqual(count_text(8), "8 wydarzeń")

    def test_parse_date(self) -> None:
        self.assertEqual(parse_polish_date("02.08.2026"), dt.date(2026, 8, 2))
        with self.assertRaises(ValueError):
            parse_polish_date("31.02.2026")

    def test_all_day_multi_day_event(self) -> None:
        event = event_from_google(
            {
                "id": "e1",
                "summary": "Obóz",
                "start": {"date": "2026-08-02"},
                "end": {"date": "2026-08-05"},
            },
            self.calendar,
        )
        self.assertTrue(event.occurs_on(dt.date(2026, 8, 2)))
        self.assertTrue(event.occurs_on(dt.date(2026, 8, 4)))
        self.assertFalse(event.occurs_on(dt.date(2026, 8, 5)))

    def test_timed_event(self) -> None:
        event = event_from_google(
            {
                "id": "e2",
                "summary": "Spotkanie",
                "start": {"dateTime": "2026-08-02T10:00:00+02:00"},
                "end": {"dateTime": "2026-08-02T11:30:00+02:00"},
            },
            self.calendar,
        )
        self.assertFalse(event.all_day)
        self.assertEqual(event.start_date, dt.date(2026, 8, 2))
        self.assertIn(event.start_dt.strftime("%H:%M"), event.display_text(event.start_date))

    def test_collection(self) -> None:
        first = event_from_google(
            {"id": "a", "summary": "Lekarz", "start": {"date": "2026-08-03"}, "end": {"date": "2026-08-04"}},
            self.calendar,
        )
        second = event_from_google(
            {"id": "b", "summary": "Praca", "start": {"date": "2026-08-03"}, "end": {"date": "2026-08-04"}},
            self.calendar,
        )
        collection = EventCollection([first, second])
        self.assertEqual(len(collection.for_date(dt.date(2026, 8, 3))), 2)
        self.assertEqual(collection.search("lekarz")[0].event_id, "a")


if __name__ == "__main__":
    unittest.main()
