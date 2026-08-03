from __future__ import annotations

import calendar
import datetime as dt
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from dataclasses import dataclass, field

POLISH_MONTHS = (
    "", "stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca",
    "lipca", "sierpnia", "września", "października", "listopada", "grudnia",
)
POLISH_MONTHS_NOMINATIVE = (
    "", "styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec",
    "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień",
)
POLISH_WEEKDAYS = (
    "poniedziałek", "wtorek", "środa", "czwartek", "piątek", "sobota", "niedziela",
)



RECURRENCE_CHOICES = (
    ("none", "Nie powtarza się"),
    ("daily", "Codziennie"),
    ("weekly", "Co tydzień"),
    ("monthly", "Co miesiąc"),
    ("quarterly", "Co 3 miesiące"),
    ("semiannual", "Co 6 miesięcy"),
    ("yearly", "Co rok"),
)
RECURRENCE_LABELS = dict(RECURRENCE_CHOICES)
RRULE_WEEKDAYS = ("MO", "TU", "WE", "TH", "FR", "SA", "SU")


@dataclass(frozen=True, slots=True)
class RecurrenceSettings:
    mode: str = "none"
    end_date_inclusive: dt.date | None = None
    supported: bool = True
    raw_lines: tuple[str, ...] = ()

    @property
    def is_recurring(self) -> bool:
        return self.mode != "none"

    @property
    def label(self) -> str:
        if not self.supported:
            return "zaawansowany cykl"
        return RECURRENCE_LABELS.get(self.mode, self.mode)

    def validate(self, start_date: dt.date) -> None:
        if self.mode not in RECURRENCE_LABELS:
            raise ValueError("Wybrany rodzaj powtarzania nie jest obsługiwany.")
        if self.mode == "none":
            return
        if self.end_date_inclusive is not None and self.end_date_inclusive < start_date:
            raise ValueError(
                "Data zakończenia cyklu nie może być wcześniejsza od daty rozpoczęcia."
            )

    def display_text(self) -> str:
        if not self.supported:
            return "zaawansowany cykl utworzony poza GCM"
        if not self.is_recurring:
            return "nie powtarza się"
        if self.end_date_inclusive is None:
            return f"{self.label}, bez daty zakończenia"
        return f"{self.label}, do {format_short_date(self.end_date_inclusive)} włącznie"


def recurrence_mode_index(mode: str) -> int:
    for index, (value, _label) in enumerate(RECURRENCE_CHOICES):
        if value == mode:
            return index
    return 0


def recurrence_mode_from_index(index: int) -> str:
    if 0 <= index < len(RECURRENCE_CHOICES):
        return RECURRENCE_CHOICES[index][0]
    return "none"


def _parse_rrule_parts(line: str) -> dict[str, str] | None:
    text = str(line or "").strip()
    if not text.upper().startswith("RRULE:"):
        return None
    result: dict[str, str] = {}
    for part in text[6:].split(";"):
        clean = part.strip()
        if not clean or "=" not in clean:
            return None
        key, value = clean.split("=", 1)
        key = key.strip().upper()
        value = value.strip().upper()
        if not key or not value or key in result:
            return None
        result[key] = value
    return result


def _parse_rrule_end_date(
    value: str,
    *,
    time_zone: str,
    all_day: bool,
) -> dt.date | None:
    text = str(value or "").strip().upper()
    digits = "".join(character for character in text if character.isdigit())
    if len(digits) < 8:
        return None
    try:
        date_value = dt.date(int(digits[:4]), int(digits[4:6]), int(digits[6:8]))
        if all_day or "T" not in text or len(digits) < 14:
            return date_value
        utc_value = dt.datetime(
            date_value.year,
            date_value.month,
            date_value.day,
            int(digits[8:10]),
            int(digits[10:12]),
            int(digits[12:14]),
            tzinfo=dt.timezone.utc,
        )
        try:
            zone = ZoneInfo(time_zone or "Europe/Warsaw")
        except ZoneInfoNotFoundError:
            zone = dt.datetime.now().astimezone().tzinfo or dt.timezone.utc
        return utc_value.astimezone(zone).date()
    except (TypeError, ValueError):
        return None


def recurrence_from_google(
    item: dict,
    start_date: dt.date,
    time_zone: str = "Europe/Warsaw",
    all_day: bool = True,
) -> RecurrenceSettings:
    lines = tuple(str(value) for value in (item.get("recurrence") or []))
    if not lines:
        return RecurrenceSettings()
    if len(lines) != 1:
        return RecurrenceSettings(mode="unsupported", supported=False, raw_lines=lines)

    parts = _parse_rrule_parts(lines[0])
    if not parts or "FREQ" not in parts or "COUNT" in parts:
        return RecurrenceSettings(mode="unsupported", supported=False, raw_lines=lines)

    # WKST does not change the meaning of the simple one-day rules supported by GCM.
    relevant = {key: value for key, value in parts.items() if key != "WKST"}
    allowed_common = {"FREQ", "INTERVAL", "UNTIL"}
    freq = relevant.get("FREQ", "")
    interval = relevant.get("INTERVAL", "1")
    mode = "unsupported"
    supported = True

    if freq == "DAILY":
        supported = set(relevant) <= allowed_common and interval == "1"
        mode = "daily"
    elif freq == "WEEKLY":
        supported = set(relevant) <= allowed_common | {"BYDAY"} and interval == "1"
        byday = relevant.get("BYDAY", RRULE_WEEKDAYS[start_date.weekday()])
        supported = supported and byday == RRULE_WEEKDAYS[start_date.weekday()]
        mode = "weekly"
    elif freq == "MONTHLY":
        supported = set(relevant) <= allowed_common | {"BYMONTHDAY"}
        bymonthday = relevant.get("BYMONTHDAY", str(start_date.day))
        supported = supported and bymonthday == str(start_date.day)
        if interval == "1":
            mode = "monthly"
        elif interval == "3":
            mode = "quarterly"
        elif interval == "6":
            mode = "semiannual"
        else:
            supported = False
    elif freq == "YEARLY":
        supported = set(relevant) <= allowed_common | {"BYMONTH", "BYMONTHDAY"}
        supported = supported and interval == "1"
        supported = supported and relevant.get("BYMONTH", str(start_date.month)) == str(start_date.month)
        supported = supported and relevant.get("BYMONTHDAY", str(start_date.day)) == str(start_date.day)
        mode = "yearly"
    else:
        supported = False

    end_date = None
    if "UNTIL" in relevant:
        end_date = _parse_rrule_end_date(
            relevant["UNTIL"],
            time_zone=time_zone,
            all_day=all_day,
        )
        if end_date is None:
            supported = False

    if not supported:
        return RecurrenceSettings(mode="unsupported", supported=False, raw_lines=lines)
    return RecurrenceSettings(
        mode=mode,
        end_date_inclusive=end_date,
        supported=True,
        raw_lines=lines,
    )

@dataclass(frozen=True, slots=True)
class SearchCriteria:
    query: str
    start_date: dt.date
    end_date_inclusive: dt.date

    def validate(self) -> None:
        if not self.query.strip():
            raise ValueError("Wpisz tekst do wyszukania.")
        if self.end_date_inclusive < self.start_date:
            raise ValueError("Data końcowa wyszukiwania nie może być wcześniejsza niż początkowa.")

    @property
    def end_date_exclusive(self) -> dt.date:
        return self.end_date_inclusive + dt.timedelta(days=1)


@dataclass(frozen=True, slots=True)
class CalendarInfo:
    calendar_id: str
    name: str
    primary: bool = False
    selected: bool = False
    access_role: str = "reader"
    time_zone: str = "Europe/Warsaw"

    @property
    def can_write(self) -> bool:
        return self.access_role in {"writer", "owner"}


@dataclass(frozen=True, slots=True)
class EventDraft:
    calendar_id: str
    title: str
    all_day: bool
    start_date: dt.date
    end_date_inclusive: dt.date
    start_time: dt.time | None = None
    end_time: dt.time | None = None
    location: str = ""
    description: str = ""
    recurrence: RecurrenceSettings = field(default_factory=RecurrenceSettings)

    def validate(self) -> None:
        if not self.calendar_id.strip():
            raise ValueError("Wybierz kalendarz.")
        if not self.title.strip():
            raise ValueError("Wpisz tytuł wydarzenia.")
        if self.end_date_inclusive < self.start_date:
            raise ValueError("Data zakończenia nie może być wcześniejsza od daty rozpoczęcia.")
        self.recurrence.validate(self.start_date)
        if self.all_day:
            return
        if self.start_time is None:
            raise ValueError("Podaj godzinę rozpoczęcia.")
        if self.end_time is None:
            raise ValueError("Podaj godzinę zakończenia.")
        start = dt.datetime.combine(self.start_date, self.start_time)
        end = dt.datetime.combine(self.end_date_inclusive, self.end_time)
        if end <= start:
            raise ValueError("Koniec wydarzenia musi być późniejszy od początku.")


@dataclass(frozen=True, slots=True)
class CalendarEvent:
    event_id: str
    calendar_id: str
    calendar_name: str
    title: str
    all_day: bool
    start_date: dt.date
    end_date_exclusive: dt.date
    start_dt: dt.datetime | None = None
    end_dt: dt.datetime | None = None
    location: str = ""
    description: str = ""
    html_link: str = ""
    recurring_event_id: str = ""
    original_start: dt.date | dt.datetime | None = None
    has_attendees: bool = False
    event_type: str = "default"
    locked: bool = False
    recurrence: RecurrenceSettings = field(default_factory=RecurrenceSettings)

    @property
    def is_recurring_instance(self) -> bool:
        return bool(self.recurring_event_id)

    @property
    def supports_basic_edit(self) -> bool:
        return not self.locked and self.event_type == "default"

    @property
    def supports_delete(self) -> bool:
        """Google can delete all ordinary and special event types unless locked."""
        return not self.locked and bool(self.event_id)

    def to_draft(self) -> EventDraft:
        if self.all_day:
            return EventDraft(
                calendar_id=self.calendar_id,
                title=self.title,
                all_day=True,
                start_date=self.start_date,
                end_date_inclusive=self.end_date_exclusive - dt.timedelta(days=1),
                location=self.location,
                description=self.description,
                recurrence=self.recurrence,
            )
        if self.start_dt is None or self.end_dt is None:
            raise ValueError("Wydarzenie godzinowe nie ma pełnych danych czasu.")
        return EventDraft(
            calendar_id=self.calendar_id,
            title=self.title,
            all_day=False,
            start_date=self.start_dt.date(),
            end_date_inclusive=self.end_dt.date(),
            start_time=self.start_dt.time().replace(tzinfo=None, microsecond=0),
            end_time=self.end_dt.time().replace(tzinfo=None, microsecond=0),
            location=self.location,
            description=self.description,
            recurrence=self.recurrence,
        )

    def occurs_on(self, value: dt.date) -> bool:
        return self.start_date <= value < self.end_date_exclusive

    def display_text(self, selected_day: dt.date) -> str:
        if self.all_day:
            if self.end_date_exclusive > self.start_date + dt.timedelta(days=1):
                end_inclusive = self.end_date_exclusive - dt.timedelta(days=1)
                timing = (
                    f"cały dzień, wydarzenie wielodniowe od "
                    f"{format_short_date(self.start_date)} do {format_short_date(end_inclusive)}"
                )
            else:
                timing = "cały dzień"
        elif self.start_dt and self.end_dt:
            if self.start_dt.date() == selected_day:
                timing = f"{self.start_dt:%H:%M}–{self.end_dt:%H:%M}"
            else:
                timing = f"trwa od {format_short_datetime(self.start_dt)}"
        else:
            timing = "bez określonej godziny"
        return f"{timing}, {self.title}, kalendarz {self.calendar_name}"

    def details_text(self) -> str:
        lines = [
            f"Tytuł: {self.title}",
            f"Kalendarz: {self.calendar_name}",
        ]
        if self.all_day:
            end_inclusive = self.end_date_exclusive - dt.timedelta(days=1)
            if end_inclusive == self.start_date:
                lines.append(f"Data: {format_full_date(self.start_date)}")
                lines.append("Czas: wydarzenie całodniowe")
            else:
                lines.append(
                    f"Zakres: {format_full_date(self.start_date)} — "
                    f"{format_full_date(end_inclusive)}"
                )
                lines.append("Czas: wydarzenie całodniowe, wielodniowe")
        elif self.start_dt and self.end_dt:
            lines.append(f"Początek: {format_full_datetime(self.start_dt)}")
            lines.append(f"Koniec: {format_full_datetime(self.end_dt)}")
        if self.is_recurring_instance:
            lines.append("Powtarzanie: wydarzenie należy do cyklu")
        elif self.recurrence.is_recurring or not self.recurrence.supported:
            lines.append(f"Powtarzanie: {self.recurrence.display_text()}")
        lines.append(f"Lokalizacja: {self.location or 'brak'}")
        lines.append(f"Opis: {self.description or 'brak'}")
        return "\n".join(lines)


class EventCollection:
    def __init__(self, events: list[CalendarEvent] | None = None) -> None:
        self._events = list(events or [])

    def replace(self, events: list[CalendarEvent]) -> None:
        self._events = list(events)

    def all(self) -> list[CalendarEvent]:
        return list(self._events)

    def for_date(self, value: dt.date) -> list[CalendarEvent]:
        return sorted(
            (event for event in self._events if event.occurs_on(value)),
            key=lambda event: (
                0 if event.all_day else 1,
                event.start_dt or dt.datetime.min.replace(tzinfo=dt.timezone.utc),
                event.title.casefold(),
            ),
        )

    def search(self, query: str) -> list[CalendarEvent]:
        needle = query.strip().casefold()
        if not needle:
            return []
        return sorted(
            (
                event for event in self._events
                if needle in event.title.casefold()
                or needle in event.location.casefold()
                or needle in event.description.casefold()
                or needle in event.calendar_name.casefold()
            ),
            key=lambda event: (
                event.start_date,
                0 if event.all_day else 1,
                event.start_dt or dt.datetime.min.replace(tzinfo=dt.timezone.utc),
            ),
        )


def month_days(year: int, month: int) -> list[dt.date]:
    count = calendar.monthrange(year, month)[1]
    return [dt.date(year, month, day) for day in range(1, count + 1)]


def month_range(year: int, month: int) -> tuple[dt.date, dt.date]:
    start = dt.date(year, month, 1)
    if month == 12:
        end = dt.date(year + 1, 1, 1)
    else:
        end = dt.date(year, month + 1, 1)
    return start, end


def parse_google_datetime(value: str) -> dt.datetime:
    parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.datetime.now().astimezone().tzinfo)
    return parsed.astimezone()


def parse_google_start_marker(value: dict | None) -> dt.date | dt.datetime | None:
    marker = value or {}
    if marker.get("date"):
        return dt.date.fromisoformat(str(marker["date"]))
    if marker.get("dateTime"):
        return parse_google_datetime(str(marker["dateTime"]))
    return None


def event_from_google(item: dict, calendar: CalendarInfo) -> CalendarEvent:
    start = item.get("start") or {}
    end = item.get("end") or {}
    if start.get("date"):
        start_date = dt.date.fromisoformat(start["date"])
        end_date = dt.date.fromisoformat(end.get("date") or start["date"])
        if end_date <= start_date:
            end_date = start_date + dt.timedelta(days=1)
        return CalendarEvent(
            event_id=str(item.get("id") or ""),
            calendar_id=calendar.calendar_id,
            calendar_name=calendar.name,
            title=str(item.get("summary") or "Bez tytułu"),
            all_day=True,
            start_date=start_date,
            end_date_exclusive=end_date,
            location=str(item.get("location") or ""),
            description=str(item.get("description") or ""),
            html_link=str(item.get("htmlLink") or ""),
            recurring_event_id=str(item.get("recurringEventId") or ""),
            original_start=parse_google_start_marker(item.get("originalStartTime")),
            has_attendees=any(
                not bool(attendee.get("self", False))
                for attendee in (item.get("attendees") or [])
                if isinstance(attendee, dict)
            ),
            event_type=str(item.get("eventType") or "default"),
            locked=bool(item.get("locked", False)),
            recurrence=recurrence_from_google(
                item,
                start_date,
                str(start.get("timeZone") or calendar.time_zone),
                all_day=True,
            ),
        )

    start_dt = parse_google_datetime(str(start.get("dateTime")))
    end_dt = parse_google_datetime(str(end.get("dateTime") or start.get("dateTime")))
    end_marker = end_dt - dt.timedelta(microseconds=1) if end_dt > start_dt else start_dt
    return CalendarEvent(
        event_id=str(item.get("id") or ""),
        calendar_id=calendar.calendar_id,
        calendar_name=calendar.name,
        title=str(item.get("summary") or "Bez tytułu"),
        all_day=False,
        start_date=start_dt.date(),
        end_date_exclusive=end_marker.date() + dt.timedelta(days=1),
        start_dt=start_dt,
        end_dt=end_dt,
        location=str(item.get("location") or ""),
        description=str(item.get("description") or ""),
        html_link=str(item.get("htmlLink") or ""),
        recurring_event_id=str(item.get("recurringEventId") or ""),
        original_start=parse_google_start_marker(item.get("originalStartTime")),
        has_attendees=any(
            not bool(attendee.get("self", False))
            for attendee in (item.get("attendees") or [])
            if isinstance(attendee, dict)
        ),
        event_type=str(item.get("eventType") or "default"),
        locked=bool(item.get("locked", False)),
        recurrence=recurrence_from_google(
            item,
            start_dt.date(),
            str(start.get("timeZone") or calendar.time_zone),
            all_day=False,
        ),
    )


def format_full_date(value: dt.date) -> str:
    return f"{POLISH_WEEKDAYS[value.weekday()]}, {value.day} {POLISH_MONTHS[value.month]} {value.year}"


def format_short_date(value: dt.date) -> str:
    return value.strftime("%d.%m.%Y")


def format_full_datetime(value: dt.datetime) -> str:
    return f"{format_full_date(value.date())}, {value:%H:%M}"


def format_short_datetime(value: dt.datetime) -> str:
    return f"{value:%d.%m.%Y, %H:%M}"


def format_month(year: int, month: int) -> str:
    return f"{POLISH_MONTHS_NOMINATIVE[month]} {year}"


def count_text(count: int) -> str:
    if count == 0:
        return "brak wydarzeń"
    if count == 1:
        return "1 wydarzenie"
    if 2 <= count <= 4:
        return f"{count} wydarzenia"
    return f"{count} wydarzeń"


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


def parse_polish_time(text: str) -> dt.time:
    cleaned = str(text or "").strip().replace(".", ":")
    parts = [part.strip() for part in cleaned.split(":")]
    if len(parts) != 2:
        raise ValueError("Podaj godzinę w formacie GG:MM.")
    try:
        hour, minute = (int(part) for part in parts)
        return dt.time(hour, minute)
    except (TypeError, ValueError) as error:
        raise ValueError("Podana godzina jest nieprawidłowa.") from error
