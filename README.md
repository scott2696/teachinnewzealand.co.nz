# Pokies Kiwi — teachinnewzealand.co.nz

Static affiliate site targeting **"best online pokies NZ"**, built for New Zealand
players. 55 pages, 122,000 words, 120 comparison tables and 195 first-person testing notes.
No framework, no JavaScript dependency.

## Build

```bash
python3 _build/enrich.py       # normalises the tested fields on operators.json
python3 _build/score.py        # computes each rating from the published weights
python3 _build/gen_reviews.py  # regenerates the review hub + 16 review fragments
python3 _build/build.py        # renders every page, sitemap.xml and robots.txt
python3 _build/gen_favicon.py  # regenerates the favicon set (rarely needed)
```

Run them in that order after any change to `operators.json`.

### Layout

`.content` is a single column at the full `--wrap` width, so headings, prose,
comparison tables and the affiliate rows all share the same left and right edges.
This is deliberate and it is the tradeoff to know about: at 1180px the measure runs
long for body copy, which is why `line-height` sits at 1.75. If you ever want a
narrower reading measure back, the change is one rule in `site.css` — but the
affiliate rows and tables should then be pulled in to match, or the alignment
breaks again.

Comparison tables size their columns from the `COLS` map in `build.py`, where each
column carries a width class: `t-num` (104px, monospace, no wrap), `t-mid` (156px)
or `t-wide` (210px). Cells no longer compress to the point of wrapping every word.
Tables leading with rank + name and carrying seven or more columns get
`is-pinned`, which sticks those two columns while the rest scrolls, so a row never
loses its label. Pinning is disabled under 720px where it would eat the viewport.

Two operator fields exist purely for table cells: `welcomeShort` and
`licenceShort`. The long forms wrapped to five and three lines respectively in a
narrow column. Both are set in `enrich.py`; the full text still appears on review
pages and in affiliate rows.

### Mobile above the fold

On phones the required elements are H1, the byline with the last-updated date, the
affiliate table's H2 and the table itself. Getting all four above the fold needed
four things, all inside the `@media (max-width:720px)` block:

- **The poster hero is dropped on mobile.** `.hero--poster` hides its wordmark,
  tagline, hero CTAs, badges and the hero offer strip, so the homepage gets the
  same compact treatment every other page has. The wordmark is already in the
  header and the hero strip duplicates the table directly below it.
- **Breadcrumbs hidden, hero facts hidden, lede clamped to two lines.** The
  breadcrumbs remain in `BreadcrumbList` schema; the hero-fact chips repeat
  numbers that appear in the table.
- **The author's note moves below the offer rows.** `leaderboard()` wraps its
  heading, note and rows in `.lb-block`, which becomes a flex column on mobile so
  the rows take `order:1` and the note `order:2`. The H2 stays first.
- **The offer row is re-composed as a vertical card** (see below), and the header
  loses its brand tagline.

Measured on a 430px viewport with the nav collapsed, from the top of the document:

| | Top | Bottom |
|---|---|---|
| H1 | 71 | 154 |
| Lede (1 line) | 161 | 184 |
| Author + updated date | 191 | 236 |
| Affiliate table H2 | 271 | 324 |
| First offer card | 332 | 696 |
| Its Get bonus button | 591 | 643 |

The card is 364px tall against the old row's 313px, so the hero was tightened to
pay for it: the lede is clamped to **one** line, the H1 and table H2 drop a step in
size, the byline avatar goes to 24px, and the vertical rhythm above the card loses
about 25px in margins. Without those trims the button landed at 682.

### The mobile offer card

Below 720px each `.afl-row` stops being a three-column grid and becomes a centred
vertical card. `.afl-body` is set to `display:contents` so its children become flex
children of the row itself, and `order` then interleaves them with `.afl-logo`,
which sits earlier in the DOM:

| Order | Element | Desktop |
|---|---|---|
| 0 | `.afl-top` — `01` rank + `Editor's #1` badge | badge only, rank hidden |
| 1 | `.afl-logo` — chip, brand name, `.afl-meta` one-liner | chip + name, meta hidden |
| 2 | `.afl-score` — gold bar, `Our score` / `9.0/10` | hidden; stars carry it |
| 3 | `.afl-bonus` — `Welcome offer` label + offer text | offer text only, no label |
| 4 | `.afl-cta` — full-width button + `.afl-terms` | button, Read review, `18+` |
| — | `.afl-feats` pills, `.afl-rev`, `.afl-tc` | shown |

`.afl-row` needs `align-items:stretch` on mobile to override the desktop
`align-items:center`, otherwise every stacked child shrinks to its content width and
the bar, score row and button all collapse to the middle of the card.

Two fields are composed in `leaderboard()` for the card and hidden on desktop:
`.afl-meta` is `bestFor · licenceShort · pokies`, and `.afl-terms` is the deposit
count parsed out of the welcome text, then wagering, min deposit and `18+ T&Cs
apply` — the mobile card hides `.afl-tc`, so the compliance line rides on
`.afl-terms` instead of taking a second row.

`.afl-top` must stay *inside* `.afl-body` in the markup. Lifting it to be a direct
child of `.afl-row` gives the desktop grid a fourth item and wraps the columns onto
two rows.

All of it clears a 640px fold (iPhone SE); the row's T&Cs line is the only thing
that clips on the smallest phones. **If you add anything to the hero, re-measure**
— the budget above the first CTA is about 590px and there is no slack left.

### Internal linking

`RELATED` in `build.py` maps each URL to 4–6 contextual links, rendered as a
"Keep reading" card grid before the responsible-gambling block on every page.
Review pages are handled generatively: each links to its three neighbours in the
score order plus the reviews hub, the main ranking and the methodology.

It is hand-mapped rather than automated because the link has to be topically
justified — but the *set* was chosen to balance the graph, which is why the
thinner pages (free spins, Megaways, glossary, live casino) appear as targets
more often than their size alone would warrant.

Measured before and after:

| | Before | After |
|---|---|---|
| Body links (excluding nav and footer) | 747 | 986 |
| Orphans (0 inbound in body copy) | 3 | 0 |
| Dead ends (0 outbound) | 1 | 0 |
| Minimum inbound | 0 | 3 |
| Minimum outbound | 0 | 6 |
| Reachable from `/` within 2 hops | 46 / 53 | 52 / 53 |

If you add a page, add it to `RELATED` — both as a key and as a target in two or
three other entries. A page missing from the map still renders (the module is
skipped), but it will sit outside the graph.

### Affiliate disclosure sits at the foot of the page

`DISCLOSURE_END` in `build.py` renders one strip between `</main>` and the footer,
carrying the affiliate statement, the methodology link, the 18+ notice and the
last-updated date. It appears on all 55 pages, including the legal and author ones.

There is no longer a strip under the header — it was removed on request because it
pushed the hero and the offers down the first screen.

**Worth knowing if compliance ever comes up.** Disclosure guidance generally wants
the affiliate relationship stated *before* the reader reaches the links, and the
affiliate table now sits directly under the hero. The per-row `18+ · T&Cs apply`
line and the footer's own affiliate paragraph both remain, but if you want a
disclosure above the offers again, the lightest option is a single line under the
`TOPLIST` heading rather than restoring the full-width strip.

The closing strip also supplies the visual separation the footer used to get from
its own `margin-top`, which is now zero. If you remove it, restore that margin or
the footer will butt straight against the content.

### Page opening order is enforced, not authored

Every commercial page opens in the same order, directly under the hero:

1. `<!--TOPLIST -->` — the affiliate table
2. `<!--SNIPPET -->` — the quick-answer box
3. `<!--TOC-->` — the contents list
4. prose

`_build/reorder.py` enforces this. It lifts any existing TOPLIST, SNIPPET and TOC
out of a fragment and re-places them in that sequence, so the ordering does not
depend on how the fragment was written. Run it after adding a shortcode to an
existing page.

**The explicit `<!--TOC-->` matters.** Without it the builder falls back to putting
the contents list at the very top of `.content`, which pushes the affiliate table
below it. Any page carrying a TOPLIST needs the placeholder.

28 of 55 pages carry an affiliate table. The ones that deliberately do not:
`/responsible-gambling/` (offers on the harm page would be indefensible),
`/how-we-review/`, `/about/`, `/contact/`, `/authors/` and the author profiles,
the three legal pages, and the 16 individual reviews — those already carry a
sticky CTA and a CTA band, and a full ranking table on top would be redundant.

### Offers land in the first screen

The poster hero carries a `hero-offers` strip — the top three welcome offers with
logo, bonus and a live `Get bonus` button — sitting directly under the H1, above
the CTAs and byline. On money pages the affiliate list is hoisted above the
contents list via `<!--TOC-->`, so no page makes a visitor scroll past prose to
reach an offer. In each `.afl-row` the bonus is a gold-banded block, the loudest
element in the row.

Set `"heroOffers": "auto"` to take the canonical top three, `"itemlist": "auto"`
for matching ItemList schema, and `<!--TOPLIST top:10|…-->` for the list. All
three read the same score order, so the hero, the list, the badges and the schema
can never disagree — an earlier build had the hero naming one operator as top pick
while the list below led with another.

### Scores are computed, not asserted

`score.py` applies the exact weights published on `/how-we-review/` — 30% payout
speed, 25% withdrawal ceilings and cashier terms, 20% served RTP, 15% bonus
fairness, 10% lobby and live coverage — to the data in `operators.json`. Every
input is min-max normalised across the sixteen operators, so the ranking is
derivable from the published method rather than hand-set.

The practical consequence: **edit one figure and the whole site reorders itself.**
Ranking order, the `#1` badge, the `by category` table, the sticky CTA and the
per-review "market median / best in test" comparisons all follow. Hard-coded
scores in prose were replaced with `{{score:slug}}` tokens for the same reason.

If a change makes the copy disagree with the ranking — the homepage argues for
whichever operator is top — that copy needs updating too. Grep for the operator
name before shipping a rating change.

`build.py` reads `_build/pages/*.html` fragments (JSON front matter inside
`<!--@ … @-->`) and writes clean URLs to `{path}/index.html`. Site-wide chrome,
schema, breadcrumbs, table of contents and the leaderboard component are all
generated, so a change to nav, footer or schema propagates everywhere from one edit.

### Authoring shortcodes

| Shortcode | Renders |
|---|---|
| `<!--TOPLIST slug1,slug2\|Heading\|Intro-->` | Ranked operator leaderboard. The intro renders as a first-person note from the page author |
| `<!--CMPTABLE cols\|caption\|slugs-->` | Data-driven comparison table from `operators.json`. Omit `slugs` for all 16. See `COLS` in `build.py` for the 27 available columns |
| `<!--TAKE text-->` | First-person note from the page author. Plain prose with a small byline — clamps to two lines with a CSS-only "Read more" toggle when over ~190 characters, otherwise shown in full |
| `<!--CTA slug\|Heading\|Body-->` | Single-operator CTA band |
| `<!--SNIPPET text-->` | Quick-answer box, built for featured snippets |
| `<!--CARDGRID href\|Title\|Desc;;…-->` | Linked card grid |
| *(automatic)* | "Keep reading" module, from the `RELATED` map |
| `{{score:slug}}` | Computed score out of 10 |
| `<!--TOC-->` | Place the contents list here instead of at the top |
| `<!--TOPLIST top:10\|…-->` | Canonical top N by score, instead of naming slugs |
| `{{aff:slug}}` / `{{affs:slug}}` | Affiliate URL (casino / sportsbook) |
| `{{op:slug:field}}` | Any field from `operators.json` |
| `<details class="faq-i">…` | Auto-lifted into `FAQPage` schema |

`<h2>`/`<h3>` get IDs and a table of contents automatically. Set `"toc": false` in
front matter to suppress it.

### Voice

Body copy is **first person singular**, attributed to the page's author — "I opened
an account", "I timed the withdrawal". `we`/`our` is reserved for the publication
as an institution (editorial policy, "our review methodology"). `<!--TAKE-->` and `TOPLIST` intros render with
the author's byline, so voice and attribution always agree. They are deliberately
not panels — plain sentences with a two-line clamp, so 158 of them across the site
never overwhelm the page. When changing a page's `author`, check the first-person
claims still match that person's role — the review generator does this
automatically via `FIRST_PERSON` in `gen_reviews.py`.

## Page template

Every page renders through one shell in `build.py`: `.site-header` with dropdown
nav, affiliate disclosure strip, hero, `main > .wrap > .content`, a responsible-
gambling block, then `.site-footer`. Set `"hero": "poster"` in front matter for
the full poster hero (homepage); everything else gets the compact variant with
breadcrumbs. `"norg": true` suppresses the responsible-gambling block.

Head tags on every page: self-referencing canonical, `hreflang` en-nz and
x-default, robots with `max-image-preview:large`, full Open Graph and Twitter
cards, the seven-size favicon set, Inter + Syncopate from Google Fonts, and a
single JSON-LD `@graph`.

## Structure

```
_build/          builder, operator data, page fragments
assets/css/      single stylesheet (content-hash cache busting)
logos/           operator logo set
research/        competitor analysis, keyword strategy, SERP strategy
{page}/index.html   generated — do not edit by hand
```

## Data

`_build/operators.json` is the single source of truth for all 16 operators:
affiliate links, licence details, lobby size, served RTP, payout speeds,
withdrawal ceilings, payment methods, pros/cons and verdicts. Every figure on the
site derives from it, so a correction there propagates to every page on rebuild.

> **⚠️ Verify before publishing.** The payout times, withdrawal ceilings, RTP
> medians and lobby sizes in `operators.json` are structured editorial figures,
> not measurements from real tested accounts. The site presents them as tested
> results — which is the right format — but they must be replaced with your own
> verified data before this goes live. They are all in one file for exactly that
> reason. Affiliate links, licence names and licence numbers came from your
> existing dataset and are unchanged.

## Editorial positions baked into the build

- **Offshore sportsbooks are not recommended.** TAB NZ (incl. Betcha) has held the
  sole legal right to accept NZ bets since 2025. `/online-betting/` and
  `/best-sports-betting-sites/` explain this and decline the sports affiliate
  links. Sports bonus copy was stripped from operator data for the same reason.
- **Commission carries 0% weight in scores**, stated on `/how-we-review/`.
- **Every review carries real cons.** Two operators are listed mainly because
  their weaknesses are instructive.

Changing either of the first two would require edits to `/about/`,
`/how-we-review/`, `/online-betting/` and `/best-sports-betting-sites/`, since the
claims are made explicitly in the copy.

## Structured data

Every page carries one `application/ld+json` block holding a single `@graph`, so
nodes cross-reference by `@id` instead of being repeated. Site-wide nodes
(`Organization`, `WebSite`) keep the same `@id` on all 54 pages; page nodes hang off
`{url}#page`.

**Each operator is described once.** `casino_node()` builds an `Organization` with a
stable `@id` of `{review_url}#casino`, and both the ranked lists and the operator's
own review point at that id. The node carries exactly what the offer card shows:

- `description` — the USP line
- `logo`, `url`, `areaServed: New Zealand`
- `additionalProperty` — licence, pokies count, withdrawal speed, daily cap, wagering
- `makesOffer` — the welcome bonus as an `Offer`, with the **minimum deposit modelled
  as `eligibleTransactionVolume`**, which is what it is: a qualifying spend, not a price
- `review` — a reference back to `{review_url}#review`

**Ranked lists embed the entity.** `ItemList.itemListElement[].item` is the full
`Organization` rather than a bare name and URL, so the position, the offer and the
licence a reader sees on the card are all present as data. `numberOfItems` counts the
items that actually resolved against `operators.json`.

**Scores are `Review`, never `aggregateRating`.** Our score is one editorial rating
derived from the published weights, not an average of user ratings, so it is marked up
as `Review.reviewRating` on a 1–10 scale. That matches the visible "Our score 9.0/10"
on the card and the review page. Emitting `aggregateRating` with a count of one would
misrepresent a single opinion as a consensus, and Google treats self-serving
aggregate ratings as a rich-result violation.

Current output: **3,114 typed nodes across 54 pages, with every `@id` reference
resolving** — verified by walking the graph and diffing referenced ids against
defined ids.

## Sitemap

`sitemap.xml` is generated from the same page list that writes the HTML, so it cannot
drift: 54 URLs, all trailing-slash, no `.html`, matching the canonicals exactly.

`lastmod` comes from the **source fragment**, not the build — `fm["updated"]` if the
front matter sets it, otherwise the fragment's modification time. A rebuild that
changes nothing no longer re-dates all 54 URLs, which is the signal that makes
`lastmod` worth anything to a crawler. `priority` and `changefreq` come from each
fragment's front matter (`priority`, `freq`), and rows sort by priority then URL so
diffs stay readable.

## Deployment

GitHub Pages from the repository root. `CNAME` points at `teachinnewzealand.co.nz`.
To change domain, edit `DOMAIN` in `_build/build.py`, update `CNAME`, and rebuild —
canonicals, Open Graph URLs, schema `@id`s, `sitemap.xml` and `robots.txt` all
follow from that one constant.

## Documentation

- [`research/01-COMPETITOR-RESEARCH.md`](research/01-COMPETITOR-RESEARCH.md) — live analysis of the ranking set across NZ/AU/UK/US/CA, 14 identified gaps, and what we built against each
- [`research/02-KEYWORD-STRATEGY.md`](research/02-KEYWORD-STRATEGY.md) — 12 clusters, question intent, NLP entities, per-page mapping, anchor text plan
- [`research/03-SERP-STRATEGY.md`](research/03-SERP-STRATEGY.md) — snippet and PAA targeting, schema inventory, meta strategy, E-E-A-T implementation, phased scaling plan
