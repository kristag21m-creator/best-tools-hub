#!/usr/bin/env python3
import csv, os, sys, html

def build_site(csv_file, out_folder):
    os.makedirs(out_folder, exist_ok=True)

    # Load rows
    with open(csv_file, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    # Main index.html
    with open(os.path.join(out_folder, "index.html"), "w", encoding="utf-8") as f:
        f.write("<!doctype html><meta charset='utf-8'>")
        f.write("<link rel='stylesheet' href='styles.css'>")
        f.write("<title>Offers Hub</title><body>")
        f.write("<h1>Offers Hub</h1><ul>")
        for i, r in enumerate(rows):
            name = r.get("Name") or r.get("Title") or f"Offer {i+1}"
            f.write(f"<li><a href='offer_{i}.html'>{html.escape(name)}</a></li>")
        f.write("</ul></body>")

    # Offer pages
    for i, r in enumerate(rows):
        name = r.get("Name") or r.get("Title") or f"Offer {i+1}"
        desc = r.get("Description") or ""
        link = r.get("Link") or r.get("URL") or r.get("Affiliate_Link") or "#"
        with open(os.path.join(out_folder, f"offer_{i}.html"), "w", encoding="utf-8") as f:
            f.write("<!doctype html><meta charset='utf-8'>")
            f.write("<link rel='stylesheet' href='styles.css'>")
            f.write(f"<title>{html.escape(name)}</title><body>")
            f.write("<p><a href='index.html'>&larr; Back</a></p>")
            f.write(f"<h1>{html.escape(name)}</h1>")
            if desc: f.write(f"<p>{html.escape(desc)}</p>")
            if link: f.write(f"<p><a href='{html.escape(link)}' rel='nofollow sponsored'>Go to offer</a></p>")
            f.write("</body>")

    print(f"[done] Built {len(rows)} pages into: {os.path.abspath(out_folder)}")

if __name__ == "__main__":
    try:
        csv_path = sys.argv[sys.argv.index("--csv")+1]
        out_path = sys.argv[sys.argv.index("--out")+1]
    except Exception:
        print("Usage: python3 build.py --csv data/100_offers.csv --out out")
        sys.exit(1)
    build_site(csv_path, out_path)
