#!/usr/bin/env python3
"""
Fetch famous public-domain paintings from Wikidata / Wikimedia Commons.

Uses a curated list of Wikidata QIDs (more reliable than open-ended SPARQL)
to fetch labels, images, year, and museum via the Wikidata API. Downloads
images to public/images/wiki_{Q_id}.jpg and writes the same three output
files as fetch_met_paintings.py so the clean → apply pipeline works identically.

Usage:
    pip install -r scripts/requirements.txt
    python scripts/fetch_wikimedia_paintings.py
    python scripts/fetch_wikimedia_paintings.py --limit 30
    python scripts/fetch_wikimedia_paintings.py --no-download
"""

import requests
import json
import time
import re
import argparse
from pathlib import Path
from io import BytesIO

try:
    from colorthief import ColorThief
    HAS_COLORTHIEF = True
except ImportError:
    HAS_COLORTHIEF = False

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

WIKIDATA_API = "https://www.wikidata.org/w/api.php"
SPARQL_URL   = "https://query.wikidata.org/sparql"
IMAGES_DIR   = Path("public/images")
OUTPUT_DIR   = Path("scripts/output")
RATE_DELAY   = 0.4
USER_AGENT   = "MasterpieceGameBot/1.0 (https://github.com/markloomis32/masterpiece)"

# ---------------------------------------------------------------------------
# Curated list of famous painting QIDs
# Ranked roughly by cultural fame / Wikipedia coverage
# ---------------------------------------------------------------------------

FAMOUS_QIDS = [
    "Q12418",    # Mona Lisa — Leonardo da Vinci
    "Q45585",    # The Starry Night — Van Gogh
    "Q185372",   # Girl with a Pearl Earring — Vermeer
    "Q151047",   # The Birth of Venus — Botticelli
    "Q18891156", # The Scream — Edvard Munch
    "Q252485",   # The Great Wave off Kanagawa — Hokusai
    "Q128910",   # The Last Supper — Leonardo da Vinci
    "Q219831",   # The Night Watch — Rembrandt
    "Q208758",   # Las Meninas — Velázquez
    "Q175036",   # Guernica — Picasso
    "Q464782",   # American Gothic — Grant Wood
    "Q698487",   # The Kiss — Klimt
    "Q687182",   # Whistler's Mother — James Whistler
    "Q29530",    # Liberty Leading the People — Delacroix
    "Q1044742",  # A Sunday on La Grande Jatte — Seurat
    "Q311243",   # Wanderer above the Sea of Fog — Friedrich
    "Q220859",   # The Arnolfini Portrait — Jan van Eyck
    "Q321303",   # The Garden of Earthly Delights — Bosch
    "Q83872",    # Nighthawks — Edward Hopper
    "Q1245354",  # A Bar at the Folies-Bergère — Manet
    "Q212616",   # The Raft of the Medusa — Géricault
    "Q2366825",  # The Hay Wain — Constable
    "Q186953",   # The School of Athens — Raphael
    "Q1189907",  # Water Lilies — Monet
    "Q110819859", # Washington Crossing the Delaware — Leutze
    "Q523974",   # View of Delft — Vermeer
    "Q500242",   # The Creation of Adam — Michelangelo
    "Q1752990",  # The Death of Socrates — David
    "Q18689458", # Wheat Field with Cypresses — Van Gogh
    "Q167605",   # The Milkmaid — Vermeer
    "Q699091",   # The Tower of Babel — Bruegel
    "Q737062",   # Olympia — Manet
    "Q152509",   # Le Déjeuner sur l'herbe — Manet
    "Q12859951", # The Swing — Fragonard
    "Q257580",   # The Fighting Temeraire — Turner
    "Q328523",   # Impression, Sunrise — Monet
    "Q1167907",  # The Luncheon of the Boating Party — Renoir
    "Q354396",   # Portrait of Adele Bloch-Bauer I — Klimt
    "Q1061035",  # The Treachery of Images — Magritte
    "Q1368055",  # The Gleaners — Jean-François Millet
    "Q1091086",  # The Third of May 1808 — Goya
    "Q540488",   # A Burial at Ornans — Courbet
    "Q661378",   # The Anatomy Lesson of Dr. Nicolaes Tulp — Rembrandt
    "Q604761",   # The Blue Boy — Gainsborough
    "Q883994",   # View of Toledo — El Greco
    "Q19363211", # Self-Portrait with Bandaged Ear — Van Gogh
    "Q40432",    # The Horse Fair — Rosa Bonheur
    "Q19925470", # Snap the Whip — Winslow Homer
    "Q7738501",  # The Gulf Stream — Winslow Homer
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

def extract_dominant_colors(image_bytes, count=5):
    if not HAS_COLORTHIEF or not image_bytes:
        return []
    try:
        ct = ColorThief(BytesIO(image_bytes))
        return [rgb_to_hex(*c) for c in ct.get_palette(color_count=count, quality=3)[:count]]
    except Exception:
        return []

def parse_year(time_str):
    if not time_str:
        return None
    m = re.search(r'(-?\d{4})', str(time_str))
    return int(m.group(1)) if m else None

def get_initials(name):
    parts = name.split()
    return ".".join(p[0].upper() for p in parts if p) + "." if parts else "?"

def commons_filename_to_url(filename):
    """Convert a Wikimedia Commons filename to a downloadable URL."""
    encoded = filename.replace(" ", "_")
    return f"https://commons.wikimedia.org/wiki/Special:FilePath/{requests.utils.quote(encoded)}"

def download_image(url, dest_path):
    headers = {"User-Agent": USER_AGENT}
    try:
        r = requests.get(url, headers=headers, timeout=30, allow_redirects=True)
        r.raise_for_status()
        if not r.headers.get("Content-Type", "").startswith("image/"):
            return None
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_bytes(r.content)
        return r.content
    except Exception as e:
        print(f"    ⚠️  Download failed: {e}")
        return None

# ---------------------------------------------------------------------------
# Wikidata entity API (fast — no SPARQL needed)
# ---------------------------------------------------------------------------

def fetch_entities_batch(qids):
    """Fetch up to 50 entities at once via wbgetentities."""
    params = {
        "action":    "wbgetentities",
        "ids":       "|".join(qids),
        "format":    "json",
        "languages": "en",
        "props":     "labels|claims",
    }
    headers = {"User-Agent": USER_AGENT}
    r = requests.get(WIKIDATA_API, params=params, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json().get("entities", {})

def get_label(entity, lang="en"):
    return entity.get("labels", {}).get(lang, {}).get("value", "")

def get_claim_value(entity, prop):
    """Return the main datavalue for the first statement of a property."""
    claims = entity.get("claims", {}).get(prop, [])
    if not claims:
        return None
    snak = claims[0].get("mainsnak", {})
    dv = snak.get("datavalue", {})
    val = dv.get("value")
    return val

def get_qid_label(qid):
    """Look up the English label for a single QID."""
    params = {"action": "wbgetentities", "ids": qid, "format": "json",
              "languages": "en", "props": "labels"}
    headers = {"User-Agent": USER_AGENT}
    try:
        r = requests.get(WIKIDATA_API, params=params, headers=headers, timeout=15)
        r.raise_for_status()
        entity = r.json()["entities"].get(qid, {})
        return get_label(entity)
    except Exception:
        return ""

# Manual title overrides for Wikidata label quality issues
TITLE_OVERRIDES = {
    "Q1245354": "A Bar at the Folies-Bergère",  # Wikidata label has erroneous "Sharon" suffix
    "Q152509":  "Le Déjeuner sur l'herbe",
}

def parse_entity(qid, entity):
    """Extract game-relevant fields from a raw Wikidata entity dict."""
    title = TITLE_OVERRIDES.get(qid) or get_label(entity)
    if not title or re.match(r'^Q\d+$', title):
        return None

    # Image (P18) — Commons filename
    image_val = get_claim_value(entity, "P18")
    if not image_val:
        return None
    image_filename = str(image_val)

    # Year (P571 inception)
    inception = get_claim_value(entity, "P571")
    year = parse_year(inception.get("time") if isinstance(inception, dict) else inception)

    # Artist (P170) — resolve QID to label
    artist_val = get_claim_value(entity, "P170")
    artist_qid = artist_val.get("id") if isinstance(artist_val, dict) else None
    artist = get_qid_label(artist_qid) if artist_qid else "Unknown Artist"
    time.sleep(RATE_DELAY)

    # Museum / location (P276 or P195)
    location_val = get_claim_value(entity, "P276") or get_claim_value(entity, "P195")
    location_qid = location_val.get("id") if isinstance(location_val, dict) else None
    museum = get_qid_label(location_qid) if location_qid else "Unknown Collection"
    if location_qid:
        time.sleep(RATE_DELAY)

    return {
        "wikidataId":     qid,
        "title":          title,
        "artist":         artist,
        "year":           year,
        "museum":         museum,
        "museumUrl":      f"https://www.wikidata.org/wiki/{qid}",
        "imageFilename":  image_filename,
        "imageUrlRemote": commons_filename_to_url(image_filename),
    }

# ---------------------------------------------------------------------------
# Main fetch loop
# ---------------------------------------------------------------------------

def fetch_paintings(limit=50, download=True):
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not HAS_COLORTHIEF:
        print("⚠️  colorthief not found — dominant colors will be empty. pip install colorthief\n")

    qids_to_fetch = FAMOUS_QIDS[:limit]
    print(f"🎨 Fetching {len(qids_to_fetch)} famous paintings from Wikidata…\n")

    # Batch-fetch entity data (50 at a time)
    all_entities = {}
    for i in range(0, len(qids_to_fetch), 50):
        batch = qids_to_fetch[i:i + 50]
        entities = fetch_entities_batch(batch)
        all_entities.update(entities)
        time.sleep(RATE_DELAY)

    results = []
    for qid in qids_to_fetch:
        entity = all_entities.get(qid)
        if not entity:
            print(f"  ⚠️  {qid}: not found — skipping")
            continue

        parsed = parse_entity(qid, entity)
        if not parsed:
            print(f"  ⚠️  {qid}: missing title or image — skipping")
            continue

        print(f"  [{len(results) + 1}] {parsed['title']} — {parsed['artist']}")

        # Download image
        image_bytes    = None
        local_filename = f"wiki_{qid}.jpg"
        local_path     = IMAGES_DIR / local_filename

        if download and not local_path.exists():
            print(f"       ↳ downloading…", end=" ", flush=True)
            image_bytes = download_image(parsed["imageUrlRemote"], local_path)
            print("done" if image_bytes else "FAILED")
            time.sleep(RATE_DELAY)
        elif local_path.exists():
            image_bytes = local_path.read_bytes()
            print(f"       ↳ cached")
        else:
            print(f"       ↳ skipped (--no-download)")

        if download and not local_path.exists():
            continue  # no image on disk — skip

        colors         = extract_dominant_colors(image_bytes)
        game_image_url = f"/images/{local_filename}" if download else parsed["imageUrlRemote"]

        results.append({
            **parsed,
            "imageUrl":       game_image_url,
            "dominantColors": colors,
            "funFact":        "TODO",
            "curatorsNote":   "TODO",
            "clues": {
                "round1": "TODO — abstract/thematic vibe",
                "round2": "TODO — artistic style/movement",
                "round3": "TODO — historical context",
                "round4": "TODO — artist nationality/era",
                "round5": f"TODO — artist initials: {get_initials(parsed['artist'])}",
            },
        })

    print(f"\n✅ Collected {len(results)} paintings.")
    return results

# ---------------------------------------------------------------------------
# Write outputs  (same format as fetch_met_paintings.py)
# ---------------------------------------------------------------------------

def write_outputs(results):
    START_ID = 201  # Met paintings use 101–199; Wikimedia starts at 201

    raw_path = OUTPUT_DIR / "painting_data.json"
    raw_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"📄 Raw metadata  → {raw_path}")

    js_entries = [
        f'  {{ id: {START_ID + i:>3}, '
        f'title: {json.dumps(p["title"]):<55}, '
        f'artist: {json.dumps(p["artist"])} }},'
        for i, p in enumerate(results)
    ]
    js_path = OUTPUT_DIR / "game_paintings.js"
    js_path.write_text("export const paintings = [\n" + "\n".join(js_entries) + "\n]\n")
    print(f"🖼️  paintings.js   → {js_path}")

    puzzle_entries = [
        {
            "id":            "TODO — assign puzzle number",
            "date":          "TODO — assign date (YYYY-MM-DD)",
            "paintingId":    START_ID + i,
            "title":         p["title"],
            "artist":        p["artist"],
            "year":          p["year"],
            "museum":        p["museum"],
            "museumUrl":     p["museumUrl"],
            "imageUrl":      p["imageUrl"],
            "dominantColors": p["dominantColors"] or ["TODO"],
            "funFact":       p["funFact"],
            "curatorsNote":  p["curatorsNote"],
            "clues":         p["clues"],
        }
        for i, p in enumerate(results)
    ]
    puzzles_path = OUTPUT_DIR / "game_puzzles_partial.json"
    puzzles_path.write_text(json.dumps({"puzzles": puzzle_entries}, indent=2, ensure_ascii=False))
    print(f"🧩 puzzles.json   → {puzzles_path}  (fill in TODO fields before using)")

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Fetch famous paintings from Wikidata/Wikimedia Commons.")
    parser.add_argument("--limit",       type=int, default=len(FAMOUS_QIDS),
                        help=f"Number of paintings to fetch (default: all {len(FAMOUS_QIDS)})")
    parser.add_argument("--no-download", action="store_true", help="Skip image downloads")
    args = parser.parse_args()

    results = fetch_paintings(limit=args.limit, download=not args.no_download)
    if results:
        write_outputs(results)
    else:
        print("⚠️  No results collected.")

if __name__ == "__main__":
    main()
