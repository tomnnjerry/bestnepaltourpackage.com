"""Build content/outlines.json for the self-drawn SVG maps (no map API, no tiles).

Source (public domain, Natural Earth, https://www.naturalearthdata.com):
- ne_10m_admin_0_countries_nep: country outlines as seen from Nepal's point of view, so Nepal's
  border follows its official map (including Kalapani, Lipulekh and Limpiyadhura).

Usage: python tools/build_outlines.py   (downloads the file into .cache/ on first run)
"""
import json
import math
import sys
import urllib.request
from pathlib import Path

sys.setrecursionlimit(100000)
ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".cache"
BASE = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/"
FILE = "ne_10m_admin_0_countries_nep.geojson"
COUNTRIES = ["Nepal", "India", "China", "Bhutan", "Bangladesh"]
BOX = (76, 23, 95, 34)  # lng/lat window we ever draw


def fetch(name):
    CACHE.mkdir(exist_ok=True)
    p = CACHE / name
    if not p.exists():
        print("downloading", name)
        urllib.request.urlretrieve(BASE + name, p)
    return json.loads(p.read_text(encoding="utf-8"))


def rdp(pts, eps):
    if len(pts) < 3:
        return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1
    norm = math.hypot(dx, dy) or 1e-12
    dmax, idx = 0, 0
    for i in range(1, len(pts) - 1):
        x0, y0 = pts[i]
        d = abs(dy * x0 - dx * y0 + x2 * y1 - y2 * x1) / norm
        if d > dmax:
            dmax, idx = d, i
    if dmax > eps:
        return rdp(pts[: idx + 1], eps)[:-1] + rdp(pts[idx:], eps)
    return [pts[0], pts[-1]]


def clip_box(ring):
    """Clamp far-away points into a padded window so huge countries (China, India) stay light."""
    pad = 3
    return [(min(max(x, BOX[0] - pad), BOX[2] + pad), min(max(y, BOX[1] - pad), BOX[3] + pad)) for x, y in ring]


def rings(geom, eps, min_pts=4, clip=False):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    out = []
    for poly in polys:
        ring = poly[0]
        xs = [p[0] for p in ring]
        ys = [p[1] for p in ring]
        if max(xs) < BOX[0] or min(xs) > BOX[2] or max(ys) < BOX[1] or min(ys) > BOX[3]:
            continue
        pts = [(round(x, 3), round(y, 3)) for x, y in ring]
        if clip:
            pts = clip_box(pts)
        mid = len(pts) // 2  # closed rings start and end on the same point: simplify each half
        simp = rdp(pts[: mid + 1], eps)[:-1] + rdp(pts[mid:], eps)
        if len(simp) >= min_pts:
            out.append(simp)
    return out


def main():
    countries = fetch(FILE)
    out = {"countries": {}}
    for f in countries["features"]:
        name = f["properties"].get("ADMIN")
        if name in COUNTRIES:
            eps = 0.006 if name == "Nepal" else 0.03
            out["countries"][name] = rings(f["geometry"], eps, clip=name in ("China", "India"))
    dest = ROOT / "content" / "outlines.json"
    dest.write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    n = sum(len(r) for v in out["countries"].values() for r in v)
    print(f"wrote {dest} · {len(out['countries'])} countries · {n} points · {dest.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
