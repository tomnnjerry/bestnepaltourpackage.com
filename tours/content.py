"""In-memory catalogue built from content/*.json.

Every page on the site is rendered from this catalogue. In DEBUG the catalogue
reloads when any content file changes, so writers see edits on refresh.
"""
import json
import re
from collections import OrderedDict
from pathlib import Path

from django.conf import settings
from django.urls import reverse

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
MONTH_SHORT = [m[:3] for m in MONTHS]
REGION_ORDER = ["kathmandu-valley", "pokhara", "annapurna", "mustang", "everest", "langtang", "manaslu",
                "chitwan", "lumbini", "east-nepal", "far-west", "kailash"]

# Each region wears the colours it is known for.
# ground = dark sections, accent = highlights on dark, ink = accent text on light, tint = light wash
# grad = 3-stop dark ground gradient, foil = metallic accent (light → mid → deep)
LANDS = {
    "kathmandu-valley": {"palette": "Durbar brick and temple gold", "icon": "pagoda",
                         "ground": "#4A1712", "accent": "#F0B54A", "ink": "#97560B", "tint": "#F8EBDD",
                         "grad": ("#2A0B07", "#5E1D14", "#8C301C"), "foil": ("#FFE8A6", "#F0B54A", "#C47E14")},
    "pokhara": {"palette": "Phewa teal and paraglider orange", "icon": "paraglider",
                "ground": "#08404A", "accent": "#FF8F4A", "ink": "#B44A0E", "tint": "#E0F0F1",
                "grad": ("#03262E", "#0A4D59", "#13707A"), "foil": ("#FFD3B0", "#FF8F4A", "#DB5A16")},
    "annapurna": {"palette": "Rhododendron red and fir green", "icon": "rhododendron",
                  "ground": "#15301F", "accent": "#FF6B7F", "ink": "#B5213A", "tint": "#E5EFE6",
                  "grad": ("#0A1C11", "#1A3D27", "#2A5C3A"), "foil": ("#FFD0D7", "#FF6B7F", "#D13350")},
    "mustang": {"palette": "Canyon rust and Lo ochre", "icon": "chorten",
                "ground": "#5B2410", "accent": "#F6C453", "ink": "#8C5A00", "tint": "#F8E9DC",
                "grad": ("#381406", "#6E2C12", "#A04618"), "foil": ("#FFF0B0", "#F6C453", "#C8901A")},
    "everest": {"palette": "Glacier blue and summit ice", "icon": "summit",
                "ground": "#0B2244", "accent": "#8FD3FF", "ink": "#145DA0", "tint": "#E4EEF9",
                "grad": ("#061633", "#0F2F5E", "#1D4E8F"), "foil": ("#FFFFFF", "#A9DEFF", "#5AA6E0")},
    "langtang": {"palette": "Gosaikunda turquoise and Tamang red", "icon": "lake",
                 "ground": "#0B3437", "accent": "#4FE0C8", "ink": "#09695C", "tint": "#DFF2EF",
                 "grad": ("#04201F", "#0C4043", "#156460"), "foil": ("#D2FFF6", "#4FE0C8", "#16A891")},
    "manaslu": {"palette": "Slate ridge and prayer-flag yellow", "icon": "flags",
                "ground": "#262A3B", "accent": "#F7D046", "ink": "#806400", "tint": "#ECEDF3",
                "grad": ("#141725", "#2A2F45", "#424A6A"), "foil": ("#FFF4B8", "#F7D046", "#C9A10E")},
    "chitwan": {"palette": "Sal forest and grassland gold", "icon": "rhino",
                "ground": "#1F2F14", "accent": "#C9E265", "ink": "#5C7310", "tint": "#EAF0DC",
                "grad": ("#111B0A", "#24391A", "#385728"), "foil": ("#F2FFC4", "#C9E265", "#8FAE22")},
    "lumbini": {"palette": "Lotus plum and monk saffron", "icon": "lotus",
                "ground": "#4A1838", "accent": "#FFB547", "ink": "#9A5800", "tint": "#F6E7EF",
                "grad": ("#2C0A21", "#5A1D45", "#84306A"), "foil": ("#FFE6B2", "#FFB547", "#D77F0F")},
    "east-nepal": {"palette": "Ilam tea green and Kanchenjunga dawn", "icon": "tea",
                   "ground": "#0F3D34", "accent": "#FFB38A", "ink": "#A0451A", "tint": "#E0F0EB",
                   "grad": ("#06231D", "#104638", "#1B6A54"), "foil": ("#FFE2D2", "#FFB38A", "#E07848")},
    "far-west": {"palette": "Rara sapphire and Karnali jade", "icon": "boat",
                 "ground": "#102A5E", "accent": "#7FE3B0", "ink": "#16784A", "tint": "#E3EAF7",
                 "grad": ("#081A40", "#14347A", "#2452AA"), "foil": ("#D8FFEA", "#7FE3B0", "#2FAF74")},
    "kailash": {"palette": "Mansarovar lapis and pilgrim saffron", "icon": "kailash",
                "ground": "#1B1A4A", "accent": "#FF9F43", "ink": "#964B00", "tint": "#E9E8F6",
                "grad": ("#0D0C2C", "#231F5F", "#3B2F8C"), "foil": ("#FFDDB5", "#FF9F43", "#DB6A0B")},
}

# Package types: label, plural, icon, the style page that lists them, and a short promise
TYPES = OrderedDict([
    ("heli", {"label": "Heli tour", "plural": "Heli tours", "icon": "heli", "theme": "heli-tours", "verb": "Fly"}),
    ("trek", {"label": "Trek", "plural": "Treks", "icon": "boot", "theme": "trekking", "verb": "Walk"}),
    ("tour", {"label": "Tour", "plural": "Tours", "icon": "pagoda", "theme": "cultural-tours", "verb": "See"}),
    ("pilgrimage", {"label": "Pilgrimage", "plural": "Pilgrimages", "icon": "bell", "theme": "pilgrimage", "verb": "Pray"}),
    ("safari", {"label": "Safari", "plural": "Safaris", "icon": "rhino", "theme": "wildlife-safari", "verb": "Spot"}),
    ("adventure", {"label": "Adventure", "plural": "Adventures", "icon": "paraglider", "theme": "adventure-sports", "verb": "Jump"}),
    ("climb", {"label": "Peak climb", "plural": "Peak climbs", "icon": "axe", "theme": "peak-climbing", "verb": "Climb"}),
    ("yatra", {"label": "Kailash yatra", "plural": "Kailash yatras", "icon": "kailash", "theme": "kailash-yatra", "verb": "Circle"}),
])
GRADES = ["Easy", "Moderate", "Challenging", "Strenuous"]

KINDS = OrderedDict([
    ("culture", ("Culture", "Durbar squares, old towns and living crafts", "Guided walks through palaces, temples and workshops, told by people who grew up with them.")),
    ("spiritual", ("Temples and monasteries", "Pashupati, Muktinath, Boudha and the gompas", "Darshan, puja and monastery visits at the right hour, with guides who explain the rituals.")),
    ("nature", ("Nature and views", "Lakes, viewpoints and valleys", "Sunrise points, lakeshores and forest walks timed for clear skies.")),
    ("wildlife", ("Wildlife", "Rhino, tiger, birds and red panda", "Jeep drives, canoe trips and guided walks in Nepal's national parks.")),
    ("adventure", ("Adventure", "Paragliding, rafting, bungee and zipline", "Licensed operators, clear weight and age rules, and honest prices.")),
    ("aerial", ("Scenic flights", "Helicopters, mountain flights and ultralights", "Morning flights over the Himalaya with landing rules explained up front.")),
    ("hiking", ("Day hikes", "Viewpoints and acclimatisation walks", "Half-day and full-day walks graded by hours and height gain.")),
    ("food", ("Food", "Momo, Newari feasts and Thakali dal bhat", "Kitchens, markets and the dishes each region is known for.")),
    ("water", ("On the water", "Phewa, Rara, Begnas and the Rapti", "Boats, canoes and lakeshore time at the best light.")),
    ("wellness", ("Wellness", "Yoga, meditation and hot springs", "Retreats and quiet days with qualified teachers.")),
])

_cache = {"stamp": None, "cat": None}


def _read(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def _stamp(root):
    return max((p.stat().st_mtime for p in root.rglob("*.json")), default=0)


def catalogue():
    root = Path(settings.CONTENT_DIR)
    if _cache["cat"] is None or settings.DEBUG:
        stamp = _stamp(root)
        if stamp != _cache["stamp"]:
            _cache["cat"] = Catalogue(root)
            _cache["stamp"] = stamp
    return _cache["cat"]


def month_bar(best):
    best = best or [0] * 12
    return [{"m": MONTH_SHORT[i], "full": MONTHS[i], "v": best[i] if i < len(best) else 0} for i in range(12)]


def best_range(best):
    """'Oct – Mar' style label from a 12-int array (rating 2 = best)."""
    if not best:
        return ""
    good = {i for i, v in enumerate(best) if v == 2} or {i for i, v in enumerate(best) if v >= 1}
    if not good:
        return ""
    if len(good) == 12:
        return "All year"
    runs = []
    for i in range(12):
        if i in good and (i - 1) % 12 not in good:
            run, j = [i], (i + 1) % 12
            while j in good:
                run.append(j)
                j = (j + 1) % 12
            runs.append(run)
    return " · ".join(MONTH_SHORT[r[0]] if len(r) == 1 else f"{MONTH_SHORT[r[0]]} – {MONTH_SHORT[r[-1]]}" for r in runs)


def inr(n):
    """Indian digit grouping: 125000 -> '1,25,000'."""
    try:
        n = int(n)
    except (TypeError, ValueError):
        return ""
    s = str(abs(n))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        head = re.sub(r"(\d)(?=(\d\d)+$)", r"\1,", head)
        s = f"{head},{tail}"
    return ("-" if n < 0 else "") + s


def code_for(pkg):
    """Short pass code printed on package tickets, e.g. EBC-14D."""
    words = [w for w in re.split(r"[-\s]+", pkg["slug"]) if w and not w.isdigit() and w not in
             ("days", "day", "nights", "night", "n", "d", "tour", "trek", "package", "and", "the", "with", "via", "from", "of", "to", "by")]
    letters = "".join(w[0] for w in words[:3]).upper() or "NP"
    return f"{letters}-{pkg.get('nights', 0) + 1}D"


def acclimatisation(days):
    """Flags days where sleeping altitude rises > 500 m above 3,000 m (the usual rule of thumb)."""
    flags = []
    prev = None
    for d in days:
        alt = d.get("altitude_m") or 0
        if prev is not None and alt > 3000 and alt - prev > 500:
            flags.append(d.get("day"))
        prev = alt
    return flags


class Catalogue:
    def __init__(self, root):
        self.root = root
        tf = root / "themes.json"
        self.themes = OrderedDict((t["slug"], t) for t in (_read(tf) if tf.exists() else []))
        of = root / "origins.json"
        self.origins = OrderedDict((o["slug"], o) for o in (_read(of) if of.exists() else []))
        img_file = root / "images.json"
        self.images = _read(img_file) if img_file.exists() else {}
        block_file = root / "image_blocklist.json"  # Commons file titles we never show (portraits, wrong subject)
        blocked = set(_read(block_file)) if block_file.exists() else set()
        if blocked:
            self.images = {k: [r for r in v if r["file"] not in blocked] for k, v in self.images.items()}
        self.regions = OrderedDict()
        self.places = OrderedDict()
        self.experiences = OrderedDict()
        self.packages = OrderedDict()
        self.stays = OrderedDict()
        self.guides = OrderedDict()
        self.festivals = OrderedDict()
        self.routes = OrderedDict()
        for slug in REGION_ORDER:
            base = root / slug
            if (base / "region.json").exists():
                try:
                    self._load_region(slug, base)
                except (ValueError, KeyError):  # a writer is mid-edit; skip the region until it parses
                    self.regions.pop(slug, None)
        self.posts = OrderedDict()
        for p in (root / "journal").glob("*.json") if (root / "journal").exists() else []:
            try:
                d = _read(p)
            except ValueError:
                continue
            d["url"] = reverse("post", args=[d["slug"]])
            self.posts[d["slug"]] = d
        self.posts = OrderedDict(sorted(self.posts.items(), key=lambda kv: kv[1].get("date", ""), reverse=True))
        self._link()
        self._link_posts()

    # ---------- loading ----------
    def _load_region(self, slug, base):
        r = _read(base / "region.json")
        r["slug"] = slug
        r.update(LANDS[slug])
        r["url"] = reverse("region", args=[slug])
        r["places"], r["packages"], r["stays"], r["guides"], r["festivals"], r["routes"] = [], [], [], [], [], []
        self.regions[slug] = r
        for p in sorted((base / "places").glob("*.json")):
            d = _read(p)
            d["region"] = slug
            d["url"] = reverse("place", args=[slug, d["slug"]])
            self.places[d["slug"]] = d
            r["places"].append(d)
            for e in d.get("experiences", []):
                e["place"] = d["slug"]
                e["region"] = slug
                e["url"] = reverse("experience", args=[slug, d["slug"], e["slug"]])
                self.experiences[e["slug"]] = e
        for p in sorted((base / "packages").glob("*.json")):
            d = _read(p)
            d["region"] = slug
            d["url"] = reverse("package", args=[d["slug"]])
            self.packages[d["slug"]] = d
            r["packages"].append(d)
        for name, store, key, view in (("stays.json", self.stays, "stays", "stay"),
                                       ("festivals.json", self.festivals, "festivals", "festival"),
                                       ("routes.json", self.routes, "routes", "route")):
            f = base / name
            for d in (_read(f) if f.exists() else []):
                d["region"] = slug
                d["url"] = reverse(view, args=[d["slug"]])
                store[d["slug"]] = d
                r[key].append(d)
        for p in sorted((base / "guides").glob("*.json")):
            d = _read(p)
            d["region"] = slug
            d["url"] = reverse("guide", args=[d["slug"]])
            self.guides[d["slug"]] = d
            r["guides"].append(d)

    def _imgs(self, *keys):
        for k in keys:
            if self.images.get(k):
                return self.images[k]
        return []

    def _link(self):
        for slug in [s for s, rt in self.routes.items() if rt.get("from") not in self.places or rt.get("to") not in self.places]:
            dead = self.routes.pop(slug)
            self.regions[dead["region"]]["routes"].remove(dead)
        for p in self.places.values():
            p["region_obj"] = self.regions[p["region"]]
            p["images"] = self._imgs(f"place:{p['slug']}")
            p["best_label"] = best_range(p.get("best_months"))
            p["bar"] = month_bar(p.get("best_months"))
            p["nearby_objs"] = [self.places[s] for s in p.get("nearby", []) if s in self.places]
            p["stay_objs"] = [self.stays[s] for s in p.get("stays", []) if s in self.stays]
            p["package_objs"] = [k for k in self.packages.values()
                                 if any(s.get("place") == p["slug"] for s in k.get("stops", []))
                                 or any(d.get("place") == p["slug"] for d in k.get("days", []))]
            p["festival_objs"] = [f for f in self.festivals.values() if f.get("place") == p["slug"]]
            p["route_objs"] = [rt for rt in self.routes.values() if p["slug"] in (rt.get("from"), rt.get("to"))]
        for r in self.regions.values():
            r["top_places"] = sorted(r["places"], key=lambda p: (-len(p["package_objs"]), p["name"]))
            r["images"] = self._imgs(f"region:{r['slug']}") or [
                i for p in r["top_places"][:6] for i in p["images"][:1]]
            r["best_label"] = best_range(r.get("best_months"))
            r["bar"] = month_bar(r.get("best_months"))
            prices = [k.get("price_from_inr") for k in r["packages"] if k.get("price_from_inr")]
            r["price_from_inr"] = min(prices) if prices else None
            usd = [k.get("price_from_usd") for k in r["packages"] if k.get("price_from_usd")]
            r["price_from_usd"] = min(usd) if usd else None
            r["types"] = [t for t in TYPES if any(k.get("type") == t for k in r["packages"])]
        for e in self.experiences.values():
            place = self.places[e["place"]]
            e["place_obj"] = place
            e["region_obj"] = place["region_obj"]
            e["images"] = self._imgs(f"exp:{e['slug']}") or place["images"][1:] or place["images"]
            e["themes"] = place.get("themes", [])
            e["kind_name"] = KINDS.get(e.get("kind"), (e.get("kind", "").title(),))[0]
        for s in self.stays.values():
            place = self.places.get(s.get("place"))
            s["place_obj"] = place
            s["region_obj"] = self.regions[s["region"]]
            s["images"] = self._imgs(f"stay:{s['slug']}") or (place["images"] if place else [])
            s["package_objs"] = [k for k in self.packages.values() if s["slug"] in k.get("stays", [])]
        for k in self.packages.values():
            k["region_obj"] = self.regions[k["region"]]
            stops = [dict(st, obj=self.places[st["place"]]) for st in k.get("stops", []) if st.get("place") in self.places]
            k["stop_objs"] = stops
            day_places = []
            for d in k.get("days", []):
                d["place_obj"] = self.places.get(d.get("place"))
                if d["place_obj"] and d["place_obj"] not in day_places:
                    day_places.append(d["place_obj"])
            k["route_places"] = day_places or [s["obj"] for s in stops]
            # Hero photo: mountain trips lead with their highest stop; other trips skip the arrival city
            if k.get("type") in ("trek", "heli", "climb", "yatra"):
                photo_order = sorted(k["route_places"], key=lambda p: -(p.get("altitude_m") or 0))
            else:
                photo_order = k["route_places"][1:] + k["route_places"][:1]
            k["images"] = self._imgs(f"pkg:{k['slug']}") or [
                i for p in photo_order for i in p["images"][:1]] or k["region_obj"]["images"]
            k["stay_objs"] = [self.stays[s] for s in k.get("stays", []) if s in self.stays]
            k["best_label"] = best_range(k.get("best_months"))
            k["bar"] = month_bar(k.get("best_months"))
            k["days_count"] = k.get("nights", 0) + 1
            k["type_obj"] = TYPES.get(k.get("type"), TYPES["tour"])
            k["code"] = code_for(k)
            k["inr"] = inr(k.get("price_from_inr"))
            k["acclim_flags"] = acclimatisation(k.get("days", []))
            k["walk_days"] = sum(1 for d in k.get("days", []) if d.get("walk"))
            k["flight_legs"] = [d["flight"] for d in k.get("days", []) if d.get("flight")]
            k["alts"] = [[d.get("altitude_m") or 0, d.get("max_m") or d.get("altitude_m") or 0] for d in k.get("days", [])]
        for g in self.guides.values():
            g["region_obj"] = self.regions[g["region"]]
            rel = [self.places[s] for s in g.get("related_places", []) if s in self.places]
            g["related_objs"] = rel
            g["images"] = self._imgs(f"guide:{g['slug']}") or [i for p in rel for i in p["images"][:1]] or g["region_obj"]["images"]
            words = sum(len(" ".join(s.get("paras", []) + s.get("list", [])).split()) for s in g.get("sections", []))
            g["read_min"] = max(3, round(words / 220))
            for s in g.get("sections", []):
                s["anchor"] = re.sub(r"[^a-z0-9]+", "-", s.get("heading", "").lower()).strip("-")
        for f in self.festivals.values():
            place = self.places.get(f.get("place"))
            f["place_obj"] = place
            f["region_obj"] = self.regions[f["region"]]
            f["images"] = self._imgs(f"fest:{f['slug']}") or (place["images"] if place else [])
        for rt in self.routes.values():
            rt["from_obj"] = self.places.get(rt.get("from"))
            rt["to_obj"] = self.places.get(rt.get("to"))
            rt["region_obj"] = self.regions[rt["region"]]
            rt["images"] = (rt["to_obj"] or {}).get("images", []) + (rt["from_obj"] or {}).get("images", [])[:1]
        for t in self.themes.values():
            t["url"] = reverse("theme", args=[t["slug"]])
            t["type"] = next((k for k, v in TYPES.items() if v["theme"] == t["slug"]), None)
            t["icon"] = TYPES[t["type"]]["icon"] if t["type"] else THEME_ICONS.get(t["slug"], "compass")
            items = self.theme_items(t["slug"])
            t["images"] = self._imgs(f"theme:{t['slug']}") or [
                i for k in items["packages"][:6] for i in k["images"][:1]]
            prices = [k["price_from_inr"] for k in items["packages"] if k.get("price_from_inr")]
            t["price_from_inr"] = min(prices) if prices else None
        for o in self.origins.values():
            o["url"] = reverse("theme", args=[o["slug"]])
            o["region_objs"] = [self.regions[r] for r in o.get("regions", []) if r in self.regions]

    def _link_posts(self):
        from datetime import date
        stores = {"package": self.packages, "place": self.places, "stay": self.stays, "guide": self.guides,
                  "festival": self.festivals}
        for d in self.posts.values():
            d["region_objs"] = [self.regions[r] for r in d.get("regions", []) if r in self.regions]
            d["package_objs"] = [self.packages[j] for j in d.get("related_packages", []) if j in self.packages]
            d["place_objs"] = [self.places[x] for x in d.get("related_places", []) if x in self.places]
            d["images"] = (self._imgs(f"blog:{d['slug']}") or [i for x in d["place_objs"] for i in x["images"][:1]]
                           or [i for x in d["package_objs"] for i in x["images"][:1]])
            words = sum(len(" ".join(s.get("paras", []) + s.get("list", [])).split()) for s in d.get("sections", []))
            d["read_min"] = max(3, round(words / 220))
            d["cat_slug"] = re.sub(r"[^a-z0-9]+", "-", d.get("category", "").lower()).strip("-")
            try:
                d["date_obj"] = date.fromisoformat(d.get("date", ""))
            except ValueError:
                d["date_obj"] = None
            d["land"] = d["region_objs"][0]["slug"] if d["region_objs"] else None
            for sec in d.get("sections", []):
                sec["anchor"] = re.sub(r"[^a-z0-9]+", "-", sec.get("heading", "").lower()).strip("-")
                objs = []
                for ln in sec.get("links", []):
                    o = stores.get(ln.get("type"), {}).get(ln.get("slug"))
                    if o:
                        objs.append({"type": ln["type"], "title": o.get("title") or o.get("name"), "url": o["url"],
                                     "img": (o.get("images") or [None])[0], "obj": o})
                sec["link_objs"] = objs
        self.post_categories = OrderedDict()
        for d in self.posts.values():
            self.post_categories.setdefault(d["cat_slug"], {"slug": d["cat_slug"], "name": d.get("category"), "posts": []})["posts"].append(d)

    # ---------- queries ----------
    def theme_items(self, theme, region=None):
        def ok(x):
            return region is None or x.get("region") == region
        ttype = next((k for k, v in TYPES.items() if v["theme"] == theme), None)
        packages = [k for k in self.packages.values() if ok(k) and (theme in k.get("themes", []) or (ttype and k.get("type") == ttype))]
        places = [p for p in self.places.values() if theme in p.get("themes", []) and ok(p)]
        place_slugs = {p["slug"] for p in places}
        stays = [s for s in self.stays.values() if s.get("place") in place_slugs and ok(s)]
        experiences = [e for e in self.experiences.values() if e["place"] in place_slugs and ok(e)]
        return {"packages": packages, "places": places, "stays": stays, "experiences": experiences}

    def region_theme_pairs(self):
        """(region, theme) pairs with enough content to deserve a page."""
        out = []
        for r in self.regions:
            for t in self.themes:
                items = self.theme_items(t, r)
                if len(items["packages"]) >= 2 or (items["packages"] and len(items["places"]) >= 3):
                    out.append((r, t))
        return out

    def region_kind_pairs(self):
        out = []
        for r in self.regions:
            for k in KINDS:
                if sum(1 for e in self.experiences.values() if e["region"] == r and e.get("kind") == k) >= 3:
                    out.append((r, k))
        return out

    def counts(self):
        return {"regions": len(self.regions), "places": len(self.places), "experiences": len(self.experiences),
                "packages": len(self.packages), "stays": len(self.stays), "guides": len(self.guides),
                "festivals": len(self.festivals), "routes": len(self.routes), "themes": len(self.themes),
                "posts": len(self.posts), "origins": len(self.origins)}

    def all_images(self):
        seen, out = set(), []
        for key, recs in self.images.items():
            for rec in recs:
                if rec["file"] not in seen:
                    seen.add(rec["file"])
                    out.append(dict(rec, used_for=key))
        return out


THEME_ICONS = {
    "family-holidays": "family", "honeymoon": "heart", "luxury-nepal": "crown", "budget-nepal": "coin",
    "buddhist-circuit": "lotus", "wellness-yoga": "yoga", "short-breaks": "clock", "overland-from-india": "road",
    "photography": "camera", "festivals": "lamp",
}
