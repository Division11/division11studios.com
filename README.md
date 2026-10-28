# division11studios.com

Official website of **Division 11 Studios** (Division Eleven Studios – Custom Software Design and Development, S.P.C.), served by GitHub Pages at https://www.division11studios.com.

## How it works

- `build.py` generates every page into `_site/` (Python 3, no dependencies). All visible text lives in the `T` (site) and `APPS` (per-app) tables, keyed by language.
- Languages: English at `/`, Arabic at `/ar/`. To add one, add it to `LANGS` and give it a block in `T` and in each app's `text`; missing strings fall back to English.
- Light and dark themes follow the visitor's system setting, with a toggle in the header (system → light → dark).
- App icons live in `brand/apps/`.
- `site.css` is the shared stylesheet (the brand pattern is embedded in it).
- `brand/` holds the approved D11 logo SVGs; `policies/` holds each app's privacy policy, published at `/<app>/privacy/`.
- `app-ads.txt` is published at the site root for AdMob / LevelPlay seller verification.
- `.github/workflows/pages.yml` builds and deploys on every push to `main`.

Preview locally: `python3 build.py && python3 -m http.server -d _site 8000`.
