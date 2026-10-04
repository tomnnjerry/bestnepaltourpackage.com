# Best Nepal Tour Package: content schema and house rules

Best Nepal Tour Package (bestnepaltourpackage.com) is a commercial tour agency selling Nepal tour packages,
helicopter tours, treks, pilgrimages, wildlife safaris, adventure sports and Kailash Mansarovar yatras via Nepal.
Byline on everything: "Best Nepal Tour Package Travel Desk". Voice: confident, clear, helpful, first person plural
("we"). We sell, but we sell with facts: prices, days, altitudes, hours, distances.
Audience: Indian families, couples, pilgrims and groups (largest market, prices in INR) plus international
trekkers and travellers (prices also in USD).

The site covers twelve regions (folder slug → name):
`kathmandu-valley` Kathmandu Valley · `pokhara` Pokhara & the Middle Hills · `annapurna` Annapurna ·
`mustang` Mustang & Dolpo · `everest` Everest & Khumbu · `langtang` Langtang & Gosaikunda ·
`manaslu` Manaslu & Tsum Valley · `chitwan` Chitwan & the Central Terai · `lumbini` Lumbini & the Buddha's Nepal ·
`east-nepal` Kanchenjunga & the East · `far-west` Rara & the Far West · `kailash` Kailash & Tibet (via Nepal)

All content is JSON, UTF-8, under `content/<region-slug>/`. The Django site renders every page from these
files, so the JSON must parse (no comments, no trailing commas). Slugs are lowercase-hyphenated ASCII and
unique within their type across the WHOLE site (prefix with the place or region if needed,
e.g. `namche-sherpa-museum-walk`, `everest-base-camp-trek-14-days`).

## Writing rules (strict)

- Headings and titles: no full stop at the end; short, one line on desktop (≤ 60 characters).
- Plain and specific: numbers over adjectives (km, hours, metres, INR, USD, months, °C).
- BANNED words/phrases: nestled, breathtaking, hidden gem, paradise, tapestry, embark, delve, unleash, vibrant,
  bustling, mesmerizing, stunning, magical, heaven on earth, a feast for the eyes, something for everyone,
  whether you're, look no further, ultimate guide, in this blog, in conclusion, unforgettable, world-class,
  seamless, curated, elevate, immerse, timeless, jewel, iconic (max once per file), boasts, once-in-a-lifetime,
  bucket list, hassle-free.
- No emoji. No exclamation marks.
- Never claim "No. 1", "best-selling", "award-winning", "trusted by thousands", years in business, licence numbers,
  staff names, client counts, reviews, star ratings or statistics about the company. Facts about places only.
- Facts that change (permits, fees, flight schedules, heli landing rules, Kailash rules for Indian passport holders,
  road openings, park closures, festival dates): state the rule as you understand it and add
  "check current status before you travel".
- Altitudes in metres, from reliable sources (e.g. Everest Base Camp 5,364 m, Kala Patthar 5,644 m, Thorong La 5,416 m,
  Muktinath 3,710 m, Gosaikunda 4,380 m, Namche Bazaar 3,440 m, Kathmandu 1,400 m, Pokhara 822 m).
- Prices: indicative "from" price per person, twin sharing. Give BOTH `price_from_inr` (round to the nearest 1,000)
  and `price_from_usd` (round to the nearest 10). Be realistic for a commercial agency, for example:
  Kathmandu 3N city break ₹14,000–25,000 (3-star) · Kathmandu–Pokhara–Chitwan 6N ₹28,000–45,000 (3-star),
  ₹95,000+ at 5-star · Everest Base Camp trek 12–14 days with Lukla flights US$1,300–1,800 ·
  Annapurna Base Camp trek 10–12 days US$750–1,100 · Everest heli tour with landing, shared seat, US$1,100–1,400
  (private 5-seat charter US$5,000–6,500 per helicopter) · Muktinath heli from Pokhara ≈ ₹45,000–65,000 per seat ·
  Kailash overland via Kerung 12–15 days ₹1,90,000–2,60,000 · Kailash via Simikot by helicopter ₹2,60,000–3,60,000 ·
  Chitwan 2N safari package ₹12,000–20,000. Say in `good_to_know` what the price assumes.
- Hotels and lodges: REAL, currently operating properties only (3-star to 5-star hotels, well-known lodges and
  resorts, notable teahouse lodges like Yeti Mountain Home or Hotel Everest View). Do not invent amenities, room counts,
  awards or prices. If unsure a property still operates, leave it out.
- Distances and drive times by road must be realistic for Nepal's roads ("≈ 200 km · 6–7 h").
- `best_months` is ALWAYS an array of 12 integers, Jan..Dec: 2 = best, 1 = good, 0 = avoid/closed.
- `wiki` = the EXACT title of an existing English Wikipedia article about that thing (used to fetch photos
  with credits). Use "" if none exists. Do not guess.
- `image_query` = 3–6 words that would find a real photo of exactly that subject on Wikimedia Commons
  (e.g. "Ama Dablam from Tengboche", "Boudhanath stupa prayer flags").
- FAQs: real questions travellers search for ("Can I do Everest heli tour with kids?", "Nepal tour package cost
  from India"); answers 40–90 words, answer first, specific.
- Helicopter content: always explain weather dependency (morning flights, clouds by noon), payload rules (fewer
  passengers at altitude, so some tours shuttle or land in two groups), the short time allowed at high landings
  (often 10–15 minutes above 5,000 m) and who should not fly to high altitude (heart/lung conditions, pregnancy).
- Trek content: walking hours per day, height gain, grade, permits (TIMS, national park, restricted area permits,
  licensed-guide rules), acclimatisation days and altitude sickness basics.

## Anchor places (shared slugs)

Packages often cross regions (most start in Kathmandu). Any package may use these slugs in `stops` and `days[].place`,
even if another region owns them. The OWNER region MUST create a place file with exactly this slug.

- kathmandu-valley: `kathmandu`, `bhaktapur`, `patan`, `nagarkot`, `dhulikhel`
- pokhara: `pokhara`, `sarangkot`, `bandipur`, `manakamana`, `gorkha`
- annapurna: `ghorepani`, `ghandruk`, `annapurna-base-camp`, `manang`
- mustang: `jomsom`, `muktinath`, `kagbeni`, `lo-manthang`
- everest: `lukla`, `namche-bazaar`, `tengboche`, `everest-base-camp`, `kala-patthar`
- langtang: `syabrubesi`, `kyanjin-gompa`, `gosaikunda`
- manaslu: `samagaun`
- chitwan: `chitwan-national-park`, `janakpur`
- lumbini: `lumbini`, `tansen`
- east-nepal: `ilam`, `pathibhara`
- far-west: `nepalgunj`, `bardia-national-park`, `rara-lake`, `simikot`
- kailash: `mount-kailash`, `lake-manasarovar`, `lhasa`, `kyirong`

All other places you create are yours alone; reference only your own places, stays and festivals otherwise.

## Files to write for each region `<r>`

### 1. `content/<r>/region.json`
```json
{
  "slug": "everest", "name": "Everest & Khumbu", "short": "Everest",
  "tagline": "≤ 8 words",
  "meta_description": "≤ 158 chars",
  "summary": "40–60 word answer-first summary",
  "intro": ["para (60–110 words)", "para", "para", "para"],
  "facts": [["Best months", "Mar – May · Oct – Nov"], ["Gateway", "Lukla (35 min flight) or Ramechhap"], ["Highest point", "Kala Patthar 5,644 m"], ["Ideal length", "…"], ["Permits", "…"], ["Good for", "…"], ["Altitude range", "2,610 – 5,644 m"]],
  "best_months": [1,1,2,2,2,0,0,0,1,2,2,1],
  "max_altitude_m": 5644,
  "highlights": [{"title": "…", "text": "35–60 words"}],          // exactly 6
  "getting_there": "90–150 words",
  "permits": "60–120 words, or '' if none apply",
  "wiki": "Khumbu",
  "lat": 27.9, "lng": 86.8,
  "months": [                                                      // exactly 12, Jan..Dec
    {"month": "January", "rating": 1, "weather": "Namche −8 to 7 °C, dry, clear mornings", "summary": "60–100 words",
     "go": ["place-slug", "place-slug", "place-slug"], "events": ["festival-slug"], "tip": "one sentence"}
  ],
  "faqs": [{"q": "…", "a": "…"}]                                    // exactly 9
}
```

### 2. `content/<r>/places/<place-slug>.json` (one file per place; count given in your task)
```json
{
  "slug": "namche-bazaar", "name": "Namche Bazaar", "region": "everest",
  "kind": "city | old town | lake town | hill station | viewpoint | trekking village | base camp | lake | pass | national park | temple town | monastery | pilgrimage site | valley | border town | heritage site",
  "wiki": "Namche Bazaar", "image_query": "Namche Bazaar Sherpa village Kongde",
  "lat": 27.805, "lng": 86.713, "altitude_m": 3440,
  "tagline": "≤ 70 chars",
  "meta_description": "≤ 158 chars",
  "summary": "40–60 word answer-first summary",
  "intro": ["para 70–120 words", "para", "para"],
  "facts": [["Altitude", "3,440 m"], ["Best months", "…"], ["Nights we suggest", "2"], ["Nearest airport", "…"], ["From Kathmandu", "≈ 35 min flight to Lukla + 2 days' walk"], ["Known for", "…"]],
  "best_months": [1,1,2,2,2,0,0,0,1,2,2,1],
  "nights": "2",
  "highlights": [{"title": "…", "text": "35–60 words"}],          // 5–6
  "how_to_reach": [{"mode": "Air", "text": "…"}, {"mode": "Road", "text": "…"}, {"mode": "On foot", "text": "…"}],   // 2–4 modes; mode one of Air, Helicopter, Road, On foot, Rail
  "where_to_stay": "70–120 words naming areas and real hotels or lodges",
  "stays": ["stay-slug"],                                         // slugs from your stays.json in this place ([] if none)
  "tips": ["one sentence", "…"],                                   // 5
  "themes": ["trekking", "heli-tours"],                            // from THEMES below
  "nearby": ["place-slug"],                                        // 2–4 other places in YOUR region
  "experiences": [                                                 // exactly 3
    {"slug": "namche-sherpa-culture-museum-walk", "title": "≤ 55 chars",
     "kind": "culture | spiritual | nature | wildlife | adventure | aerial | hiking | food | water | wellness",
     "duration": "2 hours", "best_time": "Morning, Mar–May and Oct–Nov", "price_hint": "Included in most treks | ≈ ₹2,500 per person | ''",
     "image_query": "Sherpa museum Namche", "wiki": "",
     "summary": "35–55 words", "body": ["para 70–120 words", "para", "para"],
     "good_for": ["couples", "families", "first-timers", "photographers", "solo", "seniors", "pilgrims", "groups"],
     "faqs": [{"q": "…", "a": "…"}]}                                // exactly 3
  ],
  "faqs": [{"q": "…", "a": "…"}]                                    // exactly 9
}
```

### 3. `content/<r>/packages/<package-slug>.json` (count and mix given in your task)
```json
{
  "slug": "everest-base-camp-trek-14-days", "title": "≤ 50 chars, include days or nights", "region": "everest",
  "type": "heli | trek | tour | pilgrimage | safari | adventure | climb | yatra",
  "grade": "Easy | Moderate | Challenging | Strenuous",
  "nights": 13, "themes": ["trekking", "photography"],
  "stops": [{"place": "kathmandu", "nights": 2}, {"place": "namche-bazaar", "nights": 2}],   // key catalogue places only (own or anchor); nights need not sum to total
  "start": "Kathmandu (Tribhuvan International Airport)", "end": "Kathmandu",
  "price_from_inr": 125000, "price_from_usd": 1490,
  "best_months": [0,0,2,2,2,0,0,0,1,2,2,0],
  "max_altitude_m": 5644,
  "accommodation": "3-star hotel in Kathmandu, teahouse lodges on the trail",
  "transport": "Kathmandu–Lukla flights, private car transfers",
  "group": "Private or small group, 2–12",
  "meta_description": "≤ 158 chars including 'N days'",
  "summary": "40–60 words", "intro": ["para 70–120 words", "para"],
  "highlights": ["…"],                                                          // 5–6 short lines
  "days": [                                                                     // exactly nights + 1 entries
    {"day": 1, "title": "≤ 45 chars", "place": "kathmandu or '' ", "overnight": "Kathmandu",
     "altitude_m": 1400, "max_m": 1400,                                          // overnight altitude; max_m = highest point that day
     "walk": "≈ 6 h · 11 km or ''", "drive": "≈ 200 km · 7 h or ''", "flight": "Kathmandu–Lukla · 35 min or ''",
     "text": "60–120 words", "meals": "Dinner | Breakfast | B, L, D …"}
  ],
  "stays": ["stay-slug"],                                                       // your own stays only
  "includes": ["…"], "excludes": ["…"],                                         // 7–10 each
  "good_to_know": ["…"],                                                        // 4–6
  "add_ons": [{"name": "Kala Patthar heli return", "price": "≈ US$ 550 per seat"}], // 0–3, optional extras
  "faqs": [{"q": "…", "a": "…"}]                                                // exactly 9
}
```
Rules for packages: `days` = nights + 1 (a one-day heli tour has nights 0 and one day). Every day needs `altitude_m`
and `max_m` (the elevation profile is drawn from them). Heli tours: put flight legs in `flight` with minutes.

### 4. `content/<r>/stays.json` — array (count given in your task)
```json
[{"slug": "hotel-everest-view", "name": "Hotel Everest View", "place": "namche-bazaar",
  "kind": "5-star hotel | 4-star hotel | 3-star hotel | resort | boutique hotel | heritage hotel | mountain lodge | teahouse lodge | jungle lodge | tented camp | monastery guesthouse",
  "class": "Luxury | Premium | Standard",
  "wiki": "Hotel Everest View", "image_query": "Hotel Everest View Syangboche",
  "summary": "35–55 words", "body": ["para 70–110 words", "para"],
  "why": ["one line", "one line", "one line"], "best_for": ["couples", "…"],
  "website": "official URL only if certain, else ''",
  "faqs": [{"q": "…", "a": "…"}]}]                                                // exactly 3
```

### 5. `content/<r>/guides/<guide-slug>.json` (count given in your task)
```json
{"slug": "everest-base-camp-trek-cost", "title": "≤ 60 chars", "region": "everest",
 "category": "planning | costs | seasons | permits | trekking | heli | culture | food | wildlife | practical | packages | pilgrimage",
 "meta_description": "≤ 158 chars", "summary": "40–60 words answer-first",
 "sections": [{"heading": "≤ 50 chars", "paras": ["…"], "list": ["optional"], "table": {"head": ["…"], "rows": [["…"]]}}],
 "related_places": ["place-slug"],
 "faqs": [{"q": "…", "a": "…"}]}                                                 // exactly 9
```
Guides: 1,000–1,500 words of body across 5–8 sections; use a table in at least one section. Write guides people
search for: costs, best time, permits, difficulty, packing, heli vs trek, itineraries compared, food, safety.

### 6. `content/<r>/festivals.json` — array (count given in your task; `[]` allowed only if told)
```json
[{"slug": "mani-rimdu-festival", "name": "Mani Rimdu", "place": "tengboche", "wiki": "Mani Rimdu",
  "image_query": "Mani Rimdu Tengboche mask dance", "when": "Oct–Nov, Tibetan lunar calendar", "month_nums": [10, 11],
  "summary": "35–55 words", "body": ["para 70–110 words", "para", "para"], "tips": ["…", "…", "…"],
  "faqs": [{"q": "…", "a": "…"}]}]                                                // exactly 4
```

### 7. `content/<r>/routes.json` — array (count given in your task): getting between two places
```json
[{"slug": "kathmandu-to-lukla", "from": "kathmandu", "to": "lukla", "distance_km": 136,
  "summary": "35–55 words",
  "options": [{"mode": "Flight", "time": "35 min", "text": "50–90 words"}, {"mode": "Helicopter", "time": "45 min", "text": "…"}, {"mode": "Road + walk", "time": "…", "text": "…"}],
  "stops_on_way": ["…"], "tip": "one sentence",
  "faqs": [{"q": "…", "a": "…"}]}]                                                // exactly 4
```
`from` and `to` must be your own places or anchor places, and at least one must be yours.

## THEMES (use these slugs only)
heli-tours, trekking, cultural-tours, pilgrimage, wildlife-safari, adventure-sports, peak-climbing,
family-holidays, honeymoon, luxury-nepal, budget-nepal, buddhist-circuit, wellness-yoga, short-breaks,
overland-from-india, kailash-yatra, photography, festivals

## Cross-references
Every slug you reference must exist in your own region's files, except anchor places listed above.
Run `python tools/check_region.py <r>` until it prints OK (and `--wiki` once at the end).
