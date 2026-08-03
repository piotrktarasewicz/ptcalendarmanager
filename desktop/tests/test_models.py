import datetime as dt
import unittest

from gcm_core.calendar_api import (
    CalendarGateway,
    build_event_body,
    build_event_patch_body,
    recurrence_until_before,
    trim_recurrence_before,
)
from gcm_core.models import (
    CalendarInfo,
    EventCollection,
    EventDraft,
    SearchCriteria,
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


class CreateEventTests(unittest.TestCase):
    def test_calendar_write_permission(self) -> None:
        self.assertTrue(CalendarInfo("a", "A", access_role="owner").can_write)
        self.assertTrue(CalendarInfo("a", "A", access_role="writer").can_write)
        self.assertFalse(CalendarInfo("a", "A", access_role="reader").can_write)

    def test_all_day_body_uses_exclusive_google_end_date(self) -> None:
        draft = EventDraft(
            calendar_id="cal-1",
            title="Urlop",
            all_day=True,
            start_date=dt.date(2026, 8, 10),
            end_date_inclusive=dt.date(2026, 8, 12),
        )
        body = build_event_body(draft, "Europe/Warsaw")
        self.assertEqual(body["start"]["date"], "2026-08-10")
        self.assertEqual(body["end"]["date"], "2026-08-13")

    def test_timed_body_preserves_dates_times_and_timezone(self) -> None:
        draft = EventDraft(
            calendar_id="cal-1",
            title="Nocne spotkanie",
            all_day=False,
            start_date=dt.date(2026, 8, 10),
            end_date_inclusive=dt.date(2026, 8, 11),
            start_time=dt.time(23, 30),
            end_time=dt.time(0, 30),
        )
        body = build_event_body(draft, "Europe/Warsaw")
        self.assertEqual(body["start"]["dateTime"], "2026-08-10T23:30:00")
        self.assertEqual(body["end"]["dateTime"], "2026-08-11T00:30:00")
        self.assertEqual(body["start"]["timeZone"], "Europe/Warsaw")

    def test_timed_event_must_end_after_start(self) -> None:
        draft = EventDraft(
            calendar_id="cal-1",
            title="Błędne",
            all_day=False,
            start_date=dt.date(2026, 8, 10),
            end_date_inclusive=dt.date(2026, 8, 10),
            start_time=dt.time(10, 0),
            end_time=dt.time(9, 0),
        )
        with self.assertRaises(ValueError):
            draft.validate()


class EditEventTests(unittest.TestCase):
    def setUp(self) -> None:
        self.calendar = CalendarInfo(
            "cal-1",
            "Główny",
            primary=True,
            access_role="owner",
            time_zone="Europe/Warsaw",
        )

    def test_all_day_event_converts_to_edit_draft(self) -> None:
        event = event_from_google(
            {
                "id": "e1",
                "summary": "Urlop",
                "start": {"date": "2026-08-10"},
                "end": {"date": "2026-08-13"},
                "location": "Dom",
            },
            self.calendar,
        )
        draft = event.to_draft()
        self.assertTrue(draft.all_day)
        self.assertEqual(draft.start_date, dt.date(2026, 8, 10))
        self.assertEqual(draft.end_date_inclusive, dt.date(2026, 8, 12))
        self.assertEqual(draft.location, "Dom")

    def test_timed_event_converts_to_edit_draft(self) -> None:
        event = event_from_google(
            {
                "id": "e2",
                "summary": "Spotkanie",
                "start": {"dateTime": "2026-08-10T23:30:00+02:00"},
                "end": {"dateTime": "2026-08-11T00:30:00+02:00"},
            },
            self.calendar,
        )
        draft = event.to_draft()
        self.assertFalse(draft.all_day)
        self.assertEqual(draft.start_time, event.start_dt.time().replace(tzinfo=None, microsecond=0))
        self.assertEqual(draft.end_date_inclusive, event.end_dt.date())
        self.assertEqual(draft.end_time, event.end_dt.time().replace(tzinfo=None, microsecond=0))

    def test_google_metadata_marks_recurring_and_attendees(self) -> None:
        event = event_from_google(
            {
                "id": "instance-1",
                "recurringEventId": "series-1",
                "summary": "Cykl",
                "attendees": [{"email": "a@example.com"}],
                "start": {"date": "2026-08-10"},
                "end": {"date": "2026-08-11"},
            },
            self.calendar,
        )
        self.assertTrue(event.is_recurring_instance)
        self.assertTrue(event.has_attendees)
        self.assertTrue(event.supports_basic_edit)


    def test_self_only_attendee_does_not_trigger_notifications(self) -> None:
        event = event_from_google(
            {
                "id": "self-1",
                "summary": "Własne wydarzenie",
                "attendees": [{"email": "me@example.com", "self": True}],
                "start": {"date": "2026-08-10"},
                "end": {"date": "2026-08-11"},
            },
            self.calendar,
        )
        self.assertFalse(event.has_attendees)

    def test_special_event_type_is_not_basic_editable(self) -> None:
        event = event_from_google(
            {
                "id": "birthday-1",
                "eventType": "birthday",
                "summary": "Urodziny",
                "start": {"date": "2026-08-10"},
                "end": {"date": "2026-08-11"},
            },
            self.calendar,
        )
        self.assertFalse(event.supports_basic_edit)

    def test_patch_body_can_clear_optional_fields(self) -> None:
        draft = EventDraft(
            calendar_id="cal-1",
            title="Nowy tytuł",
            all_day=True,
            start_date=dt.date(2026, 8, 10),
            end_date_inclusive=dt.date(2026, 8, 10),
            location="",
            description="",
        )
        body = build_event_patch_body(draft, "Europe/Warsaw")
        self.assertIn("location", body)
        self.assertIn("description", body)
        self.assertEqual(body["location"], "")
        self.assertEqual(body["description"], "")

    def test_gateway_patch_preserves_event_and_notifies_attendees(self) -> None:
        class FakeRequest:
            def __init__(self, response):
                self.response = response

            def execute(self):
                return self.response

        class FakeEvents:
            def __init__(self, response):
                self.response = response
                self.kwargs = None

            def patch(self, **kwargs):
                self.kwargs = kwargs
                return FakeRequest(self.response)

        class FakeService:
            def __init__(self, response):
                self.events_resource = FakeEvents(response)

            def events(self):
                return self.events_resource

        original = event_from_google(
            {
                "id": "e3",
                "summary": "Przed",
                "attendees": [{"email": "a@example.com"}],
                "start": {"date": "2026-08-10"},
                "end": {"date": "2026-08-11"},
            },
            self.calendar,
        )
        response = {
            "id": "e3",
            "summary": "Po",
            "attendees": [{"email": "a@example.com"}],
            "start": {"date": "2026-08-11"},
            "end": {"date": "2026-08-12"},
        }
        gateway = CalendarGateway.__new__(CalendarGateway)
        gateway._service = FakeService(response)
        draft = EventDraft(
            calendar_id="cal-1",
            title="Po",
            all_day=True,
            start_date=dt.date(2026, 8, 11),
            end_date_inclusive=dt.date(2026, 8, 11),
        )
        updated = gateway.update_event(self.calendar, original, draft)
        self.assertEqual(updated.title, "Po")
        self.assertEqual(
            gateway._service.events_resource.kwargs["sendUpdates"],
            "all",
        )
        self.assertEqual(gateway._service.events_resource.kwargs["eventId"], "e3")
        self.assertNotIn("attendees", gateway._service.events_resource.kwargs["body"])




class DeleteEventTests(unittest.TestCase):
    def setUp(self) -> None:
        self.calendar = CalendarInfo(
            "cal-1",
            "Główny",
            primary=True,
            access_role="owner",
            time_zone="Europe/Warsaw",
        )

    @staticmethod
    def _event(
        *,
        event_id: str = "e-delete",
        attendees=None,
        recurring_event_id: str = "",
        locked: bool = False,
        event_type: str = "default",
    ):
        data = {
            "id": event_id,
            "summary": "Do usunięcia",
            "start": {"date": "2026-08-10"},
            "end": {"date": "2026-08-11"},
            "locked": locked,
            "eventType": event_type,
        }
        if attendees is not None:
            data["attendees"] = attendees
        if recurring_event_id:
            data["recurringEventId"] = recurring_event_id
        return data

    @staticmethod
    def _gateway():
        class FakeRequest:
            def execute(self):
                return None

        class FakeEvents:
            def __init__(self):
                self.kwargs = None

            def delete(self, **kwargs):
                self.kwargs = kwargs
                return FakeRequest()

        class FakeService:
            def __init__(self):
                self.events_resource = FakeEvents()

            def events(self):
                return self.events_resource

        gateway = CalendarGateway.__new__(CalendarGateway)
        gateway._service = FakeService()
        return gateway

    def test_delete_sends_updates_to_real_attendees(self) -> None:
        event = event_from_google(
            self._event(attendees=[{"email": "guest@example.com"}]),
            self.calendar,
        )
        gateway = self._gateway()
        gateway.delete_event(self.calendar, event)
        self.assertEqual(gateway._service.events_resource.kwargs["sendUpdates"], "all")

    def test_delete_does_not_notify_when_only_owner_is_present(self) -> None:
        event = event_from_google(
            self._event(attendees=[{"email": "me@example.com", "self": True}]),
            self.calendar,
        )
        gateway = self._gateway()
        gateway.delete_event(self.calendar, event)
        self.assertEqual(gateway._service.events_resource.kwargs["sendUpdates"], "none")

    def test_recurring_instance_uses_instance_id_not_series_id(self) -> None:
        event = event_from_google(
            self._event(
                event_id="instance-20260810",
                recurring_event_id="series-1",
            ),
            self.calendar,
        )
        gateway = self._gateway()
        gateway.delete_event(self.calendar, event)
        self.assertEqual(
            gateway._service.events_resource.kwargs["eventId"],
            "instance-20260810",
        )
        self.assertNotEqual(
            gateway._service.events_resource.kwargs["eventId"],
            event.recurring_event_id,
        )

    def test_special_event_type_can_be_deleted(self) -> None:
        event = event_from_google(
            self._event(event_type="birthday"),
            self.calendar,
        )
        self.assertTrue(event.supports_delete)
        gateway = self._gateway()
        gateway.delete_event(self.calendar, event)
        self.assertEqual(
            gateway._service.events_resource.kwargs["eventId"],
            event.event_id,
        )

    def test_locked_event_is_rejected(self) -> None:
        event = event_from_google(
            self._event(locked=True),
            self.calendar,
        )
        self.assertFalse(event.supports_delete)
        gateway = self._gateway()
        with self.assertRaises(ValueError):
            gateway.delete_event(self.calendar, event)

    def test_read_only_calendar_is_rejected(self) -> None:
        read_only = CalendarInfo(
            "cal-1",
            "Tylko odczyt",
            access_role="reader",
        )
        event = event_from_google(self._event(), read_only)
        gateway = self._gateway()
        with self.assertRaises(PermissionError):
            gateway.delete_event(read_only, event)

    def test_event_from_another_calendar_is_rejected(self) -> None:
        other_calendar = CalendarInfo(
            "cal-2",
            "Inny",
            access_role="owner",
        )
        event = event_from_google(self._event(), other_calendar)
        gateway = self._gateway()
        with self.assertRaises(ValueError):
            gateway.delete_event(self.calendar, event)




class RecurringDeleteScopeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.calendar = CalendarInfo(
            "cal-1",
            "Główny",
            access_role="owner",
            time_zone="Europe/Warsaw",
        )

    def _instance(
        self,
        *,
        original_date: str = "2026-08-17",
        timed: bool = False,
        attendees=None,
    ):
        if timed:
            start = {"dateTime": "2026-08-17T10:00:00+02:00"}
            end = {"dateTime": "2026-08-17T11:00:00+02:00"}
            original = {"dateTime": original_date}
        else:
            start = {"date": "2026-08-17"}
            end = {"date": "2026-08-18"}
            original = {"date": original_date}
        data = {
            "id": "instance-2",
            "recurringEventId": "series-1",
            "originalStartTime": original,
            "summary": "Cykl",
            "start": start,
            "end": end,
        }
        if attendees is not None:
            data["attendees"] = attendees
        return event_from_google(data, self.calendar)

    @staticmethod
    def _gateway(parent):
        class FakeRequest:
            def __init__(self, response=None):
                self.response = response

            def execute(self):
                return self.response

        class FakeEvents:
            def __init__(self, parent_event):
                self.parent_event = parent_event
                self.get_kwargs = None
                self.update_kwargs = None
                self.delete_kwargs = None

            def get(self, **kwargs):
                self.get_kwargs = kwargs
                return FakeRequest(dict(self.parent_event))

            def update(self, **kwargs):
                self.update_kwargs = kwargs
                return FakeRequest(kwargs["body"])

            def delete(self, **kwargs):
                self.delete_kwargs = kwargs
                return FakeRequest(None)

        class FakeService:
            def __init__(self, parent_event):
                self.events_resource = FakeEvents(parent_event)

            def events(self):
                return self.events_resource

        gateway = CalendarGateway.__new__(CalendarGateway)
        gateway._service = FakeService(parent)
        return gateway

    def test_original_start_time_is_retained(self) -> None:
        event = self._instance()
        self.assertEqual(event.original_start, dt.date(2026, 8, 17))

    def test_all_day_until_is_previous_date(self) -> None:
        self.assertEqual(
            recurrence_until_before(dt.date(2026, 8, 17)),
            "20260816",
        )

    def test_timed_until_is_utc_second_before(self) -> None:
        marker = dt.datetime(
            2026,
            8,
            17,
            10,
            0,
            tzinfo=dt.timezone(dt.timedelta(hours=2)),
        )
        self.assertEqual(
            recurrence_until_before(marker),
            "20260817T075959Z",
        )

    def test_trim_replaces_count_and_preserves_exdate(self) -> None:
        result = trim_recurrence_before(
            [
                "RRULE:FREQ=WEEKLY;COUNT=10;BYDAY=MO",
                "EXDATE;VALUE=DATE:20260824",
            ],
            dt.date(2026, 8, 17),
        )
        self.assertEqual(
            result[0],
            "RRULE:FREQ=WEEKLY;BYDAY=MO;UNTIL=20260816",
        )
        self.assertEqual(result[1], "EXDATE;VALUE=DATE:20260824")

    def test_delete_following_updates_parent_rrule(self) -> None:
        parent = {
            "id": "series-1",
            "summary": "Cykl",
            "start": {"date": "2026-08-03"},
            "end": {"date": "2026-08-04"},
            "recurrence": ["RRULE:FREQ=WEEKLY;COUNT=10"],
        }
        gateway = self._gateway(parent)
        whole_series_deleted = gateway.delete_recurring_from(
            self.calendar,
            self._instance(),
        )
        self.assertFalse(whole_series_deleted)
        events = gateway._service.events_resource
        self.assertIsNone(events.delete_kwargs)
        self.assertEqual(events.update_kwargs["eventId"], "series-1")
        self.assertEqual(
            events.update_kwargs["body"]["recurrence"],
            ["RRULE:FREQ=WEEKLY;UNTIL=20260816"],
        )

    def test_delete_following_from_first_deletes_parent(self) -> None:
        parent = {
            "id": "series-1",
            "summary": "Cykl",
            "start": {"date": "2026-08-17"},
            "end": {"date": "2026-08-18"},
            "recurrence": ["RRULE:FREQ=WEEKLY;COUNT=10"],
        }
        gateway = self._gateway(parent)
        whole_series_deleted = gateway.delete_recurring_from(
            self.calendar,
            self._instance(),
        )
        self.assertTrue(whole_series_deleted)
        events = gateway._service.events_resource
        self.assertIsNone(events.update_kwargs)
        self.assertEqual(events.delete_kwargs["eventId"], "series-1")

    def test_delete_whole_series_uses_parent_id(self) -> None:
        gateway = self._gateway({})
        gateway.delete_recurring_series(self.calendar, self._instance())
        self.assertEqual(
            gateway._service.events_resource.delete_kwargs["eventId"],
            "series-1",
        )

    def test_delete_series_notifies_guests(self) -> None:
        gateway = self._gateway({})
        event = self._instance(attendees=[{"email": "guest@example.com"}])
        gateway.delete_recurring_series(self.calendar, event)
        self.assertEqual(
            gateway._service.events_resource.delete_kwargs["sendUpdates"],
            "all",
        )

    def test_non_recurring_event_is_rejected_for_series_delete(self) -> None:
        event = event_from_google(
            {
                "id": "one",
                "summary": "Jednorazowe",
                "start": {"date": "2026-08-17"},
                "end": {"date": "2026-08-18"},
            },
            self.calendar,
        )
        gateway = self._gateway({})
        with self.assertRaises(ValueError):
            gateway.delete_recurring_series(self.calendar, event)




class SearchRangeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.calendar = CalendarInfo(
            "cal-1",
            "Rodzinne",
            access_role="owner",
        )

    def test_search_range_end_is_inclusive(self) -> None:
        criteria = SearchCriteria(
            query="lekarz",
            start_date=dt.date(2026, 8, 3),
            end_date_inclusive=dt.date(2026, 8, 10),
        )
        self.assertEqual(criteria.end_date_exclusive, dt.date(2026, 8, 11))

    def test_search_rejects_reversed_range(self) -> None:
        criteria = SearchCriteria(
            query="spotkanie",
            start_date=dt.date(2026, 8, 10),
            end_date_inclusive=dt.date(2026, 8, 3),
        )
        with self.assertRaises(ValueError):
            criteria.validate()

    def test_search_rejects_empty_query(self) -> None:
        criteria = SearchCriteria(
            query="   ",
            start_date=dt.date(2026, 8, 3),
            end_date_inclusive=dt.date(2026, 8, 10),
        )
        with self.assertRaises(ValueError):
            criteria.validate()

    def test_gateway_fetches_full_range_and_filters_locally(self) -> None:
        doctor = event_from_google(
            {
                "id": "doctor",
                "summary": "Lekarz kontrola",
                "start": {"date": "2026-08-10"},
                "end": {"date": "2026-08-11"},
            },
            self.calendar,
        )
        work = event_from_google(
            {
                "id": "work",
                "summary": "Praca",
                "start": {"date": "2026-08-09"},
                "end": {"date": "2026-08-10"},
            },
            self.calendar,
        )
        captured = {}
        gateway = CalendarGateway.__new__(CalendarGateway)

        def fake_list_events(calendars, start_date, end_date):
            captured["calendars"] = calendars
            captured["start"] = start_date
            captured["end"] = end_date
            return [work, doctor]

        gateway.list_events = fake_list_events
        criteria = SearchCriteria(
            query="lekarz",
            start_date=dt.date(2026, 8, 1),
            end_date_inclusive=dt.date(2026, 8, 10),
        )
        results = gateway.search_events([self.calendar], criteria)
        self.assertEqual(captured["start"], dt.date(2026, 8, 1))
        self.assertEqual(captured["end"], dt.date(2026, 8, 11))
        self.assertEqual([event.event_id for event in results], ["doctor"])

    def test_search_matches_calendar_name(self) -> None:
        event = event_from_google(
            {
                "id": "family",
                "summary": "Obiad",
                "start": {"date": "2026-08-10"},
                "end": {"date": "2026-08-11"},
            },
            self.calendar,
        )
        gateway = CalendarGateway.__new__(CalendarGateway)
        gateway.list_events = lambda calendars, start, end: [event]
        criteria = SearchCriteria(
            query="rodzinne",
            start_date=dt.date(2026, 8, 1),
            end_date_inclusive=dt.date(2026, 8, 31),
        )
        results = gateway.search_events([self.calendar], criteria)
        self.assertEqual(results[0].event_id, "family")


if __name__ == "__main__":
    unittest.main()
