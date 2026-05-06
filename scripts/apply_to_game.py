#!/usr/bin/env python3
"""
Injects clues, fun facts, and curator's notes into game_puzzles_partial.json,
assigns puzzle IDs and dates, then writes directly to:
  src/data/puzzles.json   (merges with existing 7 placeholder puzzles)
  src/data/paintings.js   (merges existing 45 entries with the 21 new Met paintings)
"""

import json
from pathlib import Path
from datetime import date, timedelta

SRC_DATA  = Path("src/data")
PARTIAL   = Path("scripts/output/game_puzzles_partial.json")

# ---------------------------------------------------------------------------
# Editorial content keyed by paintingId (101–121)
# ---------------------------------------------------------------------------

CONTENT = {
    101: {
        "funFact": (
            "This colossal painting (12 × 21 feet) was actually painted in Düsseldorf, Germany "
            "by Emanuel Leutze, a German-American artist. He used the Rhine River as a stand-in "
            "for the Delaware. The original version was damaged by fire and flood; what hangs in "
            "the Met is the second, improved version, completed in 1851."
        ),
        "curatorsNote": (
            "The painting is full of historical inaccuracies: the flag shown wasn't yet in use, "
            "the boats are too small, and the crossing happened in pitch darkness, not at dawn. "
            "Leutze was painting a symbol of courage and determination — not a documentary record."
        ),
        "clues": {
            "round1": "A crowded boat pushes through icy, churning waters in the dead of winter toward an uncertain shore",
            "round2": "An epic Romantic history painting, monumental in both scale and patriotic ambition, depicting a turning point in war",
            "round3": "Depicts a pivotal surprise attack launched on the night of December 25, 1776 during the American Revolutionary War",
            "round4": "Painted in 1851 by a German-American artist in Düsseldorf; the heroic scene takes place in New Jersey",
            "round5": "Artist initials: E.L.",
        },
    },
    102: {
        "funFact": (
            "When Madame X debuted at the Paris Salon of 1884, the original version showed one "
            "strap of her dress fallen suggestively off her shoulder. The scandal was so severe "
            "that Sargent repainted the strap upright, but the damage was done — he abandoned "
            "Paris and moved to London."
        ),
        "curatorsNote": (
            "The subject, Virginie Gautreau, was a Louisiana-born American socialite famous in "
            "Paris for her beauty and her habit of powdering her skin with lavender-tinted powder, "
            "giving her the distinctively cool, bluish complexion Sargent preserved forever in paint."
        ),
        "clues": {
            "round1": "A pale figure in a low-cut black gown turns in sharp profile against a dark background, every line deliberate and severe",
            "round2": "A Gilded Age portrait combining Realist technique with bold, almost theatrical composition — and a scandal at its first showing",
            "round3": "Exhibited at the Paris Salon of 1884, the painting outraged audiences and effectively ended the artist's career in France",
            "round4": "Painted by an American expatriate artist working in Paris and London in the late 19th century",
            "round5": "Artist initials: J.S.S.",
        },
    },
    103: {
        "funFact": (
            "David painted this just two years before the French Revolution, and it was immediately "
            "read as a political manifesto about civic virtue and dying for one's beliefs. It became "
            "an icon of the revolutionary movement and secured David's reputation as the greatest "
            "Neoclassical painter in France."
        ),
        "curatorsNote": (
            "One key historical detail is deliberately wrong: Plato, who was present at Socrates' "
            "death, is shown here as the solemn elderly man at the foot of the bed — but Plato was "
            "only in his late twenties at the time. David aged him to lend the scene greater gravity."
        ),
        "clues": {
            "round1": "A serene, muscular figure in a stone chamber gestures upward while surrounded by grieving companions",
            "round2": "A defining work of French Neoclassicism, celebrating stoic virtue through a scene drawn from ancient Greek philosophy",
            "round3": "Painted in 1787, just two years before the French Revolution, and widely read as a call to civic courage",
            "round4": "Painted by a French artist who would later become the official court painter of Napoleon Bonaparte",
            "round5": "Artist initials: J.-L.D.",
        },
    },
    104: {
        "funFact": (
            "Van Gogh painted three versions of this composition in the summer of 1889 while staying "
            "at the Saint-Paul-de-Mausole asylum in Saint-Rémy. He wrote to his brother Theo that "
            "cypresses were 'as beautiful as an Egyptian obelisk.' The Met's version is considered "
            "the finest of the three."
        ),
        "curatorsNote": (
            "The specific wheat field Van Gogh painted has been identified — it is located just "
            "outside the asylum walls and is still recognizable today. Van Gogh had to request "
            "special permission from the asylum director each time he wanted to go outside to paint."
        ),
        "clues": {
            "round1": "Vigorous, swirling brushstrokes animate a golden field beneath a turbulent sky, with dark flame-like trees on the right",
            "round2": "A Post-Impressionist landscape in which every element — grass, clouds, and trees — vibrates with the same restless energy",
            "round3": "Painted in the summer of 1889 by an artist recuperating at an asylum in Provence, southern France",
            "round4": "Painted by a Dutch artist while a voluntary patient in Saint-Rémy; he described cypresses in letters to his brother",
            "round5": "Artist initials: V.V.G.",
        },
    },
    105: {
        "funFact": (
            "Van Gogh painted over 35 self-portraits in just three years (1885–1889), partly "
            "because he couldn't afford to pay models and wanted to practice painting faces. "
            "This one was made during his stay in Paris, where contact with the Impressionists "
            "and Pointillists transformed his palette from dark to vivid."
        ),
        "curatorsNote": (
            "This self-portrait is painted on the reverse side of another Van Gogh work, "
            "The Potato Peeler, on the same physical canvas. During conservation work at the Met, "
            "the two paintings were carefully separated and are now displayed independently."
        ),
        "clues": {
            "round1": "A direct, probing gaze beneath a wide-brimmed summer hat, rendered in short, confident dabs of bright color",
            "round2": "A Post-Impressionist self-portrait showing clear influence from Impressionism and Pointillism during the artist's Paris years",
            "round3": "One of more than 35 self-portraits made between 1885 and 1889 — painted cheaply, as a substitute for hired models",
            "round4": "Painted by a Dutch artist during his two years in Paris, where exposure to French avant-garde painting transformed his style",
            "round5": "Artist initials: V.V.G.",
        },
    },
    106: {
        "funFact": (
            "The Harvesters is part of a series of five large panels Bruegel painted depicting "
            "the months of the year — one of the first secular landscape series in Western art. "
            "This panel represents late summer, August or September. The five surviving panels "
            "are now split between New York, Vienna, and Prague."
        ),
        "curatorsNote": (
            "Look closely at the lower right corner: workers are taking a lunch break in the "
            "shade of a pear tree, including a figure sprawled asleep on the ground. This candid, "
            "unsentimental portrayal of peasant rest was considered bold — Bruegel observed ordinary "
            "life with a dignity that was entirely new."
        ),
        "clues": {
            "round1": "A vast golden landscape stretches under a hazy summer sky, with tiny figures laboring in fields that reach to the horizon",
            "round2": "A Flemish Renaissance masterwork from a pioneering seasonal series that elevated landscape and peasant life to the status of high art",
            "round3": "One of five surviving panels from a 1565 commission depicting the months; among the first great secular landscape paintings in history",
            "round4": "Painted by a Flemish artist from the Southern Netherlands, considered the greatest painter of the Northern Renaissance",
            "round5": "Artist initials: P.B.",
        },
    },
    107: {
        "funFact": (
            "Van Gogh painted irises repeatedly, finding in their twisted, organic forms the same "
            "expressive energy he saw in wheat fields and cypresses. In letters to his brother, "
            "he described working on irises as his 'lightning rod' — a way to stay anchored during "
            "his most turbulent mental periods."
        ),
        "curatorsNote": (
            "This version was painted in Auvers-sur-Oise in 1890, in the final months of Van Gogh's "
            "life — distinct from the more famous Irises at the Getty Museum, which was painted "
            "a year earlier in Saint-Rémy. The lighter, more open background reflects the brighter "
            "mood of his final spring."
        ),
        "clues": {
            "round1": "Dense clusters of deep violet-blue flowers emerge from a tangle of curved green stems and leaves",
            "round2": "A Post-Impressionist floral study with bold outlines and vibrant complementary color contrasts recalling Japanese woodblock prints",
            "round3": "Painted in 1890 during the final year of the artist's life; he described flowers as a refuge from psychological distress",
            "round4": "Painted by a Dutch artist in the French village of Auvers-sur-Oise, where he died two months after completing this work",
            "round5": "Artist initials: V.V.G.",
        },
    },
    108: {
        "funFact": (
            "Degas painted and drew the subject of ballet dancers over 1,500 times — more than half "
            "his entire output. He had special backstage access to the Paris Opéra and was fascinated "
            "not by the performance itself but by the rehearsal: the effort, discipline, and tedium "
            "invisible to the audience."
        ),
        "curatorsNote": (
            "The older man leaning on a staff at the center is Jules Perrot, a real and celebrated "
            "ballet master who choreographed Giselle. He was well past his prime when Degas painted "
            "him here, lending the scene an air of passing time and the bittersweet weight of a "
            "career's end."
        ),
        "clues": {
            "round1": "Young figures in white tutus fill a large practice room, caught mid-movement or waiting, observed by an older man with a staff",
            "round2": "An Impressionist interior celebrated for its asymmetric composition, cropped framing, and candid backstage observation",
            "round3": "Painted in 1874, offering an unprecedented view of the rehearsal rooms and rigorous training behind the Paris Opéra",
            "round4": "Painted by a French Impressionist who had special access to the Paris Opéra and devoted his career to studying dancers",
            "round5": "Artist initials: E.D.",
        },
    },
    109: {
        "funFact": (
            "The Met's Sunflowers is one of Van Gogh's early sunflower paintings, made in Paris "
            "in 1887. Unlike the famous yellow-on-yellow Arles series (now in London, Amsterdam, "
            "and Munich), this version shows cut flowers lying flat on a surface, exploring decay "
            "and the cycle of life as much as beauty."
        ),
        "curatorsNote": (
            "Van Gogh painted two distinct sunflower series a year apart: the Paris series (1887, "
            "cut flowers on a surface, exploring wilting and color) and the Arles series (1888–89, "
            "flowers in a vase, celebrating life). The Met's painting is the finest example of "
            "the earlier, more melancholy Paris series."
        ),
        "clues": {
            "round1": "Heavy-headed flowers, some fully open and some already wilting, rendered in thick impasto paint against a plain surface",
            "round2": "A Post-Impressionist still life — bold and direct — marking a turning point away from the artist's earlier, darker palette",
            "round3": "Painted in Paris in 1887, before the more famous Arles sunflower series; it dwells on beauty in the process of fading",
            "round4": "Painted by a Dutch artist during his two years in Paris, where encounters with Impressionism radically brightened his color",
            "round5": "Artist initials: V.V.G.",
        },
    },
    110: {
        "funFact": (
            "This painting was commissioned in 1652 by a Sicilian nobleman who asked Rembrandt "
            "simply for 'a philosopher.' It was purchased by the Metropolitan Museum of Art in "
            "1961 for $2.3 million — a world record auction price at the time, front-page news "
            "across the United States."
        ),
        "curatorsNote": (
            "Look at the hand resting on Homer's marble bust — it is an extraordinarily tender, "
            "almost sorrowful gesture. Rembrandt seems to suggest that Aristotle, the supreme "
            "philosopher, envies Homer, the poet: that reason envies feeling, and the mind envies "
            "the heart."
        ),
        "clues": {
            "round1": "A richly robed figure in warm golden light places a contemplative hand on a white marble bust",
            "round2": "A Dutch Golden Age painting at the peak of Rembrandt's mature style — celebrated for its profound psychological depth and chiaroscuro",
            "round3": "Commissioned in 1653 by a Sicilian nobleman; when it sold at auction in 1961, the price set a world record",
            "round4": "Painted by a 17th-century Dutch master in Amsterdam; the subject is a philosopher from ancient Greece",
            "round5": "Artist initials: R.V.R.",
        },
    },
    111: {
        "funFact": (
            "Van Gogh painted five versions of La Berceuse, all depicting Augustine Roulin, "
            "wife of his postman friend Joseph Roulin. He planned to display the five canvases "
            "as a triptych flanked by two of his Sunflowers paintings — like a sailor's altarpiece "
            "that would bring comfort to 'simple sailors' far from home."
        ),
        "curatorsNote": (
            "The rope in Augustine's hands disappears off the bottom of the canvas — she is rocking "
            "an unseen cradle just out of frame. The deliberately loud, clashing floral wallpaper "
            "was Van Gogh's intentional choice, meant to create a hypnotic, lullaby-like effect "
            "through color rather than sound."
        ),
        "clues": {
            "round1": "A broad-faced woman sits squarely in the center, hands folded, against an intensely patterned and almost overwhelming floral background",
            "round2": "A Post-Impressionist portrait combining frontal, icon-like composition with deliberately loud, decorative color — described by the artist as a 'lullaby in paint'",
            "round3": "One of five versions painted in early 1889; the artist intended all five to be displayed together alongside paintings of sunflowers",
            "round4": "Painted by a Dutch artist while living in Arles, France; the subject is the wife of his close friend, the local postman",
            "round5": "Artist initials: V.V.G.",
        },
    },
    112: {
        "funFact": (
            "The Roulin family — postman Joseph, his wife Augustine, and their children — were "
            "among Van Gogh's closest companions in Arles and his most frequent portrait subjects. "
            "Baby Marcelle, shown here, was born in July 1888 and was just four months old when "
            "this was painted."
        ),
        "curatorsNote": (
            "Van Gogh painted this tender mother-and-child scene in late November 1888, just weeks "
            "before his famous breakdown and the episode in which he cut off part of his own ear. "
            "Despite the turmoil in his private life, the painting has a rare and surprising calm."
        ),
        "clues": {
            "round1": "A mother in a green dress holds a wide-eyed infant in her lap, both looking directly at the viewer",
            "round2": "A Post-Impressionist double portrait using flat color areas and bold outlines influenced by Japanese woodblock prints",
            "round3": "Painted in Arles in November 1888, weeks before a famous breakdown; the subjects were the artist's closest friends at the time",
            "round4": "Painted by a Dutch artist while living in southern France; the subjects are a postal worker's wife and infant child",
            "round5": "Artist initials: V.V.G.",
        },
    },
    113: {
        "funFact": (
            "These worn leather shoes became the subject of a famous philosophical dispute. "
            "Martin Heidegger cited a Van Gogh shoe painting in his 1935 essay 'The Origin of "
            "the Work of Art,' claiming the shoes belonged to a peasant woman. Art historian "
            "Meyer Schapiro later countered that they were actually the artist's own city shoes."
        ),
        "curatorsNote": (
            "Heidegger wrote: 'From the dark opening of the worn insides of the shoes the toilsome "
            "tread of the worker stares forth.' Schapiro replied, bluntly, that Heidegger had "
            "projected a fantasy onto a pair of shoes Van Gogh had bought himself in a Paris "
            "market and wore around the city."
        ),
        "clues": {
            "round1": "A pair of heavily worn, unlaced leather shoes sits alone on a plain surface, painted with thick, expressive brushwork",
            "round2": "A Post-Impressionist still life that transforms a mundane discarded object into a subject of existential weight",
            "round3": "This humble subject sparked a famous 20th-century philosophical debate about meaning, labor, and what art reveals",
            "round4": "Painted by a Dutch artist while living in Paris; the objects depicted were reportedly his own personal belongings",
            "round5": "Artist initials: V.V.G.",
        },
    },
    114: {
        "funFact": (
            "To research this painting, Bonheur spent 18 months attending the Paris horse market "
            "every week — dressed as a man, because women were not allowed to attend unaccompanied. "
            "She had to apply to the Paris police for special dispensation to wear trousers in "
            "public, which she renewed every six months."
        ),
        "curatorsNote": (
            "When exhibited at the Paris Salon of 1853, The Horse Fair was an immediate sensation. "
            "It was sent on a triumphant tour of Britain and the United States, and Queen Victoria "
            "requested a private viewing. At over 8 × 16 feet, it is the largest painting "
            "Bonheur ever completed."
        ),
        "clues": {
            "round1": "Powerful horses rear and surge in a churning mass of bodies, manes, and dust against a stormy sky",
            "round2": "A monumental Realist painting giving working animals the dramatic scale and grandeur traditionally reserved for history painting",
            "round3": "Exhibited at the Paris Salon of 1853 to immediate acclaim; the artist attended her subject for 18 months disguised as a man",
            "round4": "Painted by a celebrated French female artist who was one of the most acclaimed painters in mid-19th century Europe",
            "round5": "Artist initials: R.B.",
        },
    },
    115: {
        "funFact": (
            "When buyers asked Homer to change the ending — to add a visible rescue ship — he "
            "refused absolutely. A ship IS faintly visible on the horizon, but whether it will "
            "arrive in time is left completely open. Homer's reply: 'The subject is the gulf "
            "stream and the small figure — that is all.'"
        ),
        "curatorsNote": (
            "Homer exhibited this painting in 1900, at the height of Jim Crow-era racial violence "
            "in America. The subject — a Black man adrift and abandoned at sea, surrounded by "
            "sharks — was widely understood as a comment on the condition of Black Americans. "
            "Homer refused all interviews about its meaning."
        ),
        "clues": {
            "round1": "A lone figure lies across the deck of a small, damaged boat surrounded by a dark sea, circling sharks, and a distant waterspout",
            "round2": "An American Realist painting combining raw naturalism with powerful social undertones about survival, fate, and abandonment",
            "round3": "Painted in 1899 and exhibited in 1900 at a time of intense racial violence in the United States; the artist refused to explain it",
            "round4": "Painted by a major American artist known for seascapes and unflinching scenes of humans confronting the forces of nature",
            "round5": "Artist initials: W.H.",
        },
    },
    116: {
        "funFact": (
            "This painting was originally exhibited at the American Art-Union in 1845 under the "
            "title 'French Trader and Half-Breed Son.' The Met renamed it Fur Traders Descending "
            "the Missouri when it acquired the work. The mysterious black animal tied to the bow "
            "has been debated for 175 years — most likely a fox cub or a young bear."
        ),
        "curatorsNote": (
            "Bingham creates an uncanny, dreamlike mood entirely at odds with the rugged frontier "
            "subject: the two figures are utterly motionless, drifting on a glassy, mirror-smooth "
            "river, their reflections dissolving below them. The golden haze gives the American "
            "wilderness an almost mythological, timeless quality."
        ),
        "clues": {
            "round1": "Two figures drift in perfect stillness on a glassy river at dawn, with a mysterious dark animal tied at the front of their canoe",
            "round2": "An American Romantic painting of frontier life with an unusual, dreamlike stillness and a golden, almost mythological atmosphere",
            "round3": "Painted in 1845 and first exhibited under a different, racially charged title; it helped define the visual mythology of the American West",
            "round4": "Painted by an American artist from Missouri who devoted his career to documenting life on the Mississippi and Missouri Rivers",
            "round5": "Artist initials: G.C.B.",
        },
    },
    117: {
        "funFact": (
            "Bierstadt joined a government survey expedition to Wyoming in 1859, gathering "
            "sketches that would fuel paintings for a decade. When this canvas — over 10 feet "
            "wide — was exhibited in New York, crowds paid admission to view it. Critics compared "
            "the experience to watching a theatrical spectacle."
        ),
        "curatorsNote": (
            "The painting was often displayed in darkened rooms with theatrical lighting to "
            "maximize the drama of its glowing peaks — essentially a cinematic experience engineered "
            "a century before cinema. Bierstadt deliberately made the mountains taller and the "
            "light more golden than any photograph could capture."
        ),
        "clues": {
            "round1": "Impossibly tall, snow-capped peaks rise above a sunlit valley, with a waterfall and a Native American encampment in the foreground",
            "round2": "A monumental Hudson River School landscape in the Luminist tradition, celebrating the sublime grandeur of untamed American wilderness",
            "round3": "Painted in 1863 based on sketches made during a government survey expedition to the Wind River Mountains of Wyoming in 1859",
            "round4": "Painted by a German-American artist who became the preeminent painter of the American West in the 19th century",
            "round5": "Artist initials: A.B.",
        },
    },
    118: {
        "funFact": (
            "Homer painted this scene just seven years after the end of the Civil War, and its "
            "images of carefree rural childhood had deep emotional resonance for a nation trying "
            "to heal. He later made a widely circulated wood engraving of the same composition "
            "for Harper's Weekly, giving the image mass distribution across the country."
        ),
        "curatorsNote": (
            "The one-room schoolhouse in the background was a powerful symbol of democratic "
            "values and equal opportunity in the postwar United States. Homer sets the exuberant "
            "game in the foreground against this emblem of civic order — childhood energy held "
            "gently in check by the institutions of a recovering republic."
        ),
        "clues": {
            "round1": "A line of barefoot boys in suspenders plays a running game in a sunlit meadow, a small white schoolhouse visible behind them",
            "round2": "An American Realist painting celebrated for its direct, unsentimental observation of rural childhood in the years after the Civil War",
            "round3": "Painted in 1872, seven years after the end of the Civil War; images of innocent childhood carried particular weight for a nation healing from trauma",
            "round4": "Painted by an American artist who was also a celebrated illustrator for Harper's Weekly, giving his images a national audience",
            "round5": "Artist initials: W.H.",
        },
    },
    119: {
        "funFact": (
            "Vermeer's entire authenticated output is just 34 to 36 paintings across roughly "
            "20 years of work — fewer than Van Gogh painted in a single month. He worked slowly, "
            "sold through a single dealer in Delft, and died in 1675 leaving 11 children and a "
            "mountain of debt. He was largely forgotten until rediscovered in the 1860s."
        ),
        "curatorsNote": (
            "X-ray analysis of this painting revealed that Vermeer originally included a map on "
            "the back wall and a jewelry box on the table, then removed both to simplify the "
            "composition. The woman is shown opening a window — a recurring Vermeer motif — "
            "to let in the cool morning light."
        ),
        "clues": {
            "round1": "A woman in a white headdress leans gently toward a window, morning light falling softly across her face and linen clothing",
            "round2": "A Dutch Golden Age interior scene — intimate and perfectly still — demonstrating the artist's unparalleled mastery of natural light on everyday surfaces",
            "round3": "Painted around 1662 by a Delft master who produced only 34–36 known works in his entire career and died leaving his family in debt",
            "round4": "Painted by a 17th-century Dutch artist who was almost entirely forgotten after his death and rediscovered by art historians in the 1860s",
            "round5": "Artist initials: J.V.",
        },
    },
    120: {
        "funFact": (
            "This is one of the earliest known Western paintings to depict a scene of everyday "
            "commercial life as its primary subject — a radical choice in 1449. The 'goldsmith' "
            "shown may actually be Saint Eligius, patron saint of goldsmiths, depicted in "
            "secular clothing to blend religious subject matter with genre painting."
        ),
        "curatorsNote": (
            "The small convex mirror in the lower right corner — a standard goldsmith's "
            "tool to watch the whole shop — reflects two elegantly dressed figures standing "
            "outside in the street. This device anticipates the famous convex mirror in Jan "
            "van Eyck's Arnolfini Portrait, though this painting was made 14 years earlier."
        ),
        "clues": {
            "round1": "A craftsman behind a well-lit counter examines precious objects, surrounded by the tools, scales, and goods of his trade",
            "round2": "A landmark Early Netherlandish painting — among the first Western works to give a scene of everyday commerce the full dignity of high art",
            "round3": "Painted in 1449; the figure depicted may be Saint Eligius, patron of goldsmiths, shown in secular dress as a cunning devotional disguise",
            "round4": "Painted by a 15th-century Flemish artist from Bruges, then the wealthiest trading city in northern Europe",
            "round5": "Artist initials: P.C.",
        },
    },
    121: {
        "funFact": (
            "Van Gogh wrote to his brother Theo about cypresses with unusual intensity: "
            "'It astonishes me that they have not yet been done as I see them... beautiful "
            "as regards line and proportion, like an Egyptian obelisk. And the green has "
            "such a distinguished quality. It is a splash of black in a sunny landscape.' "
            "He wanted to dedicate an entire series to them."
        ),
        "curatorsNote": (
            "Unlike the Wheat Field with Cypresses (also in the Met, painted the same month), "
            "this canvas places a single massive cypress at its center, filling almost the "
            "entire frame. The swirling treatment of the trunk and the turbulent stars in the "
            "upper right directly anticipate The Starry Night, painted weeks later."
        ),
        "clues": {
            "round1": "A single massive dark tree, its form twisting upward like a flame, dominates the entire canvas against a swirling sky",
            "round2": "A Post-Impressionist painting in which every brushstroke — sky, earth, and tree alike — follows the same restless, turbulent energy",
            "round3": "Painted in June 1889 at an asylum in Provence, weeks before a more famous painting of a night sky over a village",
            "round4": "Painted by a Dutch artist who called these trees 'as beautiful as an Egyptian obelisk' and planned a full series devoted to them",
            "round5": "Artist initials: V.V.G.",
        },
    },
}

# ---------------------------------------------------------------------------
# Date assignment — new puzzles start the day after the existing 7
# ---------------------------------------------------------------------------

START_DATE    = date(2026, 5, 12)
START_PUZZLE_ID = 8  # existing puzzles are 1–7


def main():
    # Load partial output
    raw = json.loads(PARTIAL.read_text())
    partial_puzzles = raw["puzzles"]

    # Load existing game puzzles
    existing_path = SRC_DATA / "puzzles.json"
    existing = json.loads(existing_path.read_text())
    existing_puzzles = existing["puzzles"]

    # Build new puzzle entries
    new_puzzles = []
    for i, p in enumerate(partial_puzzles):
        pid = p["paintingId"]
        content = CONTENT.get(pid, {})

        if not content:
            print(f"  ⚠️  No content for paintingId {pid} ({p['title']}) — skipping")
            continue

        puzzle_date = START_DATE + timedelta(days=i)
        puzzle_id   = START_PUZZLE_ID + i

        new_puzzles.append({
            "id":            puzzle_id,
            "date":          puzzle_date.isoformat(),
            "paintingId":    pid,
            "title":         p["title"],
            "artist":        p["artist"],
            "year":          p["year"],
            "museum":        p["museum"],
            "museumUrl":     p["museumUrl"],
            "imageUrl":      p["imageUrl"],
            "dominantColors": p["dominantColors"],
            "funFact":       content["funFact"],
            "curatorsNote":  content["curatorsNote"],
            "clues":         content["clues"],
        })
        print(f"  ✅ #{puzzle_id} ({puzzle_date}) — {p['title']} — {p['artist']}")

    # Write merged puzzles.json
    all_puzzles = {"puzzles": existing_puzzles + new_puzzles}
    existing_path.write_text(json.dumps(all_puzzles, indent=2, ensure_ascii=False))
    print(f"\n📅 puzzles.json: {len(existing_puzzles)} existing + {len(new_puzzles)} new = {len(all_puzzles['puzzles'])} total")

    # -----------------------------------------------------------------------
    # Merge paintings.js
    # -----------------------------------------------------------------------
    # Read existing paintings list from the JS source
    paintings_path = SRC_DATA / "paintings.js"
    existing_js = paintings_path.read_text()

    # Parse existing entries
    import re
    existing_entries = re.findall(
        r'\{\s*id:\s*(\d+),\s*title:\s*(\'[^\']*\'|"[^"]*"),\s*artist:\s*(\'[^\']*\'|"[^"]*")\s*\}',
        existing_js
    )
    existing_ids = {int(e[0]) for e in existing_entries}

    # Load new paintings from cleaned output
    new_paintings_js = Path("scripts/output/game_paintings.js").read_text()
    new_entries = re.findall(
        r'\{\s*id:\s*(\d+),\s*title:\s*(\'[^\']*\'|"[^"]*"),\s*artist:\s*(\'[^\']*\'|"[^"]*")\s*\}',
        new_paintings_js
    )

    # Deduplicate by (title, artist) — keep new entry if same title+artist already exists
    def unquote(s):
        return s.strip('"\'')

    existing_ta = {(unquote(e[1]).lower(), unquote(e[2]).lower()) for e in existing_entries}
    truly_new = [e for e in new_entries if (unquote(e[1]).lower(), unquote(e[2]).lower()) not in existing_ta]
    duplicates = [e for e in new_entries if (unquote(e[1]).lower(), unquote(e[2]).lower()) in existing_ta]

    if duplicates:
        print("\n  ℹ️  Skipping duplicates already in paintings.js:")
        for d in duplicates:
            print(f"       id {d[0]}: {unquote(d[1])} — {unquote(d[2])}")

    # Build final merged list — original entries first, then new
    all_js_lines = []
    for e in existing_entries:
        all_js_lines.append(
            f'  {{ id: {int(e[0]):>3}, title: {e[1]:<55}, artist: {e[2]} }},'
        )
    for e in truly_new:
        all_js_lines.append(
            f'  {{ id: {int(e[0]):>3}, title: {e[1]:<55}, artist: {e[2]} }},'
        )

    merged_js = "export const paintings = [\n" + "\n".join(all_js_lines) + "\n]\n"
    paintings_path.write_text(merged_js)
    print(f"\n🖼️  paintings.js: {len(existing_entries)} existing + {len(truly_new)} new = {len(all_js_lines)} total")
    print("\n✅ Done. Run `npm run dev` to test the updated game.")


if __name__ == "__main__":
    main()
