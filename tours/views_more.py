"""Blog, policies, contact, how-we-work, enquiries, newsletter and search index."""
import json

from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .content import MONTHS, TYPES, catalogue
from .forms import EnquiryForm, SubscribeForm
from .models import Subscriber
from .policies import POLICIES, UPDATED
from .views import COMPANY_FAQS, _get, _mid, crumbs, faq_ld, img_url, ld, org_ld


def journal(request, cat=None):
    c = catalogue()
    posts = list(c.posts.values())
    category = None
    if cat:
        category = c.post_categories.get(cat)
        if not category:
            raise Http404
        posts = category["posts"]
    trail = [("Blog", reverse("journal"))] + ([(category["name"], request.path)] if category else [])
    items, bc = crumbs(*trail)
    return render(request, "tours/journal.html", {"posts": posts, "category": category,
                                                  "cats": list(c.post_categories.values()), "crumbs": items, "ld": ld(bc)})


def post(request, slug):
    c = catalogue()
    d = _get(c.posts, slug)
    items, bc = crumbs(("Blog", reverse("journal")), (d["title"], d["url"]))
    article = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": d["title"],
               "description": d.get("summary"), "datePublished": d.get("date"), "image": img_url(d),
               "author": {"@type": "Organization", "name": settings.SITE["byline"]},
               "publisher": {"@type": "Organization", "name": settings.SITE["name"]}}
    more = [x for x in c.posts.values() if x is not d and (
        x["cat_slug"] == d["cat_slug"] or set(x.get("regions", [])) & set(d.get("regions", [])))][:3]
    return render(request, "tours/post.html", {"d": d, "more": more, "crumbs": items,
                                               "ld": ld(bc, article, faq_ld(d.get("faqs", [])))})


def policies(request):
    items, bc = crumbs(("Policies", reverse("policies")))
    return render(request, "tours/policies.html", {"policies": [dict(v, slug=k) for k, v in POLICIES.items()],
                                                   "crumbs": items, "ld": ld(bc)})


def policy(request, slug):
    pol = POLICIES.get(slug)
    if not pol:
        raise Http404
    items, bc = crumbs(("Policies", reverse("policies")), (pol["title"], request.path))
    sections = [{"heading": h, "blocks": [b if isinstance(b, dict) else {"p": b} for b in body]} for h, body in pol["sections"]]
    others = [(k, v["nav"]) for k, v in POLICIES.items() if k != slug]
    return render(request, "tours/policy.html", {"pol": pol, "slug": slug, "sections": sections, "others": others,
                                                 "updated": UPDATED, "crumbs": items, "ld": ld(bc)})


def contact(request):
    items, bc = crumbs(("Contact", reverse("contact")))
    form = EnquiryForm(initial={"source_page": request.path, "kind": "callback"})
    return render(request, "tours/contact.html", {"form": form, "crumbs": items, "ld": ld(bc, org_ld())})


def how_we_work(request):
    items, bc = crumbs(("How booking works", reverse("how_we_work")))
    return render(request, "tours/how_we_work.html", {"crumbs": items, "faqs": COMPANY_FAQS[:6],
                                                      "ld": ld(bc, faq_ld(COMPANY_FAQS[:6]))})


def plan(request):
    cat = catalogue()
    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("plan_thanks")
    else:
        g = request.GET
        initial = {"source_page": g.get("from", "")[:300], "kind": "full"}
        if g.get("region") in cat.regions:
            initial["regions"] = [g["region"]]
        if g.get("type") in TYPES:
            initial["trip_type"] = g["type"]
        month = (g.get("month") or "").capitalize()
        if month in MONTHS:
            initial["month"] = month
        if g.get("package") in cat.packages:
            k = cat.packages[g["package"]]
            initial.update({"package": k["title"], "trip_type": k.get("type"), "regions": [k["region"]], "days": k["days_count"]})
        if g.get("days", "").isdigit():
            initial["days"] = int(g["days"])
        if g.get("city"):
            initial["from_city"] = g["city"][:80]
        form = EnquiryForm(initial=initial)
    items, bc = crumbs(("Get a quote", reverse("plan")))
    return render(request, "tours/plan.html", {"form": form, "crumbs": items, "ld": ld(bc)})


def enquire(request):
    """Quick quote, call-back and booking-request forms post here; errors fall back to the full planner."""
    if request.method != "POST":
        return redirect("plan")
    form = EnquiryForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect("plan_thanks")
    items, bc = crumbs(("Get a quote", reverse("plan")))
    return render(request, "tours/plan.html", {"form": form, "crumbs": items, "ld": ld(bc)})


def plan_thanks(request):
    return render(request, "tours/plan_thanks.html", {"crumbs": crumbs(("Get a quote", reverse("plan")))[0],
                                                      "packages": _mid(list(catalogue().packages.values()), 3)})


def subscribe(request):
    if request.method != "POST":
        return redirect("home")
    form = SubscribeForm(request.POST)
    ok = form.is_valid() and not form.cleaned_data.get("website")
    if ok:
        Subscriber.objects.get_or_create(email=form.cleaned_data["email"].lower(),
                                         defaults={"source_page": form.cleaned_data.get("source_page", "")[:300]})
    return render(request, "tours/subscribed.html", {"ok": ok, "crumbs": crumbs(("Blog", reverse("journal")))[0]})


def search_index(request):
    """Compact JSON index for the on-site search overlay: [title, url, kind, context]."""
    c = catalogue()
    rows = [[r["name"], r["url"], "Destination", r.get("palette", "")] for r in c.regions.values()]
    rows += [[k["title"], k["url"], f"{k['type_obj']['label']} · {k['days_count']} days", f"from ₹{k['inr']}"] for k in c.packages.values()]
    rows += [[t["name"], t["url"], "Tour style", ""] for t in c.themes.values()]
    rows += [[p["name"], p["url"], "Place", p["region_obj"]["name"]] for p in c.places.values()]
    rows += [[e["title"], e["url"], "Things to do", e["place_obj"]["name"]] for e in c.experiences.values()]
    rows += [[s["name"], s["url"], "Hotel", s["region_obj"]["name"]] for s in c.stays.values()]
    rows += [[g["title"], g["url"], "Guide", g["region_obj"]["name"]] for g in c.guides.values()]
    rows += [[d["title"], d["url"], "Blog", d.get("category", "")] for d in c.posts.values()]
    rows += [[f["name"], f["url"], "Festival", f["region_obj"]["name"]] for f in c.festivals.values()]
    rows += [[o["title"], o["url"], "From India", o["city"]] for o in c.origins.values()]
    resp = HttpResponse(json.dumps(rows, ensure_ascii=False, separators=(",", ":")), content_type="application/json")
    resp["Cache-Control"] = "public, max-age=3600"
    return resp
