import gettext
import locale
import os

try:
    import addonHandler
    addonHandler.initTranslation()
except Exception:
    addonHandler = None

try:
    import languageHandler
except Exception:
    languageHandler = None

SUPPORTED_LANGS = ("pl", "en")

WEEKDAYS = {'en': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
 'pl': ['poniedziałek', 'wtorek', 'środa', 'czwartek', 'piątek', 'sobota', 'niedziela']}

MONTHS = {'en': ['January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'],
 'pl': ['stycznia',
        'lutego',
        'marca',
        'kwietnia',
        'maja',
        'czerwca',
        'lipca',
        'sierpnia',
        'września',
        'października',
        'listopada',
        'grudnia']}

RECURRENCE_CHOICES = {'en': ['One time', 'Daily', 'Weekly', 'Monthly', 'Yearly'],
 'pl': ['Jednorazowo', 'Codziennie', 'Co tydzień', 'Co miesiąc', 'Co rok']}

ENGLISH_MESSAGES = {'add_event_all_day_label': 'All-day event',
 'add_event_calendar_label': 'Calendar',
 'add_event_day_label': 'Start day',
 'add_event_dialog_title': 'Add event',
 'add_event_end_day_label': 'End day',
 'add_event_end_hour_label': 'End time, hours',
 'add_event_end_minute_label': 'End time, minutes',
 'add_event_end_month_label': 'End month',
 'add_event_error_calendar_required': 'Choose a calendar.',
 'add_event_error_day_required': 'Enter a valid start day.',
 'add_event_error_end_before_start': 'End time must be later than start time.',
 'add_event_error_end_date_before_start': 'End date cannot be earlier than start date.',
 'add_event_error_end_day_required': 'Enter a valid end day.',
 'add_event_error_end_month_required': 'Enter a valid end month.',
 'add_event_error_end_time': 'Enter a valid end time.',
 'add_event_error_failed': 'Failed to add the event. Press the “Details” button to learn more.',
 'add_event_error_invalid_date': 'Enter a valid start date.',
 'add_event_error_invalid_end_date': 'Enter a valid end date.',
 'add_event_error_month_required': 'Enter a valid start month.',
 'add_event_error_recurrence_end_before_start': 'Recurrence end date cannot be earlier than start date.',
 'add_event_error_recurrence_end_day_required': 'Enter a valid recurrence end day.',
 'add_event_error_recurrence_end_month_required': 'Enter a valid recurrence end month.',
 'add_event_error_recurrence_end_year_required': 'Enter a valid recurrence end year.',
 'add_event_error_recurrence_end_year_range': 'Enter a recurrence end year between {min_year} and {max_year}.',
 'add_event_error_recurrence_invalid_end_date': 'Enter a valid recurrence end date.',
 'add_event_error_start_time': 'Enter a valid start time.',
 'add_event_error_title_required': 'Enter the event title.',
 'add_event_location_label': 'Location',
 'add_event_open_label': 'Add event',
 'add_event_month_label': 'Start month',
 'add_event_recurrence_end_day_label': 'Recurrence end day',
 'add_event_recurrence_end_month_label': 'Recurrence end month',
 'add_event_recurrence_end_year_label': 'Recurrence end year',
 'add_event_recurrence_label': 'Recurrence',
 'add_event_recurrence_no_end_label': 'No recurrence end date',
 'add_event_start_hour_label': 'Start time, hours',
 'add_event_start_minute_label': 'Start time, minutes',
 'add_event_success_all_day_range': 'Added a new event to calendar {calendar}: from {start_date} to {end_date} {title}',
 'add_event_success_all_day_single': 'Added a new event to calendar {calendar}: {date} {title}',
 'add_event_success_timed': 'Added a new event to calendar {calendar}: {date} at {time} {title}',
 'add_event_title_label': 'Title',
 'add_recurrence_success_daily': 'Added recurring event: daily from {date}',
 'add_recurrence_success_daily_timed': 'Added recurring event: daily from {date} at {time}',
 'add_recurrence_success_monthly': 'Added recurring event: monthly from {date}',
 'add_recurrence_success_monthly_timed': 'Added recurring event: monthly from {date} at {time}',
 'add_recurrence_success_weekly': 'Added recurring event: weekly from {date}',
 'add_recurrence_success_weekly_timed': 'Added recurring event: weekly from {date} at {time}',
 'add_recurrence_success_yearly': 'Added recurring event: yearly from {date}',
 'add_recurrence_success_yearly_timed': 'Added recurring event: yearly from {date} at {time}',
 'all_day_full': 'all-day event, {summary}{calendar_label}',
 'all_day_range_short': 'all-day, {range_text}, {summary}',
 'all_day_short': 'all-day, {summary}{calendar_label}',
 'busy_adding_event': 'Adding the event to the calendar...',
 'busy_deleting_event': 'Deleting the event from the calendar...',
 'busy_deleting_events': 'Deleting events from the calendar...',
 'busy_fetching_calendars': 'Fetching the calendar list...',
 'busy_fetching_events': 'Fetching calendar events...',
 'busy_fetching_events_for_selected_day': 'Fetching events for the selected day...',
 'busy_fetching_events_to_delete': 'Fetching events to delete...',
 'busy_fetching_events_to_edit': 'Fetching events to edit...',
 'busy_saving_event_changes': 'Saving changes to the calendar...',
 'busy_searching_events': 'Searching calendar events...',
 'calendar_dialog_info': 'Choose calendars to read. If you select none, the primary calendar will be used.',
 'calendar_dialog_title': 'Google Calendar selection',
 'calendar_list_empty_title': 'Calendars',
 'calendar_list_failed_title': 'Calendar error',
 'calendar_list_fetch_failed': 'Could not fetch calendar list.',
 'calendar_prefix': 'calendar {name}',
 'checked_state': 'selected',
 'date_no_events': '{date}. No events.',
 'date_range': '{start} to {end}',
 'delete_event_confirm_all_day_range': 'Delete the event from calendar {calendar}: from {start_date} to {end_date} '
                                       '{title}?',
 'delete_event_confirm_all_day_single': 'Delete the event from calendar {calendar}: {date} {title}?',
 'delete_event_confirm_delete_label': 'Delete',
 'delete_event_confirm_instance_all_day_range': 'Delete only this occurrence from calendar {calendar}: from '
                                                '{start_date} to {end_date} {title}?',
 'delete_event_confirm_instance_all_day_single': 'Delete only this occurrence from calendar {calendar}: {date} '
                                                 '{title}?',
 'delete_event_confirm_instance_timed': 'Delete only this occurrence from calendar {calendar}: {date} at {time} '
                                        '{title}?',
 'delete_event_confirm_multiple_intro': 'Delete {count} selected events?',
 'delete_event_confirm_recurrence_daily': 'Delete recurring event: daily from {date}?',
 'delete_event_confirm_recurrence_daily_timed': 'Delete recurring event: daily from {date} at {time}?',
 'delete_event_confirm_recurrence_monthly': 'Delete recurring event: monthly from {date}?',
 'delete_event_confirm_recurrence_monthly_timed': 'Delete recurring event: monthly from {date} at {time}?',
 'delete_event_confirm_recurrence_weekly': 'Delete recurring event: weekly from {date}?',
 'delete_event_confirm_recurrence_weekly_timed': 'Delete recurring event: weekly from {date} at {time}?',
 'delete_event_confirm_recurrence_yearly': 'Delete recurring event: yearly from {date}?',
 'delete_event_confirm_recurrence_yearly_timed': 'Delete recurring event: yearly from {date} at {time}?',
 'delete_event_confirm_timed': 'Delete the event from calendar {calendar}: {date} at {time} {title}?',
 'delete_event_day_dialog_title': 'Choose the day of the event to delete',
 'delete_event_day_label': 'Choose the day for deleting events',
 'delete_event_dialog_title': 'Delete event',
 'delete_event_error_failed': 'Failed to delete the event. Press the “Details” button to learn more.',
 'delete_event_month_label': 'Choose the month for deleting events',
 'delete_event_multiple_partial_error': 'Deleted {deleted_count} events before the error occurred.',
 'delete_event_multiple_success': 'Deleted {deleted_count} events.',
 'delete_event_no_events': 'No events to delete for the selected day.',
 'delete_event_no_selection': 'No events were selected for deletion.',
 'delete_event_open_label': 'Delete',
 'delete_event_scope_dialog_title': 'Recurring event deletion',
 'delete_event_scope_label': 'This event belongs to a recurring series. Choose what you want to delete.',
 'delete_event_scope_bulk_label': 'One or more selected events belong to a recurring series. Choose how to delete recurring events in this selection.',
 'delete_event_select_dialog_title': 'Choose an event to delete',
 'delete_event_select_label': 'Events. Use space to select or unselect, then press Tab to move to the Delete button.',
 'delete_event_success_all_day_range': 'Deleted the event from calendar {calendar}: from {start_date} to {end_date} '
                                       '{title}',
 'delete_event_success_all_day_single': 'Deleted the event from calendar {calendar}: {date} {title}',
 'delete_event_success_timed': 'Deleted the event from calendar {calendar}: {date} at {time} {title}',
 'delete_recurrence_success_daily': 'Deleted recurring event: daily from {date}',
 'delete_recurrence_success_daily_timed': 'Deleted recurring event: daily from {date} at {time}',
 'delete_recurrence_success_monthly': 'Deleted recurring event: monthly from {date}',
 'delete_recurrence_success_monthly_timed': 'Deleted recurring event: monthly from {date} at {time}',
 'delete_recurrence_success_weekly': 'Deleted recurring event: weekly from {date}',
 'delete_recurrence_success_weekly_timed': 'Deleted recurring event: weekly from {date} at {time}',
 'delete_recurrence_success_yearly': 'Deleted recurring event: yearly from {date}',
 'delete_recurrence_success_yearly_timed': 'Deleted recurring event: yearly from {date} at {time}',
 'deselect_all_label': 'Deselect all',
 'dialog_cancel': 'Cancel',
 'dialog_ok': 'OK',
 'edit_event_day_dialog_title': 'Choose the day of the event to edit',
 'edit_event_day_label': 'Choose the day for editing events',
 'edit_event_dialog_title': 'Edit event',
 'edit_event_error_failed': 'Failed to update the event. Press the “Details” button to learn more.',
 'edit_event_month_label': 'Choose the month for editing events',
 'edit_event_no_events': 'No events to edit for the selected day.',
 'edit_event_open_label': 'Edit',
 'edit_event_save_label': 'Save',
 'edit_event_scope_dialog_title': 'Recurring event editing',
 'edit_event_scope_label': 'This event belongs to a recurring series. Choose what you want to edit.',
 'edit_event_select_dialog_title': 'Choose an event to edit',
 'edit_event_select_label': 'Events',
 'edit_event_success_all_day_range': 'Updated the event in calendar {calendar}: from {start_date} to {end_date} '
                                     '{title}',
 'edit_event_success_all_day_single': 'Updated the event in calendar {calendar}: {date} {title}',
 'edit_event_success_timed': 'Updated the event in calendar {calendar}: {date} at {time} {title}',
 'edit_recurrence_success_daily': 'Updated recurring event: daily from {date}',
 'edit_recurrence_success_daily_timed': 'Updated recurring event: daily from {date} at {time}',
 'edit_recurrence_success_monthly': 'Updated recurring event: monthly from {date}',
 'edit_recurrence_success_monthly_timed': 'Updated recurring event: monthly from {date} at {time}',
 'edit_recurrence_success_weekly': 'Updated recurring event: weekly from {date}',
 'edit_recurrence_success_weekly_timed': 'Updated recurring event: weekly from {date} at {time}',
 'edit_recurrence_success_yearly': 'Updated recurring event: yearly from {date}',
 'edit_recurrence_success_yearly_timed': 'Updated recurring event: yearly from {date} at {time}',
 'error_details_open_failed': 'Could not open the error details file.',
 'error_dialog_close': 'Close',
 'error_dialog_details': 'Details',
 'error_dialog_title': 'Event operation error',
 'events_fetch_failed': 'Could not fetch events.',
 'few_events_prefix': '{date}. {count} events.',
 'googleauth_import_error_title': 'Error',
 'helper_calendar_list_error': 'Could not fetch the calendar list.',
 'helper_delete_event_error': 'Could not delete the event.',
 'helper_event_list_for_edit_error': 'Could not fetch event list for editing.',
 'helper_events_error': 'Could not fetch calendar events.',
 'helper_fetched_calendars': 'Fetched {count} calendars.',
 'helper_fetched_events': 'Fetched {count} events.',
 'helper_invalid_days_ahead': 'Invalid days_ahead parameter.',
 'helper_missing_days_ahead': 'Missing days_ahead parameter.',
 'helper_not_logged_in': 'You are not signed in.',
 'helper_search_events_error': 'Could not search calendar events.',
 'helper_service_error': 'Could not start Google Calendar API.',
 'helper_update_event_error': 'Could not update the event.',
 'import_error_googleauth': 'googleAuth import error: {error}',
 'import_error_modules': 'Module import error: {error}',
 'import_error_settings': 'settings import error: {error}',
 'in_progress': 'until {end}, {summary} in progress{calendar_label}',
 'login_cancelled_text': 'Google sign-in has been cancelled.',
 'login_cancelled_title': 'Sign-in cancelled',
 'login_dialog_text': 'After you press OK, your default browser will open. When sign-in is complete, open the addon '
                      'layer again and press 0.',
 'login_dialog_title': 'Starting Google sign-in',
 'login_failed_text': 'Unable to complete Google sign-in.',
 'login_failed_title': 'Sign-in failed',
 'login_in_progress_text': 'Complete sign-in in your browser, then open the addon layer and press 0 again.',
 'login_in_progress_title': 'Sign-in in progress',
 'login_required_title': 'Sign-in required',
 'login_status_signed_in': 'You are signed in to Google Calendar.',
 'login_status_title': 'Sign-in status',
 'many_events_prefix': '{date}. {count} events.',
 'missing_client_secret': 'Missing client_secret.json file.',
 'missing_client_secret_title': 'Missing file',
 'mode_full': 'Full mode',
 'mode_short': 'Short mode',
 'module_import_error_title': 'Error',
 'multi_select_check_hint': 'Space toggles selection. Use Select all or Deselect all to quickly change the whole '
                            'selection.',
 'network_operation_in_progress': 'Another Google Calendar Manager operation is already in progress.',
 'no_calendars_available': 'No calendars available.',
 'no_calendars_selected': 'No calendars selected. The primary calendar will be used.',
 'no_data': 'No data.',
 'no_name': 'unnamed',
 'no_title': 'untitled',
 'not_logged_in_use_zero': 'You are not signed in. Open the Google Calendar Manager layer and press 0 to start Google '
                           'sign-in.',
 'one_event_prefix': '{date}. One event.',
 'pick_day_events_day_label': 'Choose the day for showing events',
 'pick_day_events_dialog_title': 'Choose the day of events to show',
 'pick_day_events_month_label': 'Choose the month for showing events',
 'pick_day_events_other_day_label': 'Choose another day',
 'pick_day_events_results_title': 'Events for the selected day',
 'primary_suffix': ' (primary)',
 'recurrence_scope_entire_series': 'Entire series',
 'recurrence_scope_this_occurrence': 'Only this occurrence',
 'recurring_suffix_daily': ', recurring daily',
 'recurring_suffix_monthly': ', recurring monthly',
 'recurring_suffix_weekly': ', recurring weekly',
 'recurring_suffix_yearly': ', recurring yearly',
 'saved_calendars': 'Saved calendars: {names}',
 'script_add_event_desc': 'Add a new event to Google Calendar',
 'script_day_after_desc': 'Read Google Calendar events for the day after tomorrow',
 'script_day_plus_3_desc': 'Read Google Calendar events for 3 days from now',
 'script_day_plus_4_desc': 'Read Google Calendar events for 4 days from now',
 'script_day_plus_5_desc': 'Read Google Calendar events for 5 days from now',
 'script_day_plus_6_desc': 'Read Google Calendar events for 6 days from now',
 'script_delete_event_desc': 'Delete an event from Google Calendar',
 'script_edit_event_desc': 'Edit an event in Google Calendar',
 'script_layer_desc': 'Opens the Google Calendar Manager layer',
 'script_login_desc': 'Sign in to Google Calendar or check sign-in status',
 'script_pick_day_preview_desc': 'Show events for a selected day',
 'script_search_events_desc': 'Search Google Calendar events',
 'script_select_calendars_desc': 'Choose Google Calendars to read',
 'script_today_desc': "Read today's Google Calendar events",
 'script_toggle_mode_desc': 'Toggle speech mode',
 'script_tomorrow_desc': "Read tomorrow's Google Calendar events",
 'search_events_custom_range_title': 'Custom search range',
 'search_events_dialog_title': 'Search events',
 'search_events_end_day_label': 'End day',
 'search_events_end_month_label': 'End month',
 'search_events_error_end_before_start': 'End date cannot be earlier than start date.',
 'search_events_error_end_day_required': 'Enter a valid end day.',
 'search_events_error_end_month_required': 'Enter a valid end month.',
 'search_events_error_invalid_end_date': 'Enter a valid end date.',
 'search_events_error_invalid_start_date': 'Enter a valid start date.',
 'search_events_error_query_required': 'Enter search text.',
 'search_events_error_start_day_required': 'Enter a valid start day.',
 'search_events_error_start_month_required': 'Enter a valid start month.',
 'search_events_new_search_label': 'New search',
 'search_events_no_results': 'No matching events found for "{query}" from {start_date} to {end_date}.',
 'search_events_open_label': 'Search',
 'search_events_query_label': 'Search text',
 'search_events_range_12_months': 'Next 12 months',
 'search_events_range_1_month': 'Next month',
 'search_events_range_3_months': 'Next 3 months',
 'search_events_range_6_months': 'Next 6 months',
 'search_events_range_custom': 'Custom range',
 'search_events_range_label': 'Search range',
 'search_events_results_intro': 'Search results for "{query}". Found {count} matching events from {start_date} to '
                                '{end_date}.',
 'search_events_results_intro_one': 'Search results for "{query}". Found one matching event from {start_date} to '
                                    '{end_date}.',
 'search_events_results_title': 'Search results',
 'search_events_start_day_label': 'Start day',
 'search_events_start_month_label': 'Start month',
 'select_all_label': 'Select all',
 'selection_all_cleared': 'All events deselected.',
 'selection_all_selected': 'All events selected.',
 'selection_cancelled': 'Calendar selection cancelled.',
 'shortcuts_checkbox_label': 'Show keyboard shortcuts',
 'shortcuts_dialog_text': 'NVDA+Shift+G — Google Calendar Manager layer\n'
                          '0 — sign in or sign-in status\n'
                          "1 — today's events\n"
                          "2 — tomorrow's events\n"
                          '3 — events for the day after tomorrow\n'
                          '4 — events in 3 days\n'
                          '5 — events in 4 days\n'
                          '6 — events in 5 days\n'
                          '7 — events in 6 days\n'
                          '8 — switch reading mode\n'
                          '9 — choose calendars\n'
                          'N — add event\n'
                          'E — edit event\n'
                          'U — delete event\n'
                          'P — show events for a selected day\n'
                          'S — search events\n'
                          'H — show shortcut help',
 'shortcuts_dialog_title': 'Keyboard shortcuts',
 'time_range': '{start} to {end}, {summary}{calendar_label}',
 'time_start_only': '{start}, {summary}{calendar_label}',
 'unchecked_state': 'not selected'}

POLISH_MESSAGES = {'add_event_all_day_label': 'Wydarzenie całodniowe',
 'add_event_calendar_label': 'Kalendarz',
 'add_event_day_label': 'Dzień początkowy',
 'add_event_dialog_title': 'Dodaj wydarzenie',
 'add_event_end_day_label': 'Dzień końcowy',
 'add_event_end_hour_label': 'Godzina zakończenia, godziny',
 'add_event_end_minute_label': 'Godzina zakończenia, minuty',
 'add_event_end_month_label': 'Miesiąc końcowy',
 'add_event_error_calendar_required': 'Wybierz kalendarz.',
 'add_event_error_day_required': 'Wpisz poprawny dzień początkowy.',
 'add_event_error_end_before_start': 'Godzina zakończenia musi być późniejsza niż godzina rozpoczęcia.',
 'add_event_error_end_date_before_start': 'Data końcowa nie może być wcześniejsza niż data początkowa.',
 'add_event_error_end_day_required': 'Wpisz poprawny dzień końcowy.',
 'add_event_error_end_month_required': 'Wpisz poprawny miesiąc końcowy.',
 'add_event_error_end_time': 'Wpisz poprawną godzinę zakończenia.',
 'add_event_error_failed': 'Nie udało się dodać wydarzenia. Naciśnij przycisk „Szczegóły”, by dowiedzieć się więcej.',
 'add_event_error_invalid_date': 'Wpisz poprawną datę początkową.',
 'add_event_error_invalid_end_date': 'Wpisz poprawną datę końcową.',
 'add_event_error_month_required': 'Wpisz poprawny miesiąc początkowy.',
 'add_event_error_recurrence_end_before_start': 'Data końca cyklu nie może być wcześniejsza niż data początkowa.',
 'add_event_error_recurrence_end_day_required': 'Wpisz poprawny dzień końca cyklu.',
 'add_event_error_recurrence_end_month_required': 'Wpisz poprawny miesiąc końca cyklu.',
 'add_event_error_recurrence_end_year_required': 'Wpisz poprawny rok końca cyklu.',
 'add_event_error_recurrence_end_year_range': 'Wpisz rok końca cyklu z zakresu od {min_year} do {max_year}.',
 'add_event_error_recurrence_invalid_end_date': 'Wpisz poprawną datę końca cyklu.',
 'add_event_error_start_time': 'Wpisz poprawną godzinę rozpoczęcia.',
 'add_event_error_title_required': 'Wpisz tytuł wydarzenia.',
 'add_event_location_label': 'Lokalizacja',
 'add_event_open_label': 'Dodaj wydarzenie',
 'add_event_month_label': 'Miesiąc początkowy',
 'add_event_recurrence_end_day_label': 'Dzień końca cyklu',
 'add_event_recurrence_end_month_label': 'Miesiąc końca cyklu',
 'add_event_recurrence_end_year_label': 'Rok końca cyklu',
 'add_event_recurrence_label': 'Cykliczność',
 'add_event_recurrence_no_end_label': 'Bez daty końca cyklu',
 'add_event_start_hour_label': 'Godzina rozpoczęcia, godziny',
 'add_event_start_minute_label': 'Godzina rozpoczęcia, minuty',
 'add_event_success_all_day_range': 'Dodano nowe wydarzenie w kalendarzu {calendar}: od {start_date} do {end_date} '
                                    '{title}',
 'add_event_success_all_day_single': 'Dodano nowe wydarzenie w kalendarzu {calendar}: {date} {title}',
 'add_event_success_timed': 'Dodano nowe wydarzenie w kalendarzu {calendar}: {date} o {time} {title}',
 'add_event_title_label': 'Tytuł',
 'add_recurrence_success_daily': 'Dodano wydarzenie cykliczne: codziennie od {date}',
 'add_recurrence_success_daily_timed': 'Dodano wydarzenie cykliczne: codziennie od {date} o {time}',
 'add_recurrence_success_monthly': 'Dodano wydarzenie cykliczne: co miesiąc od {date}',
 'add_recurrence_success_monthly_timed': 'Dodano wydarzenie cykliczne: co miesiąc od {date} o {time}',
 'add_recurrence_success_weekly': 'Dodano wydarzenie cykliczne: co tydzień od {date}',
 'add_recurrence_success_weekly_timed': 'Dodano wydarzenie cykliczne: co tydzień od {date} o {time}',
 'add_recurrence_success_yearly': 'Dodano wydarzenie cykliczne: co rok od {date}',
 'add_recurrence_success_yearly_timed': 'Dodano wydarzenie cykliczne: co rok od {date} o {time}',
 'all_day_full': 'wydarzenie całodniowe, {summary}{calendar_label}',
 'all_day_range_short': 'całodniowe, {range_text}, {summary}',
 'all_day_short': 'całodniowe, {summary}{calendar_label}',
 'busy_adding_event': 'Dodaję wydarzenie do kalendarza...',
 'busy_deleting_event': 'Usuwam wydarzenie z kalendarza...',
 'busy_deleting_events': 'Usuwam wydarzenia z kalendarza...',
 'busy_fetching_calendars': 'Pobieram listę kalendarzy...',
 'busy_fetching_events': 'Pobieram wydarzenia z kalendarza...',
 'busy_fetching_events_for_selected_day': 'Pobieram wydarzenia z wybranego dnia...',
 'busy_fetching_events_to_delete': 'Pobieram wydarzenia do usunięcia...',
 'busy_fetching_events_to_edit': 'Pobieram wydarzenia do edycji...',
 'busy_saving_event_changes': 'Zapisuję zmiany w kalendarzu...',
 'busy_searching_events': 'Szukam wydarzeń w kalendarzu...',
 'calendar_dialog_info': 'Wybierz kalendarze do odczytu. Jeśli nic nie zaznaczysz, użyty będzie kalendarz główny.',
 'calendar_dialog_title': 'Wybór kalendarzy Google',
 'calendar_list_empty_title': 'Kalendarze',
 'calendar_list_failed_title': 'Błąd kalendarzy',
 'calendar_list_fetch_failed': 'Nie udało się pobrać listy kalendarzy.',
 'calendar_prefix': 'kalendarz {name}',
 'checked_state': 'zaznaczone',
 'date_no_events': '{date}. Brak wydarzeń.',
 'date_range': '{start} do {end}',
 'delete_event_confirm_all_day_range': 'Usunąć wydarzenie z kalendarza {calendar}: od {start_date} do {end_date} '
                                       '{title}?',
 'delete_event_confirm_all_day_single': 'Usunąć wydarzenie z kalendarza {calendar}: {date} {title}?',
 'delete_event_confirm_delete_label': 'Usuń',
 'delete_event_confirm_instance_all_day_range': 'Usunąć tylko to wystąpienie z kalendarza {calendar}: od {start_date} '
                                                'do {end_date} {title}?',
 'delete_event_confirm_instance_all_day_single': 'Usunąć tylko to wystąpienie z kalendarza {calendar}: {date} {title}?',
 'delete_event_confirm_instance_timed': 'Usunąć tylko to wystąpienie z kalendarza {calendar}: {date} o {time} {title}?',
 'delete_event_confirm_multiple_intro': 'Usunąć {count} wybranych wydarzeń?',
 'delete_event_confirm_recurrence_daily': 'Usunąć wydarzenie cykliczne: codziennie od {date}?',
 'delete_event_confirm_recurrence_daily_timed': 'Usunąć wydarzenie cykliczne: codziennie od {date} o {time}?',
 'delete_event_confirm_recurrence_monthly': 'Usunąć wydarzenie cykliczne: co miesiąc od {date}?',
 'delete_event_confirm_recurrence_monthly_timed': 'Usunąć wydarzenie cykliczne: co miesiąc od {date} o {time}?',
 'delete_event_confirm_recurrence_weekly': 'Usunąć wydarzenie cykliczne: co tydzień od {date}?',
 'delete_event_confirm_recurrence_weekly_timed': 'Usunąć wydarzenie cykliczne: co tydzień od {date} o {time}?',
 'delete_event_confirm_recurrence_yearly': 'Usunąć wydarzenie cykliczne: co rok od {date}?',
 'delete_event_confirm_recurrence_yearly_timed': 'Usunąć wydarzenie cykliczne: co rok od {date} o {time}?',
 'delete_event_confirm_timed': 'Usunąć wydarzenie z kalendarza {calendar}: {date} o {time} {title}?',
 'delete_event_day_dialog_title': 'Wybierz dzień wydarzenia do usunięcia',
 'delete_event_day_label': 'Wybierz dzień do usunięcia wydarzeń',
 'delete_event_dialog_title': 'Usuń wydarzenie',
 'delete_event_error_failed': 'Nie udało się usunąć wydarzenia. Naciśnij przycisk „Szczegóły”, by dowiedzieć się '
                              'więcej.',
 'delete_event_month_label': 'Wybierz miesiąc do usunięcia wydarzeń',
 'delete_event_multiple_partial_error': 'Usunięto {deleted_count} wydarzeń przed wystąpieniem błędu.',
 'delete_event_multiple_success': 'Usunięto {deleted_count} wydarzeń.',
 'delete_event_no_events': 'Brak wydarzeń do usunięcia dla wybranego dnia.',
 'delete_event_no_selection': 'Nie wybrano żadnych wydarzeń do usunięcia.',
 'delete_event_open_label': 'Usuń',
 'delete_event_scope_dialog_title': 'Usuwanie wydarzenia cyklicznego',
 'delete_event_scope_label': 'To wydarzenie należy do cyklu. Wybierz, co chcesz usunąć.',
 'delete_event_scope_bulk_label': 'Jedno lub więcej zaznaczonych wydarzeń należy do cyklu. Wybierz, jak usunąć wydarzenia cykliczne w tym zaznaczeniu.',
 'delete_event_select_dialog_title': 'Wybierz wydarzenie do usunięcia',
 'delete_event_select_label': 'Wydarzenia. Użyj spacji, aby zaznaczyć lub odznaczyć, a następnie tabulatorem przejdź '
                              'do przycisku Usuń.',
 'delete_event_success_all_day_range': 'Usunięto wydarzenie z kalendarza {calendar}: od {start_date} do {end_date} '
                                       '{title}',
 'delete_event_success_all_day_single': 'Usunięto wydarzenie z kalendarza {calendar}: {date} {title}',
 'delete_event_success_timed': 'Usunięto wydarzenie z kalendarza {calendar}: {date} o {time} {title}',
 'delete_recurrence_success_daily': 'Usunięto wydarzenie cykliczne: codziennie od {date}',
 'delete_recurrence_success_daily_timed': 'Usunięto wydarzenie cykliczne: codziennie od {date} o {time}',
 'delete_recurrence_success_monthly': 'Usunięto wydarzenie cykliczne: co miesiąc od {date}',
 'delete_recurrence_success_monthly_timed': 'Usunięto wydarzenie cykliczne: co miesiąc od {date} o {time}',
 'delete_recurrence_success_weekly': 'Usunięto wydarzenie cykliczne: co tydzień od {date}',
 'delete_recurrence_success_weekly_timed': 'Usunięto wydarzenie cykliczne: co tydzień od {date} o {time}',
 'delete_recurrence_success_yearly': 'Usunięto wydarzenie cykliczne: co rok od {date}',
 'delete_recurrence_success_yearly_timed': 'Usunięto wydarzenie cykliczne: co rok od {date} o {time}',
 'deselect_all_label': 'Odznacz wszystko',
 'dialog_cancel': 'Anuluj',
 'dialog_ok': 'OK',
 'edit_event_day_dialog_title': 'Wybierz dzień wydarzenia do edycji',
 'edit_event_day_label': 'Wybierz dzień do edycji wydarzeń',
 'edit_event_dialog_title': 'Edytuj wydarzenie',
 'edit_event_error_failed': 'Nie udało się zaktualizować wydarzenia. Naciśnij przycisk „Szczegóły”, by dowiedzieć się '
                            'więcej.',
 'edit_event_month_label': 'Wybierz miesiąc do edycji wydarzeń',
 'edit_event_no_events': 'Brak wydarzeń do edycji dla wybranego dnia.',
 'edit_event_open_label': 'Edytuj',
 'edit_event_save_label': 'Zapisz',
 'edit_event_scope_dialog_title': 'Edycja wydarzenia cyklicznego',
 'edit_event_scope_label': 'To wydarzenie należy do cyklu. Wybierz, co chcesz edytować.',
 'edit_event_select_dialog_title': 'Wybierz wydarzenie do edycji',
 'edit_event_select_label': 'Wydarzenia',
 'edit_event_success_all_day_range': 'Zaktualizowano wydarzenie w kalendarzu {calendar}: od {start_date} do {end_date} '
                                     '{title}',
 'edit_event_success_all_day_single': 'Zaktualizowano wydarzenie w kalendarzu {calendar}: {date} {title}',
 'edit_event_success_timed': 'Zaktualizowano wydarzenie w kalendarzu {calendar}: {date} o {time} {title}',
 'edit_recurrence_success_daily': 'Zaktualizowano wydarzenie cykliczne: codziennie od {date}',
 'edit_recurrence_success_daily_timed': 'Zaktualizowano wydarzenie cykliczne: codziennie od {date} o {time}',
 'edit_recurrence_success_monthly': 'Zaktualizowano wydarzenie cykliczne: co miesiąc od {date}',
 'edit_recurrence_success_monthly_timed': 'Zaktualizowano wydarzenie cykliczne: co miesiąc od {date} o {time}',
 'edit_recurrence_success_weekly': 'Zaktualizowano wydarzenie cykliczne: co tydzień od {date}',
 'edit_recurrence_success_weekly_timed': 'Zaktualizowano wydarzenie cykliczne: co tydzień od {date} o {time}',
 'edit_recurrence_success_yearly': 'Zaktualizowano wydarzenie cykliczne: co rok od {date}',
 'edit_recurrence_success_yearly_timed': 'Zaktualizowano wydarzenie cykliczne: co rok od {date} o {time}',
 'error_details_open_failed': 'Nie udało się otworzyć pliku ze szczegółami błędu.',
 'error_dialog_close': 'Zamknij',
 'error_dialog_details': 'Szczegóły',
 'error_dialog_title': 'Błąd operacji na wydarzeniu',
 'events_fetch_failed': 'Nie udało się pobrać wydarzeń.',
 'few_events_prefix': '{date}. {count} wydarzenia.',
 'googleauth_import_error_title': 'Błąd',
 'helper_calendar_list_error': 'Nie udało się pobrać listy kalendarzy.',
 'helper_delete_event_error': 'Nie udało się usunąć wydarzenia.',
 'helper_event_list_for_edit_error': 'Nie udało się pobrać listy wydarzeń do edycji.',
 'helper_events_error': 'Nie udało się pobrać wydarzeń z kalendarza.',
 'helper_fetched_calendars': 'Pobrano {count} kalendarzy.',
 'helper_fetched_events': 'Pobrano {count} wydarzeń.',
 'helper_invalid_days_ahead': 'Nieprawidłowy parametr days_ahead.',
 'helper_missing_days_ahead': 'Brak parametru days_ahead.',
 'helper_not_logged_in': 'Nie jesteś zalogowany.',
 'helper_search_events_error': 'Nie udało się wyszukać wydarzeń.',
 'helper_service_error': 'Nie udało się uruchomić Google Calendar API.',
 'helper_update_event_error': 'Nie udało się zaktualizować wydarzenia.',
 'import_error_googleauth': 'Błąd importu googleAuth: {error}',
 'import_error_modules': 'Błąd importu modułów: {error}',
 'import_error_settings': 'Błąd importu settings: {error}',
 'in_progress': 'do {end}, trwa {summary}{calendar_label}',
 'login_cancelled_text': 'Logowanie do Google zostało anulowane.',
 'login_cancelled_title': 'Logowanie anulowane',
 'login_dialog_text': 'Po naciśnięciu OK otworzy się domyślna przeglądarka. Po ukończeniu logowania uruchom warstwę '
                      'dodatku ponownie i naciśnij 0.',
 'login_dialog_title': 'Rozpoczynasz logowanie Google',
 'login_failed_text': 'Nie udało się zakończyć logowania do Google.',
 'login_failed_title': 'Logowanie nieudane',
 'login_in_progress_text': 'Dokończ logowanie w przeglądarce, a następnie uruchom warstwę dodatku i naciśnij 0 '
                           'ponownie.',
 'login_in_progress_title': 'Logowanie w toku',
 'login_required_title': 'Logowanie wymagane',
 'login_status_signed_in': 'Jesteś zalogowany do Google Calendar.',
 'login_status_title': 'Status logowania',
 'many_events_prefix': '{date}. {count} wydarzeń.',
 'missing_client_secret': 'Brak pliku client_secret.json.',
 'missing_client_secret_title': 'Brak pliku',
 'mode_full': 'Tryb rozszerzony',
 'mode_short': 'Tryb prosty',
 'module_import_error_title': 'Błąd',
 'multi_select_check_hint': 'Spacja przełącza zaznaczenie. Użyj przycisków Zaznacz wszystko lub Odznacz wszystko, aby '
                            'szybko zmienić cały wybór.',
 'network_operation_in_progress': 'Inna operacja Google Calendar Manager jest już w toku.',
 'no_calendars_available': 'Brak dostępnych kalendarzy.',
 'no_calendars_selected': 'Nie wybrano żadnych kalendarzy. Odczyt będzie używał kalendarza głównego.',
 'no_data': 'Brak danych.',
 'no_name': 'bez nazwy',
 'no_title': 'bez tytułu',
 'not_logged_in_use_zero': 'Nie jesteś zalogowany. Użyj warstwy Google Calendar Manager i naciśnij 0, aby rozpocząć '
                           'logowanie.',
 'one_event_prefix': '{date}. Jedno wydarzenie.',
 'pick_day_events_day_label': 'Wybierz dzień do pokazania wydarzeń',
 'pick_day_events_dialog_title': 'Wybierz dzień wydarzeń do pokazania',
 'pick_day_events_month_label': 'Wybierz miesiąc do pokazania wydarzeń',
 'pick_day_events_other_day_label': 'Wybierz inny dzień',
 'pick_day_events_results_title': 'Wydarzenia dla wybranego dnia',
 'primary_suffix': ' (główny)',
 'recurrence_scope_entire_series': 'Cały cykl',
 'recurrence_scope_this_occurrence': 'Tylko to wystąpienie',
 'recurring_suffix_daily': ', cykliczne codziennie',
 'recurring_suffix_monthly': ', cykliczne co miesiąc',
 'recurring_suffix_weekly': ', cykliczne co tydzień',
 'recurring_suffix_yearly': ', cykliczne co rok',
 'saved_calendars': 'Zapisano kalendarze: {names}',
 'script_add_event_desc': 'Dodaj nowe wydarzenie do Google Calendar',
 'script_day_after_desc': 'Odczyt wydarzeń na pojutrze z Google Calendar',
 'script_day_plus_3_desc': 'Odczyt wydarzeń za 3 dni z Google Calendar',
 'script_day_plus_4_desc': 'Odczyt wydarzeń za 4 dni z Google Calendar',
 'script_day_plus_5_desc': 'Odczyt wydarzeń za 5 dni z Google Calendar',
 'script_day_plus_6_desc': 'Odczyt wydarzeń za 6 dni z Google Calendar',
 'script_delete_event_desc': 'Usuń wydarzenie z Google Calendar',
 'script_edit_event_desc': 'Edytuj wydarzenie w Google Calendar',
 'script_layer_desc': 'Uruchamia warstwę Google Calendar Manager',
 'script_login_desc': 'Logowanie do Google Calendar lub sprawdzenie stanu logowania',
 'script_pick_day_preview_desc': 'Pokaż wydarzenia dla wybranego dnia',
 'script_search_events_desc': 'Wyszukaj wydarzenia w Google Calendar',
 'script_select_calendars_desc': 'Wybierz kalendarze Google do odczytu',
 'script_today_desc': 'Odczyt wydarzeń na dziś z Google Calendar',
 'script_toggle_mode_desc': 'Przełącz tryb odczytu',
 'script_tomorrow_desc': 'Odczyt wydarzeń na jutro z Google Calendar',
 'search_events_custom_range_title': 'Własny zakres wyszukiwania',
 'search_events_dialog_title': 'Wyszukaj wydarzenia',
 'search_events_end_day_label': 'Dzień końcowy',
 'search_events_end_month_label': 'Miesiąc końcowy',
 'search_events_error_end_before_start': 'Data końcowa nie może być wcześniejsza niż data początkowa.',
 'search_events_error_end_day_required': 'Wpisz poprawny dzień końcowy.',
 'search_events_error_end_month_required': 'Wpisz poprawny miesiąc końcowy.',
 'search_events_error_invalid_end_date': 'Wpisz poprawną datę końcową.',
 'search_events_error_invalid_start_date': 'Wpisz poprawną datę początkową.',
 'search_events_error_query_required': 'Wpisz szukany tekst.',
 'search_events_error_start_day_required': 'Wpisz poprawny dzień początkowy.',
 'search_events_error_start_month_required': 'Wpisz poprawny miesiąc początkowy.',
 'search_events_new_search_label': 'Nowe wyszukiwanie',
 'search_events_no_results': 'Nie znaleziono wydarzeń pasujących do „{query}” od {start_date} do {end_date}.',
 'search_events_open_label': 'Szukaj',
 'search_events_query_label': 'Szukany tekst',
 'search_events_range_12_months': 'Najbliższe 12 miesięcy',
 'search_events_range_1_month': 'Najbliższy miesiąc',
 'search_events_range_3_months': 'Najbliższe 3 miesiące',
 'search_events_range_6_months': 'Najbliższe 6 miesięcy',
 'search_events_range_custom': 'Własny zakres',
 'search_events_range_label': 'Zakres wyszukiwania',
 'search_events_results_intro': 'Wyniki wyszukiwania dla „{query}”. Znaleziono {count} pasujących wydarzeń od '
                                '{start_date} do {end_date}.',
 'search_events_results_intro_one': 'Wyniki wyszukiwania dla „{query}”. Znaleziono jedno pasujące wydarzenie od '
                                    '{start_date} do {end_date}.',
 'search_events_results_title': 'Wyniki wyszukiwania',
 'search_events_start_day_label': 'Dzień początkowy',
 'search_events_start_month_label': 'Miesiąc początkowy',
 'select_all_label': 'Zaznacz wszystko',
 'selection_all_cleared': 'Odznaczono wszystkie wydarzenia.',
 'selection_all_selected': 'Zaznaczono wszystkie wydarzenia.',
 'selection_cancelled': 'Anulowano wybór kalendarzy.',
 'shortcuts_checkbox_label': 'Pokaż skróty klawiszowe',
 'shortcuts_dialog_text': 'NVDA+Shift+G — warstwa Google Calendar Manager\n'
                          '0 — logowanie lub status logowania\n'
                          '1 — wydarzenia na dziś\n'
                          '2 — wydarzenia na jutro\n'
                          '3 — wydarzenia na pojutrze\n'
                          '4 — wydarzenia za 3 dni\n'
                          '5 — wydarzenia za 4 dni\n'
                          '6 — wydarzenia za 5 dni\n'
                          '7 — wydarzenia za 6 dni\n'
                          '8 — przełącz tryb odczytu\n'
                          '9 — wybór kalendarzy\n'
                          'N — dodaj wydarzenie\n'
                          'E — edytuj wydarzenie\n'
                          'U — usuń wydarzenie\n'
                          'P — pokaż wydarzenia dla wybranego dnia\n'
                          'S — wyszukaj wydarzenia\n'
                          'H — pokaż pomoc ze skrótami',
 'shortcuts_dialog_title': 'Skróty klawiszowe',
 'time_range': '{start} do {end}, {summary}{calendar_label}',
 'time_start_only': '{start}, {summary}{calendar_label}',
 'unchecked_state': 'niezaznaczone'}

_TRANSLATOR_CACHE = {}


def normalize_lang(lang):
    if not lang:
        return "en"
    lang = str(lang).strip().lower().replace("-", "_")
    if lang == "windows":
        lang = _get_system_locale()
    if lang.startswith("pl"):
        return "pl"
    return "en"


def _get_system_locale():
    for getter in (
        lambda: locale.getlocale()[0],
        lambda: locale.getdefaultlocale()[0],
    ):
        try:
            value = getter()
            if value:
                return value
        except Exception:
            pass
    for env_name in ("LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG"):
        value = os.environ.get(env_name, "").strip()
        if value:
            return value
    return "en"


def get_runtime_language(fallback="en"):
    env_lang = os.environ.get("GCR_LANG", "").strip()
    if env_lang:
        return normalize_lang(env_lang)

    try:
        if languageHandler is not None:
            nvda_lang = languageHandler.getLanguage()
            if nvda_lang:
                return normalize_lang(nvda_lang)
    except Exception:
        pass

    return normalize_lang(fallback)


def _locale_dir():
    # i18n.py lives in: addonRoot/globalPlugins/googleCalendarManager/i18n.py
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "locale"))


def _get_translator(lang):
    lang = normalize_lang(lang)
    if lang == "en":
        return None
    if lang not in _TRANSLATOR_CACHE:
        try:
            _TRANSLATOR_CACHE[lang] = gettext.translation(
                "nvda",
                localedir=_locale_dir(),
                languages=[lang],
                fallback=True,
            )
        except Exception:
            _TRANSLATOR_CACHE[lang] = gettext.NullTranslations()
    return _TRANSLATOR_CACHE[lang]


def t(key, lang=None, **kwargs):
    if lang is None:
        lang = get_runtime_language("en")
    lang = normalize_lang(lang)

    text = ENGLISH_MESSAGES.get(key, key)
    if lang != "en":
        translator = _get_translator(lang)
        try:
            translated = translator.gettext(text) if translator is not None else text
        except Exception:
            translated = text
        if translated == text and lang == "pl":
            translated = POLISH_MESSAGES.get(key, translated)
        text = translated

    if kwargs:
        return text.format(**kwargs)
    return text


def format_date_for_language(target_date, lang=None):
    lang = normalize_lang(lang or get_runtime_language("en"))
    month = MONTHS[lang][target_date.month - 1]

    if lang == "pl":
        return f"{target_date.day} {month}"
    return f"{month} {target_date.day}"


def format_day_date_for_language(target_date, lang=None):
    lang = normalize_lang(lang or get_runtime_language("en"))
    weekday = WEEKDAYS[lang][target_date.weekday()]
    date_text = format_date_for_language(target_date, lang)
    return f"{weekday}, {date_text}"


def get_recurrence_choice_labels(lang=None):
    lang = normalize_lang(lang or get_runtime_language("en"))
    return RECURRENCE_CHOICES.get(lang, RECURRENCE_CHOICES["en"])


def recurrence_mode_to_index(mode):
    mapping = {
        "none": 0,
        "daily": 1,
        "weekly": 2,
        "monthly": 3,
        "yearly": 4,
    }
    return mapping.get(str(mode or "").strip().lower(), 0)


def recurrence_index_to_mode(index):
    mapping = {
        0: "none",
        1: "daily",
        2: "weekly",
        3: "monthly",
        4: "yearly",
    }
    return mapping.get(int(index), "none")
