const DIFFICULTIES = [
  {
    key: 'easy',
    label: 'Easy',
    subtitle: 'Famous Masterpieces',
    desc: 'Household names — works most people could name on sight',
    accent: 'border-emerald-600 hover:border-emerald-400 hover:bg-emerald-950/30',
    labelColor: 'text-emerald-400',
  },
  {
    key: 'hard',
    label: 'Hard',
    subtitle: 'Gallery Standards',
    desc: 'Works any regular museum-goer would recognize',
    accent: 'border-amber-600 hover:border-amber-400 hover:bg-amber-950/30',
    labelColor: 'text-amber-400',
  },
  {
    key: 'artHistorian',
    label: 'Art Historian',
    subtitle: 'Deep Cuts',
    desc: 'Specialist knowledge required — for the serious collector',
    accent: 'border-rose-700 hover:border-rose-500 hover:bg-rose-950/30',
    labelColor: 'text-rose-400',
  },
]

export default function DifficultyScreen({ onSelect }) {
  return (
    <div className="flex-1 flex flex-col items-center justify-center gap-8 px-4 py-8">
      <div className="text-center space-y-1">
        <h2 className="text-gray-100 font-serif text-2xl font-bold">Choose your difficulty</h2>
        <p className="text-gray-500 text-sm">Each level draws from a different pool of paintings</p>
      </div>

      <div className="flex flex-col gap-3 w-full max-w-sm">
        {DIFFICULTIES.map(({ key, label, subtitle, desc, accent, labelColor }) => (
          <button
            key={key}
            type="button"
            onClick={() => onSelect(key)}
            className={`text-left w-full bg-gray-900 border rounded-xl px-5 py-4 transition-all ${accent}`}
          >
            <div className="flex items-baseline gap-2 mb-1">
              <span className={`font-bold text-base ${labelColor}`}>{label}</span>
              <span className="text-gray-400 text-sm">{subtitle}</span>
            </div>
            <p className="text-gray-500 text-xs leading-relaxed">{desc}</p>
          </button>
        ))}
      </div>
    </div>
  )
}
