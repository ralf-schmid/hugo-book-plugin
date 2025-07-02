#!/usr/bin/env python3
import os
import argparse
import frontmatter
import requests
from PIL import Image
from pyzbar.pyzbar import decode

API_URL = "https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
GOOGLE_BOOKS_URL = "https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"

class ISBNNotFoundError(Exception):
    pass

def fetch_openlibrary(isbn):
    url = API_URL.format(isbn=isbn)
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    key = f"ISBN:{isbn}"
    return data.get(key)

def fetch_google_books(isbn):
    url = GOOGLE_BOOKS_URL.format(isbn=isbn)
    resp = requests.get(url)
    resp.raise_for_status()
    items = resp.json().get("items", [])
    if not items:
        return None
    return items[0].get("volumeInfo", {})

def fetch_metadata(isbn):
    isbn_clean = isbn.replace('-', '').strip()
    ol = fetch_openlibrary(isbn_clean)
    if ol:
        desc = ol.get("description")
        if isinstance(desc, dict):
            desc = desc.get("value", "")
        return {
            "override_author": ol.get("authors", [{}])[0].get("name", ""),
            "override_pages": ol.get("number_of_pages", 0),
            "override_description": desc or "",
        }
    gb = fetch_google_books(isbn_clean)
    if gb:
        return {
            "override_author": ", ".join(gb.get("authors", [])),
            "override_pages": gb.get("pageCount", 0),
            "override_description": gb.get("description", "")
        }
    raise ISBNNotFoundError(f"Keine Daten gefunden für ISBN {isbn}")

def process_markdown(content_dir):
    for root, _, files in os.walk(content_dir):
        for file in files:
            if not file.endswith(".md"):
                continue
            path = os.path.join(root, file)
            post = frontmatter.load(path)
            isbn = str(post.get("isbn", "")).strip()
            if not isbn:
                continue
            try:
                meta = fetch_metadata(isbn)
            except ISBNNotFoundError as e:
                print(f"[ERROR] {file}: {e}")
                continue

            updated = False
            for key, value in meta.items():
                if value and not post.get(key):
                    post[key] = value
                    updated = True
            if post.get("override_author") and not post.get("authors"):
                post["authors"] = [post["override_author"]]
                updated = True

            if updated:
                with open(path, "wb") as f:
                    frontmatter.dump(post, f)
                print(f"[MD] aktualisiert: {file}")

def decode_isbns_from_images(image_dir):
    try:
        from PIL import Image
        from pyzbar.pyzbar import decode
    except ImportError as e:
        print(f"[WARN] Barcode-Unterstützung nicht verfügbar: {e}")
        return []
    found = set()
    for fname in os.listdir(image_dir):
        if not fname.lower().endswith((".jpg", ".jpeg")):
            continue
        img = Image.open(os.path.join(image_dir, fname))
        for code in decode(img):
            data = code.data.decode("utf-8")
            if data.isdigit() and len(data) in (10, 13):
                found.add(data)
    return sorted(found)

def create_markdown_for_isbns(isbns, output_dir):
    for isbn in isbns:
        filename = os.path.join(output_dir, f"{isbn}.md")
        if os.path.exists(filename):
            print(f"[SKIP] {filename} existiert bereits")
            continue
        try:
            meta = fetch_metadata(isbn)
        except ISBNNotFoundError as e:
            print(f"[ERROR] {filename}: {e}")
            continue

        post = frontmatter.Post(
            title="",
            date="",
            isbn=isbn,
            override_author=meta.get("override_author", ""),
            override_pages=meta.get("override_pages", 0),
            override_description=meta.get("override_description", ""),
            tags=[],
            rating=0,
            comment="",
            draft=True
        )
        if post.get("override_author"):
            post["authors"] = [post["override_author"]]

        with open(filename, "wb") as f:
            frontmatter.dump(post, f)
        print(f"[NEW] erstellt: {filename}")

def main():
    parser = argparse.ArgumentParser(
        description="Buchtitel/Metadaten per ISBN auffüllen – optional via Bild-Ordner"
    )
    parser.add_argument(
        "-c", "--content-dir",
        default="content/books",
        help="Verzeichnis mit vorhandenen .md-Dateien"
    )
    parser.add_argument(
        "-i", "--images-dir",
        help="Optional: Verzeichnis mit Buch-Fotos (JPGs), um ISBN per Barcode zu lesen"
    )
    parser.add_argument(
        "--new-from-images", action="store_true",
        help="Neue .md für jede gefundene ISBN anlegen"
    )
    args = parser.parse_args()

    process_markdown(args.content_dir)

    if args.images_dir:
        isbns = decode_isbns_from_images(args.images_dir)
        print(f"Gefundene ISBNs: {', '.join(isbns)}")
        if args.new_from_images:
            create_markdown_for_isbns(isbns, args.content_dir)

if __name__ == "__main__":
    main()
