#!/usr/bin/env python3
"""Mirror one RSS feed as an excerpt.

Two jobs, and the first one is the important one:

1. Refuse to pass on anything that isn't a feed. If Cloudflare ever starts
   challenging GitHub's runners the way it challenges Vercel's, this must fail
   loudly rather than write 5KB of "Just a moment..." into the mirror — pegboard's
   parser would read that as a feed with zero items, which is a silent outage.

2. Cut each item's body down to an excerpt. ResetEra emits no <description>, so
   the blurb pegboard ranks and renders comes from <content:encoded>, which is
   the whole quoted post. Mirroring those verbatim would republish the forum;
   mirroring ~600 characters of stripped text is a link index, and pegboard's
   blurbFrom() calls stripHtml() on it anyway. Ranking reads ~375 characters.
"""
import html
import re
import sys

EXCERPT_CHARS = 600
MIN_ITEMS = 5
MIN_BYTES = 5_000


def fail(msg):
    print(f"::error::{msg}", file=sys.stderr)
    sys.exit(1)


def strip_html(raw: str) -> str:
    text = re.sub(r"<(script|style)\b.*?</\1>", " ", raw, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def excerpt(text: str) -> str:
    if len(text) <= EXCERPT_CHARS:
        return text
    cut = text[:EXCERPT_CHARS]
    # Back off to a word boundary so the excerpt doesn't end mid-word.
    space = cut.rfind(" ")
    return (cut[:space] if space > EXCERPT_CHARS * 0.6 else cut).rstrip() + "…"


def cdata(text: str) -> str:
    # Nothing can close the section early once ]]> is gone.
    return f"<![CDATA[{text.replace(']]>', ']] >')}]]>"


def main(src: str, dst: str) -> None:
    raw = open(src, encoding="utf-8", errors="replace").read()

    if len(raw) < MIN_BYTES:
        fail(f"{len(raw)} bytes is too small to be the feed — a challenge or error page?")
    if "<rss" not in raw[:2000]:
        head = strip_html(raw)[:200]
        fail(f"no <rss> element; got: {head}")
    items = raw.count("<item>")
    if items < MIN_ITEMS:
        fail(f"only {items} items — the feed normally carries 40")

    def shrink(m):
        return f"<content:encoded>{cdata(excerpt(strip_html(m.group(1))))}</content:encoded>"

    out = re.sub(r"<content:encoded>(.*?)</content:encoded>", shrink, raw, flags=re.S)

    with open(dst, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"{items} items, {len(raw)} bytes in, {len(out)} bytes out")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
