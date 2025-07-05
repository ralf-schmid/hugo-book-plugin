#!/usr/bin/env python3
import sys
from prefill_books import fetch_metadata, ISBNNotFoundError

def main():
    if len(sys.argv) > 1:
        isbn = sys.argv[1]
    else:
        isbn = input("ISBN eingeben: ").strip()

    try:
        data = fetch_metadata(isbn)
        print("\n📚 Gefundene Metadaten:")
        for key, value in data.items():
            print(f"{key}: {value}")
    except ISBNNotFoundError as e:
        print(f"❌ Fehler: {e}")
    except Exception as e:
        print(f"❗ Unerwarteter Fehler: {e}")

if __name__ == "__main__":
    main()
