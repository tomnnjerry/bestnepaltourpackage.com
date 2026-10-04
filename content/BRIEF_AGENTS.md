# Writer brief (shared by all region agents)

You are writing content for bestnepaltourpackage.com, a commercial Nepal tour agency site rendered by Django
from JSON. Project root: `C:\Projects\bestnepaltourpackage.com`.

1. Read `content/SCHEMA.md` completely before writing anything. It fixes every field, count and house rule.
2. Write ONLY inside your own folder `content/<your-region>/`. Never touch other folders or any code.
3. Create the files in this order: places (anchor places first), stays.json, festivals.json, packages,
   routes.json, guides, region.json last (its month `go` and `events` lists reference your places and festivals).
4. Validate often: `python tools/check_region.py <your-region>` until it prints OK with no ERROR lines. Fix WARN lines
   about banned words, too-long headings, thin guides and max altitude mismatches too. At the very end run it with
   `--wiki` and fix or blank any wrong `wiki` titles.
5. Accuracy beats volume. Use real altitudes, real hotel names, realistic drive times and prices. You may use
   WebSearch to confirm that a hotel still operates, an altitude, a permit rule or a Wikipedia title. If unsure,
   leave it out or say "check current status before you travel".
6. Write Python helper scripts if useful (put them in your scratchpad, not in the project), but every JSON file must
   be hand-quality prose: specific, varied, no repeated boilerplate between files. Each package's day-by-day text
   must be specific to that route (villages, hours, height gain, what you see).
7. This is a large job. Work steadily through every file; do not stop early or leave placeholders.
8. When done, reply with: the counts line from the validator, OK status, and a short list of facts you were not sure
   of (so the editor can confirm them). No other summary needed.
