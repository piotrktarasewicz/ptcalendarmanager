# Copyright (C) 2026 Piotr Tarasewicz
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import json
from pathlib import Path

from .errors import clear_error, save_error
from .i18n import tr
from .paths import (
    client_secret_path,
    find_client_secret,
    plaintext_token_path,
    token_path,
)
from .secure_storage import read_protected_text, write_protected_text

SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar.calendarlist.readonly",
    "https://www.googleapis.com/auth/calendar.settings.readonly",
]


def has_client_secret() -> bool:
    return find_client_secret() is not None


def _credentials_from_json(text: str):
    from google.oauth2.credentials import Credentials

    payload = json.loads(text)
    if not isinstance(payload, dict):
        raise ValueError("Invalid OAuth token data.")
    return Credentials.from_authorized_user_info(payload, SCOPES)


def _save_credentials(credentials) -> None:
    """Store the OAuth token encrypted for the current Windows user."""
    write_protected_text(token_path(), credentials.to_json())
    legacy_plaintext = plaintext_token_path()
    if legacy_plaintext.exists():
        legacy_plaintext.unlink()


def load_credentials():
    encrypted = token_path()
    plaintext = plaintext_token_path()

    if encrypted.is_file():
        try:
            credentials = _credentials_from_json(read_protected_text(encrypted))
            if plaintext.exists():
                try:
                    plaintext.unlink()
                except OSError:
                    pass
            return credentials
        except Exception as error:
            save_error(tr("Odczyt zaszyfrowanego tokenu OAuth"), error)
            # A retained legacy token can still be migrated if the encrypted
            # file was copied from another Windows account and DPAPI cannot
            # decrypt it on this computer.

    if not plaintext.is_file():
        return None

    try:
        credentials = _credentials_from_json(plaintext.read_text(encoding="utf-8"))
    except Exception as error:
        save_error(tr("Odczyt tokenu OAuth"), error)
        return None

    try:
        _save_credentials(credentials)
        clear_error()
    except Exception as error:
        # Fail closed: do not use a plaintext token when Windows could not
        # protect it. The original file is retained so migration can be retried
        # after the underlying DPAPI problem has been resolved.
        save_error(tr("Szyfrowanie tokenu OAuth"), error)
        return None
    return credentials


def ensure_valid_credentials():
    credentials = load_credentials()
    if credentials is None:
        return None
    if credentials.valid:
        return credentials
    if credentials.expired and credentials.refresh_token:
        try:
            from google.auth.transport.requests import Request

            credentials.refresh(Request())
            _save_credentials(credentials)
            clear_error()
            return credentials
        except Exception as error:
            save_error(tr("Odświeżanie tokenu OAuth"), error)
            return None
    return None


def is_logged_in() -> bool:
    """Return whether a reusable OAuth token is stored, without network I/O.

    This function is called by the wxPython UI thread. It must never refresh an
    expired token because a network wait here would freeze the whole window.
    Actual refresh is performed by ensure_valid_credentials() inside a
    background task immediately before a Google operation.
    """
    credentials = load_credentials()
    if credentials is None:
        return False
    return bool(credentials.valid or credentials.refresh_token)


def login():
    secret = find_client_secret()
    if secret is None:
        raise FileNotFoundError(tr("Nie znaleziono pliku client_secret.json."))
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow

        flow = InstalledAppFlow.from_client_secrets_file(str(secret), SCOPES)
        credentials = flow.run_local_server(
            host="127.0.0.1",
            port=0,
            open_browser=True,
            authorization_prompt_message=tr(
                "Otwieranie przeglądarki do logowania Google. Po zakończeniu wróć do aplikacji PT Calendar Manager."
            ),
            success_message=tr(
                "Logowanie zakończone. Możesz zamknąć tę kartę i wrócić do PT Calendar Manager."
            ),
        )
        _save_credentials(credentials)
        clear_error()
        return credentials
    except Exception as error:
        save_error(tr("Logowanie OAuth"), error)
        raise


def logout() -> None:
    for path in (token_path(), plaintext_token_path()):
        if path.exists():
            path.unlink()
