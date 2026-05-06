import { useState, useRef, useEffect } from 'react'
import Fuse from 'fuse.js'
import { paintings } from '../data/paintings'

export default function GuessBar({ onGuess, onSkip, disabled, eliminatedIds = [] }) {
  const [inputValue, setInputValue] = useState('')
  const [results, setResults] = useState([])
  const [selectedPainting, setSelectedPainting] = useState(null)
  const [showDropdown, setShowDropdown] = useState(false)
  const inputRef = useRef(null)
  const dropdownRef = useRef(null)

  const availablePaintings = paintings.filter(p => !eliminatedIds.includes(p.id))

  const fuse = new Fuse(availablePaintings, {
    keys: ['title', 'artist'],
    threshold: 0.4,
    includeScore: true,
    minMatchCharLength: 2,
  })

  const handleInput = (e) => {
    const val = e.target.value
    setInputValue(val)
    setSelectedPainting(null)

    if (val.length < 2) {
      setResults([])
      setShowDropdown(false)
      return
    }
    const hits = fuse.search(val).slice(0, 8).map(r => r.item)
    setResults(hits)
    setShowDropdown(hits.length > 0)
  }

  const handleSelect = (painting) => {
    setInputValue(`${painting.title} — ${painting.artist}`)
    setSelectedPainting(painting)
    setShowDropdown(false)
    inputRef.current?.focus()
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!selectedPainting || disabled) return
    onGuess(selectedPainting)
    setInputValue('')
    setSelectedPainting(null)
    setResults([])
  }

  // Close dropdown on outside click
  useEffect(() => {
    const handler = (e) => {
      if (!dropdownRef.current?.contains(e.target) && !inputRef.current?.contains(e.target)) {
        setShowDropdown(false)
      }
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  return (
    <form onSubmit={handleSubmit} className="space-y-2">
      <div className="relative">
        <input
          ref={inputRef}
          type="text"
          value={inputValue}
          onChange={handleInput}
          onFocus={() => results.length > 0 && setShowDropdown(true)}
          disabled={disabled}
          placeholder="Search by title or artist…"
          autoComplete="off"
          className="w-full bg-gray-900 border border-gray-700 focus:border-amber-500 rounded-xl px-4 py-3 text-gray-100 placeholder-gray-600 outline-none transition-colors disabled:opacity-40"
        />

        {showDropdown && (
          <ul
            ref={dropdownRef}
            className="absolute z-30 left-0 right-0 bottom-full mb-1 bg-gray-900 border border-gray-700 rounded-xl overflow-hidden shadow-xl max-h-64 overflow-y-auto"
          >
            {results.map(p => (
              <li key={p.id}>
                <button
                  type="button"
                  className="w-full text-left px-4 py-2.5 hover:bg-gray-800 active:bg-gray-700 transition-colors"
                  onMouseDown={(e) => { e.preventDefault(); handleSelect(p) }}
                >
                  <span className="text-gray-100 text-sm">{p.title}</span>
                  <span className="text-gray-500 text-xs ml-2">— {p.artist}</span>
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>

      <div className="flex gap-2">
        <button
          type="submit"
          disabled={!selectedPainting || disabled}
          className="flex-1 bg-amber-500 hover:bg-amber-400 active:bg-amber-600 disabled:opacity-30 disabled:cursor-not-allowed text-gray-950 font-bold py-3 rounded-xl transition-colors"
        >
          Guess
        </button>
        <button
          type="button"
          onClick={onSkip}
          disabled={disabled}
          className="px-5 bg-gray-800 hover:bg-gray-700 active:bg-gray-600 disabled:opacity-30 disabled:cursor-not-allowed text-gray-400 font-medium py-3 rounded-xl transition-colors text-sm"
        >
          Skip →
        </button>
      </div>
    </form>
  )
}
