# Copyright (C) 2026 Piotr Tarasewicz
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from html import escape

from .branding import INDEPENDENCE_NOTICE_EN, INDEPENDENCE_NOTICE_PL
from .i18n import get_language


def _paragraph(text: str) -> str:
    return f"<p>{escape(text)}</p>"


def _list(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{escape(item)}</li>" for item in items) + "</ul>"


def _section(title: str, *content: str) -> str:
    return f"<section><h2>{escape(title)}</h2>{''.join(content)}</section>"


def get_help_html(language: str | None = None) -> str:
    """Return the accessible, self-contained help document for the selected language."""
    selected_language = language or get_language()
    if selected_language == "pl":
        title = "PT Calendar Manager — pomoc i skróty klawiaturowe"
        sections = [
            _section(
                "Przeznaczenie aplikacji",
                _paragraph(
                    "PT Calendar Manager służy do szybkiego, dostępnego zarządzania "
                    "Kalendarzem Google. Bardziej zaawansowane funkcje pozostają "
                    "w oficjalnym interfejsie Google."
                ),
            ),
            _section(
                "Układ głównego okna",
                _paragraph(
                    "Na górze znajduje się klasyczny pasek menu: Kalendarz, Wydarzenie, "
                    "Konto, Ustawienia i Pomoc. Lewy Alt przenosi fokus do menu. Po lewej "
                    "znajduje się lista dni bieżącego miesiąca, a po prawej lista wydarzeń "
                    "zaznaczonego dnia. Tab przełącza tylko między tymi dwiema listami. "
                    "Enter na liście dni przenosi fokus na wydarzenia, a Enter na wydarzeniu "
                    "otwiera szczegóły. Shift+F10 otwiera menu kontekstowe bieżącej listy."
                ),
            ),
            _section(
                "Skróty aplikacji",
                _list(
                    [
                        "Ctrl+L — zaloguj do Google albo wyloguj.",
                        "Ctrl+, — otwórz ustawienia.",
                        "Ctrl+K — otwórz ustawienia, zachowany skrót wyboru kalendarzy.",
                        "F1 — otwórz pomoc.",
                        "Alt+Strzałka w lewo — poprzedni miesiąc.",
                        "Ctrl+D — dzisiaj.",
                        "Alt+Strzałka w prawo — następny miesiąc.",
                        "Ctrl+G — przejdź do daty.",
                        "Ctrl+F — wyszukaj wydarzenia.",
                        "Ctrl+N — dodaj wydarzenie.",
                        "F5 — odśwież dane.",
                        "Ctrl+E — edytuj wydarzenie.",
                        "Delete — usuń wydarzenie.",
                        "Ctrl+Shift+G — otwórz wydarzenie w Kalendarzu Google.",
                        "Ctrl+J — otwórz lub skopiuj link spotkania.",
                    ]
                ),
            ),
            _section(
                "Język aplikacji",
                _paragraph(
                    "Dostępne są ustawienia Automatycznie, Polski i English. Tryb "
                    "automatyczny używa języka Windows: polskiego dla polskiego systemu, "
                    "a angielskiego dla pozostałych. Ręczna zmiana języka zaczyna działać "
                    "po ponownym uruchomieniu PT Calendar Manager."
                ),
            ),
            _section(
                "O programie i prywatność",
                _paragraph(
                    "W menu Pomoc znajduje się polecenie O programie. Udostępnia ono "
                    "informacje o wersji, autorze, niezależności produktu, politykę "
                    "prywatności oraz informacje prawne. Token Google jest przechowywany "
                    "lokalnie i szyfrowany mechanizmem Windows DPAPI."
                ),
            ),
            _section(
                "Wydarzenia cykliczne",
                _paragraph(
                    "PT Calendar Manager tworzy i edytuje podstawowe cykle: codzienne, "
                    "tygodniowe, miesięczne, kwartalne, półroczne i roczne. Zaawansowane "
                    "reguły utworzone poza PT Calendar Manager można edytować tylko jako "
                    "pojedyncze wystąpienia."
                ),
            ),
            _section(
                "Otwieranie w Google i link spotkania",
                _paragraph(
                    "Otwórz w Google przechodzi do wybranego wydarzenia w przeglądarce. "
                    "Link spotkania można otworzyć albo skopiować, jeżeli został dodany "
                    "do wydarzenia poza PT Calendar Manager."
                ),
            ),
            _section(
                "Informacja o niezależności",
                _paragraph(INDEPENDENCE_NOTICE_PL),
            ),
        ]
        document_language = "pl"
    else:
        title = "PT Calendar Manager — help and keyboard shortcuts"
        sections = [
            _section(
                "Purpose",
                _paragraph(
                    "PT Calendar Manager provides quick, accessible management of Google "
                    "Calendar. More advanced features remain available in Google's official "
                    "interface."
                ),
            ),
            _section(
                "Main window",
                _paragraph(
                    "A standard menu bar at the top contains Calendar, Event, Account, "
                    "Settings and Help. Press the left Alt key to move to the menu bar. The "
                    "days of the current month are listed on the left and events for the "
                    "selected day are on the right. Tab moves only between these two lists. "
                    "Enter on the day list moves focus to events, and Enter on an event opens "
                    "its details. Shift+F10 opens the context menu for the focused list."
                ),
            ),
            _section(
                "Application shortcuts",
                _list(
                    [
                        "Ctrl+L — sign in to or sign out of Google.",
                        "Ctrl+, — open Settings.",
                        "Ctrl+K — open Settings; retained as the former calendar shortcut.",
                        "F1 — open Help.",
                        "Alt+Left Arrow — previous month.",
                        "Ctrl+D — today.",
                        "Alt+Right Arrow — next month.",
                        "Ctrl+G — go to date.",
                        "Ctrl+F — search events.",
                        "Ctrl+N — add an event.",
                        "F5 — refresh data.",
                        "Ctrl+E — edit an event.",
                        "Delete — delete an event.",
                        "Ctrl+Shift+G — open the event in Google Calendar.",
                        "Ctrl+J — open or copy a meeting link.",
                    ]
                ),
            ),
            _section(
                "Application language",
                _paragraph(
                    "The available choices are Automatic, Polish and English. Automatic "
                    "uses the Windows language: Polish on a Polish system and English for "
                    "other systems. A manual language change takes effect after PT Calendar "
                    "Manager is restarted."
                ),
            ),
            _section(
                "About and privacy",
                _paragraph(
                    "The Help menu contains About with version and author information, the "
                    "independence notice, the Privacy Policy and legal information. The Google "
                    "token is stored locally and encrypted with Windows DPAPI."
                ),
            ),
            _section(
                "Recurring events",
                _paragraph(
                    "PT Calendar Manager creates and edits basic daily, weekly, monthly, "
                    "quarterly, semiannual and yearly recurrences. Advanced rules created "
                    "outside PT Calendar Manager can only be edited as individual occurrences."
                ),
            ),
            _section(
                "Opening in Google and meeting links",
                _paragraph(
                    "Open in Google opens the selected event in a browser. A meeting link can "
                    "be opened or copied when it was added to the event outside PT Calendar "
                    "Manager."
                ),
            ),
            _section(
                "Independence notice",
                _paragraph(INDEPENDENCE_NOTICE_EN),
            ),
        ]
        document_language = "en"

    return (
        "<!doctype html>"
        f'<html lang="{document_language}"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f"<title>{escape(title)}</title>"
        "<style>"
        ":root{color-scheme:light dark}"
        "body{font-family:'Segoe UI',sans-serif;font-size:100%;line-height:1.55;"
        "margin:1rem;max-width:70rem}"
        "h1{font-size:1.75rem}h2{font-size:1.35rem;margin-top:1.5rem}"
        "li{margin:.3rem 0}"
        "</style></head><body>"
        f'<main aria-labelledby="help-title"><h1 id="help-title">{escape(title)}</h1>'
        + "".join(sections)
        + "</main></body></html>"
    )
