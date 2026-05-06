export default function ClueBox({ puzzle, round, powerUps }) {
  if (!puzzle) return null

  const clue = puzzle.clues[`round${round}`]
  const curatorsNoteUsed = powerUps?.curatorsNote?.used

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
    </div>
  )
}
