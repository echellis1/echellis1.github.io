"""Pelican settings for local development.

Build:   pelican content
Preview: pelican --autoreload --listen   (then open http://localhost:8000)
"""

import hashlib
import re
import sys
from pathlib import Path

import markdown

sys.path.append(str(Path(__file__).parent))

AUTHOR = "Eric Chellis"
SITENAME = "Eric Chellis"
SITE_TAGLINE = "Broadcast & AV Production"
SITE_DESCRIPTION = (
    "Eric Chellis — Cable TV Coordinator and live broadcast producer. "
    "vMix, Dante, NDI and TelVue broadcast operations in Exeter, NH."
)
SITEURL = ""  # empty for local preview; publishconf.py sets the real address

PATH = "content"
TIMEZONE = "America/New_York"
DEFAULT_LANG = "en"
DEFAULT_DATE_FORMAT = "%b %d, %Y"

THEME = "themes/broadcast"
PLUGIN_PATHS = ["plugins"]
PLUGINS = ["post_cover"]

# ---------------------------------------------------------------------------
# Content layout
#   content/pages/         Home, Experience, Skills, Contact
#   content/posts/<id>/    One folder per Featured post: index.md + its images
#   content/experience/    One Markdown file per job (shown on Experience page)
#   content/images/        Files served at /images/... (resume.pdf, photos)
#   content/extra/         Files copied to the site root as-is
# ---------------------------------------------------------------------------
PAGE_PATHS = ["pages"]
ARTICLE_PATHS = ["posts"]
STATIC_PATHS = ["posts", "images", "extra"]
EXTRA_PATH_METADATA = {
    "extra/post.html": {"path": "post.html"},  # redirects old post.html?post=... links
}

# The post's folder name (e.g. 20250925) becomes its slug and URL.
PATH_METADATA = r"posts/(?P<slug>[^/]+)/index\.md"

ARTICLE_URL = "posts/{slug}/"
ARTICLE_SAVE_AS = "posts/{slug}/index.html"
PAGE_URL = "{slug}.html"
PAGE_SAVE_AS = "{slug}.html"

# Only build the pages this site actually uses.
DIRECT_TEMPLATES = ["featured"]
FEATURED_SAVE_AS = "featured.html"
INDEX_SAVE_AS = ""
CATEGORY_SAVE_AS = CATEGORIES_SAVE_AS = ""
TAG_SAVE_AS = TAGS_SAVE_AS = ""
AUTHOR_SAVE_AS = AUTHORS_SAVE_AS = ""
ARCHIVES_SAVE_AS = ""
ARTICLE_LANG_SAVE_AS = PAGE_LANG_SAVE_AS = ""

# No feeds while previewing locally (publishconf.py turns one on).
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.extra": {},
        "markdown.extensions.meta": {},
        "markdown.extensions.codehilite": {"css_class": "highlight"},
    },
    "output_format": "html5",
}

# ---------------------------------------------------------------------------
# Header, nav and social links (used by the theme)
# ---------------------------------------------------------------------------
SHOW_TALLY = True  # the red "ON AIR" badge in the header; set False to hide it

NAV = [
    ("Home", "index.html"),
    ("Experience", "experience.html"),
    ("Skills", "skills.html"),
    ("Featured", "featured.html"),
    ("Contact", "contact.html"),
]

SOCIAL = [
    ("LinkedIn", "https://www.linkedin.com/in/eric-chellis/", "linkedin.svg"),
    ("GitHub", "https://github.com/echellis1", "github.svg"),
    ("Instagram", "https://www.instagram.com/hockeyfan1279/", "instagram.svg"),
    ("Facebook", "https://www.facebook.com/ericchellis", "facebook.svg"),
]

# Picture used when a page is shared on LinkedIn/Facebook. Put a 1200x630
# image in content/images/ and set this to e.g. "images/share.jpg".
# Posts use their own cover image automatically.
SOCIAL_IMAGE = ""

# How many posts the Home page shows under "Featured Posts".
HOME_POST_COUNT = 3

# ---------------------------------------------------------------------------
# Cache-busting: the stylesheet link gets ?v=<hash of styles.css>, so browsers
# fetch the new CSS whenever you change it. No more bumping ?v=14 by hand.
# ---------------------------------------------------------------------------
_css = Path(__file__).parent / THEME / "static" / "css" / "styles.css"
CSS_VERSION = hashlib.md5(_css.read_bytes()).hexdigest()[:8] if _css.exists() else "1"


# ---------------------------------------------------------------------------
# Experience page: every .md file in content/experience/ is rendered and
# sorted newest first by the "*Month YYYY – Month YYYY*" line, same as before.
# Add a job = add a file. Nothing else to edit.
# ---------------------------------------------------------------------------
_MONTHS = ["jan", "feb", "mar", "apr", "may", "jun",
           "jul", "aug", "sep", "oct", "nov", "dec"]


def _month_index(text):
    if re.search(r"present", text, re.I):
        return float("inf")
    m = re.search(r"([A-Za-z]+)\s+(\d{4})", text)
    if not m:
        return 0
    month = m.group(1)[:3].lower()
    return int(m.group(2)) * 12 + (_MONTHS.index(month) if month in _MONTHS else 0)


def _sort_key(md_text):
    m = re.search(r"\*([^*]+?)\s+[–-]\s+([^*]+?)\*", md_text)
    if not m:
        return (0, 0)
    return (_month_index(m.group(2)), _month_index(m.group(1)))


def _load_experience():
    folder = Path(__file__).parent / PATH / "experience"
    docs = [p.read_text(encoding="utf-8") for p in sorted(folder.glob("*.md"))]
    docs.sort(key=_sort_key, reverse=True)
    return [markdown.markdown(d, extensions=["extra"], output_format="html5") for d in docs]


EXPERIENCE = _load_experience()
