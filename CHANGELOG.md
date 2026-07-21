# Changelog

All notable changes to Google Calendar Manager are documented in this file.

## 1.0.3 - 2026-07-21

### Changed

- The custom event-search range is now configured directly in the main search dialog.
- Selecting `Custom range` shows the start day, start month, end day, and end month fields before the Search button.
- Switching back to a predefined range hides the custom date fields and removes them from keyboard navigation.
- The predefined one-, three-, six-, and twelve-month search ranges continue to work as before.

## 1.0.2 - 2026-07-06

Public test release candidate.

### Added

- Google sign-in from NVDA through the user's default web browser.
- Calendar selection.
- Reading events for today and the next six days.
- Reading events for a selected day.
- Adding an event directly from the selected-day results window.
- Event search by text with selectable time ranges.
- Adding events, including recurring events.
- Editing existing events.
- Deleting one or more selected events.
- Support for recurring-event scope selection: selected occurrence or entire series.
- Bulk handling of recurring-event scope when deleting multiple selected events.
- Short and full speech modes.
- English and Polish user interface messages.
- Local storage of sign-in token and add-on settings in the NVDA user configuration directory.

### Changed

- The add-on name is now Google Calendar Manager.
- The internal add-on name is `googleCalendarManager`.
- The user data directory is now `googleCalendarManager`.
- Existing data from the old `googleCalendarReader` directory is migrated when possible.
- Dialog focus handling was improved so add-on dialogs receive focus more reliably when opened from other applications.
- The search range selector now starts from the first option for easier keyboard exploration.
- The add/edit event form now separates event duration fields from recurrence end fields more clearly.

### Fixed

- Recurring events with a defined end date now require an explicit end year, in addition to end day and end month.
- Recurrence end year validation was added. The end year must be between the event start year and the start year plus 50 years.
- Editing an existing recurring event should no longer silently replace the recurrence end date with the event start date when the event start date is changed.
- Multi-day all-day non-recurring events are handled separately from recurrence end dates.
- The add-on no longer repeatedly asks for recurring-event scope for every selected occurrence when deleting multiple recurring events.
- Checkbox state feedback in event selection lists was made less verbose when selecting or deselecting items.

### Security and privacy

- OAuth scopes are limited to the Google Calendar API scopes needed by the add-on:
  - `https://www.googleapis.com/auth/calendar.events`
  - `https://www.googleapis.com/auth/calendar.calendarlist.readonly`
  - `https://www.googleapis.com/auth/calendar.settings.readonly`
- The add-on does not use the broader full-calendar scope.
- The add-on does not use an external server controlled by the author.
- The add-on does not send Google Calendar data to third-party services controlled by the author.

### Notes

- This is a test release candidate. Google sign-in is currently available only for Google accounts added as OAuth test users by the author.
- The add-on does not manage meeting participants, Google Meet links, room availability, Google Maps place search, attachments, or reminders.
- The option to edit or delete this and following recurring occurrences is not included.
