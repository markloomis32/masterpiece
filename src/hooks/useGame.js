import { useReducer, useEffect } from 'react'
import { getTodaysPuzzle } from '../utils/getPuzzle'
import { paintings } from '../data/paintings'

const ROUND_POINTS = { 1: 1000, 2: 800, 3: 600, 4: 400, 5: 200 }

const INITIAL_STATE = {
  puzzle: null,
  round: 1,
  status: 'playing',
  guesses: [],
  score: 0,
  powerUps: {
    restoration: { used: false, spot: null },
    curatorsNote: { used: false },
    paletteReveal: { used: false },
    eliminator: { used: false, eliminated: [] },
  },
}

function gameReducer(state, action) {
  switch (action.type) {
    case 'HYDRATE':
      return action.state

    case 'INIT':
      return { ...INITIAL_STATE, puzzle: action.puzzle }

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

    case 'USE_RESTORATION':
      return {
        ...state,
        powerUps: { ...state.powerUps, restoration: { used: true, spot: action.spot } },
      }

    case 'USE_CURATORS_NOTE':
      return {
        ...state,
        powerUps: { ...state.powerUps, curatorsNote: { used: true } },
      }

    case 'USE_PALETTE_REVEAL':
      return {
        ...state,
        powerUps: { ...state.powerUps, paletteReveal: { used: true } },
      }

    case 'USE_ELIMINATOR': {
      const wrongPaintings = paintings
        .filter(p => p.id !== state.puzzle.paintingId)
        .sort(() => Math.random() - 0.5)
        .slice(0, 2)
        .map(p => p.id)
      return {
        ...state,
        powerUps: { ...state.powerUps, eliminator: { used: true, eliminated: wrongPaintings } },
      }
    }

    default:
      return state
  }
}

function getStorageKey(puzzle) {
  return puzzle ? `masterpiece-${puzzle.date}` : null
}

export function useGame() {
  const [state, dispatch] = useReducer(gameReducer, INITIAL_STATE)

  useEffect(() => {
    const puzzle = getTodaysPuzzle()
    const key = getStorageKey(puzzle)
    const saved = key ? localStorage.getItem(key) : null

    if (saved) {
      try {
        const parsed = JSON.parse(saved)
        dispatch({ type: 'HYDRATE', state: { ...parsed, puzzle } })
        return
      } catch {
        // ignore corrupt save
      }
    }
    dispatch({ type: 'INIT', puzzle })
  }, [])

  useEffect(() => {
    if (!state.puzzle) return
    const key = getStorageKey(state.puzzle)
    if (!key) return
    const { puzzle: _p, ...toSave } = state
    localStorage.setItem(key, JSON.stringify(toSave))
  }, [state])

  const submitGuess = (painting) => {
    dispatch({ type: 'GUESS', paintingId: painting.id, displayValue: `${painting.title} — ${painting.artist}` })
  }

  const skipRound = () => dispatch({ type: 'SKIP' })

  const usePowerUp = (type, payload) => {
    const typeMap = {
      restoration: 'USE_RESTORATION',
      curatorsNote: 'USE_CURATORS_NOTE',
      paletteReveal: 'USE_PALETTE_REVEAL',
      eliminator: 'USE_ELIMINATOR',
    }
    if (typeMap[type]) dispatch({ type: typeMap[type], ...payload })
  }

  return { state, submitGuess, skipRound, usePowerUp }
}
