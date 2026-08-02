from __future__ import annotations

import calendar
import datetime as dt
from dataclasses import dataclass, replace
from typing import Iterable
from uuid import uuid4


POLISH_MONTHS = (
    "",
    "stycznia",
    "lutego",
    "marca",
    "kwietnia",
    "maja",
    "czerwca",
    "lipca",
    "sierpnia",
    "września",
    "października",
    "listopada",
    "grudnia",
)

POLISH_MONTHS_NOMINATIVE = (
    "",
    "styczeń",
    "luty",
    "marzec",
    "kwiecień",
    "maj",
    "czerwiec",
    "lipiec",
    "sierpień",
    "wrzesień",
    "październik",
    "listopad",
    "grudzień",
)

POLISH_WEEKDAYS = (
    "poniedziałek",
    "wtorek",
    "środa",
    "czwartek",
    "piątek",
    "sobota",
    "niedziela",
)


@dataclass(frozen=True, slots=True)
class CalendarEvent:
    event_id: str
    date: dt.date
    title: str
    calendar_name: str = "Mój kalendarz"
    all_day: bool = False
    start_time: dt.time | None = None
    end_time: dt.time | None = None
    location: str = ""
    description: str = ""

    def display_text(self) -> str:
        if self.all_day:
            timing = "cały dzień"
        elif self.start_time and self.end_time:
            timing = (
                f"{self.start_time.strftime('%H:%M')}–"
                f"{self.end_time.strftime('%H:%M')}"
            )
        elif self.start_time:
            timing = self.start_time.strftime("%H:%M")
        else:
            timing = "bez określonej godziny"
        return f"{timing}, {self.title}, kalendarz {self.calendar_name}"

    def details_text(self) -> str:
        lines = [
            f"Tytuł: {self.title}",
            f"Data: {format_full_date(self.date)}",
            f"Kalendarz: {self.calendar_name}",
        ]
        if self.all_day:
            lines.append("Czas: wydarzenie całodniowe")
        else:
            start = self.start_time.strftime("%H:%M") if self.start_time else "brak"
            end = self.end_time.strftime("%H:%M") if self.end_time else "brak"
            lines.append(f"Czas: {start}–{end}")
        lines.append(f"Lokalizacja: {self.location or 'brak'}")
        lines.append(f"Opis: {self.description or 'brak'}")
        return "\n".join(lines)


def format_full_date(value: dt.date) -> str:
    return (
        f"{POLISH_WEEKDAYS[value.weekday()]}, "
        f"{value.day} {POLISH_MONTHS[value.month]} {value.year}"
    )


def format_month(value: dt.date) -> str:
    return f"{POLISH_MONTHS_NOMINATIVE[value.month]} {value.year}"


def count_text(count: int) -> str:
    if count == 0:
        return "brak wydarzeń"
    if count == 1:
        return "1 wydarzenie"
    if 2 <= count <= 4:
        return f"{count} wydarzenia"
    return f"{count} wydarzeń"


def format_day_item(value: dt.date, event_count: int) -> str:
    return f"{format_full_date(value)}, {count_text(event_count)}"


def parse_polish_date(text: str) -> dt.date:
    cleaned = str(text or "").strip().replace("/", ".").replace("-", ".")
    parts = [part.strip() for part in cleaned.split(".") if part.strip()]
    if len(parts) != 3:
        raise ValueError("Podaj datę w formacie DD.MM.RRRR.")
    try:
        day, month, year = (int(part) for part in parts)
        return dt.date(year, month, day)
    except (TypeError, ValueError) as error:
        raise ValueError("Podana data jest nieprawidłowa.") from error


def parse_time(text: str) -> dt.time:
    cleaned = str(text or "").strip().replace(".", ":")
    parts = [part.strip() for part in cleaned.split(":")]
    if len(parts) != 2:
        raise ValueError("Podaj godzinę w formacie GG:MM.")
    try:
        hour, minute = (int(part) for part in parts)
        return dt.time(hour, minute)
    except (TypeError, ValueError) as error:
        raise ValueError("Podana godzina jest nieprawidłowa.") from error


class EventStore:
    def __init__(self, reference_date: dt.date | None = None) -> None:
        self.reference_date = reference_date or dt.date.today()
        self._events: dict[str, CalendarEvent] = {}
        self._seed_examples()

    def _seed_examples(self) -> None:
        year = self.reference_date.year
        month = self.reference_date.month
        max_day = calendar.monthrange(year, month)[1]

        def safe_day(preferred: int) -> dt.date:
            return dt.date(year, month, min(preferred, max_day))

        examples = [
            CalendarEvent(
                event_id=str(uuid4()),
                date=safe_day(2),
                title="Test wydarzenia całodniowego",
                calendar_name="Familijne",
                all_day=True,
                location="Mielno",
                description="Przykładowe wydarzenie służące do testu listy.",
            ),
            CalendarEvent(
                event_id=str(uuid4()),
                date=safe_day(2),
                title="Spotkanie w sprawie aplikacji",
                calendar_name="Praca",
                start_time=dt.time(10, 0),
                end_time=dt.time(11, 30),
                description="Sprawdzenie, jak czytnik odczytuje wydarzenie godzinowe.",
            ),
            CalendarEvent(
                event_id=str(uuid4()),
                date=safe_day(5),
                title="Wizyta kontrolna",
                calendar_name="Mój kalendarz",
                start_time=dt.time(14, 15),
                end_time=dt.time(15, 0),
                location="Kraków",
            ),
            CalendarEvent(
                event_id=str(uuid4()),
                date=safe_day(12),
                title="Urodziny Adama",
                calendar_name="Familijne",
                all_day=True,
            ),
        ]
        for event in examples:
            self._events[event.event_id] = event

    def month_days(self, year: int, month: int) -> list[dt.date]:
        count = calendar.monthrange(year, month)[1]
        return [dt.date(year, month, day) for day in range(1, count + 1)]

    def events_for_date(self, value: dt.date) -> list[CalendarEvent]:
        events = [event for event in self._events.values() if event.date == value]
        return sorted(
            events,
            key=lambda event: (
                0 if event.all_day else 1,
                event.start_time or dt.time.min,
                event.title.casefold(),
            ),
        )

    def add_event(
        self,
        *,
        date: dt.date,
        title: str,
        calendar_name: str,
        all_day: bool,
        start_time: dt.time | None,
        end_time: dt.time | None,
        location: str,
        description: str,
    ) -> CalendarEvent:
        event = CalendarEvent(
            event_id=str(uuid4()),
            date=date,
            title=title.strip(),
            calendar_name=calendar_name.strip() or "Mój kalendarz",
            all_day=all_day,
            start_time=None if all_day else start_time,
            end_time=None if all_day else end_time,
            location=location.strip(),
            description=description.strip(),
        )
        self._events[event.event_id] = event
        return event

    def update_event(self, event_id: str, **changes: object) -> CalendarEvent:
        existing = self._events[event_id]
        updated = replace(existing, **changes)
        self._events[event_id] = updated
        return updated

    def delete_event(self, event_id: str) -> None:
        del self._events[event_id]

    def get_event(self, event_id: str) -> CalendarEvent | None:
        return self._events.get(event_id)

    def search(self, query: str) -> list[CalendarEvent]:
        needle = query.strip().casefold()
        if not needle:
            return []
        results: Iterable[CalendarEvent] = self._events.values()
        return sorted(
            (
                event
                for event in results
                if needle in event.title.casefold()
                or needle in event.location.casefold()
                or needle in event.description.casefold()
                or needle in event.calendar_name.casefold()
            ),
            key=lambda event: (
                event.date,
                0 if event.all_day else 1,
                event.start_time or dt.time.min,
                event.title.casefold(),
            ),
        )
