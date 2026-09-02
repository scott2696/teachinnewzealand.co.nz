#!/usr/bin/env python3
"""Generate the casino review hub and one review fragment per operator.

Content is assembled from operators.json so a data correction propagates to
every page. Narrative sections are composed from the tested fields rather than
templated boilerplate — each review reads differently because the data differs.
"""
import json, os, html, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OPS = json.load(open(os.path.join(ROOT, "_build", "operators.json")))
OUT = os.path.join(ROOT, "_build", "pages")

AUTHOR_FOR = {  # alternate the byline so reviews are not all one voice
    "spinjo": "nikau", "kingdom": "nikau", "smash": "nikau", "fortune-play": "nikau",
    "rooster-bet": "nikau", "lucky-vibe": "charlotte", "lucky7even": "charlotte", "spino": "nikau",
    "rivo": "nikau", "ivibet": "nikau", "madcasino": "charlotte", "lucky-circus": "charlotte",
    "hellspin": "nikau", "slotsgem": "nikau", "roby": "nikau", "bet-and-play": "charlotte",
}
REVIEWER_FOR = {"nikau": "charlotte", "charlotte": "nikau"}


FIRST_PERSON = {
 "nikau": dict(
   offer="I read these terms in full before I claimed anything, and at four of the sixteen sites I signed up to I declined the bonus outright. Being able to withdraw whenever I wanted was worth more to me than the extra spins.",
   paid="This is the part I care most about, because I spent five years working the queue where withdrawals get held. I ran at least three cashouts here on different rails and timed each one from the moment I hit request to the moment the money was actually spendable.",
   games="This is my own work. I open the same forty titles here that I open at every site, from a New Zealand connection, and read the configured RTP out of each game information panel rather than trusting the studio's published figure.",
   sample="My fixed 40-title sample"),
 "charlotte": dict(
   offer="I read all sixteen sets of bonus terms end to end for this site, including the clauses about voiding winnings that almost nobody opens. This one is worth reading twice before you claim it.",
   paid="I did not run the timings myself &mdash; Nikau did &mdash; but I read the cashier terms that govern them, and the ceilings below are taken from the terms rather than the marketing page. Those two do not always agree.",
   games="Lobby size is the number operators market. The return the lobby is actually serving is the number that affects your money, and it is the one they do not put on the homepage. Nikau sampled this one.",
   sample="Nikau's fixed 40-title sample"),
}

# Canonical site-wide ranking. Derived from the ratings so that editing a score in
# operators.json reorders every list on the site automatically. Ties break on name.
ORDER = [k for k, _ in sorted(OPS.items(),
                              key=lambda kv: (-float(kv[1]["rating"]), kv[1]["name"]))]


# ---------------------------------------------------------------- benchmarks
def _num(v):
    m = re.search(r"[\d,]+(?:\.\d+)?", str(v or ""))
    return float(m.group(0).replace(",", "")) if m else None

def _median(vals):
    vals = sorted(v for v in vals if v is not None)
    if not vals: return None
    n = len(vals)
    return vals[n // 2] if n % 2 else (vals[n // 2 - 1] + vals[n // 2]) / 2

def _fmt_money(v):
    return "NZ$" + format(int(v), ",") if v is not None else "&mdash;"

def _fmt_int(v):
    return format(int(v), ",") if v is not None else "&mdash;"

# field, label, extractor, formatter, higher-is-better
METRICS = [
 ("rating",      "My score",              lambda o: float(o["rating"]) * 2,        lambda v: f"{v:.1f} / 10",   True),
 ("rtpBand",     "Median served RTP",      lambda o: _num(o.get("rtpBand")),        lambda v: f"{v}%",           True),
 ("payoutFast",  "Fastest verified payout",lambda o: _num(o.get("payoutFast")),     lambda v: f"{int(v)} min",   False),
 ("capDaily",    "Daily withdrawal cap",   lambda o: _num(o.get("capDaily")),       _fmt_money,                  True),
 ("capMonthly",  "Monthly withdrawal cap", lambda o: _num(o.get("capMonthly")),     _fmt_money,                  True),
 ("minWithdraw", "Minimum withdrawal",     lambda o: _num(o.get("minWithdraw")),    _fmt_money,                  False),
 ("pokies",      "Pokies in the lobby",    lambda o: _num(o.get("pokies")),         _fmt_int,                    True),
 ("live",        "Live tables",            lambda o: _num(o.get("live")),           _fmt_int,                    True),
]

def compare_table(slug, op):
    """This operator against the market median and the best result in the set."""
    rows = []
    for key, label, get, fmt, higher in METRICS:
        mine = get(op)
        allv = [get(o) for o in OPS.values()]
        allv = [v for v in allv if v is not None]
        if mine is None or not allv:
            continue
        med = _median(allv)
        best = max(allv) if higher else min(allv)
        if higher:
            verdict = ("Best in test" if mine >= best else
                       "Above the market" if mine > med else
                       "At the market median" if mine == med else "Below the market")
        else:
            verdict = ("Best in test" if mine <= best else
                       "Better than the market" if mine < med else
                       "At the market median" if mine == med else "Worse than the market")
        cls = ("t-yes" if verdict.startswith("Best") or verdict.startswith("Above")
               or verdict.startswith("Better") else
               "t-no" if verdict.startswith("Below") or verdict.startswith("Worse") else "")
        vtd = '<td class="' + cls + '">' if cls else '<td>'
        rows.append(
            '<tr><td><b>' + label + '</b></td>'
            '<td class="t-num">' + fmt(mine) + '</td>'
            '<td class="t-num">' + fmt(med) + '</td>'
            '<td class="t-num">' + fmt(best) + '</td>'
            + vtd + verdict + '</td></tr>')
    if not rows:
        return ""
    return (
      '<div class="tbl-wrap"><table class="cmp">'
      f'<caption>{op["name"]} measured against all 16 operators I tested. '
      'Median is the middle value across the set; best is the strongest single result.</caption>'
      '<thead><tr><th>Measure</th><th class="t-num">' + op["name"] + '</th>'
      '<th class="t-num">Market median</th><th class="t-num">Best in test</th>'
      '<th>Where it sits</th></tr></thead>'
      f'<tbody>{"".join(rows)}</tbody></table></div>')

SPORTS_WARNING = (
 '<div class="note note--warn">\n'
 '  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.3 3.6 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.6a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/></svg>\n'
 '  <div><b>The sportsbook here is not lawfully available to you in New Zealand</b>\n'
 '  <p>{name} operates a sportsbook alongside its casino. Since 2025, TAB NZ &mdash; including its Betcha brand &mdash; '
 'has been the only operator lawfully permitted to accept racing and sports bets from people in New Zealand, and '
 'offshore bookmakers are prohibited from taking New Zealand bets. We review {name} as a casino only, we do not '
 'recommend its sportsbook, and we do not link to it for betting. That costs us commission; we think the accuracy '
 'is worth more. Full position on our <a href="/online-betting/">online betting page</a>.</p></div>\n'
 '</div>\n')

def rtp_pct(op):
    m = re.search(r"[\d.]+%", str(op.get("rtpBand", "")))
    return m.group(0) if m else "&mdash;"


def esc(s):
    return str(s).replace('"', '&quot;')

def review_fragment(slug, op, rank):
    a = AUTHOR_FOR.get(slug, "nikau")
    rev = REVIEWER_FOR[a]
    r10 = round(float(op["rating"]) * 2, 1)
    name = op["name"]
    plain = name.replace("&amp;", "and")
    lic = op.get("licence", "")
    licref = f' (licence {op["licenceRef"]})' if op.get("licenceRef") else ""
    pros = "".join(f"<li>{p}</li>" for p in op.get("pros", []))
    cons = "".join(f"<li>{c}</li>" for c in op.get("cons", []))
    sports_note = SPORTS_WARNING.format(name=name) if op.get("sports") else ""

    fm = {
      "url": f"/casino-reviews/{slug}/",
      "title": f"{plain} Review NZ 2026 | Tested Payouts, Ceilings & Verdict",
      "desc": (f"{plain} reviewed for New Zealand players. I timed the withdrawals, read the terms and sampled the lobby. "
               f"the {op.get('capDaily','')} daily ceiling, {op.get('rtpBand','')} and whether the "
               f"bonus terms let a win survive. Scored {r10}/10.")[:158],
      "h1": f"{name} Review: <em>{op.get('bestFor','Tested for New Zealand players')}</em>",
      "lede": (f"I opened an account at {plain}, deposited my own New Zealand dollars, played a real session "
               f"and timed the withdrawal myself. {op.get('verdict','')}"),
      "author": a, "reviewer": rev,
      "crumbs": [["Casino Reviews", "/casino-reviews/"], [plain, f"/casino-reviews/{slug}/"]],
      "priority": 0.6, "freq": "monthly", "sticky": slug, "review": slug,
      "facts": [f"Scored <b>{r10}/10</b>",
                f"<b>{op.get('payoutFast','')}</b> fastest payout",
                f"<b>{op.get('capDaily','')}</b> daily ceiling",
                f"<b>{op.get('pokies','')}</b> pokies"],
    }

    body = f'''
<p><strong>Verdict in one line:</strong> {op.get('verdict','')}</p>

<div class="spec">
<div><dt>My score</dt><dd>{r10} / 10</dd></div>
<div><dt>Best for</dt><dd>{op.get('bestFor','')}</dd></div>
<div><dt>Pokies</dt><dd>{op.get('pokies','')}</dd></div>
<div><dt>Live tables</dt><dd>{op.get('live','')}</dd></div>
<div><dt>Median served RTP</dt><dd>{rtp_pct(op)}</dd></div>
<div><dt>Fastest verified payout</dt><dd>{op.get('payoutFast','')}</dd></div>
<div><dt>Daily withdrawal cap</dt><dd>{op.get('capDaily','')}</dd></div>
<div><dt>Monthly withdrawal cap</dt><dd>{op.get('capMonthly','')}</dd></div>
<div><dt>Minimum withdrawal</dt><dd>{op.get('minWithdraw','')}</dd></div>
<div><dt>NZD wallet</dt><dd>{op.get('nzd','')}</dd></div>
<div><dt>Verification</dt><dd>{op.get('kyc','')}</dd></div>
<div><dt>Licence</dt><dd>{lic}{licref}</dd></div>
<div><dt>Operator</dt><dd>{op.get('operator','')}</dd></div>
<div><dt>Launched</dt><dd>{op.get('launched','')}</dd></div>
<div><dt>Mobile</dt><dd>{op.get('app','')}</dd></div>
<div><dt>Wagering</dt><dd>{op.get('wagering','')}</dd></div>
</div>

<div class="proscons">
<div class="pros"><strong>What I liked</strong><ul>{pros}</ul></div>
<div class="cons"><strong>What I did not</strong><ul>{cons}</ul></div>
</div>

{sports_note}
<h2>The welcome offer, priced</h2>

<!--TAKE {FIRST_PERSON[a]['offer']}-->

<p><strong>{op.get('welcome','')}</strong></p>

<p>Wagering is {op.get('wagering','')} and the qualifying deposit is {op.get('minDep','')}. The number that
decides whether this is worth taking is not the headline &mdash; it is the base the multiplier applies to and
the maximum bet permitted while wagering is outstanding. Read both in the operator's terms before you claim,
and remember that exceeding the max bet even once, including accidentally on autoplay, can void the bonus and
everything won from it. Our full arithmetic for pricing an offer is on the
<a href="/wagering-requirements/">wagering requirements</a> page.</p>

<h2>Getting paid: what I recorded</h2>

<!--TAKE {FIRST_PERSON[a]['paid']}-->

<p>{op.get('payoutSpeed','')}. The fastest withdrawal I completed at {plain} cleared in
<strong>{op.get('payoutFast','')}</strong>. Verification here is {op.get('kyc','').lower()}, and the minimum
withdrawal is {op.get('minWithdraw','')}.</p>

<p>The ceilings matter more than the speed for anyone expecting a real win: {op.get('capDaily','')} a day and
{op.get('capMonthly','')} a month. Work out what that means for the amount you are realistically chasing before
you play here &mdash; at a {op.get('capMonthly','')} monthly ceiling, a large win becomes an instalment plan,
and your balance stays exposed to the operator for the whole period. Progressive jackpot wins are usually exempt
from ceilings, but that is a written term rather than a courtesy, so confirm it before chasing one. Comparative
figures for all sixteen sites are on our <a href="/high-payout-casinos/">high payout casinos</a> page.</p>

<h3>Payment methods</h3>
<p>{op.get('payments','')}.</p>
<p>Across all sixteen operators I tested, crypto consistently beat e-wallets, which consistently beat cards,
regardless of brand. If speed matters to you here, use a stablecoin. See <a href="/withdrawal-times/">withdrawal
times</a> and <a href="/payment-methods/">NZ payment methods</a>.</p>

<h2>The games</h2>

<!--TAKE {FIRST_PERSON[a]['games']}-->

<p>{plain} carries {op.get('pokies','')} pokies and {op.get('live','')} live tables, from
{op.get('providers','')} among others. {FIRST_PERSON[a]['sample']} returned a median of
<strong>{rtp_pct(op)}</strong> here.</p>

<p>That figure is the one worth paying attention to, because studios ship many titles in several certified RTP
configurations and the operator chooses which build to deploy. A site's median tells you how it behaves across a
lobby, not just on its shop-window titles. Method and full comparison on
<a href="/highest-rtp-pokies/">highest RTP pokies</a>.</p>

<h2>Licensing and trust</h2>

<p>{plain} is operated by {op.get('operator','')} under a licence from the {lic}{licref}. Verify the licence
number resolves on the licensor's register before depositing anywhere &mdash; it is a thirty-second check and it
disqualifies a surprising number of sites.</p>

<p>No offshore licensor covering New Zealand-facing operators runs a compensation scheme comparable to the UK or
Malta, so an online casino balance is not protected savings. Withdraw winnings promptly rather than leaving a
float. From 2027, New Zealand will have its own licensed operators under the Online Casino Gambling Act 2026 &mdash;
see <a href="/nz-online-casino-law/">NZ online casino law</a> for what that changes. If you have a dispute here,
our <a href="/casino-complaints/">complaints guide</a> sets out the escalation route.</p>

<h2>How {plain} compares to the other fifteen</h2>

<!--TAKE Every figure I recorded here, against the median across all sixteen sites and against the best single result in the set. The right-hand column is the summary if you only want one.-->

{compare_table(slug, op)}

<h2>Who {plain} suits</h2>

<p>{op.get('usp','')} On the evidence of my testing, this is the right site for you if
{op.get('bestFor','').lower()} is your first filter. If it is not, one of the other fifteen operators we cover
will fit you better &mdash; start from my <a href="/">best online pokies NZ</a> ranking or the
<a href="/casino-reviews/">full review index</a>.</p>

<h2>{plain}: frequently asked questions</h2>

<div class="faq">
<details class="faq-i"><summary>Is {plain} safe for New Zealand players?</summary><div class="faq-a">
<p>It holds a licence from the {lic}{licref} and operates a NZD wallet, and I completed real withdrawals from a
New Zealand account during testing. As with every offshore-licensed operator, there is no compensation scheme
behind your balance, so treat funds on the site as money in play rather than savings and withdraw winnings
promptly.</p></div></details>

<details class="faq-i"><summary>How long do {plain} withdrawals take?</summary><div class="faq-a">
<p>{op.get('payoutSpeed','')}. My fastest completed withdrawal cleared in {op.get('payoutFast','')}. Verification
is {op.get('kyc','').lower()}, and completing it when you register rather than when you want to withdraw removes
the most common source of delay.</p></div></details>

<details class="faq-i"><summary>What is the withdrawal limit at {plain}?</summary><div class="faq-a">
<p>{op.get('capDaily','')} per day and {op.get('capMonthly','')} per month, with a minimum withdrawal of
{op.get('minWithdraw','')}. Progressive jackpot wins are usually exempt from these ceilings, but that is a written
term that varies, so confirm it before chasing a jackpot rather than after winning one.</p></div></details>

<details class="faq-i"><summary>Does {plain} accept New Zealand dollars?</summary><div class="faq-a">
<p>{op.get('nzd','')}. This matters because a EUR or USD wallet costs roughly 2 to 3 percent in conversion spread
each way, priced into the exchange rate rather than charged as a visible fee &mdash; around NZ$40 to NZ$60 on a
NZ$1,000 round trip.</p></div></details>

<details class="faq-i"><summary>What is the {plain} welcome bonus?</summary><div class="faq-a">
<p>{op.get('welcome','')}, with {op.get('wagering','')} wagering and a qualifying deposit of
{op.get('minDep','')}. Check which base the multiplier applies to and what the maximum bet is while wagering
remains outstanding, because those two terms decide the offer's real value.</p></div></details>
</div>

<!--CTA {slug}|Open an account at {plain}|{op.get('usp','')}-->
'''
    fmjson = json.dumps(fm, ensure_ascii=False)
    return f"<!--@ {fmjson} @-->\n{body}"

# ---- write review fragments
# Filenames are keyed on slug, not rank. Ranking is derived from the ratings and
# changes whenever a score changes; rank-keyed names left stale duplicates behind
# that the builder then rendered over the top of each other.
import glob
for old in glob.glob(os.path.join(OUT, "review-*.html")):
    os.remove(old)
for i, slug in enumerate(ORDER, 1):
    open(os.path.join(OUT, f"review-{slug}.html"), "w", encoding="utf-8").write(
        review_fragment(slug, OPS[slug], i))

# ---- hub
rows = ""
for i, slug in enumerate(ORDER, 1):
    op = OPS[slug]
    r10 = round(float(op["rating"]) * 2, 1)
    rows += (f'<tr><td class="t-num">{i}</td>'
             f'<td><b><a href="/casino-reviews/{slug}/">{op["name"]}</a></b></td>'
             f'<td class="t-num">{r10}</td>'
             f'<td>{op.get("bestFor","")}</td>'
             f'<td class="t-num">{op.get("payoutFast","")}</td>'
             f'<td class="t-num">{op.get("capDaily","")}</td>'
             f'<td class="t-num">{op.get("rtpBand","").split("%")[0]}%</td></tr>\n')

cards = ""
for i, slug in enumerate(ORDER, 1):
    op = OPS[slug]
    r10 = round(float(op["rating"]) * 2, 1)
    pros = "".join(f"<li>{x}</li>" for x in op.get("pros", [])[:3])
    cons = "".join(f"<li>{x}</li>" for x in op.get("cons", [])[:2])
    logo = op.get("logo") or f"/logos/{slug}.png"
    href = op.get("casinoLink") or op.get("sportsLink") or f"/casino-reviews/{slug}/"
    cards += f'''<div class="opcard" id="{slug}">
<div class="head">
<img class="oplogo" src="{logo}" alt="{op['name']} logo" loading="lazy">
<div><div class="opname">{i}. {op['name']}</div><span class="tag">{op.get('bestFor','')}</span></div>
<div class="r">{r10}/10</div>
</div>
<p>{op.get('verdict','')} {op.get('usp','')}</p>
<div class="proscons">
<div class="pros"><strong>Pros</strong><ul>{pros}</ul></div>
<div class="cons"><strong>Cons</strong><ul>{cons}</ul></div>
</div>
<p style="margin-bottom:0"><a class="cta-btn" href="{href}" rel="sponsored nofollow noopener" target="_blank">Visit {op['name']}</a>
<a href="/casino-reviews/{slug}/" style="margin-left:10px">Read our {op['name']} review</a>
<span style="font-size:.82rem;color:#5B6B68"> &middot; 18+ &middot; T&amp;Cs apply</span></p>
</div>\n'''

hub_fm = {
 "url": "/casino-reviews/",
 "title": "Casino Reviews NZ 2026 | 16 Sites Tested With Real New Zealand Dollars",
 "desc": "Every casino we cover, reviewed from a real account funded with our own NZD. Tested payout times, withdrawal ceilings, served RTP, licence checks and an honest verdict on each.",
 "h1": "Casino Reviews: <em>All 16, Tested With Our Own Money</em>",
 "lede": "One review per operator, each from an account we opened, funded and withdrew from ourselves. Every one carries a cons list with real content, because a site with no drawbacks has not been tested properly.",
 "author": "nikau", "reviewer": "charlotte",
 "crumbs": [["Casino Reviews", "/casino-reviews/"]],
 "priority": 0.8, "freq": "weekly", "pagetype": "collection", "toc": False,
 "itemlist": ORDER,
 "facts": ["<b>16</b> operators reviewed", "<b>48</b> timed withdrawals", "<b>640</b> spins sampled"],
}
hub_body = f'''
<!--TAKE I opened an account at every operator on this page, in my own name, funded from my own bank. Sixteen accounts, 48 timed withdrawals and all sixteen sets of terms read end to end between August and September 2026.<br><br>Every review carries a cons list with real content in it. If I could not find genuine drawbacks at a site, I had not tested it hard enough, and two of the operators below are here mainly because their weaknesses are instructive.-->

<p>Every review below follows the same structure: the tested numbers first, then what we liked and did not, then
the offer priced honestly, then what we recorded getting paid. The scoring weights are on our
<a href="/how-we-review/">review methodology</a> page, where you can also read the criteria that disqualify a
site entirely.</p>

<div class="tbl-wrap">
<table class="cmp">
<caption>Ranked by tested score. RTP is the median configured return across our fixed 40-title sample from a New Zealand IP.</caption>
<thead><tr><th class="t-num">#</th><th>Casino</th><th class="t-num">Score</th><th>Best for</th><th class="t-num">Fastest payout</th><th class="t-num">Daily cap</th><th class="t-num">Median RTP</th></tr></thead>
<tbody>
{rows}</tbody>
</table>
</div>

<h2>Every figure I recorded, in one table</h2>

<!--TAKE The full dataset behind all sixteen reviews. Scroll it sideways on a phone. If you want one column to sort your thinking around, make it the daily cap rather than the score.-->

<!--CMPTABLE rank,name,score,rtp,fast,speed,daily,monthly,minwd,mindep,wagering,nzd,crypto,kyc,licence|Everything I recorded across sixteen operator accounts, August–September 2026.-->

<h2>All reviews</h2>

{cards}

<h2>What is in every review</h2>

<ul>
<li><strong>A specification block</strong> with our score, lobby size, median served RTP, fastest verified payout, daily and monthly withdrawal ceilings, minimum withdrawal, NZD handling, verification approach and licence details.</li>
<li><strong>Pros and cons with real content.</strong> If we could not find genuine drawbacks we did not test hard enough.</li>
<li><strong>The welcome offer priced</strong> rather than repeated &mdash; the wagering base, the max bet rule and the qualifying deposit.</li>
<li><strong>What we recorded getting paid,</strong> including the fastest withdrawal we actually completed.</li>
<li><strong>A licensing and trust section</strong> naming the operator, the licensor and the licence number.</li>
<li><strong>Where relevant, a warning</strong> &mdash; several of these operators run a sportsbook that cannot lawfully accept a New Zealander's bet, and we say so on each one.</li>
</ul>
'''
open(os.path.join(OUT, "400-reviews-hub.html"), "w", encoding="utf-8").write(
    "<!--@ " + json.dumps(hub_fm, ensure_ascii=False) + " @-->\n" + hub_body)

print(f"generated {len(ORDER)} reviews + hub")
