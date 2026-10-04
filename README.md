# bestnepaltourpackage.com

Django site for Best Nepal Tour Package: Nepal tour packages, helicopter tours, treks, pilgrimages,
safaris and Kailash yatras, with prices in INR and USD. Every content page is rendered from JSON in
`content/`; the database only stores enquiries and newsletter sign-ups.

## Run it locally

```bash
python -m venv .venv && . .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser                    # to read enquiries at /admin/
python manage.py runserver
```

In DEBUG (the default locally), the catalogue reloads whenever a content file changes, so you see JSON
edits as soon as you refresh.

## Content

| Path | What it holds |
| --- | --- |
| `content/SCHEMA.md` | Every field, count and house-style rule. Read it before editing content |
| `content/<region>/region.json` | Region overview, 12 month notes, FAQs. A region without it is not shown |
| `content/<region>/places/*.json` | One file per place, each with 3 things to do |
| `content/<region>/packages/*.json` | Packages with day-by-day itineraries and prices |
| `content/<region>/stays.json`, `festivals.json`, `routes.json`, `guides/*.json` | Hotels, festivals, getting-around pages, long guides |
| `content/themes.json`, `origins.json` | Tour styles and "Nepal tour package from <city>" pages |
| `content/journal/*.json` | Blog posts |
| `content/images.json` | Photo records (Wikimedia Commons) built by `tools/build_images.py` |
| `content/outlines.json` | Country outlines for the self-drawn SVG maps (`tools/build_outlines.py`) |

## Tools

```bash
python tools/check_region.py <region> [--wiki]   # validate one region against SCHEMA.md
python tools/build_images.py                     # fill content/images.json with free-licence photos
python tools/crawl.py                            # render every linked page and report 404/500s
```

After adding places, stays or festivals, run `build_images.py` again; it only looks up new subjects
(use `--refresh` to redo everything). Photos are credited on each page and on `/photo-credits/`.

## Settings (environment variables)

| Variable | Purpose |
| --- | --- |
| `DJANGO_SECRET_KEY` | Required in production |
| `DJANGO_DEBUG` | `0` in production (default `1`) |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated host names |
| `BNTP_EMAIL`, `BNTP_PHONE`, `BNTP_WHATSAPP` | Contact details shown on the site (defaults: hello@bestnepaltourpackage.com, +91 99546 34102; WhatsApp: digits with country code) |
| `BNTP_GA4` | Google Analytics 4 measurement ID (optional) |
| `BNTP_HASHED_STATIC` | `1` to serve hashed, compressed static files via WhiteNoise |
| `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS` | SMTP for enquiry alerts (optional) |
| `BNTP_NOTIFY_EMAIL` | Where enquiry alerts go (defaults to `BNTP_EMAIL`) |
| `DJANGO_HSTS_SECONDS` | Raise to `31536000` once HTTPS works everywhere |

## Deploy

```bash
pip install -r requirements.txt gunicorn
export DJANGO_DEBUG=0 DJANGO_SECRET_KEY=... BNTP_HASHED_STATIC=1
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn bntp.wsgi --bind 0.0.0.0:8000 --workers 3
```

Put Nginx or your host's HTTPS proxy in front, forwarding `X-Forwarded-Proto`. WhiteNoise serves `/static/`.

## Before launch

Placeholders in `[BRACKETS]` render as they are until you replace them:

- `bntp/settings.py` `SITE`: legal name, office address, office hours and Department of Tourism registration number
  (email, phone and WhatsApp are set to the defaults above; override with the environment variables).
- `templates/tours/base.html` footer: TAAN / NATTA membership and accepted payment methods.
- `tours/policies.py`: every bracketed value (deposit %, cancellation scale, refund days, review date);
  have the policies checked by a lawyer.
- Facts the content marks "check current status before you travel" (permit fees, Kailash rules, flights)
  should be re-confirmed each season.
