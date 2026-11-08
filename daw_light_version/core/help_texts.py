"""
Help texts for the "? HELP" mode — the same idea as the help tooltips in the
Catalogue Manager.  One entry per UI element: key → {language: (title, text)}.

Add a new explanation:
    1. add an entry here (de / en / fr),
    2. in the GUI code call  help_mode.set_help(widget, "<key>").
"""
from __future__ import annotations

HELP: dict[str, dict[str, tuple[str, str]]] = {
    # ── Toolbar ──────────────────────────────────────────────────────────
    "file": {
        "de": ("Datei", "Projekte anlegen, speichern und öffnen, MIDI und Audio laden sowie den Song als WAV/MP3 exportieren."),
        "en": ("File", "Create, save and open projects, load MIDI and audio, and export the song as WAV/MP3."),
        "fr": ("Fichier", "Créer, sauvegarder et ouvrir des projets, charger MIDI et audio, exporter le morceau en WAV/MP3."),
    },
    "channel_rack": {
        "de": ("Channel Rack", "Step-Sequencer für Beats: Klicke Schritte an, um Drums und Samples im Raster zu programmieren."),
        "en": ("Channel Rack", "Step sequencer for beats: click steps to program drums and samples on a grid."),
        "fr": ("Rack de canaux", "Séquenceur pas à pas : clique sur les pas pour programmer batterie et samples."),
    },
    "add_track": {
        "de": ("Spur hinzufügen", "Legt eine neue Instrumentenspur an. Danach wählst du ein Instrument (SoundFont, SFZ oder VST)."),
        "en": ("Add track", "Creates a new instrument track. You then pick an instrument (SoundFont, SFZ or VST)."),
        "fr": ("Ajouter une piste", "Crée une nouvelle piste d'instrument. Tu choisis ensuite un instrument (SoundFont, SFZ ou VST)."),
    },
    "tools": {
        "de": ("Werkzeuge", "Zusatzfunktionen: Instrumente automatisch zuweisen, KI-Mix, WAV mastern, Telemetrie und Gamepad."),
        "en": ("Tools", "Extra functions: auto-assign instruments, AI mix, master a WAV, telemetry and gamepad."),
        "fr": ("Outils", "Fonctions annexes : attribution d'instruments, mix IA, mastering WAV, télémétrie et manette."),
    },
    "panels": {
        "de": ("Seitenleiste", "Blendet die Panels rechts (FX, Audio, Humanize, Sampler) ein oder aus – für mehr Platz in der Mitte."),
        "en": ("Side panels", "Shows or hides the panels on the right (FX, Audio, Humanize, Sampler) – for more room in the middle."),
        "fr": ("Panneaux", "Affiche ou masque les panneaux de droite (FX, Audio, Humanize, Sampler) pour plus d'espace."),
    },
    "settings": {
        "de": ("Einstellungen", "Sprache (DE/EN/FR) und Design (Dunkel/Hell) umstellen. Die Auswahl wird gespeichert."),
        "en": ("Settings", "Switch language (DE/EN/FR) and theme (dark/light). Your choice is saved."),
        "fr": ("Paramètres", "Changer la langue (DE/EN/FR) et le thème (sombre/clair). Le choix est enregistré."),
    },
    "help": {
        "de": ("Hilfe", "Schaltet diese Erklärungen an oder aus. Bei AUS erscheinen nur noch kurze Hinweise."),
        "en": ("Help", "Turns these explanations on or off. When off, only short hints are shown."),
        "fr": ("Aide", "Active ou désactive ces explications. Désactivée, seuls de courts indices s'affichent."),
    },
    # ── Transport ────────────────────────────────────────────────────────
    "play": {
        "de": ("Play", "Spielt das Projekt ab der Position des Abspielkopfs ab."),
        "en": ("Play", "Plays the project from the playhead position."),
        "fr": ("Lecture", "Lit le projet à partir de la tête de lecture."),
    },
    "stop": {
        "de": ("Stop", "Stoppt die Wiedergabe und springt zurück an den Anfang."),
        "en": ("Stop", "Stops playback and jumps back to the start."),
        "fr": ("Stop", "Arrête la lecture et revient au début."),
    },
    "record": {
        "de": ("Aufnahme", "Nimmt gespielte Noten (Keyboard, Gamepad, MIDI) auf die ausgewählte Spur auf."),
        "en": ("Record", "Records played notes (keyboard, gamepad, MIDI) onto the selected track."),
        "fr": ("Enregistrer", "Enregistre les notes jouées (clavier, manette, MIDI) sur la piste sélectionnée."),
    },
    "bpm": {
        "de": ("Tempo (BPM)", "Schläge pro Minute. Höher = schneller. Klicke ins Feld, dann tippen oder mit den Pfeilen ändern."),
        "en": ("Tempo (BPM)", "Beats per minute. Higher = faster. Click the field, then type or use the arrows."),
        "fr": ("Tempo (BPM)", "Battements par minute. Plus haut = plus rapide. Clique puis saisis ou utilise les flèches."),
    },
    "comp_view": {
        "de": ("Composition View", "Zeigt in der Piano Roll alle Spuren gleichzeitig, damit du siehst, wie sie zusammenpassen."),
        "en": ("Composition view", "Shows all tracks at once in the piano roll so you can see how they fit together."),
        "fr": ("Vue composition", "Affiche toutes les pistes dans le piano roll pour voir comment elles s'accordent."),
    },
    "loop": {
        "de": ("Loop", "Spielt den markierten Bereich in Dauerschleife. Den Bereich legst du fest, indem du im Lineal ziehst."),
        "en": ("Loop", "Repeats the marked region. Set the region by dragging in the ruler."),
        "fr": ("Boucle", "Répète la zone marquée. Définis-la en faisant glisser dans la règle."),
    },
    "scale": {
        "de": ("Tonleiter", "Tonleiter für Keyboard und Gamepad – gespielte Töne passen dann immer zur Tonart."),
        "en": ("Scale", "Scale for keyboard and gamepad – played notes always fit the key."),
        "fr": ("Gamme", "Gamme pour clavier et manette – les notes jouées restent dans la tonalité."),
    },
    "root": {
        "de": ("Grundton", "Startton der Tonleiter, z. B. C4 für C-Dur bzw. C-Moll."),
        "en": ("Root note", "Starting note of the scale, e.g. C4 for C major / C minor."),
        "fr": ("Tonique", "Note de départ de la gamme, p. ex. C4 pour do majeur / mineur."),
    },
    "octave": {
        "de": ("Oktave", "Verschiebt Keyboard und Gamepad um ganze Oktaven nach oben oder unten."),
        "en": ("Octave", "Shifts keyboard and gamepad up or down by whole octaves."),
        "fr": ("Octave", "Décale clavier et manette d'octaves entières vers le haut ou le bas."),
    },
    "panic": {
        "de": ("Panic", "Notfall-Stopp: schaltet sofort alle hängenden Töne aus."),
        "en": ("Panic", "Emergency stop: instantly silences all stuck notes."),
        "fr": ("Panique", "Arrêt d'urgence : coupe immédiatement toutes les notes bloquées."),
    },
    # ── Main areas ───────────────────────────────────────────────────────
    "arrangement": {
        "de": ("Arrangement", "Jede Zeile ist eine Spur. Klick auf eine Spur öffnet ihre Noten. Mausrad scrollt, Shift+Mausrad bewegt die Zeit, Ctrl+Mausrad zoomt."),
        "en": ("Arrangement", "Each row is a track. Click a track to open its notes. Wheel scrolls, Shift+wheel moves in time, Ctrl+wheel zooms."),
        "fr": ("Arrangement", "Chaque ligne est une piste. Clique pour ouvrir ses notes. Molette : défiler, Maj+molette : temps, Ctrl+molette : zoom."),
    },
    "piano_roll": {
        "de": ("Piano Roll", "Hier bearbeitest du die Noten einer Spur: links die Tonhöhe, nach rechts die Zeit. Im DRAW-Modus zeichnest du Noten."),
        "en": ("Piano roll", "Edit the notes of a track: pitch on the left, time to the right. In DRAW mode you paint notes."),
        "fr": ("Piano roll", "Édite les notes d'une piste : hauteur à gauche, temps vers la droite. En mode DRAW, tu dessines des notes."),
    },
    "back_arrangement": {
        "de": ("Zurück zum Arrangement", "Schließt die Piano Roll und zeigt wieder alle Spuren."),
        "en": ("Back to arrangement", "Closes the piano roll and shows all tracks again."),
        "fr": ("Retour à l'arrangement", "Ferme le piano roll et réaffiche toutes les pistes."),
    },
    "draw_mode": {
        "de": ("Draw / Select", "DRAW: Klicken setzt Noten. SELECT: Noten markieren, verschieben und löschen."),
        "en": ("Draw / Select", "DRAW: clicking places notes. SELECT: mark, move and delete notes."),
        "fr": ("Dessin / Sélection", "DRAW : un clic place une note. SELECT : sélectionner, déplacer, supprimer."),
    },
    "grid": {
        "de": ("Raster", "Notenlänge, an der Noten einrasten (z. B. 1/16). T = Triolen, D = punktiert, Free = ohne Raster."),
        "en": ("Grid", "Note value notes snap to (e.g. 1/16). T = triplets, D = dotted, Free = no snapping."),
        "fr": ("Grille", "Valeur sur laquelle les notes s'alignent (p. ex. 1/16). T = triolets, D = pointé, Free = libre."),
    },
    "velocity": {
        "de": ("Anschlagstärke (VEL)", "Zeigt, wie laut jede Note gespielt wird. Ziehe einen Balken hoch oder runter, um ihn zu ändern."),
        "en": ("Velocity (VEL)", "Shows how loud each note is played. Drag a bar up or down to change it."),
        "fr": ("Vélocité (VEL)", "Indique la force de chaque note. Fais glisser une barre pour la modifier."),
    },
    "zoom": {
        "de": ("Zoom", "Vergrößert oder verkleinert die Zeitachse. Alternativ: Ctrl + Mausrad."),
        "en": ("Zoom", "Zooms the timeline in or out. Alternatively: Ctrl + mouse wheel."),
        "fr": ("Zoom", "Agrandit ou réduit la ligne du temps. Sinon : Ctrl + molette."),
    },
    # ── Mixer ────────────────────────────────────────────────────────────
    "mixer_strip": {
        "de": ("Mixer-Kanal", "Lautstärke (VOL) und Stereo-Position (PAN) einer Spur. M = stumm, S = solo, Punkt = Spur auswählen."),
        "en": ("Mixer channel", "Volume (VOL) and stereo position (PAN) of a track. M = mute, S = solo, dot = select track."),
        "fr": ("Tranche de mixage", "Volume (VOL) et position stéréo (PAN) d'une piste. M = muet, S = solo, point = sélectionner."),
    },
    "master": {
        "de": ("Master", "Gesamtlautstärke aller Spuren. Der Limiter verhindert Übersteuern; Ceil ist die maximale Lautstärke."),
        "en": ("Master", "Overall volume of all tracks. The limiter prevents clipping; Ceil is the maximum level."),
        "fr": ("Master", "Volume global de toutes les pistes. Le limiteur évite la saturation ; Ceil = niveau maximal."),
    },
    # ── Side panels ──────────────────────────────────────────────────────
    "panel_fx": {
        "de": ("Effekte (FX)", "Klangeffekte für die ausgewählte Spur: Equalizer, Hall, Kompressor und Chorus. Häkchen bei Active schaltet sie ein."),
        "en": ("Effects (FX)", "Sound effects for the selected track: EQ, reverb, compressor and chorus. Tick Active to enable."),
        "fr": ("Effets (FX)", "Effets pour la piste sélectionnée : égaliseur, réverbe, compresseur, chorus. Coche Active pour activer."),
    },
    "panel_audio": {
        "de": ("Audio FX", "Effektkette für Audiospuren (importierte WAV/MP3): Lautstärke, Panorama und Effekt-Slots."),
        "en": ("Audio FX", "Effect chain for audio tracks (imported WAV/MP3): volume, pan and effect slots."),
        "fr": ("Audio FX", "Chaîne d'effets des pistes audio (WAV/MP3 importés) : volume, pan et emplacements d'effets."),
    },
    "panel_human": {
        "de": ("Humanize", "Macht programmierte Noten lebendiger, indem die Anschlagstärke leicht zufällig variiert wird."),
        "en": ("Humanize", "Makes programmed notes feel more alive by slightly varying their velocity."),
        "fr": ("Humaniser", "Rend les notes programmées plus vivantes en variant légèrement leur vélocité."),
    },
    "panel_sampler": {
        "de": ("Sampler (DS)", "Lädt Decent-Sampler-Instrumente (.dspreset) mit eigenen Reglern für die ausgewählte Spur."),
        "en": ("Sampler (DS)", "Loads Decent Sampler instruments (.dspreset) with their own controls for the selected track."),
        "fr": ("Sampler (DS)", "Charge des instruments Decent Sampler (.dspreset) avec leurs réglages pour la piste choisie."),
    },
}


# ── Detailed explanations for single controls (for beginners) ──────────────
HELP.update({
    # Arrangement / piano roll regions
    "track_header": {
        "de": ("Spurkopf", "Name, Kanal und Notenzahl der Spur. Klick = Noten öffnen, Rechtsklick = Instrument ändern oder Spur entfernen. AUTO = Automation, FX = Audio-Effekte."),
        "en": ("Track header", "Name, channel and note count. Click = open notes, right-click = change instrument or remove track. AUTO = automation, FX = audio effects."),
        "fr": ("En-tête de piste", "Nom, canal et nombre de notes. Clic = ouvrir les notes, clic droit = changer d'instrument ou supprimer. AUTO = automation, FX = effets audio."),
    },
    "ruler": {
        "de": ("Lineal (Takte)", "Zeigt die Takte. Klicken setzt den Abspielkopf, Ziehen markiert einen Bereich für LOOP."),
        "en": ("Ruler (bars)", "Shows the bars. Click to move the playhead, drag to mark a region for LOOP."),
        "fr": ("Règle (mesures)", "Affiche les mesures. Clic = déplacer la tête de lecture, glisser = zone pour la boucle."),
    },
    "keyboard": {
        "de": ("Klaviatur", "Zeigt die Tonhöhe jeder Zeile. Weiter oben = höherer Ton. C4 ist das mittlere C."),
        "en": ("Keyboard", "Shows the pitch of each row. Higher up = higher note. C4 is middle C."),
        "fr": ("Clavier", "Indique la hauteur de chaque ligne. Plus haut = plus aigu. C4 = do central."),
    },
    # Effects panel
    "fx_active": {
        "de": ("Active", "Schaltet diesen Effekt für die Spur ein oder aus. Aus = Regler haben keine Wirkung."),
        "en": ("Active", "Turns this effect on or off for the track. Off = the controls have no effect."),
        "fr": ("Active", "Active ou désactive cet effet pour la piste. Désactivé = les réglages n'agissent pas."),
    },
    "eq": {
        "de": ("Equalizer (EQ)", "Macht einzelne Frequenzen lauter oder leiser: 32 = tiefer Bass, 1k = Mitten, 16k = Höhen. Regler hoch = mehr davon."),
        "en": ("Equalizer (EQ)", "Boosts or cuts frequency ranges: 32 = deep bass, 1k = mids, 16k = treble. Slider up = more of it."),
        "fr": ("Égaliseur (EQ)", "Renforce ou atténue des fréquences : 32 = grave, 1k = médiums, 16k = aigus. Vers le haut = plus."),
    },
    "reverb": {
        "de": ("Hall (Reverb)", "Lässt die Spur klingen, als wäre sie in einem Raum – von kleinem Zimmer bis Kirche."),
        "en": ("Reverb", "Makes the track sound as if it were in a room – from a small room to a church."),
        "fr": ("Réverbération", "Donne l'impression que la piste joue dans une pièce – de la chambre à l'église."),
    },
    "rev_room": {
        "de": ("Room (Raumgröße)", "Größe des Raums. Höher = längerer, größerer Hall."),
        "en": ("Room (size)", "Size of the room. Higher = longer, bigger reverb."),
        "fr": ("Room (taille)", "Taille de la pièce. Plus haut = réverbe plus longue et ample."),
    },
    "rev_damp": {
        "de": ("Damp (Dämpfung)", "Wie stark die Höhen im Hall geschluckt werden. Höher = wärmer, dumpfer Hall."),
        "en": ("Damp", "How much treble the reverb absorbs. Higher = warmer, darker reverb."),
        "fr": ("Damp (amortissement)", "Quantité d'aigus absorbés. Plus haut = réverbe plus chaude et sombre."),
    },
    "rev_width": {
        "de": ("Width (Breite)", "Wie breit der Hall im Stereobild ist. Höher = breiter, umhüllender Klang."),
        "en": ("Width", "Stereo width of the reverb. Higher = wider, more enveloping."),
        "fr": ("Width (largeur)", "Largeur stéréo de la réverbe. Plus haut = plus enveloppant."),
    },
    "rev_level": {
        "de": ("Level (Anteil)", "Wie viel Hall zum Originalklang gemischt wird. 0 = kein Hall."),
        "en": ("Level", "How much reverb is mixed into the dry sound. 0 = no reverb."),
        "fr": ("Level (niveau)", "Quantité de réverbe ajoutée au son original. 0 = aucune."),
    },
    "compressor": {
        "de": ("Kompressor", "Gleicht laute und leise Stellen an, damit die Spur gleichmäßiger und druckvoller klingt."),
        "en": ("Compressor", "Evens out loud and quiet parts so the track sounds steadier and punchier."),
        "fr": ("Compresseur", "Équilibre passages forts et faibles pour un son plus régulier et percutant."),
    },
    "comp_thresh": {
        "de": ("Thresh (Schwelle)", "Ab dieser Lautstärke greift der Kompressor. Niedriger = er arbeitet öfter."),
        "en": ("Thresh (threshold)", "Level above which the compressor acts. Lower = it works more often."),
        "fr": ("Thresh (seuil)", "Niveau à partir duquel le compresseur agit. Plus bas = il agit plus souvent."),
    },
    "comp_ratio": {
        "de": ("Ratio (Stärke)", "Wie stark laute Stellen leiser gemacht werden. 2 = sanft, 10+ = sehr stark."),
        "en": ("Ratio", "How strongly loud parts are reduced. 2 = gentle, 10+ = very strong."),
        "fr": ("Ratio", "Force de la réduction des passages forts. 2 = doux, 10+ = très fort."),
    },
    "comp_attack": {
        "de": ("Attack", "Wie schnell der Kompressor reagiert (ms). Langsam lässt den Anschlag durch, schnell glättet ihn."),
        "en": ("Attack", "How fast the compressor reacts (ms). Slow lets the hit through, fast smooths it."),
        "fr": ("Attack", "Vitesse de réaction (ms). Lent laisse passer l'attaque, rapide la lisse."),
    },
    "comp_release": {
        "de": ("Release", "Wie schnell der Kompressor wieder loslässt (ms), wenn es leiser wird."),
        "en": ("Release", "How fast the compressor lets go again (ms) when the sound gets quieter."),
        "fr": ("Release", "Vitesse à laquelle le compresseur relâche (ms) quand le son baisse."),
    },
    "chorus": {
        "de": ("Chorus", "Verdoppelt den Klang leicht verstimmt – klingt breiter und schwebender, wie mehrere Spieler."),
        "en": ("Chorus", "Doubles the sound slightly detuned – wider and shimmering, like several players."),
        "fr": ("Chorus", "Double le son légèrement désaccordé – plus large et chatoyant."),
    },
    "cho_level": {
        "de": ("Level", "Wie stark der Chorus-Effekt zu hören ist."),
        "en": ("Level", "How strongly the chorus effect is heard."),
        "fr": ("Level", "Intensité audible de l'effet chorus."),
    },
    "cho_speed": {
        "de": ("Speed", "Wie schnell der Klang schwebt. Langsam = ruhig, schnell = flatternd."),
        "en": ("Speed", "How fast the sound wavers. Slow = calm, fast = fluttering."),
        "fr": ("Speed", "Vitesse d'ondulation. Lent = calme, rapide = vibrant."),
    },
    "cho_depth": {
        "de": ("Depth", "Wie stark der Klang verstimmt wird. Höher = deutlicherer Effekt."),
        "en": ("Depth", "How much the sound is detuned. Higher = more obvious effect."),
        "fr": ("Depth", "Ampleur du désaccord. Plus haut = effet plus marqué."),
    },
    # Mixer strip parts
    "mix_vol": {
        "de": ("Lautstärke (VOL)", "Fader nach oben = Spur lauter, nach unten = leiser."),
        "en": ("Volume (VOL)", "Fader up = track louder, down = quieter."),
        "fr": ("Volume (VOL)", "Fader vers le haut = plus fort, vers le bas = moins fort."),
    },
    "mix_pan": {
        "de": ("Panorama (PAN)", "Position im Stereobild: links, Mitte oder rechts."),
        "en": ("Pan", "Position in the stereo field: left, centre or right."),
        "fr": ("Panoramique (PAN)", "Position stéréo : gauche, centre ou droite."),
    },
    "mix_mute": {
        "de": ("Mute (M)", "Schaltet die Spur stumm, ohne sie zu löschen."),
        "en": ("Mute (M)", "Silences the track without deleting it."),
        "fr": ("Muet (M)", "Rend la piste muette sans la supprimer."),
    },
    "mix_solo": {
        "de": ("Solo (S)", "Nur diese Spur ist zu hören – praktisch, um sie einzeln anzuhören."),
        "en": ("Solo (S)", "Only this track is heard – handy for listening to it alone."),
        "fr": ("Solo (S)", "Seule cette piste est audible – pratique pour l'écouter seule."),
    },
    "mix_select": {
        "de": ("Spur auswählen", "Wählt die Spur aus: Effekte rechts und Piano Roll zeigen dann diese Spur."),
        "en": ("Select track", "Selects the track: the effects panel and piano roll then show this track."),
        "fr": ("Sélectionner", "Sélectionne la piste : effets et piano roll affichent alors cette piste."),
    },
    "mix_remove": {
        "de": ("Spur entfernen", "Löscht diese Spur aus dem Projekt."),
        "en": ("Remove track", "Deletes this track from the project."),
        "fr": ("Supprimer la piste", "Supprime cette piste du projet."),
    },
    "mix_name": {
        "de": ("Spurname", "Name der Spur in ihrer Farbe (gleiche Farbe wie im Arrangement). Doppelklick = umbenennen. Darunter: das Instrument und CH = MIDI-Kanal."),
        "en": ("Track name", "Name of the track in its colour (same as in the arrangement). Double-click = rename. Below: the instrument and CH = MIDI channel."),
        "fr": ("Nom de piste", "Nom de la piste dans sa couleur (comme dans l'arrangement). Double-clic = renommer. En dessous : l'instrument et CH = canal MIDI."),
    },
    # Master strip parts
    "master_audition": {
        "de": ("Abhörmodus", "Wie du den Mix hörst: normal (Bypass), als Vorschau oder wie auf Streaming-Plattformen."),
        "en": ("Audition mode", "How you hear the mix: normal (bypass), as a preview or as on streaming platforms."),
        "fr": ("Mode d'écoute", "Comment tu entends le mix : normal (bypass), aperçu ou comme sur le streaming."),
    },
    "master_meter": {
        "de": ("Pegelanzeige", "Zeigt, wie laut der Gesamtmix gerade ist (links/rechts). Oben = sehr laut."),
        "en": ("Level meter", "Shows how loud the whole mix is right now (left/right). Top = very loud."),
        "fr": ("Vumètre", "Indique le niveau actuel du mix (gauche/droite). En haut = très fort."),
    },
    "master_gain": {
        "de": ("Master-Lautstärke", "Lautstärke des gesamten Songs."),
        "en": ("Master volume", "Volume of the whole song."),
        "fr": ("Volume master", "Volume de l'ensemble du morceau."),
    },
    "master_limiter": {
        "de": ("Limiter", "Verhindert, dass der Song übersteuert und verzerrt. Am besten AN lassen."),
        "en": ("Limiter", "Stops the song from clipping and distorting. Best left ON."),
        "fr": ("Limiteur", "Empêche la saturation et la distorsion. Mieux vaut le laisser activé."),
    },
    "master_ceiling": {
        "de": ("Ceil (Obergrenze)", "Lauter als dieser Wert (in dB) wird der Song nie. −0,1 dB ist üblich."),
        "en": ("Ceil (ceiling)", "The song never gets louder than this (in dB). −0.1 dB is common."),
        "fr": ("Ceil (plafond)", "Le morceau ne dépasse jamais ce niveau (dB). −0,1 dB est courant."),
    },
})

HELP.update({
    "eq_32": {
        "de": ("EQ 32 Hz – Tiefbass", "Der tiefste Bereich, eher spürbar als hörbar (Kick-Druck, Sub-Bass). Hoch = mehr Wumms, runter = weniger Dröhnen."),
        "en": ("EQ 32 Hz – sub bass", "The lowest range, felt more than heard (kick punch, sub bass). Up = more boom, down = less rumble."),
        "fr": ("EQ 32 Hz – infra-grave", "La zone la plus grave, plus ressentie qu'entendue. Haut = plus de punch, bas = moins de grondement."),
    },
    "eq_250": {
        "de": ("EQ 250 Hz – Bass/Wärme", "Fülle und Wärme von Bass, Gitarre und Stimme. Zu viel klingt matschig."),
        "en": ("EQ 250 Hz – bass/warmth", "Body and warmth of bass, guitar and voice. Too much sounds muddy."),
        "fr": ("EQ 250 Hz – grave/chaleur", "Corps et chaleur de la basse, guitare et voix. Trop = son boueux."),
    },
    "eq_1k": {
        "de": ("EQ 1 kHz – Mitten", "Hier sitzen Melodien und Stimmen. Anheben = präsenter, absenken = weicher."),
        "en": ("EQ 1 kHz – mids", "Where melodies and voices sit. Boost = more present, cut = softer."),
        "fr": ("EQ 1 kHz – médiums", "Zone des mélodies et voix. Renforcer = plus présent, atténuer = plus doux."),
    },
    "eq_4k": {
        "de": ("EQ 4 kHz – Präsenz", "Deutlichkeit und Biss, z. B. Anschlag von Snare und Gitarre. Zu viel klingt scharf."),
        "en": ("EQ 4 kHz – presence", "Clarity and bite, e.g. snare and guitar attack. Too much sounds harsh."),
        "fr": ("EQ 4 kHz – présence", "Clarté et mordant (attaque caisse claire, guitare). Trop = son agressif."),
    },
    "eq_16k": {
        "de": ("EQ 16 kHz – Brillanz", "Luft und Glanz, z. B. Hi-Hats und Becken. Hoch = heller, runter = dunkler."),
        "en": ("EQ 16 kHz – air", "Air and sparkle, e.g. hi-hats and cymbals. Up = brighter, down = darker."),
        "fr": ("EQ 16 kHz – brillance", "Air et éclat (charleston, cymbales). Haut = plus brillant, bas = plus sombre."),
    },
})


def help_for(key: str, lang: str) -> tuple[str, str] | None:
    """(title, text) for *key* in *lang*, English as fallback; None if unknown."""
    entry = HELP.get(key)
    if not entry:
        return None
    return entry.get(lang) or entry.get("en")
