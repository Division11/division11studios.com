# division11studios.com

Official website of **Division 11 Studios** (Division Eleven Studios – Custom Software Design and Development, S.P.C.), served by GitHub Pages at https://www.division11studios.com.

## How it works

- `build.py` generates every page into `_site/` (Python 3, no dependencies). Company details and app listings live in the `CO` and `APPS` data at the top.
- `site.css` is the shared stylesheet (the brand pattern is embedded in it).
- `brand/` holds the approved D11 logo SVGs; `policies/` holds each app's privacy policy, published at `/<app>/privacy/`.
- `app-ads.txt` is published at the site root for AdMob / LevelPlay seller verification.
- `.github/workflows/pages.yml` builds and deploys on every push to `main`.

Preview locally: `python3 build.py && python3 -m http.server -d _site 8000`.
