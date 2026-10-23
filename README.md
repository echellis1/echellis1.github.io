# echellis1.github.io

Eric Chellis's portfolio site, built with [Pelican](https://getpelican.com) and
published to GitHub Pages by GitHub Actions on every push to `main`.

Live site: https://echellis1.github.io/

## Where things are

| To change… | Edit |
|---|---|
| Home page text | `content/pages/home.md` |
| A job on the Experience page | `content/experience/<job>.md` (one file per job) |
| Education (bottom of Experience) | `content/pages/experience.md` |
| Skills | `content/pages/skills.md` |
| Contact | `content/pages/contact.md` |
| A Featured post | `content/posts/<yyyymmdd>/index.md` |
| Nav links, social links, "ON AIR" badge, share image | `pelicanconf.py` |
| Page layout / HTML | `themes/broadcast/templates/` |
| Styles | `themes/broadcast/static/css/styles.css` |
| Favicon | `themes/broadcast/static/images/favicon.svg` |
| Live site address | `publishconf.py` (`SITEURL`) |

## First-time setup in VS Code

1. Open this folder in VS Code. Accept the recommended extensions when asked.
2. **Terminal → Run Task… → Setup: create .venv and install Pelican.**
   (Needs Python 3.11 or newer: check with `python3 --version`.)
3. If VS Code asks which Python interpreter to use, pick the one in `.venv`.

## Day to day

- **Preview:** press **Ctrl+Shift+B** (runs *Pelican: Preview with live reload*),
  then open http://localhost:8000. Every time you save a file the site rebuilds;
  refresh the browser to see it. Stop it with the trash-can icon on the terminal.
- **Publish:** commit and push to `main`. GitHub Actions builds the site and
  deploys it in about a minute. Watch progress in the repo's **Actions** tab.

Don't commit `output/`. It's ignored on purpose; GitHub builds its own copy.

## Adding things

**A new post:** Terminal → Run Task… → **New post (today's date)**. It creates
`content/posts/<today>/index.md` with this header:

```
---
Title: Untitled post
Date: 2026-10-22
Summary: One line shown on the post card
Image:
Status: draft
---
```

- Drop photos in the same folder and link them with `![caption](photo.jpg)`.
- The card/cover image is `<foldername>.jpg` (e.g. `20261022.jpg`), or whatever
  file you name in `Image:`. If neither exists, the card just has no picture.
- **Delete the `Status: draft` line when it's ready to go live.** Drafts don't
  appear anywhere on the site.
- Resize photos before adding them. Around 2000 px wide is plenty; phone
  originals (3–6 MB) make pages slow on mobile.

**A new job:** add a file to `content/experience/` in the same format as the
others. Jobs sort themselves newest-first by the `*Month YYYY – Month YYYY*` line.

**Your resume:** save it as `content/images/resume.pdf`, then add this line to
the list in `content/pages/contact.md`:

```
- **Resume:** [Download PDF]({static}../images/resume.pdf)
```

**A link-preview picture for LinkedIn/Facebook:** save a 1200×630 image as
`content/images/share.jpg` and set `SOCIAL_IMAGE = "images/share.jpg"` in
`pelicanconf.py`. Posts use their own cover image automatically.

**A custom domain later:** put the domain in a file named `content/extra/CNAME`,
add `"extra/CNAME": {"path": "CNAME"}` to `EXTRA_PATH_METADATA` in
`pelicanconf.py`, change `SITEURL` in `publishconf.py`, and set the domain under
the repo's **Settings → Pages**.

## Old links

Old post links like `post.html?post=20250925` redirect to the new
`posts/20250925/` address, so anything you've already shared keeps working.
