import { useState } from 'react'

const ROUND_STYLES = {
  1: { transform: 'scale(5)', transformOrigin: '50% 40%', filter: '' },
  2: { transform: 'scale(2.5)', transformOrigin: '50% 50%', filter: '' },
  3: { transform: 'scale(1)', filter: 'blur(14px)', transformOrigin: '50% 50%' },
  4: { transform: 'scale(1)', filter: '', transformOrigin: '50% 50%' },
  5: { transform: 'scale(1)', filter: 'grayscale(100%)', transformOrigin: '50% 50%' },
}

export default function PaintingCanvas({ puzzle, round, status, powerUps, onRestorationClick, awaitingRestoration }) {
  if (!puzzle) return <div className="w-full aspect-[4/3] bg-gray-900 animate-pulse rounded-xl" />

  const isComplete = status === 'won' || status === 'lost'
  const displayRound = isComplete ? 'complete' : round
  const styles = ROUND_STYLES[displayRound] ?? {}

  const isCheckerboard = displayRound === 4
  const restorationSpot = powerUps?.restoration?.spot

  return (
    <div
      className={`relative w-full aspect-[4/3] overflow-hidden rounded-xl bg-gray-900 select-none ${awaitingRestoration ? 'cursor-crosshair ring-2 ring-amber-400' : ''}`}
      onClick={(e) => {
        if (!awaitingRestoration) return
        const rect = e.currentTarget.getBoundingClientRect()
        const x = ((e.clientX - rect.left) / rect.width) * 100
        const y = ((e.clientY - rect.top) / rect.height) * 100
        onRestorationClick({ x, y })
      }}
    >
      {awaitingRestoration && (
        <div className="absolute inset-0 z-20 flex items-center justify-center pointer-events-none">
          <span className="bg-black/60 text-amber-400 text-sm font-medium px-3 py-1.5 rounded-full">
            Tap to reveal a spot
          </span>
        </div>
      )}

      {/* Main image layer */}
      <img
        src={puzzle.imageUrl}
        alt="Today's painting"
        draggable={false}
        className={`absolute inset-0 w-full h-full object-cover transition-all duration-700 ${isCheckerboard ? 'checkerboard-mask' : ''}`}
        style={styles}
        crossOrigin="anonymous"
      />

      {/* Restoration reveal — clear image clipped to a circle at the tapped spot */}
      {restorationSpot && !isComplete && (
        <img
          src={puzzle.imageUrl}
          alt=""
          draggable={false}
          className="absolute inset-0 w-full h-full object-cover pointer-events-none"
          style={{
            clipPath: `circle(44px at ${restorationSpot.x}% ${restorationSpot.y}%)`,
            outline: '2px solid #f59e0b',
          }}
          crossOrigin="anonymous"
        />
      )}

      {/* Round label overlay */}
      {!isComplete && (
        <div className="absolute top-2 left-2 bg-black/50 text-gray-300 text-xs font-mono px-2 py-0.5 rounded pointer-events-none">
          Round {round} of 5
        </div>
      )}
    </div>
  )
}
