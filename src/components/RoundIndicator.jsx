const ROUND_POINTS = { 1: 1000, 2: 800, 3: 600, 4: 400, 5: 200 }

export default function RoundIndicator({ round, guesses, status }) {
  return (
    <div className="flex items-center justify-center gap-2">
      {[1, 2, 3, 4, 5].map(r => {
        const guess = guesses.find(g => g.round === r)
        const isCurrent = r === round && status === 'playing'
        const isCorrect = guess?.correct
        const isWrong = guess && !guess.correct && !guess.skipped
        const isSkipped = guess?.skipped
        const isFuture = !guess && r > round

        return (
          <div key={r} className="flex flex-col items-center gap-1">
            <div
              className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold border-2 transition-all ${
                isCorrect
                  ? 'bg-green-500 border-green-400 text-white'
                  : isWrong
                  ? 'bg-gray-700 border-gray-600 text-gray-400'
                  : isSkipped
                  ? 'bg-gray-800 border-gray-700 text-gray-600'
                  : isCurrent
                  ? 'bg-transparent border-amber-400 text-amber-400 ring-2 ring-amber-400/30'
                  : 'bg-transparent border-gray-700 text-gray-700'
              }`}
            >
              {isCorrect ? '✓' : isWrong ? '✗' : isSkipped ? '–' : r}
            </div>
            <span className={`text-[10px] font-mono ${isCurrent ? 'text-amber-400' : 'text-gray-700'}`}>
              {ROUND_POINTS[r]}
            </span>
          </div>
        )
      })}
    </div>
  )
}
