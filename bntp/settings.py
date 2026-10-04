"""Django settings for bestnepaltourpackage.com."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-change-me-in-production")
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,testserver,bestnepaltourpackage.com,www.bestnepaltourpackage.com").split(",")
CSRF_TRUSTED_ORIGINS = ["https://bestnepaltourpackage.com", "https://www.bestnepaltourpackage.com"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "tours",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

try:  # optional: serves /static/ efficiently in production
    import whitenoise  # noqa: F401
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
except ImportError:
    pass

ROOT_URLCONF = "bntp.urls"
WSGI_APPLICATION = "bntp.wsgi.application"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
        "tours.context.site",
    ]},
}]

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}

LANGUAGE_CODE = "en-gb"
TIME_ZONE = "Asia/Kathmandu"
USE_I18N = False
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CONTENT_DIR = BASE_DIR / "content"

# Business details. Fill these before launch; placeholders render as-is.
SITE = {
    "name": "Best Nepal Tour Package",
    "short": "BNTP",
    "domain": "bestnepaltourpackage.com",
    "url": "https://bestnepaltourpackage.com",
    "email": os.environ.get("BNTP_EMAIL", "[YOUR EMAIL]"),
    "phone": os.environ.get("BNTP_PHONE", "[YOUR PHONE]"),
    "whatsapp": os.environ.get("BNTP_WHATSAPP", ""),  # digits with country code, e.g. 9779800000000
    "address": "[YOUR OFFICE ADDRESS], Kathmandu, Nepal",
    "licence": "[NEPAL TOURISM / DEPARTMENT OF TOURISM REGISTRATION NO.]",
    "byline": "Best Nepal Tour Package Travel Desk",
    "usd_rate": 84,  # INR per USD, only used by the budget calculator for display
}

# Enquiry alerts by email (optional). Every enquiry is always saved and listed in /admin/;
# set EMAIL_HOST (and friends) to also get an email for each one.
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "1") == "1"
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER or "webmaster@bestnepaltourpackage.com")
ENQUIRY_NOTIFY_TO = os.environ.get("BNTP_NOTIFY_EMAIL", SITE["email"])

# Production hardening: on when DEBUG is off (the site is served behind HTTPS).
if not DEBUG:
    if SECRET_KEY.startswith("dev-only"):
        raise RuntimeError("Set DJANGO_SECRET_KEY before running with DJANGO_DEBUG=0")
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
    SECURE_HSTS_SECONDS = int(os.environ.get("DJANGO_HSTS_SECONDS", "0"))  # raise to 31536000 once HTTPS is confirmed

# Optional Google Analytics 4 measurement ID (e.g. G-XXXXXXX). Leave empty to load no analytics.
GA4_ID = os.environ.get("BNTP_GA4", "")

# Production: hashed file names so every deploy busts browser caches.
if os.environ.get("BNTP_HASHED_STATIC") == "1":
    STORAGES = {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
                        if "whitenoise.middleware.WhiteNoiseMiddleware" in MIDDLEWARE
                        else "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"},
    }
