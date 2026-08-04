from __future__ import annotations

import json
from dataclasses import asdict, dataclass

from .i18n import LANGUAGE_AUTO, normalize_language_preference
from .paths import settings_path


@dataclass(slots=True)
class AppSettings:
    selected_calendar_ids: list[str]
    language: str = LANGUAGE_AUTO


DEFAULT_SETTINGS = AppSettings(selected_calendar_ids=[], language=LANGUAGE_AUTO)


def load_settings() -> AppSettings:
    path = settings_path()
    if not path.is_file():
        return AppSettings(selected_calendar_ids=[], language=LANGUAGE_AUTO)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        ids = data.get("selected_calendar_ids", [])
        if not isinstance(ids, list):
            ids = []
        language = normalize_language_preference(data.get("language", LANGUAGE_AUTO))
        return AppSettings(
            selected_calendar_ids=[str(value) for value in ids if value],
            language=language,
        )
    except Exception:
        return AppSettings(selected_calendar_ids=[], language=LANGUAGE_AUTO)


def save_settings(settings: AppSettings) -> None:
    path = settings_path()
    temp = path.with_suffix(".tmp")
    normalized = AppSettings(
        selected_calendar_ids=[
            str(value) for value in settings.selected_calendar_ids if str(value).strip()
        ],
        language=normalize_language_preference(settings.language),
    )
    temp.write_text(
        json.dumps(asdict(normalized), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temp.replace(path)
