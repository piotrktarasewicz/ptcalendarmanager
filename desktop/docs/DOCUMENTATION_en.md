# PT Calendar Manager — User Documentation

Version 0.14.0

## 1. Purpose

PT Calendar Manager is an accessible Windows application for everyday Google Calendar management without requiring the full web interface. It is not intended to reproduce every Google Calendar feature. Advanced operations can be opened directly in Google's official interface.

The interface is keyboard-driven and tested with NVDA, JAWS and Narrator.

## 2. First launch and sign-in

The main window remains usable without signing in. Language settings and About information are available offline.

To connect a Google Account:

1. Choose “Sign in to Google” or press `Ctrl+L`.
2. If the OAuth configuration is not found, select `client_secret.json`.
3. Sign in and grant the requested permissions in the browser.
4. Return to PT Calendar Manager.

The sign-in token is stored locally as `token.dat` and encrypted with Windows DPAPI for the current Windows user.

## 3. Main window

The top row contains Sign in or Sign out, Settings, and Help and shortcuts. Navigation and common actions appear below. The left list contains days of the current month and the right list contains events for the selected day.

Press `Enter` on the day list to move focus to events. Press `Enter` on an event to open its details.

## 4. Settings

Open Settings with `Ctrl+,` or `Ctrl+K`.

Settings provides:

- Automatic, Polish or English application language;
- calendar selection;
- an About button.

When the effective language changes, the application offers to restart immediately. Calendar-only changes do not require a restart.

About contains version and author information, the independence notice, the Privacy Policy and legal information.

## 5. Creating and editing events

PT Calendar Manager supports timed and all-day events. The form includes title, dates, times, location, calendar and basic recurrence.

Supported recurrence patterns:

- daily;
- weekly;
- monthly;
- every 3 months;
- every 6 months;
- yearly.

A series can have no end date or end on a selected date.

A recurring event can be edited as one occurrence or as an entire simple series. Advanced rules created outside PT Calendar Manager are protected against accidental simplification.

## 6. Deleting events

Deletion always requires confirmation. A recurring event can be deleted as:

- this occurrence only;
- this and all following occurrences;
- the entire series.

The safest single-occurrence option is selected by default.

## 7. Searching

Search uses the selected calendars, search text, and inclusive start and end dates. Selecting a result moves to the correct day and focuses the event.

## 8. Opening in Google and meeting links

Open in Google opens the selected event in the official Google Calendar interface.

When an event contains a supported web meeting link created outside the application, Meeting link can open or copy it. PT Calendar Manager does not create Google Meet conferences.

## 9. Application shortcuts

- `Ctrl+L` — sign in or sign out;
- `Ctrl+,` — Settings;
- `Ctrl+K` — Settings, retained as the former calendar shortcut;
- `F1` — Help;
- `Alt+Left Arrow` — previous month;
- `Ctrl+D` — today;
- `Alt+Right Arrow` — next month;
- `Ctrl+G` — go to date;
- `Ctrl+F` — search;
- `Ctrl+N` — add an event;
- `F5` — refresh;
- `Ctrl+E` — edit;
- `Delete` — delete;
- `Ctrl+Shift+G` — open the event in Google;
- `Ctrl+J` — open or copy a meeting link.

Buttons also expose standard Windows `Alt+letter` access keys to screen readers.

## 10. User data

Local data is stored in `%APPDATA%\PT Calendar Manager`. See the Privacy Policy for details.

Signing out removes the local token. Access can also be revoked in the security settings of the user's Google Account.

## 11. Intentionally unsupported features

The first release does not include:

- adding or editing attendees;
- creating Google Meet conferences;
- per-event reminders;
- manual time-zone selection;
- free or busy status selection;
- custom recurrence rules.

Use Open in Google for these operations.
