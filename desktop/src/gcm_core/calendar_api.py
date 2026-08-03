from __future__ import annotations

import datetime as dt

from .models import (
    CalendarEvent,
    CalendarInfo,
    EventCollection,
    EventDraft,
    SearchCriteria,
    event_from_google,
    parse_google_start_marker,
)


def _build_event_time(draft: EventDraft, time_zone: str) -> tuple[dict, dict]:
    if draft.all_day:
        return (
            {"date": draft.start_date.isoformat()},
            {"date": (draft.end_date_inclusive + dt.timedelta(days=1)).isoformat()},
        )
    start_dt = dt.datetime.combine(draft.start_date, draft.start_time)
    end_dt = dt.datetime.combine(draft.end_date_inclusive, draft.end_time)
    zone = time_zone or "Europe/Warsaw"
    return (
        {"dateTime": start_dt.isoformat(), "timeZone": zone},
        {"dateTime": end_dt.isoformat(), "timeZone": zone},
    )


def build_event_body(draft: EventDraft, time_zone: str) -> dict:
    draft.validate()
    body: dict = {"summary": draft.title.strip()}
    if draft.location.strip():
        body["location"] = draft.location.strip()
    if draft.description.strip():
        body["description"] = draft.description.strip()
    body["start"], body["end"] = _build_event_time(draft, time_zone)
    return body


def build_event_patch_body(draft: EventDraft, time_zone: str) -> dict:
    """Build a partial update that can also clear location and description."""
    draft.validate()
    start, end = _build_event_time(draft, time_zone)
    return {
        "summary": draft.title.strip(),
        "location": draft.location.strip(),
        "description": draft.description.strip(),
        "start": start,
        "end": end,
    }


def recurrence_until_before(
    target: dt.date | dt.datetime,
) -> str:
    """
    Return an inclusive RFC5545 UNTIL immediately before the target occurrence.
    """
    if isinstance(target, dt.datetime):
        aware = target
        if aware.tzinfo is None:
            aware = aware.replace(tzinfo=dt.datetime.now().astimezone().tzinfo)
        cutoff = (
            aware.astimezone(dt.timezone.utc).replace(microsecond=0)
            - dt.timedelta(seconds=1)
        )
        return cutoff.strftime("%Y%m%dT%H%M%SZ")
    return (target - dt.timedelta(days=1)).strftime("%Y%m%d")


def trim_recurrence_before(
    recurrence: list[str],
    target: dt.date | dt.datetime,
) -> list[str]:
    """Replace COUNT/UNTIL in RRULE with an UNTIL before target."""
    until = recurrence_until_before(target)
    result: list[str] = []
    found_rrule = False

    for line in recurrence:
        text = str(line)
        if not text.upper().startswith("RRULE:"):
            result.append(text)
            continue

        found_rrule = True
        kept: list[str] = []
        for part in text[6:].split(";"):
            clean = part.strip()
            if not clean:
                continue
            key = clean.split("=", 1)[0].upper()
            if key in {"COUNT", "UNTIL"}:
                continue
            kept.append(clean)
        kept.append(f"UNTIL={until}")
        result.append("RRULE:" + ";".join(kept))

    if not found_rrule:
        raise ValueError("Wydarzenie nadrzędne nie zawiera reguły RRULE.")
    return result


def _markers_are_compatible(
    first: dt.date | dt.datetime,
    target: dt.date | dt.datetime,
) -> bool:
    return isinstance(first, dt.datetime) == isinstance(target, dt.datetime)


class CalendarGateway:
    def __init__(self, credentials) -> None:
        from googleapiclient.discovery import build
        self._service = build("calendar", "v3", credentials=credentials, cache_discovery=False)

    def list_calendars(self) -> list[CalendarInfo]:
        result: list[CalendarInfo] = []
        page_token = None
        while True:
            response = self._service.calendarList().list(pageToken=page_token).execute()
            for item in response.get("items", []):
                result.append(
                    CalendarInfo(
                        calendar_id=str(item.get("id") or ""),
                        name=str(item.get("summaryOverride") or item.get("summary") or "Bez nazwy"),
                        primary=bool(item.get("primary", False)),
                        selected=bool(item.get("selected", False)),
                        access_role=str(item.get("accessRole") or "reader"),
                        time_zone=str(item.get("timeZone") or "Europe/Warsaw"),
                    )
                )
            page_token = response.get("nextPageToken")
            if not page_token:
                break
        return sorted(result, key=lambda value: (not value.primary, value.name.casefold()))

    def list_events(
        self,
        calendars: list[CalendarInfo],
        start_date: dt.date,
        end_date: dt.date,
    ) -> list[CalendarEvent]:
        local_tz = dt.datetime.now().astimezone().tzinfo
        time_min = dt.datetime.combine(start_date, dt.time.min, tzinfo=local_tz).isoformat()
        time_max = dt.datetime.combine(end_date, dt.time.min, tzinfo=local_tz).isoformat()
        events: list[CalendarEvent] = []
        for calendar in calendars:
            page_token = None
            while True:
                response = self._service.events().list(
                    calendarId=calendar.calendar_id,
                    timeMin=time_min,
                    timeMax=time_max,
                    singleEvents=True,
                    orderBy="startTime",
                    maxResults=2500,
                    pageToken=page_token,
                ).execute()
                for item in response.get("items", []):
                    if item.get("status") == "cancelled":
                        continue
                    events.append(event_from_google(item, calendar))
                page_token = response.get("nextPageToken")
                if not page_token:
                    break
        return events

    def search_events(
        self,
        calendars: list[CalendarInfo],
        criteria: SearchCriteria,
    ) -> list[CalendarEvent]:
        criteria.validate()
        events = self.list_events(
            calendars,
            criteria.start_date,
            criteria.end_date_exclusive,
        )
        return EventCollection(events).search(criteria.query)

    def update_event(
        self,
        calendar: CalendarInfo,
        existing: CalendarEvent,
        draft: EventDraft,
    ) -> CalendarEvent:
        if not calendar.can_write:
            raise PermissionError(
                f"Kalendarz {calendar.name} nie pozwala temu kontu edytować wydarzeń."
            )
        if not existing.event_id:
            raise ValueError("Wydarzenie nie ma identyfikatora Google.")
        if existing.calendar_id != calendar.calendar_id:
            raise ValueError("Wydarzenie nie należy do wskazanego kalendarza.")
        if draft.calendar_id != calendar.calendar_id:
            raise ValueError("Edycja nie może przenieść wydarzenia do innego kalendarza.")
        if not existing.supports_basic_edit:
            raise ValueError(
                "Ten rodzaj wydarzenia nie jest jeszcze obsługiwany przez edycję GCM."
            )
        body = build_event_patch_body(draft, calendar.time_zone)
        item = self._service.events().patch(
            calendarId=calendar.calendar_id,
            eventId=existing.event_id,
            body=body,
            sendUpdates="all" if existing.has_attendees else "none",
        ).execute()
        return event_from_google(item, calendar)

    def _validate_delete_target(
        self,
        calendar: CalendarInfo,
        existing: CalendarEvent,
    ) -> None:
        if not calendar.can_write:
            raise PermissionError(
                f"Kalendarz {calendar.name} nie pozwala temu kontu usuwać wydarzeń."
            )
        if existing.calendar_id != calendar.calendar_id:
            raise ValueError("Wydarzenie nie należy do wskazanego kalendarza.")
        if not existing.supports_delete:
            raise ValueError(
                "Google oznaczył to wydarzenie jako zablokowane i nie pozwala go usunąć."
            )

    @staticmethod
    def _send_updates(existing: CalendarEvent) -> str:
        return "all" if existing.has_attendees else "none"

    def delete_event(
        self,
        calendar: CalendarInfo,
        existing: CalendarEvent,
    ) -> None:
        self._validate_delete_target(calendar, existing)
        if not existing.event_id:
            raise ValueError("Wydarzenie nie ma identyfikatora Google.")
        self._service.events().delete(
            calendarId=calendar.calendar_id,
            eventId=existing.event_id,
            sendUpdates=self._send_updates(existing),
        ).execute()

    def delete_recurring_series(
        self,
        calendar: CalendarInfo,
        instance: CalendarEvent,
    ) -> None:
        self._validate_delete_target(calendar, instance)
        if not instance.is_recurring_instance:
            raise ValueError("To wydarzenie nie jest wystąpieniem cyklu.")
        self._service.events().delete(
            calendarId=calendar.calendar_id,
            eventId=instance.recurring_event_id,
            sendUpdates=self._send_updates(instance),
        ).execute()

    def delete_recurring_from(
        self,
        calendar: CalendarInfo,
        instance: CalendarEvent,
    ) -> bool:
        """
        Delete target and all later instances by trimming the parent RRULE.

        Returns True if target is the first occurrence and the whole parent
        series was deleted instead.
        """
        self._validate_delete_target(calendar, instance)
        if not instance.is_recurring_instance:
            raise ValueError("To wydarzenie nie jest wystąpieniem cyklu.")

        target = instance.original_start
        if target is None:
            target = instance.start_dt if not instance.all_day else instance.start_date
        if target is None:
            raise ValueError("Brak pierwotnego czasu rozpoczęcia wystąpienia cyklu.")

        parent = self._service.events().get(
            calendarId=calendar.calendar_id,
            eventId=instance.recurring_event_id,
        ).execute()

        first = parse_google_start_marker(parent.get("start"))
        if first is None:
            raise ValueError("Wydarzenie nadrzędne nie ma daty rozpoczęcia.")
        if not _markers_are_compatible(first, target):
            raise ValueError("Typ daty wystąpienia nie odpowiada typowi całego cyklu.")

        if target <= first:
            self._service.events().delete(
                calendarId=calendar.calendar_id,
                eventId=instance.recurring_event_id,
                sendUpdates=self._send_updates(instance),
            ).execute()
            return True

        recurrence = [str(value) for value in (parent.get("recurrence") or [])]
        if not recurrence:
            raise ValueError("Wydarzenie nadrzędne nie zawiera reguły powtarzania.")

        parent["recurrence"] = trim_recurrence_before(recurrence, target)
        self._service.events().update(
            calendarId=calendar.calendar_id,
            eventId=instance.recurring_event_id,
            body=parent,
            sendUpdates=self._send_updates(instance),
        ).execute()
        return False

    def create_event(self, calendar: CalendarInfo, draft: EventDraft) -> CalendarEvent:
        if not calendar.can_write:
            raise PermissionError(
                f"Kalendarz {calendar.name} nie pozwala temu kontu dodawać wydarzeń."
            )
        if draft.calendar_id != calendar.calendar_id:
            raise ValueError("Wybrany kalendarz nie odpowiada danym wydarzenia.")
        body = build_event_body(draft, calendar.time_zone)
        item = self._service.events().insert(
            calendarId=calendar.calendar_id,
            body=body,
            sendUpdates="none",
        ).execute()
        return event_from_google(item, calendar)
