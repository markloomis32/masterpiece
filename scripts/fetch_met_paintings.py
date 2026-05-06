#!/usr/bin/env python3
"""
Fetch public domain paintings from The Metropolitan Museum of Art API.

Downloads images into public/images/ and writes three output files:
  scripts/output/painting_data.json       — raw Met API metadata
  scripts/output/game_paintings.js        — drop-in replacement for src/data/paintings.js
  scripts/output/game_puzzles_partial.json — partial puzzles.json (needs manual clues/fun facts)

Usage:
    pip install -r scripts/requirements.txt
    python scripts/fetch_met_paintings.py
    python scripts/fetch_met_paintings.py --limit 30 --search "impressionism"
    python scripts/fetch_met_paintings.py --curated          # well-known Met highlights
    python scripts/fetch_met_paintings.py --no-download      # metadata only, skip images
"""

import requests
import json
import time
import os
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

SEARCH_URL  = "https://collectionapi.metmuseum.org/public/collection/v1/search"
OBJECT_URL  = "https://collectionapi.metmuseum.org/public/collection/v1/objects/"
IMAGES_DIR  = Path("public/images")
OUTPUT_DIR  = Path("scripts/output")
RATE_DELAY  = 0.15   # seconds between API calls — stay friendly to the Met

# Direct Met object IDs for iconic public-domain paintings.
# Using IDs instead of title searches avoids mismatches and duplicates.
# Curated list of (title_query, artist_keyword) pairs.
# The script searches for each pair and takes the first public-domain painting match.
# This is more reliable than hardcoding object IDs.
CURATED_SEARCHES = [
    ("Washington Crossing the Delaware", "Leutze"),
    ("Madame X",                          "Sargent"),
    ("Death of Socrates",                 "David"),
    ("Wheat Field with Cypresses",        "van Gogh"),
    ("Self-Portrait Straw Hat",           "van Gogh"),
    ("The Harvesters",                    "Bruegel"),
    ("Irises",                            "van Gogh"),
    ("The Dance Class",                   "Degas"),
    ("Sunflowers",                        "van Gogh"),
    ("Aristotle Bust of Homer",           "Rembrandt"),
    ("La Berceuse",                       "van Gogh"),
    ("Madame Roulin",                     "van Gogh"),
    ("Shoes",                             "van Gogh"),
    ("The Horse Fair",                    "Bonheur"),
    ("The Gulf Stream",                   "Homer"),
    ("Fur Traders Missouri",              "Bingham"),
    ("Rocky Mountains Lander",            "Bierstadt"),
    ("Snap the Whip",                     "Homer"),
    ("Young Woman Water Pitcher",         "Vermeer"),
    ("Portrait of a Young Woman",         "Petrus Christus"),
    ("The Harvesters",                    "Bruegel"),
    ("Cypresses",                         "van Gogh"),
    ("The Potato Eaters",                 "van Gogh"),
    ("Still Life Apples",                 "Cézanne"),
    ("Women in the Garden",               "Renoir"),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"


def extract_dominant_colors(image_bytes, count=5):
    """Return a list of `count` hex color strings from image bytes."""
    if not HAS_COLORTHIEF:
        return []
    try:
        ct = ColorThief(BytesIO(image_bytes))
        palette = ct.get_palette(color_count=count, quality=3)
        return [rgb_to_hex(*c) for c in palette[:count]]
    except Exception:
        return []


def download_image(url, dest_path):
    """Download an image URL to dest_path. Returns raw bytes or None on failure."""
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_bytes(r.content)
        return r.content
    except Exception as e:
        print(f"    ⚠️  Image download failed: {e}")
        return None


def fetch_object(obj_id):
    """Fetch a single Met object record. Returns dict or None."""
    try:
        r = requests.get(f"{OBJECT_URL}{obj_id}", timeout=15)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None


def is_usable_painting(data):
    """Return True if the record is a public-domain painting with a primary image."""
    has_image   = bool(data.get("primaryImage"))
    is_public   = data.get("isPublicDomain", False)
    # Some records store "Painting" in objectName with an empty classification field
    classification = data.get("classification", "")
    object_name    = data.get("objectName", "")
    is_painting = "Painting" in classification or object_name == "Painting"
    return is_painting and has_image and is_public


def sanitize_year(raw):
    """Pull the first 4-digit year from a string like '1882', 'ca. 1880', '1880–82'."""
    import re
    m = re.search(r"\d{4}", str(raw))
    return int(m.group()) if m else None


def build_entry(data, local_image_path, dominant_colors):
    """Build a game-compatible metadata dict from a Met API object."""
    year = sanitize_year(data.get("objectDate", ""))
    return {
        # --- auto-filled from Met API ---
        "metObjectId":     data.get("objectID"),
        "title":           data.get("title", "Untitled"),
        "artist":          data.get("artistDisplayName") or "Unknown Artist",
        "year":            year,
        "medium":          data.get("medium", ""),
        "museum":          "The Metropolitan Museum of Art, New York",
        "museumUrl":       data.get("objectURL", ""),
        "imageUrl":        str(local_image_path),
        "imageUrlRemote":  data.get("primaryImage", ""),
        "dominantColors":  dominant_colors,
        "creditLine":      data.get("creditLine", ""),
        "department":      data.get("department", ""),
        "culture":         data.get("culture", ""),
        "period":          data.get("period", ""),
        # --- must be filled in manually before adding to puzzles.json ---
        "funFact":         "TODO",
        "curatorsNote":    "TODO",
        "clues": {
            "round1": "TODO — abstract/thematic vibe",
            "round2": "TODO — artistic style/movement",
            "round3": "TODO — historical context",
            "round4": "TODO — artist nationality/era",
            "round5": f"TODO — artist initials: {get_initials(data.get('artistDisplayName', ''))}",
        },
    }


def get_initials(name):
    """'Vincent van Gogh' → 'V.V.G.'"""
    if not name:
        return "?"
    parts = name.split()
    return ".".join(p[0].upper() for p in parts if p) + "."


# ---------------------------------------------------------------------------
# Search strategies
# ---------------------------------------------------------------------------

def search_ids_broad(query, limit):
    """Broad search — returns up to `limit * 3` object IDs to filter through."""
    params = {"q": query, "isPublicDomain": "true", "hasImages": "true"}
    try:
        r = requests.get(SEARCH_URL, params=params, timeout=15)
        r.raise_for_status()
        ids = r.json().get("objectIDs") or []
        return ids[: limit * 3]
    except Exception as e:
        print(f"  ❌ Search failed: {e}")
        return []


def search_ids_curated():
    """Search for each (title, artist) pair and return the best matching object ID."""
    ids = []
    seen = set()
    for title_q, artist_q in CURATED_SEARCHES:
        query = f"{title_q} {artist_q}"
        params = {"q": query, "isPublicDomain": "true", "hasImages": "true"}
        try:
            r = requests.get(SEARCH_URL, params=params, timeout=15)
            r.raise_for_status()
            found = r.json().get("objectIDs") or []
            for oid in found[:5]:  # check up to 5 candidates per search
                if oid not in seen:
                    seen.add(oid)
                    ids.append(oid)
                    break
        except Exception:
            pass
        time.sleep(RATE_DELAY)
    return ids


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def fetch_paintings(query="painting", limit=20, curated=False, download=True):
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not HAS_COLORTHIEF:
        print("⚠️  colorthief not found — dominant colors will be empty.")
        print("   Install with: pip install colorthief\n")

    # --- 1. Collect object IDs ---
    if curated:
        print(f"🎨 Searching for {len(CURATED_SEARCHES)} curated Met highlights…")
        object_ids = search_ids_curated()
        print(f"   Resolved {len(object_ids)} candidate IDs.\n")
    else:
        print(f"🔍 Searching Met API for: '{query}' (public domain, with images)…")
        object_ids = search_ids_broad(query, limit)
        print(f"   Found {len(object_ids)} candidates. Will collect up to {limit} usable paintings.\n")

    # --- 2. Fetch details and build records ---
    results = []
    processed = 0

    for obj_id in object_ids:
        if not curated and len(results) >= limit:
            break

        data = fetch_object(obj_id)
        time.sleep(RATE_DELAY)

        if not data or not is_usable_painting(data):
            continue

        processed += 1
        title  = data.get("title", "Untitled")
        artist = data.get("artistDisplayName") or "Unknown"
        print(f"  [{len(results) + 1}] {title} — {artist}")

        # --- 3. Download image ---
        image_bytes    = None
        local_img_path = IMAGES_DIR / f"{obj_id}.jpg"
        remote_url     = data.get("primaryImage", "")

        if download and not local_img_path.exists():
            print(f"       ↳ downloading image…", end=" ", flush=True)
            image_bytes = download_image(remote_url, local_img_path)
            print("done" if image_bytes else "FAILED")
        elif local_img_path.exists():
            image_bytes = local_img_path.read_bytes()
            print(f"       ↳ image already cached")

        # --- 4. Dominant colors ---
        colors = extract_dominant_colors(image_bytes) if image_bytes else []

        # Use local path for game; fall back to remote if download skipped
        game_image_url = f"/images/{obj_id}.jpg" if download else remote_url

        entry = build_entry(data, game_image_url, colors)
        results.append(entry)

    print(f"\n✅ Collected {len(results)} paintings.")
    return results


def write_outputs(results):
    # --- Raw data dump ---
    raw_path = OUTPUT_DIR / "painting_data.json"
    raw_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"📄 Raw metadata  → {raw_path}")

    # --- Drop-in paintings.js for autocomplete ---
    # Assigns sequential IDs starting after 45 (the existing placeholder list ends at 45)
    START_ID = 101
    js_entries = []
    for i, p in enumerate(results):
        js_entries.append(
            f'  {{ id: {START_ID + i:>3}, '
            f'title: {json.dumps(p["title"]):<55}, '
            f'artist: {json.dumps(p["artist"])} }},'
        )
    js_body = "export const paintings = [\n" + "\n".join(js_entries) + "\n]\n"
    js_path = OUTPUT_DIR / "game_paintings.js"
    js_path.write_text(js_body)
    print(f"🖼️  paintings.js   → {js_path}")

    # --- Partial puzzles.json (manual fields still needed) ---
    puzzle_entries = []
    for i, p in enumerate(results):
        puzzle_entries.append({
            "id":          f"TODO — assign puzzle number",
            "date":        f"TODO — assign date (YYYY-MM-DD)",
            "paintingId":  101 + i,
            "title":       p["title"],
            "artist":      p["artist"],
            "year":        p["year"],
            "museum":      p["museum"],
            "museumUrl":   p["museumUrl"],
            "imageUrl":    p["imageUrl"],
            "dominantColors": p["dominantColors"] if p["dominantColors"] else ["TODO"],
            "funFact":     p["funFact"],
            "curatorsNote": p["curatorsNote"],
            "clues":       p["clues"],
        })
    puzzles_path = OUTPUT_DIR / "game_puzzles_partial.json"
    puzzles_path.write_text(json.dumps({"puzzles": puzzle_entries}, indent=2, ensure_ascii=False))
    print(f"🧩 puzzles.json   → {puzzles_path}  (fill in TODO fields before using)")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Fetch Met Museum paintings for Masterpiece game.")
    parser.add_argument("--search",      default="painting", help="Search query (default: 'painting')")
    parser.add_argument("--limit",       type=int, default=20, help="Max paintings to collect (default: 20)")
    parser.add_argument("--curated",     action="store_true",  help="Use the built-in curated list of Met highlights")
    parser.add_argument("--no-download", action="store_true",  help="Skip image downloads (metadata only)")
    args = parser.parse_args()

    results = fetch_paintings(
        query=args.search,
        limit=args.limit,
        curated=args.curated,
        download=not args.no_download,
    )

    if results:
        write_outputs(results)
    else:
        print("⚠️  No results collected.")


if __name__ == "__main__":
    main()
