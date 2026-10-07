# Weekly Deals – Website (Entwurf v1)

Statische, mobile-first Seite (HTML/CSS/JS, keine externen Skripte, Systemschriften).

- Firmendaten: `_build/build.py` → `CONFIG`, dann `python3 _build/build.py`
- Alle `[Platzhalter]` ersetzen (Firma, Adresse, UID, Telefon, Texte, Team, Bewertungen, Deals)
- Formular: `FORMULAR_ACTION` auf echten Dienst setzen (z. B. Formspree)
- Statistik: erst nach Opt-in, Einbindung in `js/main.js` → `loadAnalytics()`
- Datenschutz, AGB, Impressum: Vorlagen, von Jurist/in prüfen lassen
- Kontakt (Telefon, E-Mail) und Logo/Farben sind eingetragen. Firma, Adresse, UID und Domain fehlen noch (Impressum, Datenschutz, AGB, canonical, Sitemap) – vor Livegang ergänzen. Ohne Domain wird keine `sitemap.xml` erzeugt.
- Vor Livegang: Domain in CONFIG, Google Business Profile (NAP identisch), Search Console, Bilder als WebP
