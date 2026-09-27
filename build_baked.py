#!/usr/bin/env python3
"""BAKED GOODS — the Garden's cookbook of fixes that worked, each written as a recipe (ingredients = tools, method = steps).
Recipes live in recipes/*.json (Chronic adds new ones weekly from the vault and the week's successful fixes).

Usage: build_baked.py     -> site/index.html (the whole cookbook, tappable table of contents) + latest.json
"""
import datetime as dt, glob, json, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
sys.path.insert(0, ROOT)
import pubkit as pk   # noqa: E402
import flipbook as fb   # noqa: E402
from pubkit import e   # noqa: E402

fb.CSS_FILE = "baked-goods.css"
REPO = "https://github.com/real-CAK3D/BakedGoods"
ORDER = ["Raspberry Pi", "Home Assistant", "Network & Tailscale", "Hermes & Agents", "Windows PCs", "Web & Cloud", "The Vault", "Odds & Ends"]


def recipes():
    rs = [pk.load(f) for f in glob.glob(os.path.join(ROOT, "recipes", "*.json"))]
    rs = [r for r in rs if r.get("title") and r.get("steps")]
    for r in rs:
        r["category"] = r.get("category") if r.get("category") in ORDER else "Odds & Ends"
    return sorted(rs, key=lambda r: (ORDER.index(r["category"]), r["title"]))


def recipe_page(r):
    ing = "".join("<li>%s</li>" % e(x) for x in r.get("ingredients") or [])
    steps = "".join("<li>%s</li>" % e(x) for x in r.get("steps") or [])
    tips = "".join("<li>%s</li>" % e(x) for x in r.get("tips") or [])
    return ('<div class="bg-recipe"><div class="bg-cat">%s</div><h2 class="bg-title">%s</h2><p class="bg-intro">%s</p>'
            '<div class="bg-meta"><span>🍽 Serves: <b>%s</b></span><span>⏲ Prep: <b>%s</b></span><span>🔥 Difficulty: <b>%s</b></span></div>'
            '<div class="bg-cols"><div class="bg-ing"><h4>Ingredients</h4><ul>%s</ul></div><div class="bg-steps"><h4>Method</h4><ol>%s</ol></div></div>%s'
            '<div class="bg-by">%s<span>Baked by %s · %s%s</span></div></div>'
            % (e(r["category"]), e(r["title"]), e(r.get("intro")), e(r.get("serves") or "the Garden"), e(r.get("prep") or "—"), e(r.get("difficulty") or "medium"),
               ing, steps, ('<div class="bg-tips"><h4>Chef\'s tips</h4><ul>%s</ul></div>' % tips) if tips else "", fb.mug(r.get("agent") or "CHRONIC", "mug sm"),
               e(r.get("agent") or "CHRONIC"), e(pk.nice(r.get("date", ""), "%B %-d, %Y")), (" · " + e(r["source"])) if r.get("source") else ""))


def build():
    pk.sync_portraits(SITE)
    rs = recipes()
    today = dt.date.today()
    seal = '<a class="seal" href="/" aria-label="Back to The Corner Chronicle">%s</a>' % fb.SEAL
    body, toc, n = [], [], 3   # 1 cover, 2 contents
    cats = {}
    for r in rs:
        cats.setdefault(r["category"], []).append((r, n))
        body.append(fb.page(r["title"], recipe_page(r)))
        n += 1
    toc = "".join('<div class="bg-toc-cat"><h4>%s</h4><ol>%s</ol></div>' % (e(c), "".join('<li><a data-goto="%d">%s <span>%s</span></a></li>' % (pg, e(r["title"]), e(r.get("prep") or "")) for r, pg in items))
                  for c, items in cats.items())
    newest = max(rs, key=lambda r: r.get("date", "")) if rs else {}
    mo = today.strftime("%Y-%m")
    art = pk.draw_image(os.path.join(SITE, "img", "covers", mo + ".jpg"), (
        "Bright, airy editorial food photograph for the cover of an upscale home-living and entertaining magazine, vertical, no text or lettering. "
        "A beautiful homemade %s dessert (a lattice-top fruit pie or a frosted layer cake, whichever suits the season) on a white footed cake stand, "
        "set on a pale sage-green linen with a vintage silver cake server and a small sprig of fresh herbs; as a playful garnish, one tiny green circuit board "
        "tucked beside the plate like a place card. Soft north-window daylight, gentle shadows, pastel palette, crisp and elegant styling, shallow depth of field. "
        "The top third is clean soft white background with nothing in it, and the left edge is calm and uncluttered for cover lines." % pk.SEASONS.get(today.month, "autumn")),
        size="1024x1536")
    pages = [fb.page("Baked Goods", (
        '<div class="mx%s">%s<div class="mx-kick">THE GARDEN KITCHEN</div><h1 class="mx-t">Baked Goods</h1><div class="mx-date">%s · %d RECIPES</div>'
        '<div class="mx-lines"><div><small>Fresh this week</small><b>%s</b></div><div><small>Tried &amp; tested</small><b>Fixes that actually worked</b></div>'
        '<div><small>Inside</small><b>Pi · Home Assistant · Agents</b></div></div><div class="mx-foot"><span class="mx-seal">%s</span><span>Open the cookbook ›</span></div></div>')
        % ("" if art else " mx-noimg", ('<img class="mx-photo" src="../img/covers/%s.jpg" alt="A styled homemade dessert">' % mo) if art else "",
           today.strftime("%B %Y").upper(), len(rs), e(newest.get("title") or "The first batch"), seal), " hardcover bg-cov"),
             fb.page("Contents", '<div class="bg-toc"><h2 class="bg-title">What\'s Cooking</h2><p class="small">Tap a recipe to turn to it.</p>%s</div>' % (toc or '<p>No recipes yet.</p>'))]
    pages += body
    pages.append(fb.page("Back Page", ('<div class="gum"><span>BAKED GOODS · THE GARDEN KITCHEN</span></div><div class="pb-body">%s<h2 class="pb-title">Baked Goods</h2>'
                                       '<p>Every recipe is a fix that actually worked in the Garden.<br>Collected by CHRONIC from the vault and the week\'s follow-ups.</p>%s'
                                       '<p class="pb-code">%d recipes · updated %s</p></div>') % (seal, fb.back_codes(REPO, "BakedGoods"), len(rs), today.isoformat()), " hardcover back"))
    html = fb.book(pages, date=today.isoformat(), no=len(rs), lists={}, paper="Baked Goods", motto="Tried, tested & fresh out of the oven",
                   gum="HOME-BAKED FIXES · TESTED IN THE GARDEN", price="PRICE: ONE BROWNIE", delivered="COLLECTED BY CHRONIC",
                   flap="Baked Goods · the Garden's cookbook of fixes", body_class="pub-bg", est="THE GARDEN KITCHEN · EST. 2026")
    open(os.path.join(SITE, "index.html"), "w").write(html.replace('href="../', 'href="').replace('src="../', 'src="'))
    dates = sorted({r.get("date", "") for r in rs if r.get("date")}, reverse=True)
    pk.latest(SITE, "Baked Goods", dates[0] if dates else today.isoformat(), "%d recipes — fresh: %s" % (len(rs), newest.get("title") or "—"), "", dates[:10],
              cover=("img/covers/%s.jpg" % mo) if art else "")
    print("baked goods built: %d recipes" % len(rs))


if __name__ == "__main__":
    build()
