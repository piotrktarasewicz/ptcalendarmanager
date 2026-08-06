# Copyright (C) 2026 Piotr Tarasewicz
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import json
import sys
from pathlib import Path


def validate_payload(payload: object) -> None:
    if not isinstance(payload, dict):
        raise ValueError("Top-level JSON value must be an object.")

    installed = payload.get("installed")
    if not isinstance(installed, dict):
        raise ValueError("The OAuth client must have Desktop app type.")

    client_id = installed.get("client_id")
    if not isinstance(client_id, str) or not client_id.endswith(
        ".apps.googleusercontent.com"
    ):
        raise ValueError("A valid Desktop app client_id is required.")

    client_secret = installed.get("client_secret")
    if not isinstance(client_secret, str) or not client_secret:
        raise ValueError("A non-empty client_secret is required.")

    if installed.get("auth_uri") != "https://accounts.google.com/o/oauth2/auth":
        raise ValueError("The Google OAuth authorization endpoint is invalid.")

    if installed.get("token_uri") != "https://oauth2.googleapis.com/token":
        raise ValueError("The Google OAuth token endpoint is invalid.")

    redirect_uris = installed.get("redirect_uris")
    if not isinstance(redirect_uris, list) or not redirect_uris:
        raise ValueError("At least one loopback redirect URI is required.")
    if not all(isinstance(uri, str) and uri for uri in redirect_uris):
        raise ValueError("Every redirect URI must be a non-empty string.")


def validate_file(path: Path) -> None:
    with Path(path).open("r", encoding="utf-8-sig") as stream:
        payload = json.load(stream)
    validate_payload(payload)


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if len(arguments) != 1:
        print("Usage: validate_oauth_client.py <client_secret.json>", file=sys.stderr)
        return 2
    try:
        validate_file(Path(arguments[0]))
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        print(f"Invalid OAuth client configuration: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
