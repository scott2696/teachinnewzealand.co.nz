#!/usr/bin/env python3
"""Pokies Kiwi static builder.

Reads _build/pages/*.html fragments (JSON front matter inside <!--@ ... @-->)
and writes clean-URL pages to {url}index.html.

Handles for authors:
  {{aff:slug}}                affiliate URL (casino)
  {{affs:slug}}               affiliate URL (sportsbook, falls back to casino)
  {{op:slug:field}}           any field from operators.json
  <!--TOPLIST slugs|Heading|Intro-->      renders the ranked leaderboard
  <!--CTA slug|Heading|Body-->            renders a single-operator CTA band
  <details class="faq-i">...              auto-lifted into FAQPage schema

Emits: page HTML, sitemap.xml, robots.txt.
"""
import datetime
import json, os, re, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, "_build", "pages")

DOMAIN   = "https://teachinnewzealand.co.nz"
SITE     = "Pokies Kiwi"
BRAND_A  = "POKIES"
BRAND_B  = "KIWI"
TAGLINE  = "NZ Online Pokies &amp; Casino Guide"
POSTER_TAGLINE = "We put our own money on the table, then tell you what happened."
UPDATED  = "2026-09-02"
UPDATED_H= "2 September 2026"
PUBLISHED= "2026-05-04"
EMAIL    = "editor@teachinnewzealand.co.nz"

OPS = json.load(open(os.path.join(ROOT, "_build", "operators.json")))
DEFAULT_ORDER = [k for k, _ in sorted(OPS.items(),
                                      key=lambda kv: (-float(kv[1]["rating"]), kv[1]["name"]))]

# cache-buster derived from the stylesheet itself, so a CSS edit invalidates
# every page's cached copy without touching the HTML by hand
import hashlib
_css_path = os.path.join(ROOT, "assets", "css", "site.css")
CSS_V = hashlib.md5(open(_css_path, "rb").read()).hexdigest()[:8] if os.path.exists(_css_path) else "1"

# ---------------------------------------------------------------- authors
AUTHORS = {
 "nikau": dict(
   name="Nikau Te Aho", slug="nikau-te-aho", initials="NT", url="/authors/nikau-te-aho/",
   photo="/images/authors/nikau-te-aho.jpg",
   role="Lead Reviewer", short="Lead Reviewer",
   knows=["online pokies","online casinos","NZD payments","withdrawal testing","RTP and volatility","cryptocurrency gambling"],
   job="Lead Reviewer",
   bio="Nikau spent five years as a payments and fraud analyst inside a licensed gaming operator before moving to the other side of the cashier. He opens every account on this site himself, funds it with his own New Zealand dollars, times each withdrawal from a residential connection in Auckland, and runs the 40-title RTP sample behind every return figure we publish.",
   long="Nikau Te Aho (Ng&#257;ti Porou) worked five years as a payments and fraud analyst for a licensed gaming operator, reconciling deposits and investigating withdrawal holds, before he started writing about the industry from the player's side. He built the withdrawal timing protocol this site uses and the 40-title RTP sampling method behind every return figure we publish, and has personally opened and verified an account at all sixteen sites we cover. He tests on a 2019 Android handset on Spark 4G as well as on desktop fibre, because that is what most Kiwi readers are actually using.",
   sameAs=["https://www.linkedin.com/in/example-nikau-te-aho"]),
 "charlotte": dict(
   name="Charlotte Wilson", slug="charlotte-wilson", initials="CW", url="/authors/charlotte-wilson/",
   photo="/images/authors/charlotte-wilson.jpg",
   role="Editor, Law &amp; Regulation", short="Editor, Law &amp; Regulation",
   knows=["New Zealand gambling law","Online Casino Gambling Act 2026","Gambling Act 2003","bonus terms and conditions","gambling taxation","responsible gambling"],
   job="Editor, Law and Regulation",
   bio="Charlotte read law at Te Herenga Waka&mdash;Victoria University of Wellington and reported on regulation before joining us. She reads the full terms on every offer we publish and fact-checks every legal and tax claim on this site.",
   long="Charlotte Wilson read law at Te Herenga Waka&mdash;Victoria University of Wellington and spent four years covering regulatory affairs before moving into gambling publishing. She tracks the Department of Internal Affairs licensing programme week by week, reads the complete terms and conditions on every bonus this site publishes, and is the final fact-check on all legal, tax and licensing statements we make. Where our reading of the law is contested, she says so in the text rather than smoothing it over.",
   sameAs=["https://www.linkedin.com/in/example-charlotte-wilson"]),
 "team": dict(
   name="The Pokies Kiwi Team", slug="editorial-team", initials="PK", url="/authors/",
   photo=None, role="Editorial Team", short="Editorial Team",
   knows=["online pokies","New Zealand gambling"],
   job="Editorial Team",
   bio="Our editorial team is based in New Zealand and tests every site we write about with real New Zealand dollars.",
   long="Pokies Kiwi is written and edited in New Zealand. Every operator we list has been signed up to, deposited into and withdrawn from by a member of the team using their own money.",
   sameAs=[]),
}

# ---------------------------------------------------------------- navigation
NAV = [
 ("Best Pokies", "/online-pokies/", [
   ("Best Online Pokies NZ", "/online-pokies/"),
   ("Highest RTP Pokies", "/highest-rtp-pokies/"),
   ("Jackpot Pokies", "/jackpot-pokies/"),
   ("Megaways Pokies", "/megaways-pokies/"),
   ("Mobile Pokies", "/mobile-pokies/"),
   ("Free Pokies (Demo Play)", "/free-pokies/"),
   ("Pokies Glossary", "/pokies-glossary/"),
 ]),
 ("Casinos", "/online-casinos/", [
   ("Best Online Casinos NZ", "/best-online-casinos/"),
   ("High Payout Casinos", "/high-payout-casinos/"),
   ("Fast Payout Casinos", "/fast-payout-casinos/"),
   ("Live Dealer Casinos", "/live-casinos/"),
   ("Crypto Casinos", "/best-crypto-casinos/"),
   ("Minimum Deposit Casinos", "/minimum-deposit-casinos/"),
   ("All Casino Reviews", "/casino-reviews/"),
 ]),
 ("Bonuses", "/online-casinos/bonuses/", [
   ("Casino Bonuses NZ", "/online-casinos/bonuses/"),
   ("No Deposit Bonuses", "/no-deposit-casinos/"),
   ("Free Spins", "/free-spins/"),
   ("Wagering Requirements", "/wagering-requirements/"),
 ]),
 ("Betting", "/online-betting/", [
   ("Online Betting NZ", "/online-betting/"),
   ("Sports Betting Sites", "/best-sports-betting-sites/"),
 ]),
 ("Guides", None, [
   ("NZ Online Casino Law", "/nz-online-casino-law/"),
   ("Tax on Winnings", "/gambling-winnings-tax-nz/"),
   ("Payment Methods", "/payment-methods/"),
   ("Withdrawal Times", "/withdrawal-times/"),
   ("Pub Pokies vs Online", "/pub-pokies-vs-online-pokies/"),
   ("Complaints &amp; Disputes", "/casino-complaints/"),
   ("How We Review", "/how-we-review/"),
 ]),
 ("About", "/about/", None),
 ("Contact", "/contact/", None),
]

FOOTER = [
 ("Pokies", [("Best Online Pokies NZ","/online-pokies/"),("Highest RTP Pokies","/highest-rtp-pokies/"),
   ("Jackpot Pokies","/jackpot-pokies/"),("Megaways Pokies","/megaways-pokies/"),
   ("Mobile Pokies","/mobile-pokies/"),("Free Pokies","/free-pokies/"),("Pokies Glossary","/pokies-glossary/")]),
 ("Casinos &amp; Bonuses", [("Best Online Casinos NZ","/best-online-casinos/"),("High Payout Casinos","/high-payout-casinos/"),
   ("Fast Payout Casinos","/fast-payout-casinos/"),("Live Dealer Casinos","/live-casinos/"),
   ("Crypto Casinos","/best-crypto-casinos/"),("Minimum Deposit Casinos","/minimum-deposit-casinos/"),
   ("Casino Bonuses","/online-casinos/bonuses/"),("No Deposit Bonuses","/no-deposit-casinos/"),
   ("Free Spins","/free-spins/"),("Casino Reviews","/casino-reviews/")]),
 ("Betting &amp; Guides", [("Online Betting NZ","/online-betting/"),("Sports Betting Sites","/best-sports-betting-sites/"),
   ("NZ Online Casino Law","/nz-online-casino-law/"),("Tax on Gambling Winnings","/gambling-winnings-tax-nz/"),
   ("Payment Methods","/payment-methods/"),("Withdrawal Times","/withdrawal-times/"),
   ("Pub Pokies vs Online","/pub-pokies-vs-online-pokies/"),("Wagering Requirements","/wagering-requirements/"),
   ("Complaints &amp; Disputes","/casino-complaints/")]),
 ("Company", [("About Us","/about/"),("Contact Us","/contact/"),("Our Authors","/authors/"),
   ("How We Review","/how-we-review/"),("Responsible Gambling","/responsible-gambling/"),
   ("Terms and Conditions","/terms/"),("Privacy Policy","/privacy/"),("Cookie Policy","/cookie-policy/")]),
]

# ---------------------------------------------------------------- icons
IC = {
 "star":  '<path d="M12 3l2.6 5.3 5.9.9-4.3 4.1 1 5.8L12 16.9 6.8 19.2l1-5.8L3.5 9.2l5.9-.9z"/>',
 "bolt":  '<path d="M13 2 3 14h7l-1 8 10-12h-7z"/>',
 "warn":  '<path d="M10.3 3.6 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.6a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/>',
 "info":  '<circle cx="12" cy="12" r="9"/><path d="M12 16v-4M12 8h.01"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "check": '<path d="M20 6 9 17l-5-5"/>',
 "shield":'<path d="M12 3l7 3v6c0 4.5-3 8-7 9-4-1-7-4.5-7-9V6z"/><path d="M9.5 12l1.8 1.8 3.4-3.6"/>',
 "law":   '<path d="M12 3v18M5 7h14M7 7l-3 7h6zM17 7l-3 7h6z"/>',
 "coin":  '<circle cx="12" cy="12" r="9"/><path d="M12 7v10M9.5 9.5h4a1.8 1.8 0 0 1 0 3.6h-3a1.8 1.8 0 0 0 0 3.6h4"/>',
 "flag":  '<path d="M5 21V4M5 4h13l-2.5 4L18 12H5"/>',
 "user":  '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
}
def ic(k, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{IC[k]}</svg>')

# ---------------------------------------------------------------- helpers
MISSING = set()
def aff(slug, kind="casino"):
    op = OPS.get(slug)
    if not op:
        MISSING.add(slug); return "/casino-reviews/"
    url = op.get("sportsLink") if kind == "sports" else op.get("casinoLink")
    url = url or op.get("casinoLink") or op.get("sportsLink")
    if not url:
        MISSING.add(op["name"]); return "/casino-reviews/"
    return url

def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)

def resolve_tokens(s):
    s = re.sub(r"\{\{(aff|affs):([a-z0-9\-]+)\}\}",
               lambda m: html.escape(aff(m.group(2), "sports" if m.group(1) == "affs" else "casino"), quote=True), s)
    s = re.sub(r"\{\{op:([a-z0-9\-]+):([A-Za-z]+)\}\}",
               lambda m: str(OPS.get(m.group(1), {}).get(m.group(2), "")), s)
    s = re.sub(r"\{\{score:([a-z0-9\-]+)\}\}",
               lambda m: f"{rating10(m.group(1)):.1f}", s)
    return s

def review_url(slug):
    return f"/casino-reviews/{slug}/"

def logo_for(slug, sports=False):
    op = OPS.get(slug, {})
    if sports and op.get("logoSports"):
        return op["logoSports"]
    return op.get("logo") or f"/logos/{slug}.png"

def slugify(s):
    s = strip_tags(html.unescape(s)).lower()
    s = re.sub(r"[^a-z0-9\s\-]", "", s)
    return re.sub(r"[\s\-]+", "-", s).strip("-")[:70]


# ---------------------------------------------------------------- comparison tables
def _rtp_short(op):
    b = op.get("rtpBand", "")
    return b.split(" ")[0] if b else "&mdash;"

def _crypto(op):
    return '<span class="t-yes">Yes</span>' if op.get("crypto") else '<span class="t-no">No</span>'

def _nzd_short(op):
    v = op.get("nzd", "")
    return '<span class="t-yes">Yes</span>' if v.lower().startswith("yes") else v or "&mdash;"

def _score(op):
    return f'<b>{round(float(op.get("rating", 4)) * 2, 1)}</b>'

def _name(op):
    return f'<b><a href="{review_url(op["slug"])}">{op["name"]}</a></b>'

# column key -> (header, cell renderer, css classes on th/td)
# t-num  = monospace, no wrap, 104px min
# t-mid  = 150px min   t-wide = 210px min   (stops cells wrapping every word)
COLS = {
 "rank":     ("#",                 None,                                            "t-num"),
 "name":     ("Casino",            _name,                                           "t-mid"),
 "score":    ("Score",             _score,                                          "t-num"),
 "bestfor":  ("Best for",          lambda o: o.get("bestFor", ""),                  "t-mid"),
 "verdict":  ("Our verdict",       lambda o: o.get("verdict", ""),                  "t-wide"),
 "usp":      ("Standout",          lambda o: o.get("usp", ""),                      "t-wide"),
 "pokies":   ("Pokies",            lambda o: o.get("pokies", ""),                   "t-num"),
 "live":     ("Live tables",       lambda o: o.get("live", ""),                     "t-num"),
 "rtp":      ("Median RTP",        _rtp_short,                                      "t-num"),
 "fast":     ("Fastest payout",    lambda o: o.get("payoutFast", ""),               "t-num"),
 "speed":    ("Payout speeds",     lambda o: o.get("payoutSpeed", ""),              "t-wide"),
 "daily":    ("Daily cap",         lambda o: o.get("capDaily", ""),                 "t-num"),
 "monthly":  ("Monthly cap",       lambda o: o.get("capMonthly", ""),               "t-num"),
 "minwd":    ("Min withdrawal",    lambda o: o.get("minWithdraw", ""),              "t-num"),
 "mindep":   ("Min deposit",       lambda o: o.get("minDep", ""),                   "t-num"),
 "welcome":  ("Welcome offer",     lambda o: o.get("welcomeShort") or o.get("welcome",""), "t-wide"),
 "wagering": ("Wagering",          lambda o: o.get("wagering", ""),                 "t-mid"),
 "nzd":      ("NZD wallet",        _nzd_short,                                      ""),
 "crypto":   ("Crypto",            _crypto,                                         ""),
 "kyc":      ("Verification",      lambda o: o.get("kyc", ""),                      "t-wide"),
 "licence":  ("Licence",           lambda o: o.get("licenceShort") or o.get("licence",""), "t-mid"),
 "licref":   ("Licence number",    lambda o: o.get("licenceRef") or "Not published", "t-mid"),
 "operator": ("Operator",          lambda o: o.get("operator", ""),                 "t-mid"),
 "launched": ("Launched",          lambda o: str(o.get("launched", "")),            "t-num"),
 "app":      ("Mobile",            lambda o: o.get("app", ""),                      "t-mid"),
 "payments": ("Payment methods",   lambda o: o.get("payments", ""),                 "t-wide"),
 "providers":("Studios",           lambda o: o.get("providers", ""),                "t-wide"),
 "games":    ("Library",           lambda o: o.get("games", ""),                    "t-mid"),
}

def cmp_table(colkeys, caption, slugs):
    cols = [c.strip() for c in colkeys.split(",") if c.strip() in COLS]
    if not cols or not slugs:
        return ""
    def _th(c):
        cls = COLS[c][2]
        return "<th" + (' class="' + cls + '"' if cls else "") + ">" + COLS[c][0] + "</th>"
    head = "".join(_th(c) for c in cols)
    rows = []
    for i, slug in enumerate(slugs, 1):
        op = OPS.get(slug)
        if not op:
            MISSING.add(slug); continue
        tds = []
        for c in cols:
            label, fn, cls = COLS[c]
            val = str(i) if c == "rank" else (fn(op) if fn else "")
            klass = f' class="{cls}"' if cls else ""
            tds.append(f'<td{klass}>{val}</td>')
        rows.append("<tr>" + "".join(tds) + "</tr>")
    cap = f'<caption>{caption}</caption>' if caption else ""
    pinned = " is-pinned" if (cols[:2] == ["rank", "name"] and len(cols) >= 7) else ""
    return (f'<div class="tbl-wrap"><table class="cmp{pinned}">{cap}'
            f'<thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>')

# ---------------------------------------------------------------- chrome
def brand_lockup():
    mark = ('<span class="brand-mark">'
            '<svg viewBox="0 0 24 24" fill="none" stroke="#07211D" stroke-width="2.5" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            '<path d="M4 4v16"/><path d="M4 12.5 12.5 4"/><path d="M9 9l8 11"/>'
            '<circle cx="19" cy="6" r="1.7" fill="#07211D" stroke="none"/></svg></span>')
    return (f'{mark}<span><span class="bw">{BRAND_A}<em>{BRAND_B}</em></span>'
            f'<span class="brand-tag">{TAGLINE}</span></span>')


def nav_html():
    out = ['<header class="site-header"><div class="wrap">',
           f'<a class="brand" href="/" aria-label="{SITE} home">{brand_lockup()}</a>',
           '<button class="nav-toggle" aria-label="Menu" aria-expanded="false" '
           'onclick="var n=document.getElementById(\'nav\');n.classList.toggle(\'open\');'
           'this.setAttribute(\'aria-expanded\',n.classList.contains(\'open\'))">&#9776;</button>',
           '<nav class="nav" id="nav" aria-label="Main">']
    for label, href, kids in NAV:
        if not kids:
            out.append(f'<div class="nav-item"><a class="nav-top" href="{href}">{label}</a></div>')
        else:
            trig = (f'<a class="nav-top" href="{href}" aria-haspopup="true">{label}'
                    '<span class="nav-caret" aria-hidden="true">&#9662;</span></a>' if href else
                    f'<span class="nav-top" tabindex="0" role="button" aria-haspopup="true">{label}'
                    '<span class="nav-caret" aria-hidden="true">&#9662;</span></span>')
            links = "".join(f'<a href="{h}" role="menuitem">{l}</a>' for l, h in kids)
            out.append(f'<div class="nav-item has-sub">{trig}'
                       f'<div class="nav-drop" role="menu">{links}</div></div>')
    out.append('<a class="nav-cta" href="/online-pokies/">Top pokies sites</a>')
    out.append('</nav></div></header>')
    return "".join(out)


def foot_html():
    cols = ""
    for title, links in FOOTER:
        items = "".join(f'<a href="{h}">{l}</a>' for l, h in links)
        cols += f'<div><h4>{title}</h4>{items}</div>'
    year = datetime.date.today().year
    return f'''<footer class="site-footer"><div class="wrap">
<div class="foot-top">
<div class="foot-brand"><h4>{SITE}</h4>
<p>Independent New Zealand reviews of online pokies, casinos and betting. We open real accounts,
deposit our own New Zealand dollars and time every withdrawal &mdash; then publish what we found,
including the parts that cost us commission.</p>
<div class="foot-badges">
<span class="foot-badge"><span class="gc-18">18+</span> Strictly 18+</span>
<span class="foot-badge">{ic("shield")} Independently tested</span>
<span class="foot-badge">{ic("flag")} Written in NZ</span>
</div>
<div class="rg-mini"><span class="gc-18">18+</span> Gambling can be harmful. Free, confidential help in NZ:
<a href="tel:0800654655">Gambling Helpline 0800 654 655</a> &middot; free text 8006 &middot;
<a href="https://www.pgf.nz/" rel="nofollow noopener" target="_blank">PGF NZ</a>.</div>
</div>
<div class="cols">{cols}</div>
</div>
<div class="legal">
<p><strong>Affiliate disclosure:</strong> {SITE} is reader-supported. When you open an account through
a link on this site we may earn a commission, at no cost to you. It never influences a ranking &mdash;
our <a href="/how-we-review/">review methodology</a> is applied identically to every operator, and
commission carries zero weight in the score.</p>
<p><strong>New Zealand legal position.</strong> Online casinos serving New Zealanders are currently
licensed offshore. The <strong>Online Casino Gambling Act 2026</strong> came into force on 1 May 2026 and
the Department of Internal Affairs is issuing up to 15 New Zealand online casino licences; operators that
had not applied by 1 December 2026 must stop serving New Zealand players. Sports and racing betting is
separate and stricter: <strong>TAB NZ</strong>, including its Betcha brand, is the only operator lawfully
permitted to accept bets from people in New Zealand. See our <a href="/nz-online-casino-law/">guide to the
law</a> and our <a href="/online-betting/">betting page</a>.</p>
<p>&copy; {year} {SITE}. All rights reserved. You must be 18 or older to gamble online in New Zealand
(20+ for land-based casinos). Bonuses, terms and payout times were accurate at our last update
({UPDATED_H}) and change without notice &mdash; always read the operator's current terms before you deposit.
Please gamble responsibly and only with money you can afford to lose.
<a href="/terms/">Terms</a> &middot; <a href="/privacy/">Privacy</a> &middot;
<a href="/cookie-policy/">Cookies</a> &middot; <a href="/authors/">Authors</a> &middot;
<a href="/sitemap.xml">Sitemap</a></p>
</div>
</div></footer>'''


# ---------------------------------------------------------------- hero
DISCLOSURE_END = (
 '<div class="disclosure disclosure--end"><div class="wrap">' + ic("info") +
 '<p>We are an independent guide, not a casino. Some links on this page are affiliate links: if you open '
 'an account through one we may be paid a commission at no cost to you. Commission never buys a ranking '
 '&mdash; positions come from the tested scores set out in our '
 '<a href="/how-we-review/">review methodology</a>. 18+ only. Please gamble responsibly. '
 f'Last updated {UPDATED_H}.</p></div></div>')


def ticks():
    return ('<span class="ticks left" aria-hidden="true">' + '<i></i>' * 30 + '</span>'
            '<span class="ticks right" aria-hidden="true">' + '<i></i>' * 30 + '</span>')


def hero_html(fm, lede):
    a = AUTHORS[fm.get("author", "team")]
    rev = AUTHORS[fm["reviewer"]] if fm.get("reviewer") else None
    checked = (f' &middot; Fact-checked by <a href="{rev["url"]}">{rev["name"]}</a>' if rev else "")
    meta = (f'<div class="meta-line">{avatar(a, "av", 34)}'
            f'Written by <a href="{a["url"]}">{a["name"]}</a>{checked} '
            f'&middot; Updated <time datetime="{UPDATED}">{UPDATED_H}</time></div>')

    if fm.get("hero") == "poster":
        badges = ""
        if fm.get("facts"):
            badges = ('<div class="badges">' +
                      "".join(f'<span class="badge">{strip_tags(f)}</span>' for f in fm["facts"]) +
                      '</div>')
        offers = ""
        if fm.get("heroOffers"):
            ho = fm["heroOffers"]
            if ho == "auto":
                ho = DEFAULT_ORDER[:3]
            cards = ""
            for n, sl in enumerate(ho, 1):
                op = OPS.get(sl)
                if not op:
                    continue
                href = html.escape(aff(sl), quote=True)
                lbl = ("Top pick" if n == 1 else
                       f"#{n} &middot; {op.get('bestFor','')}" if op.get("bestFor") else f"#{n}")
                cards += (
                  f'<div class="ho-card">'
                  f'<span class="ho-rank">{lbl}</span>'
                  f'<img class="ho-logo" src="{logo_for(sl)}" alt="{strip_tags(op["name"])} logo" '
                  f'loading="eager" width="92" height="34">'
                  f'<span class="ho-bonus">{op.get("welcome","")}</span>'
                  f'<a class="cta-btn" href="{href}" rel="sponsored nofollow noopener" target="_blank">'
                  f'Get bonus</a>'
                  f'<span class="ho-tc">18+ &middot; T&amp;Cs apply &middot; {op.get("wagering","")}</span>'
                  f'</div>')
            if cards:
                offers = ('<div class="hero-offers"><span class="ho-head">Today&rsquo;s top welcome '
                          'offers for New Zealand players</span>'
                          f'<div class="ho-grid">{cards}</div></div>')

        ctas = ""
        if fm.get("cta"):
            prim, sec = fm["cta"]
            ctas = (f'<div class="hero-cta"><a class="cta-btn" href="{prim[1]}">{prim[0]}</a>'
                    f'<a class="cta-ghost" href="{sec[1]}">{sec[0]}</a></div>')
        return f'''<section class="hero hero--poster">{ticks()}<div class="wrap">
<div class="hero-meta"><span>Aotearoa &middot; New Zealand</span><span>41&deg;S &middot; 174&deg;E &mdash; Est. 2026</span></div>
<p class="wordmark">{BRAND_A.title()}<em>{BRAND_B.title()}</em><span class="dot">.</span></p>
<p class="hero-tagline">{POSTER_TAGLINE}</p>
<h1>{fm["h1"]}</h1>
<p class="lede">{lede}</p>
{offers}
{ctas}{badges}
{meta}
</div></section>'''

    crumbs = ""
    if fm.get("crumbs"):
        parts = ['<a href="/">Home</a>']
        for i, (n, h) in enumerate(fm["crumbs"]):
            parts.append('<span>&rsaquo;</span>')
            parts.append(f'<span>{n}</span>' if i == len(fm["crumbs"]) - 1 else f'<a href="{h}">{n}</a>')
        crumbs = f'<nav class="crumbs" aria-label="Breadcrumb">{"".join(parts)}</nav>'
    facts = ""
    if fm.get("facts"):
        facts = ('<div class="hero-facts">' +
                 "".join(f'<span class="hero-fact">{f}</span>' for f in fm["facts"]) + '</div>')
    return f'''<section class="hero hero--page">{ticks()}<div class="wrap">
{crumbs}<h1>{fm["h1"]}</h1>
<p class="lede">{lede}</p>{facts}
{meta}
</div></section>'''


# ---------------------------------------------------------------- leaderboard
def rating10(slug):
    return round(float(OPS.get(slug, {}).get("rating", 4.0)) * 2, 1)

def stars(r10):
    full = int(round(r10 / 2))
    return "&#9733;" * full + "&#9734;" * (5 - full)


_take_n = [0]

def avatar(a, cls, px):
    """Author avatar: a portrait where we have one, initials where we do not."""
    if a.get("photo"):
        p = a["photo"]
        return (f'<img class="{cls}" src="{p}" srcset="{p} 1x, {p.replace(".jpg", "@2x.jpg")} 2x" '
                f'alt="{strip_tags(html.unescape(a["name"]))}" width="{px}" height="{px}" loading="lazy" decoding="async">')
    return f'<span class="{cls}" aria-hidden="true">{a["initials"]}</span>'


def take_block(author, text):
    """A first-person note from the page's author. Plain prose, no panel.

    Long notes clamp to two lines with a CSS-only Read more toggle; short ones
    render as-is, so we never show a toggle that reveals nothing."""
    if not text:
        return ""
    plain = re.sub(r"\s+", " ", strip_tags(html.unescape(text))).strip()
    paras = [p.strip() for p in re.split(r"(?:<br\s*/?>\s*){2,}", text) if p.strip()]
    body = "".join(f"<p>{p}</p>" for p in paras)
    by = (f'<p class="take-by">{author["name"]} &middot; {author["short"]}</p>')

    if len(plain) <= 190:
        return f'<div class="take">{by}<div class="take-text is-short">{body}</div></div>'

    _take_n[0] += 1
    tid = f"tk{_take_n[0]}"
    return (f'<div class="take">{by}'
            f'<input type="checkbox" id="{tid}" class="take-cb">'
            f'<div class="take-text">{body}</div>'
            f'<label class="take-more" for="{tid}"></label></div>')

def leaderboard(slugs, heading="", intro="", sports=False, start=1, author=None):
    rows = []
    for i, slug in enumerate(slugs, start):
        op = OPS.get(slug)
        if not op:
            MISSING.add(slug); continue
        r10  = rating10(slug)
        r5   = round(float(op.get("rating", 4)), 1)
        href = html.escape(aff(slug, "sports" if sports else "casino"), quote=True)
        name = op["name"]
        top  = " is-top" if i == 1 else ""
        label = ("Editor&rsquo;s #1" if i == 1 else "Runner-up" if i == 2
                 else "Great value" if i == 3 else f"#{i}")
        badge_cls = "top" if i == 1 else ("" if i == 2 else "num")

        # one-line identity under the brand name, used on the mobile card
        meta = " &middot; ".join(x for x in [
            op.get("bestFor"), op.get("licenceShort"),
            (op.get("pokies") + " pokies") if op.get("pokies") else None] if x)

        pills = []
        if op.get("payoutFast"):  pills.append(f'<span class="afl-pill">{op["payoutFast"]} payouts</span>')
        if op.get("capDaily"):    pills.append(f'<span class="afl-pill">{op["capDaily"]}/day cap</span>')
        wag = re.search(r"\d+x", str(op.get("wagering", "")))
        if wag:                   pills.append(f'<span class="afl-pill warn">{wag.group(0)} wagering</span>')
        pills.append('<span class="afl-pill">NZD accepted</span>')

        # terms strip under the button
        w = op.get("welcome", "").lower()
        dep = next((f"{n.capitalize()} deposits" for n in
                    ("two", "three", "four", "five") if n + " deposit" in w), None)
        terms = " &middot; ".join(x for x in [
            dep,
            (wag.group(0) + " wagering") if wag else None,
            (op.get("minDep") + " min deposit") if op.get("minDep") else None] if x)

        offer = op.get("welcomeSports" if sports else "welcome") or op.get("welcome", "")
        rows.append(f'''<div class="afl-row{top}" id="op-{slug}">
<div class="afl-logo"><span class="afl-chip"><img class="oplogo" src="{logo_for(slug, sports)}" alt="{strip_tags(name)} logo" loading="lazy" decoding="async" width="96" height="44"></span>
<span class="afl-brandname"><a href="{review_url(slug)}">{name}</a></span>
<span class="afl-meta">{meta}</span></div>
<div class="afl-body">
<div class="afl-top"><span class="afl-rank">{i:02d}</span><span class="afl-badge {badge_cls}">{label}</span></div>
<div class="afl-score"><div class="afl-bar"><span style="width:{min(99, int(r10 * 10))}%"></span></div>
<div class="afl-scorerow"><span>Our score</span><b>{r10}/10</b></div></div>
<div class="afl-bonus"><span class="afl-bonus-l">Welcome offer</span><span class="afl-bonus-v">{offer}</span></div>
<div class="afl-feats">{"".join(pills)}<span class="afl-stars">{stars(r10)}<b>{r5}/5</b></span></div>
</div>
<div class="afl-cta"><a class="cta-btn" href="{href}" rel="sponsored nofollow noopener" target="_blank">Get bonus</a>
<a class="afl-rev" href="{review_url(slug)}">Read review</a>
<span class="afl-terms">{terms}{" &middot; " if terms else ""}18+ T&amp;Cs apply</span>
<span class="afl-tc">18+ &middot; T&amp;Cs apply</span></div>
</div>''')
    if not rows:
        return ""
    head = f'<h2 id="{slugify(heading)}">{heading}</h2>' if heading else ""
    head += take_block(author or AUTHORS["team"], intro) if intro else ""
    return f'<div class="lb-block">{head}<div class="afl-list">{"".join(rows)}</div></div>'


def cta_band(slug, heading, body, sports=False):
    op = OPS.get(slug)
    if not op:
        MISSING.add(slug); return ""
    href = html.escape(aff(slug, "sports" if sports else "casino"), quote=True)
    return f'''<div class="band"><h3>{heading}</h3><p>{body}</p>
<a class="cta-btn" href="{href}" rel="sponsored nofollow noopener" target="_blank">Claim at {op['name']}</a>
<a class="cta-ghost" href="{review_url(slug)}">Read our review</a>
<span class="band-terms">18+. New customers only. Wagering and full terms apply &mdash; read them before you deposit.
Gamble responsibly: Gambling Helpline 0800 654 655.</span></div>'''

# ---------------------------------------------------------------- shortcodes
def expand_shortcodes(body, author):
    def _top(m):
        parts = m.group(1).split("|")
        spec = parts[0].strip()
        if spec.startswith("top:"):
            slugs = DEFAULT_ORDER[:int(spec[4:])]
        else:
            slugs = [s.strip() for s in spec.split(",") if s.strip()]
        heading = parts[1].strip() if len(parts) > 1 else ""
        intro   = parts[2].strip() if len(parts) > 2 else ""
        sports  = len(parts) > 3 and parts[3].strip() == "sports"
        return leaderboard(slugs, heading, intro, sports, author=author)
    body = re.sub(r"<!--TOPLIST\s+(.*?)-->", _top, body, flags=re.S)

    def _cta(m):
        parts = m.group(1).split("|")
        return cta_band(parts[0].strip(),
                        parts[1].strip() if len(parts) > 1 else "Ready to play?",
                        parts[2].strip() if len(parts) > 2 else "",
                        len(parts) > 3 and parts[3].strip() == "sports")
    body = re.sub(r"<!--CTA\s+(.*?)-->", _cta, body, flags=re.S)

    def _cmp(m):
        parts = m.group(1).split("|")
        colkeys = parts[0].strip()
        caption = parts[1].strip() if len(parts) > 1 else ""
        slugs = ([s.strip() for s in parts[2].split(",") if s.strip()]
                 if len(parts) > 2 and parts[2].strip() else DEFAULT_ORDER)
        return cmp_table(colkeys, caption, slugs)
    body = re.sub(r"<!--CMPTABLE\s+(.*?)-->", _cmp, body, flags=re.S)

    body = re.sub(r"<!--TAKE\s+(.*?)-->",
                  lambda m: take_block(author, m.group(1).strip()), body, flags=re.S)

    body = re.sub(r"<!--SNIPPET\s+(.*?)-->",
                  lambda m: f'<div class="snippet">{m.group(1).strip()}</div>', body, flags=re.S)
    body = re.sub(r"<!--CARDGRID\s+(.*?)-->", _cardgrid, body, flags=re.S)
    return body


def _cardgrid(m):
    cards = ""
    for item in m.group(1).split(";;"):
        bits = [b.strip() for b in item.split("|")]
        if len(bits) < 3:
            continue
        href, title, desc = bits[0], bits[1], bits[2]
        cards += f'<a href="{href}"><span class="t">{title}</span><span class="d">{desc}</span></a>'
    return f'<div class="cardgrid">{cards}</div>' if cards else ""

# ---------------------------------------------------------------- TOC + anchors
def add_anchors_and_toc(body, want_toc):
    items = []
    def _h2(m):
        attrs, text = m.group(1), m.group(2)
        if 'id=' in attrs:
            i = re.search(r'id="([^"]+)"', attrs).group(1)
        else:
            i = slugify(text)
            attrs = f' id="{i}"' + attrs
        items.append((i, strip_tags(text)))
        return f'<h2{attrs}>{text}</h2>'
    body = re.sub(r'<h2([^>]*)>(.*?)</h2>', _h2, body, flags=re.S)

    def _h3(m):
        attrs, text = m.group(1), m.group(2)
        if 'id=' not in attrs:
            attrs = f' id="{slugify(text)}"' + attrs
        return f'<h3{attrs}>{text}</h3>'
    body = re.sub(r'<h3([^>]*)>(.*?)</h3>', _h3, body, flags=re.S)

    if not want_toc or len(items) < 4:
        return body, ""
    lis = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in items)
    return body, ('<nav class="toc" aria-label="On this page"><strong>On this page</strong>'
                  f'<ol>{lis}</ol></nav>')

# ---------------------------------------------------------------- schema
def faq_schema(body):
    qs = re.findall(r'<details class="faq-i"[^>]*>\s*<summary>(.*?)</summary>\s*'
                    r'<div class="faq-a">(.*?)</div>\s*</details>', body, flags=re.S)
    if not qs:
        return None
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip_tags(html.unescape(q)).strip(),
         "acceptedAnswer": {"@type": "Answer",
                            "text": re.sub(r"\s+", " ", strip_tags(html.unescape(a))).strip()}}
        for q, a in qs]}

def author_ref(a):
    """Schema @id for a byline. The collective byline resolves to the Organization."""
    if a["slug"] == "editorial-team":
        return {"@id": f"{DOMAIN}/#organization"}
    return {"@id": f"{DOMAIN}/authors/{a['slug']}/#person"}

def person_node(a):
    if a["slug"] == "editorial-team":
        return None
    n = {"@type": "Person", "@id": f"{DOMAIN}/authors/{a['slug']}/#person",
         "name": strip_tags(html.unescape(a["name"])), "url": DOMAIN + a["url"],
         "jobTitle": strip_tags(html.unescape(a["job"])),
         "description": strip_tags(html.unescape(a["bio"])),
         "knowsAbout": a["knows"],
         "worksFor": {"@id": f"{DOMAIN}/#organization"}}
    if a.get("sameAs"):
        n["sameAs"] = a["sameAs"]
    return n

ORG = {
 "@type": "Organization", "@id": f"{DOMAIN}/#organization", "name": SITE, "url": DOMAIN + "/",
 "logo": {"@type": "ImageObject", "url": f"{DOMAIN}/favicon-192x192.png", "width": 192, "height": 192},
 "email": EMAIL,
 "description": "Independent New Zealand guide to online pokies, casinos and betting, with real-money testing of every site listed.",
 "areaServed": {"@type": "Country", "name": "New Zealand"},
 "knowsAbout": ["online pokies", "online casinos", "New Zealand gambling law", "responsible gambling"],
 "publishingPrinciples": f"{DOMAIN}/how-we-review/",
 "ethicsPolicy": f"{DOMAIN}/about/",
 "contactPoint": {"@type": "ContactPoint", "contactType": "editorial", "email": EMAIL,
                  "availableLanguage": ["en-NZ"], "areaServed": "NZ"},
}
WEBSITE = {
 "@type": "WebSite", "@id": f"{DOMAIN}/#website", "url": DOMAIN + "/", "name": SITE,
 "inLanguage": "en-NZ", "publisher": {"@id": f"{DOMAIN}/#organization"},
 "potentialAction": {"@type": "SearchAction",
   "target": {"@type": "EntryPoint", "urlTemplate": DOMAIN + "/?s={search_term_string}"},
   "query-input": "required name=search_term_string"},
}

def casino_id(slug):
    """One stable @id per operator, referenced from every ranked list and its review."""
    return DOMAIN + review_url(slug) + "#casino"


def money(v):
    m = re.search(r"([\d,.]+)", str(v or ""))
    return float(m.group(1).replace(",", "")) if m else None


def offer_node(slug, sports=False):
    """The welcome bonus as shown on the offer card. Min deposit is modelled as
    eligibleTransactionVolume, which is what it actually is: a qualifying spend."""
    op = OPS[slug]
    txt = op.get("welcomeSports" if sports else "welcome") or op.get("welcome", "")
    if not txt:
        return None
    o = {"@type": "Offer",
         "name": "Welcome bonus",
         "category": "Welcome bonus",
         "description": strip_tags(html.unescape(txt)),
         "url": DOMAIN + review_url(slug),
         "eligibleRegion": {"@type": "Country", "name": "New Zealand"},
         "seller": {"@id": casino_id(slug)}}
    dep = money(op.get("minDep"))
    if dep:
        o["eligibleTransactionVolume"] = {
            "@type": "PriceSpecification", "minPrice": dep, "priceCurrency": "NZD"}
    return o


def casino_node(slug, sports=False):
    """Full Organization node for an operator, matching the offer card's fields."""
    op = OPS[slug]
    n = {"@type": "Organization", "@id": casino_id(slug), "name": strip_tags(op["name"]),
         "url": DOMAIN + review_url(slug),
         "areaServed": {"@type": "Country", "name": "New Zealand"}}
    if op.get("usp"):
        n["description"] = strip_tags(html.unescape(op["usp"]))
    if op.get("logo"):
        n["logo"] = DOMAIN + logo_for(slug, sports)
    props = [("Licence", op.get("licenceShort")),
             ("Pokies", op.get("pokies")),
             ("Withdrawal speed", op.get("payoutFast")),
             ("Daily withdrawal cap", op.get("capDaily")),
             ("Wagering requirement", op.get("wagering"))]
    props = [{"@type": "PropertyValue", "name": k, "value": strip_tags(html.unescape(str(v)))}
             for k, v in props if v]
    if props:
        n["additionalProperty"] = props
    off = offer_node(slug, sports)
    if off:
        n["makesOffer"] = off
    # our score is one editorial rating, so it belongs to the Review, never to a
    # fabricated aggregateRating
    n["review"] = {"@id": DOMAIN + review_url(slug) + "#review"}
    return n


def build_schema(fm, body, url, title, desc):
    a = AUTHORS[fm.get("author", "team")]
    page_url = DOMAIN + url
    graph = [ORG, WEBSITE]

    crumb_items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"}]
    for i, (n, h) in enumerate(fm.get("crumbs", []), 2):
        crumb_items.append({"@type": "ListItem", "position": i,
                            "name": strip_tags(html.unescape(n)),
                            "item": DOMAIN + (h if h else url)})
    if len(crumb_items) > 1:
        graph.append({"@type": "BreadcrumbList", "@id": page_url + "#breadcrumb", "itemListElement": crumb_items})

    ptype = fm.get("pagetype", "article")
    TYPEMAP = {"article": "Article", "webpage": "WebPage", "profilepage": "ProfilePage",
               "collection": "CollectionPage", "faq": "WebPage", "contact": "ContactPage",
               "about": "AboutPage"}
    page_node = {
        "@type": TYPEMAP.get(ptype, "WebPage"),
        "@id": page_url + "#page",
        "url": page_url,
        "name" if ptype != "article" else "headline": strip_tags(html.unescape(fm["h1"])),
        "description": strip_tags(html.unescape(desc)),
        "inLanguage": "en-NZ",
        "isPartOf": {"@id": f"{DOMAIN}/#website"},
        "datePublished": fm.get("published", PUBLISHED),
        "dateModified": UPDATED,
        "author": author_ref(a),
        "publisher": {"@id": f"{DOMAIN}/#organization"},
        "primaryImageOfPage": f"{DOMAIN}/favicon-512x512.png",
    }
    if len(crumb_items) > 1:
        page_node["breadcrumb"] = {"@id": page_url + "#breadcrumb"}
    if fm.get("reviewer"):
        page_node["reviewedBy"] = author_ref(AUTHORS[fm["reviewer"]])
    if ptype == "profilepage":
        page_node["mainEntity"] = author_ref(a)
    graph.append(page_node)
    for who in [a] + ([AUTHORS[fm["reviewer"]]] if fm.get("reviewer") else []):
        node = person_node(who)
        if node and not any(n.get("@id") == node["@id"] for n in graph):
            graph.append(node)

    f = faq_schema(body)
    if f:
        f["@id"] = page_url + "#faq"
        f["isPartOf"] = {"@id": page_url + "#page"}
        graph.append(f)

    if fm.get("itemlist"):
        il = DEFAULT_ORDER[:10] if fm["itemlist"] == "auto" else fm["itemlist"]
        il = [x for x in il if x in OPS]
        sportsl = bool(fm.get("sports"))
        graph.append({
            "@type": "ItemList", "@id": page_url + "#itemlist",
            "name": strip_tags(html.unescape(fm["h1"])),
            "itemListOrder": "https://schema.org/ItemListOrderDescending",
            "numberOfItems": len(il),
            "isPartOf": {"@id": page_url + "#page"},
            "itemListElement": [
                {"@type": "ListItem", "position": i,
                 "url": DOMAIN + review_url(x),
                 "item": casino_node(x, sportsl)}
                for i, x in enumerate(il, 1)]})

    if fm.get("review"):
        s = fm["review"]; op = OPS[s]
        graph.append({
            "@type": "Review", "@id": page_url + "#review",
            "itemReviewed": casino_node(s),
            "url": page_url,
            "isPartOf": {"@id": page_url + "#page"},
            "reviewRating": {"@type": "Rating", "ratingValue": rating10(s),
                             "bestRating": 10, "worstRating": 1},
            "author": author_ref(a),
            "publisher": {"@id": f"{DOMAIN}/#organization"},
            "datePublished": fm.get("published", PUBLISHED),
            "reviewBody": strip_tags(html.unescape(op.get("verdict", op.get("usp", "")))),
            "positiveNotes": {"@type": "ItemList", "itemListElement": [
                {"@type": "ListItem", "position": i, "name": strip_tags(html.unescape(p))}
                for i, p in enumerate(op.get("pros", []), 1)]},
            "negativeNotes": {"@type": "ItemList", "itemListElement": [
                {"@type": "ListItem", "position": i, "name": strip_tags(html.unescape(c))}
                for i, c in enumerate(op.get("cons", []), 1)]},
        })

    for extra in fm.get("schema", []):
        graph.append(extra)

    return json.dumps({"@context": "https://schema.org", "@graph": graph},
                      ensure_ascii=False, separators=(",", ":"))


# ---------------------------------------------------------------- related links
# A contextual "keep reading" module rendered on every page. Hand-mapped rather
# than generated, so each link is topically justified — but the set is chosen to
# balance the inbound graph, which is why the thinner pages appear here often.
RELATED = {
 "/": [("/online-pokies/","Online Pokies NZ","The games worth playing and the RTP each site serves"),
       ("/best-online-casinos/","Best Online Casinos","All 16 ranked on the published weighting"),
       ("/fast-payout-casinos/","Fast Payout Casinos","48 withdrawals timed on our own accounts"),
       ("/online-casinos/bonuses/","Casino Bonuses","Every offer priced by what it costs to clear"),
       ("/nz-online-casino-law/","NZ Casino Law","The 2026 Act and the licensing deadlines"),
       ("/pub-pokies-vs-online-pokies/","Pub Pokies vs Online","The $2.50 cap nobody else mentions")],
 "/online-pokies/": [("/highest-rtp-pokies/","Highest RTP Pokies","Verified returns, not press releases"),
       ("/megaways-pokies/","Megaways Pokies","117,649 ways and what they cost"),
       ("/jackpot-pokies/","Jackpot Pokies","What the jackpot takes from your return"),
       ("/free-pokies/","Free Pokies","Demo play, and how to check a site's RTP free"),
       ("/mobile-pokies/","Mobile Pokies","Tested on 4G, not on a flagship"),
       ("/pokies-glossary/","Pokies Glossary","Every term, plainly")],
 "/best-online-casinos/": [("/high-payout-casinos/","High Payout Casinos","Both halves of payout, measured"),
       ("/fast-payout-casinos/","Fast Payout Casinos","Who actually paid us quickest"),
       ("/live-casinos/","Live Dealer Casinos","Tables staffed in NZ evening hours"),
       ("/minimum-deposit-casinos/","Minimum Deposit Casinos","What NZ$10 and NZ$20 really buy"),
       ("/casino-reviews/","All 16 Reviews","Tested with our own money, cons included"),
       ("/how-we-review/","How We Review","The weighting, and what disqualifies a site")],
 "/fast-payout-casinos/": [("/withdrawal-times/","Withdrawal Times","The full timing log by method and operator"),
       ("/payment-methods/","Payment Methods","What works from NZ in 2026"),
       ("/best-crypto-casinos/","Crypto Casinos","The fastest rail, and the IRD catch"),
       ("/high-payout-casinos/","High Payout Casinos","The ceiling that caps a fast payout"),
       ("/casino-complaints/","Complaints & Disputes","When to escalate, and how"),
       ("/best-online-casinos/","Best Online Casinos","The full ranking")],
 "/high-payout-casinos/": [("/highest-rtp-pokies/","Highest RTP Pokies","The titles and the builds sites deploy"),
       ("/fast-payout-casinos/","Fast Payout Casinos","Speed, measured"),
       ("/jackpot-pokies/","Jackpot Pokies","Why progressives return 88%"),
       ("/live-casinos/","Live Dealer Casinos","Blackjack at 99.3%"),
       ("/withdrawal-times/","Withdrawal Times","How long a big win takes to clear"),
       ("/best-online-casinos/","Best Online Casinos","The full ranking")],
 "/best-crypto-casinos/": [("/payment-methods/","Payment Methods","Every rail compared"),
       ("/gambling-winnings-tax-nz/","Tax on Winnings","Cryptoassets are property, not currency"),
       ("/fast-payout-casinos/","Fast Payout Casinos","Where crypto sits against the alternatives"),
       ("/withdrawal-times/","Withdrawal Times","Approval clock vs settlement clock"),
       ("/best-online-casinos/","Best Online Casinos","The full ranking"),
       ("/online-casinos/","All Casino Guides","Every category in one place")],
 "/live-casinos/": [("/high-payout-casinos/","High Payout Casinos","House edge by game type"),
       ("/online-casinos/bonuses/","Casino Bonuses","Why tables count 10% or nothing"),
       ("/mobile-pokies/","Mobile Play","Streaming a live table on 4G"),
       ("/best-online-casinos/","Best Online Casinos","The full ranking"),
       ("/online-casinos/","All Casino Guides","Every category in one place"),
       ("/free-pokies/","Free Play","Try the lobby before you deposit")],
 "/online-casinos/bonuses/": [("/wagering-requirements/","Wagering Requirements","The arithmetic, worked"),
       ("/no-deposit-casinos/","No Deposit Bonuses","Free to try, capped by design"),
       ("/free-spins/","Free Spins","The four numbers that decide the value"),
       ("/minimum-deposit-casinos/","Minimum Deposit Casinos","Whether a bonus is worth it on NZ$20"),
       ("/highest-rtp-pokies/","Highest RTP Pokies","Which titles bonuses exclude, and why"),
       ("/best-online-casinos/","Best Online Casinos","The full ranking")],
 "/no-deposit-casinos/": [("/free-spins/","Free Spins","What a spins offer is actually worth"),
       ("/online-casinos/bonuses/","Casino Bonuses","Every offer priced"),
       ("/wagering-requirements/","Wagering Requirements","Why 50x makes an offer unclearable"),
       ("/minimum-deposit-casinos/","Minimum Deposit Casinos","Usually better value than no deposit"),
       ("/free-pokies/","Free Pokies","Try a lobby at zero risk"),
       ("/best-online-casinos/","Best Online Casinos","The full ranking")],
 "/free-spins/": [("/online-casinos/bonuses/","Casino Bonuses","Every offer priced"),
       ("/no-deposit-casinos/","No Deposit Bonuses","Spins before any deposit"),
       ("/wagering-requirements/","Wagering Requirements","The maths behind the multiplier"),
       ("/highest-rtp-pokies/","Highest RTP Pokies","Check the locked title's real return"),
       ("/free-pokies/","Free Pokies","Demo play with no strings"),
       ("/online-casinos/","All Casino Guides","Every category in one place")],
 "/wagering-requirements/": [("/online-casinos/bonuses/","Casino Bonuses","Every offer priced by expected cost"),
       ("/free-spins/","Free Spins","Wagering on spin winnings"),
       ("/no-deposit-casinos/","No Deposit Bonuses","Where 50x and a win cap meet"),
       ("/live-casinos/","Live Dealer Casinos","Why tables are weighted at 10%"),
       ("/pokies-glossary/","Pokies Glossary","Every term, plainly"),
       ("/best-online-casinos/","Best Online Casinos","The full ranking")],
 "/minimum-deposit-casinos/": [("/free-spins/","Free Spins","Better value than a small match"),
       ("/no-deposit-casinos/","No Deposit Bonuses","Free, and capped"),
       ("/highest-rtp-pokies/","Highest RTP Pokies","Stretching a small bankroll"),
       ("/payment-methods/","Payment Methods","Withdrawal floors by site"),
       ("/free-pokies/","Free Pokies","Play before you deposit"),
       ("/online-casinos/","All Casino Guides","Every category in one place")],
 "/highest-rtp-pokies/": [("/online-pokies/","Online Pokies NZ","The games and the maths"),
       ("/megaways-pokies/","Megaways Pokies","Why 97.7% is the ceiling there"),
       ("/jackpot-pokies/","Jackpot Pokies","Where 88% comes from"),
       ("/high-payout-casinos/","High Payout Casinos","Which sites serve the full builds"),
       ("/free-pokies/","Free Pokies","Check a build without depositing"),
       ("/pokies-glossary/","Pokies Glossary","RTP, volatility, hit frequency")],
 "/jackpot-pokies/": [("/highest-rtp-pokies/","Highest RTP Pokies","The opposite end of the trade"),
       ("/high-payout-casinos/","High Payout Casinos","Ceilings and the jackpot exemption"),
       ("/gambling-winnings-tax-nz/","Tax on Winnings","What happens after a large win"),
       ("/online-pokies/","Online Pokies NZ","Mechanics compared"),
       ("/megaways-pokies/","Megaways Pokies","The other high-variance format"),
       ("/online-casinos/","All Casino Guides","Every category in one place")],
 "/megaways-pokies/": [("/highest-rtp-pokies/","Highest RTP Pokies","White Rabbit at 97.7%"),
       ("/online-pokies/","Online Pokies NZ","Every mechanic compared"),
       ("/jackpot-pokies/","Jackpot Pokies","The other high-variance format"),
       ("/free-pokies/","Free Pokies","Demo 200 spins before committing"),
       ("/pokies-glossary/","Pokies Glossary","Cascades, multipliers, ways to win"),
       ("/minimum-deposit-casinos/","Minimum Deposit Casinos","Bankroll for 250 spins")],
 "/mobile-pokies/": [("/online-pokies/","Online Pokies NZ","The games worth playing"),
       ("/live-casinos/","Live Dealer Casinos","Streaming on 4G"),
       ("/free-pokies/","Free Pokies","Demo on a phone"),
       ("/payment-methods/","Payment Methods","Why in-app browsers break cashiers"),
       ("/best-online-casinos/","Best Online Casinos","The full ranking"),
       ("/pokies-glossary/","Pokies Glossary","Every term, plainly")],
 "/free-pokies/": [("/online-pokies/","Online Pokies NZ","When you are ready for real money"),
       ("/highest-rtp-pokies/","Highest RTP Pokies","Use demo to check the build"),
       ("/no-deposit-casinos/","No Deposit Bonuses","Real money at zero risk"),
       ("/megaways-pokies/","Megaways Pokies","Feel the variance for free"),
       ("/mobile-pokies/","Mobile Pokies","Demo on a phone"),
       ("/responsible-gambling/","Play Safe","What demo mode cannot teach you")],
 "/pokies-glossary/": [("/online-pokies/","Online Pokies NZ","The terms in context"),
       ("/highest-rtp-pokies/","Highest RTP Pokies","RTP explained properly"),
       ("/wagering-requirements/","Wagering Requirements","Bonus vocabulary"),
       ("/megaways-pokies/","Megaways Pokies","Cascades and ways to win"),
       ("/payment-methods/","Payment Methods","KYC, AML, ceilings"),
       ("/pub-pokies-vs-online-pokies/","Class 4 Explained","The NZ-specific terms")],
 "/payment-methods/": [("/withdrawal-times/","Withdrawal Times","How long each rail took us"),
       ("/best-crypto-casinos/","Crypto Casinos","The fastest option"),
       ("/fast-payout-casinos/","Fast Payout Casinos","Who paid quickest"),
       ("/minimum-deposit-casinos/","Minimum Deposit Casinos","Floors and qualifiers"),
       ("/casino-complaints/","Complaints & Disputes","When a payment goes wrong"),
       ("/online-casinos/","All Casino Guides","Every category in one place")],
 "/withdrawal-times/": [("/fast-payout-casinos/","Fast Payout Casinos","The ranked list"),
       ("/payment-methods/","Payment Methods","Every rail compared"),
       ("/high-payout-casinos/","High Payout Casinos","Ceilings, not just speed"),
       ("/casino-complaints/","Complaints & Disputes","When to escalate"),
       ("/best-crypto-casinos/","Crypto Casinos","Why crypto clears first"),
       ("/how-we-review/","How We Review","The timing protocol")],
 "/casino-complaints/": [("/withdrawal-times/","Withdrawal Times","What normal looks like"),
       ("/nz-online-casino-law/","NZ Casino Law","Who regulates what"),
       ("/online-casinos/bonuses/","Casino Bonuses","The clauses that void wins"),
       ("/how-we-review/","How We Review","What gets a site dropped"),
       ("/responsible-gambling/","Play Safe","Free confidential help"),
       ("/contact/","Report a Casino","We investigate every documented report")],
 "/nz-online-casino-law/": [("/gambling-winnings-tax-nz/","Tax on Winnings","The IRD position"),
       ("/online-betting/","Online Betting NZ","Why sport is different"),
       ("/pub-pokies-vs-online-pokies/","Pub Pokies vs Online","Class 4 rules compared"),
       ("/casino-complaints/","Complaints & Disputes","Your recourse today"),
       ("/responsible-gambling/","Play Safe","Limits and free help"),
       ("/best-online-casinos/","Best Online Casinos","Sites operating through the transition")],
 "/gambling-winnings-tax-nz/": [("/nz-online-casino-law/","NZ Casino Law","The 2026 licensing regime"),
       ("/best-crypto-casinos/","Crypto Casinos","Where the property rules bite"),
       ("/jackpot-pokies/","Jackpot Pokies","After a very large win"),
       ("/high-payout-casinos/","High Payout Casinos","Getting a big win out"),
       ("/online-betting/","Online Betting NZ","Betting winnings too"),
       ("/online-casinos/","All Casino Guides","Every category in one place")],
 "/pub-pokies-vs-online-pokies/": [("/online-pokies/","Online Pokies NZ","The online product in full"),
       ("/nz-online-casino-law/","NZ Casino Law","Class 4 and the 2026 Act"),
       ("/responsible-gambling/","Play Safe","Supplying your own limits"),
       ("/highest-rtp-pokies/","Highest RTP Pokies","The six-point return gap"),
       ("/pokies-glossary/","Pokies Glossary","Class 4 and the rest"),
       ("/best-online-casinos/","Best Online Casinos","The full ranking")],
 "/online-betting/": [("/best-sports-betting-sites/","Sports Betting Sites","Who can lawfully take a bet"),
       ("/nz-online-casino-law/","NZ Casino Law","The other regime"),
       ("/gambling-winnings-tax-nz/","Tax on Winnings","Betting winnings are untaxed too"),
       ("/best-online-casinos/","Best Online Casinos","What is lawful for you"),
       ("/responsible-gambling/","Play Safe","Free confidential help"),
       ("/online-casinos/","All Casino Guides","Every category in one place")],
 "/best-sports-betting-sites/": [("/online-betting/","Online Betting NZ","The law in full"),
       ("/nz-online-casino-law/","NZ Casino Law","The casino regime"),
       ("/best-online-casinos/","Best Online Casinos","Where you can lawfully play"),
       ("/gambling-winnings-tax-nz/","Tax on Winnings","No tax either way"),
       ("/responsible-gambling/","Play Safe","Limits and free help"),
       ("/live-casinos/","Live Dealer Casinos","If you want something to watch")],
 "/online-casinos/": [("/best-online-casinos/","Best Online Casinos","The full ranking"),
       ("/online-pokies/","Online Pokies NZ","The games worth playing"),
       ("/casino-reviews/","All 16 Reviews","Tested with our own money"),
       ("/free-spins/","Free Spins","Offers priced honestly"),
       ("/pokies-glossary/","Pokies Glossary","Every term, plainly"),
       ("/how-we-review/","How We Review","The method behind every score")],
 "/casino-reviews/": [("/best-online-casinos/","Best Online Casinos","The ranking these come from"),
       ("/how-we-review/","How We Review","Weights and disqualifiers"),
       ("/fast-payout-casinos/","Fast Payout Casinos","Who paid quickest"),
       ("/high-payout-casinos/","High Payout Casinos","Ceilings compared"),
       ("/online-casinos/","All Casino Guides","Every category in one place"),
       ("/casino-complaints/","Complaints & Disputes","If a site will not pay")],
 "/how-we-review/": [("/best-online-casinos/","Best Online Casinos","The method applied"),
       ("/casino-reviews/","All 16 Reviews","Every operator tested"),
       ("/authors/","Our Authors","Who does the work"),
       ("/withdrawal-times/","Withdrawal Times","The timing protocol in practice"),
       ("/highest-rtp-pokies/","Highest RTP Pokies","The RTP sample explained"),
       ("/about/","About Us","How we are funded")],
 "/responsible-gambling/": [("/pub-pokies-vs-online-pokies/","Pub Pokies vs Online","Where the brakes went"),
       ("/free-pokies/","Free Pokies","Play with no money at stake"),
       ("/minimum-deposit-casinos/","Minimum Deposit Casinos","Keeping stakes small"),
       ("/nz-online-casino-law/","NZ Casino Law","Harm rules under the 2026 Act"),
       ("/about/","About Us","What we will not publish"),
       ("/contact/","Contact Us","Getting in touch")],
 "/about/": [("/how-we-review/","How We Review","The scoring in full"),
       ("/authors/","Our Authors","Who writes this"),
       ("/contact/","Contact Us","Corrections and reports"),
       ("/responsible-gambling/","Play Safe","Free confidential help"),
       ("/best-online-casinos/","Best Online Casinos","The rankings themselves"),
       ("/terms/","Terms and Conditions","Including our affiliate disclosure")],
 "/contact/": [("/casino-complaints/","Complaints & Disputes","The escalation route"),
       ("/about/","About Us","Who we are"),
       ("/authors/","Our Authors","The editorial team"),
       ("/how-we-review/","How We Review","Our methodology"),
       ("/responsible-gambling/","Play Safe","Free confidential help"),
       ("/privacy/","Privacy Policy","What we do with what you send us")],
 "/authors/": [("/about/","About Us","How the site is funded"),
       ("/how-we-review/","How We Review","The method they apply"),
       ("/contact/","Contact Us","Corrections welcome"),
       ("/best-online-casinos/","Best Online Casinos","Their rankings"),
       ("/nz-online-casino-law/","NZ Casino Law","Charlotte's coverage"),
       ("/withdrawal-times/","Withdrawal Times","Nikau's timing log")],
}
# author profiles and legal pages share a compact set
_COMPANY = [("/about/","About Us","Who we are and how we are funded"),
            ("/authors/","Our Authors","The editorial team"),
            ("/how-we-review/","How We Review","The method behind every score"),
            ("/contact/","Contact Us","Corrections and casino reports"),
            ("/responsible-gambling/","Play Safe","Free confidential help in NZ"),
            ("/best-online-casinos/","Best Online Casinos","The rankings")]
for _u in ["/authors/nikau-te-aho/", "/authors/charlotte-wilson/"]:
    RELATED[_u] = _COMPANY

# the legal pages cross-link each other so none of them sits one body link deep
_LEGAL = {
 "/terms/":         [("/privacy/","Privacy Policy","How we handle personal information"),
                     ("/cookie-policy/","Cookie Policy","What we set, and how to refuse it")],
 "/privacy/":       [("/cookie-policy/","Cookie Policy","Including the affiliate tracking cookie"),
                     ("/terms/","Terms and Conditions","What this site is, and is not")],
 "/cookie-policy/": [("/privacy/","Privacy Policy","How we handle personal information"),
                     ("/terms/","Terms and Conditions","What this site is, and is not")],
}
for _u, _pair in _LEGAL.items():
    RELATED[_u] = _pair + [
        ("/about/", "About Us", "Who we are and how we are funded"),
        ("/how-we-review/", "How We Review", "The method behind every score"),
        ("/responsible-gambling/", "Play Safe", "Free confidential help in NZ"),
        ("/contact/", "Contact Us", "Corrections and casino reports")]


def related_html(url):
    """Contextual cross-links. Review pages get siblings plus the key guides."""
    items = RELATED.get(url)
    if items is None and url.startswith("/casino-reviews/") and url != "/casino-reviews/":
        slug = url.strip("/").split("/")[-1]
        order = DEFAULT_ORDER
        i = order.index(slug) if slug in order else 0
        sibs = [order[(i + n) % len(order)] for n in (1, 2, 3)]
        items = [(review_url(s), OPS[s]["name"] + " review",
                  OPS[s].get("bestFor", "Tested with our own money")) for s in sibs]
        items += [("/casino-reviews/", "All 16 Reviews", "Every operator we tested"),
                  ("/best-online-casinos/", "Best Online Casinos", "The full ranking"),
                  ("/how-we-review/", "How We Review", "Weights and disqualifiers")]
    if not items:
        return ""
    cards = "".join(
        f'<a href="{h}"><span class="t">{t}</span><span class="d">{d}</span></a>'
        for h, t, d in items)
    return (f'<h2 id="keep-reading">Keep reading</h2>'
            f'<div class="cardgrid">{cards}</div>')


# ---------------------------------------------------------------- page shell
FAVICONS = '''<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-48x48.png" sizes="48x48" type="image/png">
<link rel="icon" href="/favicon-96x96.png" sizes="96x96" type="image/png">
<link rel="icon" href="/favicon-144x144.png" sizes="144x144" type="image/png">
<link rel="icon" href="/favicon-192x192.png" sizes="192x192" type="image/png">
<link rel="shortcut icon" href="/favicon.ico">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">'''

FONTS = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Syncopate:wght@400;700&display=swap" rel="stylesheet">'''

RG_BLOCK = '''<div class="rg">
<h3>Responsible gambling &mdash; play it safe, Kiwi</h3>
<p>Gambling is entertainment, never a way to make money or escape stress. Set a deposit limit before you
play rather than during a bad run, never chase a loss, and stop when it stops being fun. Every site we
list offers deposit limits, loss limits, reality checks, time-outs and self-exclusion &mdash; use them.</p>
<p>If gambling is causing harm to you or someone you care about, free and confidential help is available
in New Zealand, 24 hours a day. You do not need to be in crisis to call, and support is there for family
and wh&#257;nau too.</p>
<ul>
<li><strong>Gambling Helpline Aotearoa</strong> &mdash; call <a href="tel:0800654655">0800 654 655</a> or free text <strong>8006</strong></li>
<li><strong>Problem Gambling Foundation</strong> &mdash; <a href="tel:0800664262">0800 664 262</a>, free counselling including kaupapa M&#257;ori, Pasifika and Asian services</li>
<li><strong>Need to Talk</strong> &mdash; call or text <a href="tel:1737">1737</a> to reach a trained counsellor any time</li>
<li><strong>Safer Gambling Aotearoa</strong> &mdash; <a href="https://www.safergambling.org.nz/" rel="nofollow noopener" target="_blank">safergambling.org.nz</a></li>
</ul>
<p style="margin-bottom:0"><span class="gc-18">18+</span> You must be at least 18 to gamble online in
New Zealand (20+ for land-based casinos). Read our <a href="/responsible-gambling/">responsible gambling guide</a>.</p>
</div>'''

def render(fm, body):
    url   = fm["url"]
    title = fm["title"]
    desc  = fm["desc"]
    canonical = DOMAIN + url
    lede  = fm.get("lede", desc)

    body = resolve_tokens(body)
    body = expand_shortcodes(body, AUTHORS[fm.get("author", "team")])
    body, toc = add_anchors_and_toc(body, fm.get("toc", True))
    schema = build_schema(fm, body, url, title, desc)

    og_img = f"{DOMAIN}/favicon-512x512.png"
    sticky = ""
    if fm.get("sticky"):
        sslug = fm["sticky"]; op = OPS.get(sslug)
        if op:
            href = html.escape(aff(sslug), quote=True)
            sticky = (f'<div class="sticky"><img src="{logo_for(sslug)}" alt="" width="44" height="30" loading="lazy">'
                      f'<span class="sticky-t"><b>{op["name"]}</b>{op.get("bestFor","Our #1 pick")}</span>'
                      f'<a class="cta-btn" href="{href}" rel="sponsored nofollow noopener" target="_blank">Visit</a></div>')

    rg = "" if fm.get("norg") else RG_BLOCK
    rel = related_html(url)

    return f'''<!DOCTYPE html>
<html lang="en-NZ">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="en-nz" href="{canonical}">
<link rel="alternate" hreflang="x-default" href="{canonical}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<meta name="rating" content="adult">
<meta name="author" content="{strip_tags(html.unescape(AUTHORS[fm.get('author','team')]['name']))}">
<meta name="geo.region" content="NZ">
<meta property="og:type" content="{'website' if fm.get('hero') == 'poster' else 'article'}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{SITE}">
<meta property="og:locale" content="en_NZ">
<meta property="og:image" content="{og_img}">
<meta property="article:modified_time" content="{UPDATED}T09:00:00+12:00">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_img}">
<meta name="theme-color" content="#07211D">
{FAVICONS}
{FONTS}
<link rel="stylesheet" href="/assets/css/site.css?v={CSS_V}">
<script type="application/ld+json">{schema}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{nav_html()}
{hero_html(fm, lede)}
<main id="main"><div class="wrap"><div class="content">
{"" if "<!--TOC-->" in body else toc}
{body.replace("<!--TOC-->", toc)}
{rel}
{rg}
</div></div></main>
{DISCLOSURE_END}
{foot_html()}
{sticky}
</body>
</html>
'''


# ---------------------------------------------------------------- run
def parse(path):
    raw = open(path, encoding="utf-8").read()
    m = re.match(r"\s*<!--@(.*?)@-->", raw, flags=re.S)
    if not m:
        raise SystemExit(f"no front matter in {path}")
    fm = json.loads(m.group(1))
    return fm, raw[m.end():]

def main():
    pages = []
    seen = {}
    for fn in sorted(os.listdir(SRC)):
        if not fn.endswith(".html"):
            continue
        fm, body = parse(os.path.join(SRC, fn))
        if fm["url"] in seen:
            raise SystemExit(f"duplicate URL {fm['url']}: {seen[fm['url']]} and {fn}")
        seen[fm["url"]] = fn
        out = os.path.join(ROOT, fm["url"].strip("/"), "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8").write(render(fm, body))
        # lastmod tracks the source fragment, not the build, so untouched pages
        # stop claiming a fresh date on every run
        lm = fm.get("updated") or datetime.date.fromtimestamp(
            os.path.getmtime(os.path.join(SRC, fn))).isoformat()
        pages.append((fm["url"], fm.get("priority", 0.7), fm.get("freq", "monthly"), lm))
        print(f"  {fm['url']:44} <- {fn}")

    # sitemap
    urls = "".join(
        f'<url><loc>{DOMAIN}{html.escape(u, quote=True)}</loc><lastmod>{lm}</lastmod>'
        f'<changefreq>{f}</changefreq><priority>{p:.1f}</priority></url>\n'
        for u, p, f, lm in sorted(pages, key=lambda x: (-x[1], x[0])))
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n')

    # robots
    blocked = ["AhrefsBot", "SemrushBot", "MJ12bot", "DotBot", "Rogerbot", "serpstatbot", "SistrixBot"]
    rb = ["# robots.txt for " + DOMAIN, "",
          "User-agent: *", "Allow: /", "Disallow: /_build/", "", "# SEO crawlers", ""]
    for b in blocked:
        rb += [f"User-agent: {b}", "Disallow: /", ""]
    rb += [f"Sitemap: {DOMAIN}/sitemap.xml", ""]
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write("\n".join(rb))

    print(f"\n{len(pages)} pages, sitemap.xml, robots.txt")
    if MISSING:
        print("MISSING affiliate links / slugs:", sorted(MISSING))

if __name__ == "__main__":
    main()
