from __future__ import annotations

import datetime as dt

from .models import CalendarEvent, CalendarInfo, event_from_google


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
