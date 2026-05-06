const ROUNDS = [
  { round: 1, visual: 'Tiny detail crop',         clue: 'Abstract vibe',         pts: 1000 },
  { round: 2, visual: 'Wider crop',                clue: 'Style / movement',      pts: 800  },
  { round: 3, visual: 'Blurred full view',         clue: 'Historical context',    pts: 600  },
  { round: 4, visual: 'Checkerboard reveal',       clue: 'Nationality / era',     pts: 400  },
  { round: 5, visual: 'Grayscale full canvas',     clue: 'Artist initials',       pts: 200  },
]

export default function HowToPlayModal({ onClose }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4">
      <div className="bg-gray-900 border border-gray-700 rounded-2xl max-w-sm w-full p-6 space-y-4 max-h-[90vh] overflow-y-auto">
        <div className="text-center">
          <div className="text-3xl mb-1">🖼️</div>
          <h2 className="text-xl font-serif font-bold text-white">How to Play</h2>
          <p className="text-gray-400 text-sm mt-1">Identify the famous painting in as few rounds as possible.</p>
        </div>

        <div className="space-y-2">
          {ROUNDS.map(r => (
            <div key={r.round} className="flex items-start gap-3 text-sm">
              <span className="text-gray-500 w-6 text-right shrink-0">#{r.round}</span>
              <div className="flex-1">
                <span className="text-gray-200">{r.visual}</span>
                <span className="text-gray-500 mx-1">·</span>
                <span className="text-gray-400">{r.clue}</span>
              </div>
              <span className="text-amber-400 font-mono text-xs shrink-0">{r.pts.toLocaleString()}</span>
            </div>
          ))}
        </div>

        <div className="border-t border-gray-700 pt-4 space-y-2 text-sm text-gray-400">
          <p>Type a painting title or artist name in the search bar. Select from the dropdown to lock in your guess.</p>
          <p>You also have <span className="text-white">4 one-time power-ups</span> — use them wisely.</p>
          <p>A new painting drops every day at midnight. 🕛</p>
        </div>

        <button
          onClick={onClose}
          className="w-full bg-amber-500 hover:bg-amber-400 active:bg-amber-600 text-gray-950 font-bold py-3 rounded-xl transition-colors"
        >
          Let's Go!
        </button>
      </div>
    </div>
  )
}
