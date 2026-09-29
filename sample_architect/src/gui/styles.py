# ── Backgrounds — true black ────────────────────────────────────────────────
BG0 = '#000000'   # window chrome
BG1 = '#080808'   # sidebar
BG2 = '#0f0f0f'   # main content
BG3 = '#161616'   # card background
BG4 = '#1e1e1e'   # inputs / row
BG5 = '#282828'   # hover / selected

# ── Highlights — brown and pink ──────────────────────────────────────────────
PINK   = '#ff6ec7'   # hot pink  — primary highlight
CYAN   = '#ff8fab'   # rose pink — replaces all cyan accents
ORANGE = '#c87c3e'   # warm brown — replaces all orange buttons
GREEN  = '#2ecc71'   # keep: universally means "good score"
YELLOW = '#d4884a'   # amber-brown — replaces yellow
PURPLE = '#cc3d88'   # deep rose — replaces purple
RED    = '#e84d6a'   # errors / warnings

# ── Text ─────────────────────────────────────────────────────────────────────
TXT_BRT = '#f0e6e6'   # warm off-white
TXT_MED = '#7a5f5f'   # warm muted
TXT_DIM = '#332222'   # near-invisible, very dark

# ── Typography ────────────────────────────────────────────────────────────────
_UI   = 'Segoe UI'
_MONO = 'Consolas'

FN_TITLE  = (_UI,   18, 'bold')
FN_HEAD   = (_UI,   13, 'bold')
FN_SUB    = (_UI,   11, 'bold')
FN_BODY   = (_UI,   10)
FN_SMALL  = (_UI,    9)
FN_MONO   = (_MONO, 10)
FN_MONO_S = (_MONO,  9)

# Legacy aliases
FN_S = FN_MONO_S
FN_X = (_MONO, 8)
FN_M = FN_BODY
FN_L = FN_HEAD

# ── Role colours — all mapped to brown / pink family ─────────────────────────
ROLE_COLORS = {
    # classifier sub-tags
    'kick':       ORANGE,    # warm brown
    'snare':      YELLOW,    # amber
    'hihat':      TXT_MED,   # warm muted
    'percussion': PINK,      # hot pink
    'bass':       CYAN,      # rose pink
    'chords':     PURPLE,    # deep rose
    'lead':       PINK,      # hot pink
    'pad':        PURPLE,    # deep rose
    'arp':        YELLOW,    # amber
    'stabs':      ORANGE,    # warm brown
    'texture':    TXT_BRT,   # warm white
    'fx':         TXT_MED,   # warm muted
    # setup slot names
    'drums':      ORANGE,    # warm brown
    'perc':       PINK,      # hot pink
}

# ── Structural constants (used by backend) ────────────────────────────────────
ALL_ROLES = [
    'kick', 'snare', 'hihat', 'percussion',
    'bass', 'chords', 'lead', 'pad', 'arp', 'stabs', 'texture', 'fx',
]

SETUP_ROLES = [
    'drums', 'perc', 'bass', 'chords', 'lead', 'arp', 'pad', 'stabs', 'texture', 'fx',
]

SLOT_TO_CLASSIFIER_ROLES = {
    'drums':   ['kick', 'snare', 'hihat'],
    'perc':    ['percussion'],
    'bass':    ['bass'],
    'chords':  ['chords'],
    'lead':    ['lead'],
    'arp':     ['arp'],
    'pad':     ['pad'],
    'stabs':   ['stabs'],
    'texture': ['texture'],
    'fx':      ['fx'],
}
