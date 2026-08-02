from __future__ import annotations

from pathlib import Path

from .errors import clear_error, save_error
from .paths import client_secret_path, find_client_secret, token_path

SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar.calendarlist.readonly",
    "https://www.googleapis.com/auth/calendar.settings.readonly",
]


def has_client_secret() -> bool:
    return find_client_secret() is not None


def load_credentials():
    path = token_path()
    if not path.is_file():
        return None
    try:
        from google.oauth2.credentials import Credentials
        return Credentials.from_authorized_user_file(str(path), SCOPES)
    except Exception as error:
        save_error("Odczyt tokenu OAuth", error)
        return None


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
            token_path().write_text(credentials.to_json(), encoding="utf-8")
            clear_error()
            return credentials
        except Exception as error:
            save_error("Odświeżanie tokenu OAuth", error)
            return None
    return None


def is_logged_in() -> bool:
    return ensure_valid_credentials() is not None


def login():
    secret = find_client_secret()
    if secret is None:
        raise FileNotFoundError("Nie znaleziono pliku client_secret.json.")
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        flow = InstalledAppFlow.from_client_secrets_file(str(secret), SCOPES)
        credentials = flow.run_local_server(
            host="127.0.0.1",
            port=0,
            open_browser=True,
            authorization_prompt_message=(
                "Otwieranie przeglądarki do logowania Google. "
                "Po zakończeniu wróć do aplikacji GCM by Piotrek."
            ),
            success_message=(
                "Logowanie zakończone. Możesz zamknąć tę kartę i wrócić do "
                "GCM by Piotrek."
            ),
        )
        token_path().write_text(credentials.to_json(), encoding="utf-8")
        clear_error()
        return credentials
    except Exception as error:
        save_error("Logowanie OAuth", error)
        raise


def logout() -> None:
    path = token_path()
    if path.exists():
        path.unlink()
