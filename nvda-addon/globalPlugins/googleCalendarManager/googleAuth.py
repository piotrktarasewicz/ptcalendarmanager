import os
import sys
import importlib

from .i18n import get_runtime_language

try:
    from .paths import (
        LIB_DIR,
        CLIENT_SECRET_PATH,
        ERROR_PATH,
        ensure_user_data_dir,
    )
except Exception:
    BASE_DIR = os.path.dirname(__file__)
    if BASE_DIR not in sys.path:
        sys.path.insert(0, BASE_DIR)
    from paths import (  # type: ignore
        LIB_DIR,
        CLIENT_SECRET_PATH,
        ERROR_PATH,
        ensure_user_data_dir,
    )


if LIB_DIR not in sys.path:
    sys.path.insert(0, LIB_DIR)


def has_client_secret():
    return os.path.exists(CLIENT_SECRET_PATH)


def get_last_error():
    if not os.path.exists(ERROR_PATH):
        return ""
    try:
        with open(ERROR_PATH, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return ""


def _save_local_error(text):
    try:
        ensure_user_data_dir()
        with open(ERROR_PATH, "w", encoding="utf-8") as f:
            f.write(str(text or "").strip())
    except Exception:
        pass


def _get_ui_language():
    return get_runtime_language("en")


def _repair_email_package():
    email_package_dir = os.path.join(LIB_DIR, "email")
    email_mime_init = os.path.join(email_package_dir, "mime", "__init__.py")

    if not os.path.exists(email_mime_init):
        return

    try:
        loaded_email = sys.modules.get("email")
        needs_reload = False

        if loaded_email is None:
            needs_reload = True
        else:
            loaded_path = getattr(loaded_email, "__path__", None)
            if not loaded_path:
                needs_reload = True
            else:
                normalized_loaded = [
                    os.path.normcase(os.path.abspath(p))
                    for p in loaded_path
                ]
                normalized_expected = os.path.normcase(os.path.abspath(email_package_dir))
                if normalized_expected not in normalized_loaded:
                    needs_reload = True

        if needs_reload:
            for module_name in list(sys.modules.keys()):
                if module_name == "email" or module_name.startswith("email."):
                    del sys.modules[module_name]

            importlib.invalidate_caches()

        import email.mime  # noqa: F401

    except Exception as e:
        _save_local_error(f"email repair error: {repr(e)}")
        raise


def _helper():
    try:
        if LIB_DIR not in sys.path:
            sys.path.insert(0, LIB_DIR)

        _repair_email_package()

        from . import auth_helper
        return auth_helper

    except Exception as e:
        _save_local_error(f"_helper import error: {repr(e)}")
        raise


def is_logged_in():
    try:
        helper = _helper()
        creds = helper.ensure_valid_credentials()
        return creds is not None
    except Exception as e:
        _save_local_error(f"is_logged_in error: {repr(e)}")
        return False


def start_login():
    try:
        helper = _helper()
        result_code = helper.cmd_login()
        if result_code == 0:
            return {
                "ok": True,
                "text": "success",
            }

        error_text = helper.get_saved_error_text()
        return {
            "ok": False,
            "text": error_text or "Sign-in failed.",
        }
    except Exception as e:
        _save_local_error(f"start_login error: {repr(e)}")
        return {
            "ok": False,
            "text": str(e),
        }


def logout():
    try:
        helper = _helper()
        result_code = helper.cmd_logout()
        return result_code == 0
    except Exception as e:
        _save_local_error(f"logout error: {repr(e)}")
        return False


def get_calendars():
    try:
        helper = _helper()
        lang = _get_ui_language()
        return helper.api_list_calendars(lang)
    except Exception as e:
        _save_local_error(f"get_calendars error: {repr(e)}")
        return {
            "ok": False,
            "text": str(e),
        }


def get_events_for_day(days_ahead):
    try:
        helper = _helper()
        lang = _get_ui_language()
        return helper.api_events(days_ahead, lang)
    except Exception as e:
        _save_local_error(f"get_events_for_day error: {repr(e)}")
        return {
            "ok": False,
            "text": str(e),
        }


def list_events_for_edit(target_date_iso):
    try:
        helper = _helper()
        lang = _get_ui_language()
        return helper.api_list_events_for_edit(target_date_iso, lang)
    except Exception as e:
        _save_local_error(f"list_events_for_edit error: {repr(e)}")
        return {
            "ok": False,
            "text": str(e),
        }



def search_events(query, start_date_iso, end_date_iso):
    try:
        helper = _helper()
        lang = _get_ui_language()
        return helper.api_search_events(query, start_date_iso, end_date_iso, lang)
    except Exception as e:
        _save_local_error(f"search_events error: {repr(e)}")
        return {
            "ok": False,
            "text": str(e),
        }

def create_event(event_data):
    try:
        helper = _helper()
        lang = _get_ui_language()
        return helper.api_create_event(event_data, lang)
    except Exception as e:
        _save_local_error(f"create_event error: {repr(e)}")
        return {
            "ok": False,
            "text": str(e),
        }


def update_event(event_data):
    try:
        helper = _helper()
        lang = _get_ui_language()
        return helper.api_update_event(event_data, lang)
    except Exception as e:
        _save_local_error(f"update_event error: {repr(e)}")
        return {
            "ok": False,
            "text": str(e),
        }


def delete_event(event_data):
    try:
        helper = _helper()
        lang = _get_ui_language()
        return helper.api_delete_event(event_data, lang)
    except Exception as e:
        _save_local_error(f"delete_event error: {repr(e)}")
        return {
            "ok": False,
            "text": str(e),
        }