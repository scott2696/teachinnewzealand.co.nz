#!/usr/bin/env python3
"""Helpers for growing a page fragment: insert a block before an anchor, and
append extra FAQ entries to the page's existing FAQ list."""
import sys

def ins(path, anchor, block):
    s = open(path, encoding='utf-8').read()
    if anchor not in s:
        sys.exit(f"  !! anchor missing in {path}: {anchor[:50]}")
    open(path, 'w', encoding='utf-8').write(s.replace(anchor, block + "\n\n" + anchor, 1))
    print(f"  ok {path.split('/')[-1]} (+block)")

def faqs(path, items):
    s = open(path, encoding='utf-8').read()
    j = s.rfind('</details>')
    if j == -1:
        sys.exit(f"  !! no FAQ list in {path}")
    j += len('</details>')
    block = "".join(
        f'\n\n<details class="faq-i"><summary>{q}</summary><div class="faq-a">\n<p>{a}</p></div></details>'
        for q, a in items)
    open(path, 'w', encoding='utf-8').write(s[:j] + block + s[j:])
    print(f"  ok {path.split('/')[-1]} (+{len(items)} FAQ)")
