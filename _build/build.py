#!/usr/bin/env python3
# Erzeugt die statische Seite. Aufruf: python3 _build/build.py
# Alle Firmendaten stehen im CONFIG-Block – dort ersetzen, dann neu bauen.
import os, html

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

CONFIG = {
    "NAME": "Weekly Deals",
    "FIRMA": "[Firmenname GmbH/Einzelfirma]",
    "RECHTSFORM": "[Rechtsform]",
    "STRASSE": "[Strasse Nr.]",
    "PLZ_ORT": "[PLZ Ort]",
    "ORT": "Schweiz",                      # für SEO-Texte, z. B. "Schwyz"
    "TEL": "+41 00 000 00 00",
    "TEL_RAW": "+41000000000",
    "WA_RAW": "41000000000",
    "EMAIL": "info@weekly-deals.example",
    "UID": "CHE-000.000.000",
    "MWST": "CHE-000.000.000 MWST",
    "DOMAIN": "https://www.weekly-deals.example",
    "LAT": "47.0", "LON": "8.0",
    "FORMULAR_ACTION": "https://formspree.io/f/PLATZHALTER",
}
C = CONFIG

# Beispiel-Deals (Platzhalter – echte Ware, echte Preise, echte Fotos eintragen)
DEALS = [
    ("elektronik", "g1", "Kabellose Kopfhörer, Noise-Cancelling", 89, 199, 5, "Neuware, OVP"),
    ("elektronik", "g1", "Smartwatch Fitness-Tracker", 59, 149, 8, "Neuware, OVP"),
    ("sneaker-mode", "g2", "Laufschuhe Herren, Gr. 42–45", 74, 159, 12, "Neuware, Restposten"),
    ("sneaker-mode", "g2", "Daunenjacke Damen, alle Grössen", 99, 249, 6, "Neuware mit Etikett"),
    ("haushalt-garten", "g3", "Kaffeevollautomat, B-Ware", 249, 599, 3, "Retoure, geprüft"),
    ("haushalt-garten", "g3", "Akku-Gartenset 3-teilig", 129, 289, 7, "Neuware, OVP"),
]
CATS = {
    "elektronik": ("Elektronik-Deals", "Kopfhörer, Smartwatches, Haushaltselektronik und mehr – jede Woche neu und bis zu 60 % günstiger als der Listenpreis.", "Elektronik"),
    "sneaker-mode": ("Sneaker & Mode-Deals", "Marken-Sneaker, Jacken und Kleidung als Restposten und Überbestände – solange Vorrat reicht.", "Sneaker & Mode"),
    "haushalt-garten": ("Haushalt & Garten-Deals", "Küchengeräte, Werkzeug und Gartenartikel zum Schnäppchenpreis – Neuware und geprüfte B-Ware.", "Haushalt & Garten"),
}
NAV = [("wochendeals/", "Wochendeals"), ("angebot/", "Angebot"), ("ueber-uns/", "Über uns"),
       ("bewertungen/", "Bewertungen"), ("faq/", "FAQ"), ("kontakt/", "Kontakt")]
PAGES = []  # (path, priority) für Sitemap

def deal_card(d, root, example=True):
    cat, g, title, price, old, stock, cond = d
    pct = round((1 - price / old) * 100)
    ex = '<span class="tag">Beispiel</span> ' if example else ""
    return f'''<article class="card deal" data-cat="{cat}">
  <div class="deal-img {g}" role="img" aria-label="Platzhalter für Produktfoto: {html.escape(title)}"><span class="badge">–{pct}%</span><span>Echtes Foto folgt</span><span class="stock">Nur noch {stock} Stk.</span></div>
  <div class="deal-body">{ex}<h3>{html.escape(title)}</h3>
    <div class="price"><b>CHF {price}.–</b><s>CHF {old}.–</s></div>
    <p class="small">inkl. MwSt. · {cond} · gültig bis Sonntag</p>
    <a class="btn btn-primary btn-block" href="{root}kontakt/?deal={html.escape(title)}">Deal sichern</a></div></article>'''

def layout(path, title, desc, body, depth, current=None, hero_class=None, noindex=False):
    root = "../" * depth
    nav = "".join(f'<a href="{root}{h}"' + (' aria-current="page"' if current == h else "") + f'>{t}</a>' for h, t in NAV)
    canon = f'{C["DOMAIN"]}/{path}'.replace("/index.html", "/")
    schema = f'''{{"@context":"https://schema.org","@type":"Store","name":"{C["NAME"]}","url":"{C["DOMAIN"]}/","telephone":"{C["TEL_RAW"]}","email":"{C["EMAIL"]}","address":{{"@type":"PostalAddress","streetAddress":"{C["STRASSE"]}","addressLocality":"{C["PLZ_ORT"]}","addressCountry":"CH"}},"priceRange":"CHF","openingHoursSpecification":[{{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"09:00","closes":"18:00"}},{{"@type":"OpeningHoursSpecification","dayOfWeek":"Saturday","opens":"09:00","closes":"16:00"}}]}}'''
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    page = f'''<!doctype html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
{robots}
<meta name="theme-color" content="#0b1226">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website"><meta property="og:locale" content="de_CH">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23c62d14'/%3E%3Ctext x='32' y='44' font-size='34' font-family='Arial' font-weight='900' text-anchor='middle' fill='white'%3EW%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="{root}css/style.css">
<script type="application/ld+json">{schema}</script>
</head>
<body>
<a class="skip" href="#main">Zum Inhalt springen</a>
<div class="topstrip">Neue Deals jeden <strong>Montag</strong> · Aktion endet <strong>Sonntag 23:59</strong></div>
<header class="site-header"><div class="wrap bar">
  <a class="logo" href="{root}" aria-label="{C["NAME"]} – Startseite"><i>W</i>{C["NAME"]}</a>
  <a class="btn btn-primary call-btn" href="tel:{C["TEL_RAW"]}" aria-label="Anrufen {C["TEL"]}">📞 Anrufen</a>
  <button class="burger" aria-label="Menü" aria-expanded="false" aria-controls="nav">☰</button>
  <nav id="nav" class="nav" aria-label="Hauptnavigation">{nav}</nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="site-footer"><div class="wrap">
  <div class="fgrid">
    <div><h3>{C["NAME"]}</h3><p>Jede Woche von Montag bis Sonntag neue Top-Deals und Rabatte.<br>{C["FIRMA"]}<br>{C["STRASSE"]}, {C["PLZ_ORT"]}<br><a href="tel:{C["TEL_RAW"]}">{C["TEL"]}</a><br><a href="mailto:{C["EMAIL"]}">{C["EMAIL"]}</a></p></div>
    <div><h3>Angebot</h3><ul><li><a href="{root}wochendeals/">Wochendeals</a></li><li><a href="{root}angebot/elektronik/">Elektronik</a></li><li><a href="{root}angebot/sneaker-mode/">Sneaker &amp; Mode</a></li><li><a href="{root}angebot/haushalt-garten/">Haushalt &amp; Garten</a></li></ul></div>
    <div><h3>Firma</h3><ul><li><a href="{root}ueber-uns/">Über uns</a></li><li><a href="{root}bewertungen/">Bewertungen</a></li><li><a href="{root}faq/">FAQ</a></li><li><a href="{root}kontakt/">Kontakt</a></li></ul></div>
    <div><h3>Rechtliches</h3><ul><li><a href="{root}impressum/">Impressum</a></li><li><a href="{root}datenschutz/">Datenschutz</a></li><li><a href="{root}agb/">AGB</a></li><li><a href="#" id="consent-open">Cookie-Einstellungen</a></li></ul></div>
  </div>
  <p class="small" style="color:#94a3b8">Alle Preise in CHF inkl. MwSt. © <span id="year">2026</span> {C["NAME"]}</p>
</div></footer>
<div class="mbar" aria-label="Schnellkontakt">
  <a class="btn btn-dark" href="tel:{C["TEL_RAW"]}">📞 Anrufen</a>
  <a class="btn btn-light" href="https://wa.me/{C["WA_RAW"]}">💬 WhatsApp</a>
  <a class="btn btn-primary" href="{root}wochendeals/">🔥 Deals</a>
</div>
<div id="consent" class="consent" role="dialog" aria-labelledby="ctitle" aria-live="polite">
  <h3 id="ctitle">Deine Privatsphäre</h3>
  <p class="small">Wir nutzen nur notwendige Technik. Mit deiner Zustimmung messen wir zusätzlich anonymisiert, ob Anrufe und Anfragen ankommen (Statistik). Details in der <a href="{root}datenschutz/">Datenschutzerklärung</a>.</p>
  <div class="btn-row"><button class="btn btn-primary" data-consent="all">Alle akzeptieren</button><button class="btn btn-light" data-consent="necessary">Nur notwendige</button></div>
</div>
<script src="{root}js/main.js" defer></script>
</body>
</html>'''
    out = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    if not noindex:
        PAGES.append(path)

def phero(root, crumbs, h1, lead):
    return f'<section class="page-hero"><div class="wrap"><div class="crumbs"><a href="{root}">Start</a> › {crumbs}</div><h1>{h1}</h1><p class="lead">{lead}</p></div></section>'

def cta(root, text="Keine Deal-Woche verpassen"):
    return f'''<section class="cta-band"><div class="wrap"><h2>{text}</h2><p>Schreib uns auf WhatsApp oder ruf an – wir reservieren deinen Deal.</p>
<div class="btn-row" style="justify-content:center"><a class="btn btn-light" href="tel:{C["TEL_RAW"]}">📞 {C["TEL"]}</a><a class="btn btn-light" href="https://wa.me/{C["WA_RAW"]}">💬 WhatsApp</a></div></div></section>'''

def legal(root, h1, inner):
    return f'''<section class="page-hero"><div class="wrap"><div class="crumbs"><a href="{root}">Start</a> › {h1}</div><h1>{h1}</h1></div></section>
<section class="section"><div class="wrap legal"><p class="draft-note"><b>Entwurf/Vorlage:</b> Platzhalter in [eckigen Klammern] ausfüllen und Text vor Veröffentlichung von einer Juristin / einem Juristen prüfen lassen.</p>{inner}</div></section>'''

# ---------- Startseite ----------
top3 = "".join(deal_card(d, "", True) for d in (DEALS[0], DEALS[2], DEALS[4]))
home = f'''
<section class="hero"><div class="wrap">
  <span class="eyebrow" style="color:var(--accent)">Neue Deals · jede Woche · Mo–So</span>
  <h1>Krasse Deals. <em>Jede Woche neu.</em> Bis zu 60&nbsp;% Rabatt.</h1>
  <p class="lead">Elektronik, Sneaker, Mode und Haushalt aus Restposten und Überbeständen – geprüft, mit Schweizer Preisen inkl. MwSt. Nur bis Sonntag, solange Vorrat reicht.</p>
  <div id="countdown" class="countdown" role="timer" aria-label="Zeit bis Aktionsende">
    <div><b>00</b><span>Tage</span></div><div><b>00</b><span>Std</span></div><div><b>00</b><span>Min</span></div><div><b>00</b><span>Sek</span></div></div>
  <div class="btn-row"><a class="btn btn-primary" href="wochendeals/">🔥 Deals der Woche ansehen</a><a class="btn btn-light" href="tel:{C["TEL_RAW"]}">📞 Jetzt anrufen</a></div>
  <div class="trust"><div>✔ Geprüfte Ware</div><div>✔ Preise inkl. MwSt.</div><div>✔ Versand aus der Schweiz</div><div>✔ Persönlicher Kontakt</div></div>
</div></section>
<section class="section"><div class="wrap">
  <span class="eyebrow">Diese Woche</span><h2>Die Top-Deals der Woche</h2>
  <div class="grid c3">{top3}</div>
  <p style="margin-top:20px"><a class="btn btn-dark" href="wochendeals/">Alle Wochendeals →</a></p>
</div></section>
<section class="section soft"><div class="wrap">
  <h2>So einfach geht's</h2>
  <ol class="steps"><li><h3>Deal aussuchen</h3><p>Jeden Montag neue Angebote – nur bis Sonntag.</p></li><li><h3>Anrufen oder schreiben</h3><p>Per Telefon, WhatsApp oder Formular. Wir reservieren dir die Ware.</p></li><li><h3>Abholen oder Versand</h3><p>Du holst ab oder wir schicken dir die Ware per Post.</p></li></ol>
</div></section>
<section class="section"><div class="wrap">
  <h2>Unser Angebot</h2>
  <div class="grid c3">
  {"".join(f'<a class="card" style="text-decoration:none;color:inherit" href="angebot/{k}/"><h3>{v[0]}</h3><p class="small">{v[1]}</p><b style="color:var(--brand)">Mehr erfahren →</b></a>' for k, v in CATS.items())}
  </div>
</div></section>
<section class="section soft"><div class="wrap">
  <h2>Warum {C["NAME"]}?</h2>
  <div class="grid c2">
    <div class="card"><h3>Echte Rabatte</h3><p>Wir kaufen Restposten und Überbestände günstig ein und geben den Vorteil weiter.</p></div>
    <div class="card"><h3>Klare Preise</h3><p>Alle Preise in CHF, inkl. MwSt. Keine versteckten Kosten.</p></div>
    <div class="card"><h3>Schnell &amp; persönlich</h3><p>Ein Anruf genügt. Wir antworten in der Regel am selben Werktag.</p></div>
    <div class="card"><h3>Jede Woche neu</h3><p>Neue Deals von Montag bis Sonntag – lohnt sich, regelmässig vorbeizuschauen.</p></div>
  </div>
  <p style="margin-top:20px"><a href="bewertungen/">Das sagen unsere Kunden →</a></p>
</div></section>
<section class="section"><div class="wrap" style="max-width:640px">
  <h2>Deal-Alarm jeden Montag</h2>
  <p>Wir schicken dir die neuen Deals per E-Mail. Abmeldung jederzeit mit einem Klick.</p>
  <form data-form data-thanks="danke/" action="{C["FORMULAR_ACTION"]}" method="post">
    <div class="hp" aria-hidden="true"><label>Nicht ausfüllen<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
    <input type="hidden" name="form" value="newsletter">
    <div><label for="nl-mail">E-Mail</label><input id="nl-mail" type="email" name="email" required autocomplete="email"></div>
    <label class="check"><input type="checkbox" required name="consent"><span>Ich möchte den wöchentlichen Deal-Alarm erhalten und habe die <a href="datenschutz/">Datenschutzerklärung</a> gelesen.</span></label>
    <button class="btn btn-primary" type="submit">Deal-Alarm bestellen</button>
  </form>
</div></section>
{cta("")}
'''
layout("index.html", f'Weekly Deals {C["ORT"]} – Krasse Wochendeals bis 60 % Rabatt', f'Jede Woche neue Deals von Montag bis Sonntag: Elektronik, Sneaker, Mode & Haushalt bis 60 % günstiger. Jetzt anrufen oder Deal sichern – {C["ORT"]}.', home, 0)

# ---------- Wochendeals ----------
chips = '<button class="chip" data-filter="alle" aria-pressed="true">Alle</button>' + "".join(f'<button class="chip" data-filter="{k}" aria-pressed="false">{v[2]}</button>' for k, v in CATS.items())
wd = phero("../", "Wochendeals", f'Wochendeals {C["ORT"]}: Bis Sonntag 23:59', 'Neue Angebote jeden Montag. Weg ist weg – einmal ausverkauft, gibt es die Ware nicht nachgeliefert.') + f'''
<section class="section"><div class="wrap">
<div id="countdown" class="countdown" role="timer" aria-label="Zeit bis Aktionsende" style="--x:0"><div><b>00</b><span>Tage</span></div><div><b>00</b><span>Std</span></div><div><b>00</b><span>Min</span></div><div><b>00</b><span>Sek</span></div></div>
<div class="chips" role="group" aria-label="Kategorie filtern">{chips}</div>
<div class="grid c3">{"".join(deal_card(d, "../") for d in DEALS)}</div>
<p class="small" style="margin-top:16px">Beispieldaten. Durchgestrichener Preis = bisheriger Verkaufspreis bzw. Listenpreis des Herstellers (vor Veröffentlichung pro Artikel belegen).</p>
</div></section>''' + cta("../")
layout("wochendeals/index.html", f'Wochendeals {C["ORT"]} – Aktuelle Angebote bis Sonntag | Weekly Deals', 'Alle Deals der Woche im Überblick: Elektronik, Sneaker, Mode, Haushalt. Neue Angebote jeden Montag, gültig bis Sonntag.', wd, 1, "wochendeals/")

# ---------- Angebot ----------
ov = phero("../", "Angebot", "Unser Angebot", f'Drei Kategorien, jede Woche neue Deals – für Kundschaft in {C["ORT"]} und per Post in die ganze Schweiz.') + f'''
<section class="section"><div class="wrap"><div class="grid c3">
{"".join(f'<a class="card" style="text-decoration:none;color:inherit" href="{k}/"><h2 style="font-size:1.4rem">{v[0]}</h2><p>{v[1]}</p><b style="color:var(--brand)">Zu den Deals →</b></a>' for k, v in CATS.items())}
</div></div></section>''' + cta("../")
layout("angebot/index.html", f'Angebot {C["ORT"]} – Elektronik, Mode, Haushalt günstig | Weekly Deals', 'Unser Angebot: Elektronik, Sneaker & Mode sowie Haushalt & Garten als wöchentliche Deals mit hohen Rabatten.', ov, 1, "angebot/")

for k, (h1, text, short) in CATS.items():
    ds = [d for d in DEALS if d[0] == k]
    body = phero("../../", f'<a href="../">Angebot</a> › {short}', f'{h1} {C["ORT"]}', text) + f'''
<section class="section"><div class="wrap"><div class="grid c3">{"".join(deal_card(d, "../../") for d in ds)}</div>
<h2 style="margin-top:36px">Warum {short} bei Weekly Deals?</h2>
<ul><li>Jede Woche neue {short}-Deals, Montag bis Sonntag</li><li>Preise in CHF inkl. MwSt., Zustand klar angegeben (Neuware, B-Ware)</li><li>Abholung in {C["ORT"]} oder Versand per Post</li></ul>
<p><a class="btn btn-dark" href="../../wochendeals/">Alle Wochendeals</a></p></div></section>''' + cta("../../")
    layout(f"angebot/{k}/index.html", f'{h1} {C["ORT"]} – bis 60 % Rabatt | Weekly Deals', f'{short} günstig kaufen in {C["ORT"]}: {text[:110]}', body, 2, "angebot/")

# ---------- Über uns ----------
team = "".join(f'<div class="card"><div class="avatar" aria-hidden="true">Foto</div><h3>[Name {i}]</h3><p class="small">[Rolle] – [ein Satz über die Person]</p></div>' for i in (1, 2, 3))
about = phero("../", "Über uns", "Über uns: Wer hinter den Deals steht", f'Ein kleines Team aus {C["ORT"]}, das Marken-Ware zu fairen Preisen weitergibt.') + f'''
<section class="section"><div class="wrap" style="max-width:760px">
<h2>Unsere Geschichte</h2>
<p>[Platzhalter: Wie ist {C["NAME"]} entstanden? Wer seid ihr? Warum Reselling? 3–4 Sätze, persönlich und konkret.]</p>
<h2>So arbeiten wir</h2>
<ul><li>Wir kaufen Restposten und Überbestände ein.</li><li>Jeder Artikel wird geprüft und mit dem echten Zustand beschrieben.</li><li>Ein Ansprechpartner von der Anfrage bis zur Übergabe.</li></ul>
</div></section>
<section class="section soft"><div class="wrap"><h2>Das Team</h2><div class="grid c3">{team}</div>
<p class="small" style="margin-top:12px">Echte Fotos verwenden – Einwilligung der abgebildeten Personen einholen.</p></div></section>''' + cta("../")
layout("ueber-uns/index.html", f'Über uns – Das Team von Weekly Deals {C["ORT"]}', f'Lerne das Team hinter Weekly Deals kennen: persönlich, ehrlich, aus {C["ORT"]}.', about, 1, "ueber-uns/")

# ---------- Bewertungen ----------
rev = "".join(f'<div class="card quote"><div class="stars" aria-label="5 von 5 Sternen">★★★★★</div><p>„[Platzhalter – echte Kundenstimme hier einfügen]“</p><p class="small"><b>[Vorname N.], [Ort]</b> · <span class="tag">Beispiel</span></p></div>' for _ in range(3))
rv = phero("../", "Bewertungen", "Bewertungen &amp; Referenzen", 'Was Kundinnen und Kunden über uns sagen.') + f'''
<section class="section"><div class="wrap"><div class="grid c3">{rev}</div>
<p class="small" style="margin-top:14px">Nur echte, belegbare Bewertungen veröffentlichen (z. B. aus Google Business Profile, mit Einverständnis). Keine erfundenen Zitate.</p></div></section>''' + cta("../", "Überzeuge dich selbst")
layout("bewertungen/index.html", f'Bewertungen – Kundenstimmen zu Weekly Deals {C["ORT"]}', 'Echte Kundenbewertungen und Referenzen zu Weekly Deals: Das sagen unsere Kunden.', rv, 1, "bewertungen/")

# ---------- FAQ ----------
faqs = [
 ("Wie oft gibt es neue Deals?", "Jede Woche neu: Start am Montag, Ende am Sonntag um 23:59 Uhr."),
 ("Sind die Preise inklusive MwSt.?", "Ja. Alle Preise sind Endpreise in CHF inkl. Mehrwertsteuer."),
 ("Ist die Ware neu?", "Je nach Artikel Neuware, Restposten oder geprüfte B-Ware. Der Zustand steht bei jedem Deal."),
 ("Kann ich einen Deal reservieren?", "Ja, per Telefon, WhatsApp oder Formular. Wir bestätigen dir die Reservation."),
 ("Wie läuft Abholung und Versand?", "[Abholung nach Terminvereinbarung / Versand per Post – Kosten und Lieferfrist hier eintragen.]"),
 ("Kann ich etwas zurückgeben?", "[Rückgaberegelung hier eintragen – siehe AGB.]"),
]
fq = phero("../", "FAQ", "Häufige Fragen", 'Kurze Antworten zu Deals, Preisen, Abholung und Versand.') + '<section class="section"><div class="wrap" style="max-width:760px">' + "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs) + '</div></section>' + cta("../", "Frage nicht dabei?")
fq = fq.replace("</main>", "")
schema_faq = '<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[' + ",".join('{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}' % (q, a) for q, a in faqs) + ']}</script>'
layout("faq/index.html", f'FAQ – Häufige Fragen zu Weekly Deals {C["ORT"]}', 'Antworten zu Wochendeals, Preisen inkl. MwSt., Abholung, Versand und Rückgabe.', fq + schema_faq, 1, "faq/")

# ---------- Kontakt ----------
kt = phero("../", "Kontakt", f'Kontakt &amp; Anfahrt {C["ORT"]}', 'Anrufen ist am schnellsten. Oder schick uns eine Nachricht.') + f'''
<section class="section"><div class="wrap grid c2">
<div>
  <h2>So erreichst du uns</h2>
  <div class="btn-row"><a class="btn btn-primary" href="tel:{C["TEL_RAW"]}">📞 {C["TEL"]}</a><a class="btn btn-light" href="https://wa.me/{C["WA_RAW"]}">💬 WhatsApp</a></div>
  <p style="margin-top:16px"><b>{C["FIRMA"]}</b><br>{C["STRASSE"]}<br>{C["PLZ_ORT"]}<br><a href="mailto:{C["EMAIL"]}">{C["EMAIL"]}</a></p>
  <h3>Öffnungszeiten <span class="tag">Platzhalter</span></h3>
  <table><tr><th>Mo–Fr</th><td>09:00–18:00</td></tr><tr><th>Sa</th><td>09:00–16:00</td></tr><tr><th>So</th><td>Geschlossen (Deals laufen online bis 23:59)</td></tr></table>
  <div class="map-box" style="margin-top:16px" data-src="https://www.openstreetmap.org/export/embed.html?bbox={float(C["LON"])-0.01}%2C{float(C["LAT"])-0.007}%2C{float(C["LON"])+0.01}%2C{float(C["LAT"])+0.007}&amp;layer=mapnik&amp;marker={C["LAT"]}%2C{C["LON"]}">
    <div><p>Die Karte wird erst nach Klick geladen (OpenStreetMap). Dabei wird deine IP-Adresse an den Kartenanbieter übermittelt.</p><button id="map-load" class="btn btn-dark" type="button">Karte laden</button></div></div>
</div>
<div class="card">
  <h2>Nachricht senden</h2>
  <form data-form data-thanks="../danke/" action="{C["FORMULAR_ACTION"]}" method="post">
    <div class="hp" aria-hidden="true"><label>Nicht ausfüllen<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
    <input type="hidden" name="form" value="kontakt">
    <div><label for="f-name">Name</label><input id="f-name" type="text" name="name" required autocomplete="name"></div>
    <div><label for="f-mail">E-Mail</label><input id="f-mail" type="email" name="email" required autocomplete="email"></div>
    <div><label for="f-tel">Telefon (optional)</label><input id="f-tel" type="tel" name="tel" autocomplete="tel"></div>
    <div><label for="f-msg">Nachricht / gewünschter Deal</label><textarea id="f-msg" name="message" required></textarea></div>
    <label class="check"><input type="checkbox" required name="privacy"><span>Ich habe die <a href="../datenschutz/">Datenschutzerklärung</a> gelesen und bin mit der Bearbeitung meiner Angaben zur Beantwortung der Anfrage einverstanden.</span></label>
    <button class="btn btn-primary" type="submit">Anfrage senden</button>
  </form>
</div></div></section>'''
kt = kt.replace('<section class="section"><div class="wrap grid c2">', '<section class="section"><div class="wrap grid c2">', 1)
layout("kontakt/index.html", f'Kontakt & Anfahrt – Weekly Deals {C["ORT"]}', f'Weekly Deals {C["ORT"]}: Telefon, WhatsApp, Adresse, Öffnungszeiten, Karte und Kontaktformular.', kt, 1, "kontakt/")

# ---------- Danke / 404 ----------
layout("danke/index.html", 'Danke für deine Nachricht | Weekly Deals', 'Wir haben deine Nachricht erhalten.', f'''<section class="section"><div class="wrap" style="max-width:640px;text-align:center"><h1>Danke! ✅</h1><p class="lead">Wir melden uns in der Regel am selben Werktag. Dringend? Ruf uns an.</p>
<div class="btn-row" style="justify-content:center"><a class="btn btn-primary" href="tel:{C["TEL_RAW"]}">📞 {C["TEL"]}</a><a class="btn btn-light" href="../wochendeals/">Weitere Deals ansehen</a></div></div></section>''', 1, noindex=True)
layout("404.html", 'Seite nicht gefunden | Weekly Deals', 'Diese Seite gibt es nicht.', '''<section class="section"><div class="wrap" style="max-width:640px;text-align:center"><h1>404 – Hier ist nichts</h1><p class="lead">Die Seite gibt es nicht (mehr). Die aktuellen Deals findest du hier:</p><a class="btn btn-primary" href="/wochendeals/">🔥 Zu den Wochendeals</a></div></section>''', 0, noindex=True)

# ---------- Rechtliches ----------
imp = f'''<h2>Betreiberin</h2><p>{C["FIRMA"]}<br>Rechtsform: {C["RECHTSFORM"]}<br>{C["STRASSE"]}<br>{C["PLZ_ORT"]}<br>Schweiz</p>
<h2>Kontakt</h2><p>Telefon: <a href="tel:{C["TEL_RAW"]}">{C["TEL"]}</a><br>E-Mail: <a href="mailto:{C["EMAIL"]}">{C["EMAIL"]}</a></p>
<h2>Handelsregister / Steuern</h2><p>UID: {C["UID"]}<br>MWST-Nr.: {C["MWST"]} [falls mehrwertsteuerpflichtig]</p>
<h2>Vertretungsberechtigte Person(en)</h2><p>[Name, Funktion]</p>
<h2>Haftungsausschluss</h2><p>Wir prüfen die Inhalte dieser Website sorgfältig, übernehmen aber keine Gewähr für Richtigkeit, Vollständigkeit und Aktualität. Für Inhalte verlinkter Seiten sind ausschliesslich deren Betreiber verantwortlich.</p>
<h2>Urheberrecht</h2><p>Texte, Bilder und Grafiken dieser Website sind urheberrechtlich geschützt. Eine Verwendung bedarf unserer vorgängigen Zustimmung.</p>'''
layout("impressum/index.html", 'Impressum | Weekly Deals', 'Impressum von Weekly Deals: Firma, Adresse, UID, Kontakt.', legal("../", "Impressum", imp), 1, noindex=False)

ds = f'''<h2>1. Verantwortliche Stelle</h2><p>{C["FIRMA"]}, {C["STRASSE"]}, {C["PLZ_ORT"]}, Schweiz. Kontakt für Datenschutzfragen: <a href="mailto:{C["EMAIL"]}">{C["EMAIL"]}</a></p>
<h2>2. Geltungsbereich</h2><p>Diese Erklärung beschreibt, wie wir beim Besuch dieser Website und bei Anfragen Personendaten nach dem schweizerischen Datenschutzgesetz (revDSG) bearbeiten. Soweit Personen aus der EU/dem EWR angesprochen werden, beachten wir zusätzlich die DSGVO.</p>
<h2>3. Welche Daten, wozu</h2>
<ul><li><b>Server-Logdaten</b> (IP-Adresse, Zeitpunkt, aufgerufene Seite, Browser): technisch notwendig für Betrieb und Sicherheit. [Hosting-Anbieter und Standort eintragen]</li>
<li><b>Kontaktformular / E-Mail / Telefon / WhatsApp</b>: Name, E-Mail, ggf. Telefon und Nachricht – nur zur Beantwortung deiner Anfrage und Abwicklung von Reservationen.</li>
<li><b>Deal-Alarm (Newsletter)</b>: E-Mail-Adresse, nur mit deiner Einwilligung. Abmeldung jederzeit über den Link in jeder E-Mail (Art. 3 Abs. 1 lit. o UWG).</li>
<li><b>Statistik</b>: nur nach deiner Einwilligung im Cookie-Banner. [Tool eintragen, z. B. Google Analytics / Plausible; bei Google: Datenübermittlung in die USA.] Gemessen werden Seitenaufrufe, Anrufklicks, WhatsApp-Klicks und Formular-Absendungen.</li>
<li><b>Karte</b>: wird erst nach Klick von OpenStreetMap geladen. Dabei erhält der Anbieter deine IP-Adresse. [Bei Wechsel auf Google Maps hier anpassen: Übermittlung in die USA.]</li>
<li><b>Schriften</b>: Es werden Systemschriften verwendet, keine Schriften von Drittanbietern.</li></ul>
<h2>4. Weitergabe</h2><p>Wir geben Daten nur weiter, soweit nötig: Hosting, Formular-Dienst [Anbieter], E-Mail-Versand, Zahlungs- und Versanddienstleister [eintragen]. Mit Dienstleistern bestehen Verträge zur Auftragsbearbeitung. Bei Anbietern in Ländern ohne angemessenen Datenschutz (z. B. USA) stützen wir uns auf Garantien wie Standardvertragsklauseln bzw. das Swiss-US Data Privacy Framework [prüfen].</p>
<h2>5. Aufbewahrung</h2><p>Wir speichern Daten nur so lange, wie es für den Zweck nötig ist oder gesetzliche Pflichten es verlangen (z. B. 10 Jahre für Geschäftsunterlagen).</p>
<h2>6. Deine Rechte</h2><p>Du hast das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung, Datenherausgabe und Widerspruch sowie darauf, eine Einwilligung jederzeit zu widerrufen. Schreib uns an <a href="mailto:{C["EMAIL"]}">{C["EMAIL"]}</a>. Beschwerden kannst du beim Eidg. Datenschutz- und Öffentlichkeitsbeauftragten (EDÖB) einreichen.</p>
<h2>7. Cookies</h2><p>Notwendige Technik funktioniert ohne Einwilligung. Alles Weitere (Statistik) wird nur nach Opt-in geladen. Deine Wahl kannst du über „Cookie-Einstellungen“ im Footer ändern.</p>
<h2>8. Änderungen</h2><p>Wir können diese Erklärung anpassen. Es gilt die jeweils veröffentlichte Version. Stand: [Datum].</p>'''
layout("datenschutz/index.html", 'Datenschutzerklärung | Weekly Deals', 'Datenschutzerklärung nach revDSG: Welche Daten wir wozu bearbeiten und welche Rechte du hast.', legal("../", "Datenschutzerklärung", ds), 1)

agb = f'''<h2>1. Geltung</h2><p>Diese AGB gelten für alle Verkäufe von {C["FIRMA"]} (nachfolgend «Verkäuferin») an Kundinnen und Kunden.</p>
<h2>2. Angebot und Preise</h2><p>Alle Preise sind Endpreise in CHF inkl. MwSt., zuzüglich allfälliger Versandkosten, die vor der Bestellung ausgewiesen werden. Wochendeals sind befristet (Montag bis Sonntag) und gelten solange Vorrat reicht. Der Zustand der Ware (Neuware, B-Ware, gebraucht) wird beim Artikel angegeben.</p>
<h2>3. Vertragsschluss</h2><p>Der Vertrag kommt zustande, sobald wir die Bestellung bzw. Reservation schriftlich (z. B. per E-Mail) bestätigen. [Bestellprozess präzisieren]</p>
<h2>4. Zahlung</h2><p>Zahlungsarten: [z. B. TWINT, Rechnung, Vorkasse, Barzahlung bei Abholung]. Zahlungsfrist: [x Tage].</p>
<h2>5. Lieferung</h2><p>Abholung in {C["PLZ_ORT"]} oder Versand per [Post/Kurier]. Versandkosten: [CHF x]. Lieferfrist: [x Werktage].</p>
<h2>6. Rückgabe</h2><p>[Freiwillige Rückgabefrist oder Ausschluss festlegen und klar nennen.]</p>
<h2>7. Gewährleistung</h2><p>Es gelten die gesetzlichen Bestimmungen. [Bei gebrauchter Ware/B-Ware: Verkürzung der Frist gemäss Art. 210 OR juristisch prüfen.]</p>
<h2>8. Haftung</h2><p>[Haftungsbeschränkung im gesetzlich zulässigen Rahmen formulieren.]</p>
<h2>9. Datenschutz</h2><p>Siehe <a href="../datenschutz/">Datenschutzerklärung</a>.</p>
<h2>10. Recht und Gerichtsstand</h2><p>Es gilt Schweizer Recht. Gerichtsstand: [Ort]. Zwingende Konsumentengerichtsstände bleiben vorbehalten.</p>'''
layout("agb/index.html", 'AGB | Weekly Deals', 'Allgemeine Geschäftsbedingungen von Weekly Deals: Preise, Zahlung, Lieferung, Rückgabe.', legal("../", "Allgemeine Geschäftsbedingungen (AGB)", agb), 1)

# ---------- Sitemap / robots ----------
urls = "".join(f'<url><loc>{C["DOMAIN"]}/{p.replace("index.html","")}</loc><changefreq>weekly</changefreq></url>' for p in sorted(PAGES))
open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
open(os.path.join(OUT, "robots.txt"), "w").write(f'User-agent: *\nAllow: /\nDisallow: /danke/\nSitemap: {C["DOMAIN"]}/sitemap.xml\n')
# 404 liegt in beliebiger Tiefe -> absolute Pfade
f404 = os.path.join(OUT, "404.html"); t = open(f404, encoding="utf-8").read()
for a in ('href="css/', 'src="js/', 'href="wochendeals/', 'href="angebot/', 'href="ueber-uns/', 'href="bewertungen/', 'href="faq/', 'href="kontakt/', 'href="impressum/', 'href="datenschutz/', 'href="agb/'):
    t = t.replace(a, a[:-len(a.split('"')[1])] + "/" + a.split('"')[1])
t = t.replace('href=""', 'href="/"')
open(f404, "w", encoding="utf-8").write(t)
print(len(PAGES), "indexierbare Seiten gebaut")
