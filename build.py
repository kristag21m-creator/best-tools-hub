import csv, os, argparse
from pathlib import Path

TEMPLATE = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>{title}</title></head>
<body>
<h1>{title}</h1>
<p>{description}</p>
<a href="{url}">Go to Offer</a>
</body>
</html>"""

def main(csv_file, out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            slug = row['Slug']
            html = TEMPLATE.format(title=row['Title'], description=row['Description'], url=row['URL'])
            (out/ f"{slug}.html").write_text(html, encoding='utf-8')
    print("Built site in", out)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--csv", default="data/example.csv")
    p.add_argument("--out", default="out")
    args = p.parse_args()
    main(args.csv, args.out)
