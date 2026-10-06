# games.whizkidworld.in

The public site of Whizkid World LLP: each game's page, privacy policy and data-deletion page,
and the shared `app-ads.txt`. Plain HTML and one stylesheet. There is no build step, no
JavaScript, no CDN and no webfont: a privacy policy that fetches a font from a third party while
explaining what it collects is not a good look.

Hosted on **GitHub Pages** from this repository (`whizkidworld` organisation, free plan, so the
repository has to be public; it holds only what the site shows anyway). Decided by the owner
2026-10-06, replacing the earlier Vercel plan, because Vercel's free plan excludes commercial
use. Served at **`games.whizkidworld.in`**. DNS stays at GoDaddy, and the only record that points here
is the `games` CNAME. The bare domain, `www` and every other record (school portals, payments,
email) belong to other systems and must not be touched from here. The domain is verified for the
organisation by the TXT record `_github-pages-challenge-whizkidworld`; keep it.

## Rules

- **Published URLs are permanent.** They are declared in Play Console and built into the apps:
  `/sudoku/privacy/` (with its `#deleting` anchor), `/sudoku/delete-data/`,
  `/mindthetop/privacy/`, `/app-ads.txt`. Never move or rename them.
- **`app-ads.txt` stays at the site root and is never emptied.** AdMob finds it because each
  Play listing's website is `https://games.whizkidworld.in`. An empty file tells buyers to refuse
  the publisher's inventory, which is worse than no file.
- **Each game's pages are owned by that game's repository**, which holds the source text and
  the guard tests that check it against the code. Change the text there first, then copy it here.
  - Sudoku: `docs/PRIVACY_POLICY.md` in `nitishbarbaria/Sudoku`.
  - Mind the Top: `site/` in `nitishbarbaria/Puzzle_Match`, the copy this site was seeded from.
- **Nothing here may take payments or show ads.** GitHub Pages' terms exclude sites mainly
  for commercial transactions; information pages for free apps are what it is for.

## Checking it locally

```sh
python -m http.server 8000
```

Then open `http://localhost:8000/sudoku/`. Root-relative paths (`/style.css`) need the server
root at this folder.
