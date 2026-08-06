# -*- coding: utf-8 -*-
"""
settings.py

Small, defensive settings layer for the Google Calendar Manager add-on.
Settings are stored in settings.json inside the NVDA user configuration directory.

Functions used by core.py:
- get_selected_calendar_ids()
- set_selected_calendar_ids(ids)
- get_speech_mode()
- set_speech_mode(mode)
- toggle_speech_mode()

Compatibility helpers kept for the rest of the project:
- get_show_shortcuts_on_status()
- set_show_shortcuts_on_status(value)
- get_last_added_event_calendar_id()
- set_last_added_event_calendar_id(calendar_id)
"""

from __future__ import annotations

import os
import json
from typing import Any, Dict, List

try:
    from .paths import SETTINGS_PATH, ensure_user_data_dir
except Exception:
    from paths import SETTINGS_PATH, ensure_user_data_dir  # type: ignore

DEFAULT_SETTINGS: Dict[str, Any] = {
    "selected_calendar_ids": [],
    "speech_mode": "short",
    "show_shortcuts_on_status": True,
    "last_added_event_calendar_id": "",
}


def _normalize_settings(data: Any) -> Dict[str, Any]:
    """
    Merge loaded settings with defaults and enforce expected types.
    """
    result = dict(DEFAULT_SETTINGS)

    if isinstance(data, dict):
        result.update(data)

    selected = result.get("selected_calendar_ids", [])
    if not isinstance(selected, list):
        selected = []
    result["selected_calendar_ids"] = [
        str(item).strip() for item in selected if str(item).strip()
    ]

    speech_mode = str(result.get("speech_mode", "short")).strip().lower()
    if speech_mode not in ("short", "full"):
        speech_mode = "short"
    result["speech_mode"] = speech_mode

    result["show_shortcuts_on_status"] = bool(
        result.get("show_shortcuts_on_status", True)
    )

    result["last_added_event_calendar_id"] = str(
        result.get("last_added_event_calendar_id", "")
    ).strip()

    return result


def load_settings() -> Dict[str, Any]:
    """
    Load settings.json.
    If the file is missing or invalid, return default settings.
    """
    if not os.path.exists(SETTINGS_PATH):
        return dict(DEFAULT_SETTINGS)

    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return _normalize_settings(data)
    except Exception:
        return dict(DEFAULT_SETTINGS)


def save_settings(data: Dict[str, Any]) -> bool:
    """
    Save settings.json.
    Return True on success, False on failure.
    """
    normalized = _normalize_settings(data)

    try:
        ensure_user_data_dir()
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(normalized, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def get_selected_calendar_ids() -> List[str]:
    data = load_settings()
    return list(data.get("selected_calendar_ids", []))


def set_selected_calendar_ids(calendar_ids: List[str]) -> bool:
    data = load_settings()
    if not isinstance(calendar_ids, list):
        calendar_ids = []
    data["selected_calendar_ids"] = [
        str(item).strip() for item in calendar_ids if str(item).strip()
    ]
    return save_settings(data)


def get_speech_mode() -> str:
    data = load_settings()
    mode = str(data.get("speech_mode", "short")).strip().lower()
    if mode not in ("short", "full"):
        return "short"
    return mode


def set_speech_mode(mode: str) -> str:
    data = load_settings()
    mode = str(mode or "").strip().lower()
    if mode not in ("short", "full"):
        mode = "short"
    data["speech_mode"] = mode
    save_settings(data)
    return mode


def toggle_speech_mode() -> str:
    current = get_speech_mode()
    new_mode = "full" if current == "short" else "short"
    set_speech_mode(new_mode)
    return new_mode


def get_show_shortcuts_on_status() -> bool:
    data = load_settings()
    return bool(data.get("show_shortcuts_on_status", True))


def set_show_shortcuts_on_status(value: bool) -> bool:
    data = load_settings()
    data["show_shortcuts_on_status"] = bool(value)
    return save_settings(data)


def get_last_added_event_calendar_id() -> str:
    data = load_settings()
    return str(data.get("last_added_event_calendar_id", "")).strip()


def set_last_added_event_calendar_id(calendar_id: str) -> bool:
    data = load_settings()
    data["last_added_event_calendar_id"] = str(calendar_id or "").strip()
    return save_settings(data)
