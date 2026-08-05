# Privacy Policy

PT CALENDAR MANAGER PRIVACY POLICY

Last updated: 5 August 2026

1. Scope

This policy explains how PT Calendar Manager accesses, uses and stores Google Calendar data. The application is developed by Piotr Tarasewicz under the PT Projects name.

2. Google sign-in and access scopes

Sign-in takes place in the user's browser through Google OAuth 2.0. The user grants the requested permissions. The application uses these scopes:

- https://www.googleapis.com/auth/calendar.events
- https://www.googleapis.com/auth/calendar.calendarlist.readonly
- https://www.googleapis.com/auth/calendar.settings.readonly

They are used to read the calendar list and time-zone settings and to read, search, create, edit and delete events when the user explicitly requests an action.

3. Google data accessed

The application may process calendar and event data, including names, titles, descriptions, locations, dates, times, recurrence rules, technical identifiers, attendee information and existing meeting links. This data is used only for features visible in the application interface.

4. Local storage

PT Calendar Manager does not maintain an external database of users' events. Downloaded events are held in application memory while the program is running and are not written to a separate local event database.

The %APPDATA%\PT Calendar Manager folder may contain:

- token.dat — the Google token encrypted with Windows DPAPI and tied to the current Windows user account;
- settings.json — the selected language and selected calendar identifiers;
- client_secret.json — the application's OAuth client configuration;
- last_error.txt — a local technical report for the most recent error.

An error report may contain technical identifiers, calendar names or fragments of data related to the operation that failed. It is not automatically sent to the developer or to another server.

When upgrading from an earlier version, a previous token.json file may temporarily remain in the current data folder. After successful encryption, the application removes the current-folder plaintext copy. Data folders from older application versions are not removed automatically so that rollback remains possible.

5. Data transmission and sharing

Calendar data is transmitted directly between the application and the Google services required for sign-in and the Google Calendar API. PT Projects does not receive copies of users' calendars, events or tokens and does not use them for advertising, profiling or analytics.

The application does not sell or disclose user data to other parties. Its use of information received from Google APIs is limited to the application's user-facing features and complies with the Google API Services User Data Policy, including the Limited Use requirements.

6. User control and deletion

Signing out in the application removes the local Google token. Access can also be revoked in the security settings of the user's Google Account. Other local data can be removed by deleting the %APPDATA%\PT Calendar Manager folder after closing the application.

A future installed version may preserve user settings during uninstall when the user chooses to keep them. The installer should clearly explain that choice.

7. Security

The token is protected by Windows DPAPI, which limits its use by another Windows account on the same computer. No technical measure can provide absolute security, so users should protect their Windows account and device.

8. Changes and contact

This policy may be updated when the application, Google access scopes or data storage practices change. The current version will be published on the PT Projects website. Questions can be submitted through https://ptprojects.app/.
