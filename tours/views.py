import json
from datetime import date

from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .content import GRADES, KINDS, MONTH_SHORT, MONTHS, TYPES, catalogue, month_bar

COMPANY_FAQS = [
    {"q": "What does Best Nepal Tour Package sell?",
     "a": "Nepal tour packages, helicopter tours, treks, pilgrimages, wildlife safaris, adventure sports, peak climbs and Kailash Mansarovar yatras via Nepal. Every package on the site can be booked as shown or changed: dates, hotels, number of days and the places you visit."},
    {"q": "Are the prices on the site final?",
     "a": "They are indicative 'from' prices per person, twin sharing, in Indian rupees and US dollars. Your final price depends on dates, hotel class, group size and flight or helicopter availability. We send a written quote with every line itemised before you pay anything."},
    {"q": "Do Indian citizens need a passport or visa for Nepal?",
     "a": "Indian citizens do not need a visa. A valid passport or a voter ID card is accepted at the border and at Kathmandu airport; children can travel with a passport or school ID and birth certificate, depending on age. Kailash yatras need a passport. Check current status before you travel."},
    {"q": "How do I book a package?",
     "a": "Send the quote form or message us on WhatsApp. We reply with a written quote, usually within one working day. To confirm, you pay a deposit; the balance is due before departure. Our payment and cancellation policies set out the exact terms."},
    {"q": "Can you arrange a trip from my city in India?",
     "a": "Yes. We plan flights to Kathmandu or Bhairahawa, or road journeys via Sonauli, Raxaul, Rupaidiha, Jogbani and Kakarbhitta. Our 'Nepal tour package from' pages list routes and times for twelve Indian cities."},
    {"q": "Are helicopter tours safe?",
     "a": "Helicopter tours in Nepal are run by licensed operators and fly only when the pilot judges the weather safe, usually early in the morning. Fewer passengers can land at very high points, and time on the ground above 5,000 m is short. Read our helicopter and altitude terms before you book."},
    {"q": "Do I need a guide for treks in Nepal?",
     "a": "Since April 2023 Nepal requires foreign trekkers in national parks and conservation areas to trek with a licensed guide, and restricted areas need a registered agency and at least two trekkers. Indian citizens follow some separate rules. Check current status before you travel."},
    {"q": "Where do your photos come from?",
     "a": "Every photo on this site comes from Wikimedia Commons under a free licence. We name the author and licence under each photo and list them all, with links to the originals, on our photo credits page."},
    {"q": "Is travel insurance included?",
     "a": "No. For treks, heli tours, climbs and Kailash yatras we require insurance that covers helicopter evacuation up to the highest altitude on your route. For city and safari tours we strongly recommend it."},
]


def ld(*items):
    return [json.dumps(i, ensure_ascii=False).replace("</", "<\\/") for i in items if i]


def crumbs(*pairs):
    items = [("Home", reverse("home"))] + list(pairs)
    data = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": settings.SITE["url"] + u}
        for i, (n, u) in enumerate(items)]}
    return items, data


def faq_ld(faqs):
    if not faqs:
        return None
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faqs]}


def img_url(obj):
    imgs = obj.get("images") or []
    return imgs[0]["thumb"] if imgs else None


def org_ld():
    s = settings.SITE
    return {"@context": "https://schema.org", "@type": "TravelAgency", "name": s["name"], "url": s["url"],
            "areaServed": ["Nepal", "Tibet"], "address": {"@type": "PostalAddress", "addressLocality": "Kathmandu", "addressCountry": "NP"}}


def _get(store, slug):
    obj = store.get(slug)
    if not obj:
        raise Http404
    return obj


def _month_now():
    return date.today().month - 1


def _mid(pkgs, n=1):
    pkgs = sorted(pkgs, key=lambda k: k.get("price_from_inr", 0))
    return pkgs[len(pkgs) // 2: len(pkgs) // 2 + n] if pkgs else []


# ---------------- home and indexes ----------------
def home(request):
    cat = catalogue()
    regions = list(cat.regions.values())
    pk = list(cat.packages.values())
    heli = sorted([k for k in pk if k.get("type") == "heli"], key=lambda k: k.get("price_from_inr", 0))
    treks = [k for k in pk if k.get("type") in ("trek", "climb")]
    picks = []
    for t in ("tour", "heli", "trek", "pilgrimage", "safari", "yatra", "adventure", "climb"):
        for k in _mid([x for x in pk if x.get("type") == t], 1):
            picks.append(k)
    classics = [k for k in cat.regions.get("kathmandu-valley", {}).get("packages", []) if k.get("type") == "tour"][:4]
    m = _month_now()
    in_season = [p for p in cat.places.values() if (p.get("best_months") or [0] * 12)[m] == 2]
    in_season = in_season[::max(1, len(in_season) // 8)][:8]
    fests = [f for f in cat.festivals.values() if (m + 1) in f.get("month_nums", []) or ((m + 1) % 12 + 1) in f.get("month_nums", [])][:4]
    ladder = []  # the altitude ladder in the hero: one real place per band, low to high
    for slug in ("chitwan-national-park", "pokhara", "kathmandu", "namche-bazaar", "muktinath", "gosaikunda",
                 "everest-base-camp", "kala-patthar"):
        p = cat.places.get(slug)
        if p:
            ladder.append(p)
    trek_points = [{"t": k["title"], "u": k["url"], "d": k["days_count"], "a": k.get("max_altitude_m", 0),
                    "g": k.get("grade"), "r": k["region_obj"]["short"] if k["region_obj"].get("short") else k["region_obj"]["name"],
                    "p": k.get("price_from_usd"), "c": k["region_obj"]["accent"]} for k in treks]
    return render(request, "tours/home.html", {
        "regions": regions, "heli": heli[:6], "picks": picks[:8], "classics": classics, "month": MONTHS[m], "month_i": m,
        "in_season": in_season, "festivals": fests, "guides": list(cat.guides.values())[::9][:4],
        "themes": list(cat.themes.values()), "months_full": MONTHS, "ladder": ladder,
        "posts": list(cat.posts.values())[:3], "origins": list(cat.origins.values()),
        "trek_points": json.dumps(trek_points).replace("</", "<\\/"), "types": TYPES,
        "faqs": COMPANY_FAQS[:6],
        "ld": ld(org_ld(), {"@context": "https://schema.org", "@type": "WebSite", "name": settings.SITE["name"], "url": settings.SITE["url"],
                            "potentialAction": {"@type": "SearchAction", "target": settings.SITE["url"] + "/packages/?q={q}", "query-input": "required name=q"}},
                 faq_ld(COMPANY_FAQS[:6])),
    })


def regions(request):
    cat = catalogue()
    items, bc = crumbs(("Destinations", reverse("regions")))
    return render(request, "tours/regions.html", {"regions": list(cat.regions.values()), "crumbs": items,
                                                  "months_short": MONTH_SHORT, "ld": ld(bc)})


def region(request, region):
    cat = catalogue()
    r = _get(cat.regions, region)
    items, bc = crumbs(("Destinations", reverse("regions")), (r["name"], r["url"]))
    styles = [cat.themes[t] for (rr, t) in cat.region_theme_pairs() if rr == region]
    months = [{"name": MONTHS[i], "slug": MONTHS[i].lower(), "rating": (r.get("best_months") or [0] * 12)[i],
               "weather": (r.get("months") or [{}] * 12)[i].get("weather", "") if i < len(r.get("months", [])) else ""}
              for i in range(12)]
    by_type = [(TYPES[t], [k for k in r["packages"] if k.get("type") == t]) for t in r["types"]]
    dest = {"@context": "https://schema.org", "@type": "TouristDestination", "name": r["name"],
            "description": r.get("summary"), "url": settings.SITE["url"] + r["url"],
            "includesAttraction": [{"@type": "TouristAttraction", "name": p["name"]} for p in r["places"]]}
    return render(request, "tours/region.html", {
        "r": r, "crumbs": items, "styles": styles, "months": months, "by_type": by_type,
        "kinds": [(k, KINDS[k][0]) for rr, k in cat.region_kind_pairs() if rr == region],
        "map_points": json.dumps([{"name": p["name"], "lat": p.get("lat"), "lng": p.get("lng"), "url": p["url"], "alt": p.get("altitude_m")}
                                  for p in sorted(r["places"], key=lambda p: p.get("altitude_m") or 0) if p.get("lat")]),
        "ld": ld(bc, dest, faq_ld(r.get("faqs", []))),
    })


def region_month(request, region, month):
    cat = catalogue()
    r = _get(cat.regions, region)
    names = [m.lower() for m in MONTHS]
    if month not in names:
        raise Http404
    i = names.index(month)
    md = r.get("months", [])[i] if i < len(r.get("months", [])) else {}
    go = [cat.places[s] for s in md.get("go", []) if s in cat.places]
    events = [cat.festivals[s] for s in md.get("events", []) if s in cat.festivals]
    pkgs = [k for k in r["packages"] if (k.get("best_months") or [0] * 12)[i] >= 1]
    pkgs.sort(key=lambda k: -(k.get("best_months") or [0] * 12)[i])
    rating = (r.get("best_months") or [0] * 12)[i]
    others = [{"r": rr, "rating": (rr.get("best_months") or [0] * 12)[i]} for rr in cat.regions.values() if rr["slug"] != region]
    items, bc = crumbs(("Destinations", reverse("regions")), (r["name"], r["url"]), (MONTHS[i], request.path))
    title = f"{r['name']} in {MONTHS[i]}"
    faqs = [
        {"q": f"Is {MONTHS[i]} a good time to visit {r['name']}?",
         "a": (md.get("summary") or "")[:600] or f"See our month-by-month notes for {r['name']}."},
        {"q": f"What is the weather like in {r['name']} in {MONTHS[i]}?",
         "a": f"{md.get('weather', 'Weather varies with altitude')}. Conditions change fast with altitude, so check the mountain forecast a few days before you travel."},
        {"q": f"Which {r['name']} packages work in {MONTHS[i]}?",
         "a": ("Good choices this month: " + ", ".join(k["title"] for k in pkgs[:4]) + ". " if pkgs else "Few of our packages run this month. ") + (md.get("tip") or "")},
    ]
    return render(request, "tours/region_month.html", {
        "r": r, "i": i, "month": MONTHS[i], "md": md, "go": go, "events": events, "packages": pkgs[:9],
        "rating": rating, "others": others, "crumbs": items, "title": title, "faqs": faqs,
        "prev": names[(i - 1) % 12], "next": names[(i + 1) % 12], "prev_name": MONTHS[(i - 1) % 12], "next_name": MONTHS[(i + 1) % 12],
        "ld": ld(bc, faq_ld(faqs)),
    })


def region_theme(request, region, theme):
    cat = catalogue()
    r = _get(cat.regions, region)
    t = _get(cat.themes, theme)
    if (region, theme) not in cat.region_theme_pairs():
        raise Http404
    data = cat.theme_items(theme, region)
    items, bc = crumbs(("Destinations", reverse("regions")), (r["name"], r["url"]), (t.get("short") or t["name"], request.path))
    return render(request, "tours/region_theme.html", {"r": r, "t": t, **data, "crumbs": items, "ld": ld(bc)})


def place(request, region, place):
    cat = catalogue()
    p = _get(cat.places, place)
    if p["region"] != region:
        return redirect(p["url"], permanent=True)
    r = p["region_obj"]
    items, bc = crumbs(("Destinations", reverse("regions")), (r["name"], r["url"]), (p["name"], p["url"]))
    dest = {"@context": "https://schema.org", "@type": "TouristDestination", "name": p["name"],
            "description": p.get("summary"), "url": settings.SITE["url"] + p["url"], "image": img_url(p)}
    if p.get("lat"):
        dest["geo"] = {"@type": "GeoCoordinates", "latitude": p["lat"], "longitude": p["lng"], "elevation": p.get("altitude_m")}
    return render(request, "tours/place.html", {
        "p": p, "r": r, "crumbs": items, "ld": ld(bc, dest, faq_ld(p.get("faqs", []))),
        "map_points": json.dumps([{"name": x["name"], "lat": x.get("lat"), "lng": x.get("lng"), "url": x["url"], "main": x is p, "alt": x.get("altitude_m")}
                                  for x in [p] + p["nearby_objs"] if x.get("lat")]),
    })


def experience(request, region, place, exp):
    cat = catalogue()
    e = _get(cat.experiences, exp)
    p = e["place_obj"]
    if p["slug"] != place or e["region"] != region:
        return redirect(e["url"], permanent=True)
    r = e["region_obj"]
    siblings = [x for x in p.get("experiences", []) if x is not e]
    more = [x for x in cat.experiences.values() if x.get("kind") == e.get("kind") and x["region"] == r["slug"] and x["place"] != p["slug"]][:3]
    items, bc = crumbs(("Destinations", reverse("regions")), (r["name"], r["url"]), (p["name"], p["url"]), (e["title"], e["url"]))
    attraction = {"@context": "https://schema.org", "@type": "TouristAttraction", "name": e["title"],
                  "description": e.get("summary"), "image": img_url(e), "containedInPlace": {"@type": "Place", "name": p["name"]}}
    return render(request, "tours/experience.html", {
        "e": e, "p": p, "r": r, "siblings": siblings, "more": more, "crumbs": items,
        "ld": ld(bc, attraction, faq_ld(e.get("faqs", []))),
    })


SORTS = {"recommended": "Recommended", "price": "Price, low to high", "price-desc": "Price, high to low",
         "days": "Shortest first", "altitude": "Highest first"}


def packages(request):
    cat = catalogue()
    pk = list(cat.packages.values())
    g = request.GET
    f = {"type": g.get("type", ""), "region": g.get("region", ""), "grade": g.get("grade", ""), "month": g.get("month", ""),
         "days": g.get("days", ""), "budget": g.get("budget", ""), "q": g.get("q", "").strip()[:80], "sort": g.get("sort", "recommended")}
    if f["type"] in TYPES:
        pk = [k for k in pk if k.get("type") == f["type"]]
    if f["region"] in cat.regions:
        pk = [k for k in pk if k["region"] == f["region"] or any(p["region"] == f["region"] for p in k["route_places"])]
    if f["grade"] in GRADES:
        pk = [k for k in pk if k.get("grade") == f["grade"]]
    if f["month"] in [m.lower() for m in MONTHS]:
        mi = [m.lower() for m in MONTHS].index(f["month"])
        pk = [k for k in pk if (k.get("best_months") or [0] * 12)[mi] >= 1]
    ranges = {"1-3": (1, 3), "4-7": (4, 7), "8-12": (8, 12), "13-30": (13, 60)}
    if f["days"] in ranges:
        lo, hi = ranges[f["days"]]
        pk = [k for k in pk if lo <= k["days_count"] <= hi]
    budgets = {"under-30k": (0, 30000), "30k-75k": (30000, 75000), "75k-150k": (75000, 150000), "150k-plus": (150000, 10 ** 9)}
    if f["budget"] in budgets:
        lo, hi = budgets[f["budget"]]
        pk = [k for k in pk if lo <= (k.get("price_from_inr") or 0) < hi]
    if f["q"]:
        q = f["q"].lower()
        pk = [k for k in pk if q in (k["title"] + " " + k.get("summary", "") + " " + k["region_obj"]["name"]).lower()]
    order = {"price": lambda k: k.get("price_from_inr", 0), "price-desc": lambda k: -k.get("price_from_inr", 0),
             "days": lambda k: k["days_count"], "altitude": lambda k: -k.get("max_altitude_m", 0)}
    if f["sort"] in order:
        pk.sort(key=order[f["sort"]])
    else:
        rank = {t: i for i, t in enumerate(TYPES)}
        pk.sort(key=lambda k: (rank.get(k.get("type"), 9), k.get("price_from_inr", 0)))
    t = TYPES.get(f["type"])
    title = f"{t['plural']} in Nepal" if t else "Nepal tour packages"
    if f["region"] in cat.regions:
        title += f" · {cat.regions[f['region']]['name']}"
    items, bc = crumbs(("Packages", reverse("packages")))
    filtered = any(v for k, v in f.items() if k != "sort" and v)
    return render(request, "tours/packages.html", {
        "packages": pk, "f": f, "filtered": filtered, "title": title, "types": TYPES, "grades": GRADES,
        "regions": list(cat.regions.values()), "months": MONTHS, "sorts": SORTS, "crumbs": items,
        "ld": ld(bc, {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": settings.SITE["url"] + k["url"], "name": k["title"]} for i, k in enumerate(pk[:30])]}),
    })


def package(request, slug):
    cat = catalogue()
    k = _get(cat.packages, slug)
    r = k["region_obj"]
    items, bc = crumbs(("Packages", reverse("packages")), (k["type_obj"]["plural"], f"{reverse('packages')}?type={k.get('type')}"), (k["title"], k["url"]))
    trip = {"@context": "https://schema.org", "@type": "TouristTrip", "name": k["title"], "description": k.get("summary"),
            "image": img_url(k), "touristType": [cat.themes[t]["name"] for t in k.get("themes", []) if t in cat.themes],
            "itinerary": {"@type": "ItemList", "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "item": {"@type": "Place", "name": p["name"]}} for i, p in enumerate(k["route_places"])]},
            "offers": [{"@type": "Offer", "priceCurrency": "INR", "price": k.get("price_from_inr"), "description": "Indicative price per person, twin sharing"},
                       {"@type": "Offer", "priceCurrency": "USD", "price": k.get("price_from_usd"), "description": "Indicative price per person, twin sharing"}]}
    same_type = [x for x in cat.packages.values() if x is not k and x.get("type") == k.get("type")]
    related = [x for x in r["packages"] if x is not k][:3]
    if len(related) < 3:
        related += [x for x in same_type if x not in related][: 3 - len(related)]
    alternatives = sorted([x for x in same_type if x not in related], key=lambda x: abs(x["days_count"] - k["days_count"]))[:3]
    pts = [{"name": p["name"], "lat": p.get("lat"), "lng": p.get("lng"), "url": p["url"], "alt": p.get("altitude_m")}
           for p in k["route_places"] if p.get("lat")]
    return render(request, "tours/package.html", {
        "k": k, "r": r, "crumbs": items, "related": related, "alternatives": alternatives,
        "map_points": json.dumps(pts), "guides": [g for g in r["guides"]][:3],
        "ld": ld(bc, trip, faq_ld(k.get("faqs", []))),
    })


def stays(request):
    cat = catalogue()
    items, bc = crumbs(("Hotels", reverse("stays")))
    return render(request, "tours/stays.html", {"regions": [r for r in cat.regions.values() if r["stays"]], "crumbs": items, "ld": ld(bc)})


def stay(request, slug):
    cat = catalogue()
    s = _get(cat.stays, slug)
    items, bc = crumbs(("Hotels", reverse("stays")), (s["name"], s["url"]))
    hotel = {"@context": "https://schema.org", "@type": "Hotel", "name": s["name"], "description": s.get("summary"),
             "image": img_url(s), "address": {"@type": "PostalAddress", "addressLocality": (s.get("place_obj") or {}).get("name", ""), "addressCountry": "NP"}}
    if s.get("website"):
        hotel["sameAs"] = s["website"]
    others = [x for x in s["region_obj"]["stays"] if x is not s][:3]
    return render(request, "tours/stay.html", {"s": s, "crumbs": items, "others": others,
                                               "ld": ld(bc, hotel, faq_ld(s.get("faqs", [])))})


def experiences(request):
    cat = catalogue()
    items, bc = crumbs(("Things to do", reverse("experiences")))
    return render(request, "tours/experiences.html", {"regions": list(cat.regions.values()),
                                                      "kind_links": [(k, v[0], v[1]) for k, v in KINDS.items()],
                                                      "crumbs": items, "ld": ld(bc)})


def _kind_page(request, kind, region=None):
    cat = catalogue()
    if kind not in KINDS:
        raise Http404
    name, tagline, intro = KINDS[kind]
    exps = [e for e in cat.experiences.values() if e.get("kind") == kind and (region is None or e["region"] == region)]
    r = cat.regions.get(region) if region else None
    if region and (not r or (region, kind) not in cat.region_kind_pairs()):
        raise Http404
    if not exps:
        raise Http404
    trail = [("Things to do", reverse("experiences"))]
    if r:
        trail = [("Destinations", reverse("regions")), (r["name"], r["url"]), (name, request.path)]
    else:
        trail.append((name, request.path))
    items, bc = crumbs(*trail)
    lands = [cat.regions[rr] for rr, k in cat.region_kind_pairs() if k == kind]
    others = [(k, v[0]) for k, v in KINDS.items() if k != kind and (region is None or (region, k) in cat.region_kind_pairs())]
    return render(request, "tours/experience_kind.html", {
        "kind": kind, "name": name, "tagline": tagline, "intro": intro, "exps": exps, "r": r,
        "lands": lands, "others": others, "crumbs": items, "ld": ld(bc)})


def experience_kind(request, kind):
    return _kind_page(request, kind)


def region_kind(request, region, kind):
    return _kind_page(request, kind, region)


def guides(request):
    cat = catalogue()
    items, bc = crumbs(("Travel guides", reverse("guides")))
    return render(request, "tours/guides.html", {"regions": [r for r in cat.regions.values() if r["guides"]], "crumbs": items, "ld": ld(bc)})


def guide(request, slug):
    cat = catalogue()
    g = _get(cat.guides, slug)
    r = g["region_obj"]
    items, bc = crumbs(("Travel guides", reverse("guides")), (g["title"], g["url"]))
    article = {"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g.get("summary"),
               "image": img_url(g), "author": {"@type": "Organization", "name": settings.SITE["byline"]},
               "publisher": {"@type": "Organization", "name": settings.SITE["name"]}}
    more = [x for x in r["guides"] if x is not g][:3]
    pkgs = _mid(r["packages"], 3)
    return render(request, "tours/guide.html", {"g": g, "r": r, "crumbs": items, "more": more, "packages": pkgs,
                                                "ld": ld(bc, article, faq_ld(g.get("faqs", [])))})


def festivals(request):
    cat = catalogue()
    items, bc = crumbs(("Festivals", reverse("festivals")))
    by_month = [{"name": m, "festivals": [f for f in cat.festivals.values() if (i + 1) in f.get("month_nums", [])]} for i, m in enumerate(MONTHS)]
    return render(request, "tours/festivals.html", {"by_month": by_month, "crumbs": items, "ld": ld(bc)})


def festival(request, slug):
    cat = catalogue()
    f = _get(cat.festivals, slug)
    items, bc = crumbs(("Festivals", reverse("festivals")), (f["name"], f["url"]))
    pkgs = [k for k in f["region_obj"]["packages"] if "festivals" in k.get("themes", [])][:3] or _mid(f["region_obj"]["packages"], 3)
    return render(request, "tours/festival.html", {"f": f, "crumbs": items, "packages": pkgs,
                                                   "bar": month_bar([2 if (i + 1) in f.get("month_nums", []) else 0 for i in range(12)]),
                                                   "ld": ld(bc, faq_ld(f.get("faqs", [])))})


def routes(request):
    cat = catalogue()
    items, bc = crumbs(("Getting around", reverse("routes")))
    return render(request, "tours/routes.html", {"regions": [r for r in cat.regions.values() if r["routes"]], "crumbs": items, "ld": ld(bc)})


def route(request, slug):
    cat = catalogue()
    rt = _get(cat.routes, slug)
    items, bc = crumbs(("Getting around", reverse("routes")), (f"{rt['from_obj']['name']} to {rt['to_obj']['name']}", rt["url"]))
    pts = [x for x in (rt["from_obj"], rt["to_obj"]) if x and x.get("lat")]
    pkgs = [k for k in cat.packages.values() if rt["from_obj"] in k["route_places"] and rt["to_obj"] in k["route_places"]][:3]
    return render(request, "tours/route.html", {"rt": rt, "crumbs": items, "packages": pkgs, "ld": ld(bc, faq_ld(rt.get("faqs", []))),
                                                "map_points": json.dumps([{"name": x["name"], "lat": x["lat"], "lng": x["lng"], "url": x["url"], "alt": x.get("altitude_m")} for x in pts])})


def themes(request):
    cat = catalogue()
    items, bc = crumbs(("Tour styles", reverse("themes")))
    return render(request, "tours/themes.html", {"themes": list(cat.themes.values()), "origins": list(cat.origins.values()),
                                                 "crumbs": items, "ld": ld(bc)})


def theme_or_origin(request, slug):
    cat = catalogue()
    if slug in cat.themes:
        return _theme(request, cat, cat.themes[slug])
    if slug in cat.origins:
        return _origin(request, cat, cat.origins[slug])
    raise Http404


def _theme(request, cat, t):
    data = cat.theme_items(t["slug"])
    pairs = [cat.regions[r] for (r, tt) in cat.region_theme_pairs() if tt == t["slug"]]
    items, bc = crumbs(("Tour styles", reverse("themes")), (t.get("short") or t["name"], t["url"]))
    tpl = {"heli-tours": "tours/theme_heli.html", "trekking": "tours/theme_trek.html"}.get(t["slug"], "tours/theme.html")
    pk = data["packages"]
    pk.sort(key=lambda k: k.get("price_from_inr", 0))
    trek_points = [{"t": k["title"], "u": k["url"], "d": k["days_count"], "a": k.get("max_altitude_m", 0), "g": k.get("grade"),
                    "r": k["region_obj"].get("short") or k["region_obj"]["name"], "p": k.get("price_from_usd"), "c": k["region_obj"]["accent"]}
                   for k in pk] if t["slug"] in ("trekking", "peak-climbing") else []
    return render(request, tpl, {"t": t, **data, "region_pages": pairs, "crumbs": items, "grades": GRADES,
                                 "trek_points": json.dumps(trek_points).replace("</", "<\\/"),
                                 "ld": ld(bc, faq_ld(t.get("faqs", [])))})


def _origin(request, cat, o):
    regs = o["region_objs"] or list(cat.regions.values())[:3]
    pkgs = []
    for r in regs:
        pkgs += _mid([k for k in r["packages"] if k.get("type") in ("tour", "pilgrimage", "safari")], 2) or _mid(r["packages"], 2)
    heli = sorted([k for k in cat.packages.values() if k.get("type") == "heli"], key=lambda k: k.get("price_from_inr", 0))[:3]
    overland = [k for k in cat.packages.values() if "overland-from-india" in k.get("themes", [])][:3]
    items, bc = crumbs(("From India", reverse("origins")), (o["city"], o["url"]))
    others = [x for x in cat.origins.values() if x is not o]
    return render(request, "tours/origin.html", {"o": o, "regions_list": regs, "packages": pkgs[:6], "heli": heli, "overland": overland,
                                                 "others": others, "crumbs": items, "ld": ld(bc, faq_ld(o.get("faqs", [])))})


def origins(request):
    cat = catalogue()
    items, bc = crumbs(("From India", reverse("origins")))
    return render(request, "tours/origins.html", {"origins": list(cat.origins.values()), "crumbs": items,
                                                  "overland": [k for k in cat.packages.values() if "overland-from-india" in k.get("themes", [])],
                                                  "ld": ld(bc)})


def seasons(request):
    cat = catalogue()
    items, bc = crumbs(("Best time to visit Nepal", reverse("seasons")))
    m = _month_now()
    return render(request, "tours/seasons.html", {"regions": list(cat.regions.values()), "months": MONTHS, "now": m,
                                                  "months_short": MONTH_SHORT, "crumbs": items, "ld": ld(bc)})


# ---------------- tools ----------------
def tools(request):
    items, bc = crumbs(("Trip tools", reverse("tools")))
    return render(request, "tours/tools.html", {"crumbs": items, "ld": ld(bc)})


def tool_season(request):
    cat = catalogue()
    items, bc = crumbs(("Trip tools", reverse("tools")), ("Season finder", reverse("tool_season")))
    data = [{"n": p["name"], "u": p["url"], "r": p["region_obj"]["name"], "rs": p["region"], "b": p.get("best_months") or [0] * 12,
             "k": p.get("kind", ""), "a": p.get("altitude_m"), "i": (p["images"][0]["thumb"] if p["images"] else "")} for p in cat.places.values()]
    return render(request, "tours/tool_season.html", {"crumbs": items, "data": json.dumps(data).replace("</", "<\\/"), "months": MONTHS,
                                                      "regions": list(cat.regions.values()), "now": _month_now(), "ld": ld(bc)})


def tool_budget(request):
    items, bc = crumbs(("Trip tools", reverse("tools")), ("Budget calculator", reverse("tool_budget")))
    return render(request, "tours/tool_budget.html", {"crumbs": items, "ld": ld(bc), "regions": list(catalogue().regions.values())})


def tool_altitude(request):
    cat = catalogue()
    items, bc = crumbs(("Trip tools", reverse("tools")), ("Altitude checker", reverse("tool_altitude")))
    pk = [k for k in cat.packages.values() if k.get("max_altitude_m", 0) >= 2500]
    pk.sort(key=lambda k: -k.get("max_altitude_m", 0))
    data = {k["slug"]: {"t": k["title"], "u": k["url"], "days": [[d.get("day"), d.get("overnight", ""), d.get("altitude_m") or 0, d.get("max_m") or 0]
                                                                   for d in k.get("days", [])]} for k in pk}
    chosen = cat.packages.get(request.GET.get("package")) or (pk[0] if pk else None)
    return render(request, "tours/tool_altitude.html", {"crumbs": items, "packages": pk, "chosen": chosen,
                                                        "data": json.dumps(data).replace("</", "<\\/"), "ld": ld(bc)})


def tool_permits(request):
    cat = catalogue()
    items, bc = crumbs(("Trip tools", reverse("tools")), ("Permit finder", reverse("tool_permits")))
    return render(request, "tours/tool_permits.html", {"crumbs": items, "regions": list(cat.regions.values()), "ld": ld(bc)})


# ---------------- static and utility ----------------
def faq(request):
    cat = catalogue()
    items, bc = crumbs(("FAQ", reverse("faq")))
    groups = [{"name": "Booking with us", "faqs": COMPANY_FAQS}] + [
        {"name": r["name"], "faqs": r.get("faqs", []), "url": r["url"], "slug": r["slug"]} for r in cat.regions.values()]
    return render(request, "tours/faq.html", {"groups": groups, "crumbs": items, "ld": ld(bc, faq_ld(COMPANY_FAQS))})


def about(request):
    items, bc = crumbs(("About us", reverse("about")))
    return render(request, "tours/about.html", {"crumbs": items, "regions": list(catalogue().regions.values()), "ld": ld(bc, org_ld())})


def photo_credits(request):
    cat = catalogue()
    items, bc = crumbs(("Photo credits", reverse("photo_credits")))
    return render(request, "tours/photo_credits.html", {"images": cat.all_images(), "crumbs": items, "ld": ld(bc)})


def html_sitemap(request):
    cat = catalogue()
    items, bc = crumbs(("Sitemap", reverse("html_sitemap")))
    return render(request, "tours/sitemap.html", {
        "cat": cat, "regions": list(cat.regions.values()), "crumbs": items,
        "pairs": [(cat.regions[r], cat.themes[t]) for r, t in cat.region_theme_pairs()],
        "kind_pairs": [(cat.regions[r], k, KINDS[k][0]) for r, k in cat.region_kind_pairs()],
        "month_slugs": [(m, m.lower()) for m in MONTHS], "ld": ld(bc)})


def design_system(request):
    cat = catalogue()
    items, bc = crumbs(("Design system", reverse("design_system")))
    from .icons import ICONS
    sample = next(iter(cat.packages.values()), None)
    heli = next((k for k in cat.packages.values() if k.get("type") == "heli"), sample)
    return render(request, "tours/design_system.html", {"crumbs": items, "regions": list(cat.regions.values()),
                                                        "icons": sorted(ICONS), "sample": sample, "heli": heli, "types": TYPES,
                                                        "ld": ld(bc)})


def robots(request):
    body = (f"User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /plan/thank-you/\nDisallow: /design-system/\n\n"
            f"Sitemap: {settings.SITE['url']}/sitemap.xml\n")
    return HttpResponse(body, content_type="text/plain")


def llms(request):
    cat = catalogue()
    u = settings.SITE["url"]
    lines = [f"# {settings.SITE['name']}", "",
             "> Nepal tour packages, helicopter tours, treks, pilgrimages, safaris and Kailash Mansarovar yatras via Nepal, "
             "with indicative prices in INR and USD.", ""]
    for t in cat.themes.values():
        lines.append(f"- [{t['name']}]({u}{t['url']}): {t.get('summary', '')}")
    lines.append("")
    for r in cat.regions.values():
        lines.append(f"## {r['name']}")
        lines.append(f"- [{r['name']} overview]({u}{r['url']}): {r.get('summary', '')}")
        for k in r["packages"]:
            lines.append(f"- [{k['title']}]({u}{k['url']}): from ₹{k.get('inr')} / US${k.get('price_from_usd')} · {k['days_count']} days · {k.get('summary', '')}")
        for p in r["places"]:
            lines.append(f"- [{p['name']}]({u}{p['url']}): {p.get('summary', '')}")
        lines.append("")
    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")


def not_found(request, exception=None):
    return render(request, "tours/404.html", {"crumbs": [], "packages": _mid(list(catalogue().packages.values()), 3)}, status=404)
