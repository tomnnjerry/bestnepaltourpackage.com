"""Validate one region's content against content/SCHEMA.md.

Usage: python tools/check_region.py <region-slug> [--wiki]
--wiki also confirms every `wiki` title exists on English Wikipedia.
"""
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content"
REGIONS = ["kathmandu-valley", "pokhara", "annapurna", "mustang", "everest", "langtang", "manaslu",
           "chitwan", "lumbini", "east-nepal", "far-west", "kailash"]
THEMES = set("heli-tours trekking cultural-tours pilgrimage wildlife-safari adventure-sports peak-climbing "
             "family-holidays honeymoon luxury-nepal budget-nepal buddhist-circuit wellness-yoga short-breaks "
             "overland-from-india kailash-yatra photography festivals".split())
ANCHORS = {
    "kathmandu-valley": ["kathmandu", "bhaktapur", "patan", "nagarkot", "dhulikhel"],
    "pokhara": ["pokhara", "sarangkot", "bandipur", "manakamana", "gorkha"],
    "annapurna": ["ghorepani", "ghandruk", "annapurna-base-camp", "manang"],
    "mustang": ["jomsom", "muktinath", "kagbeni", "lo-manthang"],
    "everest": ["lukla", "namche-bazaar", "tengboche", "everest-base-camp", "kala-patthar"],
    "langtang": ["syabrubesi", "kyanjin-gompa", "gosaikunda"],
    "manaslu": ["samagaun"],
    "chitwan": ["chitwan-national-park", "janakpur"],
    "lumbini": ["lumbini", "tansen"],
    "east-nepal": ["ilam", "pathibhara"],
    "far-west": ["nepalgunj", "bardia-national-park", "rara-lake", "simikot"],
    "kailash": ["mount-kailash", "lake-manasarovar", "lhasa", "kyirong"],
}
ALL_ANCHORS = {s for v in ANCHORS.values() for s in v}
TYPES = {"heli", "trek", "tour", "pilgrimage", "safari", "adventure", "climb", "yatra"}
GRADES = {"Easy", "Moderate", "Challenging", "Strenuous"}
KINDS = {"culture", "spiritual", "nature", "wildlife", "adventure", "aerial", "hiking", "food", "water", "wellness"}
BANNED = ["nestled", "breathtaking", "hidden gem", "paradise", "tapestry", "embark", "delve", "unleash",
          "vibrant", "bustling", "mesmeriz", "stunning", "magical", "heaven on earth", "feast for the eyes",
          "something for everyone", "whether you're", "look no further", "ultimate guide", "in this blog",
          "in conclusion", "unforgettable", "world-class", "seamless", "curated", "elevate", "immerse", "timeless",
          "boasts", "once-in-a-lifetime", "bucket list", "hassle-free", "award-winning", "no. 1", "!"]
errors, warns = [], []


def err(where, msg):
    errors.append(f"{where}: {msg}")


def load(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except FileNotFoundError:
        err(p, "missing file")
    except Exception as e:  # noqa: BLE001
        err(p, f"invalid JSON ({e})")
    return None


def months(where, v):
    if not (isinstance(v, list) and len(v) == 12 and all(x in (0, 1, 2) for x in v)):
        err(where, "best_months must be 12 ints of 0/1/2")


def faqs(where, v, n):
    if not isinstance(v, list) or len(v) != n:
        err(where, f"needs exactly {n} faqs (has {len(v) if isinstance(v, list) else 0})")
        return
    for f in v:
        if not f.get("q") or not f.get("a"):
            err(where, "faq missing q/a")


def heading(where, t, limit=60):
    if not t:
        return
    if t.rstrip().endswith("."):
        err(where, f"heading ends with full stop: {t!r}")
    if len(t) > limit:
        warns.append(f"{where}: heading longer than {limit} chars: {t!r}")


def scan_banned(where, obj):
    text = json.dumps(obj, ensure_ascii=False).lower()
    for b in BANNED:
        if b in text:
            warns.append(f"{where}: banned word/phrase '{b}'")
    if text.count("iconic") > 1:
        warns.append(f"{where}: 'iconic' used more than once")


def main():
    r = sys.argv[1]
    if r not in REGIONS:
        sys.exit(f"unknown region {r}; use one of {REGIONS}")
    base = ROOT / r
    wiki_titles = []
    reg = load(base / "region.json")
    places, stays, fests = {}, {}, {}
    for p in sorted((base / "places").glob("*.json")):
        d = load(p)
        if d:
            if d.get("slug") != p.stem:
                err(p.name, f"file name must equal slug ({d.get('slug')})")
            places[d["slug"]] = d
    for s in load(base / "stays.json") or []:
        stays[s["slug"]] = s
    for f in load(base / "festivals.json") or []:
        fests[f["slug"]] = f
    for a in ANCHORS[r]:
        if a not in places:
            err("anchors", f"this region must create anchor place '{a}'")
    linkable = set(places) | ALL_ANCHORS

    if reg:
        months("region", reg.get("best_months"))
        faqs("region", reg.get("faqs"), 9)
        if len(reg.get("highlights", [])) != 6:
            err("region", "needs 6 highlights")
        if len(reg.get("months", [])) != 12:
            err("region", "needs 12 months")
        if not reg.get("max_altitude_m"):
            err("region", "needs max_altitude_m")
        for m in reg.get("months", []):
            for g in m.get("go", []):
                if g not in places:
                    err(f"region month {m.get('month')}", f"unknown place '{g}'")
            for e in m.get("events", []):
                if e not in fests:
                    err(f"region month {m.get('month')}", f"unknown festival '{e}'")
        wiki_titles.append(reg.get("wiki"))
        scan_banned("region", reg)

    exp_slugs = set()
    for slug, d in places.items():
        w = f"place {slug}"
        months(w, d.get("best_months"))
        faqs(w, d.get("faqs"), 9)
        heading(w, d.get("tagline"), 70)
        if not isinstance(d.get("altitude_m"), (int, float)):
            err(w, "altitude_m must be a number")
        if not (isinstance(d.get("lat"), (int, float)) and isinstance(d.get("lng"), (int, float))):
            err(w, "lat/lng must be numbers")
        for t in d.get("themes", []):
            if t not in THEMES:
                err(w, f"unknown theme '{t}'")
        for n in d.get("nearby", []):
            if n not in places:
                err(w, f"unknown nearby '{n}'")
        for s in d.get("stays", []):
            if s not in stays:
                err(w, f"unknown stay '{s}'")
        ex = d.get("experiences", [])
        if len(ex) != 3:
            err(w, f"needs 3 experiences (has {len(ex)})")
        for e in ex:
            heading(f"{w} exp", e.get("title"), 55)
            faqs(f"{w} exp {e.get('slug')}", e.get("faqs"), 3)
            if e.get("kind") not in KINDS:
                err(f"{w} exp {e.get('slug')}", f"unknown kind '{e.get('kind')}'")
            if e["slug"] in exp_slugs:
                err(w, f"duplicate experience slug {e['slug']}")
            exp_slugs.add(e["slug"])
            if e.get("wiki"):
                wiki_titles.append(e["wiki"])
        wiki_titles.append(d.get("wiki"))
        scan_banned(w, d)

    pkg_files = sorted((base / "packages").glob("*.json"))
    types = {}
    for p in pkg_files:
        d = load(p)
        if not d:
            continue
        w = f"package {d.get('slug')}"
        if d.get("slug") != p.stem:
            err(w, "file name must equal slug")
        months(w, d.get("best_months"))
        faqs(w, d.get("faqs"), 9)
        heading(w, d.get("title"), 50)
        if d.get("type") not in TYPES:
            err(w, f"unknown type '{d.get('type')}'")
        types[d.get("type")] = types.get(d.get("type"), 0) + 1
        if d.get("grade") not in GRADES:
            err(w, f"unknown grade '{d.get('grade')}'")
        for k in ("price_from_inr", "price_from_usd", "max_altitude_m"):
            if not isinstance(d.get(k), int):
                err(w, f"{k} must be an integer")
        if len(d.get("days", [])) != d.get("nights", -1) + 1:
            err(w, f"days ({len(d.get('days', []))}) must equal nights + 1 ({d.get('nights', 0) + 1})")
        for i, day in enumerate(d.get("days", [])):
            if not isinstance(day.get("altitude_m"), (int, float)) or not isinstance(day.get("max_m"), (int, float)):
                err(w, f"day {i + 1} needs numeric altitude_m and max_m")
            if day.get("place") and day["place"] not in linkable:
                err(w, f"day {i + 1} unknown place '{day['place']}'")
            heading(f"{w} day {i + 1}", day.get("title"), 45)
        peak = max([day.get("max_m") or 0 for day in d.get("days", [])] or [0])
        if isinstance(d.get("max_altitude_m"), int) and peak and abs(peak - d["max_altitude_m"]) > 5:
            warns.append(f"{w}: max_altitude_m {d['max_altitude_m']} differs from highest day max_m {peak}")
        for s in d.get("stops", []):
            if s.get("place") not in linkable:
                err(w, f"unknown stop '{s.get('place')}'")
        for s in d.get("stays", []):
            if s not in stays:
                err(w, f"unknown stay '{s}'")
        for t in d.get("themes", []):
            if t not in THEMES:
                err(w, f"unknown theme '{t}'")
        if len(d.get("faqs", [])) == 9 and len(d.get("includes", [])) < 5:
            warns.append(f"{w}: thin includes list")
        scan_banned(w, d)

    for slug, s in stays.items():
        w = f"stay {slug}"
        faqs(w, s.get("faqs"), 3)
        if s.get("place") not in places:
            err(w, f"unknown place '{s.get('place')}'")
        if s.get("wiki"):
            wiki_titles.append(s["wiki"])
        scan_banned(w, s)

    for p in sorted((base / "guides").glob("*.json")):
        d = load(p)
        if not d:
            continue
        w = f"guide {d.get('slug')}"
        faqs(w, d.get("faqs"), 9)
        heading(w, d.get("title"))
        words = sum(len(" ".join(s.get("paras", []) + s.get("list", [])).split()) for s in d.get("sections", []))
        if words < 900:
            warns.append(f"{w}: only {words} words")
        if not any(s.get("table") for s in d.get("sections", [])):
            warns.append(f"{w}: no table")
        for s in d.get("sections", []):
            heading(w, s.get("heading"), 50)
        for rp in d.get("related_places", []):
            if rp not in linkable:
                err(w, f"unknown related place '{rp}'")
        scan_banned(w, d)

    for slug, f in fests.items():
        w = f"festival {slug}"
        faqs(w, f.get("faqs"), 4)
        if f.get("place") not in linkable:
            err(w, f"unknown place '{f.get('place')}'")
        if f.get("wiki"):
            wiki_titles.append(f["wiki"])
        scan_banned(w, f)

    for rt in load(base / "routes.json") or []:
        w = f"route {rt.get('slug')}"
        faqs(w, rt.get("faqs"), 4)
        for k in ("from", "to"):
            if rt.get(k) not in linkable:
                err(w, f"unknown {k} '{rt.get(k)}'")
        if rt.get("from") not in places and rt.get("to") not in places:
            err(w, "at least one end must be a place of this region")
        scan_banned(w, rt)

    if "--wiki" in sys.argv:
        titles = sorted({t for t in wiki_titles if t})
        for i in range(0, len(titles), 40):
            q = urllib.parse.urlencode({"action": "query", "titles": "|".join(titles[i:i + 40]),
                                        "redirects": 1, "format": "json", "formatversion": 2})
            req = urllib.request.Request("https://en.wikipedia.org/w/api.php?" + q,
                                         headers={"User-Agent": "BestNepalTourPackageBuild/1.0 (content check)"})
            data = json.load(urllib.request.urlopen(req, timeout=30))
            for pg in data["query"]["pages"]:
                if pg.get("missing") or pg.get("invalid"):
                    err("wiki", f"no Wikipedia article titled {pg.get('title')!r} (use '' or fix)")

    counts = (f"places={len(places)} experiences={len(exp_slugs)} stays={len(stays)} festivals={len(fests)} "
              f"packages={len(pkg_files)} {dict(sorted((k or '?', v) for k, v in types.items()))} "
              f"guides={len(list((base / 'guides').glob('*.json')))}")
    print(counts)
    for w in warns:
        print("WARN", w)
    for e in errors:
        print("ERROR", e)
    print("OK" if not errors else f"{len(errors)} errors")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
