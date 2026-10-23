"""Find each post's cover image.

Uses the post's `Image:` metadata if set, otherwise <slug>.jpg in the post's
folder (e.g. content/posts/20250925/20250925.jpg). Sets `article.cover` to the
site-relative path, or leaves it empty if no file exists, so templates can do
{% if article.cover %}.
"""

from pathlib import Path

from pelican import signals
from pelican.contents import Article


def set_cover(instance):
    if not isinstance(instance, Article):
        return
    folder = Path(instance.source_path).parent
    name = (getattr(instance, "image", "") or "").strip() or f"{instance.slug}.jpg"
    instance.cover = f"posts/{instance.slug}/{name}" if (folder / name).is_file() else ""


def register():
    signals.content_object_init.connect(set_cover)
