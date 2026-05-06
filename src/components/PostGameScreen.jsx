import { useState } from 'react'
import { buildShareText } from '../utils/shareUtils'

export default function PostGameScreen({ puzzle, guesses, score, status }) {
  const [copied, setCopied] = useState(false)

  if (!puzzle) return null

  const won = status === 'won'

  const handleShare = async () => {
    const text = buildShareText(puzzle.id, guesses, score)
    try {
      await navigator.clipboard.writeText(text)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch {
      // fallback for older browsers
      const ta = document.createElement('textarea')
      ta.value = text
      document.body.appendChild(ta)
      ta.select()
      document.execCommand('copy')
      document.body.removeChild(ta)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  return (
    <div className="space-y-4">
      {/* Result banner */}
      <div className={`rounded-xl p-4 text-center ${won ? 'bg-green-900/40 border border-green-700/50' : 'bg-gray-900 border border-gray-800'}`}>
        <div className="text-2xl mb-1">{won ? '🎉' : '😔'}</div>
        <p className={`font-bold text-lg ${won ? 'text-green-300' : 'text-gray-400'}`}>
          {won ? `+${score.toLocaleString()} points` : 'Better luck tomorrow!'}
        </p>
        {!won && (
          <p className="text-gray-500 text-sm mt-1">
            It was <span className="text-gray-300">{puzzle.title}</span> by {puzzle.artist}
          </p>
        )}
      </div>

      {/* Full painting reveal */}
      <div className="relative rounded-xl overflow-hidden aspect-[4/3] bg-gray-900">
        <img
          src={puzzle.imageUrl}
          alt={`${puzzle.title} by ${puzzle.artist}`}
          className="w-full h-full object-cover"
          crossOrigin="anonymous"
        />
        <div className="absolute bottom-0 inset-x-0 bg-gradient-to-t from-black/80 to-transparent p-4">
          <p className="text-white font-serif font-bold text-lg leading-tight">{puzzle.title}</p>
          <p className="text-gray-300 text-sm">{puzzle.artist}, {puzzle.year}</p>
        </div>
      </div>

      {/* Fun fact */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
        <p className="text-xs text-gray-500 uppercase tracking-widest mb-2">Fun Fact</p>
        <p className="text-gray-300 text-sm leading-relaxed">{puzzle.funFact}</p>
        <a
          href={puzzle.museumUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1 text-amber-400 hover:text-amber-300 text-xs mt-3 transition-colors"
        >
          View at {puzzle.museum} ↗
        </a>
      </div>

      {/* Share button */}
      <button
        onClick={handleShare}
        className="w-full bg-gray-800 hover:bg-gray-700 active:bg-gray-600 text-gray-200 font-medium py-3 rounded-xl transition-colors flex items-center justify-center gap-2"
      >
        {copied ? '✓ Copied to clipboard!' : '📋 Share your result'}
      </button>

      <p className="text-center text-gray-600 text-xs">A new painting drops at midnight 🕛</p>
    </div>
  )
}
