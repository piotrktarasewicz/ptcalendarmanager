# Copyright (C) 2026 Piotr Tarasewicz
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import traceback

from .i18n import tr
from .paths import error_path


def clear_error() -> None:
    try:
        error_path().write_text("", encoding="utf-8")
    except Exception:
        pass


def save_error(context: str, error: BaseException) -> None:
    text = tr(
        "Kontekst: {context}\nTyp: {type}\nTreść: {message}\n\n{traceback}",
        context=context,
        type=type(error).__name__,
        message=error,
        traceback=traceback.format_exc(),
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
