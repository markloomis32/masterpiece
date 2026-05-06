# Masterpiece

A daily art puzzle game. Identify a famous public-domain painting through five rounds of progressive visual reveals and contextual clues.

---

## Running the game locally

```bash
npm install
npm run dev
```

Open `http://localhost:5173` (or whichever port Vite picks).

---

## Adding new paintings

All paintings come from the [Metropolitan Museum of Art Open Access API](https://metmuseum.github.io/), which provides free, public-domain images. The pipeline runs in three steps.

### Prerequisites

```bash
pip install -r scripts/requirements.txt
```

### Step 1 — Fetch from the Met API

Run one of the following:

```bash
# Well-known Met highlights (curated search list)
python scripts/fetch_met_paintings.py --curated

# Search by topic or movement
python scripts/fetch_met_paintings.py --search "impressionism" --limit 20
python scripts/fetch_met_paintings.py --search "Renaissance portrait" --limit 15
python scripts/fetch_met_paintings.py --search "American realism" --limit 20

# Metadata only — skip image downloads (useful for previewing results)
python scripts/fetch_met_paintings.py --curated --no-download
```

This writes three files to `scripts/output/`:

| File | Contents |
|------|----------|
| `painting_data.json` | Raw Met API metadata |
| `game_paintings.js` | Autocomplete entries ready to merge into `src/data/paintings.js` |
| `game_puzzles_partial.json` | Partial puzzle entries — **requires manual editing before use** |

Images are downloaded to `public/images/{metObjectId}.jpg`.

### Step 2 — Clean the output

```bash
python scripts/clean_output.py
```

This shortens verbose museum titles to common names, normalises artist names, removes duplicates, and drops any entries whose image failed to download.

Review `scripts/output/game_paintings.js` after running to spot anything that looks wrong (unusual titles, unexpected artists, etc.).

### Step 3 — Fill in the editorial content

Open `scripts/output/game_puzzles_partial.json` and fill in the `TODO` fields for each painting:

```json
{
  "funFact":      "An interesting fact shown to the player after the game ends.",
  "curatorsNote": "A single specific trivia detail unlocked by the Curator's Note power-up.",
  "clues": {
    "round1": "Abstract / thematic vibe — very vague, no names",
    "round2": "Artistic style or movement",
    "round3": "Historical context — era, commission, event",
    "round4": "Artist nationality and century",
    "round5": "Artist initials: X.X.X."
  }
}
```

**Clue writing guidelines:**

| Round | Reveal state | Clue type | Rule |
|-------|-------------|-----------|------|
| 1 | Macro crop | Thematic vibe | No artist name, title, or movement |
| 2 | Wider crop | Style / movement | Name the movement but not the artist |
| 3 | Blurred full view | Historical context | Year, patron, event — no artist name |
| 4 | Checkerboard reveal | Nationality / era | Artist's country and century only |
| 5 | Grayscale | Artist initials | Exact format: `Artist initials: X.X.X.` |

Also assign `date` (YYYY-MM-DD) and `id` values (continuing from the last puzzle in `src/data/puzzles.json`).

### Step 4 — Apply to the game

```bash
python scripts/apply_to_game.py
```

This merges the filled-in partial JSON into `src/data/puzzles.json` and appends any new paintings to `src/data/paintings.js`.

Verify the result:

```bash
npm run build
npm run dev
```

---

## Puzzle data files

| File | Purpose |
|------|---------|
| `src/data/puzzles.json` | Daily puzzle schedule — one entry per day, ordered by date |
| `src/data/paintings.js` | Full autocomplete list — every painting that can appear as a guess option |
| `public/images/` | Downloaded painting images, named `{metObjectId}.jpg` |

A puzzle entry references a `paintingId` that must match an `id` in `paintings.js`. If a painting appears in `puzzles.json` but not in `paintings.js`, players will never be able to guess it.

---

## Project structure

```
src/
  App.jsx                  # Root component and layout
  hooks/useGame.js         # All game state (useReducer + localStorage)
  utils/getPuzzle.js       # Matches today's date to a puzzle
  utils/shareUtils.js      # Generates the shareable emoji grid
  data/
    puzzles.json           # Daily puzzle schedule
    paintings.js           # Autocomplete list
  components/
    HowToPlayModal.jsx
    PaintingCanvas.jsx     # Per-round image effects (zoom, blur, checkerboard, grayscale)
    ClueBox.jsx
    GuessBar.jsx           # Fuzzy autocomplete (Fuse.js)
    RoundIndicator.jsx
    PowerUpBar.jsx
    PostGameScreen.jsx
scripts/
  fetch_met_paintings.py   # Step 1 — fetch from Met API
  clean_output.py          # Step 2 — clean titles and remove bad entries
  apply_to_game.py         # Step 4 — merge into src/data/
  requirements.txt
public/
  images/                  # Downloaded painting images
```

---

## Deployment

```bash
npm run build
```

Deploy the `dist/` folder to [Vercel](https://vercel.com) or [Netlify](https://netlify.com). No server required — fully static.
