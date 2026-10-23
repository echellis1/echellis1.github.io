"""Settings for the live site. Used by the GitHub Actions deploy:

    pelican content -s publishconf.py
"""

import os
import sys

sys.path.append(os.curdir)
from pelicanconf import *  # noqa: E402,F401,F403

# If you add a custom domain later, change this (and add content/extra/CNAME).
SITEURL = "https://echellis1.github.io"
RELATIVE_URLS = False

FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = "feeds/posts.atom.xml"

DELETE_OUTPUT_DIRECTORY = True
