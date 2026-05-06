const ROUND_EMOJI = { correct: '🟩', wrong: '⬛', skipped: '⬛', unplayed: '⬜' }

export function buildShareText(puzzleId, guesses, score, totalRounds = 5) {
  const grid = Array.from({ length: totalRounds }, (_, i) => {
    const roundNum = i + 1
    const guess = guesses.find(g => g.round === roundNum)
    if (!guess) return ROUND_EMOJI.unplayed
    if (guess.correct) return ROUND_EMOJI.correct
    if (guess.skipped) return ROUND_EMOJI.skipped
    return ROUND_EMOJI.wrong
  })

  const scoreText = score > 0 ? `Score: ${score}` : 'Better luck tomorrow!'

  return [
    `🖼️ Masterpiece #${puzzleId}`,
    grid.join(' '),
    scoreText,
    'https://masterpiece.game',
  ].join('\n')
}
