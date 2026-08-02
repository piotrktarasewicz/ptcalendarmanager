from __future__ import annotations

import json
from dataclasses import dataclass, asdict

from .paths import settings_path


@dataclass(slots=True)
class AppSettings:
    selected_calendar_ids: list[str]


DEFAULT_SETTINGS = AppSettings(selected_calendar_ids=[])


def load_settings() -> AppSettings:
    path = settings_path()
    if not path.is_file():
        return AppSettings(selected_calendar_ids=[])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        ids = data.get("selected_calendar_ids", [])
        if not isinstance(ids, list):
            ids = []
        return AppSettings(selected_calendar_ids=[str(value) for value in ids if value])
    except Exception:
        return AppSettings(selected_calendar_ids=[])


def save_settings(settings: AppSettings) -> None:
    path = settings_path()
    temp = path.with_suffix(".tmp")
    temp.write_text(
        json.dumps(asdict(settings), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temp.replace(path)
