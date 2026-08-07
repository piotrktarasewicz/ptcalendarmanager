# Privacy Policy for Google Calendar Manager

Effective date: 2026-07-09

Google Calendar Manager is an NVDA add-on for Windows. It lets users access and manage selected Google Calendar events from NVDA.

This policy describes how the add-on accesses, uses, stores, and shares Google user data.

## Data accessed from Google Calendar

Google Calendar Manager may access the following Google Calendar data, depending on the user's actions:

- calendar list entries, so the user can choose which calendars the add-on should use;
- calendar settings, such as the user's Calendar time zone;
- event data in selected calendars, including event titles, dates, times, descriptions, locations, recurrence information, and event identifiers.

## OAuth scopes used

The add-on requests the following Google Calendar API scopes:

- `https://www.googleapis.com/auth/calendar.events`
  - Used to read, add, edit, and delete calendar events according to the user's actions.
- `https://www.googleapis.com/auth/calendar.calendarlist.readonly`
  - Used to read the user's calendar list so calendars can be selected in the add-on.
- `https://www.googleapis.com/auth/calendar.settings.readonly`
  - Used to read Calendar settings, such as the Calendar time zone.

The add-on does not request permission to create, delete, share, or modify calendars themselves.

## How data is used

Google Calendar data is used only to provide the add-on's calendar features:

- reading events aloud in NVDA;
- displaying event lists in NVDA dialogs;
- searching events by text;
- adding new events;
- editing existing events;
- deleting selected events;
- choosing calendars used by the add-on.

Google Calendar data is not used for advertising, analytics, profiling, or unrelated purposes.

## Local storage

Google Calendar Manager stores its settings and Google sign-in token locally on the user's computer, in the NVDA user configuration directory, under the `googleCalendarManager` subfolder.

Typical local files are:

- `token.json`: Google OAuth sign-in token;
- `settings.json`: selected calendars and add-on settings;
- `last_oauth_error.txt`: diagnostic information for OAuth errors.

The add-on does not store Google Calendar data on a server controlled by the author.

## Data sharing

Google Calendar Manager does not sell, rent, or share Google Calendar data with third parties.

The add-on communicates with Google Calendar API as needed to perform the actions requested by the user. It does not send calendar data to servers controlled by the author.

## Human access to user data

The author does not have access to users' Google Calendar data through the add-on.

If a user contacts the author for support and voluntarily provides logs, screenshots, or calendar details, that information will be used only to diagnose the reported issue.

## Data retention and deletion

Google Calendar Manager stores OAuth tokens and settings locally until the user removes them.

A user can remove local add-on data by deleting the `googleCalendarManager` folder from the NVDA user configuration directory.

A user can revoke the add-on's Google access at any time from the Google Account security settings, under third-party app access.

## Limited Use

Google Calendar Manager's use and transfer of information received from Google APIs will adhere to the Google API Services User Data Policy, including the Limited Use requirements.

## Contact

Author: Piotr Tarasewicz

Contact: `https://ptprojects.app/contact.html`

Project page: `https://ptprojects.app/projects/google-calendar-manager/`
