# Google Calendar Manager

[Polska wersja tego opisu](README_pl.md)

[Download Google Calendar Manager 1.0.3](https://github.com/piotrktarasewicz/nvda-google-calendar-manager/releases/download/v1.0.3/googleCalendarManager-1.0.3.nvda-addon)

Google Calendar Manager is an NVDA add-on for Windows. It lets NVDA users sign in to Google Calendar, choose calendars, read events, search events, and manage basic event operations from the keyboard.

The add-on is intended for direct keyboard access from NVDA. It does not replace the full Google Calendar web interface.

## Current status

Version 1.0.3 is the latest public test version.

The add-on package can be downloaded and installed, but Google sign-in is currently available only to Google accounts added as approved OAuth test users by the author. Full public Google sign-in requires Google OAuth app verification.

## Features

- Sign in to Google Calendar through a web browser.
- Check Google Calendar sign-in status.
- Choose which calendars are used by the add-on.
- Read events for today and the next six days.
- Read events for a selected day.
- Add an event directly from the selected-day results window.
- Search events by text in a selected time range.
- Choose predefined one-, three-, six-, or twelve-month search ranges.
- Configure a custom search range directly in the main search dialog.
- Add new events, including recurring events.
- Edit existing events.
- Delete one or more selected events.
- Choose whether operations on recurring events affect only the selected occurrence or the entire series.
- Bulk handling of recurring-event scope when deleting multiple selected events.
- Switch between short and full speech modes.
- English and Polish user interface messages.

## Not included

Google Calendar Manager does not manage:

- meeting participants,
- Google Meet links,
- room or participant availability,
- Google Maps place search,
- attachments,
- calendar reminders.

The event location field is plain text. The add-on does not search Google Maps or verify addresses.

## Requirements

- Windows.
- NVDA 2026.1 or newer.
- Internet access.
- A Google account with Google Calendar enabled.

A separate Python installation is not required. The add-on uses the Python environment provided by NVDA and includes the Python libraries it needs.

## Installation

1. Download the `.nvda-addon` file from the release page.
2. Open it and confirm installation in NVDA.
3. Restart NVDA if requested.
4. Press `NVDA+Shift+G`, then `0`, to sign in to Google Calendar or check sign-in status.

If Google sign-in is not available for your account yet, contact the author and ask to be added as a test user.

## Main keyboard layer

First press `NVDA+Shift+G`. Then press one of the following keys:

| Key | Action |
| --- | --- |
| `0` | Start Google sign-in or check sign-in status. |
| `1` | Read events for today. |
| `2` | Read events for tomorrow. |
| `3` | Read events for the day after tomorrow. |
| `4` | Read events for three days from now. |
| `5` | Read events for four days from now. |
| `6` | Read events for five days from now. |
| `7` | Read events for six days from now. |
| `8` | Switch between short and full speech mode. |
| `9` | Choose calendars. |
| `P` | Choose a day and open event actions for that day. |
| `S` | Search events by text. |
| `N` | Add an event. |
| `E` | Edit an event. |
| `U` | Delete events. |
| `H` | Show help for shortcuts. |

Direct shortcuts are also available:

- `NVDA+Control+Shift+N`: add an event.
- `NVDA+Control+Shift+E`: edit an event.
- `NVDA+Control+Shift+U`: delete events.

## Recurring events

When editing or deleting a recurring event, the add-on asks whether the action should affect only the selected occurrence or the entire series.

When deleting multiple selected recurring events, the recurring-event scope is chosen once and applied to the selected recurring events in that operation.

The option to edit or delete "this and following occurrences" is not included.

## All-day events

All-day non-recurring events can be one-day or multi-day events.

For recurring all-day events, each occurrence is treated as a single all-day occurrence. If the recurring series has an end date, the recurrence end date is set separately with day, month, and year.

## Language

The add-on uses the current NVDA language for its own messages and dialogs.

Currently included languages:

- English,
- Polish.

If the current NVDA language is not included, the add-on uses English. Event titles, descriptions, and locations are user content from Google Calendar and are not translated.

## Google Calendar access

The add-on uses OAuth 2.0 and the Google Calendar API. It requests only the scopes needed for its current features:

- `https://www.googleapis.com/auth/calendar.events`
- `https://www.googleapis.com/auth/calendar.calendarlist.readonly`
- `https://www.googleapis.com/auth/calendar.settings.readonly`

The add-on does not request permission to create, delete, share, or change calendars themselves.

## User files

The add-on stores its settings and Google sign-in token locally in the NVDA user configuration directory, in the `googleCalendarManager` subfolder.

Typical local files are:

- `token.json`: local Google sign-in token,
- `settings.json`: selected calendars and speech mode settings,
- `last_oauth_error.txt`: helper file for OAuth error diagnostics.

These files are not part of the add-on package and should not be committed to the repository.

## Privacy

See [PRIVACY.md](PRIVACY.md).

## User guide

The add-on package includes a detailed user guide:

- `docs/readme.html` — English,
- `docs/readme_pl.html` — Polish.

## License

Google Calendar Manager is licensed under the GNU General Public License version 3 or later (`GPL-3.0-or-later`). See [LICENSE](LICENSE) and [LICENSE-NOTICE.md](LICENSE-NOTICE.md).

## Author

Piotr Tarasewicz

Contact: `https://ptprojects.app/contact.html`

Project page: `https://ptprojects.app/projects/google-calendar-manager/`
