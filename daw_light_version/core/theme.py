"""
Central colour palette and Qt stylesheet of the DAW.

The colours follow the Catalogue Manager (Music_catalogue_manager_v.2/static/style.css),
so both apps look like one product (Beat Collage):
dark background, violet as the only accent, colour only where it carries meaning
(green = play/ok, red = record/danger, amber = warning).

Use the *semantic* keys in new code:
    bg, panel, field, raised        backgrounds (back → front)
    line, line_2                    borders (rgba strings)
    text, text_2, text_dim          text (strong → faint)
    accent, accent_hi, accent_lo    violet accent
    success, danger, warning, info  status colours

The older keys (void, abyss, deep, surface, cyan, pink, purple, lime, gold, orange)
still exist so code that has not been migrated keeps working; they now point to the
Catalogue Manager tones instead of the old neon colours.

C is mutated in place on a theme switch (C.update(palette)), so custom paintEvent()
code that reads C[...] while painting follows the theme automatically.
"""
from __future__ import annotations

from PySide6.QtGui import QColor


def _palette(*, bg, panel, field, raised, line, line_2, border, text, text_2, text_dim,
             accent, accent_hi, accent_lo, success, danger, warning, info, pink,
             orange, keys, grid, tracks) -> dict:
    """Build a palette with semantic keys plus the legacy aliases."""
    return {
        # semantic
        "bg": bg, "panel": panel, "field": field, "raised": raised,
        "line": line, "line_2": line_2,
        "text": text, "text_2": text_2, "text_dim": text_dim,
        "accent": accent, "accent_hi": accent_hi, "accent_lo": accent_lo,
        "success": success, "danger": danger, "warning": warning, "info": info,
        # legacy aliases (old names → new tones)
        "void": bg, "abyss": panel, "deep": field, "surface": raised,
        "cyan": accent_hi, "purple": accent, "pink": pink,
        "lime": success, "green": success, "gold": warning, "orange": orange,
        "dim": text_dim, "red": danger, "border": border,
        # piano roll
        "key_black": keys[0], "key_white_hi": keys[1], "key_white_lo": keys[2],
        "grid_black": grid[0], "grid_white": grid[1],
        # per-lane colours (distinct but softer than neon)
        "tracks": list(tracks),
    }


DARK_PALETTE: dict = _palette(
    bg="#08080d", panel="#0e0e18", field="#13131f", raised="#191926",
    line="rgba(255,255,255,0.07)", line_2="rgba(255,255,255,0.12)", border="#2a2840",
    text="#ede9fe", text_2="#9d99b8", text_dim="#5c5878",
    accent="#7c6dea", accent_hi="#a78bfa", accent_lo="#5b4fc4",
    success="#34d399", danger="#f87171", warning="#fbbf24", info="#22d3ee",
    pink="#f472b6", orange="#fb923c",
    keys=("#101019", "#232333", "#1a1a28"),
    grid=("#0b0b12", "#0f0f18"),
    tracks=("#a78bfa", "#22d3ee", "#f472b6", "#34d399", "#fbbf24", "#fb923c",
            "#38bdf8", "#f87171", "#2dd4bf", "#e879f9", "#a3e635", "#818cf8",
            "#fb7185", "#6ee7b7", "#fde047", "#60a5fa"),
)

LIGHT_PALETTE: dict = _palette(
    bg="#f6f5fb", panel="#eeecf6", field="#ffffff", raised="#e4e1f0",
    line="rgba(20,16,48,0.10)", line_2="rgba(20,16,48,0.18)", border="#d6d2e6",
    text="#1b1830", text_2="#55516f", text_dim="#8a86a3",
    accent="#6d5fd6", accent_hi="#5b4fc4", accent_lo="#4a3fb0",
    success="#059669", danger="#dc2626", warning="#b45309", info="#0891b2",
    pink="#db2777", orange="#ea580c",
    keys=("#1a1a22", "#ffffff", "#e8e6f0"),
    grid=("#e4e1f0", "#ffffff"),
    tracks=("#6d5fd6", "#0891b2", "#db2777", "#059669", "#b45309", "#ea580c",
            "#0284c7", "#dc2626", "#0d9488", "#c026d3", "#65a30d", "#4f46e5",
            "#e11d48", "#047857", "#a16207", "#2563eb"),
)

# Live palette — starts dark, MainWindow switches it with C.update(...)
C: dict = {k: (list(v) if isinstance(v, list) else v) for k, v in DARK_PALETTE.items()}


# ── helpers ────────────────────────────────────────────────────────────────

def _rgb(color: str) -> tuple[int, int, int]:
    h = color.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def mix(color: str, base: str, amount: float) -> str:
    """Opaque blend of *color* over *base* (amount 0..1) as '#rrggbb'.

    Used for borders: semi-transparent borders overlap at rounded corners and
    look pixelated, an opaque mixed colour stays smooth.
    """
    c, b = _rgb(color), _rgb(base)
    return "#" + "".join(f"{round(cv * amount + bv * (1 - amount)):02x}" for cv, bv in zip(c, b))


def rgba(color: str, alpha: float) -> str:
    """'#7c6dea', 0.2  →  'rgba(124,109,234,0.2)'  (for stylesheets)."""
    r, g, b = _rgb(color)
    return f"rgba({r},{g},{b},{alpha})"


def qcolor(color: str, alpha: int = 255) -> QColor:
    """Palette colour as QColor with optional alpha 0–255 (for paintEvent code)."""
    c = QColor(color)
    c.setAlpha(alpha)
    return c


def _arrow_icon(direction: str, color: str) -> str:
    """Small triangle (SVG) in *color* for spin-box arrows; returns a file path.

    Qt stylesheets can only draw arrows from image files, so the icon is written
    once per colour into a cache folder (follows the theme automatically).
    """
    import os
    import tempfile
    folder = os.path.join(tempfile.gettempdir(), "beat_collage_ui")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"arrow_{direction}_{color.lstrip('#')}.svg")
    if not os.path.exists(path):
        points = "1,7 5,2 9,7" if direction == "up" else "1,3 5,8 9,3"
        with open(path, "w", encoding="utf-8") as fh:
            fh.write('<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">'
                     f'<polygon points="{points}" fill="{color}"/></svg>')
    return path.replace("\\", "/")


# ── stylesheet ─────────────────────────────────────────────────────────────

def build_stylesheet(p: dict) -> str:
    """Complete application stylesheet for palette *p*.

    Buttons can opt into a style with a dynamic property, e.g.
        btn.setProperty("variant", "danger")
    Variants: primary, success, danger, warning, quiet.
    """
    a = p["accent"]
    return f"""
/* ─── Global ─────────────────────────────────────────────────────────── */
QMainWindow, QWidget {{
    background-color: {p["bg"]};
    color: {p["text"]};
    font-family: 'Helvetica Neue', 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
}}
QToolTip {{
    background: {p["raised"]}; color: {p["text"]};
    border: 1px solid {p["line_2"]}; border-radius: 6px; padding: 6px 8px;
}}
QDockWidget {{ background: {p["panel"]}; titlebar-close-icon: none; }}
QDockWidget::title {{
    background: {p["panel"]};
    padding: 6px 10px;
    font-weight: 600; font-size: 11px; letter-spacing: 1.5px;
    color: {p["text_2"]};
    border-bottom: 1px solid {p["line"]};
}}

/* ─── Buttons (neutral like the Catalogue Manager) ───────────────────── */
QPushButton {{
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 {p["raised"]}, stop:1 {p["field"]});
    color: {p["text"]};
    border: 1px solid {p["border"]};
    border-radius: 8px;
    padding: 5px 14px;
    font-size: 12px; letter-spacing: 0.3px;
}}
QPushButton:hover {{
    border-color: {mix(a, p["field"], 0.6)};
    color: {p["accent_hi"]};
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 {rgba(a, 0.16)}, stop:1 {rgba(a, 0.06)});
}}
QPushButton:pressed {{ background: {rgba(a, 0.22)}; border-color: {a}; }}
QPushButton:checked {{
    background: {rgba(a, 0.20)};
    border: 1px solid {a};
    color: {p["accent_hi"]};
}}
QPushButton:disabled {{ color: {p["text_dim"]}; border-color: {p["line"]}; }}
QPushButton[hasMenu="true"] {{ padding-right: 24px; }}
QPushButton::menu-indicator {{
    subcontrol-origin: padding; subcontrol-position: right center;
    right: 6px; width: 8px; height: 8px;
}}
QPushButton[variant="quiet"] {{ font-size: 16px; padding: 2px 10px; }}

QPushButton[variant="primary"] {{
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 {p["accent_hi"]}, stop:0.55 {a}, stop:1 {p["accent_lo"]});
    color: #ffffff; border: 1px solid {p["accent_lo"]}; font-weight: 600;
}}
QPushButton[variant="primary"]:hover {{ background: {p["accent_hi"]}; color: #ffffff; }}

QPushButton[variant="success"] {{ color: {p["success"]}; border-color: {mix(p["success"], p["field"], 0.45)}; }}
QPushButton[variant="success"]:hover,
QPushButton[variant="success"]:checked {{
    color: {p["success"]}; border-color: {p["success"]}; background: {rgba(p["success"], 0.14)};
}}
QPushButton[variant="danger"] {{ color: {p["danger"]}; border-color: {mix(p["danger"], p["field"], 0.45)}; }}
QPushButton[variant="danger"]:hover,
QPushButton[variant="danger"]:checked {{
    color: {p["danger"]}; border-color: {p["danger"]}; background: {rgba(p["danger"], 0.16)};
}}
QPushButton[variant="warning"] {{ color: {p["warning"]}; border-color: {mix(p["warning"], p["field"], 0.45)}; }}
QPushButton[variant="warning"]:hover {{
    color: {p["warning"]}; border-color: {p["warning"]}; background: {rgba(p["warning"], 0.14)};
}}
QPushButton[variant="quiet"] {{
    background: transparent; border: 1px solid transparent; color: {p["text_2"]};
}}
QPushButton[size="small"] {{ padding: 0 9px; font-size: 11px; border-radius: 6px; }}
QPushButton[variant="quiet"]:hover {{ color: {p["accent_hi"]}; background: {rgba(a, 0.12)}; }}

/* ─── Sliders ─────────────────────────────────────────────────────────── */
QSlider::groove:horizontal {{ height: 4px; background: {p["line_2"]}; border-radius: 2px; }}
QSlider::sub-page:horizontal {{ background: {a}; border-radius: 2px; }}
QSlider::handle:horizontal {{
    background: {p["accent_hi"]}; border: 2px solid {p["panel"]};
    width: 13px; height: 13px; border-radius: 7px; margin: -5px 0;
}}
QSlider::groove:vertical {{ width: 4px; background: {p["line_2"]}; border-radius: 2px; }}
QSlider::add-page:vertical {{ background: {a}; border-radius: 2px; }}
QSlider::handle:vertical {{
    background: {p["accent_hi"]}; border: 2px solid {p["panel"]};
    width: 13px; height: 13px; border-radius: 7px; margin: 0 -5px;
}}

/* ─── Combos / Spinboxes / Line edits ───────────────────────────────── */
QComboBox, QSpinBox, QDoubleSpinBox, QLineEdit {{
    background: {p["field"]};
    border: 1px solid {p["line_2"]};
    border-radius: 6px; padding: 3px 8px;
    color: {p["text"]};
    selection-background-color: {rgba(a, 0.35)};
}}
QLineEdit {{ padding: 5px 10px; }}
QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QLineEdit:focus {{
    border-color: {a};
}}
QComboBox::drop-down {{ border: none; }}
/* Spin box arrows drawn by us, so the field border stays closed on every OS */
QSpinBox, QDoubleSpinBox {{ padding-right: 18px; }}
QSpinBox::up-button, QDoubleSpinBox::up-button,
QSpinBox::down-button, QDoubleSpinBox::down-button {{
    subcontrol-origin: border; width: 16px;
    background: {p["raised"]}; border-left: 1px solid {p["line_2"]};
}}
QSpinBox::up-button, QDoubleSpinBox::up-button {{
    subcontrol-position: top right; border-top-right-radius: 6px;
    border-bottom: 1px solid {p["line"]};
}}
QSpinBox::down-button, QDoubleSpinBox::down-button {{
    subcontrol-position: bottom right; border-bottom-right-radius: 6px;
}}
QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{ background: {rgba(a, 0.25)}; }}
QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{
    image: url({_arrow_icon("up", p["text_2"])}); width: 8px; height: 8px;
}}
QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
    image: url({_arrow_icon("down", p["text_2"])}); width: 8px; height: 8px;
}}
QComboBox QAbstractItemView {{
    background: {p["field"]};
    border: 1px solid {p["line_2"]};
    selection-background-color: {rgba(a, 0.22)};
    color: {p["text"]};
}}

/* ─── Scroll bars ────────────────────────────────────────────────────── */
QScrollBar:vertical {{ background: transparent; width: 8px; }}
QScrollBar::handle:vertical {{ background: {rgba(a, 0.30)}; border-radius: 4px; min-height: 24px; }}
QScrollBar::handle:vertical:hover {{ background: {a}; }}
QScrollBar:horizontal {{ background: transparent; height: 8px; }}
QScrollBar::handle:horizontal {{ background: {rgba(a, 0.30)}; border-radius: 4px; min-width: 24px; }}
QScrollBar::handle:horizontal:hover {{ background: {a}; }}
QScrollBar::add-line, QScrollBar::sub-line {{ border: none; background: none; width: 0; height: 0; }}
QScrollBar::add-page, QScrollBar::sub-page {{ background: none; }}

/* ─── Lists ──────────────────────────────────────────────────────────── */
QListWidget, QTreeWidget, QTableWidget {{
    background: {p["field"]}; border: 1px solid {p["line"]};
    border-radius: 6px; color: {p["text"]}; outline: none;
}}
QListWidget::item:selected, QTreeWidget::item:selected, QTableWidget::item:selected {{
    background: {rgba(a, 0.22)}; color: {p["accent_hi"]};
}}
QListWidget::item:hover, QTreeWidget::item:hover {{ background: {rgba(a, 0.08)}; }}

/* ─── Group box ──────────────────────────────────────────────────────── */
QGroupBox {{
    border: 1px solid {p["line"]};
    border-radius: 8px; margin-top: 10px; padding-top: 6px;
    color: {p["text_2"]}; font-size: 11px; letter-spacing: 1px;
}}
QGroupBox::title {{ subcontrol-origin: margin; left: 10px; padding: 0 5px; color: {p["text_2"]}; }}

/* ─── Tabs (tabified docks) ──────────────────────────────────────────── */
QTabBar::tab {{
    background: {p["panel"]}; color: {p["text_2"]};
    padding: 4px 8px; font-size: 11px; border: 1px solid {p["line"]}; border-bottom: none;
    border-top-left-radius: 6px; border-top-right-radius: 6px;
}}
QTabBar::tab:selected {{ color: {p["accent_hi"]}; background: {rgba(a, 0.14)}; }}
QTabBar::tab:hover {{ color: {p["text"]}; }}

/* ─── Status bar / Tool bar ─────────────────────────────────────────── */
QStatusBar {{ background: {p["panel"]}; border-top: 1px solid {p["line"]}; }}
QStatusBar QLabel {{ padding: 0 8px; color: {p["text_2"]}; }}
QToolBar {{
    background: {p["panel"]};
    border-bottom: 1px solid {p["line"]};
    spacing: 4px; padding: 4px 8px;
}}
QToolBar::separator {{ background: {p["line_2"]}; width: 1px; margin: 6px 6px; }}
QToolButton#qt_toolbar_ext_button {{
    background: {rgba(a, 0.85)}; border: 1px solid {p["accent_lo"]};
    border-radius: 6px; margin: 2px; padding: 2px;
}}
QToolButton#qt_toolbar_ext_button:hover {{ background: {p["accent_hi"]}; }}
QLabel#brandName {{
    background: transparent; color: {p["text"]};
    font-weight: 700; font-size: 12px; letter-spacing: 2px;
}}

/* ─── Checkboxes ─────────────────────────────────────────────────────── */
QCheckBox {{ color: {p["text"]}; spacing: 6px; background: transparent; }}
QCheckBox::indicator {{
    width: 14px; height: 14px;
    border: 1px solid {p["line_2"]}; border-radius: 4px;
    background: {p["field"]};
}}
QCheckBox::indicator:checked {{ background: {a}; border-color: {a}; }}

QDial {{ background: transparent; }}
QMenu {{
    background: {p["raised"]}; color: {p["text"]};
    border: 1px solid {p["line_2"]}; border-radius: 8px; padding: 4px;
}}
QMenu::item {{ padding: 6px 18px; border-radius: 5px; }}
QMenu::item:selected {{ background: {rgba(a, 0.20)}; color: {p["accent_hi"]}; }}
QMenu::separator {{ height: 1px; background: {p["line"]}; margin: 4px 6px; }}
"""


# ── widget styles that follow the theme ────────────────────────────────────
#
# Widget.setStyleSheet(f"...{C['accent']}...") evaluates the colours ONCE, so the
# widget keeps the old colours after a theme switch.  themed() stores a function
# that builds the stylesheet and re-runs it in refresh_themed_styles().

import weakref  # noqa: E402
from typing import Callable  # noqa: E402

_themed: "weakref.WeakKeyDictionary" = weakref.WeakKeyDictionary()


def themed(widget, build: Callable[[], str]) -> None:
    """Set *widget*'s stylesheet from *build()* now and again after every theme switch."""
    _themed[widget] = build
    widget.setStyleSheet(build())


def refresh_themed_styles() -> None:
    """Re-apply all stylesheets registered with themed() (call after C.update(...))."""
    for widget, build in list(_themed.items()):
        try:
            widget.setStyleSheet(build())
        except RuntimeError:          # C++ object already deleted
            _themed.pop(widget, None)


def tiny_button_style() -> str:
    """Local stylesheet for small toggle buttons (grid values etc.).

    Set on the widget itself (via themed()) because a widget stylesheet always
    wins over the app stylesheet — keeps padding/font small enough for "1/128".
    """
    p, a = C, C["accent"]
    return (
        f"QPushButton {{ background:{p['field']}; color:{p['text_2']};"
        f" border:1px solid {p['line_2']}; border-radius:4px;"
        f" padding:0px 2px; font-size:9px; min-width:0px; }}"
        f"QPushButton:hover {{ color:{p['accent_hi']}; border-color:{rgba(a, 0.55)}; }}"
        f"QPushButton:checked {{ background:{rgba(a, 0.22)}; color:{p['accent_hi']};"
        f" border-color:{a}; }}"
        f"QPushButton:disabled {{ color:{p['text_dim']}; border-color:{p['line']}; }}"
    )
