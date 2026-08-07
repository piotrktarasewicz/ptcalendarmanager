# -*- coding: utf-8 -*-
"""
paths.py

Shared file-system paths for Google Calendar Manager.

The add-on code remains inside the add-on directory, but user data is stored
in the NVDA user configuration directory. This protects login tokens and
settings from being removed during add-on updates or reinstalls.
"""

from __future__ import annotations

import os
import shutil

BASE_DIR = os.path.dirname(__file__)
LIB_DIR = os.path.join(BASE_DIR, "lib")
CLIENT_SECRET_PATH = os.path.join(BASE_DIR, "client_secret.json")


def _get_nvda_config_path() -> str:
    """
    Return the NVDA user configuration path.

    In normal NVDA use this comes from config.getUserDefaultConfigPath().
    The fallback is only for development or static checks outside NVDA.
    """
    try:
        import config  # type: ignore
        path = config.getUserDefaultConfigPath()
        if path:
            return path
    except Exception:
        pass

    appdata = os.environ.get("APPDATA")
    if appdata:
        return os.path.join(appdata, "nvda")

    return os.path.expanduser(os.path.join("~", ".nvda"))


_NVDA_CONFIG_DIR = _get_nvda_config_path()
USER_DATA_DIR = os.path.join(_NVDA_CONFIG_DIR, "googleCalendarManager")
LEGACY_USER_DATA_DIR = os.path.join(_NVDA_CONFIG_DIR, "googleCalendarReader")

TOKEN_PATH = os.path.join(USER_DATA_DIR, "token.json")
SETTINGS_PATH = os.path.join(USER_DATA_DIR, "settings.json")
ERROR_PATH = os.path.join(USER_DATA_DIR, "last_oauth_error.txt")
CREATE_ERROR_REPORT_PATH = os.path.join(USER_DATA_DIR, "last_create_event_error.txt")
UPDATE_ERROR_REPORT_PATH = os.path.join(USER_DATA_DIR, "last_update_event_error.txt")
DELETE_ERROR_REPORT_PATH = os.path.join(USER_DATA_DIR, "last_delete_event_error.txt")

_FILE_MIGRATIONS = (
    ("token.json", TOKEN_PATH),
    ("settings.json", SETTINGS_PATH),
    ("last_oauth_error.txt", ERROR_PATH),
    ("last_create_event_error.txt", CREATE_ERROR_REPORT_PATH),
    ("last_update_event_error.txt", UPDATE_ERROR_REPORT_PATH),
    ("last_delete_event_error.txt", DELETE_ERROR_REPORT_PATH),
)

_LEGACY_USER_FILES = tuple(
    (os.path.join(source_dir, filename), new_path)
    for source_dir in (LEGACY_USER_DATA_DIR, BASE_DIR)
    for filename, new_path in _FILE_MIGRATIONS
)


def ensure_user_data_dir() -> str:
    os.makedirs(USER_DATA_DIR, exist_ok=True)
    return USER_DATA_DIR


def migrate_legacy_user_files() -> None:
    """
    Copy user data from older add-on versions or names to the current NVDA user config folder.

    The old files are intentionally left in place. This makes the migration
    non-destructive and safer during testing.
    """
    try:
        ensure_user_data_dir()
    except Exception:
        return

    for old_path, new_path in _LEGACY_USER_FILES:
        try:
            if os.path.exists(old_path) and not os.path.exists(new_path):
                shutil.copy2(old_path, new_path)
        except Exception:
            pass


migrate_legacy_user_files()
