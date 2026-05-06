export default function ClueBox({ puzzle, round, powerUps }) {
  if (!puzzle) return null

  const clue = puzzle.clues[`round${round}`]
  const curatorsNoteUsed = powerUps?.curatorsNote?.used
  const paletteUsed = powerUps?.paletteReveal?.used

  return (
    <div className="space-y-2">
      <div className="bg-gray-900 rounded-xl p-4 border border-gray-800">
        <p className="text-xs text-gray-500 uppercase tracking-widest mb-1.5">Clue — Round {round}</p>
        <p className="text-gray-200 leading-relaxed">{clue}</p>
      </div>

      {curatorsNoteUsed && (
        <div className="bg-amber-950/40 border border-amber-700/50 rounded-xl p-4">
          <p className="text-xs text-amber-500 uppercase tracking-widest mb-1.5">📜 Curator's Note</p>
          <p className="text-amber-100 text-sm leading-relaxed">{puzzle.curatorsNote}</p>
        </div>
      )}

      {paletteUsed && puzzle.dominantColors && (
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
          <p className="text-xs text-gray-500 uppercase tracking-widest mb-2.5">🎨 Dominant Colors</p>
          <div className="flex gap-2 items-center">
            {puzzle.dominantColors.map((hex, i) => (
              <div key={i} className="flex-1 flex flex-col items-center gap-1">
                <div
                  className="w-full h-8 rounded"
                  style={{ backgroundColor: hex }}
                  title={hex}
                />
                <span className="text-gray-500 text-[10px] font-mono">{hex}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
