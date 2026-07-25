from globalPluginHandler import GlobalPlugin as BaseGlobalPlugin
import scriptHandler
import ui
import os
import sys
import json
import threading
import datetime
import calendar
import wx
import tones

from .i18n import (
    t,
    get_runtime_language,
    format_date_for_language,
    format_day_date_for_language,
    get_recurrence_choice_labels,
    recurrence_mode_to_index,
    recurrence_index_to_mode,
)
from .dialogs import (
    ReadOnlyMessageDialog,
    ConfirmDialog,
    CalendarSelectionDialog,
    AddEventDialog,
    ErrorDetailsDialog,
    EventDayDialog,
    EventSelectionDialog,
    DeleteEventConfirmDialog,
    DailyEventsResultDialog,
    SearchEventsDialog,
    SearchDateRangeDialog,
)

from .paths import (
    BASE_DIR,
    LIB_DIR,
    SETTINGS_PATH,
    ERROR_PATH,
    CREATE_ERROR_REPORT_PATH,
    UPDATE_ERROR_REPORT_PATH,
    DELETE_ERROR_REPORT_PATH,
    ensure_user_data_dir,
)

if LIB_DIR not in sys.path:
    sys.path.insert(0, LIB_DIR)


def get_ui_language():
    return get_runtime_language("en")


class GlobalPlugin(BaseGlobalPlugin):
    scriptCategory = "Google Calendar Manager"

    def __init__(self, *args, **kwargs):
        super(GlobalPlugin, self).__init__(*args, **kwargs)
        self._login_in_progress = False
        self._login_thread = None
        self._last_login_result = None
        self._login_lock = threading.Lock()
        self._network_lock = threading.Lock()
        self._network_in_progress = False
        self._layer_active = False
        self._dialog_focus_timers = []

    def _t(self, key, **kwargs):
        return t(key, get_ui_language(), **kwargs)

    def _get_dialog_parent(self):
        try:
            import gui
            parent = getattr(gui, "mainFrame", None)
            if parent is not None:
                return parent
        except Exception:
            pass
        return None

    def _run_pre_popup(self):
        try:
            import gui
            parent = getattr(gui, "mainFrame", None)
            if parent is not None and hasattr(parent, "prePopup"):
                parent.prePopup()
                return True
        except Exception:
            pass
        return False

    def _run_post_popup(self):
        try:
            import gui
            parent = getattr(gui, "mainFrame", None)
            if parent is not None and hasattr(parent, "postPopup"):
                parent.postPopup()
        except Exception:
            pass

    def _activate_dialog(self, dialog):
        try:
            dialog.Raise()
        except Exception:
            pass
        try:
            dialog.SetFocus()
        except Exception:
            pass

        focus_initial_control = getattr(dialog, "focus_initial_control", None)
        if callable(focus_initial_control):
            try:
                focus_initial_control()
            except Exception:
                pass

    def _schedule_dialog_activation(self, dialog):
        def activate():
            try:
                if dialog is None:
                    return
                if hasattr(dialog, "IsBeingDeleted") and dialog.IsBeingDeleted():
                    return
            except Exception:
                pass
            self._activate_dialog(dialog)

        try:
            wx.CallAfter(activate)
        except Exception:
            pass
        for delay in (80, 250):
            try:
                timer = wx.CallLater(delay, activate)
                self._dialog_focus_timers.append(timer)
            except Exception:
                pass

        try:
            self._dialog_focus_timers = [
                timer for timer in self._dialog_focus_timers
                if hasattr(timer, "IsRunning") and timer.IsRunning()
            ]
        except Exception:
            self._dialog_focus_timers = []

    def _show_modal_dialog(self, dialog):
        did_pre_popup = self._run_pre_popup()
        try:
            self._schedule_dialog_activation(dialog)
            return dialog.ShowModal()
        finally:
            if did_pre_popup:
                self._run_post_popup()

    def _start_network_task(self, busy_message, target, on_success, on_error=None, name="GCRNetworkThread"):
        with self._network_lock:
            if self._network_in_progress:
                ui.message(self._t("network_operation_in_progress"))
                return False
            self._network_in_progress = True

        if busy_message:
            ui.message(busy_message)

        def _finish_success(result):
            with self._network_lock:
                self._network_in_progress = False
            try:
                on_success(result)
            except Exception as e:
                self._show_message(str(e), "Google Calendar Manager")

        def _finish_error(error):
            with self._network_lock:
                self._network_in_progress = False
            if on_error is not None:
                try:
                    on_error(error)
                    return
                except Exception as e:
                    self._show_message(str(e), "Google Calendar Manager")
                    return
            self._show_message(str(error), "Google Calendar Manager")

        def _runner():
            try:
                result = target()
            except Exception as e:
                wx.CallAfter(_finish_error, e)
                return
            wx.CallAfter(_finish_success, result)

        thread = threading.Thread(target=_runner, name=name, daemon=True)
        thread.start()
        return True

    def _google_ready_or_error(self, googleAuth):
        if not googleAuth.has_client_secret():
            return {
                "ok": False,
                "text": self._t("missing_client_secret"),
                "title": self._t("missing_client_secret_title"),
            }

        if not googleAuth.is_logged_in():
            return {
                "ok": False,
                "text": self._t("not_logged_in_use_zero"),
                "title": self._t("login_required_title"),
            }

        return None

    def _play_layer_activation_sound(self):
        try:
            tones.beep(880, 80)
        except Exception:
            pass

    def _play_layer_command_sound(self):
        try:
            tones.beep(440, 180)
        except Exception:
            pass

    def _activate_layer(self):
        self._layer_active = True
        self._play_layer_activation_sound()
        ui.message("Google Calendar Manager")

    def _deactivate_layer(self):
        self._layer_active = False

    def _get_layer_script(self, gesture):
        key = getattr(gesture, "mainKeyName", "")
        if not key:
            return None
        key = key.lower()

        layer_map = {
            "0": self.script_layerLoginStatus,
            "1": self.script_layerDay1,
            "2": self.script_layerDay2,
            "3": self.script_layerDay3,
            "4": self.script_layerDay4,
            "5": self.script_layerDay5,
            "6": self.script_layerDay6,
            "7": self.script_layerDay7,
            "8": self.script_layerToggleSpeechMode,
            "9": self.script_layerSelectCalendars,
            "n": self.script_layerAddEvent,
            "e": self.script_layerEditEvent,
            "u": self.script_layerDeleteEvent,
            "p": self.script_layerPickDayPreview,
            "s": self.script_layerSearchEvents,
            "h": self.script_layerHelp,
        }
        return layer_map.get(key)

    def getScript(self, gesture):
        if self._layer_active:
            script = self._get_layer_script(gesture)
            if script is not None:
                return self._wrap_layer_script(script)
            self._deactivate_layer()
            return None
        return super(GlobalPlugin, self).getScript(gesture)

    def _wrap_layer_script(self, script):
        def wrapped(gesture):
            try:
                self._play_layer_command_sound()
                script(gesture)
            finally:
                self._deactivate_layer()
        return wrapped

    def _load_settings_data(self):
        default_data = {
            "selected_calendar_ids": [],
            "speech_mode": "short",
            "show_shortcuts_on_status": True,
            "last_added_event_calendar_id": "",
        }

        if not os.path.exists(SETTINGS_PATH):
            return default_data

        try:
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                return default_data

            merged = default_data.copy()
            merged.update(data)
            return merged
        except Exception:
            return default_data

    def _save_settings_data(self, data):
        try:
            ensure_user_data_dir()
            with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _get_show_shortcuts_on_status(self):
        data = self._load_settings_data()
        return bool(data.get("show_shortcuts_on_status", True))

    def _set_show_shortcuts_on_status(self, value):
        data = self._load_settings_data()
        data["show_shortcuts_on_status"] = bool(value)
        self._save_settings_data(data)

    def _get_last_added_event_calendar_id(self):
        data = self._load_settings_data()
        return str(data.get("last_added_event_calendar_id", "")).strip()

    def _set_last_added_event_calendar_id(self, calendar_id):
        data = self._load_settings_data()
        data["last_added_event_calendar_id"] = str(calendar_id or "").strip()
        self._save_settings_data(data)

    def _speak_message(self, text):
        text = str(text or "").strip()
        if not text:
            text = self._t("no_data")
        ui.message(text)

    def _show_message(self, text, title="Google Calendar Manager"):
        text = str(text or "").strip()
        if not text:
            text = self._t("no_data")

        ui.message(text)

        def _show():
            dialog = wx.MessageDialog(
                self._get_dialog_parent(),
                text,
                title,
                wx.OK | wx.ICON_INFORMATION,
            )
            try:
                self._show_modal_dialog(dialog)
            except Exception:
                pass
            finally:
                try:
                    dialog.Destroy()
                except Exception:
                    pass

        wx.CallAfter(_show)

    def _show_readonly_dialog(self, title, text):
        dialog = ReadOnlyMessageDialog(
            self._get_dialog_parent(),
            title=title,
            message=text,
            ok_label=self._t("dialog_ok"),
        )
        try:
            self._show_modal_dialog(dialog)
        finally:
            dialog.Destroy()

    def _show_shortcuts_dialog(self):
        dialog = ReadOnlyMessageDialog(
            self._get_dialog_parent(),
            title=self._t("shortcuts_dialog_title"),
            message=self._t("shortcuts_dialog_text"),
            ok_label=self._t("dialog_ok"),
        )
        try:
            self._show_modal_dialog(dialog)
        finally:
            dialog.Destroy()

    def _show_status_dialog_with_checkbox(self):
        initial_checked = self._get_show_shortcuts_on_status()

        dialog = ReadOnlyMessageDialog(
            self._get_dialog_parent(),
            title=self._t("login_status_title"),
            message=self._t("login_status_signed_in"),
            ok_label=self._t("dialog_ok"),
            checkbox_label=self._t("shortcuts_checkbox_label"),
            checkbox_checked=initial_checked,
        )
        try:
            result = self._show_modal_dialog(dialog)
            show_shortcuts = dialog.is_checkbox_checked()
        finally:
            dialog.Destroy()

        self._set_show_shortcuts_on_status(show_shortcuts)

        if result == wx.ID_OK and show_shortcuts:
            self._show_shortcuts_dialog()

    def _start_login_thread(self):
        with self._login_lock:
            if self._login_in_progress:
                return

            self._login_in_progress = True
            self._last_login_result = None

            thread = threading.Thread(
                target=self._run_login_flow,
                name="GCRLoginThread",
                daemon=True,
            )
            self._login_thread = thread
            thread.start()

    def _run_login_flow(self):
        try:
            from . import googleAuth
            result = googleAuth.start_login()
        except Exception as e:
            result = {
                "ok": False,
                "text": str(e),
            }

        with self._login_lock:
            self._last_login_result = result
            self._login_in_progress = False
            self._login_thread = None

    def _read_events_for_offset(self, days_ahead):
        def _task():
            from . import googleAuth
            ready_error = self._google_ready_or_error(googleAuth)
            if ready_error is not None:
                return ready_error
            return googleAuth.get_events_for_day(days_ahead)

        def _done(result):
            if result.get("ok"):
                self._speak_message(result.get("text", self._t("no_data")))
            else:
                self._speak_message(result.get("text", self._t("events_fetch_failed")))

        self._start_network_task(
            self._t("busy_fetching_events"),
            _task,
            _done,
            name="GCRReadEventsThread",
        )


    def _show_calendar_selection_dialog(self):
        try:
            from . import settings
        except Exception as e:
            self._show_message(
                self._t("import_error_modules", error=e),
                self._t("module_import_error_title"),
            )
            return

        def _task():
            from . import googleAuth
            ready_error = self._google_ready_or_error(googleAuth)
            if ready_error is not None:
                return ready_error
            return googleAuth.get_calendars()

        def _done(result):
            if not result.get("ok"):
                self._show_message(
                    result.get("text", self._t("calendar_list_fetch_failed")),
                    result.get("title", self._t("calendar_list_failed_title")),
                )
                return

            calendars = result.get("calendars", [])
            if not calendars:
                self._show_message(
                    self._t("no_calendars_available"),
                    self._t("calendar_list_empty_title"),
                )
                return

            selected_ids = settings.get_selected_calendar_ids()
            labels = []
            preselected_indexes = []

            for index, item in enumerate(calendars):
                label = item.get("summary", self._t("no_name"))
                if item.get("primary"):
                    label += self._t("primary_suffix")
                labels.append(label)

                if item.get("id") in selected_ids:
                    preselected_indexes.append(index)

            dialog = CalendarSelectionDialog(
                self._get_dialog_parent(),
                title=self._t("calendar_dialog_title"),
                info_text=self._t("calendar_dialog_info"),
                labels=labels,
                checked_indexes=preselected_indexes,
                ok_label=self._t("dialog_ok"),
                cancel_label=self._t("dialog_cancel"),
            )

            try:
                result_code = self._show_modal_dialog(dialog)
                if result_code == wx.ID_OK:
                    chosen_indexes = dialog.get_selected_indexes()
                    chosen_ids = [calendars[i]["id"] for i in chosen_indexes]
                    settings.set_selected_calendar_ids(chosen_ids)

                    if not chosen_ids:
                        self._show_readonly_dialog(
                            self._t("calendar_dialog_title"),
                            self._t("no_calendars_selected"),
                        )
                    else:
                        chosen_names = [calendars[i]["summary"] for i in chosen_indexes]
                        self._show_readonly_dialog(
                            self._t("calendar_dialog_title"),
                            self._t("saved_calendars", names=", ".join(chosen_names)),
                        )
                else:
                    ui.message(self._t("selection_cancelled"))
            finally:
                dialog.Destroy()

        self._start_network_task(
            self._t("busy_fetching_calendars"),
            _task,
            _done,
            name="GCRCalendarsThread",
        )


    def _resolve_event_year(self, day, month, reference_date=None):
        if reference_date is None:
            reference_date = datetime.date.today()

        candidate = datetime.date(reference_date.year, month, day)
        if candidate < reference_date:
            candidate = datetime.date(reference_date.year + 1, month, day)
        return candidate.year

    def _get_add_edit_labels(self):
        return {
            "title": self._t("add_event_title_label"),
            "day": self._t("add_event_day_label"),
            "month": self._t("add_event_month_label"),
            "end_day": self._t("add_event_end_day_label"),
            "end_month": self._t("add_event_end_month_label"),
            "all_day": self._t("add_event_all_day_label"),
            "start_hour": self._t("add_event_start_hour_label"),
            "start_minute": self._t("add_event_start_minute_label"),
            "end_hour": self._t("add_event_end_hour_label"),
            "end_minute": self._t("add_event_end_minute_label"),
            "location": self._t("add_event_location_label"),
            "recurrence": self._t("add_event_recurrence_label"),
            "recurrence_no_end": self._t("add_event_recurrence_no_end_label"),
            "recurrence_end_day": self._t("add_event_recurrence_end_day_label"),
            "recurrence_end_month": self._t("add_event_recurrence_end_month_label"),
            "recurrence_end_year": self._t("add_event_recurrence_end_year_label"),
            "calendar": self._t("add_event_calendar_label"),
        }

    def _build_calendar_labels_for_add_event(self, calendars):
        labels = []
        selected_calendar_index = 0
        last_calendar_id = self._get_last_added_event_calendar_id()

        for index, item in enumerate(calendars):
            label = item.get("summary", self._t("no_name"))
            if item.get("primary"):
                label += self._t("primary_suffix")
            labels.append(label)

            if last_calendar_id and item.get("id") == last_calendar_id:
                selected_calendar_index = index

        return labels, selected_calendar_index

    def _parse_single_date(self, day_value, month_value, day_error_key, month_error_key, invalid_date_key, reference_date=None):
        try:
            day = int(str(day_value).strip())
        except Exception:
            return False, self._t(day_error_key), None

        try:
            month = int(str(month_value).strip())
        except Exception:
            return False, self._t(month_error_key), None

        if day < 1 or day > 31:
            return False, self._t(day_error_key), None

        if month < 1 or month > 12:
            return False, self._t(month_error_key), None

        try:
            year = self._resolve_event_year(day, month, reference_date=reference_date)
            parsed_date = datetime.date(year, month, day)
        except Exception:
            return False, self._t(invalid_date_key), None

        return True, "", parsed_date

    def _parse_day_month_to_date(self, raw_data):
        return self._parse_single_date(
            raw_data.get("day", ""),
            raw_data.get("month", ""),
            "add_event_error_day_required",
            "add_event_error_month_required",
            "add_event_error_invalid_date",
            reference_date=None,
        )

    def _parse_end_day_month_to_date(self, raw_data, start_date):
        return self._parse_single_date(
            raw_data.get("end_day", ""),
            raw_data.get("end_month", ""),
            "add_event_error_end_day_required",
            "add_event_error_end_month_required",
            "add_event_error_invalid_end_date",
            reference_date=start_date,
        )

    def _parse_recurrence_end_date(self, raw_data, start_date):
        day_value = raw_data.get("recurrence_end_day", "")
        month_value = raw_data.get("recurrence_end_month", "")
        year_value = raw_data.get("recurrence_end_year", "")

        try:
            day = int(str(day_value).strip())
        except Exception:
            return False, self._t("add_event_error_recurrence_end_day_required"), None

        try:
            month = int(str(month_value).strip())
        except Exception:
            return False, self._t("add_event_error_recurrence_end_month_required"), None

        try:
            year = int(str(year_value).strip())
        except Exception:
            return False, self._t("add_event_error_recurrence_end_year_required"), None

        if day < 1 or day > 31:
            return False, self._t("add_event_error_recurrence_end_day_required"), None

        if month < 1 or month > 12:
            return False, self._t("add_event_error_recurrence_end_month_required"), None

        min_year = start_date.year
        max_year = start_date.year + 50
        if year < min_year or year > max_year:
            return (
                False,
                self._t(
                    "add_event_error_recurrence_end_year_range",
                    min_year=min_year,
                    max_year=max_year,
                ),
                None,
            )

        try:
            parsed_date = datetime.date(year, month, day)
        except Exception:
            return False, self._t("add_event_error_recurrence_invalid_end_date"), None

        return True, "", parsed_date

    def _parse_add_event_time_range(self, raw_data, event_date):
        try:
            start_hour = int(str(raw_data.get("start_hour", "")).strip())
            start_minute = int(str(raw_data.get("start_minute", "")).strip())
        except Exception:
            return False, self._t("add_event_error_start_time"), None, None

        try:
            end_hour = int(str(raw_data.get("end_hour", "")).strip())
            end_minute = int(str(raw_data.get("end_minute", "")).strip())
        except Exception:
            return False, self._t("add_event_error_end_time"), None, None

        if start_hour < 0 or start_hour > 23 or start_minute < 0 or start_minute > 59:
            return False, self._t("add_event_error_start_time"), None, None

        if end_hour < 0 or end_hour > 23 or end_minute < 0 or end_minute > 59:
            return False, self._t("add_event_error_end_time"), None, None

        start_dt = datetime.datetime(
            event_date.year,
            event_date.month,
            event_date.day,
            start_hour,
            start_minute,
        )
        end_dt = datetime.datetime(
            event_date.year,
            event_date.month,
            event_date.day,
            end_hour,
            end_minute,
        )

        if end_dt <= start_dt:
            return False, self._t("add_event_error_end_before_start"), None, None

        return True, "", start_dt, end_dt

    def _parse_update_event_time_range(self, raw_data, event_date, original_event):
        try:
            start_hour = int(str(raw_data.get("start_hour", "")).strip())
            start_minute = int(str(raw_data.get("start_minute", "")).strip())
        except Exception:
            return False, self._t("add_event_error_start_time"), None, None

        try:
            end_hour = int(str(raw_data.get("end_hour", "")).strip())
            end_minute = int(str(raw_data.get("end_minute", "")).strip())
        except Exception:
            return False, self._t("add_event_error_end_time"), None, None

        if start_hour < 0 or start_hour > 23 or start_minute < 0 or start_minute > 59:
            return False, self._t("add_event_error_start_time"), None, None

        if end_hour < 0 or end_hour > 23 or end_minute < 0 or end_minute > 59:
            return False, self._t("add_event_error_end_time"), None, None

        day_span = 0
        original_start_iso = str(original_event.get("start_datetime", "")).strip()
        original_end_iso = str(original_event.get("end_datetime", "")).strip()
        if original_start_iso and original_end_iso:
            try:
                original_start_dt = datetime.datetime.fromisoformat(original_start_iso)
                original_end_dt = datetime.datetime.fromisoformat(original_end_iso)
                day_span = max(
                    (original_end_dt.date() - original_start_dt.date()).days,
                    0,
                )
            except Exception:
                day_span = 0

        end_date = event_date + datetime.timedelta(days=day_span)
        start_dt = datetime.datetime(
            event_date.year,
            event_date.month,
            event_date.day,
            start_hour,
            start_minute,
        )
        end_dt = datetime.datetime(
            end_date.year,
            end_date.month,
            end_date.day,
            end_hour,
            end_minute,
        )

        if end_dt <= start_dt:
            return False, self._t("add_event_error_end_before_start"), None, None

        return True, "", start_dt, end_dt

    def _build_recurrence_payload(self, raw_data, start_date):
        recurrence_mode = recurrence_index_to_mode(raw_data.get("recurrence_index", 0))
        recurrence_payload = {
            "recurrence_mode": recurrence_mode,
            "recurrence_no_end": False,
            "recurrence_end_date": "",
        }

        if recurrence_mode == "none":
            return True, "", recurrence_payload

        recurrence_no_end = bool(raw_data.get("recurrence_no_end", False))
        recurrence_payload["recurrence_no_end"] = recurrence_no_end

        if recurrence_no_end:
            return True, "", recurrence_payload

        is_valid, error_text, recurrence_end_date = self._parse_recurrence_end_date(raw_data, start_date)
        if not is_valid:
            return False, error_text, None

        if recurrence_end_date < start_date:
            return False, self._t("add_event_error_recurrence_end_before_start"), None

        recurrence_payload["recurrence_end_date"] = recurrence_end_date.isoformat()
        return True, "", recurrence_payload

    def _build_add_event_payload(self, raw_data, calendars):
        title = str(raw_data.get("title", "")).strip()
        if not title:
            return False, self._t("add_event_error_title_required"), None

        is_valid, error_text, start_date = self._parse_day_month_to_date(raw_data)
        if not is_valid:
            return False, error_text, None

        try:
            calendar_index = int(raw_data.get("calendar_index", -1))
        except Exception:
            calendar_index = -1

        if not (0 <= calendar_index < len(calendars)):
            return False, self._t("add_event_error_calendar_required"), None

        chosen_calendar = calendars[calendar_index]
        chosen_calendar_id = str(chosen_calendar.get("id", "")).strip()
        chosen_calendar_name = str(chosen_calendar.get("summary", self._t("no_name"))).strip()

        if not chosen_calendar_id:
            return False, self._t("add_event_error_calendar_required"), None

        all_day = bool(raw_data.get("all_day", False))
        location = str(raw_data.get("location", "")).strip()
        recurrence_mode = recurrence_index_to_mode(raw_data.get("recurrence_index", 0))

        payload = {
            "calendar_id": chosen_calendar_id,
            "calendar_name": chosen_calendar_name,
            "summary": title,
            "location": location,
            "all_day": all_day,
            "date": start_date.isoformat(),
        }

        if all_day:
            if recurrence_mode == "none":
                is_valid, error_text, end_date = self._parse_end_day_month_to_date(raw_data, start_date)
                if not is_valid:
                    return False, error_text, None
                if end_date < start_date:
                    return False, self._t("add_event_error_end_date_before_start"), None
            else:
                # Recurring all-day events are always single-day per occurrence;
                # the "event's own end" field is hidden in the dialog for this case
                # and must not be relied upon, even if it holds a stale value.
                end_date = start_date

            payload["end_date"] = end_date.isoformat()
        else:
            is_valid, error_text, start_dt, end_dt = self._parse_add_event_time_range(raw_data, start_date)
            if not is_valid:
                return False, error_text, None

            payload["start_datetime"] = start_dt.isoformat()
            payload["end_datetime"] = end_dt.isoformat()

        is_valid, error_text, recurrence_payload = self._build_recurrence_payload(raw_data, start_date)
        if not is_valid:
            return False, error_text, None

        payload.update(recurrence_payload)
        return True, "", payload

    def _build_update_event_payload(self, raw_data, original_event):
        title = str(raw_data.get("title", "")).strip()
        if not title:
            return False, self._t("add_event_error_title_required"), None

        # Editing must preserve the year of the loaded event. The generic
        # add-event parser intentionally chooses the next matching date, which
        # is useful when creating a new event but can silently move an existing
        # event to the following year after its anniversary has passed.
        try:
            original_start_date = datetime.date.fromisoformat(
                str(original_event.get("date", "")).strip()
            )
        except Exception:
            return False, self._t("edit_event_error_failed"), None

        is_valid, error_text, start_date = self._parse_single_date(
            raw_data.get("day", ""),
            raw_data.get("month", ""),
            "add_event_error_day_required",
            "add_event_error_month_required",
            "add_event_error_invalid_date",
            reference_date=datetime.date(original_start_date.year, 1, 1),
        )
        if not is_valid:
            return False, error_text, None

        calendar_id = str(original_event.get("calendar_id", "")).strip()
        event_id = str(original_event.get("event_id", "")).strip()
        calendar_name = str(original_event.get("calendar_name", self._t("no_name"))).strip()
        recurrence_scope = str(original_event.get("recurrence_scope", "")).strip().lower()

        if not calendar_id or not event_id:
            return False, self._t("edit_event_error_failed"), None

        all_day = bool(raw_data.get("all_day", False))
        location = str(raw_data.get("location", "")).strip()
        recurrence_mode = recurrence_index_to_mode(raw_data.get("recurrence_index", 0))

        payload = {
            "event_id": event_id,
            "calendar_id": calendar_id,
            "calendar_name": calendar_name,
            "summary": title,
            "location": location,
            "all_day": all_day,
            "date": start_date.isoformat(),
            "recurrence_scope": recurrence_scope,
        }

        if all_day:
            if recurrence_mode == "none":
                is_valid, error_text, end_date = self._parse_end_day_month_to_date(raw_data, start_date)
                if not is_valid:
                    return False, error_text, None
                if end_date < start_date:
                    return False, self._t("add_event_error_end_date_before_start"), None
            else:
                end_date = start_date

            payload["end_date"] = end_date.isoformat()
        else:
            is_valid, error_text, start_dt, end_dt = self._parse_update_event_time_range(
                raw_data,
                start_date,
                original_event,
            )
            if not is_valid:
                return False, error_text, None

            payload["start_datetime"] = start_dt.isoformat()
            payload["end_datetime"] = end_dt.isoformat()

        if recurrence_scope == "instance":
            recurrence_payload = {
                "recurrence_mode": "none",
                "recurrence_no_end": False,
                "recurrence_end_date": "",
            }
        else:
            is_valid, error_text, recurrence_payload = self._build_recurrence_payload(raw_data, start_date)
            if not is_valid:
                return False, error_text, None

        payload.update(recurrence_payload)
        return True, "", payload

    def _build_delete_event_payload(self, original_event):
        calendar_id = str(original_event.get("calendar_id", "")).strip()
        event_id = str(original_event.get("event_id", "")).strip()
        calendar_name = str(original_event.get("calendar_name", self._t("no_name"))).strip()

        if not calendar_id or not event_id:
            return False, self._t("delete_event_error_failed"), None

        payload = {
            "event_id": event_id,
            "calendar_id": calendar_id,
            "calendar_name": calendar_name,
            "summary": str(original_event.get("summary", "")).strip(),
            "all_day": bool(original_event.get("all_day", False)),
            "date": str(original_event.get("date", "")).strip(),
            "end_date": str(original_event.get("end_date", "")).strip(),
            "start_datetime": str(original_event.get("start_datetime", "")).strip(),
            "recurrence_mode": str(original_event.get("recurrence_mode", "none")).strip(),
            "recurrence_scope": str(original_event.get("recurrence_scope", "")).strip().lower(),
            "instance_event_id": str(original_event.get("instance_event_id", "")).strip(),
            "series_event_id": str(original_event.get("series_event_id", "")).strip(),
        }
        return True, "", payload

    def _format_operation_success_message(self, event_payload, timed_key, all_day_single_key, all_day_range_key, recurrence_prefix=None):
        lang = get_ui_language()
        start_date = datetime.date.fromisoformat(str(event_payload.get("date", "")).strip())
        start_date_text = format_date_for_language(start_date, lang)

        recurrence_mode = str(event_payload.get("recurrence_mode", "none")).strip().lower()
        is_recurring = recurrence_mode in ("daily", "weekly", "monthly", "yearly")

        if is_recurring and recurrence_prefix:
            if bool(event_payload.get("all_day", False)):
                key_map = {
                    "daily": f"{recurrence_prefix}_daily",
                    "weekly": f"{recurrence_prefix}_weekly",
                    "monthly": f"{recurrence_prefix}_monthly",
                    "yearly": f"{recurrence_prefix}_yearly",
                }
                return self._t(
                    key_map[recurrence_mode],
                    date=start_date_text,
                )

            start_dt = datetime.datetime.fromisoformat(str(event_payload.get("start_datetime", "")).strip())
            time_text = start_dt.strftime("%H:%M")

            key_map = {
                "daily": f"{recurrence_prefix}_daily_timed",
                "weekly": f"{recurrence_prefix}_weekly_timed",
                "monthly": f"{recurrence_prefix}_monthly_timed",
                "yearly": f"{recurrence_prefix}_yearly_timed",
            }
            return self._t(
                key_map[recurrence_mode],
                date=start_date_text,
                time=time_text,
            )

        calendar_name = str(event_payload.get("calendar_name", "")).strip() or self._t("no_name")
        title = str(event_payload.get("summary", "")).strip() or self._t("no_title")

        if bool(event_payload.get("all_day", False)):
            end_date_raw = str(event_payload.get("end_date", "")).strip()
            if end_date_raw:
                end_date = datetime.date.fromisoformat(end_date_raw)
            else:
                end_date = start_date

            if end_date > start_date:
                return self._t(
                    all_day_range_key,
                    calendar=calendar_name,
                    start_date=start_date_text,
                    end_date=format_date_for_language(end_date, lang),
                    title=title,
                )

            return self._t(
                all_day_single_key,
                calendar=calendar_name,
                date=start_date_text,
                title=title,
            )

        start_dt = datetime.datetime.fromisoformat(str(event_payload.get("start_datetime", "")).strip())
        time_text = start_dt.strftime("%H:%M")

        return self._t(
            timed_key,
            calendar=calendar_name,
            date=start_date_text,
            time=time_text,
            title=title,
        )

    def _format_delete_event_confirm_message(self, event_payload):
        lang = get_ui_language()
        start_date = datetime.date.fromisoformat(str(event_payload.get("date", "")).strip())
        start_date_text = format_date_for_language(start_date, lang)

        recurrence_scope = str(event_payload.get("recurrence_scope", "")).strip().lower()
        recurrence_mode = str(event_payload.get("recurrence_mode", "none")).strip().lower()
        is_recurring = recurrence_mode in ("daily", "weekly", "monthly", "yearly")

        if recurrence_scope == "instance":
            calendar_name = str(event_payload.get("calendar_name", "")).strip() or self._t("no_name")
            title = str(event_payload.get("summary", "")).strip() or self._t("no_title")

            if bool(event_payload.get("all_day", False)):
                end_date_raw = str(event_payload.get("end_date", "")).strip()
                end_date = start_date
                if end_date_raw:
                    try:
                        end_date = datetime.date.fromisoformat(end_date_raw)
                    except Exception:
                        end_date = start_date

                if end_date > start_date:
                    return self._t(
                        "delete_event_confirm_instance_all_day_range",
                        calendar=calendar_name,
                        start_date=start_date_text,
                        end_date=format_date_for_language(end_date, lang),
                        title=title,
                    )

                return self._t(
                    "delete_event_confirm_instance_all_day_single",
                    calendar=calendar_name,
                    date=start_date_text,
                    title=title,
                )

            start_dt = datetime.datetime.fromisoformat(str(event_payload.get("start_datetime", "")).strip())
            time_text = start_dt.strftime("%H:%M")
            return self._t(
                "delete_event_confirm_instance_timed",
                calendar=calendar_name,
                date=start_date_text,
                time=time_text,
                title=title,
            )

        if is_recurring:
            if bool(event_payload.get("all_day", False)):
                key_map = {
                    "daily": "delete_event_confirm_recurrence_daily",
                    "weekly": "delete_event_confirm_recurrence_weekly",
                    "monthly": "delete_event_confirm_recurrence_monthly",
                    "yearly": "delete_event_confirm_recurrence_yearly",
                }
                return self._t(
                    key_map[recurrence_mode],
                    date=start_date_text,
                )

            start_dt = datetime.datetime.fromisoformat(str(event_payload.get("start_datetime", "")).strip())
            time_text = start_dt.strftime("%H:%M")

            key_map = {
                "daily": "delete_event_confirm_recurrence_daily_timed",
                "weekly": "delete_event_confirm_recurrence_weekly_timed",
                "monthly": "delete_event_confirm_recurrence_monthly_timed",
                "yearly": "delete_event_confirm_recurrence_yearly_timed",
            }
            return self._t(
                key_map[recurrence_mode],
                date=start_date_text,
                time=time_text,
            )

        calendar_name = str(event_payload.get("calendar_name", "")).strip() or self._t("no_name")
        title = str(event_payload.get("summary", "")).strip() or self._t("no_title")

        if bool(event_payload.get("all_day", False)):
            end_date_raw = str(event_payload.get("end_date", "")).strip()
            if end_date_raw:
                end_date = datetime.date.fromisoformat(end_date_raw)
            else:
                end_date = start_date

            if end_date > start_date:
                return self._t(
                    "delete_event_confirm_all_day_range",
                    calendar=calendar_name,
                    start_date=start_date_text,
                    end_date=format_date_for_language(end_date, lang),
                    title=title,
                )

            return self._t(
                "delete_event_confirm_all_day_single",
                calendar=calendar_name,
                date=start_date_text,
                title=title,
            )

        start_dt = datetime.datetime.fromisoformat(str(event_payload.get("start_datetime", "")).strip())
        time_text = start_dt.strftime("%H:%M")

        return self._t(
            "delete_event_confirm_timed",
            calendar=calendar_name,
            date=start_date_text,
            time=time_text,
            title=title,
        )

    def _format_bulk_delete_confirm_message(self, delete_payloads):
        count = len(delete_payloads)
        lines = [self._t("delete_event_confirm_multiple_intro", count=count), ""]

        for index, payload in enumerate(delete_payloads, start=1):
            lines.append(f"{index}. {self._format_event_choice_label(payload)}")

        return "\n".join(lines)

    def _format_bulk_delete_success_message(self, deleted_count, failed_count):
        return self._t(
            "delete_event_multiple_success",
            deleted_count=deleted_count,
            failed_count=failed_count,
        )

    def _format_bulk_delete_partial_error_message(self, deleted_count):
        return self._t(
            "delete_event_multiple_partial_error",
            deleted_count=deleted_count,
        )

    def _read_last_error_details(self):
        try:
            with open(ERROR_PATH, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception:
            return ""

    def _build_error_report(self, operation_name, event_payload, result):
        lines = []
        lines.append(f"Google Calendar Manager - {operation_name} error")
        lines.append("")
        lines.append("User message:")
        lines.append(str(result.get("text", "")).strip())
        lines.append("")
        lines.append("Event payload:")
        lines.append(json.dumps(event_payload, ensure_ascii=False, indent=2))
        lines.append("")
        lines.append("Technical details:")
        technical = self._read_last_error_details()
        if technical:
            lines.append(technical)
        else:
            lines.append("No technical details available.")
        lines.append("")
        lines.append("Raw result:")
        lines.append(json.dumps(result, ensure_ascii=False, indent=2))
        return "\n".join(lines)

    def _save_error_report(self, path, content):
        ensure_user_data_dir()
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    def _open_path(self, path):
        try:
            os.startfile(path)
            return True
        except Exception:
            return False

    def _show_operation_error_dialog(self, message_key, event_payload, result, report_path, operation_name):
        report_content = self._build_error_report(operation_name, event_payload, result)

        try:
            self._save_error_report(report_path, report_content)
        except Exception as error:
            report_content += (
                "\n\nThe report could not be saved to disk.\n"
                f"Save error: {repr(error)}"
            )

        dialog = ErrorDetailsDialog(
            self._get_dialog_parent(),
            title=self._t("error_dialog_title"),
            message=self._t(message_key),
            details_label=self._t("error_dialog_details"),
            close_label=self._t("error_dialog_close"),
        )
        try:
            dialog_result = self._show_modal_dialog(dialog)
        finally:
            dialog.Destroy()

        if dialog_result == wx.ID_MORE:
            # Show the report inside an accessible NVDA dialog. Opening a .txt
            # file through the Windows file association remains unreliable on
            # some systems and previously hid the useful technical details.
            self._show_readonly_dialog(
                self._t("error_dialog_title"),
                report_content,
            )

    def _show_add_event_dialog(self, default_date=None):
        def _task():
            from . import googleAuth
            ready_error = self._google_ready_or_error(googleAuth)
            if ready_error is not None:
                return ready_error
            return googleAuth.get_calendars()

        def _done(calendars_result):
            if not calendars_result.get("ok"):
                self._show_message(
                    calendars_result.get("text", self._t("calendar_list_fetch_failed")),
                    calendars_result.get("title", self._t("calendar_list_failed_title")),
                )
                return

            calendars = calendars_result.get("calendars", [])
            if not calendars:
                self._show_message(
                    self._t("no_calendars_available"),
                    self._t("calendar_list_empty_title"),
                )
                return

            calendar_names, selected_calendar_index = self._build_calendar_labels_for_add_event(calendars)
            if isinstance(default_date, datetime.date):
                event_date = default_date
            else:
                event_date = datetime.date.today()

            dialog = AddEventDialog(
                self._get_dialog_parent(),
                title=self._t("add_event_dialog_title"),
                labels=self._get_add_edit_labels(),
                calendar_names=calendar_names,
                recurrence_labels=get_recurrence_choice_labels(get_ui_language()),
                selected_calendar_index=selected_calendar_index,
                selected_recurrence_index=0,
                ok_label=self._t("dialog_ok"),
                cancel_label=self._t("dialog_cancel"),
                default_title="",
                default_day=str(event_date.day),
                default_month=str(event_date.month),
                default_end_day=str(event_date.day),
                default_end_month=str(event_date.month),
                default_recurrence_end_day=str(event_date.day),
                default_recurrence_end_month=str(event_date.month),
                default_recurrence_end_year=str(event_date.year),
                default_start_hour="09",
                default_start_minute="00",
                default_end_hour="10",
                default_end_minute="00",
                default_location="",
                default_all_day=False,
                default_recurrence_no_end=False,
            )

            try:
                result = self._show_modal_dialog(dialog)
                if result != wx.ID_OK:
                    return
                raw_data = dialog.get_data()
            finally:
                dialog.Destroy()

            is_valid, error_text, event_payload = self._build_add_event_payload(raw_data, calendars)
            if not is_valid:
                self._show_message(error_text, self._t("add_event_dialog_title"))
                return

            self._create_event_async(event_payload)

        self._start_network_task(
            self._t("busy_fetching_calendars"),
            _task,
            _done,
            name="GCRAddEventCalendarsThread",
        )


    def _create_event_async(self, event_payload):
        def _task():
            from . import googleAuth
            ready_error = self._google_ready_or_error(googleAuth)
            if ready_error is not None:
                return ready_error
            return googleAuth.create_event(event_payload)

        def _done(result):
            if result.get("ok"):
                self._set_last_added_event_calendar_id(event_payload["calendar_id"])
                success_text = self._format_operation_success_message(
                    event_payload,
                    "add_event_success_timed",
                    "add_event_success_all_day_single",
                    "add_event_success_all_day_range",
                    recurrence_prefix="add_recurrence_success",
                )
                self._show_message(success_text, self._t("add_event_dialog_title"))
            else:
                if result.get("title"):
                    self._show_message(result.get("text", self._t("add_event_error_failed")), result.get("title"))
                    return
                self._show_operation_error_dialog(
                    "add_event_error_failed",
                    event_payload,
                    result,
                    CREATE_ERROR_REPORT_PATH,
                    "create_event",
                )

        self._start_network_task(
            self._t("busy_adding_event"),
            _task,
            _done,
            name="GCRCreateEventThread",
        )

    def _update_event_async(self, update_payload):
        def _task():
            from . import googleAuth
            ready_error = self._google_ready_or_error(googleAuth)
            if ready_error is not None:
                return ready_error
            return googleAuth.update_event(update_payload)

        def _done(update_result):
            if update_result.get("ok"):
                success_text = self._format_operation_success_message(
                    update_payload,
                    "edit_event_success_timed",
                    "edit_event_success_all_day_single",
                    "edit_event_success_all_day_range",
                    recurrence_prefix="edit_recurrence_success",
                )
                self._show_message(success_text, self._t("edit_event_dialog_title"))
            else:
                if update_result.get("title"):
                    self._show_message(update_result.get("text", self._t("edit_event_error_failed")), update_result.get("title"))
                    return
                self._show_operation_error_dialog(
                    "edit_event_error_failed",
                    update_payload,
                    update_result,
                    UPDATE_ERROR_REPORT_PATH,
                    "update_event",
                )

        self._start_network_task(
            self._t("busy_saving_event_changes"),
            _task,
            _done,
            name="GCRUpdateEventThread",
        )

    def _delete_events_async(self, delete_payloads):
        def _task():
            from . import googleAuth
            ready_error = self._google_ready_or_error(googleAuth)
            if ready_error is not None:
                return ready_error

            deleted_count = 0
            for delete_payload in delete_payloads:
                delete_result = googleAuth.delete_event(delete_payload)
                if delete_result.get("ok"):
                    deleted_count += 1
                    continue

                return {
                    "ok": False,
                    "deleted_count": deleted_count,
                    "failed_payload": delete_payload,
                    "failed_result": delete_result,
                }

            return {
                "ok": True,
                "deleted_count": deleted_count,
            }

        def _done(result):
            if result.get("ok"):
                if len(delete_payloads) == 1:
                    success_text = self._format_operation_success_message(
                        delete_payloads[0],
                        "delete_event_success_timed",
                        "delete_event_success_all_day_single",
                        "delete_event_success_all_day_range",
                        recurrence_prefix="delete_recurrence_success",
                    )
                else:
                    success_text = self._format_bulk_delete_success_message(result.get("deleted_count", 0), 0)
                self._show_message(success_text, self._t("delete_event_dialog_title"))
                return

            if result.get("title"):
                self._show_message(result.get("text", self._t("delete_event_error_failed")), result.get("title"))
                return

            deleted_count = int(result.get("deleted_count", 0))
            failed_payload = result.get("failed_payload") or (delete_payloads[0] if delete_payloads else {})
            failed_result = result.get("failed_result") or result

            if deleted_count == 0:
                self._show_operation_error_dialog(
                    "delete_event_error_failed",
                    failed_payload,
                    failed_result,
                    DELETE_ERROR_REPORT_PATH,
                    "delete_event",
                )
                return

            self._show_message(
                self._format_bulk_delete_partial_error_message(deleted_count),
                self._t("delete_event_dialog_title"),
            )

        self._start_network_task(
            self._t("busy_deleting_event") if len(delete_payloads) == 1 else self._t("busy_deleting_events"),
            _task,
            _done,
            name="GCRDeleteEventThread",
        )

    def _parse_event_day_dialog(self, title_key):
        today = datetime.date.today()

        day_label_key = "add_event_day_label"
        month_label_key = "add_event_month_label"

        if title_key == "edit_event_day_dialog_title":
            day_label_key = "edit_event_day_label"
            month_label_key = "edit_event_month_label"
        elif title_key == "delete_event_day_dialog_title":
            day_label_key = "delete_event_day_label"
            month_label_key = "delete_event_month_label"
        elif title_key == "pick_day_events_dialog_title":
            day_label_key = "pick_day_events_day_label"
            month_label_key = "pick_day_events_month_label"

        dialog = EventDayDialog(
            self._get_dialog_parent(),
            title=self._t(title_key),
            day_label=self._t(day_label_key),
            month_label=self._t(month_label_key),
            ok_label=self._t("dialog_ok"),
            cancel_label=self._t("dialog_cancel"),
            default_day=str(today.day),
            default_month=str(today.month),
        )

        try:
            result = self._show_modal_dialog(dialog)
            if result != wx.ID_OK:
                return None
            raw_data = dialog.get_data()
        finally:
            dialog.Destroy()

        is_valid, error_text, event_date = self._parse_day_month_to_date(raw_data)
        if not is_valid:
            self._show_message(error_text, self._t(title_key))
            return None

        return event_date

    def _format_event_choice_label(self, item, include_date=False):
        summary = str(item.get("summary", "")).strip() or self._t("no_title")

        recurrence_mode = str(item.get("recurrence_mode", "none")).strip().lower()
        if recurrence_mode == "daily":
            summary += self._t("recurring_suffix_daily")
        elif recurrence_mode == "weekly":
            summary += self._t("recurring_suffix_weekly")
        elif recurrence_mode == "monthly":
            summary += self._t("recurring_suffix_monthly")
        elif recurrence_mode == "yearly":
            summary += self._t("recurring_suffix_yearly")

        lang = get_ui_language()
        date_prefix = ""
        if include_date:
            try:
                event_date = datetime.date.fromisoformat(str(item.get("date", "")).strip())
                date_prefix = format_day_date_for_language(event_date, lang)
            except Exception:
                date_prefix = ""

        if bool(item.get("all_day", False)):
            try:
                start_date = datetime.date.fromisoformat(str(item.get("date", "")).strip())
            except Exception:
                start_date = None
            end_date_raw = str(item.get("end_date", "")).strip()
            end_date = start_date
            if end_date_raw:
                try:
                    end_date = datetime.date.fromisoformat(end_date_raw)
                except Exception:
                    end_date = start_date

            if start_date is not None and end_date is not None and end_date > start_date:
                range_text = self._t(
                    "date_range",
                    start=format_date_for_language(start_date, lang),
                    end=format_date_for_language(end_date, lang),
                )
                label = self._t("all_day_range_short", range_text=range_text, summary=summary)
            else:
                label = f"{self._t('all_day_short', summary=summary, calendar_label='')}".strip()
        else:
            start_iso = str(item.get("start_datetime", "")).strip()
            end_iso = str(item.get("end_datetime", "")).strip()

            start_text = ""
            end_text = ""

            if start_iso:
                try:
                    start_text = datetime.datetime.fromisoformat(start_iso).strftime("%H:%M")
                except Exception:
                    start_text = ""

            if end_iso:
                try:
                    end_text = datetime.datetime.fromisoformat(end_iso).strftime("%H:%M")
                except Exception:
                    end_text = ""

            if start_text and end_text:
                label = f"{self._t('date_range', start=start_text, end=end_text)}, {summary}"
            elif start_text:
                label = f"{start_text}, {summary}"
            else:
                label = summary

        if date_prefix:
            return f"{date_prefix}, {label}"
        return label

    def _select_event(self, events, title_key, label_key, ok_key, include_date=False):
        choices = [self._format_event_choice_label(item, include_date=include_date) for item in events]

        dialog = EventSelectionDialog(
            self._get_dialog_parent(),
            title=self._t(title_key),
            label_text=self._t(label_key),
            choices=choices,
            ok_label=self._t(ok_key),
            cancel_label=self._t("dialog_cancel"),
        )

        try:
            result = self._show_modal_dialog(dialog)
            if result != wx.ID_OK:
                return None
            selected_index = dialog.get_selected_index()
        finally:
            dialog.Destroy()

        if not (0 <= selected_index < len(events)):
            return None

        return events[selected_index]

    def _select_multiple_events(self, events, title_key, label_key, ok_key, include_date=False):
        choices = [self._format_event_choice_label(item, include_date=include_date) for item in events]

        dialog = EventSelectionDialog(
            self._get_dialog_parent(),
            title=self._t(title_key),
            label_text=self._t(label_key),
            choices=choices,
            ok_label=self._t(ok_key),
            cancel_label=self._t("dialog_cancel"),
            multi_select=True,
            select_all_label=self._t("select_all_label"),
            deselect_all_label=self._t("deselect_all_label"),
            checked_state_label=self._t("checked_state"),
            unchecked_state_label=self._t("unchecked_state"),
            selection_all_selected_message=self._t("selection_all_selected"),
            selection_all_cleared_message=self._t("selection_all_cleared"),
        )

        try:
            result = self._show_modal_dialog(dialog)
            if result != wx.ID_OK:
                return None
            selected_indexes = dialog.get_selected_indexes()
        finally:
            dialog.Destroy()

        valid_indexes = [index for index in selected_indexes if 0 <= index < len(events)]
        if not valid_indexes:
            return []

        return [events[index] for index in valid_indexes]

    def _list_events_for_date_async(
        self,
        target_date,
        busy_message,
        error_title_key,
        on_success,
        thread_name="GCRListEventsThread",
    ):
        def _task():
            from . import googleAuth
            ready_error = self._google_ready_or_error(googleAuth)
            if ready_error is not None:
                return ready_error
            return googleAuth.list_events_for_edit(target_date.isoformat())

        def _done(result):
            if not result.get("ok"):
                self._show_message(
                    result.get("text", self._t("helper_event_list_for_edit_error")),
                    result.get("title", self._t(error_title_key)),
                )
                return

            events = result.get("items", [])
            on_success(target_date, events)

        self._start_network_task(
            busy_message,
            _task,
            _done,
            name=thread_name,
        )

    def _show_edit_event_dialog(self):
        target_date = self._parse_event_day_dialog("edit_event_day_dialog_title")
        if target_date is None:
            return

        self._list_events_for_date_async(
            target_date,
            self._t("busy_fetching_events_to_edit"),
            "edit_event_select_dialog_title",
            self._show_edit_event_dialog_for_loaded_events,
            thread_name="GCRListEventsForEditThread",
        )

    def _show_delete_event_dialog(self):
        target_date = self._parse_event_day_dialog("delete_event_day_dialog_title")
        if target_date is None:
            return

        self._list_events_for_date_async(
            target_date,
            self._t("busy_fetching_events_to_delete"),
            "delete_event_select_dialog_title",
            self._show_delete_event_dialog_for_loaded_events,
            thread_name="GCRListEventsForDeleteThread",
        )

    def _format_daily_preview_text(self, target_date, events):
        header = format_day_date_for_language(target_date, get_ui_language())

        if not events:
            return self._t("date_no_events", date=header)

        count = len(events)
        if count == 1:
            prefix = self._t("one_event_prefix", date=header)
        elif 2 <= count <= 4:
            prefix = self._t("few_events_prefix", date=header, count=count)
        else:
            prefix = self._t("many_events_prefix", date=header, count=count)

        lines = [prefix, ""]
        for item in events:
            lines.append(self._format_event_choice_label(item))

        return "\n".join(lines)

    def _show_edit_event_dialog_for_date(self, target_date):
        self._list_events_for_date_async(
            target_date,
            self._t("busy_fetching_events_to_edit"),
            "edit_event_select_dialog_title",
            self._show_edit_event_dialog_for_loaded_events,
            thread_name="GCRListEventsForEditFromDateThread",
        )

    def _is_recurring_instance(self, event_data):
        return bool(event_data.get("is_recurring_instance")) and bool(
            str(event_data.get("series_event_id", "")).strip()
        )

    def _select_recurring_event_scope(self, operation, bulk=False):
        operation = str(operation or "").strip().lower()
        if operation == "delete":
            title_key = "delete_event_scope_dialog_title"
            label_key = "delete_event_scope_bulk_label" if bulk else "delete_event_scope_label"
            ok_key = "delete_event_open_label"
        else:
            title_key = "edit_event_scope_dialog_title"
            label_key = "edit_event_scope_label"
            ok_key = "edit_event_open_label"

        dialog = EventSelectionDialog(
            self._get_dialog_parent(),
            title=self._t(title_key),
            label_text=self._t(label_key),
            choices=[
                self._t("recurrence_scope_this_occurrence"),
                self._t("recurrence_scope_entire_series"),
            ],
            ok_label=self._t(ok_key),
            cancel_label=self._t("dialog_cancel"),
        )

        try:
            result = self._show_modal_dialog(dialog)
            if result != wx.ID_OK:
                return None
            selected_index = dialog.get_selected_index()
        finally:
            dialog.Destroy()

        if selected_index == 1:
            return "series"
        if selected_index == 0:
            return "instance"
        return None

    def _event_for_recurrence_scope(self, event_data, scope):
        scope = str(scope or "").strip().lower()

        if scope == "series":
            series_event = event_data.get("series_event")
            if isinstance(series_event, dict) and str(series_event.get("event_id", "")).strip():
                result = dict(series_event)
            else:
                result = dict(event_data)
                series_event_id = str(event_data.get("series_event_id", "")).strip()
                if series_event_id:
                    result["event_id"] = series_event_id
            result["recurrence_scope"] = "series"
            return result

        result = dict(event_data)
        instance_event_id = str(event_data.get("instance_event_id", "")).strip()
        if instance_event_id:
            result["event_id"] = instance_event_id
        result["recurrence_scope"] = "instance"
        result["recurrence_mode"] = "none"
        result["recurrence_no_end"] = False
        result["recurrence_end_date"] = ""
        return result

    def _show_edit_event_dialog_for_loaded_events(self, target_date, events, include_date=False):
        if not events:
            self._show_message(
                self._t("edit_event_no_events"),
                self._t("edit_event_select_dialog_title"),
            )
            return

        selected_event = self._select_event(
            events,
            "edit_event_select_dialog_title",
            "edit_event_select_label",
            "edit_event_open_label",
            include_date=include_date,
        )
        if selected_event is None:
            return

        if self._is_recurring_instance(selected_event):
            scope = self._select_recurring_event_scope("edit")
            if scope is None:
                return
            selected_event = self._event_for_recurrence_scope(selected_event, scope)

        try:
            original_date = datetime.date.fromisoformat(str(selected_event.get("date", "")).strip())
        except Exception:
            original_date = target_date

        original_end_date_raw = str(selected_event.get("end_date", "")).strip()
        if original_end_date_raw:
            try:
                original_end_date = datetime.date.fromisoformat(original_end_date_raw)
            except Exception:
                original_end_date = original_date
        else:
            original_end_date = original_date

        recurrence_end_raw = str(selected_event.get("recurrence_end_date", "")).strip()
        if recurrence_end_raw:
            try:
                recurrence_end_date = datetime.date.fromisoformat(recurrence_end_raw)
            except Exception:
                recurrence_end_date = original_date
        else:
            recurrence_end_date = original_date

        default_start_hour = "09"
        default_start_minute = "00"
        default_end_hour = "10"
        default_end_minute = "00"

        if not bool(selected_event.get("all_day", False)):
            start_iso = str(selected_event.get("start_datetime", "")).strip()
            end_iso = str(selected_event.get("end_datetime", "")).strip()

            if start_iso:
                try:
                    start_dt = datetime.datetime.fromisoformat(start_iso)
                    default_start_hour = start_dt.strftime("%H")
                    default_start_minute = start_dt.strftime("%M")
                except Exception:
                    pass

            if end_iso:
                try:
                    end_dt = datetime.datetime.fromisoformat(end_iso)
                    default_end_hour = end_dt.strftime("%H")
                    default_end_minute = end_dt.strftime("%M")
                except Exception:
                    pass

        calendar_names = [str(selected_event.get("calendar_name", self._t("no_name"))).strip() or self._t("no_name")]

        dialog = AddEventDialog(
            self._get_dialog_parent(),
            title=self._t("edit_event_dialog_title"),
            labels=self._get_add_edit_labels(),
            calendar_names=calendar_names,
            recurrence_labels=get_recurrence_choice_labels(get_ui_language()),
            selected_calendar_index=0,
            selected_recurrence_index=recurrence_mode_to_index(selected_event.get("recurrence_mode", "none")),
            ok_label=self._t("edit_event_save_label"),
            cancel_label=self._t("dialog_cancel"),
            default_title=str(selected_event.get("summary", "")).strip(),
            default_day=str(original_date.day),
            default_month=str(original_date.month),
            default_end_day=str(original_end_date.day),
            default_end_month=str(original_end_date.month),
            default_recurrence_end_day=str(recurrence_end_date.day),
            default_recurrence_end_month=str(recurrence_end_date.month),
            default_recurrence_end_year=str(recurrence_end_date.year),
            default_start_hour=default_start_hour,
            default_start_minute=default_start_minute,
            default_end_hour=default_end_hour,
            default_end_minute=default_end_minute,
            default_location=str(selected_event.get("location", "")).strip(),
            default_all_day=bool(selected_event.get("all_day", False)),
            default_recurrence_no_end=bool(selected_event.get("recurrence_no_end", False)),
            enable_calendar_choice=False,
            enable_recurrence_choice=str(selected_event.get("recurrence_scope", "")).strip().lower() != "instance",
        )

        try:
            result_code = self._show_modal_dialog(dialog)
            if result_code != wx.ID_OK:
                return
            raw_data = dialog.get_data()
        finally:
            dialog.Destroy()

        is_valid, error_text, update_payload = self._build_update_event_payload(raw_data, selected_event)
        if not is_valid:
            self._show_message(error_text, self._t("edit_event_dialog_title"))
            return

        self._update_event_async(update_payload)

    def _show_delete_event_dialog_for_date(self, target_date):
        self._list_events_for_date_async(
            target_date,
            self._t("busy_fetching_events_to_delete"),
            "delete_event_select_dialog_title",
            self._show_delete_event_dialog_for_loaded_events,
            thread_name="GCRListEventsForDeleteFromDateThread",
        )

    def _show_delete_event_dialog_for_loaded_events(self, target_date, events, include_date=False):
        if not events:
            self._show_message(
                self._t("delete_event_no_events"),
                self._t("delete_event_select_dialog_title"),
            )
            return

        selected_events = self._select_multiple_events(
            events,
            "delete_event_select_dialog_title",
            "delete_event_select_label",
            "delete_event_open_label",
            include_date=include_date,
        )
        if selected_events is None:
            return
        if not selected_events:
            self._show_message(
                self._t("delete_event_no_selection"),
                self._t("delete_event_dialog_title"),
            )
            return

        recurring_events = [event for event in selected_events if self._is_recurring_instance(event)]
        shared_recurring_scope = None
        if len(recurring_events) > 1:
            shared_recurring_scope = self._select_recurring_event_scope("delete", bulk=True)
            if shared_recurring_scope is None:
                return

        scoped_selected_events = []
        seen_scoped_events = set()
        for selected_event in selected_events:
            if self._is_recurring_instance(selected_event):
                scope = shared_recurring_scope
                if scope is None:
                    scope = self._select_recurring_event_scope("delete")
                if scope is None:
                    return
                selected_event = self._event_for_recurrence_scope(selected_event, scope)

            scoped_key = (
                str(selected_event.get("calendar_id", "")).strip(),
                str(selected_event.get("event_id", "")).strip(),
            )
            if scoped_key in seen_scoped_events:
                continue
            seen_scoped_events.add(scoped_key)
            scoped_selected_events.append(selected_event)

        delete_payloads = []
        for selected_event in scoped_selected_events:
            is_valid, error_text, delete_payload = self._build_delete_event_payload(selected_event)
            if not is_valid:
                self._show_message(error_text, self._t("delete_event_dialog_title"))
                return
            delete_payloads.append(delete_payload)

        if len(delete_payloads) == 1:
            confirm_message = self._format_delete_event_confirm_message(delete_payloads[0])
        else:
            confirm_message = self._format_bulk_delete_confirm_message(delete_payloads)

        dialog = DeleteEventConfirmDialog(
            self._get_dialog_parent(),
            title=self._t("delete_event_dialog_title"),
            message=confirm_message,
            delete_label=self._t("delete_event_confirm_delete_label"),
            cancel_label=self._t("dialog_cancel"),
        )
        try:
            result_code = self._show_modal_dialog(dialog)
        finally:
            dialog.Destroy()

        if result_code != wx.ID_OK:
            return

        self._delete_events_async(delete_payloads)

    def _add_months_to_date(self, source_date, months):
        try:
            months = int(months)
        except Exception:
            months = 1

        month_index = source_date.month - 1 + months
        year = source_date.year + month_index // 12
        month = month_index % 12 + 1
        day = min(source_date.day, calendar.monthrange(year, month)[1])
        return datetime.date(year, month, day)

    def _get_search_range_labels(self):
        return [
            self._t("search_events_range_1_month"),
            self._t("search_events_range_3_months"),
            self._t("search_events_range_6_months"),
            self._t("search_events_range_12_months"),
            self._t("search_events_range_custom"),
        ]

    def _parse_search_custom_range_dialog(self):
        today = datetime.date.today()
        default_end = self._add_months_to_date(today, 1)

        dialog = SearchDateRangeDialog(
            self._get_dialog_parent(),
            title=self._t("search_events_custom_range_title"),
            start_day_label=self._t("search_events_start_day_label"),
            start_month_label=self._t("search_events_start_month_label"),
            end_day_label=self._t("search_events_end_day_label"),
            end_month_label=self._t("search_events_end_month_label"),
            ok_label=self._t("dialog_ok"),
            cancel_label=self._t("dialog_cancel"),
            default_start_day=str(today.day),
            default_start_month=str(today.month),
            default_end_day=str(default_end.day),
            default_end_month=str(default_end.month),
        )

        try:
            result = self._show_modal_dialog(dialog)
            if result != wx.ID_OK:
                return None
            raw_data = dialog.get_data()
        finally:
            dialog.Destroy()

        is_valid, error_text, start_date = self._parse_single_date(
            raw_data.get("start_day", ""),
            raw_data.get("start_month", ""),
            "search_events_error_start_day_required",
            "search_events_error_start_month_required",
            "search_events_error_invalid_start_date",
            reference_date=today,
        )
        if not is_valid:
            self._show_message(error_text, self._t("search_events_custom_range_title"))
            return None

        is_valid, error_text, end_date = self._parse_single_date(
            raw_data.get("end_day", ""),
            raw_data.get("end_month", ""),
            "search_events_error_end_day_required",
            "search_events_error_end_month_required",
            "search_events_error_invalid_end_date",
            reference_date=start_date,
        )
        if not is_valid:
            self._show_message(error_text, self._t("search_events_custom_range_title"))
            return None

        if end_date < start_date:
            self._show_message(
                self._t("search_events_error_end_before_start"),
                self._t("search_events_custom_range_title"),
            )
            return None

        return start_date, end_date

    def _show_search_events_dialog(self):
        range_labels = self._get_search_range_labels()
        dialog = SearchEventsDialog(
            self._get_dialog_parent(),
            title=self._t("search_events_dialog_title"),
            query_label=self._t("search_events_query_label"),
            range_label=self._t("search_events_range_label"),
            range_choices=range_labels,
            ok_label=self._t("search_events_open_label"),
            cancel_label=self._t("dialog_cancel"),
            default_range_index=0,
        )

        try:
            result = self._show_modal_dialog(dialog)
            if result != wx.ID_OK:
                return
            raw_data = dialog.get_data()
        finally:
            dialog.Destroy()

        query = str(raw_data.get("query", "")).strip()
        if not query:
            self._show_message(
                self._t("search_events_error_query_required"),
                self._t("search_events_dialog_title"),
            )
            return

        today = datetime.date.today()
        range_index = raw_data.get("range_index", 0)
        if range_index == 4:
            custom_range = self._parse_search_custom_range_dialog()
            if custom_range is None:
                return
            start_date, end_date = custom_range
        else:
            months_by_index = {
                0: 1,
                1: 3,
                2: 6,
                3: 12,
            }
            months = months_by_index.get(range_index, 1)
            start_date = today
            end_date = self._add_months_to_date(today, months)

        self._search_events_async(query, start_date, end_date)

    def _search_events_async(self, query, start_date, end_date):
        def _task():
            from . import googleAuth
            ready_error = self._google_ready_or_error(googleAuth)
            if ready_error is not None:
                return ready_error
            return googleAuth.search_events(query, start_date.isoformat(), end_date.isoformat())

        def _done(result):
            if not result.get("ok"):
                self._show_message(
                    result.get("text", self._t("helper_search_events_error")),
                    result.get("title", self._t("search_events_results_title")),
                )
                return

            events = result.get("items", [])
            self._show_search_events_result_for_loaded_events(query, start_date, end_date, events)

        self._start_network_task(
            self._t("busy_searching_events"),
            _task,
            _done,
            name="GCRSearchEventsThread",
        )

    def _format_search_results_text(self, query, start_date, end_date, events):
        lang = get_ui_language()
        start_text = format_date_for_language(start_date, lang)
        end_text = format_date_for_language(end_date, lang)

        if not events:
            return self._t(
                "search_events_no_results",
                query=query,
                start_date=start_text,
                end_date=end_text,
            )

        if len(events) == 1:
            intro = self._t(
                "search_events_results_intro_one",
                query=query,
                start_date=start_text,
                end_date=end_text,
            )
        else:
            intro = self._t(
                "search_events_results_intro",
                query=query,
                count=len(events),
                start_date=start_text,
                end_date=end_text,
            )

        lines = [intro, ""]
        for item in events:
            lines.append(self._format_event_choice_label(item, include_date=True))

        return "\n".join(lines)

    def _show_search_events_result_for_loaded_events(self, query, start_date, end_date, events):
        result_text = self._format_search_results_text(query, start_date, end_date, events)
        has_events = bool(events)

        dialog = DailyEventsResultDialog(
            self._get_dialog_parent(),
            title=self._t("search_events_results_title"),
            message=result_text,
            ok_label=self._t("dialog_ok"),
            other_day_label=self._t("search_events_new_search_label"),
            edit_label=self._t("edit_event_open_label"),
            delete_label=self._t("delete_event_open_label"),
            management_enabled=has_events,
        )
        try:
            result_code = self._show_modal_dialog(dialog)
        finally:
            dialog.Destroy()

        if result_code == DailyEventsResultDialog.RESULT_EDIT:
            if has_events:
                self._show_edit_event_dialog_for_loaded_events(start_date, events, include_date=True)
            return
        if result_code == DailyEventsResultDialog.RESULT_DELETE:
            if has_events:
                self._show_delete_event_dialog_for_loaded_events(start_date, events, include_date=True)
            return
        if result_code == DailyEventsResultDialog.RESULT_OTHER_DAY:
            self._show_search_events_dialog()
            return

    def _show_pick_day_events_dialog(self):
        target_date = self._parse_event_day_dialog("pick_day_events_dialog_title")
        if target_date is None:
            return

        self._show_pick_day_events_dialog_for_date(target_date)

    def _show_pick_day_events_dialog_for_date(self, target_date):
        self._list_events_for_date_async(
            target_date,
            self._t("busy_fetching_events_for_selected_day"),
            "pick_day_events_results_title",
            self._show_pick_day_events_result_for_loaded_events,
            thread_name="GCRListEventsForPickedDayThread",
        )

    def _show_pick_day_events_result_for_loaded_events(self, target_date, events):
        preview_text = self._format_daily_preview_text(target_date, events)

        dialog = DailyEventsResultDialog(
            self._get_dialog_parent(),
            title=self._t("pick_day_events_results_title"),
            message=preview_text,
            ok_label=self._t("dialog_ok"),
            other_day_label=self._t("pick_day_events_other_day_label"),
            edit_label=self._t("edit_event_open_label"),
            delete_label=self._t("delete_event_open_label"),
            add_label=self._t("add_event_open_label"),
            add_enabled=True,
            management_enabled=bool(events),
        )
        try:
            result_code = self._show_modal_dialog(dialog)
        finally:
            dialog.Destroy()

        if result_code == DailyEventsResultDialog.RESULT_ADD:
            self._show_add_event_dialog(default_date=target_date)
            return
        if result_code == DailyEventsResultDialog.RESULT_EDIT:
            self._show_edit_event_dialog_for_loaded_events(target_date, events)
            return
        if result_code == DailyEventsResultDialog.RESULT_DELETE:
            self._show_delete_event_dialog_for_loaded_events(target_date, events)
            return
        if result_code == DailyEventsResultDialog.RESULT_OTHER_DAY:
            next_date = self._parse_event_day_dialog("pick_day_events_dialog_title")
            if next_date is not None:
                self._show_pick_day_events_dialog_for_date(next_date)
            return

    def _handle_login_status(self):
        try:
            from . import googleAuth
        except Exception as e:
            self._show_message(
                self._t("import_error_googleauth", error=e),
                self._t("googleauth_import_error_title"),
            )
            return

        if not googleAuth.has_client_secret():
            self._show_message(
                self._t("missing_client_secret"),
                self._t("missing_client_secret_title"),
            )
            return

        if googleAuth.is_logged_in():
            self._show_status_dialog_with_checkbox()
            return

        if self._login_in_progress:
            self._show_readonly_dialog(
                self._t("login_in_progress_title"),
                self._t("login_in_progress_text"),
            )
            return

        if self._last_login_result is not None:
            if self._last_login_result.get("ok") and googleAuth.is_logged_in():
                self._show_status_dialog_with_checkbox()
                return

            self._show_readonly_dialog(
                self._t("login_failed_title"),
                self._last_login_result.get("text", self._t("login_failed_text")),
            )
            return

        dialog = ConfirmDialog(
            self._get_dialog_parent(),
            title=self._t("login_dialog_title"),
            message=self._t("login_dialog_text"),
            ok_label=self._t("dialog_ok"),
            cancel_label=self._t("dialog_cancel"),
        )

        try:
            result = self._show_modal_dialog(dialog)
        finally:
            dialog.Destroy()

        if result != wx.ID_OK:
            self._show_readonly_dialog(
                self._t("login_cancelled_title"),
                self._t("login_cancelled_text"),
            )
            return

        self._start_login_thread()

    @scriptHandler.script(
        description=t("script_layer_desc", get_ui_language()),
        gesture="kb:NVDA+shift+g"
    )
    def script_activateLayer(self, gesture):
        self._activate_layer()

    @scriptHandler.script(
        description=t("script_add_event_desc", get_ui_language()),
        gesture="kb:NVDA+control+shift+n"
    )
    def script_addEvent(self, gesture):
        wx.CallAfter(self._show_add_event_dialog)

    @scriptHandler.script(
        description=t("script_edit_event_desc", get_ui_language()),
        gesture="kb:NVDA+control+shift+e"
    )
    def script_editEvent(self, gesture):
        wx.CallAfter(self._show_edit_event_dialog)

    @scriptHandler.script(
        description=t("script_delete_event_desc", get_ui_language()),
        gesture="kb:NVDA+control+shift+u"
    )
    def script_deleteEvent(self, gesture):
        wx.CallAfter(self._show_delete_event_dialog)

    def script_layerLoginStatus(self, gesture):
        wx.CallAfter(self._handle_login_status)

    def script_layerDay1(self, gesture):
        self._read_events_for_offset(0)

    def script_layerDay2(self, gesture):
        self._read_events_for_offset(1)

    def script_layerDay3(self, gesture):
        self._read_events_for_offset(2)

    def script_layerDay4(self, gesture):
        self._read_events_for_offset(3)

    def script_layerDay5(self, gesture):
        self._read_events_for_offset(4)

    def script_layerDay6(self, gesture):
        self._read_events_for_offset(5)

    def script_layerDay7(self, gesture):
        self._read_events_for_offset(6)

    def script_layerToggleSpeechMode(self, gesture):
        try:
            from . import settings
        except Exception as e:
            ui.message(self._t("import_error_settings", error=e))
            return

        new_mode = settings.toggle_speech_mode()
        if new_mode == "full":
            ui.message(self._t("mode_full"))
        else:
            ui.message(self._t("mode_short"))

    def script_layerSelectCalendars(self, gesture):
        wx.CallAfter(self._show_calendar_selection_dialog)

    def script_layerAddEvent(self, gesture):
        wx.CallAfter(self._show_add_event_dialog)

    def script_layerEditEvent(self, gesture):
        wx.CallAfter(self._show_edit_event_dialog)

    def script_layerDeleteEvent(self, gesture):
        wx.CallAfter(self._show_delete_event_dialog)

    def script_layerPickDayPreview(self, gesture):
        wx.CallAfter(self._show_pick_day_events_dialog)

    def script_layerSearchEvents(self, gesture):
        wx.CallAfter(self._show_search_events_dialog)

    def script_layerHelp(self, gesture):
        wx.CallAfter(self._show_shortcuts_dialog)