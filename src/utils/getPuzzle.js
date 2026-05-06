import puzzlesData from '../data/puzzles.json'

export function getTodaysPuzzle() {
  const today = new Date().toISOString().split('T')[0]
  const puzzle = puzzlesData.puzzles.find(p => p.date === today)
  return puzzle ?? puzzlesData.puzzles[0]
}

export function getPuzzleNumber() {
  const puzzle = getTodaysPuzzle()
  return puzzle.id
}
