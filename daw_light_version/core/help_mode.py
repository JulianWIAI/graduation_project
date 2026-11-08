"""
"? HELP" mode — explanation bubbles like in the Catalogue Manager.

    help ON   → hovering an element shows its explanation (title + text from
                core/help_texts.py); elements without one show their short tooltip.
    help OFF  → only the short tooltips (common in DAWs, e.g. Logic "Quick Help").

Mark an element with   set_help(widget, "key").  Child widgets inherit the
explanation of the nearest marked parent (e.g. all controls of a mixer strip).
"""
from __future__ import annotations

from html import escape
from typing import Callable
import os
import weakref

from PySide6.QtCore import QEvent, QObject, QPoint, QRect, QSettings, Qt
from PySide6.QtWidgets import (
    QAbstractButton, QAbstractSpinBox, QApplication, QComboBox, QTabBar, QToolTip, QWidget,
)

from .help_texts import help_for

_PROP = "helpKey"
_SETTINGS = ("SBS", "SynthMaster")
_SETTINGS_KEY = "help_enabled"
# Diagnosis: start with  BC_HELP_DEBUG=1 python main.py  to print every help lookup.
_DEBUG = os.environ.get("BC_HELP_DEBUG") == "1"


# Controls that show the "?" cursor while help is on (big canvases keep their
# own cursors, e.g. the pencil in the piano roll).
_CURSOR_TYPES = (QAbstractButton, QAbstractSpinBox, QComboBox)
_registered: "weakref.WeakSet[QWidget]" = weakref.WeakSet()
_current_mode: "HelpMode | None" = None


def set_help(widget: QWidget, key: str) -> None:
    """Attach the explanation *key* (see help_texts.HELP) to *widget*."""
    widget.setProperty(_PROP, key)
    _registered.add(widget)
    if _current_mode is not None:
        _current_mode.apply_cursor(widget)


class HelpMode(QObject):
    def __init__(self, get_lang: Callable[[], str], parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._get_lang = get_lang
        self.enabled: bool = QSettings(*_SETTINGS).value(_SETTINGS_KEY, True, type=bool)

    def set_enabled(self, on: bool) -> None:
        self.enabled = on
        QSettings(*_SETTINGS).setValue(_SETTINGS_KEY, on)
        if not on:
            QToolTip.hideText()
        for w in list(_registered):
            self.apply_cursor(w)

    def apply_cursor(self, widget: QWidget) -> None:
        """Help on → question-mark cursor over explained controls."""
        if isinstance(widget, _CURSOR_TYPES):
            if self.enabled:
                widget.setCursor(Qt.WhatsThisCursor)
            else:
                widget.unsetCursor()

    def eventFilter(self, obj, event) -> bool:  # noqa: N802 (Qt API)
        if not self.enabled or event.type() != QEvent.ToolTip or not isinstance(obj, QWidget):
            return False
        # The tooltip event can arrive at a parent (e.g. a scroll area) when the
        # child under the mouse ignores mouse moves — so always use the widget
        # that is really under the cursor.
        target = QApplication.widgetAt(event.globalPos()) or obj
        key = self._key_for(target, target.mapFromGlobal(event.globalPos()))
        obj = target
        if _DEBUG:
            print(f"[help] {type(target).__name__} -> {key!r}", flush=True)
        found = help_for(key, self._get_lang()) if key else None
        if not found:
            return False                         # normal short tooltip
        title, text = found
        # Qt styles a tooltip with the stylesheet of the widget passed in
        # (e.g. a dim caption colour) — so pass the main window, which only
        # has the app-wide theme, and limit the bubble to the hovered area.
        win = obj.window()
        area = QRect(obj.mapTo(win, QPoint(0, 0)), obj.size())
        QToolTip.showText(event.globalPos(),
                          f"<b>{escape(title)}</b><br>{escape(text)}", win, area)
        return True

    @staticmethod
    def _key_for(obj: QWidget, pos) -> str | None:
        """Help key for the hovered spot.

        1. tab bars: key stored per tab (setTabData),
        2. custom-drawn widgets: obj.help_key_at(pos) for regions (header, ruler …),
        3. otherwise the nearest widget (or parent) marked with set_help().
        """
        if isinstance(obj, QTabBar):
            i = obj.tabAt(pos)
            data = obj.tabData(i) if i >= 0 else None
            return str(data) if data else None
        region = getattr(obj, "help_key_at", None)
        if callable(region):
            key = region(pos)
            if key:
                return key
        w = obj
        while w is not None:
            key = w.property(_PROP)
            if key:
                return str(key)
            w = w.parentWidget()
        return None



def install(app, get_lang: Callable[[], str]) -> HelpMode:
    global _current_mode
    mode = HelpMode(get_lang, app)
    app.installEventFilter(mode)
    _current_mode = mode
    return mode
