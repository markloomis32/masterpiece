import { useReducer, useEffect } from 'react'
import { getTodaysPuzzle, getTestPuzzleId } from '../utils/getPuzzle'

const ROUND_POINTS = { 1: 1000, 2: 800, 3: 600, 4: 400, 5: 200 }

const INITIAL_STATE = {
  puzzle: null,
  difficulty: null,
  round: 1,
  status: 'playing',
  guesses: [],
  score: 0,
  powerUps: {
    curatorsNote: { used: false },
  },
}

function gameReducer(state, action) {
  switch (action.type) {
    case 'HYDRATE':
      return action.state

    case 'INIT':
      return { ...INITIAL_STATE, puzzle: action.puzzle, difficulty: action.difficulty }

    case 'GUESS': {
      const { paintingId, displayValue } = action
      const correct = paintingId === state.puzzle.paintingId
      const guess = { round: state.round, paintingId, displayValue, skipped: false, correct }

      if (correct) {
        return {
          ...state,
          guesses: [...state.guesses, guess],
          status: 'won',
          score: ROUND_POINTS[state.round],
        }
      }
      if (state.round === 5) {
        return { ...state, guesses: [...state.guesses, guess], status: 'lost' }
      }
      return { ...state, guesses: [...state.guesses, guess], round: state.round + 1 }
    }

    case 'SKIP': {
      const guess = { round: state.round, paintingId: null, displayValue: null, skipped: true, correct: false }
      if (state.round === 5) {
        return { ...state, guesses: [...state.guesses, guess], status: 'lost' }
      }
      return { ...state, guesses: [...state.guesses, guess], round: state.round + 1 }
    }

    case 'USE_CURATORS_NOTE':
      return {
        ...state,
        powerUps: { ...state.powerUps, curatorsNote: { used: true } },
      }

    default:
      return state
  }
}

function getToday() {
  return new Date().toISOString().split('T')[0]
}

function getDifficultyKey(date) {
  return `masterpiece-difficulty-${date}`
}

function getGameKey(difficulty, date) {
  return `masterpiece-${difficulty}-${date}`
}

export function useGame() {
  const [state, dispatch] = useReducer(gameReducer, INITIAL_STATE)
  const isTestMode = Boolean(getTestPuzzleId())

  useEffect(() => {
    if (isTestMode) {
      const puzzle = getTodaysPuzzle(null)
      dispatch({ type: 'INIT', puzzle, difficulty: 'easy' })
      return
    }

    const today = getToday()
    const savedDifficulty = localStorage.getItem(getDifficultyKey(today))
    if (!savedDifficulty) return // wait for difficulty selection via selectDifficulty()

    const puzzle = getTodaysPuzzle(savedDifficulty)
    const saved = localStorage.getItem(getGameKey(savedDifficulty, today))
    if (saved) {
      try {
        const parsed = JSON.parse(saved)
        dispatch({ type: 'HYDRATE', state: { ...parsed, puzzle, difficulty: savedDifficulty } })
        return
      } catch {
        // ignore corrupt save
      }
    }
    dispatch({ type: 'INIT', puzzle, difficulty: savedDifficulty })
  }, [])

  useEffect(() => {
    if (!state.puzzle || !state.difficulty || isTestMode) return
    const today = getToday()
    const { puzzle: _p, difficulty: _d, ...toSave } = state
    localStorage.setItem(getGameKey(state.difficulty, today), JSON.stringify(toSave))
  }, [state])

  const selectDifficulty = (difficulty) => {
    const today = getToday()
    localStorage.setItem(getDifficultyKey(today), difficulty)
    const puzzle = getTodaysPuzzle(difficulty)
    dispatch({ type: 'INIT', puzzle, difficulty })
  }

  const submitGuess = (painting) => {
    dispatch({ type: 'GUESS', paintingId: painting.id, displayValue: `${painting.title} — ${painting.artist}` })
  }

  const skipRound = () => dispatch({ type: 'SKIP' })

  const usePowerUp = (type) => {
    if (type === 'curatorsNote') dispatch({ type: 'USE_CURATORS_NOTE' })
  }

  return { state, submitGuess, skipRound, usePowerUp, selectDifficulty }
}
