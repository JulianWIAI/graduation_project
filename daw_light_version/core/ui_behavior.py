"""
Application-wide UI behaviour.

WheelGuard: the mouse wheel over a slider, knob, spin box or combo box only changes
its value when that control has keyboard focus (i.e. was clicked first).  Otherwise
the wheel event goes to the surrounding scroll area, so scrolling through a panel
(e.g. EFFECTS) never changes settings by accident — the usual behaviour in DAWs.
"""
from __future__ import annotations

from PySide6.QtCore import QEvent, QObject
from PySide6.QtWidgets import QAbstractSlider, QAbstractSpinBox, QComboBox, QScrollBar

_GUARDED = (QAbstractSlider, QAbstractSpinBox, QComboBox)


class WheelGuard(QObject):
    def eventFilter(self, obj, event) -> bool:  # noqa: N802 (Qt API)
        if (event.type() == QEvent.Wheel
                and isinstance(obj, _GUARDED)
                and not isinstance(obj, QScrollBar)
                and not obj.hasFocus()):
            # Ignored + handled → Qt passes the event on to the parent widget.
            event.ignore()
            return True
        return False


def install(app) -> WheelGuard:
    """Install the guards on *app*; keep the returned object alive."""
    guard = WheelGuard(app)
    app.installEventFilter(guard)
    return guard
