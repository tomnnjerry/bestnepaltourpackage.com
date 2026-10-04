import re
from pathlib import Path
from urllib.parse import quote

from django.conf import settings

from .content import KINDS, TYPES, catalogue
from .policies import POLICIES


def _asset_version():
    """Changes whenever a CSS/JS file changes, so browsers never run a stale copy."""
    root = Path(settings.BASE_DIR) / "static"
    return int(max((p.stat().st_mtime for p in root.rglob("*") if p.suffix in (".css", ".js")), default=0))


SOCIAL_LABELS = {"facebook": "Facebook", "instagram": "Instagram", "youtube": "YouTube", "x": "X", "linkedin": "LinkedIn",
                 "tiktok": "TikTok"}


def social_links(whatsapp_url=""):
    """Configured social profiles (https only) in a fixed order, WhatsApp first when we have a number."""
    out = []
    if whatsapp_url:
        out.append({"key": "whatsapp", "label": "WhatsApp", "url": whatsapp_url})
    for key, label in SOCIAL_LABELS.items():
        url = (getattr(settings, "SOCIAL", {}).get(key) or "").strip()
        if url.startswith("https://"):
            out.append({"key": key, "label": label, "url": url})
    return out


def site(request):
    cat = catalogue()
    S = settings.SITE
    regions = list(cat.regions.values())
    phone_digits = re.sub(r"\D", "", S.get("phone", ""))
    wa = re.sub(r"\D", "", S.get("whatsapp", ""))
    by_type = {}
    for k in cat.packages.values():
        by_type.setdefault(k.get("type"), []).append(k)
    nav_types = []
    for t, meta in TYPES.items():
        pk = sorted(by_type.get(t, []), key=lambda k: k.get("price_from_inr", 0))
        if pk:
            theme = cat.themes.get(meta["theme"])
            nav_types.append({"slug": t, **meta, "url": theme["url"] if theme else "/packages/?type=" + t,
                              "from_inr": pk[0].get("price_from_inr"), "picks": pk[len(pk) // 3: len(pk) // 3 + 3]})
    heli = sorted(by_type.get("heli", []), key=lambda k: k.get("price_from_inr", 0))
    treks = sorted(by_type.get("trek", []), key=lambda k: -k.get("max_altitude_m", 0))
    return {
        "SITE": S,
        "nav_regions": regions,
        "nav_types": nav_types,
        "nav_heli": heli[:6],
        "nav_treks": treks[:6],
        "nav_themes": [t for t in cat.themes.values() if not t.get("type")],
        "nav_all_themes": list(cat.themes.values()),
        "nav_kinds": [(k, v[0]) for k, v in KINDS.items()],
        "nav_origins": list(cat.origins.values()),
        "nav_posts": list(cat.posts.values())[:3],
        "nav_policies": [(k, v["nav"]) for k, v in POLICIES.items()],
        "canonical": S["url"] + request.path,
        "tel": f"+{phone_digits}" if len(phone_digits) >= 10 else "",
        "wa_base": f"https://wa.me/{wa}" if len(wa) >= 10 else "",
        "social": social_links(f"https://wa.me/{wa}" if len(wa) >= 10 else ""),
        "wa_text": quote(f"Hello Best Nepal Tour Package, I would like a quote. (Page: {S['url']}{request.path})"),
        "GA4": getattr(settings, "GA4_ID", ""),
        "V": _asset_version(),
    }
