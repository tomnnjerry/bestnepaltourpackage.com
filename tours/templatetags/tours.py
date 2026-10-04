import re

from django import template
from django.utils.safestring import mark_safe

from ..content import GRADES, TYPES, catalogue, inr as _inr

register = template.Library()
STD_WIDTHS = [500, 960, 1280, 1920]
_THUMB = re.compile(r"/(\d+)px-")


def _clean(url):
    return (url or "").split("?")[0]


def _at(img, w):
    url = _clean(img.get("thumb") or img.get("url"))
    if "/thumb/" in url and _THUMB.search(url):
        if img.get("width") and w >= img["width"]:
            return _clean(img.get("url"))
        return _THUMB.sub(f"/{w}px-", url, count=1)
    return url


@register.filter
def src(img, w=960):
    return _at(img, int(w)) if img else ""


@register.filter
def srcset(img):
    if not img:
        return ""
    widths = [w for w in STD_WIDTHS if not img.get("width") or w < img["width"]] or [img.get("width") or 960]
    return ", ".join(f"{_at(img, w)} {w}w" for w in widths)


@register.filter
def inr(value):
    s = _inr(value)
    return f"₹{s}" if s else ""


@register.filter
def usd(value):
    try:
        return f"US${int(value):,}"
    except (TypeError, ValueError):
        return ""


@register.filter
def metres(value):
    try:
        return f"{int(value):,} m"
    except (TypeError, ValueError):
        return ""


@register.filter
def thousands(value):
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return value


@register.filter
def get(d, key):
    try:
        return d.get(key)
    except AttributeError:
        return None


@register.filter
def at(seq, i):
    try:
        return seq[int(i)]
    except (IndexError, TypeError, ValueError):
        return None


@register.filter
def first_img(obj):
    imgs = (obj or {}).get("images") or []
    return imgs[0] if imgs else None


@register.filter
def nth_img(obj, n):
    imgs = (obj or {}).get("images") or []
    return imgs[int(n) % len(imgs)] if imgs else None


@register.filter
def theme_name(slug):
    t = catalogue().themes.get(slug)
    return t.get("short") or t["name"] if t else slug.replace("-", " ").capitalize()


@register.filter
def theme_url(slug):
    t = catalogue().themes.get(slug)
    return t["url"] if t else "#"


@register.filter
def place_obj(slug):
    return catalogue().places.get(slug)


@register.filter
def type_label(slug):
    return TYPES.get(slug, {}).get("label", slug)


@register.filter
def grade_level(grade):
    try:
        return GRADES.index(grade) + 1
    except ValueError:
        return 1


@register.filter
def days_label(pkg):
    d = (pkg or {}).get("nights", 0) + 1
    n = d - 1
    if n == 0:
        return "1 day"
    return f"{d} days · {n} night{'s' if n != 1 else ''}"


@register.filter
def short_credit(img):
    if not img:
        return ""
    author = re.sub(r"\s+", " ", img.get("author") or "Unknown")
    if len(author) > 48:
        author = author[:46] + "…"
    return f"{author} · {img.get('license')}"


@register.filter
def pad2(n):
    try:
        return f"{int(n):02d}"
    except (TypeError, ValueError):
        return n


@register.filter
def split_first(s, sep=" "):
    return (s or "").split(sep)[0]


@register.inclusion_tag("tours/partials/photo.html")
def photo(img, alt="", cls="", sizes="(max-width: 760px) 100vw, 50vw", eager=False, credit=True):
    return {"img": img, "alt": alt or (img or {}).get("description") or "", "cls": cls, "sizes": sizes,
            "eager": eager, "credit": credit}


@register.simple_tag
def icon(name, cls=""):
    from ..icons import svg
    return mark_safe(svg(name, cls))


@register.simple_tag
def atlas(points, route=False, legend=True):
    from ..atlas import atlas_svg
    return mark_safe(atlas_svg(points, route=route, legend=legend))


@register.simple_tag
def nepal_map(regions, active=None):
    from ..atlas import nepal_svg
    return mark_safe(nepal_svg(regions, active))


@register.simple_tag
def profile(pkg):
    from ..atlas import profile_svg
    return mark_safe(profile_svg(pkg.get("days", []), pkg.get("acclim_flags", [])))


@register.simple_tag
def spark(pkg):
    from ..atlas import spark_svg
    return mark_safe(spark_svg(pkg.get("alts", [])))
