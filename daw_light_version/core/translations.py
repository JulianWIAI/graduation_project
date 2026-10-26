"""
translations.py — i18n for SBS-Synth Master DAW
================================================
English is the source language (keys).
Each entry maps to a (german, french) tuple.
Language order: de → en → fr  (mirrors Music_catalogue_manager_v.2)
"""

# ---------------------------------------------------------------------------
# Translation table  (English key → (German, French))
# ---------------------------------------------------------------------------
_T: dict[str, tuple[str, str]] = {
    # ── Toolbar ──────────────────────────────────────────────────────────
    "✦ NEW PROJECT":       ("✦ NEUES PROJEKT",         "✦ NOUVEAU PROJET"),
    "💾 SAVE PROJECT":     ("💾 PROJEKT SPEICHERN",     "💾 SAUVEGARDER PROJET"),
    "📂 LOAD PROJECT":     ("📂 PROJEKT LADEN",         "📂 CHARGER PROJET"),
    "🎹 CHANNEL RACK":     ("🎹 KANALRACK",             "🎹 RACK DE CANAUX"),
    "+ ADD TRACK":         ("+ SPUR HINZUFÜGEN",        "+ AJOUTER PISTE"),
    "💾 SAVE MIDI":        ("💾 MIDI SPEICHERN",         "💾 SAUVEGARDER MIDI"),
    "📂 LOAD MIDI":        ("📂 MIDI LADEN",             "📂 CHARGER MIDI"),
    "🎵+ IMPORT AUDIO":    ("🎵+ AUDIO IMPORTIEREN",    "🎵+ IMPORTER AUDIO"),
    "🎹 GM DEFAULTS":      ("🎹 GM STANDARD",           "🎹 DÉFAUTS GM"),
    "🎵 EXPORT":           ("🎵 EXPORTIEREN",            "🎵 EXPORTER"),
    "🎚 MASTER":           ("🎚 MASTERN",               "🎚 MASTER"),
    "🎮 GAMEPAD":          ("🎮 GAMEPAD",               "🎮 MANETTE"),
    "⌨ KEY MAP":           ("⌨ TASTENBELEGUNG",         "⌨ RACCOURCIS"),
    # ── Status bar ───────────────────────────────────────────────────────
    "🎲 Auto-Assign Instruments": ("🎲 Instrumente Zufallszuweisung",
                                   "🎲 Instruments Aléatoires"),
    "🤖 AI MIX":           ("🤖 KI MIX",               "🤖 MIX IA"),
    "✨ Master WAV":        ("✨ WAV Mastern",            "✨ Masteriser WAV"),
    "📊 TELEMETRY":        ("📊 TELEMETRIE",             "📊 TÉLÉMÉTRIE"),
    # ── Settings dialog ──────────────────────────────────────────────────
    "⚙  SETTINGS":         ("⚙  EINSTELLUNGEN",         "⚙  PARAMÈTRES"),
    "LANGUAGE":            ("SPRACHE",                  "LANGUE"),
    "THEME":               ("DESIGN",                   "THÈME"),
    "Dark":                ("Dunkel",                   "Sombre"),
    "Light":               ("Hell",                     "Clair"),
    "Close":               ("Schließen",                "Fermer"),
    # ── Dock titles ──────────────────────────────────────────────────────
    "TRANSPORT":           ("TRANSPORT",                "TRANSPORT"),
    "MIXER":               ("MIXER",                    "MIXEUR"),
    "EFFECTS":             ("EFFEKTE",                  "EFFETS"),
    "AUDIO FX":            ("AUDIO FX",                 "AUDIO FX"),
    "HUMANIZE":            ("HUMANISIEREN",             "HUMANISER"),
    "DS INSTRUMENT":       ("DS INSTRUMENT",            "DS INSTRUMENT"),
    # ── AutoMasterDialog ─────────────────────────────────────────────────────
    "Auto-Master":                      ("Auto-Master",                       "Auto-Master"),
    "AUTO-MASTER":                      ("AUTO-MASTER",                       "AUTO-MASTER"),
    "Offline post-mix mastering chain": ("Offline-Nachbearbeitungskette",     "Chaîne de mastering post-mixage"),
    "I / O":                            ("E / A",                             "E / S"),
    "Mastering Parameters":             ("Mastering-Parameter",               "Paramètres de Mastering"),
    "Input WAV:":                       ("Eingangs-WAV:",                     "WAV d'entrée :"),
    "Output WAV:":                      ("Ausgangs-WAV:",                     "WAV de sortie :"),
    "Genre:":                           ("Genre:",                            "Genre :"),
    "Target LUFS:":                     ("Ziel-LUFS:",                        "LUFS cible :"),
    "True Peak:":                       ("Wahrer Peak:",                      "Crête réelle :"),
    "Stereo Width:":                    ("Stereobreite:",                     "Largeur stéréo :"),
    "Master":                           ("Mastern",                           "Masteriser"),
    "Browse":                           ("Wählen",                            "Parcourir"),
    "Auto-Master Complete":             ("Auto-Master abgeschlossen",         "Auto-Master terminé"),
    "Path to rendered stereo WAV …":    ("Pfad zur gerenderten Stereo-WAV …", "Chemin vers le WAV stéréo rendu …"),
    "Output path …":                    ("Ausgabepfad …",                     "Chemin de sortie …"),
    # ── AI Mix dialog ─────────────────────────────────────────────────────────
    "AI Mix":                           ("KI Mix",                            "Mix IA"),
    "AI Mix — Select Genre":            ("KI Mix — Genre wählen",             "Mix IA — Choisir le genre"),
    "Choose a genre to apply the AI FX template:": (
        "Genre für die KI-FX-Vorlage wählen:",
        "Choisir un genre pour le modèle FX IA :"),
    "▶  Apply":                         ("▶  Anwenden",                       "▶  Appliquer"),
    "Cancel":                           ("Abbrechen",                         "Annuler"),
    "AI Mix Error":                     ("KI Mix Fehler",                     "Erreur Mix IA"),
    "No MIDI tracks are loaded. Open a MIDI file first.": (
        "Keine MIDI-Spuren geladen. Bitte zuerst eine MIDI-Datei öffnen.",
        "Aucune piste MIDI chargée. Ouvrez d'abord un fichier MIDI."),
}

# Build lookup dicts for non-English languages
TRANSLATIONS: dict[str, dict[str, str]] = {
    "de": {en: tr[0] for en, tr in _T.items()},
    "fr": {en: tr[1] for en, tr in _T.items()},
}

# Ordered list of supported languages (DE → EN → FR, matching the catalogue)
LANGUAGES = ["de", "en", "fr"]
LANGUAGE_LABELS = {"de": "DE", "en": "EN", "fr": "FR"}


def translate(text: str, lang: str) -> str:
    """Return ``text`` translated to *lang*; falls back to English source."""
    if lang == "en" or lang not in TRANSLATIONS:
        return text
    return TRANSLATIONS[lang].get(text, text)
