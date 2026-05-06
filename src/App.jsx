import { useState, useEffect } from 'react'
import { useGame } from './hooks/useGame'
import { getTestPuzzleId } from './utils/getPuzzle'
import HowToPlayModal from './components/HowToPlayModal'
import DifficultyScreen from './components/DifficultyScreen'
import PaintingCanvas from './components/PaintingCanvas'
import ClueBox from './components/ClueBox'
import GuessBar from './components/GuessBar'
import RoundIndicator from './components/RoundIndicator'
import PowerUpBar from './components/PowerUpBar'
import PostGameScreen from './components/PostGameScreen'

const HOW_TO_PLAY_KEY = 'masterpiece-seen-how-to-play'

export default function App() {
  const { state, submitGuess, skipRound, usePowerUp, selectDifficulty } = useGame()
  const { puzzle, difficulty, round, status, guesses, score, powerUps } = state

  const [showHowToPlay, setShowHowToPlay] = useState(false)

  useEffect(() => {
    if (!localStorage.getItem(HOW_TO_PLAY_KEY)) {
      setShowHowToPlay(true)
    }
  }, [])

  const handleCloseHowToPlay = () => {
    localStorage.setItem(HOW_TO_PLAY_KEY, '1')
    setShowHowToPlay(false)
  }

  const isGameOver = status === 'won' || status === 'lost'

  const testPuzzleId = getTestPuzzleId()

  return (
    <div className="min-h-screen bg-gray-950 flex flex-col">
      {testPuzzleId && (
        <div className="bg-amber-500 text-gray-950 text-xs font-mono text-center py-1 px-3">
          🧪 TEST MODE — puzzle #{testPuzzleId} — progress not saved —{' '}
          {Array.from({ length: 21 }, (_, i) => i + 1).map(n => (
            <a key={n} href={`?puzzle=${n}`} className={`mx-0.5 underline ${n === testPuzzleId ? 'font-bold' : ''}`}>{n}</a>
          ))}
        </div>
      )}
      {showHowToPlay && <HowToPlayModal onClose={handleCloseHowToPlay} />}

      {/* Header */}
      <header className="flex items-center justify-between px-4 py-3 border-b border-gray-900 max-w-xl mx-auto w-full">
        <button
          onClick={() => setShowHowToPlay(true)}
          className="text-gray-600 hover:text-gray-400 text-xl transition-colors"
          aria-label="How to play"
        >
          ?
        </button>
        <h1 className="font-serif font-bold text-lg tracking-wide text-gray-100">
          Masterpiece
          {puzzle && <span className="text-gray-600 font-normal text-sm ml-2">#{puzzle.id}</span>}
        </h1>
        <div className="w-6" />
      </header>

      {/* Main content */}
      <main className="flex-1 flex flex-col gap-4 px-4 py-4 max-w-xl mx-auto w-full pb-6">
        {!difficulty && !getTestPuzzleId() && (
          <DifficultyScreen onSelect={selectDifficulty} />
        )}

        {(difficulty || getTestPuzzleId()) && (<>
          <PaintingCanvas
            puzzle={puzzle}
            round={round}
            status={status}
          />

          {!isGameOver && (
            <RoundIndicator round={round} guesses={guesses} status={status} />
          )}

          {!isGameOver && (
            <ClueBox puzzle={puzzle} round={round} powerUps={powerUps} />
          )}

          {!isGameOver && (
            <GuessBar
              onGuess={submitGuess}
              onSkip={skipRound}
              disabled={!puzzle || isGameOver}
            />
          )}

          {!isGameOver && (
            <PowerUpBar
              powerUps={powerUps}
              onUsePowerUp={usePowerUp}
              disabled={isGameOver}
            />
          )}

          {isGameOver && (
            <PostGameScreen
              puzzle={puzzle}
              guesses={guesses}
              score={score}
              status={status}
            />
          )}
        </>)}
      </main>
    </div>
  )
}
