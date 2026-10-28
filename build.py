#!/usr/bin/env python3
"""Generates the division11studios.com static site into ./_site.

Edit the CO / APPS data below, then run `python3 build.py` (no dependencies).
GitHub Actions runs this on every push to main and deploys _site to Pages.
"""
import os, re, shutil

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_site")
SRC = os.path.dirname(os.path.abspath(__file__))

CO = {
    "brand": "Division 11 Studios",
    "legal": "Division Eleven Studios – Custom Software Design and Development",
    "legal_short": "Division Eleven Studios S.P.C.",
    "legal_ar": "شركة ديفيجن إيليفن ستوديوز لتصميم وبرمجة البرمجيات الخاصة ش.ش.و.",
    "form": "Single Person Company (S.P.C.)",
    "cr": "552091",
    "founded": "2026",
    "addr_lines": ["Building 9, Street 133", "Block 1, Al Nahda", "Kuwait City, Kuwait"],
    "phone": "+965 9008 5898",
    "phone_href": "+96590085898",
    "support": "support@division11studios.com",
    "dev": "dev@division11studios.com",
    "ceo": "Abdulrahman Bader Abdulwahab Alsanad",
    "instagram": "https://www.instagram.com/division11studios/",
    "tiktok": "https://www.tiktok.com/@division11studios",
}

APPS = [
    {
        "slug": "scorey",
        "name": "Scorey",
        "tagline": "Digital card game scorecard",
        "accent": "#FFBF00",
        "bg": "#1C3156",
        "mono": "S",
        "category": "Utilities",
        "platforms": "iPhone, iPad and Android",
        "summary": "Scorey replaces pen and paper at the card table. Enter each round and it keeps the running totals, the history and the winner — fast, accurate and anonymous.",
        "features": [
            ("Instant calculation", "Enter points per round; Scorey handles the totals and shows a live preview of the running score."),
            ("Many games built in", "Kout, Trix, Hand, Balot, Tarneeb, Sbeeta, Nthala, Domino, Rummy, Cribbage, Skyjo, Uno and a general scoresheet."),
            ("Spectator mode", "Share a QR code so anyone on the same Wi-Fi can follow the scores live."),
            ("Game history & sharing", "Every finished game is saved on the device and can be shared as a visual scorecard."),
            ("Built-in rules", "Help guides with pictures explain each game's rules and scoring."),
            ("English & Arabic", "Full bilingual interface, including Arabic-Indic numerals."),
        ],
        "ios": "https://apps.apple.com/app/scorey/id6761244968",
        "android": "https://play.google.com/store/apps/details?id=com.division11.scorey",
        "pricing": "Free with ads · optional one-time “Remove Ads” purchase",
        "age": "13+",
    },
    {
        "slug": "artnest",
        "name": "ArtNest",
        "tagline": "Color, draw & imagine",
        "accent": "#FF7A59",
        "bg": "#2A1B5C",
        "mono": "A",
        "category": "Education",
        "platforms": "iPhone, iPad and Android",
        "summary": "ArtNest is a family-friendly creative studio with five ways to make art — from classic coloring pages to glowing neon drawings — in a safe, simple interface.",
        "features": [
            ("Coloring book", "A large library of outlines across many themes to build motor skills and color recognition."),
            ("Color by number", "Follow the guide to reveal finished artworks — relaxing and educational."),
            ("Pixel coloring", "Grid-based pixel art with hints and progress tracking."),
            ("Glow drawing", "A neon canvas where every stroke lights up."),
            ("Free drawing", "Brushes, glitter pens, magic markers and a big sticker collection."),
            ("Gallery & parental gate", "Artwork saves to an in-app gallery or the device; external links sit behind a parental gate."),
        ],
        "ios": "https://apps.apple.com/app/artnest-color-and-fun/id6761441675",
        "android": "https://play.google.com/store/apps/details?id=com.division11.artnest",
        "pricing": "Free · optional “Remove Ads” purchase",
        "age": "4+",
    },
]

NAV = [("/", "Home"), ("/apps/", "Apps"), ("/about/", "About"), ("/support/", "Support")]

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def wordmark(light=False):
    return ('<img class="logo logo-light" src="/assets/D11_Full_Logo_Color_On_Light.svg" alt="Division 11 Studios" width="146" height="35">'
            '<img class="logo logo-dark" src="/assets/D11_Full_Logo_Color_On_Dark.svg" alt="Division 11 Studios" width="146" height="35">')

def page(path, title, desc, body, active=None, hero=False):
    nav = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a>' for h, t in NAV)
    full_title = f"{title} · {CO['brand']}" if title else f"{CO['brand']} — Mobile apps & games from Kuwait"
    addr = "<br>".join(CO["addr_lines"])
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="https://www.division11studios.com{path}">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://www.division11studios.com{path}">
<meta name="theme-color" content="#0A0630">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Sora:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Organization","name":"{CO['brand']}","legalName":"{CO['legal']}","url":"https://www.division11studios.com","email":"{CO['support']}","telephone":"{CO['phone_href']}","foundingDate":"{CO['founded']}","address":{{"@type":"PostalAddress","streetAddress":"Building 9, Street 133, Block 1","addressLocality":"Al Nahda, Kuwait City","addressCountry":"KW"}},"sameAs":["{CO['instagram']}","{CO['tiktok']}"]}}
</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header{' on-dark' if hero else ''}">
  <div class="wrap bar">
    <a class="brand" href="/" aria-label="{CO['brand']} home">{wordmark()}</a>
    <input type="checkbox" id="navtoggle" class="navtoggle" aria-label="Menu">
    <label for="navtoggle" class="burger" aria-hidden="true"><span></span><span></span><span></span></label>
    <nav class="nav" aria-label="Main">{nav}</nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap foot-grid">
    <div>
      <div class="foot-brand">{wordmark()}</div>
      <p class="muted small">Mobile apps and games, designed and built in Kuwait.</p>
      <p class="social small"><a href="{CO['instagram']}" rel="noopener">Instagram</a> · <a href="{CO['tiktok']}" rel="noopener">TikTok</a></p>
    </div>
    <div>
      <h3>Company</h3>
      <p class="small">{esc(CO['legal'])}<br>{CO['form']}<br>Commercial Registration No. {CO['cr']}</p>
    </div>
    <div>
      <h3>Address</h3>
      <p class="small">{addr}</p>
    </div>
    <div>
      <h3>Contact</h3>
      <p class="small"><a href="mailto:{CO['support']}">{CO['support']}</a><br><a href="tel:{CO['phone_href']}">{CO['phone']}</a></p>
      <p class="small"><a href="/privacy/">Privacy</a> · <a href="/terms/">Terms</a></p>
    </div>
  </div>
  <div class="wrap legal-line small">© {CO['founded']} {esc(CO['legal'])}. All rights reserved. “Division 11 Studios” is the trading name of {esc(CO['legal_short'])}</div>
</footer>
</body>
</html>
"""
    out = os.path.join(OUT, path.strip("/"), "index.html") if path != "/404" else os.path.join(OUT, "404.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)

def store_buttons(a, cls=""):
    return f"""<div class="stores {cls}">
  <a class="store" href="{a['ios']}" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M16.4 12.6c0-2.4 2-3.6 2.1-3.7-1.1-1.7-2.9-1.9-3.5-1.9-1.5-.2-2.9.9-3.7.9-.8 0-1.9-.9-3.2-.8-1.6 0-3.1 1-4 2.4-1.7 3-.4 7.4 1.2 9.8.8 1.2 1.8 2.5 3 2.4 1.2 0 1.7-.8 3.1-.8 1.5 0 1.9.8 3.2.8 1.3 0 2.1-1.2 2.9-2.4.9-1.4 1.3-2.7 1.3-2.8-.1 0-2.5-1-2.4-3.9zM14 5.5c.7-.8 1.1-1.9 1-3-1 0-2.1.7-2.8 1.5-.6.7-1.2 1.8-1 2.9 1 .1 2.1-.6 2.8-1.4z"/></svg><span><small>Download on the</small>App Store</span></a>
  <a class="store" href="{a['android']}" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M3.6 2.3c-.3.3-.4.7-.4 1.2v17c0 .5.1.9.4 1.2l9.5-9.7-9.5-9.7zm10.6 10.8 2.6 2.6-11.2 6.4 8.6-9zm0-2.2-8.6-9 11.2 6.4-2.6 2.6zm3.9-2 3 1.7c.9.5.9 1.3 0 1.8l-3 1.7-2.8-2.6 2.8-2.6z"/></svg><span><small>Get it on</small>Google Play</span></a>
</div>"""

def app_icon(a, size="lg"):
    return f'<div class="appicon {size}" style="--a:{a["accent"]};--b:{a["bg"]}" aria-hidden="true">{a["mono"]}</div>'

# ---------- Home
def home():
    cards = "".join(f"""
    <article class="app-card">
      {app_icon(a)}
      <div>
        <h3><a href="/{a['slug']}/">{a['name']}</a></h3>
        <p class="tag">{a['tagline']}</p>
        <p>{a['summary']}</p>
        <p class="meta small">{a['category']} · {a['platforms']}</p>
        {store_buttons(a, 'compact')}
      </div>
    </article>""" for a in APPS)
    body = f"""
<section class="hero">
  <div class="wrap hero-inner">
    <p class="eyebrow">Independent app studio · Kuwait</p>
    <h1>We design and build mobile apps and games people actually use.</h1>
    <p class="lead">{CO['brand']} develops and publishes apps for iPhone, iPad and Android — from everyday utilities to creative tools for families — and builds custom software and websites for clients.</p>
    <div class="cta"><a class="btn primary" href="/apps/">See our apps</a><a class="btn ghost" href="/about/">About the company</a></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Published apps</p><h2>Available now on the App Store and Google Play</h2></div>
    <div class="app-grid">{cards}
    </div>
  </div>
</section>

<section class="section tint">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">What we do</p><h2>Software design and development</h2></div>
    <div class="three">
      <div class="feature"><h3>Mobile apps</h3><p>Native-quality apps for iOS and Android built with Flutter, from first prototype to store release, updates and support.</p></div>
      <div class="feature"><h3>Games & interactive</h3><p>Casual and creative games built in Unity, with attention to performance, accessibility and family-safe design.</p></div>
      <div class="feature"><h3>Websites & maintenance</h3><p>Website design, development and ongoing software maintenance for businesses in Kuwait and the region.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap company-strip">
    <div>
      <p class="eyebrow">The company</p>
      <h2>{esc(CO['legal'])}</h2>
      <p>A Single Person Company (S.P.C.) registered with the Kuwait Ministry of Commerce and Industry, Commercial Registration No. {CO['cr']}, trading as {CO['brand']}.</p>
      <a class="textlink" href="/about/">More about us →</a>
    </div>
    <address>
      <strong>Office</strong><br>{'<br>'.join(CO['addr_lines'])}<br><br>
      <a href="mailto:{CO['support']}">{CO['support']}</a><br>
      <a href="tel:{CO['phone_href']}">{CO['phone']}</a>
    </address>
  </div>
</section>
"""
    page("/", "", f"{CO['brand']} is an independent mobile app and game studio in Kuwait, makers of Scorey and ArtNest.", body, active="/", hero=True)

# ---------- Apps list
def apps_page():
    rows = "".join(f"""
    <article class="app-row">
      {app_icon(a)}
      <div class="app-row-body">
        <h2><a href="/{a['slug']}/">{a['name']}</a> <span class="tag">— {a['tagline']}</span></h2>
        <p>{a['summary']}</p>
        <p class="meta small">{a['category']} · {a['platforms']} · Rated {a['age']} · {a['pricing']}</p>
        {store_buttons(a)}
        <p class="small links"><a href="/{a['slug']}/">Details</a> · <a href="/{a['slug']}/privacy/">Privacy policy</a> · <a href="/support/">Support</a></p>
      </div>
    </article>""" for a in APPS)
    body = f"""
<section class="page-head"><div class="wrap"><p class="eyebrow">Our apps</p><h1>Apps by {CO['brand']}</h1><p class="lead">Everything we publish on the App Store and Google Play.</p></div></section>
<section class="section"><div class="wrap app-list">{rows}
<p class="muted">More titles are in development, including a multiplayer trivia game.</p>
</div></section>"""
    page("/apps/", "Apps", f"Apps published by {CO['brand']}: Scorey and ArtNest for iOS and Android.", body, active="/apps/")

# ---------- App detail
def app_page(a):
    feats = "".join(f'<div class="feature"><h3>{t}</h3><p>{d}</p></div>' for t, d in a["features"])
    body = f"""
<section class="app-hero" style="--a:{a['accent']};--b:{a['bg']}">
  <div class="wrap app-hero-inner">
    {app_icon(a, 'xl')}
    <div>
      <p class="eyebrow">{a['category']}</p>
      <h1>{a['name']}</h1>
      <p class="lead">{a['tagline']}</p>
      {store_buttons(a)}
    </div>
  </div>
</section>
<section class="section"><div class="wrap narrow"><p class="lead dark">{a['summary']}</p></div></section>
<section class="section tint"><div class="wrap"><div class="section-head"><h2>Features</h2></div><div class="three">{feats}</div></div></section>
<section class="section"><div class="wrap">
  <dl class="facts">
    <div><dt>Platforms</dt><dd>{a['platforms']}</dd></div>
    <div><dt>Price</dt><dd>{a['pricing']}</dd></div>
    <div><dt>Age rating</dt><dd>{a['age']}</dd></div>
    <div><dt>Developer</dt><dd>{CO['brand']}</dd></div>
  </dl>
  <p class="small links"><a href="/{a['slug']}/privacy/">{a['name']} privacy policy</a> · <a href="/terms/">Terms of use</a> · <a href="/support/">Get support</a></p>
</div></section>"""
    page(f"/{a['slug']}/", a["name"], f"{a['name']} by {CO['brand']} — {a['tagline']}. {a['summary']}", body, active="/apps/")

# ---------- About
def about():
    body = f"""
<section class="page-head"><div class="wrap"><p class="eyebrow">About</p><h1>About {CO['brand']}</h1></div></section>
<section class="section"><div class="wrap two">
  <div class="prose">
    <p class="lead dark">{CO['brand']} is an independent software studio based in Kuwait City. We design, build and publish mobile apps and games for iPhone, iPad and Android, and we develop custom software and websites for clients.</p>
    <p>The studio was founded in {CO['founded']} by {CO['ceo']}, who leads design and development. Our apps are built in Flutter and Unity and are released on both the Apple App Store and Google Play. Our first titles are <a href="/scorey/">Scorey</a>, a scorekeeper for traditional and modern card games, and <a href="/artnest/">ArtNest</a>, a creative coloring and drawing app for the whole family.</p>
    <p>We care about apps that are fast, respectful of privacy and work in both English and Arabic. Game history and artwork stay on your device, and we don’t require accounts.</p>
    <h2>Licensed activities</h2>
    <ul>
      <li>Software design and programming (application development)</li>
      <li>Website design</li>
      <li>Software maintenance and web page design</li>
    </ul>
  </div>
  <aside class="card">
    <h2>Company details</h2>
    <dl class="kv">
      <dt>Legal name</dt><dd>{esc(CO['legal'])}</dd>
      <dt>Arabic name</dt><dd lang="ar" dir="rtl">{CO['legal_ar']}</dd>
      <dt>Trading name</dt><dd>{CO['brand']}</dd>
      <dt>Legal form</dt><dd>{CO['form']}</dd>
      <dt>Commercial Registration</dt><dd>No. {CO['cr']} — Kuwait Ministry of Commerce and Industry</dd>
      <dt>Established</dt><dd>{CO['founded']}</dd>
      <dt>CEO</dt><dd>{CO['ceo']}</dd>
      <dt>Address</dt><dd>{'<br>'.join(CO['addr_lines'])}</dd>
      <dt>Email</dt><dd><a href="mailto:{CO['dev']}">{CO['dev']}</a></dd>
      <dt>Phone</dt><dd><a href="tel:{CO['phone_href']}">{CO['phone']}</a></dd>
    </dl>
  </aside>
</div></section>"""
    page("/about/", "About", f"About {CO['legal']} ({CO['brand']}), a software studio in Kuwait City.", body, active="/about/")

# ---------- Support
def support():
    body = f"""
<section class="page-head"><div class="wrap"><p class="eyebrow">Support</p><h1>How can we help?</h1><p class="lead">We usually reply within two business days.</p></div></section>
<section class="section"><div class="wrap two">
  <div class="prose">
    <h2>Contact support</h2>
    <p>Email <a href="mailto:{CO['support']}">{CO['support']}</a> and include the app name, your device model and what happened. Screenshots help.</p>
    <p>For business enquiries, partnerships or client projects, write to <a href="mailto:{CO['dev']}">{CO['dev']}</a> or call <a href="tel:{CO['phone_href']}">{CO['phone']}</a>.</p>
    <h2>Common questions</h2>
    <details><summary>I bought “Remove Ads” but still see ads.</summary><p>Open the app’s settings and tap <em>Restore purchases</em> while signed in with the same Apple ID or Google account you used to buy it. If that doesn’t work, email us with your order receipt.</p></details>
    <details><summary>How do I get a refund?</summary><p>Purchases are processed by Apple or Google. Request a refund at <a href="https://reportaproblem.apple.com" rel="noopener">reportaproblem.apple.com</a> (App Store) or through your Google Play order history.</p></details>
    <details><summary>Where is my data stored? Can I delete it?</summary><p>Scorey game history and ArtNest artwork are stored only on your device. Delete them in the app, clear the app’s data, or uninstall the app. See each app’s privacy policy for details.</p></details>
    <details><summary>Is ArtNest safe for children?</summary><p>ArtNest needs no account, collects no personal information and places external links behind a parental gate.</p></details>
  </div>
  <aside class="card">
    <h2>App resources</h2>
    {''.join(f'<p><strong>{a["name"]}</strong><br><a href="/{a["slug"]}/">About the app</a> · <a href="/{a["slug"]}/privacy/">Privacy policy</a></p>' for a in APPS)}
    <p><a href="/terms/">Terms of use</a></p>
  </aside>
</div></section>"""
    page("/support/", "Support", f"Support and contact for {CO['brand']} apps.", body, active="/support/")

# ---------- Terms
def terms():
    body = f"""
<section class="page-head"><div class="wrap"><p class="eyebrow">Legal</p><h1>Terms of Use</h1><p class="muted">Last updated: 29 October 2026</p></div></section>
<section class="section"><div class="wrap narrow prose">
<p>These terms apply to the apps published by {esc(CO['legal'])} (“{CO['brand']}”, “we”, “us”) and to this website. By downloading or using our apps you agree to them.</p>
<h2>1. Licence</h2><p>We grant you a personal, non-exclusive, non-transferable licence to use our apps on devices you own or control, subject to these terms and to the Apple Media Services Terms or Google Play Terms of Service, as applicable. Apps downloaded from the App Store are also licensed under Apple’s Standard Licensed Application End User License Agreement.</p>
<h2>2. Purchases</h2><p>In-app purchases are sold and processed by Apple or Google. Prices, payment, refunds and restoration of purchases are handled under the store’s terms.</p>
<h2>3. Acceptable use</h2><p>You may not copy, modify, reverse-engineer, redistribute or tamper with our apps, bypass their security or advertising systems, or use them for any unlawful purpose.</p>
<h2>4. Advertising</h2><p>Some apps show advertisements provided by third-party networks. Their handling of data is described in each app’s privacy policy.</p>
<h2>5. Privacy</h2><p>How we handle information is described in the privacy policy for each app: <a href="/scorey/privacy/">Scorey</a>, <a href="/artnest/privacy/">ArtNest</a>, and for this website in our <a href="/privacy/">website privacy notice</a>.</p>
<h2>6. Intellectual property</h2><p>The apps, their content, names and logos are owned by {CO['brand']} or its licensors and are protected by law.</p>
<h2>7. Disclaimer and liability</h2><p>Our apps are provided “as is”. Scores, results and content are for entertainment and convenience. To the extent permitted by law, we are not liable for indirect or consequential loss arising from use of the apps.</p>
<h2>8. Changes</h2><p>We may update these terms. The current version is always published on this page.</p>
<h2>9. Governing law</h2><p>These terms are governed by the laws of the State of Kuwait.</p>
<h2>10. Contact</h2><p>{esc(CO['legal'])}, {', '.join(CO['addr_lines'])}. Email <a href="mailto:{CO['support']}">{CO['support']}</a>.</p>
</div></section>"""
    page("/terms/", "Terms of Use", f"Terms of use for {CO['brand']} apps and website.", body)

# ---------- Website privacy
def privacy():
    body = f"""
<section class="page-head"><div class="wrap"><p class="eyebrow">Legal</p><h1>Privacy</h1><p class="muted">Last updated: 29 October 2026</p></div></section>
<section class="section"><div class="wrap narrow prose">
<h2>App privacy policies</h2>
<ul>{''.join(f'<li><a href="/{a["slug"]}/privacy/">{a["name"]} privacy policy</a></li>' for a in APPS)}</ul>
<h2>This website</h2>
<p>This website is a static site hosted on GitHub Pages. We do not use cookies, analytics or forms here, and we do not collect personal information through it. Our hosting provider may keep standard server logs (such as IP address and browser type) for security. Fonts are loaded from Google Fonts.</p>
<p>If you email us, we use your message and address only to reply.</p>
<h2>Contact</h2>
<p>{esc(CO['legal'])}, {', '.join(CO['addr_lines'])} — <a href="mailto:{CO['support']}">{CO['support']}</a></p>
</div></section>"""
    page("/privacy/", "Privacy", f"Privacy information for {CO['brand']} apps and website.", body)

def notfound():
    body = """<section class="page-head"><div class="wrap"><p class="eyebrow">404</p><h1>Page not found</h1><p class="lead">The page you’re looking for doesn’t exist. <a href="/">Go to the home page</a>.</p></div></section>"""
    page("/404", "Not found", "Page not found.", body)

# ---------- Copy existing app privacy policies, adding a link back to the site
def copy_policy(slug, src):
    with open(os.path.join(SRC, src), encoding="utf-8") as f:
        h = f.read()
    back = ('<div style="max-width:850px;margin:0 auto 16px;font:500 14px/1.4 -apple-system,Segoe UI,Roboto,sans-serif">'
            '<a href="/" style="color:inherit;opacity:.75;text-decoration:none">← Division 11 Studios</a></div>')
    h = re.sub(r"(<body[^>]*>)", r"\1\n" + back.replace("\\", "\\\\"), h, count=1)
    h = h.replace("</head>", '<link rel="canonical" href="https://www.division11studios.com/%s/privacy/">\n<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">\n</head>' % slug, 1)
    d = os.path.join(OUT, slug, "privacy")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(h)

def statics():
    a = os.path.join(OUT, "assets"); os.makedirs(a, exist_ok=True)
    shutil.copy(os.path.join(SRC, "site.css"), os.path.join(a, "site.css"))
    B = os.path.join(SRC, "brand")
    for f in ["D11_Full_Logo_Color_On_Light.svg","D11_Full_Logo_Color_On_Dark.svg"]:
        shutil.copy(os.path.join(B, f), os.path.join(a, f))
    shutil.copy(os.path.join(B, "D11_Logomark_Blue_White_Primary.svg"), os.path.join(a, "favicon.svg"))
    shutil.copy(os.path.join(SRC, "app-ads.txt"), os.path.join(OUT, "app-ads.txt"))
    with open(os.path.join(OUT, "CNAME"), "w") as f: f.write("www.division11studios.com\n")
    with open(os.path.join(OUT, ".nojekyll"), "w") as f: f.write("")
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write("User-agent: *\nAllow: /\nSitemap: https://www.division11studios.com/sitemap.xml\n")
    urls = ["/", "/apps/", "/about/", "/support/", "/terms/", "/privacy/"] + [f"/{x['slug']}/" for x in APPS] + [f"/{x['slug']}/privacy/" for x in APPS]
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u in urls: f.write(f"  <url><loc>https://www.division11studios.com{u}</loc></url>\n")
        f.write("</urlset>\n")

if __name__ == "__main__":
    shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
    home(); apps_page(); about(); support(); terms(); privacy(); notfound()
    for x in APPS: app_page(x)
    copy_policy("scorey", "policies/scorey.html")
    copy_policy("artnest", "policies/artnest.html")
    statics()
    print("built", sum(len(fs) for _, _, fs in os.walk(OUT)), "files")
