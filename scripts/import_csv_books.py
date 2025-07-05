#!/usr/bin/env python3
import csv
import os
import argparse
import frontmatter
from datetime import date
import re

def clean_price(raw_price):
    """Entfernt Währungssymbole und ersetzt Komma durch Punkt"""
    if not raw_price:
        return ""
    return raw_price.replace("€", "").replace("$", "").replace(",", ".").strip()

def slugify_title(title):
    """Entfernt Leerzeichen und Sonderzeichen für Dateinamen"""
    title = title.strip()
    title = re.sub(r"[^\w\d]", "", title)  # Entferne Sonderzeichen
    return title

def process_csv(csv_file):
    output_dir = os.path.join("content", "books")
    os.makedirs(output_dir, exist_ok=True)

    with open(csv_file, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row.get("Title", "").strip()
            if not title:
                print("[WARN] Kein Titel – überspringe Zeile")
                continue

            filename = os.path.join(output_dir, f"{slugify_title(title)}.md")
            if os.path.exists(filename):
                print(f"[SKIP] {filename} existiert bereits")
                continue

            isbn = row.get("ISBN", "").strip()

            post = frontmatter.Post(
            "",  # content
            title=title,
            subtitle=row.get("Subtitle", "").strip(),
            date=date.today().isoformat(),
            isbn=isbn,
            override_cover="",
            override_author=row.get("Author", "").strip(),
            override_pages=int(row.get("Number of Pages", 0)) if row.get("Number of Pages") else 0,
            override_description=row.get("Summary", "").strip(),
            override_price=clean_price(row.get("List Price", "")),
            tags=[],
            rating=0,
            comment="",
            draft=False
            )


            with open(filename, "wb") as f_out:
                frontmatter.dump(post, f_out)
            print(f"[NEW] erstellt: {filename}")

def main():
    parser = argparse.ArgumentParser(description="CSV → Markdown für Bücher")
    parser.add_argument("--csv", required=True, help="Pfad zur CSV-Datei (UTF-8)")
    args = parser.parse_args()

    process_csv(args.csv)

if __name__ == "__main__":
    main()
