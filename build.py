#!/usr/bin/env python3
import csv, os, sys, re, html
from pathlib import Path

def slugify(s):
    return re.sub(r"[^a-z0-9\-]+","-", (s or "").lower()).strip("-")

def pick(d, keys, default=""):
    for k in keys:
        if k in d and d[k]:
            return str(d[k]).strip()
    return default

def read_rows(csv_file):
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    norm = []
    for i, r in enumerate(rows):
        name = pick(r, ["Name","Title","Offer_Name"], "")
        if not name:
            continue
        slug = pick(r, ["Slug","slug"], "") or slugify(f"{name}-{i+1}")
        desc = pick(r, ["Description","Desc","Body"], "")
        link = pick(r, ["Link","URL","Affiliate_Link"], "#")
        cat  = pick(r, ["Category","category","Cat"], "") or "General"
        price = pick(r, ["Price","price"], "")
        badge = pick(r, ["Badge","badge"], "")
        norm.append({
            "name": name, "slug": slug, "desc": desc, "link": link,
            "cat": cat, "cat_slug": slugify(cat), "price": price, "badge": badge
        })
    return norm

CSS = (
"body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial;margin:0;color:#111}"
"header{position:sticky;top:0;background:#fff;border-bottom:1px solid #eee}"
".wrap{max-width:1100px;margin:0 auto;padding:16px}"
"h1{font-size:28px;margin:12px 0}"
".grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}"
".card{display:block;border:1px solid #eee;border-radius:14px;padding:14px;text-decoration:none;color:inherit;transition:box-shadow .15s}"
".card:hover{box-shadow:0 6px 22px rgba(0,0,0,.08)}"
".muted{color:#666;font-size:14px;margin:6px 0 0}"
".btn{display:inline-block;padding:10px 14px;border-radius:10px;border:1px solid #111;text-decoration:none}"
".badge{display:inline-block;background:#111;color:#fff;padding:2px 8px;border-radius:999px;font-size:12px;margin-left:6px}"
".toprow{display:flex;gap:10px;align-items:center;justify-content:space-between;flex-wrap:wrap}"
"nav a{margin-right:10px}"
"small{color:#666}"
)

def write_home(out, site_title, nav_html, items):
    path = out / "index.html"
    with open(path, "w", encoding="utf-8") as f:
        f.write("<!doctype html><meta charset='utf-8'>")
        f.write("<title>"+html.escape(site_title)+"</title>")
        f.write("<link rel='stylesheet' href='styles.css'>")
        f.write("<header><div class='wrap toprow'>")
        f.write("<div><strong>"+html.escape(site_title)+"</strong></div>")
        f.write("<nav>"+nav_html+"</nav></div></header>")
        f.write("<main class='wrap'><h1>Top Picks</h1><div class='grid'>")
        for r in items[:20]:
            href = ("/"+r["slug"]+".html") if r["cat_slug"]=="general" else ("/"+r["cat_slug"]+"/"+r["slug"]+".html")
            badge_html = ("<span class='badge'>"+html.escape(r["badge"])+"</span>") if r["badge"] else ""
            f.write("<a class='card' href='"+href+"'><h3>"+html.escape(r["name"])+badge_html+"</h3>")
            f.write("<p class='muted'>"+html.escape((r['desc'] or '')[:160])+"</p></a>")
        f.write("</div></main>")

def write_category(out, site_title, nav_html, cat_name, cat_slug, rows):
    d = out / cat_slug
    d.mkdir(parents=True, exist_ok=True)
    path = d / "index.html"
    with open(path, "w", encoding="utf-8") as f:
        f.write("<!doctype html><meta charset='utf-8'>")
        f.write("<title>"+html.escape(cat_name)+" – "+html.escape(site_title)+"</title>")
        f.write("<link rel='stylesheet' href='../styles.css'>")
        f.write("<header><div class='wrap toprow'>")
        f.write("<div><a href='../index.html' style='text-decoration:none;color:inherit'>← "+html.escape(site_title)+"</a></div>")
        f.write("<nav>"+nav_html+"</nav></div></header>")
        f.write("<main class='wrap'><h1>"+html.escape(cat_name)+"</h1><div class='grid'>")
        for r in rows:
            href = ("/"+r["slug"]+".html") if cat_slug=="general" else ("/"+cat_slug+"/"+r["slug"]+".html")
            badge_html = ("<span class='badge'>"+html.escape(r["badge"])+"</span>") if r["badge"] else ""
            f.write("<a class='card' href='"+href+"'><h3>"+html.escape(r["name"])+badge_html+"</h3>")
            f.write("<p class='muted'>"+html.escape(r['desc'] or '')+"</p></a>")
        f.write("</div></main>")

def write_offer(out, site_title, nav_html, r):
    # decide folder
    if r["cat_slug"]=="general":
        path = out / (r["slug"]+".html")
        rel_css = "styles.css"
        back = "index.html"
    else:
        d = out / r["cat_slug"]
        d.mkdir(parents=True, exist_ok=True)
        path = d / (r["slug"]+".html")
        rel_css = "../styles.css"
        back = "../index.html"

    badge_html = ("<span class='badge'>"+html.escape(r["badge"])+"</span>") if r["badge"] else ""
    price_html = (" · <strong>$"+html.escape(r["price"])+"</strong>") if r["price"] else ""

    with open(path, "w", encoding="utf-8") as f:
        f.write("<!doctype html><meta charset='utf-8'>")
        f.write("<title>"+html.escape(r["name"])+" – "+html.escape(site_title)+"</title>")
        f.write("<link rel='stylesheet' href='"+rel_css+"'>")
        f.write("<header><div class='wrap toprow'>")
        f.write("<div><a href='"+back+"' style='text-decoration:none;color:inherit'>← "+html.escape(site_title)+"</a></div>")
        f.write("<nav>"+nav_html+"</nav></div></header>")
        f.write("<main class='wrap'>")
        f.write("<h1 style='display:flex;align-items:center;gap:8px'>"+html.escape(r["name"])+badge_html+"</h1>")
        f.write("<p class='muted'>"+html.escape(r['desc'] or '')+price_html+"</p>")
        if r["link"] and r["link"] != "#":
            f.write("<p><a class='btn' rel='nofollow sponsored' href='"+html.escape(r['link'])+"'>Get Best Deal →</a></p>")
        f.write("</main>")

def build(csv_file, out_dir="out", site_title="Best Tools Hub"):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    (out/"styles.css").write_text(CSS, encoding="utf-8")
    rows = read_rows(csv_file)
    if not rows:
        print("[error] CSV empty or headers missing."); sys.exit(1)

    # Categories
    cats = {}
    for r in rows:
        slug = r["cat_slug"] or "general"
        name = r["cat"] or "General"
        cats.setdefault(slug, {"name": name, "items": []})
        cats[slug]["items"].append(r)

    # Nav (category links)
    nav_html = " ".join(
        f"<a href='{'/' if c=='general' else f'/{c}/index.html'}'>{html.escape(v['name'])}</a>"
        for c, v in cats.items()
    )

    # Offer pages
    for r in rows:
        write_offer(out, site_title, nav_html, r)

    # Category pages
    for c, v in cats.items():
        if c == "general":
            continue
        write_category(out, site_title, nav_html, v["name"], c, v["items"])

    # Home
    write_home(out, site_title, nav_html, rows)

    print(f\"[done] Built {len(rows)} offers across {len(cats)} categories → {out.resolve()}\" )

if __name__ == '__main__':
    try:
        csv_path = sys.argv[sys.argv.index('--csv')+1]
        out_dir  = sys.argv[sys.argv.index('--out')+1]
    except Exception:
        print('Usage: python3 build.py --csv data/100_offers_rich.csv --out out'); sys.exit(1)
    build(csv_path, out_dir, site_title='Best Tools Hub')
