# Protokoll

| Feld | Inhalt |
|---|---|
| **Datum** | Montag, 26.10.2026 |
| **Uhrzeit** | Folgeeinheit (Nachmittag) |
| **Ort** | zu Hause |
| **Teilnehmer** | Julian (Einzelarbeit) |
| **Protokollführer** | Claude (KI-Werkzeug) |
| **Thema** | Light-Theme-Nachbesserung DAW (verbleibende schwarze Bereiche), Passwort-Wiederherstellung Catalogue Manager |
| **Arbeitspakete (PSP)** | – |
| **Hilfsmittel** | Claude Code (KI), PyCharm, Git, GitHub |

---

## Agenda

1. Verbleibende schwarze Bereiche im Light-Theme beheben (Track-View-Canvas, Dialoge, FX-Plugins, Panic-Button)
2. Passwort-Wiederherstellung für `Music_catalogue_manager_v.2` konzipieren und implementieren

---

## Verlauf und Ergebnisse

### TOP 1: Light-Theme-Nachbesserung DAW

**Problem:** Nach der ersten Theme-Implementierung waren noch mehrere Bereiche im Light-Theme dunkel:
- Track-View / Piano-Roll-Canvas (schwarze Fläche trotz aktivem Light-Theme)
- Alle QDialog-Unterklassen (Export, Master, GM-Defaults, Channel Rack, Add Track, VST Browser)
- FX-Plugin-Panels (8 Dateien)
- Panic-Button (hartkodiertes `background:#1A0000`)
- Mixer-Container und Piano-Roll-Layoutcontainer

**Ursachen:**

| Problem | Ursache |
|---|---|
| Track-View bleibt schwarz | `paintEvent()` liest `C["abyss"]` / `C["void"]` zur Laufzeit; `C` war bisher nie mutiert worden |
| Dialoge bleiben dunkel | `self.setStyleSheet(STYLESHEET)` / `self.setStyleSheet(_STYLESHEET)` → einmalig ausgewertetes f-String mit dunklen Werten |
| FX-Plugins dunkel | Eigene `_C`-Kopie + `w.setStyleSheet(f"background:{_C['abyss']};")`  in jeder Datei |

**Lösung:**

1. **`C` in-place mutieren** (`_apply_theme()` ruft nun `C.update(palette)` auf, bevor `setStyleSheet` gesetzt wird) → alle `paintEvent()`-Aufrufe verwenden danach automatisch die neue Palette. `DARK_PALETTE = dict(C)` als eingefrorene Kopie für die Rückkehr zum dunklen Theme hinzugefügt.

2. **Dialog-Stylesheets dynamisieren** — In `gui_windows.py`: alle `self.setStyleSheet(STYLESHEET)` → `self.setStyleSheet(build_stylesheet(C))`. Da `C` bereits mutiert ist, wenn der Dialog geöffnet wird, erhält er immer das aktuelle Theme.

3. **Externe Dialog-Dateien** — `self.setStyleSheet(_STYLESHEET)` in `auto_mastering_dialog.py`, `export_dialog.py`, `gm_defaults_dialog.py`, `channel_rack.py` entfernt. Das app-weite QSS (`QApplication.instance().setStyleSheet(...)`) übernimmt alle Widget-Stile automatisch.

4. **FX-Plugin-Hintergründe** — `w.setStyleSheet(f"background:{_C['abyss']};")`  aus 10 Dateien entfernt (`fx_plugins_*.py`, `ai_generative_reverb.py`, `ai_smart_eq.py`, `fx_rack_widget.py`, `fx_slot_widget.py`, `grid_settings_panel.py`).

5. **Panic-Button** — `background:#1A0000` entfernt; nur `color:{C['orange']}` und `border:` bleiben.

6. **Piano-Roll-Layoutcontainer** — `setStyleSheet(f"background:{C['void/abyss']};")`  von allen reinen Layout-Containern (`piano_scroll`, `piano_with_scroll`, `piano_panel`, `central`, `arrange_panel`) entfernt.

**Geänderte Dateien:**
- `daw_light_version/core/gui_windows.py`
- `daw_light_version/core/channel_rack.py`
- `daw_light_version/core/auto_mastering_dialog.py`
- `daw_light_version/core/export_dialog.py`
- `daw_light_version/core/gm_defaults_dialog.py`
- `daw_light_version/core/fx_rack_widget.py`
- `daw_light_version/core/fx_slot_widget.py`
- `daw_light_version/core/grid_settings_panel.py`
- `daw_light_version/core/fx_plugins_cpp.py` u. 7 weitere `fx_plugins_*.py`
- `daw_light_version/core/ai_generative_reverb.py`
- `daw_light_version/core/ai_smart_eq.py`

**Commits:** `bee05a1`, `1675f12`, `e4b29dd`

---

### TOP 2: Passwort-Wiederherstellung — Konzept und Implementierung

**Anforderung:** Kein E-Mail-Server verfügbar. Zwei-Schichten-Lösung:

#### Schicht 1 — Sicherheitsfrage (Selbstbedienung)

**Fluss:**
1. Registrierung: Nutzer gibt Sicherheitsfrage und -antwort an (Antwort wird kleingeschrieben, dann bcrypt-gehasht gespeichert)
2. Login-Seite: Link „Passwort vergessen?" → Benutzername eingeben → Sicherheitsfrage wird angezeigt → Antwort eingeben → bei Korrektheit: neues Passwort setzen
3. Sicherheit: 3-Versuchs-Sperre (analog zur bestehenden Login-Sperre)

**Neue Templates:** `forgot_password.html`, `forgot_password_question.html`, `reset_password.html`

**Neue Routen in `main.py`:**
- `GET/POST /forgot-password`
- `GET/POST /forgot-password/<username>`
- `GET/POST /reset-password/<username>/<token>` (Token wird in der Session gespeichert, 15 min gültig, Einmalverwendung)

#### Schicht 2 — Admin-Temporärpasswort (Fallback)

**Fluss:**
1. Admin öffnet Einstellungen → neuer Bereich „Benutzerverwaltung" mit Tabelle aller Nutzer
2. Klick auf „Passwort zurücksetzen" → 8-stelliges zufälliges Temporärpasswort wird generiert, gehasht gespeichert, `must_change_pw = 1` gesetzt
3. Temporärpasswort wird einmalig als Flash-Nachricht angezeigt (Admin teilt es dem Nutzer außerhalb mit)
4. Beim nächsten Login mit dem Temporärpasswort → Weiterleitung auf `change_password.html` → Pflicht zur Passwortänderung → `must_change_pw = 0`

**Neues Template:** `change_password.html`

**Neue Route:** `POST /admin/reset-password/<username>`

#### Datenbankänderungen (`appdata/database.py` oder `db/database.py`)

Drei neue Spalten zur Nutzertabelle:
- `security_question TEXT`
- `security_answer_hash TEXT`
- `must_change_pw INTEGER DEFAULT 0`

Migration ist rückwärtskompatibel (`ALTER TABLE ... ADD COLUMN IF NOT EXISTS`).

#### Übersetzungen

17 neue Einträge in `translations.py` (DE → EN / FR) nach bestehendem Muster ergänzt.

**Geänderte / neue Dateien:**
- `Music_catalogue_manager_v.2/main.py` oder `auth/auth.py`
- `Music_catalogue_manager_v.2/db/database.py` (oder `appdata/database.py`)
- `Music_catalogue_manager_v.2/translations.py`
- `Music_catalogue_manager_v.2/templates/login.html` (Link „Passwort vergessen?")
- `Music_catalogue_manager_v.2/templates/register.html` (Sicherheitsfrage + Antwort)
- `Music_catalogue_manager_v.2/templates/settings.html` (Admin-Benutzerverwaltung)
- 4 neue Templates

**Commit:** `20d802f`

---

## Aufgaben und nächste Schritte

| Aufgabe | Verantwortlich | Termin |
|---|---|---|
| Light-Theme im DAW visuell vollständig abnahmen (alle Dialoge öffnen und prüfen) | Julian | nächste Einheit |
| Passwort-Wiederherstellung testen: Registrierung mit Sicherheitsfrage, Vergessen-Fluss, Admin-Reset | Julian | nächste Einheit |
| Prüfen, ob Piano-Roll-Noten und Piano-Tasten im Light-Theme gut lesbar sind | Julian | nächste Einheit |

---

Dieses Protokoll wurde maschinell erstellt und ist ohne Unterschrift gültig.

gez. Julian
