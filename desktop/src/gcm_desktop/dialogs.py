from __future__ import annotations

import datetime as dt

import wx

from gcm_core.i18n import (
    get_language,
    language_choice_labels,
    language_choice_values,
    localized,
    normalize_language_preference,
    tr,
)
from gcm_core.models import (
    CalendarEvent,
    CalendarInfo,
    EventDraft,
    RecurrenceSettings,
    SearchCriteria,
    count_text,
    format_full_date,
    format_short_date,
    parse_date_input,
    parse_time_input,
    recurrence_choices,
    recurrence_mode_from_index,
    recurrence_mode_index,
)

from .accessibility import apply_accessible_name


def _alt(polish_key: str, english_key: str) -> str:
    return f"Alt+{polish_key if get_language() == 'pl' else english_key}"


class EventCreateDialog(wx.Dialog):
    def __init__(
        self,
        parent: wx.Window,
        calendars: list[CalendarInfo],
        default_date: dt.date,
        *,
        initial_event: CalendarEvent | None = None,
        title: str | None = None,
        editing: bool = False,
        allow_recurrence_edit: bool = True,
    ) -> None:
        super().__init__(
            parent,
            title=title or tr("Dodaj wydarzenie"),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
        )
        self._calendars = calendars
        self._draft: EventDraft | None = None
        self._accessible_objects: list[wx.Accessible] = []
        self._initial_event = initial_event
        self._allow_recurrence_edit = bool(allow_recurrence_edit)
        self._editing = bool(editing)

        initial_draft = initial_event.to_draft() if initial_event else None
        form_date = initial_draft.start_date if initial_draft else default_date
        end_date = initial_draft.end_date_inclusive if initial_draft else default_date

        sizer = wx.BoxSizer(wx.VERTICAL)
        form = wx.FlexGridSizer(cols=2, vgap=8, hgap=12)
        form.AddGrowableCol(1, 1)

        self.title_ctrl = wx.TextCtrl(
            self,
            value=initial_draft.title if initial_draft else "",
        )

        calendar_labels = [
            calendar.name
            + (
                f", {tr('kalendarz główny')}"
                if calendar.primary
                else ""
            )
            for calendar in calendars
        ]
        self.calendar_ctrl = wx.Choice(self, choices=calendar_labels)
        default_index = 0
        if initial_draft:
            default_index = next(
                (
                    index
                    for index, calendar in enumerate(calendars)
                    if calendar.calendar_id == initial_draft.calendar_id
                ),
                0,
            )
        else:
            default_index = next(
                (index for index, calendar in enumerate(calendars) if calendar.primary),
                0,
            )
        if calendars:
            self.calendar_ctrl.SetSelection(default_index)

        self.start_date_ctrl = wx.TextCtrl(
            self,
            value=format_short_date(form_date),
        )
        self.all_day_ctrl = wx.CheckBox(self, label=tr("Wydarzenie całodniowe"))
        self.all_day_ctrl.SetValue(initial_draft.all_day if initial_draft else False)

        start_time = (
            initial_draft.start_time.strftime("%H:%M")
            if initial_draft and initial_draft.start_time
            else "09:00"
        )
        self.start_time_ctrl = wx.TextCtrl(self, value=start_time)
        self.end_date_ctrl = wx.TextCtrl(self, value=format_short_date(end_date))
        end_time = (
            initial_draft.end_time.strftime("%H:%M")
            if initial_draft and initial_draft.end_time
            else "10:00"
        )
        self.end_time_ctrl = wx.TextCtrl(self, value=end_time)

        self.recurrence_ctrl = wx.Choice(
            self,
            choices=[label for _mode, label in recurrence_choices()],
        )
        initial_recurrence = (
            initial_draft.recurrence if initial_draft else RecurrenceSettings()
        )
        self.recurrence_ctrl.SetSelection(
            recurrence_mode_index(initial_recurrence.mode)
        )
        if not self._allow_recurrence_edit:
            self.recurrence_ctrl.SetSelection(0)

        self.recurrence_no_end_ctrl = wx.CheckBox(
            self,
            label=tr("Bez daty zakończenia cyklu"),
        )
        self.recurrence_no_end_ctrl.SetValue(
            bool(
                initial_recurrence.is_recurring
                and initial_recurrence.end_date_inclusive is None
            )
        )
        default_recurrence_end = initial_recurrence.end_date_inclusive
        if default_recurrence_end is None:
            try:
                default_recurrence_end = form_date.replace(year=form_date.year + 1)
            except ValueError:
                default_recurrence_end = form_date + dt.timedelta(days=365)
        self.recurrence_end_date_ctrl = wx.TextCtrl(
            self,
            value=format_short_date(default_recurrence_end),
        )

        self.location_ctrl = wx.TextCtrl(
            self,
            value=initial_draft.location if initial_draft else "",
        )
        self.description_ctrl = wx.TextCtrl(
            self,
            value=initial_draft.description if initial_draft else "",
            style=wx.TE_MULTILINE,
        )
        self.description_ctrl.SetMinSize((460, 110))

        calendar_help = (
            tr(
                "Kalendarz tego wydarzenia. Przenoszenie między kalendarzami nie jest jeszcze dostępne."
            )
            if initial_event
            else tr("Wybierz kalendarz, w którym wydarzenie zostanie zapisane.")
        )
        self._name_control(
            self.title_ctrl,
            tr("Tytuł wydarzenia"),
            tr("Wpisz nazwę wydarzenia."),
        )
        self._name_control(
            self.calendar_ctrl,
            tr("Kalendarz wydarzenia") if initial_event else tr("Kalendarz docelowy"),
            calendar_help,
        )
        self._name_control(
            self.start_date_ctrl,
            tr("Data rozpoczęcia, DD.MM.RRRR lub RRRR-MM-DD"),
            tr(
                "Wpisz datę rozpoczęcia w formacie dzień, miesiąc, rok albo w formacie ISO."
            ),
        )
        self._name_control(
            self.all_day_ctrl,
            tr("Wydarzenie całodniowe"),
            tr("Zaznacz, aby pominąć godziny rozpoczęcia i zakończenia."),
        )
        self._name_control(
            self.start_time_ctrl,
            tr("Godzina rozpoczęcia, GG:MM"),
            tr(
                "Wpisz godzinę rozpoczęcia w formacie godzina, dwukropek, minuty."
            ),
        )
        self._name_control(
            self.end_date_ctrl,
            tr("Data zakończenia włącznie, DD.MM.RRRR lub RRRR-MM-DD"),
            tr("Wpisz ostatni dzień wydarzenia."),
        )
        self._name_control(
            self.end_time_ctrl,
            tr("Godzina zakończenia, GG:MM"),
            tr(
                "Wpisz godzinę zakończenia w formacie godzina, dwukropek, minuty."
            ),
        )
        self._name_control(
            self.recurrence_ctrl,
            tr("Powtarzanie wydarzenia"),
            tr("Wybierz prosty rodzaj cyklu albo wydarzenie jednorazowe."),
        )
        self._name_control(
            self.recurrence_no_end_ctrl,
            tr("Bez daty zakończenia cyklu"),
            tr("Zaznacz, aby cykl nie miał określonej daty końcowej."),
        )
        self._name_control(
            self.recurrence_end_date_ctrl,
            tr(
                "Data zakończenia cyklu włącznie, DD.MM.RRRR lub RRRR-MM-DD"
            ),
            tr("Wpisz ostatni dzień, w którym cykl może utworzyć wystąpienie."),
        )
        self._name_control(
            self.location_ctrl,
            tr("Lokalizacja"),
            tr("Wpisz miejsce wydarzenia albo pozostaw pole puste."),
        )
        self._name_control(
            self.description_ctrl,
            tr("Opis wydarzenia"),
            tr("Wpisz dodatkowy opis albo pozostaw pole puste."),
        )

        def add_row(label: str, control: wx.Window) -> None:
            form.Add(wx.StaticText(self, label=label), 0, wx.ALIGN_CENTER_VERTICAL)
            form.Add(control, 1, wx.EXPAND)

        add_row(tr("Tytuł:"), self.title_ctrl)
        add_row(tr("Kalendarz:"), self.calendar_ctrl)
        add_row(
            tr("Data rozpoczęcia, DD.MM.RRRR lub RRRR-MM-DD:"),
            self.start_date_ctrl,
        )
        form.Add(
            wx.StaticText(self, label=tr("Typ wydarzenia:")),
            0,
            wx.ALIGN_CENTER_VERTICAL,
        )
        form.Add(self.all_day_ctrl, 1, wx.EXPAND)
        add_row(tr("Godzina rozpoczęcia, GG:MM:"), self.start_time_ctrl)
        add_row(
            tr("Data zakończenia włącznie, DD.MM.RRRR lub RRRR-MM-DD:"),
            self.end_date_ctrl,
        )
        add_row(tr("Godzina zakończenia, GG:MM:"), self.end_time_ctrl)
        add_row(tr("Powtarzanie:"), self.recurrence_ctrl)
        form.Add(
            wx.StaticText(self, label=tr("Zakończenie cyklu:")),
            0,
            wx.ALIGN_CENTER_VERTICAL,
        )
        form.Add(self.recurrence_no_end_ctrl, 1, wx.EXPAND)
        add_row(
            tr(
                "Data zakończenia cyklu włącznie, DD.MM.RRRR lub RRRR-MM-DD:"
            ),
            self.recurrence_end_date_ctrl,
        )
        add_row(tr("Lokalizacja:"), self.location_ctrl)
        add_row(tr("Opis:"), self.description_ctrl)
        sizer.Add(form, 1, wx.ALL | wx.EXPAND, 12)

        buttons = wx.StdDialogButtonSizer()
        if self._editing:
            button_label = localized("&Zapisz zmiany", "&Save changes")
            button_name = tr("Zapisz zmiany")
            button_shortcut = _alt("Z", "S")
        else:
            button_label = localized("&Utwórz wydarzenie", "&Create event")
            button_name = tr("Utwórz wydarzenie")
            button_shortcut = _alt("U", "C")
        self.save_button = wx.Button(self, wx.ID_OK, button_label)
        self.cancel_button = wx.Button(
            self,
            wx.ID_CANCEL,
            localized("&Anuluj", "&Cancel"),
        )
        self._name_control(
            self.save_button,
            button_name,
            tr("Zatwierdza dane w formularzu."),
            button_shortcut,
        )
        self._name_control(
            self.cancel_button,
            tr("Anuluj"),
            tr("Zamyka formularz bez zapisywania zmian."),
            _alt("A", "C"),
        )
        self.save_button.SetDefault()
        buttons.AddButton(self.save_button)
        buttons.AddButton(self.cancel_button)
        buttons.Realize()
        sizer.Add(buttons, 0, wx.ALL | wx.ALIGN_RIGHT, 12)

        self.SetSizerAndFit(sizer)
        self.SetMinSize((700, 650))
        self.SetSize((790, 740))
        self.CentreOnParent()

        self.all_day_ctrl.Bind(wx.EVT_CHECKBOX, self._on_all_day)
        self.recurrence_ctrl.Bind(wx.EVT_CHOICE, self._on_recurrence_changed)
        self.recurrence_no_end_ctrl.Bind(
            wx.EVT_CHECKBOX,
            self._on_recurrence_changed,
        )
        self.save_button.Bind(wx.EVT_BUTTON, self._on_save)
        self._apply_all_day_state()
        self._apply_recurrence_state()
        wx.CallAfter(self.title_ctrl.SetFocus)

    def _name_control(
        self,
        control: wx.Window,
        name: str,
        description: str = "",
        keyboard_shortcut: str = "",
    ) -> None:
        accessible = apply_accessible_name(
            control,
            name,
            description,
            keyboard_shortcut,
        )
        if accessible is not None:
            self._accessible_objects.append(accessible)

    def _apply_all_day_state(self) -> None:
        enabled = not self.all_day_ctrl.GetValue()
        self.start_time_ctrl.Enable(enabled)
        self.end_time_ctrl.Enable(enabled)

    def _on_all_day(self, event: wx.CommandEvent) -> None:
        self._apply_all_day_state()
        event.Skip()

    def _apply_recurrence_state(self) -> None:
        self.recurrence_ctrl.Enable(self._allow_recurrence_edit)
        recurring = (
            self._allow_recurrence_edit
            and recurrence_mode_from_index(self.recurrence_ctrl.GetSelection())
            != "none"
        )
        self.recurrence_no_end_ctrl.Enable(recurring)
        self.recurrence_end_date_ctrl.Enable(
            recurring and not self.recurrence_no_end_ctrl.GetValue()
        )

    def _on_recurrence_changed(self, event: wx.CommandEvent) -> None:
        self._apply_recurrence_state()
        event.Skip()

    def _show_error(self, text: str, control: wx.Window | None = None) -> None:
        dialog = wx.MessageDialog(
            self,
            text,
            tr("Nieprawidłowe dane"),
            wx.OK | wx.ICON_ERROR,
        )
        try:
            dialog.ShowModal()
        finally:
            dialog.Destroy()
        if control is not None:
            control.SetFocus()

    def _on_save(self, event: wx.CommandEvent) -> None:
        title = self.title_ctrl.GetValue().strip()
        if not title:
            self._show_error(tr("Wpisz tytuł wydarzenia."), self.title_ctrl)
            return

        calendar_index = self.calendar_ctrl.GetSelection()
        if not 0 <= calendar_index < len(self._calendars):
            self._show_error(tr("Wybierz kalendarz."), self.calendar_ctrl)
            return

        try:
            start_date = parse_date_input(self.start_date_ctrl.GetValue())
        except ValueError as error:
            self._show_error(str(error), self.start_date_ctrl)
            return
        try:
            end_date = parse_date_input(self.end_date_ctrl.GetValue())
        except ValueError as error:
            self._show_error(str(error), self.end_date_ctrl)
            return

        all_day = self.all_day_ctrl.GetValue()
        start_time = None
        end_time = None
        if not all_day:
            try:
                start_time = parse_time_input(self.start_time_ctrl.GetValue())
            except ValueError as error:
                self._show_error(str(error), self.start_time_ctrl)
                return
            try:
                end_time = parse_time_input(self.end_time_ctrl.GetValue())
            except ValueError as error:
                self._show_error(str(error), self.end_time_ctrl)
                return

        recurrence_mode = "none"
        recurrence_end = None
        if self._allow_recurrence_edit:
            recurrence_mode = recurrence_mode_from_index(
                self.recurrence_ctrl.GetSelection()
            )
            if recurrence_mode != "none" and not self.recurrence_no_end_ctrl.GetValue():
                try:
                    recurrence_end = parse_date_input(
                        self.recurrence_end_date_ctrl.GetValue()
                    )
                except ValueError as error:
                    self._show_error(str(error), self.recurrence_end_date_ctrl)
                    return

        calendar = self._calendars[calendar_index]
        draft = EventDraft(
            calendar_id=calendar.calendar_id,
            title=title,
            all_day=all_day,
            start_date=start_date,
            end_date_inclusive=end_date,
            start_time=start_time,
            end_time=end_time,
            location=self.location_ctrl.GetValue().strip(),
            description=self.description_ctrl.GetValue().strip(),
            recurrence=RecurrenceSettings(
                mode=recurrence_mode,
                end_date_inclusive=recurrence_end,
            ),
        )
        try:
            draft.validate()
        except ValueError as error:
            self._show_error(str(error))
            return

        self._draft = draft
        self.EndModal(wx.ID_OK)

    def get_draft(self) -> EventDraft | None:
        return self._draft


class EventEditDialog(EventCreateDialog):
    def __init__(
        self,
        parent: wx.Window,
        calendar: CalendarInfo,
        event: CalendarEvent,
        *,
        allow_recurrence_edit: bool = False,
    ) -> None:
        super().__init__(
            parent,
            [calendar],
            event.start_date,
            initial_event=event,
            title=tr("Edytuj wydarzenie"),
            editing=True,
            allow_recurrence_edit=allow_recurrence_edit,
        )


class RestartRequiredDialog(wx.Dialog):
    def __init__(self, parent: wx.Window) -> None:
        super().__init__(
            parent,
            title=tr("Ponowne uruchomienie PT Calendar Manager"),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
        )
        self._accessible_objects: list[wx.Accessible] = []

        sizer = wx.BoxSizer(wx.VERTICAL)
        message = wx.TextCtrl(
            self,
            value=tr(
                "Język aplikacji zostanie zmieniony. Aby zastosować nowe ustawienie, PT Calendar Manager musi zostać uruchomiony ponownie.\n\nWybierz „Uruchom ponownie teraz”, aby zamknąć i ponownie uruchomić aplikację, albo „Później”, aby zastosować zmianę przy następnym uruchomieniu."
            ),
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_DONTWRAP,
        )
        message.SetMinSize((620, 150))
        accessible = apply_accessible_name(
            message,
            tr("Ponowne uruchomienie PT Calendar Manager"),
        )
        if accessible is not None:
            self._accessible_objects.append(accessible)
        sizer.Add(message, 1, wx.ALL | wx.EXPAND, 12)

        buttons = wx.BoxSizer(wx.HORIZONTAL)
        self.restart_button = wx.Button(
            self,
            wx.ID_OK,
            localized("&Uruchom ponownie teraz", "&Restart now"),
        )
        self.later_button = wx.Button(
            self,
            wx.ID_CANCEL,
            localized("&Później", "&Later"),
        )
        self.restart_button.SetDefault()

        for control, name, shortcut, description in (
            (
                self.restart_button,
                tr("Uruchom ponownie teraz"),
                _alt("U", "R"),
                tr(
                    "Zamyka bieżącą instancję i uruchamia PT Calendar Manager ponownie w wybranym języku."
                ),
            ),
            (
                self.later_button,
                tr("Później"),
                _alt("P", "L"),
                tr(
                    "Pozostawia aplikację otwartą. Nowy język zostanie zastosowany przy następnym uruchomieniu."
                ),
            ),
        ):
            accessible = apply_accessible_name(
                control,
                name,
                description,
                shortcut,
            )
            if accessible is not None:
                self._accessible_objects.append(accessible)

        buttons.Add(self.restart_button, 0, wx.RIGHT, 8)
        buttons.Add(self.later_button, 0)
        sizer.Add(buttons, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.ALIGN_RIGHT, 12)

        self.SetSizerAndFit(sizer)
        self.SetMinSize((680, 290))
        self.CentreOnParent()
        wx.CallAfter(message.SetFocus)


class SettingsDialog(wx.Dialog):
    def __init__(
        self,
        parent: wx.Window,
        calendars: list[CalendarInfo],
        selected_ids: set[str],
        language_preference: str,
        google_logged_in: bool = False,
    ) -> None:
        super().__init__(
            parent,
            title=tr("Ustawienia aplikacji"),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
        )
        self._calendars = calendars
        self._original_selected_ids = set(selected_ids)
        self._checkboxes: list[wx.CheckBox] = []
        self._accessible_objects: list[wx.Accessible] = []
        self._language_values = language_choice_values()

        sizer = wx.BoxSizer(wx.VERTICAL)
        form = wx.FlexGridSizer(cols=2, vgap=10, hgap=12)
        form.AddGrowableCol(1, 1)

        self.language_ctrl = wx.Choice(
            self,
            choices=list(language_choice_labels()),
        )
        normalized = normalize_language_preference(language_preference)
        try:
            language_index = self._language_values.index(normalized)
        except ValueError:
            language_index = 0
        self.language_ctrl.SetSelection(language_index)
        accessible = apply_accessible_name(
            self.language_ctrl,
            tr("Język aplikacji"),
            tr("Język zostanie zmieniony po ponownym uruchomieniu aplikacji."),
        )
        if accessible is not None:
            self._accessible_objects.append(accessible)
        form.Add(
            wx.StaticText(self, label=f"{tr('Język aplikacji')}:") ,
            0,
            wx.ALIGN_CENTER_VERTICAL,
        )
        form.Add(self.language_ctrl, 1, wx.EXPAND)
        sizer.Add(form, 0, wx.ALL | wx.EXPAND, 12)

        calendar_box = wx.StaticBoxSizer(
            wx.VERTICAL,
            self,
            tr("Kalendarze"),
        )
        if calendars:
            info = wx.StaticText(
                self,
                label=tr(
                    "Zaznacz kalendarze, których wydarzenia mają być pokazywane."
                ),
            )
            info.Wrap(560)
            calendar_box.Add(info, 0, wx.ALL | wx.EXPAND, 8)

            panel = wx.ScrolledWindow(
                self,
                style=wx.VSCROLL | wx.TAB_TRAVERSAL,
            )
            panel.SetScrollRate(0, 20)
            panel_sizer = wx.BoxSizer(wx.VERTICAL)
            for calendar in calendars:
                label = calendar.name + (
                    f", {tr('kalendarz główny')}" if calendar.primary else ""
                )
                checkbox = wx.CheckBox(panel, label=label)
                checkbox.SetName(label)
                checkbox.SetValue(calendar.calendar_id in selected_ids)
                self._checkboxes.append(checkbox)
                panel_sizer.Add(checkbox, 0, wx.ALL | wx.EXPAND, 6)
            panel.SetSizer(panel_sizer)
            panel.SetMinSize((580, 280))
            calendar_box.Add(panel, 1, wx.ALL | wx.EXPAND, 8)
        else:
            empty_calendar_message = (
                tr(
                    "Nie udało się jeszcze pobrać listy kalendarzy. Ustawienie języka pozostaje dostępne. Po przywróceniu połączenia zamknij Ustawienia, użyj Odśwież i otwórz Ustawienia ponownie."
                )
                if google_logged_in
                else tr(
                    "Zaloguj się do Google, aby wybrać kalendarze. Ustawienie języka jest dostępne bez logowania."
                )
            )
            info = wx.StaticText(
                self,
                label=empty_calendar_message,
            )
            info.Wrap(560)
            calendar_box.Add(info, 0, wx.ALL | wx.EXPAND, 12)
        sizer.Add(calendar_box, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 12)

        buttons = wx.StdDialogButtonSizer()
        self.save_button = wx.Button(
            self,
            wx.ID_OK,
            localized("&Zapisz", "&Save"),
        )
        self.cancel_button = wx.Button(
            self,
            wx.ID_CANCEL,
            localized("&Anuluj", "&Cancel"),
        )
        for control, name, shortcut, description in (
            (
                self.save_button,
                tr("Zapisz"),
                _alt("Z", "S"),
                tr("Zapisuje ustawienia aplikacji."),
            ),
            (
                self.cancel_button,
                tr("Anuluj"),
                _alt("A", "C"),
                tr("Zamyka ustawienia bez zapisywania zmian."),
            ),
        ):
            accessible = apply_accessible_name(
                control,
                name,
                description,
                shortcut,
            )
            if accessible is not None:
                self._accessible_objects.append(accessible)
        self.save_button.SetDefault()
        buttons.AddButton(self.save_button)
        buttons.AddButton(self.cancel_button)
        buttons.Realize()
        sizer.Add(buttons, 0, wx.ALL | wx.ALIGN_RIGHT, 12)

        self.SetSizerAndFit(sizer)
        self.SetMinSize((650, 430))
        self.SetSize((700, 520))
        self.CentreOnParent()
        self.save_button.Bind(wx.EVT_BUTTON, self._on_save)
        wx.CallAfter(
            (
                self.language_ctrl
                if not self._checkboxes
                else self.language_ctrl
            ).SetFocus
        )

    def _on_save(self, event: wx.CommandEvent) -> None:
        if self._calendars and not self.selected_ids():
            wx.MessageBox(
                tr("Zaznacz co najmniej jeden kalendarz."),
                tr("Wybór kalendarzy"),
                wx.OK | wx.ICON_ERROR,
                self,
            )
            if self._checkboxes:
                self._checkboxes[0].SetFocus()
            return
        self.EndModal(wx.ID_OK)

    def selected_ids(self) -> list[str]:
        if not self._calendars:
            return list(self._original_selected_ids)
        return [
            calendar.calendar_id
            for calendar, checkbox in zip(self._calendars, self._checkboxes)
            if checkbox.GetValue()
        ]

    def language_preference(self) -> str:
        index = self.language_ctrl.GetSelection()
        if 0 <= index < len(self._language_values):
            return self._language_values[index]
        return self._language_values[0]


class SearchDialog(wx.Dialog):
    def __init__(
        self,
        parent: wx.Window,
        default_start: dt.date,
        default_end: dt.date,
    ) -> None:
        super().__init__(
            parent,
            title=tr("Wyszukaj wydarzenia"),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
        )
        self._criteria: SearchCriteria | None = None
        self._accessible_objects: list[wx.Accessible] = []

        sizer = wx.BoxSizer(wx.VERTICAL)
        intro = wx.StaticText(
            self,
            label=tr(
                "Wyszukiwanie obejmuje wybrane kalendarze Google. Data początkowa i końcowa należą do zakresu."
            ),
        )
        intro.Wrap(620)
        sizer.Add(intro, 0, wx.ALL | wx.EXPAND, 12)

        form = wx.FlexGridSizer(cols=2, vgap=10, hgap=12)
        form.AddGrowableCol(1, 1)
        self.query_ctrl = wx.TextCtrl(self)
        self.start_date_ctrl = wx.TextCtrl(
            self,
            value=format_short_date(default_start),
        )
        self.end_date_ctrl = wx.TextCtrl(
            self,
            value=format_short_date(default_end),
        )

        self._add_accessible_name(
            self.query_ctrl,
            tr("Szukany tekst"),
            tr("Wpisz fragment tytułu, opisu, lokalizacji albo nazwy kalendarza."),
        )
        self._add_accessible_name(
            self.start_date_ctrl,
            tr("Data początkowa wyszukiwania, DD.MM.RRRR lub RRRR-MM-DD"),
            tr("Pierwszy dzień zakresu wyszukiwania, podawany włącznie."),
        )
        self._add_accessible_name(
            self.end_date_ctrl,
            tr("Data końcowa wyszukiwania, DD.MM.RRRR lub RRRR-MM-DD"),
            tr("Ostatni dzień zakresu wyszukiwania, podawany włącznie."),
        )

        form.Add(
            wx.StaticText(self, label=tr("Szukany tekst:")),
            0,
            wx.ALIGN_CENTER_VERTICAL,
        )
        form.Add(self.query_ctrl, 1, wx.EXPAND)
        form.Add(
            wx.StaticText(
                self,
                label=tr("Data początkowa, DD.MM.RRRR lub RRRR-MM-DD:"),
            ),
            0,
            wx.ALIGN_CENTER_VERTICAL,
        )
        form.Add(self.start_date_ctrl, 1, wx.EXPAND)
        form.Add(
            wx.StaticText(
                self,
                label=tr("Data końcowa, DD.MM.RRRR lub RRRR-MM-DD:"),
            ),
            0,
            wx.ALIGN_CENTER_VERTICAL,
        )
        form.Add(self.end_date_ctrl, 1, wx.EXPAND)
        sizer.Add(form, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 12)

        note = wx.StaticText(
            self,
            label=tr(
                "Duży zakres może zawierać wiele wydarzeń, ale wyszukiwanie nie blokuje głównego okna."
            ),
        )
        note.Wrap(620)
        sizer.Add(note, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 12)

        buttons = wx.StdDialogButtonSizer()
        self.search_button = wx.Button(
            self,
            wx.ID_OK,
            localized("Wy&szukaj", "&Search"),
        )
        self.cancel_button = wx.Button(
            self,
            wx.ID_CANCEL,
            localized("&Anuluj", "&Cancel"),
        )
        self._add_accessible_name(
            self.search_button,
            tr("Wyszukaj"),
            tr("Rozpoczyna wyszukiwanie w podanym zakresie."),
            _alt("S", "S"),
        )
        self._add_accessible_name(
            self.cancel_button,
            tr("Anuluj"),
            tr("Zamyka formularz wyszukiwania."),
            _alt("A", "C"),
        )
        self.search_button.SetDefault()
        buttons.AddButton(self.search_button)
        buttons.AddButton(self.cancel_button)
        buttons.Realize()
        sizer.Add(buttons, 0, wx.ALL | wx.ALIGN_RIGHT, 12)

        self.SetSizerAndFit(sizer)
        self.SetMinSize((680, 330))
        self.SetSize((720, 370))
        self.CentreOnParent()
        self.search_button.Bind(wx.EVT_BUTTON, self._on_search)
        wx.CallAfter(self.query_ctrl.SetFocus)

    def _add_accessible_name(
        self,
        control: wx.Window,
        name: str,
        description: str,
        keyboard_shortcut: str = "",
    ) -> None:
        accessible = apply_accessible_name(
            control,
            name,
            description,
            keyboard_shortcut,
        )
        if accessible is not None:
            self._accessible_objects.append(accessible)

    def _on_search(self, event: wx.Event) -> None:
        try:
            criteria = SearchCriteria(
                query=self.query_ctrl.GetValue().strip(),
                start_date=parse_date_input(self.start_date_ctrl.GetValue()),
                end_date_inclusive=parse_date_input(self.end_date_ctrl.GetValue()),
            )
            criteria.validate()
        except ValueError as error:
            wx.MessageBox(
                str(error),
                tr("Nieprawidłowe dane wyszukiwania"),
                wx.OK | wx.ICON_ERROR,
                self,
            )
            return
        self._criteria = criteria
        self.EndModal(wx.ID_OK)

    def get_criteria(self) -> SearchCriteria | None:
        return self._criteria


class SearchResultsDialog(wx.Dialog):
    def __init__(
        self,
        parent: wx.Window,
        events: list[CalendarEvent],
        criteria: SearchCriteria,
    ) -> None:
        super().__init__(
            parent,
            title=tr("Wyniki wyszukiwania"),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
        )
        self._events = events
        self.selected_event: CalendarEvent | None = None
        self._accessible_objects: list[wx.Accessible] = []
        sizer = wx.BoxSizer(wx.VERTICAL)
        summary = wx.StaticText(
            self,
            label=tr(
                "Znaleziono: {count}. Zakres od {start} do {end} włącznie.",
                count=count_text(len(events)),
                start=format_short_date(criteria.start_date),
                end=format_short_date(criteria.end_date_inclusive),
            ),
        )
        summary.Wrap(700)
        sizer.Add(summary, 0, wx.ALL | wx.EXPAND, 12)
        choices = [
            f"{format_full_date(event.start_date)}, "
            f"{event.display_text(event.start_date)}"
            for event in events
        ]
        self.results = wx.ListBox(self, choices=choices, style=wx.LB_SINGLE)
        self.results.SetName(
            tr("Wyniki wyszukiwania, {count} elementów", count=len(events))
        )
        self.results.SetMinSize((680, 300))
        if events:
            self.results.SetSelection(0)
        sizer.Add(self.results, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 12)

        buttons = wx.StdDialogButtonSizer()
        self.open_button = wx.Button(
            self,
            wx.ID_OK,
            localized("&Przejdź do wydarzenia", "&Go to event"),
        )
        self.close_button = wx.Button(
            self,
            wx.ID_CANCEL,
            localized("&Zamknij", "&Close"),
        )
        for control, name, shortcut, description in (
            (
                self.open_button,
                tr("Przejdź do wydarzenia"),
                _alt("P", "G"),
                tr("Przechodzi do zaznaczonego wyniku w głównym oknie."),
            ),
            (
                self.close_button,
                tr("Zamknij"),
                _alt("Z", "C"),
                tr("Zamyka wyniki wyszukiwania."),
            ),
        ):
            accessible = apply_accessible_name(
                control,
                name,
                description,
                shortcut,
            )
            if accessible is not None:
                self._accessible_objects.append(accessible)
        self.open_button.Enable(bool(events))
        self.open_button.SetDefault()
        buttons.AddButton(self.open_button)
        buttons.AddButton(self.close_button)
        buttons.Realize()
        sizer.Add(buttons, 0, wx.ALL | wx.ALIGN_RIGHT, 12)
        self.SetSizerAndFit(sizer)
        self.SetSize((760, 460))
        self.CentreOnParent()
        self.open_button.Bind(wx.EVT_BUTTON, self._on_open)
        self.results.Bind(wx.EVT_LISTBOX_DCLICK, self._on_open)
        wx.CallAfter(
            (self.results if events else self.close_button).SetFocus
        )

    def _on_open(self, event: wx.Event) -> None:
        index = self.results.GetSelection()
        if 0 <= index < len(self._events):
            self.selected_event = self._events[index]
            self.EndModal(wx.ID_OK)


class MeetingLinkDialog(wx.Dialog):
    def __init__(
        self,
        parent: wx.Window,
        meeting_label: str,
        meeting_url: str,
    ) -> None:
        super().__init__(
            parent,
            title=tr("Link spotkania"),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
        )
        self.action = ""
        self._accessible_objects: list[wx.Accessible] = []

        sizer = wx.BoxSizer(wx.VERTICAL)
        provider = wx.StaticText(
            self,
            label=tr(
                "Rodzaj spotkania: {meeting}",
                meeting=meeting_label or tr("spotkanie online"),
            ),
        )
        sizer.Add(provider, 0, wx.ALL | wx.EXPAND, 12)

        url_ctrl = wx.TextCtrl(
            self,
            value=meeting_url,
            style=wx.TE_READONLY,
        )
        url_ctrl.SetMinSize((620, -1))
        accessible = apply_accessible_name(
            url_ctrl,
            tr("Adres spotkania"),
            tr("Adres można zaznaczyć i skopiować ręcznie."),
        )
        if accessible is not None:
            self._accessible_objects.append(accessible)
        sizer.Add(url_ctrl, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 12)

        buttons = wx.BoxSizer(wx.HORIZONTAL)
        self.open_button = wx.Button(
            self,
            label=localized("&Otwórz link", "&Open link"),
        )
        self.copy_button = wx.Button(
            self,
            label=localized("&Kopiuj link", "&Copy link"),
        )
        self.cancel_button = wx.Button(
            self,
            wx.ID_CANCEL,
            localized("&Anuluj", "&Cancel"),
        )
        self.open_button.SetDefault()

        for control, name, shortcut, description in (
            (
                self.open_button,
                tr("Otwórz link"),
                _alt("O", "O"),
                tr("Otwiera spotkanie w domyślnej przeglądarce."),
            ),
            (
                self.copy_button,
                tr("Kopiuj link"),
                _alt("K", "C"),
                tr("Kopiuje adres spotkania do schowka."),
            ),
            (
                self.cancel_button,
                tr("Anuluj"),
                _alt("A", "C"),
                tr("Zamyka okno bez wykonywania działania."),
            ),
        ):
            accessible = apply_accessible_name(
                control,
                name,
                description,
                shortcut,
            )
            if accessible is not None:
                self._accessible_objects.append(accessible)

        buttons.Add(self.open_button, 0, wx.RIGHT, 8)
        buttons.Add(self.copy_button, 0, wx.RIGHT, 8)
        buttons.Add(self.cancel_button, 0)
        sizer.Add(buttons, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.ALIGN_RIGHT, 12)

        self.SetSizerAndFit(sizer)
        self.SetMinSize((680, 220))
        self.CentreOnParent()
        self.open_button.Bind(wx.EVT_BUTTON, self._on_open)
        self.copy_button.Bind(wx.EVT_BUTTON, self._on_copy)
        wx.CallAfter(self.open_button.SetFocus)

    def _on_open(self, event: wx.Event) -> None:
        self.action = "open"
        self.EndModal(wx.ID_OK)

    def _on_copy(self, event: wx.Event) -> None:
        self.action = "copy"
        self.EndModal(wx.ID_OK)


class HelpDialog(wx.Dialog):
    def __init__(self, parent: wx.Window, help_text: str) -> None:
        super().__init__(
            parent,
            title=tr("Pomoc i skróty klawiaturowe"),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
        )
        self._accessible_objects: list[wx.Accessible] = []

        sizer = wx.BoxSizer(wx.VERTICAL)
        text = wx.TextCtrl(
            self,
            value=help_text,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_DONTWRAP,
        )
        text.SetMinSize((720, 440))
        accessible = apply_accessible_name(
            text,
            tr("Treść pomocy i lista skrótów"),
            tr("Czytaj strzałkami. Tekst można zaznaczać i kopiować."),
        )
        if accessible is not None:
            self._accessible_objects.append(accessible)
        sizer.Add(text, 1, wx.ALL | wx.EXPAND, 12)

        close_button = wx.Button(
            self,
            wx.ID_OK,
            localized("&Zamknij", "&Close"),
        )
        close_button.SetDefault()
        accessible = apply_accessible_name(
            close_button,
            tr("Zamknij"),
            tr("Zamyka pomoc i wraca do głównego okna."),
            _alt("Z", "C"),
        )
        if accessible is not None:
            self._accessible_objects.append(accessible)
        sizer.Add(
            close_button,
            0,
            wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.ALIGN_RIGHT,
            12,
        )

        self.SetSizerAndFit(sizer)
        self.SetMinSize((760, 520))
        self.SetSize((820, 600))
        self.CentreOnParent()
        wx.CallAfter(text.SetFocus)
