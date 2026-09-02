#!/usr/bin/env python3
"""Compute each operator's score from the published methodology weights.

The weights on /how-we-review/ are the ones applied here, so the ranking on the
site is derivable from the data rather than asserted. Editing any input in
operators.json reorders every list on the site on the next build.

    30%  payout speed and reliability   (fastest verified payout)
    25%  withdrawal ceilings + cashier  (daily, monthly, minimum withdrawal)
    20%  served RTP                     (median across the fixed 40-title sample)
    15%  bonus fairness                 (wagering multiplier and its base)
    10%  lobby and live coverage        (pokies count, live tables)
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "_build", "operators.json")
ops = json.load(open(P))

def num(v):
    m = re.search(r"[\d,]+(?:\.\d+)?", str(v or ""))
    return float(m.group(0).replace(",", "")) if m else None

def norm(vals, higher_is_better):
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return {k: 0.5 for k in vals}
    return None  # unused; kept explicit below

def scale(x, lo, hi, higher_is_better):
    if hi == lo:
        return 0.5
    t = (x - lo) / (hi - lo)
    return t if higher_is_better else 1 - t

def bonus_score(op):
    """Lower wagering is better; a deposit+bonus base doubles the real obligation."""
    w = str(op.get("wagering", ""))
    m = re.search(r"(\d+)\s*x", w)
    if not m:
        return 0.5
    mult = float(m.group(1))
    if "deposit" in w.lower():
        mult *= 2
    return mult

FIELDS = {
    "speed":  lambda o: num(o.get("payoutFast")),
    "capD":   lambda o: num(o.get("capDaily")),
    "capM":   lambda o: num(o.get("capMonthly")),
    "minW":   lambda o: num(o.get("minWithdraw")),
    "rtp":    lambda o: num(o.get("rtpBand")),
    "bonus":  bonus_score,
    "pokies": lambda o: num(o.get("pokies")),
    "live":   lambda o: num(o.get("live")),
}
raw = {f: {k: fn(v) for k, v in ops.items()} for f, fn in FIELDS.items()}
for f in raw:
    fill = sorted(x for x in raw[f].values() if x is not None)
    med = fill[len(fill) // 2] if fill else 0
    for k in raw[f]:
        if raw[f][k] is None:
            raw[f][k] = med

rng = {f: (min(raw[f].values()), max(raw[f].values())) for f in raw}

BETTER = {"speed": False, "capD": True, "capM": True, "minW": False,
          "rtp": True, "bonus": False, "pokies": True, "live": True}

scores = {}
for k in ops:
    n = {f: scale(raw[f][k], rng[f][0], rng[f][1], BETTER[f]) for f in raw}
    composite = (
        0.30 * n["speed"] +
        0.25 * (0.45 * n["capD"] + 0.45 * n["capM"] + 0.10 * n["minW"]) +
        0.20 * n["rtp"] +
        0.15 * n["bonus"] +
        0.10 * (0.7 * n["pokies"] + 0.3 * n["live"])
    )
    # map the 0-1 composite onto a 7.2-9.4 band out of 10, then store out of 5
    out10 = 7.2 + composite * 2.2
    scores[k] = round(out10 / 2, 2)

for k, v in scores.items():
    ops[k]["rating"] = v
json.dump(ops, open(P, "w"), indent=2, ensure_ascii=False)

print(f"{'operator':22} {'/10':>5}   speed  capD    rtp   wager")
for k, v in sorted(scores.items(), key=lambda kv: -kv[1]):
    o = ops[k]
    print(f"{o['name']:22} {v*2:5.1f}   {o.get('payoutFast',''):>6} "
          f"{o.get('capDaily',''):>9}  {o.get('rtpBand','')[:5]:>6}  {o.get('wagering','')[:22]}")
