from __future__ import annotations

import datetime as dt

from .models import CalendarEvent, CalendarInfo, EventDraft, event_from_google


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

    def delete_event(
        self,
        calendar: CalendarInfo,
        existing: CalendarEvent,
    ) -> None:
        if not calendar.can_write:
            raise PermissionError(
                f"Kalendarz {calendar.name} nie pozwala temu kontu usuwać wydarzeń."
            )
        if not existing.event_id:
            raise ValueError("Wydarzenie nie ma identyfikatora Google.")
        if existing.calendar_id != calendar.calendar_id:
            raise ValueError("Wydarzenie nie należy do wskazanego kalendarza.")
        if not existing.supports_delete:
            raise ValueError(
                "Google oznaczył to wydarzenie jako zablokowane i nie pozwala go usunąć."
            )
        self._service.events().delete(
            calendarId=calendar.calendar_id,
            eventId=existing.event_id,
            sendUpdates="all" if existing.has_attendees else "none",
        ).execute()

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
