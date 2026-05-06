import { useState, useEffect } from 'react'
import { useGame } from './hooks/useGame'
import HowToPlayModal from './components/HowToPlayModal'
import PaintingCanvas from './components/PaintingCanvas'
import ClueBox from './components/ClueBox'
import GuessBar from './components/GuessBar'
import RoundIndicator from './components/RoundIndicator'
import PowerUpBar from './components/PowerUpBar'
import PostGameScreen from './components/PostGameScreen'

const HOW_TO_PLAY_KEY = 'masterpiece-seen-how-to-play'

export default function App() {
  const { state, submitGuess, skipRound, usePowerUp } = useGame()
  const { puzzle, round, status, guesses, score, powerUps } = state

  const [showHowToPlay, setShowHowToPlay] = useState(false)
  const [awaitingRestoration, setAwaitingRestoration] = useState(false)

  useEffect(() => {
    if (!localStorage.getItem(HOW_TO_PLAY_KEY)) {
      setShowHowToPlay(true)
    }
  }, [])

  const handleCloseHowToPlay = () => {
    localStorage.setItem(HOW_TO_PLAY_KEY, '1')
    setShowHowToPlay(false)
  }

  const handlePowerUp = (key) => {
    if (key === 'restoration') {
      setAwaitingRestoration(true)
      return
    }
    usePowerUp(key)
  }

  const handleRestorationClick = (spot) => {
    usePowerUp('restoration', { spot })
    setAwaitingRestoration(false)
  }

  const isGameOver = status === 'won' || status === 'lost'

  return (
    <div className="min-h-screen bg-gray-950 flex flex-col">
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
        <PaintingCanvas
          puzzle={puzzle}
          round={round}
          status={status}
          powerUps={powerUps}
          onRestorationClick={handleRestorationClick}
          awaitingRestoration={awaitingRestoration}
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
            eliminatedIds={powerUps?.eliminator?.eliminated ?? []}
          />
        )}

        {!isGameOver && (
          <PowerUpBar
            powerUps={powerUps}
            onUsePowerUp={handlePowerUp}
            disabled={isGameOver}
            awaitingRestoration={awaitingRestoration}
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
      </main>
    </div>
  )
}
