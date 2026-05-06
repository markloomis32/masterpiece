# Masterpiece — AI Coding Assistant Guide

A daily art puzzle web game. Players identify a famous painting through 5 rounds of progressive visual reveals and contextual clues.

## Tech Stack

- **React 18** with hooks (no class components)
- **Vite 5** for bundling and dev server
- **Tailwind CSS 3** for all styling — no custom CSS except `checkerboard-mask` in `index.css`
- **Fuse.js** for fuzzy autocomplete search

## Project Structure

```
src/
  App.jsx               # Root component, game layout, power-up orchestration
  hooks/useGame.js      # All game state via useReducer + localStorage persistence
  utils/getPuzzle.js    # Derives today's puzzle from date
  utils/shareUtils.js   # Generates shareable emoji grid text
  data/puzzles.json     # Daily puzzle schedule (one entry per day)
  data/paintings.js     # Full autocomplete list of paintings
  components/
    HowToPlayModal.jsx  # First-visit onboarding modal
    PaintingCanvas.jsx  # Image display with per-round CSS effects
    ClueBox.jsx         # Text clue + power-up reveals (curator's note, palette)
    GuessBar.jsx        # Autocomplete input + Guess/Skip buttons
    RoundIndicator.jsx  # 5-dot progress tracker
    PowerUpBar.jsx      # 4 one-use power-up buttons
    PostGameScreen.jsx  # Results, full painting reveal, share button
```

## Game Rules

- 5 rounds; each round the painting becomes less obscured and the clue more specific
- One guess per round; guessing wrong or skipping advances to the next round
- Correct guess ends the game (win); failing round 5 ends the game (loss)
- Points: 1000 / 800 / 600 / 400 / 200 for rounds 1–5

## Visual States per Round

| Round | Effect | CSS mechanism |
|-------|--------|---------------|
| 1 | Macro crop (5× zoom, center-top) | `transform: scale(5)` with `overflow: hidden` |
| 2 | Wider crop (2.5× zoom) | `transform: scale(2.5)` |
| 3 | Blurred full view | `filter: blur(14px)` |
| 4 | Checkerboard reveal | `.checkerboard-mask` utility class |
| 5 | Grayscale full canvas | `filter: grayscale(100%)` |

## Power-Ups

| Key | Behavior |
|-----|----------|
| `restoration` | User taps canvas → records `{x%, y%}` → renders unfiltered circular `clipPath` overlay |
| `curatorsNote` | Renders `puzzle.curatorsNote` in ClueBox |
| `paletteReveal` | Renders `puzzle.dominantColors` swatches in ClueBox |
| `eliminator` | Picks 2 random wrong painting IDs → stored in `powerUps.eliminator.eliminated` → GuessBar filters them out |

## State Shape (`useGame`)

```js
{
  puzzle: { ...puzzleData },         // from puzzles.json, matched by today's date
  round: 1–5,
  status: 'playing' | 'won' | 'lost',
  guesses: [{ round, paintingId, displayValue, skipped, correct }],
  score: 0 | 200 | 400 | 600 | 800 | 1000,
  powerUps: {
    restoration:   { used: bool, spot: {x, y} | null },
    curatorsNote:  { used: bool },
    paletteReveal: { used: bool },
    eliminator:    { used: bool, eliminated: [id, id] },
  }
}
```

State is persisted to `localStorage` keyed by `masterpiece-YYYY-MM-DD`. Each new day starts fresh automatically.

## Adding Puzzles (`puzzles.json`)

Each puzzle entry requires:
- `date` (YYYY-MM-DD) — must be unique
- `paintingId` — must match an `id` in `data/paintings.js`
- `imageUrl` — publicly accessible image (Wikimedia Commons recommended for public domain)
- `dominantColors` — array of 5 hex strings (use an eyedropper or palette tool)
- `clues.round1` through `clues.round5` — increasingly specific clues
- `curatorsNote` — a single interesting, specific trivia fact
- `funFact` — shown post-game; educational and engaging

## Adding Paintings to Autocomplete (`paintings.js`)

Add entries as `{ id, title, artist }`. IDs must be unique integers. Keep the list sorted by ID. Titles should match the canonical English title used in museum databases.

## Code Style

- Functional components only, hooks for all state
- No prop-types; keep component interfaces minimal and obvious from usage
- Tailwind for all styling — no inline `style` objects except for dynamic values (transforms, clip-path coordinates, color swatches)
- No comments unless explaining a non-obvious constraint
- Keep components focused — business logic belongs in `useGame.js`

## Running Locally

```bash
npm install
npm run dev
```

## Deployment

Static build via `npm run build`. Deploy `dist/` to Vercel or Netlify. No server required.
