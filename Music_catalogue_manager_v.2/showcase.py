"""
Inhalt der öffentlichen Seite „Bildstrecke“ (Produkt-Tour für Stakeholder).

Jede Folie: Bilddatei (in static/showcase/), Bereich, Titel und Text.
Die Texte sind deutsche Übersetzungsschlüssel (translations.py → EN/FR).
Neue Folie: Bild nach static/showcase/ legen und hier einen Eintrag ergänzen.
"""
from __future__ import annotations

SHOWCASE_DIR = "showcase"                       # Unterordner in static/
SHOWCASE_PDF = "Bildstrecke_Beat_Collage.pdf"   # Download der gesamten Bildstrecke

SECTION_CREATOR = "Catalogue Manager · Creator"
SECTION_OPERATOR = "Catalogue Manager · Betreiber"
SECTION_DAW = "DAW"

SLIDES: list[dict[str, str]] = [
    {"image": "01_login.jpg", "section": SECTION_CREATOR, "title": "Anmelden",
     "text": "Der Einstieg in Beat Collage: Anmeldung mit E-Mail und Passwort. Die Oberfläche lässt sich direkt auf Deutsch, Englisch oder Französisch umstellen."},
    {"image": "02_generator.jpg", "section": SECTION_CREATOR, "title": "Beat einstellen",
     "text": "Genre, Tempo und Komplexität wählen – optional auch Tonart, Klangfarbe und Instrumente. Ein Klick auf „Beat generieren“ erzeugt einen kompletten Song."},
    {"image": "03_piano_roll_catalogue.jpg", "section": SECTION_CREATOR, "title": "Ergebnis prüfen",
     "text": "Die Piano Roll zeigt alle erzeugten Spuren farbig getrennt – Kick, Percussion, Bass, Lead, Akkorde, Pad und Arpeggio. Hier: Pop-Song mit 112 BPM und 56 Takten."},
    {"image": "04_export.jpg", "section": SECTION_CREATOR, "title": "Exportieren",
     "text": "Den Song als Audiodatei herunterladen (WAV, MP3, FLAC, OGG) – oder als MIDI zur Weiterbearbeitung in der DAW. Dazu gibt es einen Produktionsberater als PDF."},
    {"image": "05_katalog.jpg", "section": SECTION_OPERATOR, "title": "Katalog verwalten",
     "text": "Für den Betreiber: alle erzeugten Tracks mit Genre, Wasserzeichen und Status (z. B. an Kunden vergeben). Grundlage für den Lizenzverkauf."},
    {"image": "06_wirtschaftlichkeit.jpg", "section": SECTION_OPERATOR, "title": "Wirtschaftlichkeit",
     "text": "Umsatz, Fixkosten, Deckungsbeitrag, Break-even und ROI werden automatisch aus den Verkäufen berechnet. Stand: vor den ersten Verkäufen."},
    {"image": "07_daw_arrangement.jpg", "section": SECTION_DAW, "title": "In der DAW weiterbearbeiten",
     "text": "Die MIDI-Datei ist in der DAW geladen: jede Spur hat ein eigenes Instrument, darunter der Mixer mit Lautstärke und Panorama, rechts die Effekte."},
    {"image": "08_daw_piano_roll.jpg", "section": SECTION_DAW, "title": "Noten bearbeiten",
     "text": "In der Piano Roll lassen sich die Noten einer Spur einzeln zeichnen, verschieben und löschen – mit Raster, Zoom und Anschlagstärke."},
    {"image": "09_daw_hilfe.jpg", "section": SECTION_DAW, "title": "Hilfe für Einsteiger",
     "text": "Mit „Hilfe AN“ erklärt die DAW jedes Element, sobald man mit der Maus darüber fährt – in einfacher Sprache und in drei Sprachen."},
    {"image": "10_daw_werkzeuge.jpg", "section": SECTION_DAW, "title": "Werkzeuge",
     "text": "Zusatzfunktionen im Menü: Instrumente automatisch zuweisen, KI-Mix per Genre-Vorlage, WAV mastern und Echtzeit-Audioanalyse."},
]

# Gruppen für die Übersicht im Titelbild (Schrittnummern, 1-basiert)
GROUPS: list[dict] = [
    {"first": 1, "last": 4, "label": "Song erzeugen & exportieren"},
    {"first": 5, "last": 6, "label": "Katalog & Wirtschaftlichkeit"},
    {"first": 7, "last": 10, "label": "Bearbeiten in der DAW"},
]

# Zusammenfassung am Ende (wie die letzte Seite der PDF)
SUMMARY: list[dict[str, str]] = [
    {"title": "Erzeugen", "text": "Komplette Songs in 11 Genres per Klick – mit Tonart, Tempo und Instrumenten frei einstellbar."},
    {"title": "Exportieren", "text": "Audio in gängigen Formaten oder MIDI zur Weiterbearbeitung, dazu ein Produktionsberater als PDF."},
    {"title": "Bearbeiten", "text": "Eigene DAW mit Piano Roll, Mixer, Effekten, KI-Mix und Hilfe-Modus für Einsteiger."},
    {"title": "Verwalten & verkaufen", "text": "Katalog, Lizenzen, Abo und Tokens sowie automatische Wirtschaftlichkeitsrechnung."},
]
