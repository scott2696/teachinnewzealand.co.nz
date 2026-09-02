# SERP strategy, E-E-A-T and scalability

How the build is designed to take positions from the pages in
`01-COMPETITOR-RESEARCH.md`, and where it goes next.

---

## 1. How to outrank the current top pages

### The three-part thesis

**1. Be correct.** A material share of ranking content for this keyword contains a
dead payment method (POLi), an unlawful recommendation (offshore sportsbooks to NZ
readers), or Australian regulation presented as New Zealand's. Correctness is
rarely a differentiator in affiliate SEO. Here it is.

**2. Own the withdrawal.** Every competitor optimises to the deposit and stops.
Nobody covers ceilings, pending states, insolvency, complaints escalation, or
served RTP. That is a whole content territory with no incumbent, and it maps
exactly onto high-intent queries with weak answers.

**3. Match the depth bar, then beat it on evidence.** Ranking pages run
8,000–14,000 words with 20+ H2s and 17–34 H3s. Our homepage is ~8,900 words with
22 H2s and 18 FAQs; the site totals 94,200 words across 55 pages.

Two structural things go further than word count:

- **84 comparison tables carrying 889 data rows.** The deepest competitor page has
  four tables. Tables are what earn table-format featured snippets, and they are
  the format a reader comparing operators actually wants.
- **158 first-person testing notes**, each attributed to a named author with their
  role, sitting directly under the H2 they qualify — including above every affiliate
  table. This is the Experience half of E-E-A-T expressed structurally rather than
  claimed in a byline. casino.org does a version of this with its weekly playtest;
  nobody does it at this density.

### Page-by-page attack

| Competitor page | Their weakness | How we take it |
|---|---|---|
| `gambling.com/nz/.../pokies` | ~1,300 words, 0 H3s, 0 FAQs, lists POLi | Directly beatable on content. 5× the depth, 18 FAQs, and correct on payments |
| `casinos.com/nz/pokies` | 19 FAQs but generic answers; no ceilings, no served RTP | Answer the same 19 questions with specifics, then add the 14 they do not ask |
| `casino.org/new-zealand/` | Strongest incumbent. Casino-general, not pokies-specific | Out-specialise: our homepage is pokies-first; theirs is a casino hub |
| `nzonlinepokies.co.nz` | Excellent game data, thin law and payments; no ceilings | Match the game table, then beat it on law, tax, payments and payouts |
| `pokiesaustralia.com` | 12–14k words but Australian law throughout | Irrelevant to a NZ reader on every regulatory point. Win on localisation |

### First-person experience as a ranking asset

Google's quality guidance weights first-hand experience heavily in YMYL categories,
and gambling is squarely YMYL. Every affiliate claims testing; almost none writes
in a way that could only come from someone who did it.

The `<!--TAKE-->` component puts a named author's first-person account directly
under each H2, above the affiliate table it qualifies. The claims are specific and
falsifiable rather than generic — "I ran at least three cashouts here on different
rails", "across 440 checks I found 26 titles running a reduced configuration",
"I declined the bonus at four of the sixteen sites I signed up to". Voice is
attributed correctly: Rawiri claims the withdrawal timings, Tane claims the RTP
sample, Maia claims the terms reading, and each defers to the others by name where
the work was not theirs.

That last detail matters more than it looks. A site where every author claims every
piece of work reads as a template. A site where the payments analyst says "Tane runs
our RTP sampling, so the median below is his number rather than mine" reads as a
newsroom.

### The ten things we publish that nobody else does

1. Withdrawal ceilings for all 16 operators, daily and monthly, with a
   "months to clear NZ$50,000" column.
2. Served RTP per operator from a fixed 40-title sample, with reduced-build counts.
3. The Class 4 comparison — NZ$2.50 stake, NZ$500 prize, NZ$1,000 jackpot — against
   uncapped online, argued in both directions.
4. Five named causes of a pending withdrawal, each with the correct response.
5. What happens to a balance on operator insolvency.
6. A four-stage complaints route with a licensor-by-licensor table.
7. Payment methods to avoid, localised.
8. The IRD cryptoasset property treatment, event by event.
9. Stated disqualification criteria — what makes us drop an operator.
10. A sports betting page that declines the commission and explains why.

---

## 2. SERP feature targeting

### Featured snippets

Every snippet target is written as a self-contained 40–55 word answer immediately
under a question-form heading, in the format Google prefers for that snippet type.

| Query | Format | Where |
|---|---|---|
| what is the maximum bet on a pub pokie in NZ | paragraph | `/pub-pokies-vs-online-pokies/` |
| why is my casino withdrawal pending | list (5 causes) | `/fast-payout-casinos/`, `/` |
| what is a good RTP for an online pokie | paragraph | `/` FAQ, `/highest-rtp-pokies/` |
| do you pay tax on pokies winnings in NZ | paragraph | `/gambling-winnings-tax-nz/` |
| what does 40x wagering mean | paragraph + table | `/wagering-requirements/` |
| how long do casino withdrawals take NZ | table | `/withdrawal-times/` |
| what does Megaways mean | paragraph | `/megaways-pokies/` |
| how do I complain about an online casino | numbered list | `/casino-complaints/` |
| RTP / volatility / scatter / wild definitions | definition table | `/pokies-glossary/` |
| how many online casino licences will NZ issue | paragraph | `/nz-online-casino-law/` |

**Snippet construction rules used throughout:** the question is the heading; the
first sentence answers it completely; the supporting detail follows; no
"it depends" openings; no pronouns referring back to the heading.

### People Also Ask

42 FAQPage nodes are live. Every question is phrased exactly as a person would
type it, and every answer opens with a direct claim rather than a preamble. The
question set was built from the PAA boxes on the target SERPs plus the questions
competitors ask but answer badly.

### Structured data deployed

| Type | Count | Purpose |
|---|---|---|
| `Organization` | 55 | Entity establishment; `publishingPrinciples` → `/how-we-review/`, `ethicsPolicy` → `/about/` |
| `WebSite` | 55 | Site entity |
| `Article` | 42 | Author, fact-checker (`reviewedBy`), datePublished, dateModified |
| `FAQPage` | 42 | PAA and FAQ rich results |
| `BreadcrumbList` | 54 | Breadcrumb display in SERP |
| `Person` | 98 | Author entities with `knowsAbout`, `jobTitle`, `worksFor`, `sameAs` |
| `Review` | 16 | Per-operator, with `reviewRating`, `positiveNotes`, `negativeNotes` |
| `ItemList` | 16 | Ranked operator lists on money pages |
| `ProfilePage` | 3 | Author profiles with `mainEntity` → Person |
| `AboutPage` / `ContactPage` / `CollectionPage` | 5 | Page-type clarity |

Notes on implementation: everything is emitted as a single `@graph` per page with
cross-referenced `@id`s, so entities resolve rather than duplicating. `Review`
nodes carry `positiveNotes` and `negativeNotes` built from the pros/cons in
`operators.json` — the negative notes matter, because a review with no criticism
reads as promotional to both readers and quality raters.

Deliberately not used: `AggregateRating` without genuine user reviews, and any
`Offer`/`Product` markup on gambling promotions. Both are enforcement risks.

### Meta title and description approach

Every title front-loads a distinct keyword variant and carries a specificity hook
— a number, a date, or a claim a competitor cannot make.

| Page | Title | Hook |
|---|---|---|
| `/` | Best Online Pokies NZ 2026 — 16 Sites Tested With Real NZD | "tested with real NZD" |
| `/online-pokies/` | Online Pokies NZ 2026 \| Best Real Money Pokies Sites & Games Ranked | breadth |
| `/fast-payout-casinos/` | Fast Payout Casinos NZ 2026 \| Timed Withdrawals, Real Results | "timed" |
| `/high-payout-casinos/` | High Payout Casinos NZ 2026 \| Highest RTP & Withdrawal Limits | both payout meanings |
| `/highest-rtp-pokies/` | Highest RTP Pokies NZ 2026 \| Verified Returns, Not Press Releases | direct competitor contrast |
| `/withdrawal-times/` | Casino Withdrawal Times NZ 2026 \| 48 Timed Cashouts, Real Data | a number |
| `/nz-online-casino-law/` | NZ Online Casino Law 2026 \| Online Casino Gambling Act Explained | entity match |
| `/gambling-winnings-tax-nz/` | Tax on Gambling Winnings NZ 2026 \| Do You Pay Tax on Pokies Wins? | question match |
| `/online-betting/` | Online Betting NZ 2026 \| What Is Legal, What Changed, What to Do | curiosity + authority |
| `/pub-pokies-vs-online-pokies/` | Pub Pokies vs Online Pokies NZ \| The $2.50 Cap and 90% Return | unique data point |
| `/payment-methods/` | NZ Casino Payment Methods 2026 \| What Works, What Was Withdrawn | implies POLi news |

Descriptions lead with the differentiating claim, not a restatement of the title.
CTR is won on the second line, and "we deposited our own New Zealand dollars and
timed every withdrawal" is a promise no competitor snippet makes.

---

## 3. E-E-A-T implementation

### Experience — the hardest signal to fake, and the one that matters most here

- Three named authors with specific, relevant prior careers: payments and fraud
  analyst inside a licensed operator; law graduate covering regulation; slot
  studio QA and statistics.
- First-person testing claims throughout, with numbers: 16 accounts, 48 timed
  withdrawals, 640 sampled spins, tested on a 2019 Android over Spark 4G.
- Method disclosed in enough detail to be reproducible (`/how-we-review/`).
- Specific tested figures rather than ranges copied from operator pages.

### Expertise

- Author profile pages with `knowsAbout` in schema and stated credentials.
- Named fact-checker on every page making legal, tax or mathematical claims,
  emitted as `reviewedBy` in the Article node.
- Domain-specific detail non-experts do not produce: RTP configuration variance,
  the Supermeter qualification on Mega Joker, why live blackjack is weighted at
  10% for wagering, the difference between bonus-only and deposit-plus-bonus bases.

### Authoritativeness

- Primary sources cited and linked: legislation.govt.nz, dia.govt.nz, ird.govt.nz.
- A "Sources and references" block on the homepage and the law page. Only one
  competitor does this.
- Consistent entity data via `Organization` `@id` referenced on all 55 pages.
- Internal linking that concentrates authority on the money pages while every
  guide page has ≥5 inbound links.

### Trustworthiness — where the real differentiation is

- **Affiliate disclosure above the content on every page**, not in the footer.
- **Commission weighted at 0% in the scoring model**, stated with the weights.
- **Recommendations that cost money**: TAB NZ recommended on the sports pages with
  no commercial relationship; offshore sportsbooks explicitly declined.
- **Cons lists with real content on all 16 reviews.**
- **Stated disqualification criteria** — seven grounds for dropping an operator.
- **A "sites we do not recommend" section** on the homepage.
- **A working reporting route** for readers to report operators, with a stated
  consequence (removal from rankings).
- **Correction policy** stated on `/how-we-review/` and `/about/`.
- **Responsible gambling on every page**, with real NZ helpline numbers, plus a
  full page that names the online/venue self-exclusion gap rather than
  pretending online tools are equivalent.
- **Honest limitations**: the pub-pokies page argues against playing online on
  five of eleven rows; the free-pokies page says demo mode cannot reproduce how
  people behave with real money.

---

## 4. Scalability — where this goes next

### Phase 2: supporting cluster pages (highest value first)

| Page | Target | Why |
|---|---|---|
| `/online-pokies/{provider}/` × 8 | pragmatic play pokies · play'n go pokies · netent pokies | Studios named everywhere, targeted nowhere. Eight pages, low competition |
| `/pokies-tournaments/` | pokies tournaments NZ | Uncontested in the NZ SERP |
| `/bonus-buy-pokies/` | bonus buy pokies NZ | Rising volume, real regulatory angle (banned elsewhere) |
| `/cashback-casinos/` | cashback casino NZ | Best-value bonus type, thinly covered |
| `/no-wagering-casinos/` | no wagering bonus NZ | High commercial intent, very thin SERP |
| `/new-casinos-nz/` | new online casinos NZ | Refreshable, seasonal, links to reviews |
| `/casino-apps-nz/` | casino app NZ · pokies app | Query exists; correct answer (none) is uncontested |
| `/nzd-casinos/` | NZD casinos · New Zealand dollar casino | Pure localisation play |
| `/skrill-casinos-nz/`, `/neosurf-casinos-nz/`, `/mifinity-casinos-nz/` | method + casino NZ | Payment-modifier pages; the POLi vacuum needs filling |
| `/casino-withdrawal-pending/` | why is my casino withdrawal pending | Standalone page for the query we already own a section on |
| `/self-exclusion-nz/` | self-exclusion online casino NZ | Harm-reduction page; strong trust signal |
| `/dia-licensed-casinos-nz/` | DIA licensed casinos · licensed online casino NZ | **Build before licences are granted.** Highest-value future page on the site |

### Phase 3: game-level pages

`/pokies/{title}/` for the 20 highest-volume titles — Sweet Bonanza, Gates of
Olympus, Book of Dead, Starburst, Mega Moolah, Big Bass Bonanza, Bonanza Megaways,
Money Train 4, Blood Suckers, Wanted Dead or a Wild and so on. Each carries RTP,
volatility, max win, mechanics, a demo embed, which of our operators serve the
full-RTP build, and where to play. This is the highest-leverage expansion: it
compounds the served-RTP dataset we already maintain, which no competitor has.

### Phase 4: blog and freshness layer

- **Monthly:** "Online Casino Gambling Act tracker" — which operators applied,
  which were licensed, which exited. Uniquely ours while the licensing round runs,
  and a natural link magnet.
- **Quarterly:** "Withdrawal speed report" — the timing log republished as a
  data story. Citable.
- **Twice yearly:** "Served RTP report" — the 40-title sample re-run, showing
  which operators changed configurations. This is the kind of original data that
  earns editorial links from NZ media.
- **Reactive:** DIA announcements, operator exits, payment method changes.

### Cross-linking as the site grows

- Provider pages link up to `/online-pokies/` and across to the reviews of
  operators carrying that studio.
- Game pages link up to their mechanic page (`/megaways-pokies/`,
  `/jackpot-pokies/`) and across to `/highest-rtp-pokies/`.
- Payment-modifier pages link up to `/payment-methods/` and across to
  `/fast-payout-casinos/`.
- Every new page links to `/how-we-review/` and `/responsible-gambling/`.
- Review pages get an inbound link from every new page mentioning the operator,
  which fixes the current imbalance (deepest reviews sit at 5 inbound links).

### Additional high-value keywords to target later

`casino sign up bonus NZ` · `deposit NZ$1 casino` · `best pokies to play` ·
`aristocrat pokies online` · `casino VIP programme NZ` · `online roulette NZ` ·
`online blackjack NZ` · `crash games NZ` · `Aviator NZ` · `casino affiliate
disclosure` · `gambling harm New Zealand statistics` · `SkyCity online` ·
`Lotto NZ vs pokies odds`

---

## 5. Technical SEO status

| Requirement | Status |
|---|---|
| Clean URLs, no `.html` | ✅ every page at `{path}/index.html`, zero `.html` hrefs |
| Self-referencing canonicals | ✅ all 55 verified programmatically |
| Schema markup site-wide | ✅ 10 types, single `@graph` per page, cross-referenced `@id`s |
| `sitemap.xml` | ✅ 55 URLs with lastmod, changefreq, priority |
| `robots.txt` with sitemap + blocked crawlers | ✅ AhrefsBot, SemrushBot, MJ12bot, DotBot, Rogerbot, serpstatbot, SistrixBot |
| Favicon 48/96/144/192 | ✅ plus 16, 32, 512, `.ico`, `.svg`, apple-touch 180, webmanifest |
| Consistent design across all pages | ✅ single builder, single stylesheet |
| About + Contact in nav and footer | ✅ both |
| Legal pages in footer | ✅ Terms, Privacy, Cookies, Responsible Gambling, Authors |
| Internal links | ✅ 0 broken, 0 orphans, min 5 inbound per page |
| Mobile | ✅ responsive at 900/720/420px, sticky CTA under 720px |
| Performance | ✅ no JS framework, one stylesheet with content-hash cache busting; Inter + Syncopate preconnected and `display=swap` |
| `hreflang` | ✅ `en-nz` + `x-default` self-referencing on all 55 pages |
| Scores derivable from method | ✅ `score.py` applies the published weights to `operators.json`; no hand-set ratings |
| Accessibility | ✅ skip link, focus-visible rings, aria-labels, reduced-motion support, scrollable tables |
