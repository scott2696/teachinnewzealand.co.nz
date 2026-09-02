# Brand logos

Master logo set for all sites under `MY_SITES/`. Copy this folder into a site as
`<site>/logos/` and reference images as `/logos/<file>`.

All artwork here is the **dark/coloured** variant, chosen to sit on the white
`.toplist-logo` tile (`background:#fff`). Note the vendors' folder naming is
inverted from what you'd expect — in the Brand Materials drive, "Light Logo"
means *for light backgrounds*, i.e. dark artwork. Variants were picked by
measuring mean luminance, not by folder name.

| Brand        | File                     | Notes                          |
|--------------|--------------------------|--------------------------------|
| Spinjo       | `spinjo.png`             |                                |
| Lucky Circus | `lucky-circus.jpg`       |                                |
| Lucky7even   | `lucky7even.jpg`         |                                |
| Lucky Vibe   | `lucky-vibe.jpg`         |                                |
| Roby Casino  | `roby-casino.jpg`        |                                |
| Spino        | `spino.jpg`              |                                |
| Ivibet       | `ivibet.png`             | casino logo                    |
| Ivibet       | `ivibet-sportsbook.jpg`  | use on sportsbook pages        |
| Hellspin     | `hellspin.jpg`           |                                |
| Slotgem      | `slotgem.jpg`            |                                |
| Bet&Play     | `betandplay.png`         |                                |
| Kingdom      | `kingdom.png`            | from Brand Materials drive     |
| MadCasino    | `madcasino.png`          | EN variant (RU also available) |
| Rivo         | `rivo.png`               | from Brand Materials drive     |
| Smash        | `smash.png`              | from Brand Materials drive     |

Vector originals for the four newest brands live in `svg/`. Prefer these where
the layout allows — they stay crisp at any size.

## Still missing

- **SpinsUp** — no asset yet. It is also held out of the site entirely until it
  gets its own affiliate link (its current one is Fortune Play's).

Rooster Bet and Fortune Play were supplied directly rather than via the drive.
Both arrived on white backgrounds with heavy padding, so near-white borders were
cropped before resizing — otherwise `object-fit:contain` letterboxes them and
they render visibly smaller than the rest of the set.

Wired into every `data-logo-slot` on `11woodward.co.nz` (see
`scratchpad/wire_logos.py` pattern: replaces the slot's fallback text with an
`<img>` keyed on the brand name).

## Slotgem corner artifacts

The original `slotgem.jpg` sits on a white rounded-rectangle card. JPEG has no
alpha channel, so the four areas outside that rounded rect encoded as solid
black — four dark 8x8 blobs, one per corner, clearly visible against the white
`.toplist-logo` tile.

Fixed by flood-filling inward from each corner and writing the result as PNG
with those regions transparent, so it now sits correctly on any background.
`slotgem.jpg` is kept as the untouched original; `slotgem.png` is the one to use.

Watch for this on any other logo supplied as JPEG with rounded corners.
