import json
import os
import socket
import sys
import urllib.parse
import webbrowser
from datetime import datetime, timedelta, time, date
from http.server import BaseHTTPRequestHandler, HTTPServer

try:
    from .paths import (
        BASE_DIR,
        LIB_DIR,
        CLIENT_SECRET_PATH,
        TOKEN_PATH,
        ERROR_PATH,
        SETTINGS_PATH,
        ensure_user_data_dir,
    )
except Exception:
    BASE_DIR = os.path.dirname(__file__)
    if BASE_DIR not in sys.path:
        sys.path.insert(0, BASE_DIR)
    from paths import (  # type: ignore
        BASE_DIR,
        LIB_DIR,
        CLIENT_SECRET_PATH,
        TOKEN_PATH,
        ERROR_PATH,
        SETTINGS_PATH,
        ensure_user_data_dir,
    )

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

if LIB_DIR not in sys.path:
    sys.path.insert(0, LIB_DIR)

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

try:
    from .i18n import get_runtime_language, t, format_date_for_language
except Exception:
    from i18n import get_runtime_language, t, format_date_for_language

SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar.calendarlist.readonly",
    "https://www.googleapis.com/auth/calendar.settings.readonly",
]
LEGACY_FULL_CALENDAR_SCOPE = "https://www.googleapis.com/auth/calendar"


WEEKDAY_TO_RRULE = {
    0: "MO",
    1: "TU",
    2: "WE",
    3: "TH",
    4: "FR",
    5: "SA",
    6: "SU",
}


def save_error(text: str) -> None:
    try:
        ensure_user_data_dir()
        with open(ERROR_PATH, "w", encoding="utf-8") as f:
            f.write(text or "")
    except Exception:
        pass


def clear_error() -> None:
    save_error("")


def get_saved_error_text() -> str:
    try:
        if not os.path.exists(ERROR_PATH):
            return ""
        with open(ERROR_PATH, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return ""


def _get_token_scopes_from_file():
    try:
        with open(TOKEN_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        raw_scopes = data.get("scopes", data.get("scope", []))
        if isinstance(raw_scopes, str):
            return {item.strip() for item in raw_scopes.split() if item.strip()}
        if isinstance(raw_scopes, list):
            return {str(item).strip() for item in raw_scopes if str(item).strip()}
    except Exception:
        pass

    return set()


def _remove_token(reason: str) -> None:
    try:
        ensure_user_data_dir()
        backup_path = TOKEN_PATH + ".legacy-scope-backup"
        if os.path.exists(backup_path):
            os.remove(backup_path)
        if os.path.exists(TOKEN_PATH):
            os.remove(TOKEN_PATH)
        save_error(reason)
    except Exception as e:
        save_error(f"token scope migration error: {repr(e)}")


def _token_requires_new_consent() -> bool:
    token_scopes = _get_token_scopes_from_file()
    if not token_scopes:
        return False

    required_scopes = set(SCOPES)
    if LEGACY_FULL_CALENDAR_SCOPE in token_scopes:
        return True

    return not required_scopes.issubset(token_scopes)


def load_credentials():
    if not os.path.exists(TOKEN_PATH):
        return None

    if _token_requires_new_consent():
        _remove_token(
            "OAuth scopes changed. The old token was removed. Sign in again to grant the current, narrower Google Calendar permissions."
        )
        return None

    try:
        return Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    except Exception as e:
        save_error(f"load_credentials error: {repr(e)}")
        return None


def save_credentials(creds) -> None:
    ensure_user_data_dir()
    with open(TOKEN_PATH, "w", encoding="utf-8") as f:
        f.write(creds.to_json())


def get_free_port() -> int:
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


def ensure_valid_credentials():
    creds = load_credentials()
    if not creds:
        return None

    if creds.valid:
        return creds

    if creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            save_credentials(creds)
            clear_error()
            return creds
        except Exception as e:
            save_error(f"refresh error: {repr(e)}")
            return None

    return None


def load_settings():
    default_data = {
        "selected_calendar_ids": [],
        "speech_mode": "short",
    }

    if not os.path.exists(SETTINGS_PATH):
        return default_data

    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            return default_data

        if "selected_calendar_ids" not in data or not isinstance(data["selected_calendar_ids"], list):
            data["selected_calendar_ids"] = []

        if data.get("speech_mode") not in ("short", "full"):
            data["speech_mode"] = "short"

        return data
    except Exception:
        return default_data


def load_selected_calendar_ids():
    data = load_settings()
    ids = data.get("selected_calendar_ids", [])
    if isinstance(ids, list):
        return [str(x) for x in ids if x]
    return []


def load_speech_mode():
    data = load_settings()
    mode = data.get("speech_mode", "short")
    if mode not in ("short", "full"):
        return "short"
    return mode


def parse_event_datetimes(item: dict):
    start = item.get("start", {})
    end = item.get("end", {})

    if "date" in start:
        return {
            "all_day": True,
            "start_dt": None,
            "end_dt": None,
        }

    start_dt_raw = start.get("dateTime")
    end_dt_raw = end.get("dateTime")

    start_dt = None
    end_dt = None

    if start_dt_raw:
        try:
            start_dt = datetime.fromisoformat(start_dt_raw.replace("Z", "+00:00")).astimezone()
        except Exception:
            start_dt = None

    if end_dt_raw:
        try:
            end_dt = datetime.fromisoformat(end_dt_raw.replace("Z", "+00:00")).astimezone()
        except Exception:
            end_dt = None

    return {
        "all_day": False,
        "start_dt": start_dt,
        "end_dt": end_dt,
    }


def is_event_finished_today(item: dict, now_local: datetime) -> bool:
    parsed = parse_event_datetimes(item)

    if parsed["all_day"]:
        return False

    end_dt = parsed["end_dt"]
    if end_dt is None:
        return False

    return end_dt <= now_local


def _recurrence_suffix(item: dict, lang="en") -> str:
    mode = str(item.get("_recurrence_mode", "none")).strip().lower()
    if mode == "daily":
        return t("recurring_suffix_daily", lang)
    if mode == "weekly":
        return t("recurring_suffix_weekly", lang)
    if mode == "monthly":
        return t("recurring_suffix_monthly", lang)
    if mode == "yearly":
        return t("recurring_suffix_yearly", lang)
    return ""


def format_event_line(item: dict, lang="en", multi_calendar=False, now_local=None, is_today=False, speech_mode="short") -> str:
    summary = (item.get("summary") or t("no_title", lang)).strip()
    summary += _recurrence_suffix(item, lang)

    parsed = parse_event_datetimes(item)
    all_day = parsed["all_day"]
    start_dt = parsed["start_dt"]
    end_dt = parsed["end_dt"]

    calendar_label = ""
    if multi_calendar:
        calendar_name = item.get("_calendar_summary", "").strip()
        if calendar_name:
            calendar_label = ", " + t("calendar_prefix", lang, name=calendar_name)

    if all_day:
        key = "all_day_full" if speech_mode == "full" else "all_day_short"
        return t(key, lang, summary=summary, calendar_label=calendar_label)

    if is_today and now_local is not None and start_dt is not None and end_dt is not None:
        if start_dt <= now_local < end_dt:
            end_text = end_dt.strftime("%H:%M")
            return t("in_progress", lang, end=end_text, summary=summary, calendar_label=calendar_label)

    start_text = start_dt.strftime("%H:%M") if start_dt else ""
    end_text = end_dt.strftime("%H:%M") if end_dt else ""

    if speech_mode == "full":
        if start_text and end_text:
            return t("time_range", lang, start=start_text, end=end_text, summary=summary, calendar_label=calendar_label)
        if start_text:
            return t("time_start_only", lang, start=start_text, summary=summary, calendar_label=calendar_label)
        return summary + calendar_label

    if start_text:
        return t("time_start_only", lang, start=start_text, summary=summary, calendar_label=calendar_label)

    return summary + calendar_label


def build_service(lang="en"):
    creds = ensure_valid_credentials()
    if not creds:
        return None, {
            "ok": False,
            "error": "not_logged_in",
            "text": t("helper_not_logged_in", lang),
        }

    try:
        service = build(
            "calendar",
            "v3",
            credentials=creds,
            cache_discovery=False,
            static_discovery=False,
        )
        return service, None
    except Exception as e:
        save_error(f"service build error: {repr(e)}")
        return None, {
            "ok": False,
            "error": "service_build_error",
            "text": t("helper_service_error", lang),
        }


def get_calendar_timezone(service) -> str:
    try:
        result = service.settings().get(setting="timezone").execute()
        tz = str(result.get("value", "")).strip()
        if tz:
            return tz
    except Exception as e:
        save_error(f"settings timezone error: {repr(e)}")

    return "Europe/Warsaw"


def _parse_rrule(item):
    recurrence = item.get("recurrence", [])
    if not recurrence:
        return {}

    first_rule = ""
    for entry in recurrence:
        if str(entry).startswith("RRULE:"):
            first_rule = str(entry)[6:]
            break

    if not first_rule:
        return {}

    parts = {}
    for part in first_rule.split(";"):
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        parts[key.strip().upper()] = value.strip()
    return parts


def _parse_until_to_date(until_value):
    value = str(until_value or "").strip()
    if not value:
        return None

    digits = "".join(ch for ch in value if ch.isdigit())
    if len(digits) < 8:
        return None

    try:
        return date(int(digits[0:4]), int(digits[4:6]), int(digits[6:8]))
    except Exception:
        return None


def _extract_recurrence_info(item):
    parts = _parse_rrule(item)
    freq = parts.get("FREQ", "").upper()

    mode = "none"
    if freq == "DAILY":
        mode = "daily"
    elif freq == "WEEKLY":
        mode = "weekly"
    elif freq == "MONTHLY":
        mode = "monthly"
    elif freq == "YEARLY":
        mode = "yearly"

    until_date = _parse_until_to_date(parts.get("UNTIL", ""))

    return {
        "recurrence_mode": mode,
        "recurrence_no_end": until_date is None and mode != "none",
        "recurrence_end_date": until_date.isoformat() if until_date else "",
    }


def _build_rrule(payload):
    mode = str(payload.get("recurrence_mode", "none")).strip().lower()
    if mode == "none":
        return []

    start_date = date.fromisoformat(str(payload.get("date", "")).strip())

    freq_map = {
        "daily": "DAILY",
        "weekly": "WEEKLY",
        "monthly": "MONTHLY",
        "yearly": "YEARLY",
    }
    freq = freq_map.get(mode)
    if not freq:
        return []

    parts = [f"FREQ={freq}"]

    if mode == "weekly":
        parts.append(f"BYDAY={WEEKDAY_TO_RRULE[start_date.weekday()]}")

    recurrence_no_end = bool(payload.get("recurrence_no_end", False))
    recurrence_end_date_raw = str(payload.get("recurrence_end_date", "")).strip()

    if not recurrence_no_end and recurrence_end_date_raw:
        until_date = date.fromisoformat(recurrence_end_date_raw)
        parts.append(f"UNTIL={until_date.strftime('%Y%m%d')}T235959Z")

    return ["RRULE:" + ";".join(parts)]


def _get_selected_or_primary_calendar_ids():
    selected_ids = load_selected_calendar_ids()
    if not selected_ids:
        return ["primary"]
    return selected_ids


def _map_calendar_names(service, lang):
    try:
        calendar_result = service.calendarList().list().execute()
        calendar_items = calendar_result.get("items", [])
        return {
            item.get("id", ""): item.get("summary", t("no_name", lang))
            for item in calendar_items
        }
    except Exception:
        return {}


def _build_edit_item(item, calendar_id, calendar_name, recurrence_info_override=None):
    parsed = parse_event_datetimes(item)
    recurrence_info = recurrence_info_override or _extract_recurrence_info(item)

    event_id = str(item.get("id", "")).strip()
    recurring_event_id = str(item.get("recurringEventId", "")).strip()

    result = {
        "event_id": event_id,
        "instance_event_id": event_id,
        "series_event_id": recurring_event_id,
        "recurring_event_id": recurring_event_id,
        "is_recurring_instance": bool(recurring_event_id),
        "calendar_id": str(calendar_id or "").strip(),
        "calendar_name": str(calendar_name or "").strip(),
        "summary": str(item.get("summary", "")).strip(),
        "location": str(item.get("location", "")).strip(),
        "all_day": bool(parsed["all_day"]),
        "date": "",
        "end_date": "",
        "start_datetime": "",
        "end_datetime": "",
        "recurrence_mode": recurrence_info["recurrence_mode"],
        "recurrence_no_end": recurrence_info["recurrence_no_end"],
        "recurrence_end_date": recurrence_info["recurrence_end_date"],
        "recurrence_scope": "",
    }

    if parsed["all_day"]:
        start_date_raw = str(item.get("start", {}).get("date", "")).strip()
        end_date_raw = str(item.get("end", {}).get("date", "")).strip()
        result["date"] = start_date_raw

        if end_date_raw:
            try:
                end_inclusive = date.fromisoformat(end_date_raw) - timedelta(days=1)
                result["end_date"] = end_inclusive.isoformat()
            except Exception:
                result["end_date"] = start_date_raw
        else:
            result["end_date"] = start_date_raw
    else:
        start_dt = parsed["start_dt"]
        end_dt = parsed["end_dt"]
        if start_dt is not None:
            result["date"] = start_dt.date().isoformat()
            result["start_datetime"] = start_dt.replace(tzinfo=None).isoformat()
        if end_dt is not None:
            result["end_datetime"] = end_dt.replace(tzinfo=None).isoformat()

    return result


def api_list_calendars(lang="en"):
    service, error = build_service(lang)
    if error:
        return error

    try:
        result = service.calendarList().list().execute()
    except Exception as e:
        save_error(f"calendarList error: {repr(e)}")
        return {
            "ok": False,
            "error": "calendar_list_error",
            "text": t("helper_calendar_list_error", lang),
        }

    items = result.get("items", [])
    calendars = []

    for item in items:
        calendars.append({
            "id": item.get("id", ""),
            "summary": item.get("summary", t("no_name", lang)),
            "primary": bool(item.get("primary", False)),
        })

    return {
        "ok": True,
        "calendars": calendars,
        "text": t("helper_fetched_calendars", lang, count=len(calendars)),
    }


def api_events(days_ahead: int, lang="en"):
    service, error = build_service(lang)
    if error:
        return error

    selected_ids = _get_selected_or_primary_calendar_ids()
    calendar_name_map = _map_calendar_names(service, lang)
    speech_mode = load_speech_mode()

    now_local = datetime.now().astimezone()
    target_date = now_local.date() + timedelta(days=days_ahead)
    is_today = days_ahead == 0

    start_dt = datetime.combine(target_date, time.min).astimezone()
    end_dt = datetime.combine(target_date, time.max).astimezone()

    all_items = []

    for calendar_id in selected_ids:
        try:
            result = service.events().list(
                calendarId=calendar_id,
                timeMin=start_dt.isoformat(),
                timeMax=end_dt.isoformat(),
                singleEvents=True,
                orderBy="startTime"
            ).execute()
        except Exception as e:
            save_error(f"events list error for {calendar_id}: {repr(e)}")
            continue

        items = result.get("items", [])
        for item in items:
            if item.get("recurringEventId"):
                try:
                    master = service.events().get(
                        calendarId=calendar_id,
                        eventId=item.get("recurringEventId", "")
                    ).execute()
                    recurrence_info = _extract_recurrence_info(master)
                except Exception:
                    recurrence_info = {"recurrence_mode": "none"}
            else:
                recurrence_info = _extract_recurrence_info(item)

            item["_calendar_id"] = calendar_id
            item["_calendar_summary"] = calendar_name_map.get(calendar_id, calendar_id)
            item["_recurrence_mode"] = recurrence_info.get("recurrence_mode", "none")
            all_items.append(item)

    def sort_key(item):
        start = item.get("start", {})
        if "dateTime" in start:
            return start.get("dateTime", "")
        if "date" in start:
            return start.get("date", "")
        return ""

    all_items.sort(key=sort_key)

    if is_today:
        filtered_items = []
        for item in all_items:
            if not is_event_finished_today(item, now_local):
                filtered_items.append(item)
        all_items = filtered_items

    date_text = format_date_for_language(target_date, lang)

    if not all_items:
        return {
            "ok": True,
            "count": 0,
            "text": t("date_no_events", lang, date=date_text),
        }

    multi_calendar = len(selected_ids) > 1
    lines = [
        format_event_line(
            item,
            lang=lang,
            multi_calendar=multi_calendar,
            now_local=now_local,
            is_today=is_today,
            speech_mode=speech_mode
        )
        for item in all_items
    ]
    count = len(lines)

    if count == 1:
        prefix = t("one_event_prefix", lang, date=date_text)
    elif 2 <= count <= 4:
        prefix = t("few_events_prefix", lang, date=date_text, count=count)
    else:
        prefix = t("many_events_prefix", lang, date=date_text, count=count)

    events_text = ". ".join(line.rstrip(" .") for line in lines if line.strip())
    if events_text and not events_text.endswith("."):
        events_text += "."

    text = prefix
    if events_text:
        text += " " + events_text

    return {
        "ok": True,
        "count": count,
        "text": text,
    }


def api_list_events_for_edit(target_date_iso: str, lang="en"):
    service, error = build_service(lang)
    if error:
        return error

    try:
        target_date = date.fromisoformat(str(target_date_iso).strip())
    except Exception as e:
        save_error(f"list_events_for_edit invalid date: {repr(e)}")
        return {
            "ok": False,
            "error": "invalid_target_date",
            "text": t("helper_event_list_for_edit_error", lang),
        }

    selected_ids = _get_selected_or_primary_calendar_ids()
    calendar_name_map = _map_calendar_names(service, lang)

    start_dt = datetime.combine(target_date, time.min).astimezone()
    end_dt = datetime.combine(target_date, time.max).astimezone()

    items_for_edit = []
    seen_ids = set()

    for calendar_id in selected_ids:
        try:
            result = service.events().list(
                calendarId=calendar_id,
                timeMin=start_dt.isoformat(),
                timeMax=end_dt.isoformat(),
                singleEvents=True,
                orderBy="startTime"
            ).execute()
        except Exception as e:
            save_error(f"list_events_for_edit error for {calendar_id}: {repr(e)}")
            continue

        items = result.get("items", [])
        for item in items:
            event_id = str(item.get("id", "")).strip()
            if not event_id:
                continue

            seen_key = f"{calendar_id}:{event_id}"
            if seen_key in seen_ids:
                continue

            recurring_master_id = str(item.get("recurringEventId", "")).strip()
            recurrence_info = None
            master_item = None

            if recurring_master_id:
                try:
                    master_item = service.events().get(
                        calendarId=calendar_id,
                        eventId=recurring_master_id
                    ).execute()
                    recurrence_info = _extract_recurrence_info(master_item)
                except Exception:
                    master_item = None
                    recurrence_info = {
                        "recurrence_mode": "none",
                        "recurrence_no_end": False,
                        "recurrence_end_date": "",
                    }

            built = _build_edit_item(
                item,
                calendar_id=calendar_id,
                calendar_name=calendar_name_map.get(calendar_id, calendar_id),
                recurrence_info_override=recurrence_info,
            )

            if recurring_master_id and master_item:
                series_event = _build_edit_item(
                    master_item,
                    calendar_id=calendar_id,
                    calendar_name=calendar_name_map.get(calendar_id, calendar_id),
                )
                series_event["event_id"] = recurring_master_id
                series_event["series_event_id"] = recurring_master_id
                series_event["recurrence_scope"] = "series"
                built["series_event"] = series_event

            if built.get("event_id"):
                seen_ids.add(seen_key)
                items_for_edit.append(built)

    def sort_key(item):
        if item.get("all_day"):
            return "0000"
        start_iso = str(item.get("start_datetime", "")).strip()
        if start_iso:
            try:
                return datetime.fromisoformat(start_iso).strftime("%H%M")
            except Exception:
                return "9999"
        return "9999"

    items_for_edit.sort(key=sort_key)

    return {
        "ok": True,
        "items": items_for_edit,
        "count": len(items_for_edit),
        "text": t("helper_fetched_events", lang, count=len(items_for_edit)),
    }



def api_search_events(query: str, start_date_iso: str, end_date_iso: str, lang="en"):
    service, error = build_service(lang)
    if error:
        return error

    query = str(query or "").strip()
    if not query:
        return {
            "ok": False,
            "error": "empty_search_query",
            "text": t("search_events_error_query_required", lang),
        }

    try:
        start_date = date.fromisoformat(str(start_date_iso).strip())
        end_date = date.fromisoformat(str(end_date_iso).strip())
    except Exception as e:
        save_error(f"search_events invalid date range: {repr(e)}")
        return {
            "ok": False,
            "error": "invalid_search_date_range",
            "text": t("helper_search_events_error", lang),
        }

    if end_date < start_date:
        return {
            "ok": False,
            "error": "invalid_search_date_range",
            "text": t("search_events_error_end_before_start", lang),
        }

    selected_ids = _get_selected_or_primary_calendar_ids()
    calendar_name_map = _map_calendar_names(service, lang)

    start_dt = datetime.combine(start_date, time.min).astimezone()
    end_dt = datetime.combine(end_date + timedelta(days=1), time.min).astimezone()

    items_for_edit = []
    seen_ids = set()

    for calendar_id in selected_ids:
        page_token = None
        while True:
            try:
                list_kwargs = {
                    "calendarId": calendar_id,
                    "timeMin": start_dt.isoformat(),
                    "timeMax": end_dt.isoformat(),
                    "singleEvents": True,
                    "orderBy": "startTime",
                    "q": query,
                    "maxResults": 100,
                }
                if page_token:
                    list_kwargs["pageToken"] = page_token
                result = service.events().list(**list_kwargs).execute()
            except Exception as e:
                save_error(f"search_events error for {calendar_id}: {repr(e)}")
                break

            items = result.get("items", [])
            for item in items:
                event_id = str(item.get("id", "")).strip()
                if not event_id:
                    continue

                seen_key = f"{calendar_id}:{event_id}"
                if seen_key in seen_ids:
                    continue

                recurring_master_id = str(item.get("recurringEventId", "")).strip()
                recurrence_info = None
                master_item = None

                if recurring_master_id:
                    try:
                        master_item = service.events().get(
                            calendarId=calendar_id,
                            eventId=recurring_master_id
                        ).execute()
                        recurrence_info = _extract_recurrence_info(master_item)
                    except Exception:
                        master_item = None
                        recurrence_info = {
                            "recurrence_mode": "none",
                            "recurrence_no_end": False,
                            "recurrence_end_date": "",
                        }

                built = _build_edit_item(
                    item,
                    calendar_id=calendar_id,
                    calendar_name=calendar_name_map.get(calendar_id, calendar_id),
                    recurrence_info_override=recurrence_info,
                )

                if recurring_master_id and master_item:
                    series_event = _build_edit_item(
                        master_item,
                        calendar_id=calendar_id,
                        calendar_name=calendar_name_map.get(calendar_id, calendar_id),
                    )
                    series_event["event_id"] = recurring_master_id
                    series_event["series_event_id"] = recurring_master_id
                    series_event["recurrence_scope"] = "series"
                    built["series_event"] = series_event

                if built.get("event_id"):
                    seen_ids.add(seen_key)
                    items_for_edit.append(built)

            page_token = result.get("nextPageToken")
            if not page_token:
                break
            if len(items_for_edit) >= 500:
                break

    def sort_key(item):
        date_raw = str(item.get("date", "")).strip()
        start_iso = str(item.get("start_datetime", "")).strip()
        if start_iso:
            try:
                return datetime.fromisoformat(start_iso).isoformat()
            except Exception:
                pass
        if date_raw:
            return date_raw + "T00:00:00"
        return "9999-12-31T23:59:59"

    items_for_edit.sort(key=sort_key)

    return {
        "ok": True,
        "items": items_for_edit,
        "count": len(items_for_edit),
        "text": t("helper_fetched_events", lang, count=len(items_for_edit)),
    }

def api_create_event(payload, lang="en"):
    service, error = build_service(lang)
    if error:
        return error

    try:
        calendar_id = str(payload.get("calendar_id", "")).strip()
        summary = str(payload.get("summary", "")).strip()
        location = str(payload.get("location", "")).strip()
        all_day = bool(payload.get("all_day", False))

        if not calendar_id or not summary:
            raise ValueError("missing required fields")

        event_body = {
            "summary": summary,
        }

        if location:
            event_body["location"] = location

        recurrence = _build_rrule(payload)
        event_timezone = get_calendar_timezone(service)

        if all_day:
            start_date = date.fromisoformat(str(payload.get("date", "")).strip())
            end_date_raw = str(payload.get("end_date", "")).strip()
            end_date = date.fromisoformat(end_date_raw) if end_date_raw else start_date
            end_exclusive = end_date + timedelta(days=1)

            if end_date < start_date:
                raise ValueError("end date earlier than start date")

            event_body["start"] = {"date": start_date.isoformat()}
            event_body["end"] = {"date": end_exclusive.isoformat()}
        else:
            start_iso = str(payload.get("start_datetime", "")).strip()
            end_iso = str(payload.get("end_datetime", "")).strip()

            if not start_iso or not end_iso:
                raise ValueError("missing datetime fields")

            start_dt = datetime.fromisoformat(start_iso)
            end_dt = datetime.fromisoformat(end_iso)

            if start_dt.tzinfo is None:
                start_dt = start_dt.astimezone()

            if end_dt.tzinfo is None:
                end_dt = end_dt.astimezone()

            event_body["start"] = {
                "dateTime": start_dt.isoformat(),
                "timeZone": event_timezone,
            }
            event_body["end"] = {
                "dateTime": end_dt.isoformat(),
                "timeZone": event_timezone,
            }

        if recurrence:
            event_body["recurrence"] = recurrence

        created = service.events().insert(
            calendarId=calendar_id,
            body=event_body
        ).execute()

        return {
            "ok": True,
            "event_id": created.get("id", ""),
            "text": "success",
        }

    except Exception as e:
        details = [
            "create_event error",
            f"exception: {repr(e)}",
            "payload:",
            json.dumps(payload, ensure_ascii=False, indent=2),
        ]
        save_error("\n".join(details))
        return {
            "ok": False,
            "error": "create_event_error",
            "text": t("add_event_error_failed", lang),
        }


def api_update_event(payload, lang="en"):
    service, error = build_service(lang)
    if error:
        return error

    try:
        calendar_id = str(payload.get("calendar_id", "")).strip()
        event_id = str(payload.get("event_id", "")).strip()
        summary = str(payload.get("summary", "")).strip()
        location = str(payload.get("location", "")).strip()
        all_day = bool(payload.get("all_day", False))
        recurrence_scope = str(payload.get("recurrence_scope", "")).strip().lower()

        if not calendar_id or not event_id or not summary:
            raise ValueError("missing required fields")

        # Google recommends reading the current event and then updating the
        # complete resource. This also lets us replace the entire start/end
        # objects when converting between timed and all-day events, so stale
        # dateTime/date fields cannot remain in the resource.
        event_body = service.events().get(
            calendarId=calendar_id,
            eventId=event_id,
        ).execute()
        if not isinstance(event_body, dict):
            raise ValueError("invalid event resource")

        event_body["summary"] = summary

        if "location" in payload:
            event_body["location"] = location

        recurrence = _build_rrule(payload)
        event_timezone = get_calendar_timezone(service)

        if all_day:
            start_date = date.fromisoformat(str(payload.get("date", "")).strip())
            end_date_raw = str(payload.get("end_date", "")).strip()
            end_date = date.fromisoformat(end_date_raw) if end_date_raw else start_date
            end_exclusive = end_date + timedelta(days=1)

            if end_date < start_date:
                raise ValueError("end date earlier than start date")

            event_body["start"] = {"date": start_date.isoformat()}
            event_body["end"] = {"date": end_exclusive.isoformat()}
        else:
            start_iso = str(payload.get("start_datetime", "")).strip()
            end_iso = str(payload.get("end_datetime", "")).strip()

            if not start_iso or not end_iso:
                raise ValueError("missing datetime fields")

            start_dt = datetime.fromisoformat(start_iso)
            end_dt = datetime.fromisoformat(end_iso)

            if end_dt <= start_dt:
                raise ValueError("end must be later than start")

            if start_dt.tzinfo is None:
                start_dt = start_dt.astimezone()

            if end_dt.tzinfo is None:
                end_dt = end_dt.astimezone()

            event_body["start"] = {
                "dateTime": start_dt.isoformat(),
                "timeZone": event_timezone,
            }
            event_body["end"] = {
                "dateTime": end_dt.isoformat(),
                "timeZone": event_timezone,
            }

        if recurrence_scope != "instance" and "recurrence_mode" in payload:
            if recurrence:
                event_body["recurrence"] = recurrence
            else:
                event_body.pop("recurrence", None)

        update_kwargs = {
            "calendarId": calendar_id,
            "eventId": event_id,
            "body": event_body,
        }
        if event_body.get("attachments"):
            update_kwargs["supportsAttachments"] = True
        if event_body.get("conferenceData"):
            update_kwargs["conferenceDataVersion"] = 1

        updated = service.events().update(**update_kwargs).execute()

        return {
            "ok": True,
            "event_id": updated.get("id", ""),
            "text": "success",
        }

    except Exception as e:
        details = [
            "update_event error",
            f"exception: {repr(e)}",
            "payload:",
            json.dumps(payload, ensure_ascii=False, indent=2),
        ]
        save_error("\n".join(details))
        return {
            "ok": False,
            "error": "update_event_error",
            "text": t("edit_event_error_failed", lang),
        }


def api_delete_event(payload, lang="en"):
    service, error = build_service(lang)
    if error:
        return error

    try:
        calendar_id = str(payload.get("calendar_id", "")).strip()
        event_id = str(payload.get("event_id", "")).strip()

        if not calendar_id or not event_id:
            raise ValueError("missing required fields")

        service.events().delete(
            calendarId=calendar_id,
            eventId=event_id
        ).execute()

        return {
            "ok": True,
            "event_id": event_id,
            "text": "success",
        }

    except Exception as e:
        details = [
            "delete_event error",
            f"exception: {repr(e)}",
            "payload:",
            json.dumps(payload, ensure_ascii=False, indent=2),
        ]
        save_error("\n".join(details))
        return {
            "ok": False,
            "error": "delete_event_error",
            "text": t("delete_event_error_failed", lang),
        }


def cmd_status() -> int:
    creds = ensure_valid_credentials()
    if creds:
        print("logged_in", flush=True)
        return 0

    print("not_logged_in", flush=True)
    return 0


def cmd_logout() -> int:
    try:
        if os.path.exists(TOKEN_PATH):
            os.remove(TOKEN_PATH)
        clear_error()
        print("logged_out", flush=True)
        return 0
    except Exception as e:
        save_error(f"logout error: {repr(e)}")
        print("logout_error", flush=True)
        return 1


def open_browser(url: str) -> bool:
    try:
        os.startfile(url)
        return True
    except Exception as e:
        save_error(f"os.startfile error: {repr(e)}")

    try:
        opened = webbrowser.open(url)
        if opened:
            return True
        save_error("webbrowser.open returned False")
    except Exception as e:
        save_error(f"webbrowser.open error: {repr(e)}")

    return False


def cmd_login() -> int:
    if not os.path.exists(CLIENT_SECRET_PATH):
        save_error("missing client_secret.json")
        return 1

    try:
        with open(CLIENT_SECRET_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict) or "installed" not in data:
            save_error("client_secret.json is not a desktop OAuth client")
            return 1
    except Exception as e:
        save_error(f"invalid client_secret.json: {repr(e)}")
        return 1

    try:
        port = get_free_port()
        redirect_uri = f"http://127.0.0.1:{port}/"

        flow = Flow.from_client_secrets_file(
            CLIENT_SECRET_PATH,
            scopes=SCOPES,
            redirect_uri=redirect_uri,
        )

        authorization_url, expected_state = flow.authorization_url(
            access_type="offline",
            prompt="consent",
        )
    except Exception as e:
        save_error(f"flow preparation error: {repr(e)}")
        return 1

    auth_result = {
        "code": None,
        "state": None,
        "error": None,
    }

    class OAuthCallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            try:
                parsed = urllib.parse.urlparse(self.path)
                params = urllib.parse.parse_qs(parsed.query)

                auth_result["code"] = params.get("code", [None])[0]
                auth_result["state"] = params.get("state", [None])[0]
                auth_result["error"] = params.get("error", [None])[0]

                if auth_result["error"]:
                    body = (
                        "<html><body><h1>Authorization failed</h1>"
                        "<p>You may close this window.</p></body></html>"
                    )
                else:
                    body = (
                        "<html><body><h1>Authentication completed</h1>"
                        "<p>You may close this window.</p></body></html>"
                    )

                encoded = body.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)
            except Exception as e:
                save_error(f"callback handler error: {repr(e)}")
                try:
                    self.send_response(500)
                    self.end_headers()
                except Exception:
                    pass

        def log_message(self, format, *args):
            return

    try:
        server = HTTPServer(("127.0.0.1", port), OAuthCallbackHandler)
        server.timeout = 300
    except Exception as e:
        save_error(f"local server start error: {repr(e)}")
        return 1

    try:
        if not open_browser(authorization_url):
            try:
                server.server_close()
            except Exception:
                pass
            return 1
    except Exception as e:
        try:
            server.server_close()
        except Exception:
            pass
        save_error(f"browser open error: {repr(e)}")
        return 1

    try:
        while auth_result["code"] is None and auth_result["error"] is None:
            server.handle_request()
    except Exception as e:
        save_error(f"server wait error: {repr(e)}")
        try:
            server.server_close()
        except Exception:
            pass
        return 1
    finally:
        try:
            server.server_close()
        except Exception:
            pass

    if auth_result["error"]:
        save_error(f"authorization error: {auth_result['error']}")
        return 1

    if not auth_result["code"]:
        save_error("authorization code was not received")
        return 1

    if auth_result["state"] != expected_state:
        save_error("state mismatch")
        return 1

    try:
        flow.fetch_token(code=auth_result["code"])
        creds = flow.credentials
        save_credentials(creds)
        clear_error()
        return 0
    except Exception as e:
        save_error(f"token fetch error: {repr(e)}")
        return 1


def cmd_list_calendars(lang="en") -> int:
    result = api_list_calendars(lang)
    print(json.dumps(result, ensure_ascii=False), flush=True)
    return 0 if result.get("ok") else 1


def cmd_events(days_ahead: int, lang="en") -> int:
    result = api_events(days_ahead, lang)
    print(json.dumps(result, ensure_ascii=False), flush=True)
    return 0 if result.get("ok") else 1


def cmd_list_events_for_edit(target_date_iso: str, lang="en") -> int:
    result = api_list_events_for_edit(target_date_iso, lang)
    print(json.dumps(result, ensure_ascii=False), flush=True)
    return 0 if result.get("ok") else 1


def cmd_create_event(raw_json: str, lang="en") -> int:
    try:
        payload = json.loads(raw_json)
    except Exception as e:
        save_error(f"create_event payload parse error: {repr(e)}")
        result = {
            "ok": False,
            "error": "invalid_payload",
            "text": t("add_event_error_failed", lang),
        }
        print(json.dumps(result, ensure_ascii=False), flush=True)
        return 1

    result = api_create_event(payload, lang)
    print(json.dumps(result, ensure_ascii=False), flush=True)
    return 0 if result.get("ok") else 1


def cmd_update_event(raw_json: str, lang="en") -> int:
    try:
        payload = json.loads(raw_json)
    except Exception as e:
        save_error(f"update_event payload parse error: {repr(e)}")
        result = {
            "ok": False,
            "error": "invalid_payload",
            "text": t("edit_event_error_failed", lang),
        }
        print(json.dumps(result, ensure_ascii=False), flush=True)
        return 1

    result = api_update_event(payload, lang)
    print(json.dumps(result, ensure_ascii=False), flush=True)
    return 0 if result.get("ok") else 1


def cmd_delete_event(raw_json: str, lang="en") -> int:
    try:
        payload = json.loads(raw_json)
    except Exception as e:
        save_error(f"delete_event payload parse error: {repr(e)}")
        result = {
            "ok": False,
            "error": "invalid_payload",
            "text": t("delete_event_error_failed", lang),
        }
        print(json.dumps(result, ensure_ascii=False), flush=True)
        return 1

    result = api_delete_event(payload, lang)
    print(json.dumps(result, ensure_ascii=False), flush=True)
    return 0 if result.get("ok") else 1


def main() -> int:
    lang = get_runtime_language("en")

    if len(sys.argv) < 2:
        print("missing_command", flush=True)
        return 1

    command = sys.argv[1].strip().lower()

    if command == "status":
        return cmd_status()

    if command == "login":
        return cmd_login()

    if command == "logout":
        return cmd_logout()

    if command == "list_calendars":
        return cmd_list_calendars(lang)

    if command == "events":
        if len(sys.argv) < 3:
            print(json.dumps({
                "ok": False,
                "error": "missing_days_ahead",
                "text": t("helper_missing_days_ahead", lang),
            }, ensure_ascii=False), flush=True)
            return 1
        try:
            days_ahead = int(sys.argv[2])
        except ValueError:
            print(json.dumps({
                "ok": False,
                "error": "invalid_days_ahead",
                "text": t("helper_invalid_days_ahead", lang),
            }, ensure_ascii=False), flush=True)
            return 1
        return cmd_events(days_ahead, lang)

    if command == "list_events_for_edit":
        if len(sys.argv) < 3:
            print(json.dumps({
                "ok": False,
                "error": "missing_target_date",
                "text": t("helper_event_list_for_edit_error", lang),
            }, ensure_ascii=False), flush=True)
            return 1
        return cmd_list_events_for_edit(sys.argv[2], lang)

    if command == "create_event":
        if len(sys.argv) < 3:
            print(json.dumps({
                "ok": False,
                "error": "missing_payload",
                "text": t("add_event_error_failed", lang),
            }, ensure_ascii=False), flush=True)
            return 1
        return cmd_create_event(sys.argv[2], lang)

    if command == "update_event":
        if len(sys.argv) < 3:
            print(json.dumps({
                "ok": False,
                "error": "missing_payload",
                "text": t("edit_event_error_failed", lang),
            }, ensure_ascii=False), flush=True)
            return 1
        return cmd_update_event(sys.argv[2], lang)

    if command == "delete_event":
        if len(sys.argv) < 3:
            print(json.dumps({
                "ok": False,
                "error": "missing_payload",
                "text": t("delete_event_error_failed", lang),
            }, ensure_ascii=False), flush=True)
            return 1
        return cmd_delete_event(sys.argv[2], lang)

    print("unknown_command", flush=True)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())