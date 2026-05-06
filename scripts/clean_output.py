#!/usr/bin/env python3
"""
Clean up game_paintings.js and game_puzzles_partial.json:
  - Shorten verbose museum titles to common names
  - Normalize artist names (hyphens, remove parentheticals)
  - Remove duplicates (same canvas, front/back)
  - Remove entries with broken image downloads
"""

import json
from pathlib import Path

OUTPUT_DIR = Path("scripts/output")
IMAGES_DIR = Path("public/images")

# ---------------------------------------------------------------------------
# Title overrides — keyed by paintingId
# ---------------------------------------------------------------------------
TITLE_OVERRIDES = {
    102: "Madame X",
    105: "Self-Portrait with a Straw Hat",
    111: "La Berceuse",
}

# ---------------------------------------------------------------------------
# Artist name normalization
# ---------------------------------------------------------------------------
ARTIST_OVERRIDES = {
    "Jacques Louis David":           "Jacques-Louis David",
    "Rembrandt (Rembrandt van Rijn)": "Rembrandt van Rijn",
    "Jean Baptiste Camille Corot":    "Jean-Baptiste-Camille Corot",
}

# ---------------------------------------------------------------------------
# IDs to drop entirely
# ---------------------------------------------------------------------------
DROP_IDS = {
    122,   # The Potato Peeler — reverse side of painting 105 (same canvas)
    123,   # Apples (Cézanne) — broken image URL from Met
}


def clean_title(pid, raw):
    return TITLE_OVERRIDES.get(pid, raw)


def clean_artist(raw):
    return ARTIST_OVERRIDES.get(raw, raw)


def image_exists(painting_id, puzzles):
    """Return True if the downloaded image file exists on disk."""
    puzzle = next((p for p in puzzles if p["paintingId"] == painting_id), None)
    if not puzzle:
        return False
    img_url = puzzle.get("imageUrl", "")
    if img_url.startswith("/images/"):
        path = Path("public") / img_url.lstrip("/")
        return path.exists()
    return True  # remote URL — assume ok


def main():
    # Load
    puzzles_path = OUTPUT_DIR / "game_puzzles_partial.json"
    raw = json.loads(puzzles_path.read_text())
    puzzles = raw["puzzles"]

    cleaned = []
    for p in puzzles:
        pid = p["paintingId"]

        # Drop unwanted entries
        if pid in DROP_IDS:
            print(f"  ✂️  Dropping {pid}: {p['title']}")
            continue

        # Drop entries whose image failed to download
        if not image_exists(pid, puzzles):
            print(f"  ✂️  Dropping {pid}: {p['title']} (no image on disk)")
            continue

        p["title"]  = clean_title(pid, p["title"])
        p["artist"] = clean_artist(p["artist"])
        cleaned.append(p)
        print(f"  ✅ {pid:>3}  {p['title'][:50]:<50}  {p['artist']}")

    # Re-number paintingIds sequentially from 101
    for i, p in enumerate(cleaned):
        p["paintingId"] = 101 + i

    # Write cleaned puzzles
    out = {"puzzles": cleaned}
    puzzles_path.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\n📄 Wrote {len(cleaned)} entries → {puzzles_path}")

    # Regenerate game_paintings.js
    js_lines = []
    for p in cleaned:
        js_lines.append(
            f'  {{ id: {p["paintingId"]:>3}, '
            f'title: {json.dumps(p["title"]):<55}, '
            f'artist: {json.dumps(p["artist"])} }},'
        )
    js = "export const paintings = [\n" + "\n".join(js_lines) + "\n]\n"
    js_path = OUTPUT_DIR / "game_paintings.js"
    js_path.write_text(js)
    print(f"🖼️  Wrote {len(cleaned)} entries → {js_path}")


if __name__ == "__main__":
    main()
