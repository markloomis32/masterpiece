import puzzlesData from '../data/puzzles.json'

// ?puzzle=N in the URL loads that puzzle ID without persistence (dev/test mode)
export function getTestPuzzleId() {
  const param = new URLSearchParams(window.location.search).get('puzzle')
  return param ? parseInt(param, 10) : null
}

export function getTodaysPuzzle(difficulty) {
  const testId = getTestPuzzleId()
  if (testId) {
    return puzzlesData.puzzles.find(p => p.id === testId) ?? puzzlesData.puzzles[0]
  }

  const pool = puzzlesData.puzzles.filter(p => p.difficulty === difficulty)
  if (!pool.length) return puzzlesData.puzzles[0]

  // Deterministic daily rotation within the difficulty pool
  const epoch = Date.UTC(2026, 4, 5) // May 5 2026 — game launch
  const now = new Date()
  const todayUTC = Date.UTC(now.getFullYear(), now.getMonth(), now.getDate())
  const dayIndex = Math.max(0, Math.floor((todayUTC - epoch) / 86400000))
  return pool[dayIndex % pool.length]
}
