"""Render every page the site links to and report failures.

Usage: python tools/crawl.py [--max N] [--show-404]
Starts from the home page and sitemap.xml, follows internal links with Django's test client
(no server needed) and prints every URL that returns 404/500 or raises while rendering.
"""
import os
import re
import sys
import traceback
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bntp.settings")
import django  # noqa: E402

django.setup()
from django.conf import settings  # noqa: E402
from django.test import Client  # noqa: E402

settings.ALLOWED_HOSTS = ["*"]
settings.DEBUG = False  # the DEBUG 500 page pretty-prints the whole catalogue and takes minutes
HREF = re.compile(r'(?:href|action)="(/[^"#?]*)')


def main():
    limit = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 100000
    c = Client(raise_request_exception=True)
    seen, queue, bad = set(), deque(["/", "/sitemap.xml", "/robots.txt", "/llms.txt", "/search.json"]), []
    while queue and len(seen) < limit:
        url = queue.popleft()
        if url in seen or url.startswith(("/static/", "/admin/")):
            continue
        seen.add(url)
        try:
            r = c.get(url)
        except Exception as e:  # noqa: BLE001
            bad.append((url, "EXC", f"{type(e).__name__}: {e}"))
            tb = traceback.format_exc().strip().splitlines()
            bad[-1] = (url, "EXC", " | ".join(tb[-4:]))
            continue
        if r.status_code in (301, 302):
            queue.append(r["Location"])
            continue
        if r.status_code != 200:
            bad.append((url, r.status_code, ""))
            continue
        body = r.content.decode("utf-8", "replace")
        if url == "/sitemap.xml":
            links = [re.sub(r"^https?://[^/]+", "", u) for u in re.findall(r"<loc>([^<]+)</loc>", body)]
        else:
            links = HREF.findall(body)
        for u in links:
            if u not in seen:
                queue.append(u)
    print(f"crawled {len(seen)} urls, {len(bad)} problems")
    for u, code, msg in bad:
        if code == 404 and "--show-404" not in sys.argv and False:
            continue
        print(code, u, msg[:400])
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
