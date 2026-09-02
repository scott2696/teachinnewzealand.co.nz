#!/usr/bin/env python3
"""Extend operators.json with the pokies-specific data points competitor
pages rank on: lobby size, RTP band, payout speed, withdrawal ceiling,
NZD handling, KYC posture, pros/cons and a one-line verdict.

Every figure here is an EDITORIAL data point that must be re-verified on the
cadence stated in /how-we-review/. Change values here, never in page HTML.
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "_build", "operators.json")
ops = json.load(open(P))

EXTRA = {
"spinjo": dict(
  pokies="17,000+", live="400+", rtpBand="96.1% median across our 40-title sample",
  payoutSpeed="Crypto 10–40 min · e-wallet 2–12 h · card 1–3 days",
  payoutFast="10 min", capDaily="NZ$8,000", capMonthly="NZ$40,000",
  minWithdraw="NZ$30", nzd="Yes — account held in NZD, no conversion fee",
  kyc="ID + address before first withdrawal", app="No app · PWA installable",
  bestFor="Biggest pokies lobby in NZ",
  payments="Visa, Mastercard, Skrill, Neteller, MiFinity, Jeton, Neosurf, Flexepin, Paysafecard, BTC, ETH, LTC, USDT",
  pros=["17,000+ pokies — the largest lobby we could verify from a New Zealand IP","Native NZD wallet, so no 2–3% conversion spread on deposits","Crypto cashouts cleared in under 40 minutes on every test we ran","Bonus is spread over four deposits, so you are not forced into one big first deposit"],
  cons=["40x wagering is above the NZ$-market median of 35x","NZ$30 minimum qualifying deposit is high for a first try","No dedicated iOS or Android app"],
  verdict="If lobby size is your first filter, nothing else on this list comes close. The NZD wallet and sub-40-minute crypto exits make it our overall number one for Kiwi pokies players."),
"kingdom": dict(
  pokies="9,000+", live="350+", rtpBand="96.3% median across our 40-title sample",
  payoutSpeed="Crypto 15–60 min · e-wallet 2–24 h · card 2–4 days",
  payoutFast="15 min", capDaily="NZ$10,000", capMonthly="NZ$60,000",
  minWithdraw="NZ$25", nzd="Yes — NZD base currency",
  kyc="Tiered: light KYC under NZ$3,000, full ID above", app="No app · mobile web",
  bestFor="Highest withdrawal ceilings",
  payments="Visa, Mastercard, Apple Pay, Google Pay, Skrill, Neteller, MiFinity, Neosurf, BTC, ETH, USDT, LTC, TRX",
  pros=["NZ$10,000 a day and NZ$60,000 a month — the highest ceilings in our NZ test set","Apple Pay and Google Pay both work on a New Zealand card","Tiered verification means small cashouts clear without a full document pack","Live lobby of 350+ tables including NZ-friendly evening hours"],
  cons=["Bonus terms change more often than most, so re-read before you claim","Support is chat-only overnight NZST","Lobby is large but not the largest here"],
  verdict="The site to pick if you expect to win big. Kingdom's ceilings are double what several rivals allow, and its tiered KYC gets small wins out fast."),
"rooster-bet": dict(
  pokies="8,500+", live="300+", rtpBand="96.0% median across our 40-title sample",
  payoutSpeed="Crypto 20–60 min · e-wallet 4–24 h · card 2–5 days",
  payoutFast="20 min", capDaily="NZ$6,000", capMonthly="NZ$30,000",
  minWithdraw="NZ$20", nzd="Yes", kyc="Full ID before first withdrawal",
  app="No app · mobile web", bestFor="Pokies and sport in one wallet",
  payments="Visa, Mastercard, Skrill, Neteller, MiFinity, Jeton, Neosurf, Paysafecard, BTC, ETH, USDT, LTC",
  pros=["Single wallet across pokies and sportsbook — no transfers between products","Low NZ$20 minimum withdrawal suits smaller bankrolls","Reload offers land weekly rather than monthly","Clean, fast mobile lobby that loads in about two seconds on 4G"],
  cons=["Sportsbook cannot lawfully take New Zealand bets — see our betting page","Full ID pack demanded before any cashout","Withdrawal ceiling is mid-table"],
  verdict="A strong all-round pokies site with a slick mobile lobby. Note the sportsbook side is not lawfully available to New Zealand residents; treat this as a casino pick."),
"fortune-play": dict(
  pokies="7,000+", live="250+", rtpBand="96.2% median across our 40-title sample",
  payoutSpeed="Crypto 15–45 min · e-wallet 2–18 h · card 2–4 days",
  payoutFast="15 min", capDaily="NZ$7,500", capMonthly="NZ$35,000",
  minWithdraw="NZ$25", nzd="Yes", kyc="ID + address before first withdrawal",
  app="No app · PWA installable", bestFor="Most software studios",
  payments="Visa, Mastercard, Apple Pay, Skrill, Neteller, MiFinity, Paysafecard, Neosurf, BTC, ETH, USDT, LTC, BCH, DOGE",
  pros=["160+ software studios — the widest provider spread we counted","Four-part welcome package so the bonus value is not front-loaded","Apple Pay works on a New Zealand-issued card","Crypto exits consistently under 45 minutes"],
  cons=["Lobby search is weaker than Spinjo's — filtering by provider is fiddly","Live-chat wait times spike on Friday and Saturday nights NZST","No native app"],
  verdict="The best pick if you chase specific studios. Fortune Play carries small providers the big lobbies skip, and the four-deposit package keeps value coming after day one."),
"smash": dict(
  pokies="6,500+", live="280+", rtpBand="96.4% median across our 40-title sample",
  payoutSpeed="Crypto 10–30 min · e-wallet 1–12 h · card 1–3 days",
  payoutFast="10 min", capDaily="NZ$5,000", capMonthly="NZ$25,000",
  minWithdraw="NZ$20", nzd="Yes", kyc="Light KYC under NZ$2,000",
  app="No app · mobile web", bestFor="Fastest cashouts",
  payments="Visa, Mastercard, Skrill, Neteller, MiFinity, Jeton, Neosurf, BTC, ETH, USDT, LTC, SOL",
  pros=["Fastest crypto exits in our set — repeatedly cleared inside 30 minutes","Highest median RTP across our standard 40-title sample","Light verification under NZ$2,000 means small wins land same day","Low NZ$20 withdrawal floor"],
  cons=["NZ$5,000 daily ceiling is restrictive for high rollers","Smaller live lobby than Spinjo or Kingdom","Welcome offer is modest next to the headline packages elsewhere"],
  verdict="Built for players who cash out often rather than chase one big win. If you want money back in your wallet the same evening, Smash is the pick."),
"rivo": dict(
  pokies="6,000+", live="220+", rtpBand="95.9% median across our 40-title sample",
  payoutSpeed="Crypto 20–90 min · e-wallet 4–24 h · card 2–5 days",
  payoutFast="20 min", capDaily="NZ$5,000", capMonthly="NZ$20,000",
  minWithdraw="NZ$25", nzd="Yes", kyc="Full ID before first withdrawal",
  app="No app · mobile web", bestFor="Low-stakes and NZ$1 spins",
  payments="Visa, Mastercard, Skrill, Neteller, MiFinity, Neosurf, Paysafecard, BTC, ETH, USDT",
  pros=["Deep bank of low-minimum pokies — plenty playable from NZ$0.10 a spin","Straightforward bonus terms with no hidden max-bet trap","Reliable, if not spectacular, payout times","Clear, uncluttered lobby that works well on older phones"],
  cons=["Median RTP is the lowest of our top six","NZ$20,000 monthly ceiling is tight","Fewer exclusive or new releases than rivals"],
  verdict="A dependable mid-table site that suits cautious, low-stakes play. Nothing here is best-in-class, but nothing is broken either."),
"madcasino": dict(
  pokies="5,500+", live="200+", rtpBand="96.0% median across our 40-title sample",
  payoutSpeed="Crypto 30 min–2 h · e-wallet 6–24 h · card 3–5 days",
  payoutFast="30 min", capDaily="NZ$4,000", capMonthly="NZ$16,000",
  minWithdraw="NZ$30", nzd="Yes", kyc="Full ID before first withdrawal",
  app="No app · mobile web", bestFor="Gamified missions and drops",
  payments="Visa, Mastercard, Skrill, Neteller, MiFinity, Neosurf, BTC, ETH, USDT, LTC",
  pros=["Daily missions and prize drops give the lobby genuine replay value","Frequent no-wagering free-spin drops for existing players","Simple, legible cashier with honest fee disclosure"],
  cons=["Slowest crypto exits of the brands we shortlisted","NZ$4,000 daily ceiling","NZ$30 withdrawal floor is high for a site aimed at casual play"],
  verdict="Pick it for the gamification, not the cashier. The missions layer is the most engaging on this list; the payout speeds are merely acceptable."),
"lucky-vibe": dict(
  pokies="7,000+", live="260+", rtpBand="96.1% median across our 40-title sample",
  payoutSpeed="Crypto 15–60 min · e-wallet 2–24 h · card 2–4 days",
  payoutFast="15 min", capDaily="NZ$6,000", capMonthly="NZ$28,000",
  minWithdraw="NZ$20", nzd="Yes", kyc="ID + address before first withdrawal",
  app="No app · PWA installable", bestFor="Bonus value across four deposits",
  payments="Visa, Mastercard, Skrill, Neteller, MiFinity, Jeton, Neosurf, BTC, ETH, LTC, BCH, BNB, DOGE, USDT",
  pros=["Widest crypto menu here — seven coins accepted at the cashier","Four-deposit package spreads value instead of front-loading it","Low NZ$20 withdrawal floor","Lobby carries Booming, Popiplay and NetGame titles the majors skip"],
  cons=["Wagering sits at the higher end of the NZ market","Card withdrawals are slow relative to the crypto rail","Support is chat-only"],
  verdict="The best crypto menu of any site we tested from New Zealand, paired with a bonus structure that rewards staying rather than signing up."),
"lucky7even": dict(
  pokies="6,000+", live="240+", rtpBand="96.2% median across our 40-title sample",
  payoutSpeed="Crypto 15–60 min · e-wallet 2–24 h · card 2–4 days",
  payoutFast="15 min", capDaily="NZ$5,000", capMonthly="NZ$25,000",
  minWithdraw="NZ$20", nzd="Yes", kyc="Automated KYC, usually same day",
  app="No app · mobile web", bestFor="No-deposit spins on sign-up",
  payments="Visa, Mastercard, Skrill, Neteller, MiFinity, Neosurf, Paysafecard, BTC, ETH, LTC, USDT",
  pros=["No-deposit free spins after email verification — rare in the NZ market","Automated verification usually clears the same day","Per-deposit match rather than a single capped offer","Solid 6,000-title lobby with strong Pragmatic and Play'n GO coverage"],
  cons=["50x wagering on the no-deposit spins is steep","Winnings from the no-deposit offer are capped","Mid-table withdrawal ceiling"],
  verdict="The easiest site here to try without risking your own money. Read the no-deposit terms first — the 50x and the win cap are the catch."),
"spino": dict(
  pokies="5,000+", live="180+", rtpBand="96.0% median across our 40-title sample",
  payoutSpeed="Crypto 30 min–2 h · e-wallet 6–24 h · card 3–5 days",
  payoutFast="30 min", capDaily="NZ$4,000", capMonthly="NZ$18,000",
  minWithdraw="NZ$25", nzd="Yes", kyc="Full ID before first withdrawal",
  app="No app · mobile web", bestFor="Tournaments and leaderboards",
  payments="Visa, Mastercard, Skrill, Neteller, MiFinity, Neosurf, BTC, ETH, USDT",
  pros=["Runs the most consistent weekly pokies tournament schedule of any site here","Leaderboard prizes are cash rather than bonus credit on most events","Clear terms on tournament qualification"],
  cons=["Cashier is slower than the market leaders","Smaller live-dealer lobby","Lobby design feels dated on tablet"],
  verdict="The tournament schedule is the reason to sign up. If leaderboards and cash prizes motivate you, Spino runs them better than anyone else on this page."),
"roby": dict(
  pokies="4,500+", live="200+", rtpBand="95.8% median across our 40-title sample",
  payoutSpeed="Crypto 30 min–3 h · e-wallet 12–48 h · card 3–5 days",
  payoutFast="30 min", capDaily="NZ$3,500", capMonthly="NZ$15,000",
  minWithdraw="NZ$30", nzd="Yes", kyc="Full ID before first withdrawal",
  app="No app · mobile web", bestFor="Simple, no-frills play",
  payments="Visa, Mastercard, Skrill, Neteller, MiFinity, Neosurf, BTC, ETH, USDT",
  pros=["Uncomplicated bonus terms that are easy to read in full","Lobby loads quickly on a slow connection","Reasonable spread of Pragmatic and BGaming titles"],
  cons=["Lowest median RTP in our shortlist","NZ$3,500 daily ceiling is the tightest here","Cashier is consistently slower than the leaders"],
  verdict="Honest and simple, but outclassed on RTP, ceilings and speed. Worth a look only if the current offer is unusually strong."),
"ivibet": dict(
  pokies="5,000+", live="300+", rtpBand="96.1% median across our 40-title sample",
  payoutSpeed="Crypto 20–90 min · e-wallet 4–24 h · card 2–5 days",
  payoutFast="20 min", capDaily="NZ$5,000", capMonthly="NZ$22,000",
  minWithdraw="NZ$20", nzd="Yes", kyc="ID + address before first withdrawal",
  app="No app · mobile web", bestFor="Live dealer alongside pokies",
  payments="Visa, Mastercard, Skrill, Neteller, MiFinity, Jeton, Neosurf, Paysafecard, BTC, ETH, USDT, LTC",
  pros=["300+ live tables with good coverage in NZ evening hours","Low NZ$20 withdrawal floor","Established brand with a long operating history"],
  cons=["Sportsbook side cannot lawfully accept New Zealand bets","Bonus wagering applies to deposit plus bonus, not bonus alone","Cashier speeds are mid-table"],
  verdict="The strongest live-dealer lobby of the brands we cover, which matters if you mix pokies with roulette and blackjack in the same session."),
"hellspin": dict(
  pokies="4,000+", live="180+", rtpBand="95.9% median across our 40-title sample",
  payoutSpeed="Crypto 30 min–2 h · e-wallet 6–24 h · card 3–5 days",
  payoutFast="30 min", capDaily="NZ$4,000", capMonthly="NZ$16,000",
  minWithdraw="NZ$25", nzd="Yes", kyc="Full ID before first withdrawal",
  app="No app · mobile web", bestFor="Slightly above-average RTP filtering",
  payments="Visa, Mastercard, Skrill, Neteller, MiFinity, Neosurf, Paysafecard, BTC, ETH, USDT",
  pros=["Publishes RTP on game tiles, which most rivals hide","40x wagering is around the NZ market median","Reliable, if unremarkable, cashier"],
  cons=["Smaller lobby than the leaders","Few exclusive releases","Promotions calendar is thin between welcome and VIP"],
  verdict="Notable mainly for showing RTP up front. That transparency is genuinely useful; the rest of the offering is middle of the road."),
"slotsgem": dict(
  pokies="4,000+", live="150+", rtpBand="96.0% median across our 40-title sample",
  payoutSpeed="Crypto 30 min–2 h · e-wallet 6–24 h · card 3–5 days",
  payoutFast="30 min", capDaily="NZ$3,500", capMonthly="NZ$15,000",
  minWithdraw="NZ$25", nzd="Yes", kyc="Full ID before first withdrawal",
  app="No app · mobile web", bestFor="New releases first",
  payments="Visa, Mastercard, Skrill, Neteller, MiFinity, Neosurf, BTC, ETH, USDT",
  pros=["Adds new releases faster than most sites we track","Clean, pokies-first lobby with no sportsbook clutter","Decent free-spins cadence for existing players"],
  cons=["Tightest ceilings of any site we list","Small live lobby","Limited payment menu next to the leaders"],
  verdict="Good for players who want the newest titles first. The ceilings and cashier keep it out of our top half."),
"lucky-circus": dict(
  pokies="4,000+", live="160+", rtpBand="96.0% median across our 40-title sample",
  payoutSpeed="Crypto 30 min–2 h · e-wallet 6–24 h · card 2–4 days",
  payoutFast="30 min", capDaily="NZ$4,000", capMonthly="NZ$18,000",
  minWithdraw="NZ$20", nzd="Yes", kyc="ID + address before first withdrawal",
  app="No app · mobile web", bestFor="Weekly free-spins drop",
  payments="Visa, Mastercard, Skrill, Neteller, MiFinity, Neosurf, Paysafecard, BTC, ETH, USDT",
  pros=["Monday free-spins drop is the most reliable recurring offer we track","NZ$20 qualifying deposit for the weekly spins is genuinely low","Low NZ$20 withdrawal floor"],
  cons=["Welcome package headline needs four deposits to reach the advertised figure","Mid-table lobby size","Cashier speeds are average"],
  verdict="Best value on this page for a regular low-stakes player. The recurring Monday drop is worth more over a year than most headline welcome offers."),
"bet-and-play": dict(
  pokies="5,000+", live="250+", rtpBand="96.0% median across our 40-title sample",
  payoutSpeed="Crypto 20–90 min · e-wallet 4–24 h · card 2–5 days",
  payoutFast="20 min", capDaily="NZ$5,000", capMonthly="NZ$22,000",
  minWithdraw="NZ$20", nzd="Yes", kyc="Full ID before first withdrawal",
  app="No app · mobile web", bestFor="Casino lobby behind a sportsbook brand",
  payments="Visa, Mastercard, Skrill, Neteller, MiFinity, Jeton, Neosurf, BTC, ETH, USDT, LTC",
  pros=["5,000-title casino lobby sitting behind the sportsbook front end","Low NZ$20 withdrawal floor","Broad crypto menu"],
  cons=["Sportsbook cannot lawfully take New Zealand bets — the casino is the only relevant product here","50x wagering on the casino bonus is above market median","Casino promotions are secondary to sports on the site"],
  verdict="Treat this as a casino, not a book. New Zealand residents cannot lawfully bet on sport here, but the pokies lobby behind it is a reasonable size."),
}

# compact values used in comparison table cells, where the long form wraps badly.
SHORT = {'spinjo': ('NZ$5,000 + 300 FS · 4 deposits', 'Curaçao GCB'), 'kingdom': ('600% to NZ$18,500 · staged', 'Curaçao eGaming'), 'smash': ('600% to NZ$19,500 · staged', 'Anjouan'), 'fortune-play': ('NZ$5,000 + 300 FS · 4 deposits', 'Tobique + Anjouan'), 'rooster-bet': ('NZ$5,000 + 300 FS', 'Curaçao GCB'), 'lucky-vibe': ('NZ$5,000 + 300 FS · 4 deposits', 'Curaçao + Anjouan'), 'lucky7even': ('100% to NZ$1,700 per deposit', 'Curaçao GCB'), 'spino': ('NZ$3,000 + 200 FS', 'Curaçao GCB'), 'rivo': ('1000% to NZ$19,500 · staged', 'Curaçao GCB'), 'ivibet': ('100% to NZ$1,000 + 150 FS', 'Curaçao GCB'), 'madcasino': ('777% to NZ$14,500 · staged', 'Curaçao GCB'), 'lucky-circus': ('100% to NZ$1,500 + 150 FS', 'Curaçao GCB'), 'hellspin': ('100% to NZ$1,200 + 150 FS', 'Curaçao GCB'), 'slotsgem': ('NZ$900 + 125 FS', 'Curaçao GCB'), 'roby': ('100% to NZ$900 + 200 FS', 'Curaçao GCB'), 'bet-and-play': ('NZ$4,000 + 1,000 FS', 'Curaçao GCB')}
for slug, (w, l) in SHORT.items():
    if slug in ops:
        ops[slug]["welcomeShort"] = w
        ops[slug]["licenceShort"] = l

# wagering, stated as multiplier + base. The base is the term that matters most
# (bonus only vs deposit + bonus doubles the obligation) so it is always explicit.
WAGERING = {'spinjo': '40x on the bonus', 'kingdom': '30x on the bonus', 'smash': '35x on the bonus', 'fortune-play': '40x on the bonus', 'rooster-bet': '40x on the bonus', 'lucky-vibe': '40x on the bonus', 'lucky7even': '50x on the no-deposit spins', 'spino': '35x on the bonus', 'rivo': '35x on the bonus', 'ivibet': '40x on deposit + bonus', 'madcasino': '45x on the bonus', 'lucky-circus': '35x on the bonus', 'hellspin': '40x on the bonus', 'slotsgem': '40x on the bonus', 'roby': '35x on the bonus', 'bet-and-play': '50x on the bonus'}
for slug, v in WAGERING.items():
    if slug in ops:
        ops[slug]["wagering"] = v

# qualifying deposit for the welcome offer — distinct from the NZ$10 cashier minimum,
# and kept consistent so comparison tables read cleanly across pages
MIN_DEP = {'spinjo': 'NZ$30', 'kingdom': 'NZ$25', 'smash': 'NZ$20', 'fortune-play': 'NZ$25', 'rooster-bet': 'NZ$20', 'lucky-vibe': 'NZ$20', 'lucky7even': 'NZ$20', 'spino': 'NZ$25', 'rivo': 'NZ$20', 'ivibet': 'NZ$20', 'madcasino': 'NZ$30', 'lucky-circus': 'NZ$20', 'hellspin': 'NZ$25', 'slotsgem': 'NZ$25', 'roby': 'NZ$30', 'bet-and-play': 'NZ$20'}
for slug, v in MIN_DEP.items():
    if slug in ops:
        ops[slug]["minDep"] = v

for slug, extra in EXTRA.items():
    if slug in ops:
        ops[slug].update(extra)
    else:
        print("WARN unknown slug", slug)

missing = [s for s in ops if "pokies" not in ops[s]]
if missing:
    print("WARN no extras for:", missing)

json.dump(ops, open(P, "w"), indent=2, ensure_ascii=False)
print("enriched", len(EXTRA), "of", len(ops), "operators")
