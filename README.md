# RADAR overview

RADAR's documentation website: a start page and 18 project documents, with local fonts, diagrams and three source PDFs. Built with Python's standard library; no packages need to be installed.

Website: **https://wsu-radar.github.io/overview/** (available once GitHub Pages is enabled and the first deployment succeeds).

## Run locally

From this repository:

```sh
RADAR_OUT=_site python3 _source/src/build.py
python3 scripts/check_site.py _site
python3 -m http.server 8000 --bind 127.0.0.1 --directory _site
```

Open http://localhost:8000/. Stop the server with Ctrl+C.

Edit document content and diagrams in `_source/src/`; see [_source/README.md](_source/README.md). Styles, fonts and downloadable source PDFs live in `assets/`. Build into `_site` for deployment, or use `RADAR_OUT=.` to refresh the checked-in HTML pages.

## Git flow

- `main`: published version. A successful push builds, checks and deploys the site.
- `develop`: integration branch. Pushes build and check the site.
- `feature/*`: branch from `develop`; open a pull request back to `develop`.
- `release/*`: branch from `develop`; merge into `main` and back into `develop`, then tag the release as `vX.Y.Z`.
- `hotfix/*`: branch from `main`; merge into both `main` and `develop`, then tag the fix.

To use the optional git-flow command-line extension in a fresh clone, run `git flow init -d`. The same branches and pull requests work with normal Git commands.

```sh
git switch develop
git pull --ff-only
git switch -c feature/document-update
# Edit and rebuild; commit and push the feature branch.
git push -u origin feature/document-update
# Open a pull request into develop, then release into main when ready.
```

## GitHub Pages

In repository **Settings → Pages → Build and deployment**, select **GitHub Actions**. The workflow is [`.github/workflows/pages.yml`](.github/workflows/pages.yml). It builds from source into `_site`, checks every internal page link and anchor plus CSS/font/PDF paths, and uploads only the generated website. Pull requests and `develop` validate without publishing; only `main` can deploy. A manual run on `main` can republish the website.

The organization currently uses GitHub Free, which requires a public repository for Pages. Keeping the repository private requires a plan that supports Pages for private repositories. The website includes the draft working documents and the linked proposal, stage-gate paper and project deck; these files are accessible to anyone who can view the published site.
