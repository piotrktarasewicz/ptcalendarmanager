from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

APP_DIR_NAME = "GCM by Piotrek"


def app_data_dir() -> Path:
    base = os.environ.get("APPDATA")
    if base:
        result = Path(base) / APP_DIR_NAME
    else:
        result = Path.home() / ".gcm-by-piotrek"
    result.mkdir(parents=True, exist_ok=True)
    return result


def token_path() -> Path:
    return app_data_dir() / "token.json"


def settings_path() -> Path:
    return app_data_dir() / "settings.json"


def client_secret_path() -> Path:
    return app_data_dir() / "client_secret.json"


def error_path() -> Path:
    return app_data_dir() / "last_error.txt"


def _runtime_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[2]


def nvda_user_data_dir() -> Path | None:
    base = os.environ.get("APPDATA")
    return Path(base) / "nvda" / "googleCalendarManager" if base else None


def nvda_addon_client_secret_candidates() -> list[Path]:
    base = os.environ.get("APPDATA")
    if not base:
        return []
    addons = Path(base) / "nvda" / "addons"
    candidates = [
        addons / "googleCalendarManager" / "globalPlugins" / "googleCalendarManager" / "client_secret.json",
        addons / "googleCalendarReader" / "globalPlugins" / "googleCalendarManager" / "client_secret.json",
    ]
    if addons.is_dir():
        try:
            for child in addons.iterdir():
                candidate = child / "globalPlugins" / "googleCalendarManager" / "client_secret.json"
                if candidate not in candidates:
                    candidates.append(candidate)
        except OSError:
            pass
    return candidates


def client_secret_candidates() -> list[Path]:
    candidates = [
        client_secret_path(),
        _runtime_root() / "client_secret.json",
    ]
    candidates.extend(nvda_addon_client_secret_candidates())
    return candidates


def find_client_secret() -> Path | None:
    for candidate in client_secret_candidates():
        if candidate.is_file():
            return candidate
    return None


def copy_client_secret(source: Path) -> Path:
    source = Path(source)
    if not source.is_file():
        raise FileNotFoundError(source)
    target = client_secret_path()
    if source.resolve() != target.resolve():
        shutil.copy2(source, target)
    return target


def migrate_from_nvda() -> dict[str, bool]:
    """Copy compatible user files from NVDA without changing their originals."""
    result = {"token": False, "settings": False, "client_secret": False}
    nvda_dir = nvda_user_data_dir()
    if nvda_dir:
        for name, target, key in (
            ("token.json", token_path(), "token"),
            ("settings.json", settings_path(), "settings"),
        ):
            source = nvda_dir / name
            if source.is_file() and not target.exists():
                shutil.copy2(source, target)
                result[key] = True

    if not client_secret_path().exists():
        for source in nvda_addon_client_secret_candidates():
            if source.is_file():
                shutil.copy2(source, client_secret_path())
                result["client_secret"] = True
                break
    return result
