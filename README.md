# Hugo Book Plugin

Ein Hugo-Modul, um Bücher via ISBN automatisch mit Cover, Autor, Seitenanzahl, Beschreibung und Kauf-Links anzuzeigen. Unterstützt Mehrfach-Tags, lokale Overrides, Tag-Filter, Bildgrößen-Parameter, deutsche und englische Übersetzung und eine Vorfill-Skript.

## Zweck

Dieses Plugin erlaubt es dir, deine gelesenen Bücher und Publikationen auf deiner Hugo-Website übersichtlich darzustellen. Du pflegst nur die ISBN ein und bekommst automatisch Titel, Autor, Cover, Seitenzahl, Beschreibung und Kauf-Links. Mehrfach-Tags, Bewertungen und Kommentare sind möglich.

## Installation

1. GitHub-Repo klonen und in Hugo einbinden:
   ```toml
   module:
     imports:
       - path: github.com/ralf-schmid/hugo-book-plugin
   ```

  ```toml
   [[imports]]
path = "github.com/ralf-schmid/hugo-book-plugin"

[[mounts]]
source = "github.com/ralf-schmid/hugo-book-plugin/scripts"
target = "scripts"
```
   
2. Parameter in `config.toml` setzen:
   ```toml
   [params.book]
   imageSizeList = "M"
   imageSizeSingle = "L"

   [[params.book.buyLinks]]
   name = "Amazon"
   url = "https://www.amazon.de/s?k={{.ISBN}}"
   ```
3. Modul-Update und Server starten:
   ```bash
   hugo mod get
   hugo server
   ```

4. Python-Abhängigkeiten installieren
```bash
pip install \
  python-frontmatter \
  requests \
  pillow \
  pyzbar
```

6. Erstes Buch anlegen
```bash
hugo new --kind book books/mein-buch.md
```

6. Daten befüllen
```bash
python scripts/prefill_books.py
```

## Vorschau

### Übersicht
![Übersicht](assets/previews/overview.png)

### Einzelbuch-Ansicht
![Einzelbuch](assets/previews/single.png)

### Volltextsuche
![Suche](assets/previews/search.png)

## Verwendung des prefill_books.py

Du kannst das Skript nutzen, um vorhandene Markdown-Dateien zu befüllen oder neue anhand von Buch-Fotos anzulegen.

### Installation der Abhängigkeiten
```bash
pip install python-frontmatter requests pillow pyzbar
```

### Befüllen vorhandener Einträge
```bash
python scripts/prefill_books.py --content-dir content/books
```

### Einträge aus Buch-Fotos erzeugen
```bash
python scripts/prefill_books.py --images-dir Pfad/zu/Buchfotos --new-from-images
```

Das Skript liest Barcodes (ISBN) aus JPG-Bildern und erstellt bzw. aktualisiert deine `.md`-Dateien automatisch.

## Massenimport
Ich habe festgestellt, dass ich ganz viele schöne Bücher im Schrank stehen habe. Das schreit nach weiterer Optimierung. Ich habe dafür die App [BookBudy](https://apps.apple.com/de/app/bookbuddy-pro-meine-b%C3%BCcher/id395149950) genutzt. Einfach ISBN oder Barcode scannen oder zur Not manuell eingeben oder nach dem Buch suchen - und schon kann man in kürzester Zeit ein ganzes Regal scannen. Über den CSV-Export kann man die perfekte Eingabedatei für das Script import_csv_books.py (Eingabedatei wird über den Parameter --csv übergeben) schaffen. Die dafür benötigten Python-Module befinden sich in der Datei requirements.txt ebenfalls im scripts-Verzeichnis. Anschließend lassen sich die Angaben mit scripts/prefill_books.py anreichern.

## Script im Einsatz
Ich habe das Plugin für Hugo in erster Linie für mich geschrieben. Hier ist das Plugin sichtbar: [https://www.ralf-schmid.de/books](https://www.ralf-schmid.de/books)

## Lizenz

MIT
