"""
Uebersetzungstabellen fuer i18n.py.

Aufbau:  "Deutscher Originaltext": ("English", "Français")

Der deutsche Text ist der Schluessel und muss EXAKT so im Code/Template
stehen (inkl. HTML-Entities wie &amp; oder &#10;). Fehlt ein Eintrag, wird
einfach der deutsche Text angezeigt.

Platzhalter muessen in allen Sprachen gleich heissen:
    _T  (Python/Templates):  %(name)s      -- ein echtes Prozentzeichen: %%
    _JS (JavaScript):        {name}

Neue Sprache ergaenzen: Tupel um einen Eintrag erweitern, unten in
TRANSLATIONS/JS eintragen und in i18n.LANGUAGES aufnehmen.
"""

# ---------------------------------------------------------------------------
# Python-Meldungen und Templates
# ---------------------------------------------------------------------------
_T = {
    # --- Navigation / Grundgeruest (base.html) ------------------------------
    "Katalog & Lizenzen": ("Catalog & Licenses", "Catalogue & licences"),
    "for creators": ("for creators", "pour les créateurs"),
    "Generate": ("Generate", "Générer"),
    "Statistik": ("Statistics", "Statistiques"),
    "Tokens": ("Tokens", "Jetons"),
    "Abo": ("Subscription", "Abonnement"),
    "Dashboard": ("Dashboard", "Tableau de bord"),
    "Katalog": ("Catalog", "Catalogue"),
    "Lizenzen": ("Licenses", "Licences"),
    "Nutzer": ("Users", "Utilisateurs"),
    "Wirtschaftlichkeit": ("Profitability", "Rentabilité"),
    "Protokoll": ("Audit log", "Journal"),
    "Einstellungen": ("Settings", "Paramètres"),
    "? Hilfe AN": ("? Help ON", "? Aide ON"),
    "Logout": ("Logout", "Déconnexion"),
    "↻ Scannen": ("↻ Scan", "↻ Scanner"),
    "Ergänzungsmodul zum Gesamtpaket · koppelt read-only an Music Architect V7 &amp; SBS-Synth Master": (
        "Add-on module for the full package · read-only link to Music Architect V7 &amp; SBS-Synth Master",
        "Module complémentaire du pack complet · couplage en lecture seule avec Music Architect V7 &amp; SBS-Synth Master"),
    "Bitte melden Sie sich an, um auf diese Seite zuzugreifen.": (
        "Please sign in to access this page.",
        "Veuillez vous connecter pour accéder à cette page."),

    # --- Anmeldung / Registrierung ------------------------------------------
    "Anmelden — SBS Catalog": ("Sign in — SBS Catalog", "Connexion — SBS Catalog"),
    "Anmelden": ("Sign in", "Se connecter"),
    "E-Mail": ("Email", "E-mail"),
    "Passwort": ("Password", "Mot de passe"),
    "Kein Konto?": ("No account?", "Pas de compte ?"),
    "Registrieren": ("Sign up", "S'inscrire"),
    "Registrieren — SBS Catalog": ("Sign up — SBS Catalog", "Inscription — SBS Catalog"),
    "Konto erstellen": ("Create account", "Créer un compte"),
    "Passwort bestätigen": ("Confirm password", "Confirmer le mot de passe"),
    "Bereits ein Konto?": ("Already have an account?", "Déjà un compte ?"),
    "E-Mail und Passwort sind erforderlich.": (
        "Email and password are required.", "L'e-mail et le mot de passe sont obligatoires."),
    "Passwoerter stimmen nicht ueberein.": (
        "Passwords do not match.", "Les mots de passe ne correspondent pas."),
    "Ein Konto mit dieser E-Mail-Adresse existiert bereits.": (
        "An account with this email address already exists.",
        "Un compte avec cette adresse e-mail existe déjà."),
    "Ungueltige E-Mail oder falsches Passwort.": (
        "Invalid email or wrong password.", "E-mail invalide ou mot de passe incorrect."),

    # --- Tarifwahl (plan.html) ----------------------------------------------
    "Tarif wählen": ("Choose your plan", "Choisir une offre"),
    "Wie möchtest du SBS Catalog nutzen? Ein Abo kannst du auch später jederzeit hier abschließen.": (
        "How would you like to use SBS Catalog? You can also take out a subscription here at any later time.",
        "Comment souhaitez-vous utiliser SBS Catalog ? Vous pourrez aussi souscrire un abonnement ici plus tard, à tout moment."),
    "Dein Abo ist aktiv bis %(date)s.": (
        "Your subscription is active until %(date)s.", "Votre abonnement est actif jusqu'au %(date)s."),
    "Dein Abo ist aktiv.": ("Your subscription is active.", "Votre abonnement est actif."),
    "Basis": ("Basic", "Base"),
    "kostenlos": ("free", "gratuit"),
    "%(n)s Sounds pro Monat": ("%(n)s sounds per month", "%(n)s sons par mois"),
    "Weitere Sounds per Token: %(price)s je Token": (
        "More sounds with tokens: %(price)s per token", "Sons supplémentaires avec des jetons : %(price)s par jeton"),
    "Als Basis-Kunde starten": ("Start as a basic customer", "Commencer avec l'offre de base"),
    "/Monat": ("/month", "/mois"),
    "Günstigere Tokens: %(price)s je Token": (
        "Cheaper tokens: %(price)s per token", "Jetons moins chers : %(price)s par jeton"),
    "%(pct)s %% Rabatt auf Lizenzen": ("%(pct)s%% discount on licenses", "%(pct)s %% de remise sur les licences"),
    "Weiter zum Generator": ("Continue to the generator", "Continuer vers le générateur"),
    "%(n)s Monat(e)": ("%(n)s month(s)", "%(n)s mois"),
    "Abo abschließen": ("Subscribe", "S'abonner"),
    "Im Basis-Tarif gilt das Kontingent je Kalendermonat, im Abo je Abo-Monat ab dem Abschlussdatum. Das Abo verlängert sich nicht automatisch. Gezählt werden gespeicherte bzw. exportierte Sounds — Vorhören ist immer kostenlos. Alle Preise netto zzgl. USt.": (
        "On the basic plan the quota applies per calendar month, with a subscription per subscription month starting on the purchase date. The subscription does not renew automatically. Saved or exported sounds are counted — previewing is always free. All prices net, plus VAT.",
        "Avec l'offre de base, le quota s'applique par mois civil ; avec l'abonnement, par mois d'abonnement à compter de la date de souscription. L'abonnement ne se renouvelle pas automatiquement. Seuls les sons enregistrés ou exportés sont comptés — la pré-écoute est toujours gratuite. Tous les prix s'entendent HT."),
    "Dein Abo läuft am %(date)s aus. Verlängere es jetzt, damit du bei %(n)s Sounds pro Monat bleibst.": (
        "Your subscription expires on %(date)s. Renew it now to keep your %(n)s sounds per month.",
        "Votre abonnement expire le %(date)s. Prolongez-le maintenant pour conserver vos %(n)s sons par mois."),
    "Dein Abo ist am %(date)s abgelaufen. Du nutzt jetzt den Basis-Tarif — hier kannst du das Abo erneuern.": (
        "Your subscription expired on %(date)s. You are now on the basic plan — you can renew the subscription here.",
        "Votre abonnement a expiré le %(date)s. Vous utilisez maintenant l'offre de base — vous pouvez renouveler l'abonnement ici."),
    "Aktuelles Kontingent: %(used)s von %(limit)s Sounds genutzt, erneuert sich am %(date)s.": (
        "Current quota: %(used)s of %(limit)s sounds used, renews on %(date)s.",
        "Quota actuel : %(used)s sons utilisés sur %(limit)s, renouvellement le %(date)s."),
    "Abo verlängern": ("Renew subscription", "Prolonger l'abonnement"),
    "Eine Verlängerung schließt nahtlos an das aktuelle Enddatum an.": (
        "A renewal continues seamlessly from the current end date.",
        "Une prolongation s'enchaîne directement après la date de fin actuelle."),
    "Abo bezahlt und aktiviert.": ("Subscription paid and activated.", "Abonnement payé et activé."),
    "Abo nicht gefunden.": ("Subscription not found.", "Abonnement introuvable."),
    "Dieses Abo ist bereits bezahlt.": (
        "This subscription has already been paid.", "Cet abonnement est déjà payé."),
    "Ungueltige Laufzeit.": ("Invalid term.", "Durée invalide."),

    # --- Kontingent & Tokens ------------------------------------------------
    "Monatslimit erreicht (%(limit)s Sounds pro Monat). Kein Token-Guthaben — weitere Sounds sind mit Tokens möglich (%(price)s je Token).": (
        "Monthly limit reached (%(limit)s sounds per month). No token balance — further sounds are possible with tokens (%(price)s per token).",
        "Limite mensuelle atteinte (%(limit)s sons par mois). Aucun jeton disponible — d'autres sons sont possibles avec des jetons (%(price)s par jeton)."),
    "Monatslimit erreicht: %(name)s hat diesen Monat %(used)s/%(limit)s Bezüge (Generierungen + Lizenzen). In diesem Monat ist kein weiterer Bezug möglich.": (
        "Monthly limit reached: %(name)s has used %(used)s/%(limit)s this month (generations + licenses). No further purchase is possible this month.",
        "Limite mensuelle atteinte : %(name)s a utilisé %(used)s/%(limit)s ce mois-ci (générations + licences). Aucune autre acquisition n'est possible ce mois-ci."),
    "Kontingent reicht nicht. %(name)s hat diesen Monat %(used)s/%(limit)s Sounds bezogen (noch %(remaining)s moeglich, %(count)s angefragt). Benoetigt: %(needed)s Token(s), Guthaben: %(balance)s. Token-Preis: %(price)s (%(group)s).": (
        "Quota insufficient. %(name)s has used %(used)s/%(limit)s sounds this month (%(remaining)s left, %(count)s requested). Required: %(needed)s token(s), balance: %(balance)s. Token price: %(price)s (%(group)s).",
        "Quota insuffisant. %(name)s a utilisé %(used)s/%(limit)s sons ce mois-ci (%(remaining)s restants, %(count)s demandés). Requis : %(needed)s jeton(s), solde : %(balance)s. Prix du jeton : %(price)s (%(group)s)."),
    "[%(mode)s] %(count)s Track(s) fuer %(user)s erzeugt. Diesen Monat %(used)s/%(limit)s (noch %(remaining)s).": (
        "[%(mode)s] %(count)s track(s) created for %(user)s. This month %(used)s/%(limit)s (%(remaining)s left).",
        "[%(mode)s] %(count)s morceau(x) généré(s) pour %(user)s. Ce mois-ci %(used)s/%(limit)s (%(remaining)s restants)."),
    "%(n)s Token(s) verbraucht.": ("%(n)s token(s) used.", "%(n)s jeton(s) consommé(s)."),
    "Zum Uebernehmen: Scannen.": ("To import them: scan.", "Pour les importer : scanner."),
    "Token-Preise muessen Zahlen sein.": ("Token prices must be numbers.", "Les prix des jetons doivent être des nombres."),
    "Token-Preise muessen groesser als 0 sein.": (
        "Token prices must be greater than 0.", "Les prix des jetons doivent être supérieurs à 0."),
    "Der Token-Preis fuer Abonnenten muss unter dem Basis-Preis liegen (aktuell %(sub)s ≥ %(basic)s).": (
        "The token price for subscribers must be below the basic price (currently %(sub)s ≥ %(basic)s).",
        "Le prix du jeton pour les abonnés doit être inférieur au prix de base (actuellement %(sub)s ≥ %(basic)s)."),
    "Betrag darf nicht 0 sein.": ("Amount must not be 0.", "Le montant ne peut pas être 0."),
    "Das Guthaben darf nicht negativ werden.": (
        "The balance must not become negative.", "Le solde ne peut pas devenir négatif."),
    "Ungueltige Anzahl.": ("Invalid quantity.", "Quantité invalide."),
    "Ungueltiger Betrag.": ("Invalid amount.", "Montant invalide."),
    "Bitte zwischen 1 und %(max)s Tokens waehlen.": (
        "Please choose between 1 and %(max)s tokens.", "Veuillez choisir entre 1 et %(max)s jetons."),
    "Nutzer nicht gefunden.": ("User not found.", "Utilisateur introuvable."),
    "Bestellung nicht gefunden.": ("Order not found.", "Commande introuvable."),
    "Diese Bestellung ist bereits bezahlt.": (
        "This order has already been paid.", "Cette commande est déjà payée."),
    "Diese Bestellung wurde storniert.": ("This order was cancelled.", "Cette commande a été annulée."),
    "Nur offene Bestellungen koennen storniert werden.": (
        "Only open orders can be cancelled.", "Seules les commandes en attente peuvent être annulées."),
    "Zahlung bestätigt — %(n)s Token(s) gutgeschrieben.": (
        "Payment confirmed — %(n)s token(s) credited.", "Paiement confirmé — %(n)s jeton(s) crédité(s)."),
    "Bestellung storniert.": ("Order cancelled.", "Commande annulée."),
    "Für stornierte Bestellungen gibt es keine Rechnung.": (
        "There is no invoice for cancelled orders.", "Il n'y a pas de facture pour les commandes annulées."),
    "Token-Guthaben angepasst.": ("Token balance adjusted.", "Solde de jetons ajusté."),

    # --- Token-Shop (tokens.html) -------------------------------------------
    "Tokens · SBS Catalog": ("Tokens · SBS Catalog", "Jetons · SBS Catalog"),
    "Kontingent aufgebraucht? Mit Tokens kannst du weitere Sounds speichern und exportieren — jeder Beat über dem Limit verbraucht genau 1 Token. Tokens verfallen nicht.": (
        "Quota used up? With tokens you can save and export more sounds — every beat above the limit uses exactly 1 token. Tokens do not expire.",
        "Quota épuisé ? Avec des jetons, vous pouvez enregistrer et exporter d'autres sons — chaque beat au-delà de la limite consomme exactement 1 jeton. Les jetons n'expirent pas."),
    "Dein Guthaben": ("Your balance", "Votre solde"),
    "Token(s)": ("token(s)", "jeton(s)"),
    "Dein Preis je Token": ("Your price per token", "Votre prix par jeton"),
    "Abo-Preis (statt": ("Subscriber price (instead of", "Prix abonné (au lieu de"),
    "Abo-Preis": ("subscriber price", "prix abonné"),
    "Basis-Preis": ("Basic price", "Prix de base"),
    "· zzgl. USt": ("· plus VAT", "· hors TVA"),
    "Abo-Vorteil": ("Subscriber benefit", "Avantage abonné"),
    "· Basis": ("· Basic", "· Base"),
    "je Token": ("per token", "par jeton"),
    "Tokens kaufen": ("Buy tokens", "Acheter des jetons"),
    "Token": ("Token", "Jeton"),
    "ohne Abo": ("without subscription", "sans abonnement"),
    "Kaufen": ("Buy", "Acheter"),
    "Eigene Menge": ("Custom quantity", "Quantité libre"),
    "Zur Kasse": ("Go to checkout", "Passer au paiement"),
    "Meine Bestellungen": ("My orders", "Mes commandes"),
    "Nr.": ("No.", "N°"),
    "Menge": ("Qty", "Quantité"),
    "Netto": ("Net", "HT"),
    "Status": ("Status", "Statut"),
    "bezahlt": ("paid", "payé"),
    "offen": ("open", "en attente"),
    "storniert": ("cancelled", "annulé"),
    "Rechnung": ("Invoice", "Facture"),
    "Bezahlen": ("Pay", "Payer"),
    "Noch keine Bestellungen.": ("No orders yet.", "Aucune commande pour l'instant."),
    "Token-Bewegungen": ("Token transactions", "Mouvements de jetons"),
    "Zeit": ("Time", "Heure"),
    "Vorgang": ("Transaction", "Opération"),
    "Noch keine Bewegungen.": ("No transactions yet.", "Aucun mouvement pour l'instant."),
    "Kauf": ("Purchase", "Achat"),
    "Verbrauch": ("Usage", "Consommation"),
    "Erstattung": ("Refund", "Remboursement"),
    "Gutschrift (Admin)": ("Credit (admin)", "Crédit (admin)"),

    # --- Checkout & Rechnung ------------------------------------------------
    "Checkout · SBS Catalog": ("Checkout · SBS Catalog", "Paiement · SBS Catalog"),
    "Checkout": ("Checkout", "Paiement"),
    "simuliert": ("simulated", "simulé"),
    "Zahlungsübersicht — Status:": ("Payment summary — status:", "Récapitulatif du paiement — statut :"),
    "Lizenz": ("License", "Licence"),
    "Position": ("Item", "Article"),
    "Käufer": ("Buyer", "Acheteur"),
    "Listenpreis": ("List price", "Prix catalogue"),
    "Abo-Rabatt": ("Subscriber discount", "Remise abonné"),
    "Nettobetrag": ("Net amount", "Montant HT"),
    "zzgl. USt (": ("plus VAT (", "TVA en sus ("),
    "Gesamtbetrag": ("Total", "Montant total"),
    "Bereits bezahlt.": ("Already paid.", "Déjà payé."),
    "Rechnung ansehen": ("View invoice", "Voir la facture"),
    "zum Token-Shop": ("to the token shop", "vers la boutique de jetons"),
    "zu den Nutzern": ("to the users", "vers les utilisateurs"),
    "zu den Lizenzen": ("to the licenses", "vers les licences"),
    "Zahlung bestätigen (simuliert)": ("Confirm payment (simulated)", "Confirmer le paiement (simulé)"),
    "Stornieren": ("Cancel order", "Annuler la commande"),
    "Abbrechen": ("Cancel", "Annuler"),
    "In der Praxis übernimmt hier ein Zahlungsdienstleister den Einzug; erst dessen Bestätigung setzt den Status auf „bezahlt“.": (
        "In practice a payment provider collects the money here; only its confirmation sets the status to “paid”.",
        "En pratique, un prestataire de paiement se charge ici de l'encaissement ; seule sa confirmation fait passer le statut à « payé »."),
    "Drucken": ("Print", "Imprimer"),
    "Musikproduktion &amp; Lizenzierung": ("Music production &amp; licensing", "Production musicale &amp; licences"),
    "RECHNUNG": ("INVOICE", "FACTURE"),
    "Rechnung an": ("Bill to", "Facturé à"),
    "Beschreibung": ("Description", "Description"),
    "Betrag": ("Amount", "Montant"),
    "Enthält Abo-Rabatt von": ("Includes subscriber discount of", "Inclut une remise abonné de"),
    "% (Liste": ("% (list", "% (catalogue"),
    "Zwischensumme (netto)": ("Subtotal (net)", "Sous-total (HT)"),
    "Umsatzsteuer": ("VAT", "TVA"),
    "Status:": ("Status:", "Statut :"),
    "bezahlt am %(date)s": ("paid on %(date)s", "payé le %(date)s"),
    "Hinweis: keine USt ausgewiesen (Kleinunternehmerregelung).": (
        "Note: no VAT shown (small business exemption).",
        "Remarque : TVA non applicable (régime des petites entreprises)."),
    "Simulierter Beleg für Demonstrationszwecke — keine echte Zahlung.": (
        "Simulated receipt for demonstration purposes — no real payment.",
        "Reçu simulé à des fins de démonstration — aucun paiement réel."),
    "Lizenz: %(title)s — %(tier)s": ("License: %(title)s — %(tier)s", "Licence : %(title)s — %(tier)s"),
    "Gast": ("Guest", "Invité"),
    "%(n)s Generierungs-Token à %(price)s (%(group)s)": (
        "%(n)s generation token(s) at %(price)s each (%(group)s)",
        "%(n)s jeton(s) de génération à %(price)s l'unité (%(group)s)"),
    "Abo — Laufzeit %(n)s Monat(e) (%(start)s bis %(end)s)": (
        "Subscription — term %(n)s month(s) (%(start)s to %(end)s)",
        "Abonnement — durée %(n)s mois (du %(start)s au %(end)s)"),
    "Rechnung nicht gefunden.": ("Invoice not found.", "Facture introuvable."),

    # --- Statistik (stats.html) ---------------------------------------------
    "Meine Statistik — SBS Catalog": ("My statistics — SBS Catalog", "Mes statistiques — SBS Catalog"),
    "&#8635; Aktualisieren": ("&#8635; Refresh", "&#8635; Actualiser"),
    "Gespeicherte Beats": ("Saved beats", "Beats enregistrés"),
    "Heute": ("Today", "Aujourd'hui"),
    "Diese Woche": ("This week", "Cette semaine"),
    "ab": ("from", "depuis le"),
    "Diesen Monat": ("This month", "Ce mois-ci"),
    "Generierungen gesamt (inkl. nicht gespeichert)": (
        "Total generations (incl. unsaved)", "Total des générations (y compris non enregistrées)"),
    "Gespeicherte Beats — letzte 7 Tage": ("Saved beats — last 7 days", "Beats enregistrés — 7 derniers jours"),
    "Genre-Verteilung (gespeicherte Tracks)": (
        "Genre distribution (saved tracks)", "Répartition par genre (morceaux enregistrés)"),

    # --- Katalog & Track-Details --------------------------------------------
    "Katalog · SBS Catalog": ("Catalog · SBS Catalog", "Catalogue · SBS Catalog"),
    "Alle aus Music Architect eingelesenen Tracks inkl. Wasserzeichen-Status.": (
        "All tracks imported from Music Architect, incl. watermark status.",
        "Tous les morceaux importés de Music Architect, avec l'état du filigrane."),
    "alle": ("all", "tous"),
    "verfügbar": ("available", "disponible"),
    "geleast": ("leased", "loué"),
    "exklusiv verkauft": ("sold exclusively", "vendu en exclusivité"),
    "exklusiv": ("exclusive", "exclusif"),
    "Exklusiv": ("Exclusive", "Exclusif"),
    "Filter zurücksetzen": ("Reset filters", "Réinitialiser les filtres"),
    "Titel": ("Title", "Titre"),
    "Wasserzeichen": ("Watermark", "Filigrane"),
    "✓ verifiziert": ("✓ verified", "✓ vérifié"),
    "Tag ohne Hash": ("Tag without hash", "Tag sans hash"),
    "Prüfsumme passt nicht": ("Checksum mismatch", "Somme de contrôle incorrecte"),
    "Seed gespeichert": ("Seed stored", "Seed enregistré"),
    "kein WM": ("no WM", "pas de filigrane"),
    "Details →": ("Details →", "Détails →"),
    "Keine Tracks gefunden. Erzeuge Demo-Daten oder scanne eure Ausgabeordner.": (
        "No tracks found. Create demo data or scan your output folders.",
        "Aucun morceau trouvé. Générez des données de démo ou scannez vos dossiers de sortie."),
    "Demo-Daten erzeugen": ("Create demo data", "Générer des données de démo"),
    "Genre:": ("Genre:", "Genre :"),
    "· angelegt am": ("· created on", "· créé le"),
    "Wasserzeichen (Layer 1)": ("Watermark (layer 1)", "Filigrane (couche 1)"),
    "Katalog-Tag (copyright)": ("Catalog tag (copyright)", "Tag du catalogue (copyright)"),
    "SHA-256-Fingerprint": ("SHA-256 fingerprint", "Empreinte SHA-256"),
    "Quelldatei (MIDI)": ("Source file (MIDI)", "Fichier source (MIDI)"),
    "– keiner gelesen –": ("– none read –", "– aucun lu –"),
    "– kein Hash gelesen –": ("– no hash read –", "– aucun hash lu –"),
    "Gemasterte Exporte (DAW)": ("Mastered exports (DAW)", "Exports masterisés (DAW)"),
    "Stufe": ("Tier", "Niveau"),
    "Datei": ("File", "Fichier"),
    "Noch keine Exportdateien zugeordnet. Nach dem DAW-Export „Scannen“ klicken.": (
        "No export files linked yet. Click “Scan” after the DAW export.",
        "Aucun fichier d'export associé pour l'instant. Cliquez sur « Scanner » après l'export DAW."),
    "Lizenz verkaufen": ("Sell license", "Vendre une licence"),
    "Dieser Track wurde exklusiv verkauft und ist gesperrt. Eine weitere Lizenzierung ist nicht mehr möglich (Exklusiv-Schutz).": (
        "This track was sold exclusively and is locked. No further licensing is possible (exclusive protection).",
        "Ce morceau a été vendu en exclusivité et est verrouillé. Aucune autre licence n'est possible (protection d'exclusivité)."),
    "Lizenz-Stufe": ("License tier", "Niveau de licence"),
    " · EXKLUSIV": (" · EXCLUSIVE", " · EXCLUSIF"),
    "Käufer (registriert)": ("Buyer (registered)", "Acheteur (inscrit)"),
    "– Gast (kein Rabatt) –": ("– Guest (no discount) –", "– Invité (sans remise) –"),
    " (Abo, Rabatt)": (" (subscriber, discount)", " (abonné, remise)"),
    "Käufer-Name (falls Gast)": ("Buyer name (if guest)", "Nom de l'acheteur (si invité)"),
    "z. B. Max Mustermann": ("e.g. Jane Doe", "p. ex. Jean Dupont"),
    "Notiz": ("Note", "Note"),
    "optional": ("optional", "facultatif"),
    "Wird ein registrierter Abonnent als Käufer gewählt, zieht das System den Abo-Rabatt automatisch vom Listenpreis ab. Der Kauf zählt außerdem als Monats-Bezug des Käufers (gemeinsamer Topf mit Generierungen); bei erschöpftem Limit wird er abgelehnt.": (
        "If a registered subscriber is selected as buyer, the system automatically deducts the subscriber discount from the list price. The purchase also counts towards the buyer's monthly quota (shared pool with generations); it is rejected once the limit is reached.",
        "Si un abonné inscrit est choisi comme acheteur, le système déduit automatiquement la remise abonné du prix catalogue. L'achat compte aussi dans le quota mensuel de l'acheteur (pot commun avec les générations) ; il est refusé une fois la limite atteinte."),
    "Bei einer Exklusiv-Lizenz wird der Track anschließend automatisch für alle weiteren Verkäufe gesperrt.": (
        "With an exclusive license the track is then automatically locked for all further sales.",
        "Avec une licence exclusive, le morceau est ensuite automatiquement verrouillé pour toute autre vente."),
    "Lizenz-Historie": ("License history", "Historique des licences"),
    "Datum": ("Date", "Date"),
    "Typ": ("Type", "Type"),
    "Rabatt": ("Discount", "Remise"),
    "Preis": ("Price", "Prix"),
    "Checkout →": ("Checkout →", "Paiement →"),
    "Noch keine Lizenz verkauft.": ("No license sold yet.", "Aucune licence vendue pour l'instant."),
    "← zurück zum Katalog": ("← back to catalog", "← retour au catalogue"),
    "Track nicht gefunden.": ("Track not found.", "Morceau introuvable."),
    "Promo (MP3)": ("Promo (MP3)", "Promo (MP3)"),
    "Basic-Lizenz (MP3)": ("Basic license (MP3)", "Licence Basic (MP3)"),
    "Premium-Lizenz (WAV)": ("Premium license (WAV)", "Licence Premium (WAV)"),
    "Exklusiv (Vollrechte)": ("Exclusive (full rights)", "Exclusif (tous droits)"),

    # --- Lizenzen -----------------------------------------------------------
    "Lizenzen · SBS Catalog": ("Licenses · SBS Catalog", "Licences · SBS Catalog"),
    "Verkaufte Lizenzen": ("Licenses sold", "Licences vendues"),
    "Vollständige Verkaufshistorie über alle Tracks.": (
        "Complete sales history across all tracks.", "Historique complet des ventes pour tous les morceaux."),
    "Track": ("Track", "Morceau"),
    "Noch keine Lizenzen verkauft. Öffne einen Track im Katalog und verkaufe eine Lizenz.": (
        "No licenses sold yet. Open a track in the catalog and sell a license.",
        "Aucune licence vendue pour l'instant. Ouvrez un morceau du catalogue et vendez une licence."),
    "Lizenz nicht gefunden.": ("License not found.", "Licence introuvable."),
    "Diese Lizenz ist bereits bezahlt.": ("This license has already been paid.", "Cette licence est déjà payée."),
    "Bezahlte Lizenzen koennen nicht storniert werden.": (
        "Paid licenses cannot be cancelled.", "Les licences payées ne peuvent pas être annulées."),
    "Zahlung bestätigt — die Lizenz ist bezahlt.": (
        "Payment confirmed — the license is paid.", "Paiement confirmé — la licence est payée."),
    "Bestellung storniert, Track wieder freigegeben.": (
        "Order cancelled, track released again.", "Commande annulée, morceau de nouveau disponible."),
    "Unbekannte Preis-Stufe: %(tier)s": ("Unknown price tier: %(tier)s", "Niveau de prix inconnu : %(tier)s"),
    "'%(title)s' wurde bereits exklusiv verkauft und ist gesperrt. Keine weitere Lizenzierung moeglich.": (
        "'%(title)s' has already been sold exclusively and is locked. No further licensing possible.",
        "« %(title)s » a déjà été vendu en exclusivité et est verrouillé. Aucune autre licence n'est possible."),
    "Achtung: Fuer diesen Track existieren bereits %(n)s Lease-Lizenz(en).": (
        "Warning: %(n)s lease license(s) already exist for this track.",
        "Attention : %(n)s licence(s) de location existent déjà pour ce morceau."),

    # --- Dashboard & Wirtschaftlichkeit -------------------------------------
    "Dashboard · SBS Catalog": ("Dashboard · SBS Catalog", "Tableau de bord · SBS Catalog"),
    "Überblick über Katalog, Lizenzerlöse und Wirtschaftlichkeit.": (
        "Overview of catalog, license revenue and profitability.",
        "Vue d'ensemble du catalogue, des revenus de licences et de la rentabilité."),
    "Noch keine Daten": ("No data yet", "Pas encore de données"),
    "Es sind noch keine Tracks erfasst. Lade Demo-Daten (erzeugt echte wasserzeichenmarkierte MIDI-Dateien) oder setze in den Einstellungen die Pfade zu euren echten Ausgabeordnern und klicke oben auf „Scannen“.": (
        "No tracks have been recorded yet. Load demo data (creates real watermarked MIDI files) or set the paths to your real output folders in the settings and click “Scan” at the top.",
        "Aucun morceau n'est encore enregistré. Chargez des données de démo (crée de vrais fichiers MIDI filigranés) ou indiquez dans les paramètres les chemins de vos dossiers de sortie réels, puis cliquez sur « Scanner » en haut."),
    "↻ Jetzt scannen": ("↻ Scan now", "↻ Scanner maintenant"),
    "Pfade einstellen": ("Set paths", "Configurer les chemins"),
    "Tracks im Katalog": ("Tracks in catalog", "Morceaux au catalogue"),
    "verfügbar ·": ("available ·", "disponibles ·"),
    "geleast ·": ("leased ·", "loués ·"),
    "Umsatz gesamt": ("Total revenue", "Chiffre d'affaires total"),
    "· Abos": ("· Subscriptions", "· Abonnements"),
    "· Tokens": ("· Tokens", "· Jetons"),
    "Deckungsbeitrag": ("Contribution margin", "Marge sur coûts variables"),
    "Umsatz − variable Kosten": ("Revenue − variable costs", "Chiffre d'affaires − coûts variables"),
    "Gewinn n. Fixkosten": ("Profit after fixed costs", "Bénéfice après coûts fixes"),
    "ROI:": ("ROI:", "ROI :"),
    "Break-even": ("Break-even", "Seuil de rentabilité"),
    "Umsatz": ("Revenue", "Chiffre d'affaires"),
    "Break-even bei": ("Break-even at", "Seuil de rentabilité à"),
    "Die Fixkosten sind gedeckt — das Projekt arbeitet profitabel.": (
        "Fixed costs are covered — the project is profitable.",
        "Les coûts fixes sont couverts — le projet est rentable."),
    "Noch": ("Still", "Encore"),
    "Umsatz bis zur Deckung der einmaligen Investition.": (
        "in revenue needed to cover the one-off investment.",
        "de chiffre d'affaires pour couvrir l'investissement initial."),
    "Umsatz nach Lizenz-Stufe": ("Revenue by license tier", "Chiffre d'affaires par niveau de licence"),
    "Wirtschaftlichkeit · SBS Catalog": ("Profitability · SBS Catalog", "Rentabilité · SBS Catalog"),
    "Kosten-Nutzen-Betrachtung, Break-even und ROI auf Basis der erfassten Verkäufe.": (
        "Cost-benefit analysis, break-even and ROI based on recorded sales.",
        "Analyse coûts-bénéfices, seuil de rentabilité et ROI sur la base des ventes enregistrées."),
    "Umsatz (netto, bezahlt)": ("Revenue (net, paid)", "Chiffre d'affaires (HT, payé)"),
    "Offene Beträge": ("Outstanding amounts", "Montants en attente"),
    "unbezahlte Bestellung(en)": ("unpaid order(s)", "commande(s) impayée(s)"),
    "Fixkosten (Invest.)": ("Fixed costs (invest.)", "Coûts fixes (invest.)"),
    "Entwicklung + Werkzeuge": ("Development + tools", "Développement + outils"),
    "Gewinn": ("Profit", "Bénéfice"),
    "Rechenweg": ("Calculation", "Détail du calcul"),
    "Umsatz aus Lizenzen (bezahlt)": ("Revenue from licenses (paid)", "Chiffre d'affaires des licences (payé)"),
    "Umsatz aus Abos (bezahlt)": ("Revenue from subscriptions (paid)", "Chiffre d'affaires des abonnements (payé)"),
    "Umsatz aus Tokens (": ("Revenue from tokens (", "Chiffre d'affaires des jetons ("),
    "Stück, bezahlt)": ("units, paid)", "unités, payé)"),
    "= Umsatz gesamt": ("= Total revenue", "= Chiffre d'affaires total"),
    "− Variable Kosten (": ("− Variable costs (", "− Coûts variables ("),
    "Tracks ×": ("tracks ×", "morceaux ×"),
    "= Deckungsbeitrag": ("= Contribution margin", "= Marge sur coûts variables"),
    "− Fixkosten (": ("− Fixed costs (", "− Coûts fixes ("),
    "= Gewinn": ("= Profit", "= Bénéfice"),
    "Nötiger Umsatz zur Kostendeckung": (
        "Revenue needed to break even", "Chiffre d'affaires nécessaire pour couvrir les coûts"),
    "Lizenzen bei Ø": ("licenses at avg.", "licences à Ø"),
    "noch keine Verkäufe für Durchschnittspreis": (
        "no sales yet for an average price", "pas encore de ventes pour un prix moyen"),
    "% erreicht": ("% reached", "% atteint"),
    "Umsatz nach Genre": ("Revenue by genre", "Chiffre d'affaires par genre"),
    "Noch keine Verkäufe.": ("No sales yet.", "Pas encore de ventes."),
    "Die Kostenannahmen (Stundensatz, Stunden, Werkzeuge, Kosten pro Track) lassen sich unter": (
        "The cost assumptions (hourly rate, hours, tools, cost per track) can be adjusted under",
        "Les hypothèses de coûts (taux horaire, heures, outils, coût par morceau) se règlent dans"),
    "anpassen — ideal für Szenarien (pessimistisch / realistisch / optimistisch) in eurer Ausarbeitung.": (
        "— ideal for scenarios (pessimistic / realistic / optimistic) in your report.",
        "— idéal pour des scénarios (pessimiste / réaliste / optimiste) dans votre dossier."),

    # --- Nutzer & Abo (users.html) ------------------------------------------
    "Nutzer & Abo · SBS Catalog": ("Users & subscriptions · SBS Catalog", "Utilisateurs & abonnements · SBS Catalog"),
    "Nutzer & Abo": ("Users & subscriptions", "Utilisateurs & abonnements"),
    "Freemium-Modell: Abonnenten dürfen mehr Sounds pro Monat beziehen und erhalten Rabatt.": (
        "Freemium model: subscribers get more sounds per month and a discount.",
        "Modèle freemium : les abonnés ont droit à plus de sons par mois et à une remise."),
    "Limit Basis": ("Basic limit", "Limite de base"),
    "Limit Abo": ("Subscriber limit", "Limite abonné"),
    "Name": ("Name", "Nom"),
    "Abo-Status": ("Subscription status", "Statut d'abonnement"),
    "Bezüge diesen Monat": ("Usage this month", "Utilisation ce mois-ci"),
    "Generieren": ("Generate", "Générer"),
    "Abo buchen": ("Book subscription", "Souscrire un abonnement"),
    "bis": ("until", "jusqu'au"),
    "frei)": ("left)", "restants)"),
    "Positiv = gutschreiben, negativ = abziehen": (
        "Positive = credit, negative = deduct", "Positif = créditer, négatif = déduire"),
    "Mon. ·": ("mo. ·", "mois ·"),
    "Buchen": ("Book", "Souscrire"),
    "Noch keine Nutzer angelegt.": ("No users created yet.", "Aucun utilisateur créé pour l'instant."),
    "„Bezüge diesen Monat“ zählt Generierungen <em>und</em> gekaufte Lizenzen zusammen gegen den Monats-Topf (": (
        "“Usage this month” counts generations <em>and</em> purchased licenses together against the monthly pool (",
        "« Utilisation ce mois-ci » additionne les générations <em>et</em> les licences achetées dans le pot mensuel ("),
    "Basis /": ("basic /", "base /"),
    "Abo). „Buchen“ öffnet den simulierten Abo-Checkout; „▶“ erzeugt Tracks über den Gateway. Ist der Topf leer, deckt der Gateway weitere Tracks mit Tokens; „▶“ ist erst gesperrt, wenn auch kein Token-Guthaben mehr da ist. „±“ schreibt Tokens gut (positiv) oder zieht sie ab (negativ).": (
        "subscriber). “Book” opens the simulated subscription checkout; “▶” creates tracks via the gateway. If the pool is empty, the gateway covers further tracks with tokens; “▶” is only locked once the token balance is empty too. “±” credits tokens (positive) or deducts them (negative).",
        "abonné). « Souscrire » ouvre le paiement simulé de l'abonnement ; « ▶ » génère des morceaux via la passerelle. Si le pot est vide, la passerelle couvre les morceaux suivants avec des jetons ; « ▶ » n'est bloqué que lorsqu'il n'y a plus de jetons non plus. « ± » crédite des jetons (positif) ou en retire (négatif)."),
    "Token-Preise: Basis": ("Token prices: basic", "Prix des jetons : base"),
    "· Abo": ("· subscriber", "· abonné"),
    "je Token (netto).": ("per token (net).", "par jeton (HT)."),
    "Letzte Token-Bestellungen": ("Recent token orders", "Dernières commandes de jetons"),
    "Preisgruppe": ("Price group", "Groupe de prix"),
    "Noch keine Token-Bestellungen.": ("No token orders yet.", "Aucune commande de jetons pour l'instant."),
    "Neuen Nutzer anlegen": ("Create new user", "Créer un utilisateur"),
    "z. B. Studio Nord": ("e.g. Studio North", "p. ex. Studio Nord"),
    "als Abonnent anlegen": ("create as subscriber", "créer comme abonné"),
    "Nutzer anlegen": ("Create user", "Créer l'utilisateur"),
    "Bitte einen Namen angeben.": ("Please enter a name.", "Veuillez indiquer un nom."),
    "Nutzer '%(name)s' angelegt (Abo).": (
        "User '%(name)s' created (subscriber).", "Utilisateur « %(name)s » créé (abonné)."),
    "Nutzer '%(name)s' angelegt.": ("User '%(name)s' created.", "Utilisateur « %(name)s » créé."),

    # --- Einstellungen, Scan, Audit -----------------------------------------
    "Einstellungen · SBS Catalog": ("Settings · SBS Catalog", "Paramètres · SBS Catalog"),
    "Kopplung an die Sound-Programme, Kostenannahmen und Preis-Stufen.": (
        "Link to the sound programs, cost assumptions and price tiers.",
        "Couplage aux programmes audio, hypothèses de coûts et niveaux de prix."),
    "Kopplung (read-only Pfade)": ("Link (read-only paths)", "Couplage (chemins en lecture seule)"),
    "Diese Ordner werden nur <strong>gelesen</strong>. Es wird nichts an Music Architect oder der DAW verändert.": (
        "These folders are only <strong>read</strong>. Nothing is changed in Music Architect or the DAW.",
        "Ces dossiers sont uniquement <strong>lus</strong>. Rien n'est modifié dans Music Architect ni dans la DAW."),
    "Katalog-Ordner (Music Architect · .mid)": (
        "Catalog folder (Music Architect · .mid)", "Dossier du catalogue (Music Architect · .mid)"),
    "Export-Ordner (SBS-Synth · WAV/MP3)": (
        "Export folder (SBS-Synth · WAV/MP3)", "Dossier d'export (SBS-Synth · WAV/MP3)"),
    "Kostenannahmen": ("Cost assumptions", "Hypothèses de coûts"),
    "Entwicklungsstunden": ("Development hours", "Heures de développement"),
    "Stundensatz (€)": ("Hourly rate (€)", "Taux horaire (€)"),
    "Werkzeuge einmalig (€)": ("Tools, one-off (€)", "Outils, coût unique (€)"),
    "Kosten je Track (€)": ("Cost per track (€)", "Coût par morceau (€)"),
    "Abo & Abrechnung": ("Subscription & billing", "Abonnement & facturation"),
    "Limit Basis (Sounds/Monat)": ("Basic limit (sounds/month)", "Limite de base (sons/mois)"),
    "Limit Abo (Sounds/Monat)": ("Subscriber limit (sounds/month)", "Limite abonné (sons/mois)"),
    "Abo-Rabatt (%)": ("Subscriber discount (%)", "Remise abonné (%)"),
    "Abo-Preis pro Monat (€)": ("Subscription price per month (€)", "Prix de l'abonnement par mois (€)"),
    "Umsatzsteuer (%)": ("VAT (%)", "TVA (%)"),
    "Verkäufer (Rechnung)": ("Seller (invoice)", "Vendeur (facture)"),
    "Token-Nachkauf": ("Token top-up", "Achat de jetons"),
    "Netto-Stückpreis je Token, wenn das Kontingent aufgebraucht ist. Der Abo-Preis muss unter dem Basis-Preis liegen.": (
        "Net unit price per token once the quota is used up. The subscriber price must be below the basic price.",
        "Prix unitaire HT par jeton une fois le quota épuisé. Le prix abonné doit être inférieur au prix de base."),
    "Token-Preis Basis (€)": ("Token price, basic (€)", "Prix du jeton, base (€)"),
    "Token-Preis Abo (€)": ("Token price, subscriber (€)", "Prix du jeton, abonné (€)"),
    "Music Architect (Echtbetrieb)": ("Music Architect (live operation)", "Music Architect (mode réel)"),
    "Aufrufbefehl — leer = Simulationsmodus": (
        "Launch command — empty = simulation mode", "Commande d'appel — vide = mode simulation"),
    "Platzhalter": ("Placeholders", "Les espaces réservés"),
    "und": ("and", "et"),
    "werden ersetzt.": ("are replaced.", "sont remplacés."),
    "Preis-Stufen (an DAW-Exportziele angelehnt)": (
        "Price tiers (based on DAW export targets)", "Niveaux de prix (calqués sur les cibles d'export de la DAW)"),
    "Einstellungen speichern": ("Save settings", "Enregistrer les paramètres"),
    "Werkzeuge": ("Tools", "Outils"),
    "↻ Ordner scannen": ("↻ Scan folders", "↻ Scanner les dossiers"),
    "Protokoll als CSV": ("Audit log as CSV", "Journal en CSV"),
    "Einstellungen gespeichert.": ("Settings saved.", "Paramètres enregistrés."),
    "Einstellungen wurden nicht gespeichert.": ("Settings were not saved.", "Les paramètres n'ont pas été enregistrés."),
    "Katalog gescannt: %(added)s neu, %(updated)s aktualisiert (%(scanned)s Dateien).": (
        "Catalog scanned: %(added)s new, %(updated)s updated (%(scanned)s files).",
        "Catalogue scanné : %(added)s nouveaux, %(updated)s mis à jour (%(scanned)s fichiers)."),
    "Exporte gescannt: %(linked)s verknuepft, %(unmatched)s ohne Zuordnung.": (
        "Exports scanned: %(linked)s linked, %(unmatched)s unmatched.",
        "Exports scannés : %(linked)s associés, %(unmatched)s sans correspondance."),
    "Demo-Daten erzeugt: %(midi)s MIDI-Dateien, %(exports)s Exporte. Jetzt 'Scannen' klicken.": (
        "Demo data created: %(midi)s MIDI files, %(exports)s exports. Now click 'Scan'.",
        "Données de démo générées : %(midi)s fichiers MIDI, %(exports)s exports. Cliquez maintenant sur « Scanner »."),
    "Katalog-Ordner nicht gefunden: %(dir)s": ("Catalog folder not found: %(dir)s", "Dossier du catalogue introuvable : %(dir)s"),
    "Export-Ordner nicht gefunden: %(dir)s": ("Export folder not found: %(dir)s", "Dossier d'export introuvable : %(dir)s"),
    "Anzahl muss mindestens 1 sein.": ("Count must be at least 1.", "Le nombre doit être au moins 1."),
    "Simulation fehlgeschlagen (mido nicht verfuegbar).": (
        "Simulation failed (mido not available).", "Échec de la simulation (mido non disponible)."),
    "Music Architect endete mit Fehlercode %(code)s.": (
        "Music Architect exited with error code %(code)s.", "Music Architect s'est terminé avec le code d'erreur %(code)s."),
    "Aufruf von Music Architect fehlgeschlagen: %(exc)s": (
        "Calling Music Architect failed: %(exc)s", "Échec de l'appel de Music Architect : %(exc)s"),
    "Protokoll · SBS Catalog": ("Audit log · SBS Catalog", "Journal · SBS Catalog"),
    "Audit-Protokoll": ("Audit log", "Journal d'audit"),
    "Revisionssichere Aufzeichnung aller geschäftsrelevanten Aktionen.": (
        "Tamper-evident record of all business-relevant actions.",
        "Enregistrement infalsifiable de toutes les actions pertinentes pour l'activité."),
    "↓ Als CSV exportieren": ("↓ Export as CSV", "↓ Exporter en CSV"),
    "Zeitstempel": ("Timestamp", "Horodatage"),
    "Ereignis": ("Event", "Événement"),
    "Objekt": ("Object", "Objet"),
    "Details": ("Details", "Détails"),
    "Noch keine Ereignisse protokolliert.": ("No events logged yet.", "Aucun événement enregistré pour l'instant."),
    "Suchbegriffe, z. B. Token": ("Search terms, e.g. token", "Mots-clés, p. ex. jeton"),
    "Protokoll durchsuchen": ("Search the audit log", "Rechercher dans le journal"),
    "Suchen": ("Search", "Rechercher"),
    "Suche zurücksetzen": ("Clear search", "Effacer la recherche"),
    "%(n)s Einträge für „%(q)s“ (die neuesten zuerst, höchstens 500).": (
        "%(n)s entries for “%(q)s” (newest first, at most 500).",
        "%(n)s entrées pour « %(q)s » (les plus récentes d'abord, 500 au maximum)."),
    "Keine Einträge für „%(q)s“ gefunden.": ("No entries found for “%(q)s”.", "Aucune entrée trouvée pour « %(q)s »."),
    "Zurück zum Generator": ("Back to the generator", "Retour au générateur"),

    # --- Generator: Server-Meldungen ----------------------------------------
    "Seed %(seed)s wurde bereits exklusiv verkauft und kann nicht erneut generiert werden.": (
        "Seed %(seed)s has already been sold exclusively and cannot be generated again.",
        "Le seed %(seed)s a déjà été vendu en exclusivité et ne peut pas être généré à nouveau."),
    "Der Seed muss eine ganze Zahl sein.": (
        "The seed must be a whole number.", "Le seed doit être un nombre entier."),
    "Rendering fehlgeschlagen: WAV-Datei fehlt oder ist leer. Bitte Server-Log pruefen.": (
        "Rendering failed: WAV file is missing or empty. Please check the server log.",
        "Échec du rendu : le fichier WAV est absent ou vide. Veuillez consulter le journal du serveur."),
    "Kein generiertes Audio gefunden. Bitte zuerst generieren.": (
        "No generated audio found. Please generate first.", "Aucun audio généré trouvé. Veuillez d'abord générer."),
    "Temporaere Datei fehlt. Bitte neu generieren.": (
        "Temporary file is missing. Please generate again.", "Fichier temporaire manquant. Veuillez générer à nouveau."),
    "Berater-Daten nicht gefunden — bitte neu generieren.": (
        "Advisor data not found — please generate again.", "Données du conseiller introuvables — veuillez générer à nouveau."),
    "Keine Datei empfangen.": ("No file received.", "Aucun fichier reçu."),
    "Keine Datei empfangen": ("No file received", "Aucun fichier reçu"),
    "Nur .sf2-Dateien erlaubt.": ("Only .sf2 files are allowed.", "Seuls les fichiers .sf2 sont autorisés."),
    "Das Format '%(fmt)s' erfordert ffmpeg. Bitte ffmpeg installieren und im PATH verfuegbar machen.": (
        "The format '%(fmt)s' requires ffmpeg. Please install ffmpeg and make it available in the PATH.",
        "Le format « %(fmt)s » nécessite ffmpeg. Veuillez installer ffmpeg et le rendre disponible dans le PATH."),
    "Keine PDF-Bibliothek installiert. Bitte 'pip install reportlab' oder 'pip install fpdf2' ausfuehren.": (
        "No PDF library installed. Please run 'pip install reportlab' or 'pip install fpdf2'.",
        "Aucune bibliothèque PDF installée. Veuillez exécuter 'pip install reportlab' ou 'pip install fpdf2'."),
    "audio_uuid fehlt": ("audio_uuid missing", "audio_uuid manquant"),
    "Ungueltiger Track-Key: '%(key)s'": ("Invalid track key: '%(key)s'", "Clé de piste invalide : « %(key)s »"),
    "Format '%(ext)s' nicht unterstuetzt. Erlaubt: %(allowed)s": (
        "Format '%(ext)s' not supported. Allowed: %(allowed)s",
        "Format « %(ext)s » non pris en charge. Autorisés : %(allowed)s"),
    "Kompositions-Session nicht gefunden": ("Composition session not found", "Session de composition introuvable"),
    "Kompositions-Verzeichnis fehlt": ("Composition directory missing", "Répertoire de composition manquant"),
    "Datei konnte nicht gespeichert werden": ("File could not be saved", "Le fichier n'a pas pu être enregistré"),
    "Datei ueberschreitet 20-MB-Limit (%(mb)s MB empfangen)": (
        "File exceeds the 20 MB limit (%(mb)s MB received)", "Le fichier dépasse la limite de 20 Mo (%(mb)s Mo reçus)"),

    # --- Generator: Oberflaeche (generate.html) -----------------------------
    "Beat generieren — SBS CATALOG": ("Generate beat — SBS CATALOG", "Générer un beat — SBS CATALOG"),
    "Kontingent": ("Quota", "Quota"),
    "diesen Monat frei ·": ("left this month ·", "restants ce mois-ci ·"),
    "Kontingent aufgebraucht? Mit Tokens kannst du weitere Beats speichern und exportieren.": (
        "Quota used up? With tokens you can save and export more beats.",
        "Quota épuisé ? Avec des jetons, vous pouvez enregistrer et exporter d'autres beats."),
    "+ kaufen": ("+ buy", "+ acheter"),
    "Prompt-Eingabe": ("Prompt input", "Saisie du prompt"),
    "z. B. &quot;Bright POP Song&quot; oder &quot;fast dark trap beat&quot;": (
        "e.g. &quot;Bright POP Song&quot; or &quot;fast dark trap beat&quot;",
        "p. ex. &quot;Bright POP Song&quot; ou &quot;fast dark trap beat&quot;"),
    "Beschreibe deinen Beat auf Englisch oder Deutsch.&#10;Beispiel: &quot;dark trap beat 140 BPM&quot;&#10;Das System erkennt Genre, BPM und Stimmung automatisch.": (
        "Describe your beat in English or German.&#10;Example: &quot;dark trap beat 140 BPM&quot;&#10;The system detects genre, BPM and mood automatically.",
        "Décrivez votre beat en anglais ou en allemand.&#10;Exemple : &quot;dark trap beat 140 BPM&quot;&#10;Le système détecte automatiquement le genre, le BPM et l'ambiance."),
    "Analysiert den Prompt und fuellt Genre, BPM und andere Parameter automatisch aus.": (
        "Analyzes the prompt and fills in genre, BPM and other parameters automatically.",
        "Analyse le prompt et remplit automatiquement le genre, le BPM et d'autres paramètres."),
    "&#9675; Erkennen": ("&#9675; Detect", "&#9675; Détecter"),
    "Basis-Parameter": ("Basic parameters", "Paramètres de base"),
    "Waehle das musikalische Genre.&#10;Bestimmt Rhythmus-Pattern, Instrumente und Klangcharakter.": (
        "Choose the musical genre.&#10;Determines rhythm patterns, instruments and sound character.",
        "Choisissez le genre musical.&#10;Détermine les motifs rythmiques, les instruments et le caractère sonore."),
    "Beats pro Minute — Tempo des Beats.&#10;Leer lassen = automatisch aus dem Genre bestimmt.&#10;Typisch: Trap 130-160, House 120-130, Techno 130-150.": (
        "Beats per minute — tempo of the beat.&#10;Leave empty = derived automatically from the genre.&#10;Typical: Trap 130-160, House 120-130, Techno 130-150.",
        "Battements par minute — tempo du beat.&#10;Laisser vide = déterminé automatiquement d'après le genre.&#10;Typique : Trap 130-160, House 120-130, Techno 130-150."),
    "Wie komplex soll der Beat sein?&#10;1 = minimalistisch (wenige Noten, einfache Pattern)&#10;10 = sehr dicht (viele Noten, komplexe Strukturen)&#10;Empfehlung fuer Einsteiger: 4-6": (
        "How complex should the beat be?&#10;1 = minimalist (few notes, simple patterns)&#10;10 = very dense (many notes, complex structures)&#10;Recommended for beginners: 4-6",
        "Quelle complexité pour le beat ?&#10;1 = minimaliste (peu de notes, motifs simples)&#10;10 = très dense (beaucoup de notes, structures complexes)&#10;Conseil pour débutants : 4-6"),
    "Komplexitaet (1-10)": ("Complexity (1-10)", "Complexité (1-10)"),
    "Zufallszahl fuer reproduzierbare Ergebnisse.&#10;Gleicher Seed + gleiche Parameter = gleicher Beat.&#10;Leer lassen fuer einen zufaelligen Seed.": (
        "Random number for reproducible results.&#10;Same seed + same parameters = same beat.&#10;Leave empty for a random seed.",
        "Nombre aléatoire pour des résultats reproductibles.&#10;Même seed + mêmes paramètres = même beat.&#10;Laisser vide pour un seed aléatoire."),
    "zufaellig": ("random", "aléatoire"),
    "Tonart &amp; Struktur": ("Key &amp; structure", "Tonalité &amp; structure"),
    "Grundton der Melodie und Akkorde.&#10;C = hell und neutral, A-Moll = melancholisch.&#10;&quot;auto&quot; = vom System bestimmt.": (
        "Root note of melody and chords.&#10;C = bright and neutral, A minor = melancholic.&#10;&quot;auto&quot; = chosen by the system.",
        "Note fondamentale de la mélodie et des accords.&#10;Do = clair et neutre, La mineur = mélancolique.&#10;&quot;auto&quot; = choisi par le système."),
    "Ton": ("Note", "Note"),
    "Tonleiter bestimmt den emotionalen Charakter.&#10;Major = froehlich · Minor = melancholisch&#10;Dorian = jazzig · Phrygian = spanisch/dunkel&#10;Pentatonik = eingaengige Melodien.": (
        "The scale determines the emotional character.&#10;Major = cheerful · Minor = melancholic&#10;Dorian = jazzy · Phrygian = Spanish/dark&#10;Pentatonic = catchy melodies.",
        "La gamme détermine le caractère émotionnel.&#10;Major = joyeux · Minor = mélancolique&#10;Dorian = jazzy · Phrygian = espagnol/sombre&#10;Pentatonique = mélodies accrocheuses."),
    "Tonleiter": ("Scale", "Gamme"),
    "Laenge des Beats in Takten (Bars).&#10;0 = automatisch (Genre-abhaengig, meist 8-16 Takte).&#10;1 Takt = 4 Viertelschlaege bei 4/4-Takt.": (
        "Length of the beat in bars.&#10;0 = automatic (depends on genre, usually 8-16 bars).&#10;1 bar = 4 quarter beats in 4/4 time.",
        "Longueur du beat en mesures.&#10;0 = automatique (selon le genre, généralement 8-16 mesures).&#10;1 mesure = 4 temps en 4/4."),
    "Dauer (Takte, 0 = auto)": ("Length (bars, 0 = auto)", "Durée (mesures, 0 = auto)"),
    "Klang &amp; Ausdruck": ("Sound &amp; expression", "Son &amp; expression"),
    "Macht Noten lebendig durch zufaellige Timing- und Lautstaerkeschwankungen.&#10;0 = Maschinen-perfekt (quantisiert)&#10;0.6 = natuerlich gespielt&#10;1 = stark unpraeziese (Jazz/Live-Feeling)": (
        "Brings notes to life with random timing and volume variations.&#10;0 = machine-perfect (quantized)&#10;0.6 = naturally played&#10;1 = very loose (jazz/live feel)",
        "Donne vie aux notes par des variations aléatoires de timing et de volume.&#10;0 = perfection mécanique (quantifié)&#10;0.6 = jeu naturel&#10;1 = très imprécis (feeling jazz/live)"),
    "Humanisierung": ("Humanization", "Humanisation"),
    "Zufaellige Abweichungen in der Akkord-Progression und Melodie.&#10;0 = vorhersehbar und strukturiert&#10;0.5 = gelegentliche Variationen&#10;1 = stark variierendes Arrangement": (
        "Random deviations in chord progression and melody.&#10;0 = predictable and structured&#10;0.5 = occasional variations&#10;1 = strongly varying arrangement",
        "Écarts aléatoires dans la progression d'accords et la mélodie.&#10;0 = prévisible et structuré&#10;0.5 = variations occasionnelles&#10;1 = arrangement très varié"),
    "Emotionale Spannung durch dissonante Akkorde und Noten.&#10;0 = harmonisch und entspannt&#10;0.7 = dramatisch&#10;1.5 = sehr dissonant / experimentell": (
        "Emotional tension through dissonant chords and notes.&#10;0 = harmonious and relaxed&#10;0.7 = dramatic&#10;1.5 = very dissonant / experimental",
        "Tension émotionnelle grâce à des accords et notes dissonants.&#10;0 = harmonieux et détendu&#10;0.7 = dramatique&#10;1.5 = très dissonant / expérimental"),
    "Spannung": ("Tension", "Tension"),
    "Klangfaerbung durch Effektketten.&#10;Bright = klar, knackig, hochfrequent betont&#10;Neutral = ausgewogen, ohne Faerbung&#10;Dark = dumpf, druckig, tieffrequent betont": (
        "Tone coloring through effect chains.&#10;Bright = clear, crisp, emphasized highs&#10;Neutral = balanced, uncolored&#10;Dark = muffled, punchy, emphasized lows",
        "Coloration sonore par des chaînes d'effets.&#10;Bright = clair, incisif, aigus accentués&#10;Neutral = équilibré, sans coloration&#10;Dark = sourd, percutant, graves accentués"),
    "FX-Kette": ("FX chain", "Chaîne FX"),
    "Generierungsmodus": ("Generation mode", "Mode de génération"),
    "Full Beat = vollstaendiger Beat mit allen Spuren&#10;Vocal-Ready = Melodie und Arpeggio weichen in Strophe und Refrain eine Oktave nach unten aus — Platz fuer Gesang&#10;Beide = derselbe Beat als Full Beat und als Vocal-Ready": (
        "Full Beat = complete beat with all tracks&#10;Vocal-Ready = melody and arpeggio move an octave down in verses and choruses — room for vocals&#10;Both = the same beat as Full Beat and as Vocal-Ready",
        "Full Beat = beat complet avec toutes les pistes&#10;Vocal-Ready = la mélodie et l'arpège descendent d'une octave dans les couplets et refrains — place pour le chant&#10;Les deux = le même beat en Full Beat et en Vocal-Ready"),
    "<strong>Full Beat</strong> = vollstaendige Komposition · <strong>Vocal-Ready</strong> = Melodie tiefer, Platz fuer Gesang · <strong>Beide</strong> = beide Fassungen desselben Beats": (
        "<strong>Full Beat</strong> = complete composition · <strong>Vocal-Ready</strong> = lower melody, room for vocals · <strong>Both</strong> = both versions of the same beat",
        "<strong>Full Beat</strong> = composition complète · <strong>Vocal-Ready</strong> = mélodie plus grave, place pour le chant · <strong>Les deux</strong> = les deux versions du même beat"),
    "Fusion-Modus": ("Fusion mode", "Mode fusion"),
    "Fusion kombiniert zwei Genres zu einem hybriden Beat.&#10;Aus = normales Genre-Modus&#10;Preset = vordefinierte Genre-Kombination&#10;Custom-Mix = freie Auswahl und Verhaeltnis zweier Genres": (
        "Fusion combines two genres into a hybrid beat.&#10;Off = normal genre mode&#10;Preset = predefined genre combination&#10;Custom mix = free choice and ratio of two genres",
        "La fusion combine deux genres en un beat hybride.&#10;Off = mode genre normal&#10;Preset = combinaison de genres prédéfinie&#10;Custom-Mix = choix libre et proportion de deux genres"),
    "Aus": ("Off", "Off"),
    "Keine Presets verfuegbar": ("No presets available", "Aucun preset disponible"),
    "Instrumente &amp; Mixer": ("Instruments &amp; mixer", "Instruments &amp; mixeur"),
    "Soundfont (SF2) bestimmt den Grundklang aller Instrumente.&#10;Genre-Standard = automatisch passende Bibliothek.&#10;Wird auf den Advisor-Mixer-SF2 synchronisiert.": (
        "The soundfont (SF2) determines the basic sound of all instruments.&#10;Genre default = automatically matching library.&#10;Is synchronized with the advisor mixer SF2.",
        "La soundfont (SF2) détermine le son de base de tous les instruments.&#10;Standard du genre = bibliothèque adaptée automatiquement.&#10;Synchronisée avec le SF2 du mixeur Advisor."),
    "— Genre-Standard (SF2) —": ("— Genre default (SF2) —", "— Standard du genre (SF2) —"),
    "Startet die Beat-Generierung mit den aktuellen Parametern.&#10;Das dauert ca. 10-30 Sekunden — bitte warten.": (
        "Starts beat generation with the current parameters.&#10;This takes about 10-30 seconds — please wait.",
        "Lance la génération du beat avec les paramètres actuels.&#10;Cela prend environ 10 à 30 secondes — veuillez patienter."),
    "&#9654; Beat generieren": ("&#9654; Generate beat", "&#9654; Générer le beat"),
    "Generierung laeuft&#8230;": ("Generating&#8230;", "Génération en cours&#8230;"),
    "Vorschau &amp; Speichern": ("Preview &amp; save", "Aperçu &amp; enregistrement"),
    "Ausgabe": ("Output", "Sortie"),
    "Wellenform": ("Waveform", "Forme d'onde"),
    "Abspielen / Anhalten": ("Play / pause", "Lecture / pause"),
    "&#8659; Diesen Re-Render exportieren": ("&#8659; Export this re-render", "&#8659; Exporter ce re-rendu"),
    "&#8617; Als Hauptversion verwenden": ("&#8617; Use as main version", "&#8617; Utiliser comme version principale"),
    "&#8659; Exportieren": ("&#8659; Export", "&#8659; Exporter"),
    "Noch kein Beat generiert. Parameter links auswaehlen und auf <strong>Beat generieren</strong> klicken.": (
        "No beat generated yet. Choose parameters on the left and click <strong>Generate beat</strong>.",
        "Aucun beat généré pour l'instant. Choisissez les paramètres à gauche et cliquez sur <strong>Générer le beat</strong>."),
    "Seed (optional)": ("Seed (optional)", "Seed (facultatif)"),
    "Reset": ("Reset", "Réinitialiser"),
    "Jahr": ("Year", "Année"),
    "Dauer": ("Duration", "Durée"),
    "Takte": ("Bars", "Mesures"),
    "AKKORDE": ("CHORDS", "ACCORDS"),
    "SPUREN": ("TRACKS", "PISTES"),
    "Nach der Generierung werden hier Song-Metadaten, Akkorde und Spur-Statistiken angezeigt.": (
        "After generation, song metadata, chords and track statistics are shown here.",
        "Après la génération, les métadonnées du morceau, les accords et les statistiques des pistes s'affichent ici."),
    "Nach der Generierung wird hier die Wellenform angezeigt.": (
        "After generation, the waveform is shown here.", "Après la génération, la forme d'onde s'affiche ici."),
    "Die Piano Roll wird nach der Generierung angezeigt.": (
        "The piano roll is shown after generation.", "Le piano roll s'affiche après la génération."),
    "Palette &amp; Prompt-Analyse": ("Palette &amp; prompt analysis", "Palette &amp; analyse du prompt"),
    "Instrumente": ("Instruments", "Instruments"),
    "Spur": ("Track", "Piste"),
    "Gain Staging &amp; Ziele": ("Gain staging &amp; targets", "Gain staging &amp; cibles"),
    "Effektketten": ("Effect chains", "Chaînes d'effets"),
    "Frequenzallokation": ("Frequency allocation", "Répartition des fréquences"),
    "BPM-Zeitwerte": ("BPM time values", "Valeurs temporelles BPM"),
    "Export-Ziele": ("Export targets", "Cibles d'export"),
    "Rendert jede Spur einzeln als separates Audio.&#10;So kannst du jedes Instrument isoliert abhoeren.&#10;Dauert etwas laenger als ein normales Rendering.": (
        "Renders each track individually as separate audio.&#10;This lets you listen to each instrument in isolation.&#10;Takes a little longer than a normal rendering.",
        "Rend chaque piste séparément en audio distinct.&#10;Vous pouvez ainsi écouter chaque instrument isolément.&#10;Prend un peu plus de temps qu'un rendu normal."),
    "&#9654; ALLE SOLOS RENDERN": ("&#9654; RENDER ALL SOLOS", "&#9654; RENDRE TOUS LES SOLOS"),
    "Loescht alle Solo-Vorschaufiles und setzt die Solo-Ansicht zurueck.": (
        "Deletes all solo preview files and resets the solo view.",
        "Supprime tous les fichiers d'aperçu solo et réinitialise la vue solo."),
    "&#10005; SOLOS ZURUECKSETZEN": ("&#10005; RESET SOLOS", "&#10005; RÉINITIALISER LES SOLOS"),
    "Swing verschiebt jeden zweiten 16tel-Schlag nach hinten.&#10;50% = gerades Timing (kein Swing)&#10;60-65% = typischer Trap/Hip-Hop Swing&#10;75% = stark geshuffelt (Jazz-Feeling)": (
        "Swing delays every second 16th note.&#10;50% = straight timing (no swing)&#10;60-65% = typical trap/hip-hop swing&#10;75% = heavily shuffled (jazz feel)",
        "Le swing retarde une double croche sur deux.&#10;50% = timing droit (pas de swing)&#10;60-65% = swing typique trap/hip-hop&#10;75% = très shufflé (feeling jazz)"),
    "Verschiebt alle Noten dieser Spur zeitlich.&#10;Negative Werte = Spur spielt frueh (aggressiver)&#10;Positive Werte = Spur spielt spaet (entspannter)&#10;Bereich: -100 bis +100 Millisekunden": (
        "Shifts all notes of this track in time.&#10;Negative values = track plays early (more aggressive)&#10;Positive values = track plays late (more relaxed)&#10;Range: -100 to +100 milliseconds",
        "Décale dans le temps toutes les notes de cette piste.&#10;Valeurs négatives = la piste joue en avance (plus agressif)&#10;Valeurs positives = la piste joue en retard (plus détendu)&#10;Plage : -100 à +100 millisecondes"),
    "Lautstaerke-Untergrenze fuer diese Spur (MIDI-Velocity).&#10;1 = sehr leise, 64 = mittel, 127 = volle Lautstaerke.&#10;Zusammen mit Vel max ergibt sich der Dynamikbereich.": (
        "Lower volume limit for this track (MIDI velocity).&#10;1 = very quiet, 64 = medium, 127 = full volume.&#10;Together with Vel max this gives the dynamic range.",
        "Limite inférieure de volume pour cette piste (vélocité MIDI).&#10;1 = très faible, 64 = moyen, 127 = volume maximal.&#10;Avec Vel max, cela définit la plage dynamique."),
    "Lautstaerke-Obergrenze fuer diese Spur (MIDI-Velocity).&#10;Muss groesser als Vel min sein.&#10;Kleiner Abstand = wenig Dynamik, grosser = viel.": (
        "Upper volume limit for this track (MIDI velocity).&#10;Must be greater than Vel min.&#10;Small gap = little dynamics, large gap = a lot.",
        "Limite supérieure de volume pour cette piste (vélocité MIDI).&#10;Doit être supérieure à Vel min.&#10;Petit écart = peu de dynamique, grand écart = beaucoup."),
    "Lautstaerke-Kurve ueber den Takt.&#10;Gleichmaessig = alle Noten gleich laut&#10;Betont = Zaehler 1 und 3 betonter&#10;Crescendo = wird lauter&#10;Diminuendo = wird leiser": (
        "Volume curve across the bar.&#10;Even = all notes equally loud&#10;Accented = beats 1 and 3 emphasized&#10;Crescendo = gets louder&#10;Diminuendo = gets quieter",
        "Courbe de volume sur la mesure.&#10;Uniforme = toutes les notes au même volume&#10;Accentué = temps 1 et 3 accentués&#10;Crescendo = de plus en plus fort&#10;Diminuendo = de plus en plus doux"),
    "Kurve": ("Curve", "Courbe"),
    "Gleichmaessig": ("Even", "Uniforme"),
    "Betont": ("Accented", "Accentué"),
    "Speichert diese Groove-Parameter fuer die ausgewaehlte Spur.&#10;Erst nach &quot;GROOVE ANWENDEN&quot; werden die Aenderungen gerendert.": (
        "Saves these groove parameters for the selected track.&#10;The changes are only rendered after &quot;APPLY GROOVE&quot;.",
        "Enregistre ces paramètres de groove pour la piste sélectionnée.&#10;Les modifications ne sont rendues qu'après &quot;APPLIQUER LE GROOVE&quot;."),
    "&#10003; Uebernehmen": ("&#10003; Apply", "&#10003; Appliquer"),
    "HUMANISIERUNG": ("HUMANIZATION", "HUMANISATION"),
    "Zufaellige Lautstaerkeschwankung pro Note (alle Spuren).&#10;0 = alle Noten exakt gleich laut&#10;±15 = natuerlich, lebendig&#10;±30 = stark variierend (Handgespielt-Feeling)": (
        "Random volume variation per note (all tracks).&#10;0 = all notes exactly equally loud&#10;±15 = natural, lively&#10;±30 = strongly varying (hand-played feel)",
        "Variation aléatoire du volume par note (toutes les pistes).&#10;0 = toutes les notes exactement au même volume&#10;±15 = naturel, vivant&#10;±30 = très variable (feeling joué à la main)"),
    "Zufaellige Timing-Abweichung pro Note (alle Spuren).&#10;0 = perfekt quantisiert&#10;±10 ms = leicht menschlich&#10;±50 ms = stark unpraeziese (Vintage-Feeling)": (
        "Random timing deviation per note (all tracks).&#10;0 = perfectly quantized&#10;±10 ms = slightly human&#10;±50 ms = very loose (vintage feel)",
        "Écart de timing aléatoire par note (toutes les pistes).&#10;0 = parfaitement quantifié&#10;±10 ms = légèrement humain&#10;±50 ms = très imprécis (feeling vintage)"),
    "Zufallszahl fuer reproduzierbare Humanisierung.&#10;Gleicher Seed = gleiche zufaellige Abweichungen.&#10;Leer = bei jedem Rendern neu berechnet.": (
        "Random number for reproducible humanization.&#10;Same seed = same random deviations.&#10;Empty = recalculated on every render.",
        "Nombre aléatoire pour une humanisation reproductible.&#10;Même seed = mêmes écarts aléatoires.&#10;Vide = recalculé à chaque rendu."),
    "Seed (leer = neu)": ("Seed (empty = new)", "Seed (vide = nouveau)"),
    "Generiert einen neuen zufaelligen Seed und rendert sofort neu.": (
        "Generates a new random seed and re-renders immediately.",
        "Génère un nouveau seed aléatoire et relance aussitôt le rendu."),
    "W&#252;rfeln": ("Roll dice", "Lancer les dés"),
    "Setzt alle Groove-Parameter auf die Standardwerte zurueck.": (
        "Resets all groove parameters to their defaults.",
        "Réinitialise tous les paramètres de groove aux valeurs par défaut."),
    "Leeren": ("Clear", "Vider"),
    "PALETTE &amp; FX-KETTE": ("PALETTE &amp; FX CHAIN", "PALETTE &amp; CHAÎNE FX"),
    "Instrument-Palette: vordefiniertes Set von GM-Instrumenten passend zum Genre.&#10;Jede Palette klingt anders — experimentiere!&#10;Erst Beat generieren, dann Palette wechseln und neu rendern.": (
        "Instrument palette: predefined set of GM instruments matching the genre.&#10;Every palette sounds different — experiment!&#10;Generate a beat first, then switch palette and re-render.",
        "Palette d'instruments : ensemble prédéfini d'instruments GM adapté au genre.&#10;Chaque palette sonne différemment — expérimentez !&#10;Générez d'abord un beat, puis changez de palette et relancez le rendu."),
    "— zuerst Beat generieren —": ("— generate a beat first —", "— générez d'abord un beat —"),
    "NATURAL: Kein zusaetzlicher EQ oder Kompressor.&#10;Klingt wie direkt aus dem Synthesizer.": (
        "NATURAL: no additional EQ or compressor.&#10;Sounds as if straight from the synthesizer.",
        "NATURAL : pas d'égaliseur ni de compresseur supplémentaire.&#10;Sonne comme directement sorti du synthétiseur."),
    "POLISHED: Mehr Hoehen, sanfte Kompression.&#10;Professioneller, kommerzieller Sound.": (
        "POLISHED: more highs, gentle compression.&#10;Professional, commercial sound.",
        "POLISHED : plus d'aigus, compression douce.&#10;Son professionnel et commercial."),
    "UNDERGROUND: Tiefpass-Filter, Saettigung.&#10;Rawer, dreckiger, analog-klingender Sound.": (
        "UNDERGROUND: low-pass filter, saturation.&#10;Raw, dirty, analog-sounding.",
        "UNDERGROUND : filtre passe-bas, saturation.&#10;Son brut, sale, de type analogique."),
    "BDRA-Theoriepruefer: analysiert 5 Klangprinzipien.&#10;P1 Sub-Bass · P2 Register · P3 Attack&#10;P4 Dichte · P5 Helligkeit&#10;Score 80+ = professionell ausgewogen.": (
        "BDRA theory checker: analyzes 5 sound principles.&#10;P1 sub-bass · P2 register · P3 attack&#10;P4 density · P5 brightness&#10;Score 80+ = professionally balanced.",
        "Vérificateur théorique BDRA : analyse 5 principes sonores.&#10;P1 sub-basse · P2 registre · P3 attaque&#10;P4 densité · P5 brillance&#10;Score 80+ = équilibre professionnel."),
    "THEORIE": ("THEORY", "THÉORIE"),
    "Analysiert das aktuelle Beat-Arrangement nach psychoakustischen Regeln.": (
        "Analyzes the current beat arrangement according to psychoacoustic rules.",
        "Analyse l'arrangement actuel du beat selon des règles psychoacoustiques."),
    "&#10003; Pruefen": ("&#10003; Check", "&#10003; Vérifier"),
    "P4 Dichte": ("P4 Density", "P4 Densité"),
    "P5 Helligkeit": ("P5 Brightness", "P5 Brillance"),
    "P1 Sub-Bass": ("P1 Sub-bass", "P1 Sub-basse"),
    "P2 Register": ("P2 Register", "P2 Registre"),
    "P3 Attack": ("P3 Attack", "P3 Attaque"),
    "Instrumente (vor Re-Rendering &#228;ndern)": (
        "Instruments (change before re-rendering)", "Instruments (à modifier avant le re-rendu)"),
    "Weise jeder Spur eine eigene Audio-Datei zu.&#10;Die Datei ersetzt den eingebauten Synthesizer fuer diese Spur.&#10;Unterstuetzte Formate: WAV, MP3, OGG, FLAC.": (
        "Assign your own audio file to each track.&#10;The file replaces the built-in synthesizer for that track.&#10;Supported formats: WAV, MP3, OGG, FLAC.",
        "Attribuez à chaque piste votre propre fichier audio.&#10;Le fichier remplace le synthétiseur intégré pour cette piste.&#10;Formats pris en charge : WAV, MP3, OGG, FLAC."),
    "Samples (eigene Audio-Dateien pro Track)": (
        "Samples (your own audio files per track)", "Samples (vos fichiers audio par piste)"),
    "Klangsynthese-Editor fuer einzelne Instrumente.&#10;Preset laden = Startwerte fuer das Instrument&#10;Dann mit den Reglern feinabstimmen.&#10;Wirkung erst nach &quot;GROOVE ANWENDEN&quot; sichtbar.": (
        "Sound synthesis editor for individual instruments.&#10;Load preset = starting values for the instrument&#10;Then fine-tune with the sliders.&#10;Only takes effect after &quot;APPLY GROOVE&quot;.",
        "Éditeur de synthèse sonore pour chaque instrument.&#10;Charger un preset = valeurs de départ pour l'instrument&#10;Affinez ensuite avec les curseurs.&#10;Effet visible seulement après &quot;APPLIQUER LE GROOVE&quot;."),
    "&#9835; TIMBRE &#8212; Klangsynthese": ("&#9835; TIMBRE &#8212; sound synthesis", "&#9835; TIMBRE &#8212; synthèse sonore"),
    "Synthesizer-Preset fuer KICK laden.&#10;(none) = eingebaute Standardsynthese.&#10;Nach Auswahl werden die Regler mit Preset-Werten befuellt.": (
        "Load synthesizer preset for KICK.&#10;(none) = built-in default synthesis.&#10;After selection the sliders are filled with the preset values.",
        "Charger un preset de synthétiseur pour KICK.&#10;(none) = synthèse standard intégrée.&#10;Après sélection, les curseurs prennent les valeurs du preset."),
    "Ziel-Frequenz des Kick-Pitchglides (Sinus-Schwanz).&#10;Tief = dunkler 808-Sub-Kick (20-45 Hz)&#10;Hoch = knackiger, melodischer Kick.": (
        "Target frequency of the kick pitch glide (sine tail).&#10;Low = dark 808 sub kick (20-45 Hz)&#10;High = crisp, melodic kick.",
        "Fréquence cible du glissement de hauteur du kick (queue sinusoïdale).&#10;Bas = kick sub 808 sombre (20-45 Hz)&#10;Haut = kick incisif et mélodique."),
    "Pitch Ende (Hz)": ("Pitch end (Hz)", "Pitch final (Hz)"),
    "Transienten-Rauschanteil des Kick-Anschlags.&#10;0 = reiner Sinus / 808-Ton&#10;Hoeher = punchigerer, knackigerer Anschlag.": (
        "Transient noise amount of the kick attack.&#10;0 = pure sine / 808 tone&#10;Higher = punchier, crisper attack.",
        "Part de bruit transitoire de l'attaque du kick.&#10;0 = sinus pur / son 808&#10;Plus haut = attaque plus percutante et incisive."),
    "Rauschanteil": ("Noise amount", "Part de bruit"),
    "Abklingzeit der Kick-Huelle.&#10;50 ms = kurz, trocken, punchig&#10;280 ms = ausgewogen&#10;800 ms = langer Sub-Schwanz (808-Style)": (
        "Decay time of the kick envelope.&#10;50 ms = short, dry, punchy&#10;280 ms = balanced&#10;800 ms = long sub tail (808 style)",
        "Temps de déclin de l'enveloppe du kick.&#10;50 ms = court, sec, percutant&#10;280 ms = équilibré&#10;800 ms = longue queue de sub (style 808)"),
    "Ausklingen (ms)": ("Decay (ms)", "Déclin (ms)"),
    "Synthesizer-Preset fuer SNARE laden.&#10;(none) = eingebaute Standardsynthese.": (
        "Load synthesizer preset for SNARE.&#10;(none) = built-in default synthesis.",
        "Charger un preset de synthétiseur pour SNARE.&#10;(none) = synthèse standard intégrée."),
    "Koerper-Pitch der Snare.&#10;80 Hz = tiefer, dumpfer Tom-Charakter&#10;140 Hz = klassische Snare&#10;400 Hz = heller, duenner Klang": (
        "Body pitch of the snare.&#10;80 Hz = deep, dull tom character&#10;140 Hz = classic snare&#10;400 Hz = bright, thin sound",
        "Hauteur du corps de la caisse claire.&#10;80 Hz = caractère de tom grave et sourd&#10;140 Hz = caisse claire classique&#10;400 Hz = son clair et fin"),
    "Verhaeltnis Rauschen zu Ton.&#10;0 = reiner Ton (klingt wie Tom)&#10;0.6 = klassische Snare-Mischung&#10;1 = nur Rauschen (Buerstensnare)": (
        "Ratio of noise to tone.&#10;0 = pure tone (sounds like a tom)&#10;0.6 = classic snare mix&#10;1 = noise only (brush snare)",
        "Rapport bruit/son.&#10;0 = son pur (sonne comme un tom)&#10;0.6 = mélange classique de caisse claire&#10;1 = bruit seul (caisse claire aux balais)"),
    "Abklingzeit der Snare-Huelle.&#10;30 ms = sehr kurz, trocken&#10;150 ms = natuerlich&#10;400 ms = langer Nachhall": (
        "Decay time of the snare envelope.&#10;30 ms = very short, dry&#10;150 ms = natural&#10;400 ms = long reverb tail",
        "Temps de déclin de l'enveloppe de la caisse claire.&#10;30 ms = très court, sec&#10;150 ms = naturel&#10;400 ms = longue résonance"),
    "Synthesizer-Preset fuer HI-HAT laden.&#10;(none) = eingebaute Standardsynthese.": (
        "Load synthesizer preset for HI-HAT.&#10;(none) = built-in default synthesis.",
        "Charger un preset de synthétiseur pour HI-HAT.&#10;(none) = synthèse standard intégrée."),
    "Abklingzeit des Hi-Hats.&#10;10-30 ms = geschlossene Hi-Hat (kurz, trocken)&#10;100-400 ms = offene Hi-Hat (laenger, zischend)": (
        "Decay time of the hi-hat.&#10;10-30 ms = closed hi-hat (short, dry)&#10;100-400 ms = open hi-hat (longer, sizzling)",
        "Temps de déclin du charleston.&#10;10-30 ms = charleston fermé (court, sec)&#10;100-400 ms = charleston ouvert (plus long, sifflant)"),
    "Hochfrequenz-Anteil des Hi-Hats.&#10;0 = dunkle, geschlossene Hi-Hat&#10;1 = helle, schneidende offene Hi-Hat": (
        "High-frequency content of the hi-hat.&#10;0 = dark, closed hi-hat&#10;1 = bright, cutting open hi-hat",
        "Part de hautes fréquences du charleston.&#10;0 = charleston fermé et sombre&#10;1 = charleston ouvert clair et tranchant"),
    "Soft-Clip-Saettigung (analoger Charakter).&#10;0 = sauber und digital&#10;1 = warme harmonische Verzerrung": (
        "Soft-clip saturation (analog character).&#10;0 = clean and digital&#10;1 = warm harmonic distortion",
        "Saturation soft-clip (caractère analogique).&#10;0 = propre et numérique&#10;1 = distorsion harmonique chaleureuse"),
    "S&#228;ttigung": ("Saturation", "Saturation"),
    "Synthesizer-Preset fuer MELODIC-Stimmen laden.&#10;(none) = eingebaute Standardsynthese.&#10;Gilt fuer Bass, Akkorde, Lead, Pad, Arp, Stabs.": (
        "Load synthesizer preset for MELODIC voices.&#10;(none) = built-in default synthesis.&#10;Applies to bass, chords, lead, pad, arp, stabs.",
        "Charger un preset de synthétiseur pour les voix MELODIC.&#10;(none) = synthèse standard intégrée.&#10;S'applique à basse, accords, lead, pad, arp, stabs."),
    "Einschwingzeit melodischer Stimmen.&#10;1 ms = Pluck / Stab (sofort da)&#10;15 ms = natuerlicher Anschlag&#10;200 ms = langsames Pad-Anschwellen": (
        "Attack time of melodic voices.&#10;1 ms = pluck / stab (instantly there)&#10;15 ms = natural attack&#10;200 ms = slow pad swell",
        "Temps d'attaque des voix mélodiques.&#10;1 ms = pluck / stab (immédiat)&#10;15 ms = attaque naturelle&#10;200 ms = montée lente de pad"),
    "Anschlag (ms)": ("Attack (ms)", "Attaque (ms)"),
    "Tiefpass-Filter-Grenzfrequenz (Helligkeit).&#10;0 = dunkel / gedaempft (Lo-Fi, Vintage)&#10;0.5 = ausgewogen&#10;1 = hell / offen (klar, strahlend)": (
        "Low-pass filter cutoff (brightness).&#10;0 = dark / muffled (lo-fi, vintage)&#10;0.5 = balanced&#10;1 = bright / open (clear, shining)",
        "Fréquence de coupure du filtre passe-bas (brillance).&#10;0 = sombre / étouffé (lo-fi, vintage)&#10;0.5 = équilibré&#10;1 = clair / ouvert (net, éclatant)"),
    "Helligkeit": ("Brightness", "Brillance"),
    "Genre fuer das Groove-Preset.&#10;Beeinflusst die verfuegbaren Feel-Presets.&#10;Wird automatisch auf das generierte Genre gesetzt.": (
        "Genre for the groove preset.&#10;Affects the available feel presets.&#10;Is set automatically to the generated genre.",
        "Genre du preset de groove.&#10;Influence les presets de feel disponibles.&#10;Réglé automatiquement sur le genre généré."),
    "Benanntes Feel-Preset: laedt einen kuratieren Groove-Charakter.&#10;z.B. Boom Bap, Lo-Fi Chill, Modern Rap (bei Hip-Hop).&#10;Leer = Genre-Standardwerte laden.": (
        "Named feel preset: loads a curated groove character.&#10;e.g. Boom Bap, Lo-Fi Chill, Modern Rap (for hip-hop).&#10;Empty = load genre defaults.",
        "Preset de feel nommé : charge un caractère de groove sélectionné.&#10;p. ex. Boom Bap, Lo-Fi Chill, Modern Rap (pour le hip-hop).&#10;Vide = charger les valeurs par défaut du genre."),
    "Laedt das ausgewaehlte Genre- oder Feel-Preset in den Mixer.&#10;Ueberschreibt die aktuellen Mixer-Einstellungen.": (
        "Loads the selected genre or feel preset into the mixer.&#10;Overwrites the current mixer settings.",
        "Charge dans le mixeur le preset de genre ou de feel sélectionné.&#10;Écrase les réglages actuels du mixeur."),
    "Preset laden": ("Load preset", "Charger le preset"),
    "Setzt alle Mixer-Spuren auf Standardwerte zurueck&#10;(Mute aus, Lautstaerke 0 dB, keine Swing/Nudge-Abweichung).": (
        "Resets all mixer tracks to their defaults&#10;(mute off, volume 0 dB, no swing/nudge offset).",
        "Réinitialise toutes les pistes du mixeur aux valeurs par défaut&#10;(mute désactivé, volume 0 dB, aucun décalage swing/nudge)."),
    "Zur&#252;cksetzen": ("Reset", "Réinitialiser"),
    "Soundfont (SF2): die Klangbibliothek fuer die MIDI-Instrumente.&#10;Genre-Standard = automatisch passendes SF2&#10;Eigene SF2 hochladen fuer individuellen Klang.": (
        "Soundfont (SF2): the sound library for the MIDI instruments.&#10;Genre default = automatically matching SF2&#10;Upload your own SF2 for an individual sound.",
        "Soundfont (SF2) : la bibliothèque de sons des instruments MIDI.&#10;Standard du genre = SF2 adapté automatiquement&#10;Importez votre propre SF2 pour un son personnalisé."),
    "Eigene SF2-Datei:": ("Your own SF2 file:", "Votre fichier SF2 :"),
    "Eigene SF2-Soundfont-Datei hochladen.&#10;Erlaubt individuelle Instrumentenklaenge jenseits der Genre-Standards.&#10;Dateigroesse: typisch 50 MB - 500 MB.": (
        "Upload your own SF2 soundfont file.&#10;Allows individual instrument sounds beyond the genre defaults.&#10;File size: typically 50 MB - 500 MB.",
        "Importer votre propre fichier soundfont SF2.&#10;Permet des sons d'instruments personnalisés au-delà des standards du genre.&#10;Taille du fichier : généralement 50 Mo - 500 Mo."),
    "&#128190; Laden": ("&#128190; Load", "&#128190; Charger"),
    "Wird hochgeladen&#8230;": ("Uploading&#8230;", "Importation en cours&#8230;"),
    "Rendert den Beat neu mit allen aktuellen Mixer-Einstellungen.&#10;Ergebnis erscheint als &quot;Groove Re-Render&quot; zum Vergleich.&#10;Dauert ca. 5-15 Sekunden.": (
        "Re-renders the beat with all current mixer settings.&#10;The result appears as &quot;Groove Re-Render&quot; for comparison.&#10;Takes about 5-15 seconds.",
        "Relance le rendu du beat avec tous les réglages actuels du mixeur.&#10;Le résultat apparaît comme &quot;Groove Re-Render&quot; pour comparaison.&#10;Prend environ 5 à 15 secondes."),
    "&#9654; GROOVE ANWENDEN &amp; NEU RENDERN": ("&#9654; APPLY GROOVE &amp; RE-RENDER", "&#9654; APPLIQUER LE GROOVE &amp; RE-RENDRE"),
    "VORSCHAU — NEU GERENDERT": ("PREVIEW — RE-RENDERED", "APERÇU — RE-RENDU"),
    "Der Production Advisor wird nach der Generierung befullt.": (
        "The Production Advisor is filled after generation.", "Le Production Advisor est rempli après la génération."),
    "AUDIO EXPORTIEREN": ("EXPORT AUDIO", "EXPORTER L'AUDIO"),
    "Schliessen": ("Close", "Fermer"),
    "&#9888; Formate mit * erfordern <strong>ffmpeg</strong> im System-PATH.": (
        "&#9888; Formats marked with * require <strong>ffmpeg</strong> in the system PATH.",
        "&#9888; Les formats marqués d'un * nécessitent <strong>ffmpeg</strong> dans le PATH système."),
    "QUELLE": ("SOURCE", "SOURCE"),
    "Neu gerendert": ("Re-rendered", "Re-rendu"),
    "&#8659; AUDIO HERUNTERLADEN": ("&#8659; DOWNLOAD AUDIO", "&#8659; TÉLÉCHARGER L'AUDIO"),
    "WEITERE EXPORTE": ("MORE EXPORTS", "AUTRES EXPORTS"),
    "&#8659; Komposition (.json)": ("&#8659; Composition (.json)", "&#8659; Composition (.json)"),
    "&#8659; Berater (.pdf)": ("&#8659; Advisor (.pdf)", "&#8659; Conseiller (.pdf)"),
    "MIDI und JSON exportieren die aktive Version (Re-Render wenn ausgewaehlt, sonst Original).": (
        "MIDI and JSON export the active version (re-render if selected, otherwise the original).",
        "MIDI et JSON exportent la version active (re-rendu si sélectionné, sinon l'original)."),
}

# ---------------------------------------------------------------------------
# JavaScript-Texte (werden in base.html als I18N an den Browser uebergeben)
# ---------------------------------------------------------------------------
_JS = {
    "? Hilfe AN": ("? Help ON", "? Aide ON"),
    "? Hilfe AUS": ("? Help OFF", "? Aide OFF"),
    "Tooltips ausschalten": ("Turn tooltips off", "Désactiver les infobulles"),
    "Tooltips einschalten": ("Turn tooltips on", "Activer les infobulles"),
    "Keine Parameter erkannt.": ("No parameters detected.", "Aucun paramètre détecté."),
    "Generierung fehlgeschlagen.": ("Generation failed.", "Échec de la génération."),
    "Netzwerkfehler: ": ("Network error: ", "Erreur réseau : "),
    "⚠ Netzwerkfehler: ": ("⚠ Network error: ", "⚠ Erreur réseau : "),
    "Zuerst einen Beat generieren.": ("Generate a beat first.", "Générez d'abord un beat."),
    "Solo-Fehler: ": ("Solo error: ", "Erreur solo : "),
    "Wird gerendert…": ("Rendering…", "Rendu en cours…"),
    "Re-Render-Fehler: ": ("Re-render error: ", "Erreur de re-rendu : "),
    "▶ GROOVE ANWENDEN & NEU RENDERN": ("▶ APPLY GROOVE & RE-RENDER", "▶ APPLIQUER LE GROOVE & RE-RENDRE"),
    "Upload fehlgeschlagen: ": ("Upload failed: ", "Échec de l'importation : "),
    "Upload fehlgeschlagen.": ("Upload failed.", "Échec de l'importation."),
    "Upload-Fehler: ": ("Upload error: ", "Erreur d'importation : "),
    "Kein Sample-File im Speicher. Bitte Seite nicht neu laden.": (
        "No sample file in memory. Please do not reload the page.",
        "Aucun fichier sample en mémoire. Veuillez ne pas recharger la page."),
    "Vorschau fehlgeschlagen: ": ("Preview failed: ", "Échec de l'aperçu : "),
    "Zuerst neu rendern.": ("Re-render first.", "Relancez d'abord le rendu."),
    "Kein Beat vorhanden.": ("No beat available.", "Aucun beat disponible."),
    "⚠ ffmpeg nicht gefunden. Bitte ffmpeg installieren oder WAV CD Quality waehlen.": (
        "⚠ ffmpeg not found. Please install ffmpeg or choose WAV CD Quality.",
        "⚠ ffmpeg introuvable. Veuillez installer ffmpeg ou choisir WAV CD Quality."),
    "Wird konvertiert…": ("Converting…", "Conversion en cours…"),
    "Fehler beim Exportieren.": ("Error while exporting.", "Erreur lors de l'export."),
    "⬇ AUDIO HERUNTERLADEN": ("⬇ DOWNLOAD AUDIO", "⬇ TÉLÉCHARGER L'AUDIO"),
    "Tokens kaufen →": ("Buy tokens →", "Acheter des jetons →"),
    "(dein Beat bleibt erhalten)": ("(your beat will be kept)", "(votre beat est conservé)"),
    "MIDI-Export fehlgeschlagen.": ("MIDI export failed.", "Échec de l'export MIDI."),
    "JSON-Export fehlgeschlagen.": ("JSON export failed.", "Échec de l'export JSON."),
    "PDF-Export fehlgeschlagen.": ("PDF export failed.", "Échec de l'export PDF."),
    " — Groove-Parameter": (" — groove parameters", " — paramètres de groove"),
    "PERKUSSION": ("PERCUSSION", "PERCUSSION"),
    "AKKORDE": ("CHORDS", "ACCORDS"),
    "TEXTUR": ("TEXTURE", "TEXTURE"),
    "Takte: ": ("Bars: ", "Mesures : "),
    "Takte": ("Bars", "Mesures"),
    "Tonart": ("Key", "Tonalité"),
    "PLR-Ziel": ("PLR target", "Cible PLR"),
    "LRA-Ziel": ("LRA target", "Cible LRA"),
    "Tonleitern": ("Scales", "Gammes"),
    "Prompt erkannt": ("Prompt detected", "Prompt détecté"),
    " (FluidSynth nicht gefunden)": (" (FluidSynth not found)", " (FluidSynth introuvable)"),
    "Server-Fehler": ("Server error", "Erreur serveur"),
    "&#9654; Beat generieren": ("&#9654; Generate beat", "&#9654; Générer le beat"),
    "— Palette waehlen —": ("— choose palette —", "— choisir une palette —"),
    "Keine Paletten fuer dieses Genre": ("No palettes for this genre", "Aucune palette pour ce genre"),
    "— Genre-Standard (SF2) —": ("— Genre default (SF2) —", "— Standard du genre (SF2) —"),
    "⚠ Format-Liste konnte nicht geladen werden (HTTP {status}). Bitte neu einloggen.": (
        "⚠ Format list could not be loaded (HTTP {status}). Please sign in again.",
        "⚠ La liste des formats n'a pas pu être chargée (HTTP {status}). Veuillez vous reconnecter."),
    "⚠ Format-Liste Fehler: {msg}": ("⚠ Format list error: {msg}", "⚠ Erreur de la liste des formats : {msg}"),
    "Format {ext} nicht unterstuetzt.": ("Format {ext} not supported.", "Format {ext} non pris en charge."),
    "Erlaubt: {allowed}": ("Allowed: {allowed}", "Autorisés : {allowed}"),
    "{label} Solo rendern und abhoeren.&#10;Zeigt nur diese Spur isoliert.": (
        "Render and listen to {label} solo.&#10;Shows only this track in isolation.",
        "Rendre et écouter {label} en solo.&#10;N'affiche que cette piste isolée."),
    "Lautstaerke von {label}.&#10;-24 dB = sehr leise · 0 dB = Standard · +6 dB = lauter": (
        "Volume of {label}.&#10;-24 dB = very quiet · 0 dB = default · +6 dB = louder",
        "Volume de {label}.&#10;-24 dB = très faible · 0 dB = standard · +6 dB = plus fort"),
    "{label} stummschalten (Mute).&#10;Stumme Spuren werden nicht in den Mix gerendert.": (
        "Mute {label}.&#10;Muted tracks are not rendered into the mix.",
        "Couper {label} (mute).&#10;Les pistes coupées ne sont pas rendues dans le mix."),
    "{label} solo schalten.&#10;Alle anderen Spuren werden gedaempft.": (
        "Solo {label}.&#10;All other tracks are muted.",
        "Mettre {label} en solo.&#10;Toutes les autres pistes sont atténuées."),
    "Lautstaerke (Gain) von {label} in Dezibel.&#10;-24 dB = sehr leise · 0 dB = Standard · +6 dB = lauter": (
        "Volume (gain) of {label} in decibels.&#10;-24 dB = very quiet · 0 dB = default · +6 dB = louder",
        "Volume (gain) de {label} en décibels.&#10;-24 dB = très faible · 0 dB = standard · +6 dB = plus fort"),
    "Stereo-Pan von {label}.&#10;L = links · C = Mitte · R = rechts": (
        "Stereo pan of {label}.&#10;L = left · C = center · R = right",
        "Panoramique stéréo de {label}.&#10;L = gauche · C = centre · R = droite"),
    "{label} stummschalten. Stumme Spuren fehlen im Re-Render.": (
        "Mute {label}. Muted tracks are missing from the re-render.",
        "Couper {label}. Les pistes coupées sont absentes du re-rendu."),
    "{label} solo schalten. Alle anderen werden gedaempft.": (
        "Solo {label}. All others are muted.", "Mettre {label} en solo. Toutes les autres sont atténuées."),
    "Audio-Datei fuer {label} auswaehlen.&#10;Unterstuetzte Formate: WAV, AIFF, FLAC, OGG, MP3&#10;Maximale Dateigroesse: 20 MB.": (
        "Choose an audio file for {label}.&#10;Supported formats: WAV, AIFF, FLAC, OGG, MP3&#10;Maximum file size: 20 MB.",
        "Choisir un fichier audio pour {label}.&#10;Formats pris en charge : WAV, AIFF, FLAC, OGG, MP3&#10;Taille maximale : 20 Mo."),
    "Zugewiesenes Sample vorabhoeren.&#10;Nur verfuegbar wenn eine Datei zugewiesen ist.": (
        "Preview the assigned sample.&#10;Only available when a file is assigned.",
        "Pré-écouter le sample attribué.&#10;Disponible uniquement si un fichier est attribué."),
    "Sample-Zuweisung fuer {label} entfernen.&#10;Die Spur verwendet wieder den eingebauten Synthesizer.": (
        "Remove the sample assignment for {label}.&#10;The track uses the built-in synthesizer again.",
        "Retirer le sample attribué à {label}.&#10;La piste réutilise le synthétiseur intégré."),
}

TRANSLATIONS = {
    "en": {de: tr[0] for de, tr in _T.items()},
    "fr": {de: tr[1] for de, tr in _T.items()},
}
JS = {
    "en": {de: tr[0] for de, tr in _JS.items()},
    "fr": {de: tr[1] for de, tr in _JS.items()},
}
