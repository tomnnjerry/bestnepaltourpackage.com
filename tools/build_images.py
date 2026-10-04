"""Build content/images.json: freely licensed photos from Wikimedia Commons, with credits.

For every region, place, experience, stay, festival and guide we look up
1. the lead image of its `wiki` article (when it has one), then
2. Commons file search on its `image_query`,
keep only JPEG photos under a free licence (CC0, public domain, CC BY, CC BY-SA) that are at
least 1,000 px wide, and store author, licence and a link back to the file page. Search hits
must mention the subject's name in the file title or description, so a search never puts a
photo of somewhere else on a page.

Keys match tours/content.py: region:<slug>, place:<slug>, exp:<slug>, stay:<slug>, fest:<slug>,
guide:<slug>. Existing keys are kept unless --refresh is given, so a rerun only fills gaps.
API responses are cached in .cache/commons/ (git-ignored).

Usage: python tools/build_images.py [--refresh] [--only place|exp|stay|fest|region|guide]
"""
import hashlib
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
CACHE = ROOT / ".cache" / "commons"
OUT = CONTENT / "images.json"
UA = "BestNepalTourPackageBuild/1.0 (https://bestnepaltourpackage.com; image credits)"
FREE = re.compile(r"^(cc0|public domain|pd|cc by(-sa)? ?\d(\.\d)?( [a-z]+)?|cc by(-sa)?)", re.I)
SKIP_WORDS = re.compile(r"\b(map|logo|flag|locator|diagram|chart|stamp|coat of arms|seal|banknote|svg)\b", re.I)
STOP = {"the", "and", "of", "in", "at", "to", "a", "on", "with", "from", "for", "by", "nepal", "tour", "trek",
        "walk", "day", "view", "hotel", "lodge", "resort", "national", "park", "temple", "lake", "base", "camp"}
WIDTH = 960


def api(host, params):
    params = dict(params, format="json", formatversion=2)
    url = f"https://{host}/w/api.php?" + urllib.parse.urlencode(params)
    key = CACHE / (hashlib.sha1(url.encode()).hexdigest() + ".json")
    if key.exists():
        return json.loads(key.read_text(encoding="utf-8"))
    for attempt in range(8):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            data = json.load(urllib.request.urlopen(req, timeout=40))
            break
        except Exception as e:  # noqa: BLE001  (429 rate limits: wait as long as the server asks)
            if attempt == 7:
                raise
            wait = getattr(e, "headers", None) and e.headers.get("Retry-After")
            time.sleep(min(int(wait) if wait and wait.isdigit() else 5 * 2 ** attempt, 120))
    CACHE.mkdir(parents=True, exist_ok=True)
    key.write_text(json.dumps(data), encoding="utf-8")
    time.sleep(0.4)
    return data


def canon(url):
    """Canonical Commons media URL: upload.wikimedia.org host, no tracking query string."""
    return (url or "").split("?")[0].replace("://thumb.wikimedia.org/", "://upload.wikimedia.org/")


def plain(s):
    s = re.sub(r"<[^>]+>", "", s or "")
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def lead_files(titles):
    """Wikipedia title -> lead image file name, in batches of 40."""
    out = {}
    titles = sorted({t for t in titles if t})
    for i in range(0, len(titles), 40):
        data = api("en.wikipedia.org", {"action": "query", "prop": "pageimages", "piprop": "name",
                                        "titles": "|".join(titles[i:i + 40]), "redirects": 1})
        q = data.get("query", {})
        back = {}
        for n in q.get("normalized", []) + q.get("redirects", []):
            back[n["to"]] = back.get(n["from"], n["from"])
        for pg in q.get("pages", []):
            if pg.get("pageimage"):
                orig = pg["title"]
                while orig in back:
                    orig = back[orig]
                out[orig] = "File:" + pg["pageimage"]
                out[pg["title"]] = "File:" + pg["pageimage"]
    return out


def search_files(query, n=8):
    """Commons file search; one request returns the hits together with their credit records."""
    if not query:
        return []
    data = api("commons.wikimedia.org", {"action": "query", "generator": "search", "gsrnamespace": 6,
                                         "gsrsearch": f"{query} filetype:bitmap", "gsrlimit": n,
                                         "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata", "iiurlwidth": WIDTH})
    pages = sorted(data.get("query", {}).get("pages", []), key=lambda pg: pg.get("index", 0))
    for pg in pages:
        _info[pg["title"]] = _record(pg)
    return [pg["title"] for pg in pages]


_info = {}


BLOCKED = set(json.loads((CONTENT / "image_blocklist.json").read_text(encoding="utf-8"))) \
    if (CONTENT / "image_blocklist.json").exists() else set()


def _record(pg):
    """Credit record for one Commons file page, or None unless it is a free-licence JPEG photo of 1,000 px or more."""
    title = pg.get("title", "")
    ii = (pg.get("imageinfo") or [None])[0]
    if title in BLOCKED or not ii or ii.get("mime") != "image/jpeg" or ii.get("width", 0) < 1000:
        return None
    meta = ii.get("extmetadata", {})
    lic = plain(meta.get("LicenseShortName", {}).get("value"))
    author = plain(meta.get("Artist", {}).get("value")) or "Unknown author"
    desc = plain(meta.get("ImageDescription", {}).get("value"))[:300]
    if not FREE.match(lic) or SKIP_WORDS.search(title + " " + desc[:120]):
        return None
    return {"file": title, "url": canon(ii["url"]), "thumb": canon(ii.get("thumburl") or ii["url"]), "page": ii.get("descriptionurl"),
            "author": author[:120], "license": lic, "width": ii["width"], "height": ii["height"], "description": desc}


def file_info(files):
    """File:... -> credit record (or None when unusable), batched 50 at a time."""
    need = [f for f in dict.fromkeys(files) if f not in _info]
    for i in range(0, len(need), 50):
        data = api("commons.wikimedia.org", {"action": "query", "prop": "imageinfo", "titles": "|".join(need[i:i + 50]),
                                             "iiprop": "url|size|mime|extmetadata", "iiurlwidth": WIDTH})
        q = data.get("query", {})
        norm = {n["to"]: n["from"] for n in q.get("normalized", [])}
        for pg in q.get("pages", []):
            title = pg.get("title")
            rec = _record(pg)
            _info[title] = rec
            if title in norm:
                _info[norm[title]] = rec
        for f in need[i:i + 50]:
            _info.setdefault(f, None)
    return [_info.get(f) for f in files]


def tokens(*names):
    out = set()
    for n in names:
        for w in re.findall(r"[a-z]{4,}", (n or "").lower()):
            if w not in STOP:
                out.add(w)
    return out


def mentions(rec, words, title_only=False):
    hay = (rec["file"] + ("" if title_only else " " + rec.get("description", ""))).lower()
    return not words or any(w in hay for w in words)


def pick(subject, n):
    """subject: dict(lead, query, names, strict); strict subjects (hotels) only take search hits whose
    file title names them, never a mere description match. Returns up to n credit records."""
    files = []
    if subject.get("lead"):
        files.append(subject["lead"])
    found = search_files(subject.get("query"))
    usable = [f for f in found if _info.get(f)]
    if len(usable) < min(n, 2) and subject.get("names") and subject["names"][0]:
        found += [f for f in search_files(subject["names"][0] + " Nepal") if f not in found]
    words = tokens(*subject.get("names", []))
    out, seen = [], set()
    for f, rec in zip(files + found, file_info(files + found)):
        if not rec or rec["file"] in seen:
            continue
        if f not in files and not mentions(rec, words, title_only=subject.get("strict")):
            continue
        seen.add(rec["file"])
        out.append(rec)
        if len(out) >= n:
            break
    return out


def load_subjects():
    subs = []
    for rdir in sorted(p for p in CONTENT.iterdir() if p.is_dir() and (p / "places").exists()):
        reg = rdir / "region.json"
        if reg.exists():
            r = json.loads(reg.read_text(encoding="utf-8"))
            subs.append(("region", rdir.name, r.get("wiki"), f"{r.get('wiki') or r.get('name')} Nepal landscape",
                         [r.get("name"), r.get("wiki")], 4, False))
        for p in sorted((rdir / "places").glob("*.json")):
            d = json.loads(p.read_text(encoding="utf-8"))
            subs.append(("place", d["slug"], d.get("wiki"), d.get("image_query"), [d.get("name"), d.get("wiki")], 5, False))
            for e in d.get("experiences", []):
                subs.append(("exp", e["slug"], e.get("wiki"), e.get("image_query"),
                             [e.get("title"), e.get("image_query"), d.get("name")], 2, False))
        for name, kind in (("stays.json", "stay"), ("festivals.json", "fest")):
            f = rdir / name
            for d in (json.loads(f.read_text(encoding="utf-8")) if f.exists() else []):
                names = [d.get("name"), d.get("wiki")]
                subs.append((kind, d["slug"], d.get("wiki"), d.get("image_query"), names, 3 if kind == "fest" else 2,
                             kind == "stay"))
    return subs


def main():
    refresh = "--refresh" in sys.argv
    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
    images = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    order = {"region": 0, "place": 1, "fest": 2, "stay": 3, "exp": 4}
    subs = sorted((s for s in load_subjects() if not only or s[0] == only), key=lambda s: order.get(s[0], 9))
    leads = lead_files([s[2] for s in subs])
    file_info(list(leads.values()))  # credit records for every lead image, 50 per request
    done = 0
    for kind, slug, wiki, query, names, n, strict in subs:
        key = f"{kind}:{slug}"
        if key in images and images[key] and not refresh:
            continue
        recs = pick({"lead": leads.get(wiki) if wiki else None, "query": query, "names": names, "strict": strict}, n)
        if recs:
            images[key] = recs
        else:
            images.pop(key, None)
        done += 1
        if done % 50 == 0:
            print(f"  {done} looked up · {len(images)} keys with photos", flush=True)
            OUT.write_text(json.dumps(images, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    OUT.write_text(json.dumps(images, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    missing = [f"{k}:{s}" for k, s, *_ in subs if f"{k}:{s}" not in images]
    print(f"wrote {OUT} · {len(images)} keys · {sum(len(v) for v in images.values())} photos · "
          f"{len(missing)} subjects without a photo")
    for m in missing[:60]:
        print("  no photo:", m)


if __name__ == "__main__":
    main()
