import datetime as dt
import unittest

from gcm_wx_prototype.model import (
    EventStore,
    count_text,
    format_day_item,
    parse_polish_date,
    parse_time,
)


class ModelTests(unittest.TestCase):
    def test_parse_polish_date(self) -> None:
        self.assertEqual(parse_polish_date("02.08.2026"), dt.date(2026, 8, 2))
        self.assertEqual(parse_polish_date("2-8-2026"), dt.date(2026, 8, 2))

    def test_parse_invalid_date(self) -> None:
        with self.assertRaises(ValueError):
            parse_polish_date("31.02.2026")

    def test_parse_time(self) -> None:
        self.assertEqual(parse_time("09:05"), dt.time(9, 5))

    def test_count_text(self) -> None:
        self.assertEqual(count_text(0), "brak wydarzeń")
        self.assertEqual(count_text(1), "1 wydarzenie")
        self.assertEqual(count_text(3), "3 wydarzenia")
        self.assertEqual(count_text(8), "8 wydarzeń")

    def test_days_and_events(self) -> None:
        store = EventStore(reference_date=dt.date(2026, 8, 2))
        self.assertEqual(len(store.month_days(2026, 8)), 31)
        self.assertEqual(len(store.events_for_date(dt.date(2026, 8, 2))), 2)
        label = format_day_item(dt.date(2026, 8, 2), 2)
        self.assertIn("niedziela", label)
        self.assertIn("2 wydarzenia", label)

    def test_add_update_delete(self) -> None:
        store = EventStore(reference_date=dt.date(2026, 8, 2))
        event = store.add_event(
            date=dt.date(2026, 8, 20),
            title="Nowe wydarzenie",
            calendar_name="Praca",
            all_day=False,
            start_time=dt.time(10, 0),
            end_time=dt.time(11, 0),
            location="Kraków",
            description="Test",
        )
        self.assertIsNotNone(store.get_event(event.event_id))
        updated = store.update_event(event.event_id, title="Zmienione")
        self.assertEqual(updated.title, "Zmienione")
        store.delete_event(event.event_id)
        self.assertIsNone(store.get_event(event.event_id))


if __name__ == "__main__":
    unittest.main()
