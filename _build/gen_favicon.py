#!/usr/bin/env python3
"""Generate the Pokies Kiwi favicon set.

Mark: kowhai-gold rounded tile, deep-pounamu 'K' letterform with a spin dot.
Rendered at 8x and downsampled with LANCZOS so the 48px tile stays crisp.
Sizes required: 48, 96, 144, 192 (multiples of 48) plus 512, ico and apple-touch.
"""
import os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOLD_A, GOLD_B = (255, 201, 76), (224, 158, 12)
INK = (10, 43, 38)

def render(px):
    S = px * 8
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # vertical gold gradient inside a rounded square
    grad = Image.new("RGB", (1, S))
    gd = ImageDraw.Draw(grad)
    for y in range(S):
        t = y / max(1, S - 1)
        gd.point((0, y), fill=tuple(int(GOLD_A[i] + (GOLD_B[i] - GOLD_A[i]) * t) for i in range(3)))
    grad = grad.resize((S, S))

    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 0.225), fill=255)
    img.paste(grad, (0, 0), mask)

    # 'K' letterform: stem + two diagonals, drawn as thick round-capped lines
    w   = int(S * 0.135)                 # stroke weight
    x0  = int(S * 0.30)                  # stem x
    top = int(S * 0.255)
    bot = int(S * 0.775)
    mid = int(S * 0.545)
    d.line([(x0, top), (x0, bot)], fill=INK, width=w, joint="curve")
    d.line([(x0, mid), (int(S * 0.665), top)], fill=INK, width=w, joint="curve")
    d.line([(int(S * 0.435), mid - int(S * 0.028)), (int(S * 0.715), bot)], fill=INK, width=w, joint="curve")
    for pt in [(x0, top), (x0, bot), (int(S * 0.665), top), (int(S * 0.715), bot)]:
        d.ellipse([pt[0] - w // 2, pt[1] - w // 2, pt[0] + w // 2, pt[1] + w // 2], fill=INK)

    # spin dot, top right
    r = int(S * 0.072)
    cx, cy = int(S * 0.775), int(S * 0.252)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=INK)

    return img.resize((px, px), Image.LANCZOS)

sizes = [16, 32, 48, 96, 144, 192, 512]
imgs = {}
for s in sizes:
    im = render(s)
    imgs[s] = im
    if s in (48, 96, 144, 192, 512):
        im.save(os.path.join(ROOT, f"favicon-{s}x{s}.png"), optimize=True)
    if s in (16, 32):
        im.save(os.path.join(ROOT, f"favicon-{s}x{s}.png"), optimize=True)

render(180).convert("RGB").save(os.path.join(ROOT, "apple-touch-icon.png"), optimize=True)
imgs[48].save(os.path.join(ROOT, "favicon.ico"),
              sizes=[(16, 16), (32, 32), (48, 48)],
              append_images=[imgs[16], imgs[32]])

SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" role="img" aria-label="Pokies Kiwi">
<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#FFC94C"/><stop offset="1" stop-color="#E09E0C"/></linearGradient></defs>
<rect width="48" height="48" rx="10.8" fill="url(#g)"/>
<g stroke="#0A2B26" stroke-width="6.5" stroke-linecap="round" fill="none">
<path d="M14.4 12.2V37.2"/><path d="M14.4 26.2 31.9 12.2"/><path d="M20.9 24.8 34.3 37.2"/>
</g><circle cx="37.2" cy="12.1" r="3.5" fill="#0A2B26"/></svg>
'''
open(os.path.join(ROOT, "favicon.svg"), "w").write(SVG)

MANIFEST = '''{
  "name": "Pokies Kiwi — NZ Online Pokies & Casino Guide",
  "short_name": "Pokies Kiwi",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#F6F4EF",
  "theme_color": "#0A2B26",
  "lang": "en-NZ",
  "icons": [
    { "src": "/favicon-48x48.png",   "sizes": "48x48",   "type": "image/png" },
    { "src": "/favicon-96x96.png",   "sizes": "96x96",   "type": "image/png" },
    { "src": "/favicon-144x144.png", "sizes": "144x144", "type": "image/png" },
    { "src": "/favicon-192x192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable" },
    { "src": "/favicon-512x512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable" }
  ]
}
'''
open(os.path.join(ROOT, "site.webmanifest"), "w").write(MANIFEST)
print("favicons written:", ", ".join(f"{s}x{s}" for s in sizes))
