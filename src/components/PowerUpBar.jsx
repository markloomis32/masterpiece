const POWER_UPS = [
  { key: 'curatorsNote',  icon: '📜', label: 'Curator', title: "Curator's Note",  desc: 'A rare, specific clue about this painting' },
  { key: 'styleTip',      icon: '🖌️', label: 'Style',   title: 'Style Hint',      desc: 'Reveals the artistic movement' },
  { key: 'eraTip',        icon: '🕰️', label: 'Era',     title: 'Era Hint',        desc: 'Reveals when and where it was painted' },
  { key: 'artistReveal',  icon: '👤', label: 'Artist',  title: 'Artist Reveal',   desc: 'Reveals the artist\'s name' },
]

export default function PowerUpBar({ powerUps, onUsePowerUp, disabled }) {
  return (
    <div className="space-y-1.5">
      <p className="text-xs text-gray-600 uppercase tracking-widest text-center">Power-ups — one use each · −50 pts</p>
      <div className="flex gap-2 justify-center">
        {POWER_UPS.map(({ key, icon, label, title, desc }) => {
          const used = powerUps?.[key]?.used
          return (
            <button
              key={key}
              type="button"
              onClick={() => !used && !disabled && onUsePowerUp(key)}
              disabled={used || disabled}
              title={used ? `${title} — already used` : `${title}: ${desc}`}
              className={`flex flex-col items-center gap-0.5 px-3 py-2 rounded-xl border text-xs font-medium transition-all select-none ${
                used
                  ? 'border-gray-800 bg-gray-900/50 text-gray-700 cursor-not-allowed opacity-40'
                  : 'border-gray-700 bg-gray-900 text-gray-400 hover:border-gray-500 hover:text-gray-200 active:bg-gray-800'
              }`}
            >
              <span className="text-lg leading-none">{icon}</span>
              <span>{label}</span>
            </button>
          )
        })}
      </div>
    </div>
  )
}
