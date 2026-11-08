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
    # ── Auto-Assign Instruments ───────────────────────────────────────────────
    "Auto-Assign Instruments":       ("Instrumente Zufallszuweisung",      "Attribution aléatoire d'instruments"),
    "Assigned instruments to {n}/{total} track(s).": (
        "{n}/{total} Spur(en) mit Instrumenten belegt.",
        "{n}/{total} piste(s) dotées d'instruments."),
    "Failed tracks: {tracks}":       ("Fehlgeschlagene Spuren: {tracks}",  "Pistes échouées : {tracks}"),
    # ── Toolbar menus (Catalogue-Manager style) ─────────────────────────────
    "📁 FILE":                          ("📁 DATEI",                          "📁 FICHIER"),
    "🧰 TOOLS":                         ("🧰 WERKZEUGE",                      "🧰 OUTILS"),
    "⚙":                                ("⚙",                                 "⚙"),
    "Settings":                         ("Einstellungen",                     "Paramètres"),
    "Language":                         ("Sprache",                           "Langue"),
    "Theme":                            ("Design",                            "Thème"),
    "New project":                      ("Neues Projekt",                     "Nouveau projet"),
    "Save project…":                    ("Projekt speichern…",                "Sauvegarder le projet…"),
    "Open project…":                    ("Projekt öffnen…",                   "Ouvrir un projet…"),
    "Save MIDI…":                       ("MIDI speichern…",                   "Sauvegarder MIDI…"),
    "Load MIDI…":                       ("MIDI laden…",                       "Charger MIDI…"),
    "Import audio…":                    ("Audio importieren…",                "Importer de l'audio…"),
    "Export (WAV / MP3)…":              ("Exportieren (WAV / MP3)…",          "Exporter (WAV / MP3)…"),
    "Mastering export…":                ("Mastering-Export…",                 "Export mastering…"),
    "GM defaults…":                     ("GM-Standards…",                     "Défauts GM…"),
    "Auto-assign instruments":          ("Instrumente automatisch zuweisen",  "Attribuer les instruments"),
    "AI mix…":                          ("KI-Mix…",                           "Mix IA…"),
    "Master WAV…":                      ("WAV mastern…",                      "Masteriser un WAV…"),
    "Telemetry":                        ("Telemetrie",                        "Télémétrie"),
    "Connect gamepad":                  ("Gamepad verbinden",                 "Connecter la manette"),
    "Key map":                          ("Tastenbelegung",                    "Raccourcis clavier"),
    # ── Short tab titles of the right-hand panels ───────────────────────────
    "FX":                               ("FX",                                "FX"),
    "AUDIO":                            ("AUDIO",                             "AUDIO"),
    "HUMAN":                            ("HUMAN",                             "HUMAIN"),
    "SAMPLER":                          ("SAMPLER",                           "SAMPLER"),
    "◨ PANELS":                         ("◨ PANELS",                          "◨ PANNEAUX"),
    "Show / hide the side panels":      ("Seitenleiste ein-/ausblenden",      "Afficher / masquer les panneaux"),
    "? HELP ON":                        ("? HILFE AN",                        "? AIDE ACTIVÉE"),
    "? HELP OFF":                       ("? HILFE AUS",                       "? AIDE DÉSACTIVÉE"),
    "Turn explanations off":            ("Erklärungen ausschalten",           "Désactiver les explications"),
    "Turn explanations on":             ("Erklärungen einschalten",           "Activer les explications"),
    "Help on: hover over a button, control or area for about a second to see an explanation (cursor shows ?).": (
        "Hilfe an: Fahre ca. eine Sekunde mit der Maus über einen Button, Regler oder Bereich, dann erscheint eine Erklärung (Mauszeiger zeigt ?).",
        "Aide activée : survole un bouton, un réglage ou une zone environ une seconde pour voir une explication (curseur ?)."),
    # ── Menu entry hints ────────────────────────────────────────────────────
    "Clear all tracks and start fresh":  ("Alle Spuren löschen und neu beginnen", "Effacer toutes les pistes et recommencer"),
    "Save full project to .dawproj":     ("Ganzes Projekt als .dawproj speichern", "Sauvegarder le projet complet en .dawproj"),
    "Load a .dawproj project file":      ("Eine .dawproj-Projektdatei öffnen",  "Ouvrir un fichier projet .dawproj"),
    "Export tracks to .mid":             ("Spuren als .mid exportieren",        "Exporter les pistes en .mid"),
    "Import MIDI file(s) — each track gets its own GM instrument": (
        "MIDI-Datei(en) laden – jede Spur bekommt ein eigenes GM-Instrument",
        "Importer des fichiers MIDI – chaque piste reçoit son instrument GM"),
    "Add audio files — each gets its own track": (
        "Audiodateien hinzufügen – jede bekommt eine eigene Spur",
        "Ajouter des fichiers audio – chacun sur sa propre piste"),
    "Export to WAV or MP3":              ("Als WAV oder MP3 exportieren",       "Exporter en WAV ou MP3"),
    "Multi-format mastering export (MP3 / WAV / Stems)": (
        "Mastering-Export in mehreren Formaten (MP3 / WAV / Stems)",
        "Export mastering multi-format (MP3 / WAV / Stems)"),
    "Default SFZ / VST3 instruments for MIDI drag-and-drop": (
        "Standard-Instrumente (SFZ / VST3) für MIDI per Drag-and-drop",
        "Instruments SFZ / VST3 par défaut pour le glisser-déposer MIDI"),
    "Assign role-appropriate instruments to all MIDI tracks": (
        "Allen MIDI-Spuren passende Instrumente zuweisen",
        "Attribuer des instruments adaptés à toutes les pistes MIDI"),
    "Genre FX template for all tracks (EQ · Comp · Reverb · Stereo)": (
        "Genre-Effektvorlage für alle Spuren (EQ · Kompressor · Hall · Stereo)",
        "Modèle d'effets par genre pour toutes les pistes (EQ · Comp · Réverbe · Stéréo)"),
    "Master an external .wav file (EQ · width · LUFS · limiter)": (
        "Externe .wav-Datei mastern (EQ · Breite · LUFS · Limiter)",
        "Masteriser un fichier .wav externe (EQ · largeur · LUFS · limiteur)"),
    "Show / hide the real-time audio telemetry panels": (
        "Echtzeit-Audioanalyse ein-/ausblenden",
        "Afficher / masquer l'analyse audio en temps réel"),
    "Connect PS5 DualSense":             ("PS5-DualSense verbinden",            "Connecter la DualSense PS5"),
    "Show keyboard mapping":             ("Tastenbelegung anzeigen",            "Afficher les raccourcis clavier"),
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
