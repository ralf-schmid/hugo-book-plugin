#!/usr/bin/env python3
import os
import frontmatter
import requests

def fetch(isbn):
    url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    resp = requests.get(url)
    data = resp.json().get(f"ISBN:{isbn}", {})
    desc = data.get("description")
    if isinstance(desc, dict):
        desc = desc.get("value", "")
    return {
        "override_author": data.get("authors", [{}])[0].get("name", ""),
        "override_pages": data.get("number_of_pages", 0),
        "override_description": desc or ""
    }

def main():
    for root, _, files in os.walk("content/books"):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                post = frontmatter.load(path)
                isbn = post.get("isbn", "")
                if isbn and not post.get("override_author"):
                    data = fetch(isbn)
                    for k, v in data.items():
                        if v:
                            post[k] = v
                    with open(path, "w") as f:
                        frontmatter.dump(post, f)
                    print(f"Updated {file}")

if __name__ == "__main__":
    main()
