#!/usr/bin/env python3
"""Standardise the opening of every commercial page fragment to:

    <!--TOPLIST ...-->   affiliate table, sitting directly under the hero
    <!--SNIPPET ...-->   quick answer, directly under the table
    <!--TOC-->           contents list
    ...prose

Any existing TOPLIST / SNIPPET / TOC is lifted out and re-placed in that order,
so the ordering is enforced rather than depending on how a fragment was authored.
An explicit <!--TOC--> is required on these pages: without it the builder puts the
contents list at the very top, above the affiliate table.
"""
import os, re, sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pages")

def split_fm(s):
    m = re.match(r"\s*<!--@(.*?)@-->\n?", s, re.S)
    return s[:m.end()], s[m.end():]

def lift(body, tag):
    """Remove the first occurrence of a shortcode and return (body, shortcode)."""
    m = re.search(r"<!--%s\b.*?-->\n?" % tag, body, re.S)
    if not m:
        return body, None
    return body[:m.start()] + body[m.end():], m.group(0).rstrip("\n")

def apply(fn, toplist=None, snippet=None):
    path = os.path.join(SRC, fn)
    fm, body = split_fm(open(path, encoding="utf-8").read())

    body, existing_top = lift(body, "TOPLIST")
    body, existing_sni = lift(body, "SNIPPET")
    body, _            = lift(body, "TOC")

    top = existing_top or toplist
    sni = existing_sni or snippet
    if not top:
        sys.exit(f"  !! {fn}: no TOPLIST supplied and none found")

    head = top + "\n\n"
    if sni:
        head += sni + "\n\n"
    head += "<!--TOC-->\n\n"

    open(path, "w", encoding="utf-8").write(fm + head + body.lstrip("\n"))
    made = []
    if not existing_top: made.append("toplist")
    if sni and not existing_sni: made.append("snippet")
    print(f"  {fn:32} ordered" + (f" (+{', '.join(made)})" if made else ""))
