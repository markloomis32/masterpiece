# Product Requirements Document (PRD)
**Project Name:** Masterpiece (Working Title)
**Document Status:** Draft / v1.0
**Product Type:** Web-based Daily Puzzle Game

## 1. Product Vision & Goals
**Objective:** Create an engaging, daily web-based puzzle game that challenges users to identify a famous painting through a series of progressive visual reveals and contextual clues. 
**Target Audience:** Fans of daily web puzzles (Wordle, Connections), art enthusiasts, and trivia gamers.
**Key Success Metrics:**
* Daily Active Users (DAU).
* Completion rate (percentage of users who play through to a win or loss).
* Share rate (percentage of users sharing their daily emoji grid on social media/messages).

---

## 2. Core Gameplay Loop
1.  **Onboarding:** The user arrives at the site and is presented with a brief "How to Play" modal on their first visit.
2.  **The Puzzle (Rounds 1–5):** The user is shown an obscured version of the day's painting and a text clue. They have one guess per round.
3.  **Guessing Mechanism:** The user types their guess into an autocomplete search bar (to prevent spelling errors). 
4.  **Progression:** If incorrect (or if they skip), the user advances to the next round. The image becomes clearer, the text clue becomes more specific, and the potential point reward decreases.
5.  **Resolution:** The game ends when the user guesses correctly or fails Round 5.
6.  **Post-Game:** The full, unaltered painting is revealed alongside a short educational "Fun Fact," an outbound link to the museum where it resides, and a button to copy their shareable emoji grid.

---

## 3. Mechanics & Scoring Table
The game features a descending scoring model to reward early, difficult guesses.

| Round | Visual Reveal State | Text Clue Type | Points Awarded |
| :--- | :--- | :--- | :--- |
| **1** | High-res Macro Crop (tiny detail) | Abstract / Thematic Vibe | 1,000 |
| **2** | Wider Crop (texture/palette) | Artistic Style / Movement | 800 |
| **3** | Blurred / Pixelated Full View | Historical Context | 600 |
| **4** | 50% Checkerboard Reveal | Artist Nationality / Era | 400 |
| **5** | Full Canvas (Grayscale/Inverted) | Artist Initials | 200 |

---

## 4. Power-Ups ("Art Supplies")
Users have access to a limited "Toolbox" of helper items located at the bottom of the UI. Each can only be used once per day.

* 🖌️ **The Restoration (Visual):** Allows the user to click a specific spot on the obscured canvas to reveal a small, perfectly clear circular area.
* 📜 **Curator’s Note (Context):** Unlocks an additional, highly specific trivia fact (e.g., "This painting was stolen in 1911").
* 🎨 **Palette Reveal (Color Theory):** Displays a "DNA strip" of the top 5 dominant hex colors used in the painting.
* ✂️ **The Eliminator (Logic):** Removes two incorrect autocomplete options when the user is trying to narrow down the artist or title.

---

## 5. UI / UX Requirements
* **Minimalist Interface:** Clean, gallery-like aesthetic (white or dark gray background) to make the artwork pop.
* **Mobile-First Design:** The layout must be optimized for portrait mode on mobile browsers, as the majority of users will play on their phones.
* **Autocomplete Search Bar:** Must be heavily optimized for typo-tolerance and speed. It should search across both Artist Names and Painting Titles.
* **Shareable Output:** A dynamically generated text block formatted for social sharing.
    > 🖼️ Masterpiece #12
    > ⬛ ⬛ ⬛ 🟩 ⬛
    > Score: 400
    > [Link to game]

---

## 6. Engineering & Workflow Requirements
* **Tech Stack:** Lightweight frontend framework (e.g., React, Vue, or Svelte) suitable for static hosting (Vercel, Netlify). 
* **Data Management:** A daily cron job or pre-scheduled JSON array that dictates the daily painting, ensuring all users experience the exact same puzzle simultaneously (tied to local midnight).
* **Image Handling:** Visual states (crops, blurs, grayscale) should ideally be pre-processed and stored in a CDN or cloud bucket (like AWS S3) rather than processed client-side, to ensure fast loading times and prevent tech-savvy users from inspecting the source code to find the original image URL.
* **Development Workflow:** The repository should be configured from day one with automated CI/CD checks to ensure stable deployments. Additionally, to accelerate development and maintain code quality, the root of the repository must include a dedicated instruction markdown file explicitly designed for AI coding assistants (like Claude). This file will govern code style, architecture rules, and testing requirements to streamline automated code review and debugging processes.

---

## 7. Future Scope (Post-Launch)
* **Player Profiles:** Local storage tracking for win streaks, average score, and total games played.
* **The "Golden Brush":** A reward for a 5-day streak that grants a special, powerful hint on a future puzzle.
* **Themed Weeks:** Specially curated weeks (e.g., "Renaissance Week" or "Women in Art Week").
