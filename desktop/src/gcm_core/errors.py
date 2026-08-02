from __future__ import annotations

import traceback

from .paths import error_path


def clear_error() -> None:
    try:
        error_path().write_text("", encoding="utf-8")
    except Exception:
        pass


def save_error(context: str, error: BaseException) -> None:
    text = (
        f"Kontekst: {context}\n"
        f"Typ: {type(error).__name__}\n"
        f"Treść: {error}\n\n"
        f"{traceback.format_exc()}"
    )
    try:
        error_path().write_text(text, encoding="utf-8")
    except Exception:
        pass


def get_error_text() -> str:
    try:
        return error_path().read_text(encoding="utf-8").strip()
    except Exception:
        return ""
