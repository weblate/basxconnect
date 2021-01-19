from django.conf import settings
from languages.languages import LANGUAGES

DEFAULTS = {"PREFERRED_LANGUAGES": ("en",)}

preferred_codes = getattr(settings, "BASXCONNECT", {}).get(
    "PREFERRED_LANGUAGES", DEFAULTS["PREFERRED_LANGUAGES"]
)
PREFERRED_LANGUAGES = [i for i in LANGUAGES if i[0] in preferred_codes]
PREFERRED_LANGUAGES.sort(key=lambda e: preferred_codes.index(e[0]))
