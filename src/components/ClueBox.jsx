export default function ClueBox({ puzzle, round, powerUps }) {
  if (!puzzle) return null

  const clue = puzzle.clues[`round${round}`]
  const { curatorsNote, styleTip, eraTip, artistReveal } = powerUps ?? {}

  return (
    <div className="space-y-2">
      <div className="bg-gray-900 rounded-xl p-4 border border-gray-800">
        <p className="text-xs text-gray-500 uppercase tracking-widest mb-1.5">Clue — Round {round}</p>
        <p className="text-gray-200 leading-relaxed">{clue}</p>
      </div>

      {curatorsNote?.used && (
        <div className="bg-amber-950/40 border border-amber-700/50 rounded-xl p-4">
          <p className="text-xs text-amber-500 uppercase tracking-widest mb-1.5">📜 Curator's Note</p>
          <p className="text-amber-100 text-sm leading-relaxed">{puzzle.curatorsNote}</p>
        </div>
      )}

      {styleTip?.used && (
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
          <p className="text-xs text-gray-500 uppercase tracking-widest mb-1">🖌️ Style</p>
          <p className="text-gray-100 text-sm font-medium">{puzzle.style}</p>
        </div>
      )}

      {eraTip?.used && (
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
          <p className="text-xs text-gray-500 uppercase tracking-widest mb-1">🕰️ Era</p>
          <p className="text-gray-100 text-sm font-medium">{puzzle.era}</p>
        </div>
      )}

      {artistReveal?.used && (
        <div className="bg-rose-950/40 border border-rose-700/50 rounded-xl p-4">
          <p className="text-xs text-rose-400 uppercase tracking-widest mb-1">👤 Artist</p>
          <p className="text-rose-100 text-sm font-semibold">{puzzle.artist}</p>
        </div>
      )}
    </div>
  )
}
