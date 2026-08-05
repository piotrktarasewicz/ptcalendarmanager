from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

from .branding import DATA_DIR_NAME, LEGACY_DATA_DIR_NAMES, LEGACY_UNIX_DATA_DIR_NAMES

_MIGRATABLE_USER_FILES = (
    "token.dat",
    "token.json",
    "settings.json",
    "client_secret.json",
    "last_error.txt",
)


def app_data_dir(*, create: bool = True) -> Path:
    base = os.environ.get("APPDATA")
    if base:
        result = Path(base) / DATA_DIR_NAME
    else:
        result = Path.home() / ".pt-calendar-manager"
    if create:
        result.mkdir(parents=True, exist_ok=True)
    return result


def legacy_app_data_dirs() -> list[Path]:
    base = os.environ.get("APPDATA")
    if base:
        return [Path(base) / name for name in LEGACY_DATA_DIR_NAMES]
    return [Path.home() / name for name in LEGACY_UNIX_DATA_DIR_NAMES]


def migrate_legacy_app_data() -> dict[str, bool]:
    """Copy compatible files from an earlier product-name directory.

    Existing files in the new directory always win. The old directory and its
    contents are never removed, so rollback to an earlier development version
    remains possible.
    """
    target_dir = app_data_dir()
    migrated = {name: False for name in _MIGRATABLE_USER_FILES}
    for legacy_dir in legacy_app_data_dirs():
        if not legacy_dir.is_dir():
            continue
        for name in _MIGRATABLE_USER_FILES:
            source = legacy_dir / name
            target = target_dir / name
            if source.is_file() and not target.exists():
                try:
                    shutil.copy2(source, target)
                except OSError:
                    continue
                migrated[name] = True
    return migrated


def token_path() -> Path:
    return app_data_dir() / "token.dat"


def plaintext_token_path() -> Path:
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
    candidates.extend(directory / "client_secret.json" for directory in legacy_app_data_dirs())
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
            ("token.json", plaintext_token_path(), "token"),
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
