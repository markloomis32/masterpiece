const ROUND_STYLES = {
  1: { transform: 'scale(5)', transformOrigin: '50% 40%', filter: '' },
  2: { transform: 'scale(2.5)', transformOrigin: '50% 50%', filter: '' },
  3: { transform: 'scale(1)', filter: 'blur(14px)', transformOrigin: '50% 50%' },
  4: { transform: 'scale(1)', filter: '', transformOrigin: '50% 50%' },
  5: { transform: 'scale(1)', filter: 'grayscale(100%)', transformOrigin: '50% 50%' },
}

export default function PaintingCanvas({ puzzle, round, status }) {
  if (!puzzle) return <div className="w-full aspect-[4/3] bg-gray-900 animate-pulse rounded-xl" />

  const isComplete = status === 'won' || status === 'lost'
  const displayRound = isComplete ? 'complete' : round
  const styles = ROUND_STYLES[displayRound] ?? {}
  const isCheckerboard = displayRound === 4

  return (
    <div className="relative w-full aspect-[4/3] overflow-hidden rounded-xl bg-gray-900 select-none">
      <img
        src={puzzle.imageUrl}
        alt="Today's painting"
        draggable={false}
        className={`absolute inset-0 w-full h-full object-cover transition-all duration-700 ${isCheckerboard ? 'checkerboard-mask' : ''}`}
        style={styles}
        crossOrigin="anonymous"
      />

      {!isComplete && (
        <div className="absolute top-2 left-2 bg-black/50 text-gray-300 text-xs font-mono px-2 py-0.5 rounded pointer-events-none">
          Round {round} of 5
        </div>
      )}
    </div>
  )
}
