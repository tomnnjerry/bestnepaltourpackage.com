"""Self-drawn SVG maps and elevation profiles. No map API, no tiles, no third-party requests.

Outlines come from content/outlines.json (Natural Earth, public domain, Nepal's point of view
for international borders). Colours come from CSS classes, so each map takes on its region's palette.
"""
import json
import math
from functools import lru_cache
from pathlib import Path

from django.conf import settings
from django.utils.html import escape

# The eight 8,000 m peaks wholly or partly in Nepal (height in metres, lat, lng)
PEAKS = [
    ("Everest", 8849, 27.988, 86.925), ("Kangchenjunga", 8586, 27.703, 88.147), ("Lhotse", 8516, 27.962, 86.933),
    ("Makalu", 8485, 27.889, 87.089), ("Cho Oyu", 8188, 28.094, 86.661), ("Dhaulagiri", 8167, 28.697, 83.487),
    ("Manaslu", 8163, 28.549, 84.560), ("Annapurna", 8091, 28.596, 83.820),
]
CAPTION = ("Drawn from Natural Earth outlines (public domain). International borders follow Nepal's official map. "
           "Not for navigation.")


@lru_cache(maxsize=1)
def _outlines():
    p = Path(settings.CONTENT_DIR) / "outlines.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"countries": {}}


def _nice(n):
    for v in (5, 10, 20, 25, 50, 100, 200, 250, 500):
        if v >= n:
            return v
    return 1000


class _Frame:
    """Equirectangular projection fitted to a set of points."""

    def __init__(self, lats, lngs, min_span=1.6, pad_k=0.25, W=1000, max_aspect=2.1):
        lat_c = (min(lats) + max(lats)) / 2
        self.k = k = math.cos(math.radians(lat_c))
        x0, x1 = min(lngs) * k, max(lngs) * k
        y0, y1 = min(lats), max(lats)
        span = max(x1 - x0, y1 - y0, min_span)
        pad = span * pad_k
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        w = max(x1 - x0 + 2 * pad, min_span)
        h = max(y1 - y0 + 2 * pad, min_span * 0.55)
        if w / h < 1.3:
            w = h * 1.3
        elif w / h > max_aspect:
            h = w / max_aspect
        self.bx0, self.bx1, self.by0, self.by1 = cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2
        self.W = W
        self.H = round(W * h / w)
        self.s = W / w
        self.w, self.h = w, h

    def P(self, lng, lat):
        return (lng * self.k - self.bx0) * self.s, (self.by1 - lat) * self.s

    def visible(self, ring):
        xs = [x * self.k for x, _ in ring]
        ys = [y for _, y in ring]
        return not (max(xs) < self.bx0 or min(xs) > self.bx1 or max(ys) < self.by0 or min(ys) > self.by1)

    def path(self, rings):
        parts = []
        for ring in rings:
            if not self.visible(ring):
                continue
            parts.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in (self.P(a, b) for a, b in ring)) + "Z")
        return "".join(parts)


def _base(fr, title):
    out = _outlines()
    svg = [f'<svg class="atlas__svg" viewBox="0 0 {fr.W} {fr.H}" role="img" aria-label="{escape(title)}" xmlns="http://www.w3.org/2000/svg">',
           f'<title>{escape(title)}</title>',
           f'<rect class="atlas__sea" width="{fr.W}" height="{fr.H}"/>']
    step = 0.5 if fr.w / fr.k < 3 else (1 if fr.w / fr.k < 8 else 2)
    lng = math.floor(fr.bx0 / fr.k / step) * step
    while lng * fr.k <= fr.bx1:
        x = (lng * fr.k - fr.bx0) * fr.s
        svg.append(f'<line class="atlas__grat" x1="{x:.1f}" y1="0" x2="{x:.1f}" y2="{fr.H}"/>')
        lng += step
    lat = math.floor(fr.by0 / step) * step
    while lat <= fr.by1:
        y = (fr.by1 - lat) * fr.s
        svg.append(f'<line class="atlas__grat" x1="0" y1="{y:.1f}" x2="{fr.W}" y2="{y:.1f}"/>')
        lat += step
    for name, rings in out["countries"].items():
        d = fr.path(rings)
        if d:
            cls = "atlas__land atlas__land--home" if name == "Nepal" else "atlas__land"
            svg.append(f'<path class="{cls}" d="{d}"><title>{escape(name)}</title></path>')
    for name, h, la, ln in PEAKS:
        x, y = fr.P(ln, la)
        if 0 < x < fr.W and 0 < y < fr.H:
            svg.append(f'<g class="atlas__peak"><path d="M{x - 7:.1f},{y + 5:.1f}L{x:.1f},{y - 7:.1f}L{x + 7:.1f},{y + 5:.1f}Z"/>'
                       f'<title>{name} {h:,} m</title></g>')
    return svg


def _scale(fr):
    km_per_unit = 111.2
    km = _nice((fr.W * 0.16) / fr.s * km_per_unit)
    bar = km / km_per_unit * fr.s
    return (f'<g class="atlas__scale" transform="translate(24,{fr.H - 26})"><line x1="0" y1="0" x2="{bar:.1f}" y2="0"/>'
            f'<line x1="0" y1="-6" x2="0" y2="6"/><line x1="{bar:.1f}" y1="-6" x2="{bar:.1f}" y2="6"/>'
            f'<text x="{bar / 2:.1f}" y="-10" text-anchor="middle">{km} km</text></g>'
            f'<g class="atlas__north" transform="translate({fr.W - 36},40)"><path d="M0,-20 L8,7 L0,2 L-8,7 Z"/>'
            f'<text y="24" text-anchor="middle">N</text></g>')


def atlas_svg(points, route=False, min_span=1.4, legend=True, label_limit=10, title=None):
    if isinstance(points, str):
        points = json.loads(points or "[]")
    pts = [p for p in points if p.get("lat") is not None and p.get("lng") is not None]
    if not pts:
        return ""
    fr = _Frame([p["lat"] for p in pts], [p["lng"] for p in pts], min_span=min_span)
    svg = _base(fr, title or "Map of " + ", ".join(p["name"] for p in pts[:10]))
    proj = [fr.P(p["lng"], p["lat"]) for p in pts]
    if route and len(proj) > 1:
        svg.append('<polyline class="atlas__route" points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in proj) + '"/>')
    # nudge overlapping pins apart
    proj = [list(xy) for xy in proj]
    for _ in range(40):
        moved = False
        for a in range(len(proj)):
            for b in range(a + 1, len(proj)):
                dx, dy = proj[b][0] - proj[a][0], proj[b][1] - proj[a][1]
                dist = math.hypot(dx, dy)
                if dist < 32:
                    if dist < 0.01:
                        dx, dy, dist = 1.0, 0.0, 1.0
                    push = (32 - dist) / 2
                    ux, uy = dx / dist, dy / dist
                    proj[a][0] -= ux * push
                    proj[a][1] -= uy * push
                    proj[b][0] += ux * push
                    proj[b][1] += uy * push
                    moved = True
        if not moved:
            break
    proj = [(min(max(x, 18), fr.W - 18), min(max(y, 18), fr.H - 18)) for x, y in proj]
    show_labels = len(pts) <= label_limit
    for i, ((x, y), p) in enumerate(zip(proj, pts), 1):
        main = " is-main" if p.get("main") else ""
        label = escape(p["name"])
        alt = f' · {p["alt"]:,} m' if p.get("alt") else ""
        svg.append(f'<a href="{escape(p.get("url", "#"))}" class="atlas__pin{main}" data-n="{i}"><title>{label}{alt}</title>')
        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="14"/><text x="{x:.1f}" y="{y + 5:.1f}" text-anchor="middle">{i}</text>')
        if show_labels:
            right = x < fr.W - 220
            tx = x + 21 if right else x - 21
            svg.append(f'<text class="atlas__label" x="{tx:.1f}" y="{y + 5:.1f}" text-anchor="{"start" if right else "end"}">{label}</text>')
        svg.append("</a>")
    svg.append(_scale(fr))
    svg.append("</svg>")
    html = ['<figure class="atlas">', "".join(svg)]
    if legend:
        html.append('<ol class="atlas__legend">' + "".join(
            f'<li><a href="{escape(p.get("url", "#"))}"><span>{i}</span>{escape(p["name"])}'
            + (f' <small>{p["alt"]:,} m</small>' if p.get("alt") else "")
            + (f' <small>{p["nights"]} night{"s" if p["nights"] != 1 else ""}</small>' if p.get("nights") else "")
            + "</a></li>" for i, p in enumerate(pts, 1)) + "</ol>")
    html.append(f"<figcaption>{CAPTION}</figcaption></figure>")
    return "".join(html)


def nepal_svg(regions, active=None):
    """Country map with one marker per region, coloured by the region's palette."""
    pts = [r for r in regions if r.get("lat") is not None]
    if not pts:
        return ""
    lats = [26.35, 30.45] + [r["lat"] for r in pts if r["slug"] != "kailash"]
    lngs = [80.05, 88.2] + [r["lng"] for r in pts if r["slug"] != "kailash"]
    fr = _Frame(lats, lngs, min_span=4, pad_k=0.04, max_aspect=2.3)
    svg = _base(fr, "Map of Nepal's travel regions")
    for r in pts:
        lat, lng = r["lat"], r["lng"]
        if r["slug"] == "kailash":  # Kailash sits beyond the north-west border: pin it on the frame edge
            lat, lng = min(lat, fr.by1 - 0.25), max(lng, fr.bx0 / fr.k + 0.4)
        x, y = fr.P(lng, lat)
        on = " is-on" if r["slug"] == active else ""
        svg.append(f'<a href="{escape(r["url"])}" class="nmap__pin{on}" data-land="{r["slug"]}" data-region="{r["slug"]}">'
                   f'<title>{escape(r["name"])}</title><circle class="nmap__halo" cx="{x:.1f}" cy="{y:.1f}" r="26"/>'
                   f'<circle class="nmap__dot" cx="{x:.1f}" cy="{y:.1f}" r="9"/>'
                   f'<text class="nmap__label" x="{x:.1f}" y="{y + 30:.1f}" text-anchor="middle">{escape(r.get("short") or r["name"])}</text></a>')
    svg.append(_scale(fr))
    svg.append("</svg>")
    return f'<figure class="atlas atlas--nepal">{"".join(svg)}<figcaption>{CAPTION}</figcaption></figure>'


# ---------------- elevation profiles ----------------
def profile_svg(days, flags=(), W=1000, H=300):
    """Day-by-day elevation profile: sleeping altitude as an area, the day's high point as a tick."""
    rows = [(d.get("altitude_m") or 0, d.get("max_m") or d.get("altitude_m") or 0, d) for d in days]
    if not rows:
        return ""
    top = max(m for _, m, _ in rows)
    ceil = max(2000, math.ceil((top + 300) / 1000) * 1000)
    L, R, T, B = 58, 18, 22, 44
    pw, ph = W - L - R, H - T - B
    n = len(rows)

    def X(i):
        return L + (pw * (i / (n - 1)) if n > 1 else pw / 2)

    def Y(a):
        return T + ph - ph * a / ceil

    out = [f'<svg class="prof__svg" viewBox="0 0 {W} {H}" role="img" aria-label="Elevation profile, highest point {top:,} m" xmlns="http://www.w3.org/2000/svg">']
    for zone, lo, cls in (("Altitude zone", 2500, "prof__zone"), ("Very high", 5000, "prof__zone prof__zone--hi")):
        if ceil > lo:
            out.append(f'<rect class="{cls}" x="{L}" y="{T}" width="{pw}" height="{Y(lo) - T:.1f}"><title>{zone}: above {lo:,} m</title></rect>')
    step = 1000 if ceil <= 6000 else 2000
    for a in range(0, ceil + 1, step):
        out.append(f'<line class="prof__grid" x1="{L}" x2="{W - R}" y1="{Y(a):.1f}" y2="{Y(a):.1f}"/>'
                   f'<text class="prof__y" x="{L - 8}" y="{Y(a) + 4:.1f}" text-anchor="end">{a:,}</text>')
    pts = [(X(i), Y(s)) for i, (s, _, _) in enumerate(rows)]
    area = f"M{X(0):.1f},{Y(0):.1f}L" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f"L{X(n - 1):.1f},{Y(0):.1f}Z"
    out.append(f'<path class="prof__area" d="{area}"/>')
    out.append('<polyline class="prof__line" points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '"/>')
    every = 1 if n <= 16 else (2 if n <= 30 else 3)
    for i, (s, m, d) in enumerate(rows):
        x = X(i)
        name = escape(d.get("overnight") or d.get("title") or "")
        if m > s + 60:
            out.append(f'<line class="prof__tick" x1="{x:.1f}" x2="{x:.1f}" y1="{Y(s):.1f}" y2="{Y(m):.1f}"/>'
                       f'<circle class="prof__peak" cx="{x:.1f}" cy="{Y(m):.1f}" r="4"><title>Day {d.get("day", i + 1)} high point {m:,} m</title></circle>')
        flag = " prof__dot--flag" if d.get("day") in flags else ""
        out.append(f'<circle class="prof__dot{flag}" cx="{x:.1f}" cy="{Y(s):.1f}" r="5"><title>Day {d.get("day", i + 1)} · {name} · {s:,} m</title></circle>')
        if i % every == 0 or i == n - 1:
            out.append(f'<text class="prof__x" x="{x:.1f}" y="{H - B + 20}" text-anchor="middle">{d.get("day", i + 1)}</text>')
    tx = X([m for _, m, _ in rows].index(top))
    out.append(f'<text class="prof__top" x="{min(max(tx, L + 60), W - R - 60):.1f}" y="{Y(top) - 12:.1f}" text-anchor="middle">{top:,} m</text>')
    out.append(f'<text class="prof__axis" x="{L}" y="{H - 6}">Day</text>')
    out.append("</svg>")
    return "".join(out)


def spark_svg(alts, W=132, H=36):
    """Tiny profile for cards: [[sleep, max], ...]."""
    if not alts:
        return ""
    vals = [max(a) for a in alts]
    top = max(vals) or 1
    n = len(vals)
    pts = [(2 + (W - 4) * (i / (n - 1) if n > 1 else .5), H - 3 - (H - 8) * v / top) for i, v in enumerate(vals)]
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = f"M{pts[0][0]:.1f},{H}L" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f"L{pts[-1][0]:.1f},{H}Z"
    return (f'<svg class="spark" viewBox="0 0 {W} {H}" aria-hidden="true"><path class="spark__area" d="{area}"/>'
            f'<polyline class="spark__line" points="{line}"/></svg>')
