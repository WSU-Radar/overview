# RADAR documentation — source

The HTML pages at the repository root are generated from these files. All updates to the documentation are made here and rebuilt. Edit here, then rebuild.

- `src/content/NN-*.html` — the text of each document (sections marked `<!--inshort-->`, `<!--why-->`, `<!--body-->`, `<!--sources-->`; `<!--fig:name-->` inserts a diagram).
- `src/docs.py` — document titles, tracks, audiences, reading paths and the "builds on / informs" links between documents.
- `src/figures*.py` + `src/svg.py` — every diagram, drawn as inline SVG in WSU colours.
- `src/build.py` — assembles the pages.

Rebuild (Python 3, no extra packages), from this `_source` folder:

    RADAR_OUT=.. python3 src/build.py

Styles live in `assets/radar.css` at the repository root (WSU Crimson #A60F2D, Gray #4D4D4D, Montserrat). The three linked source PDFs are bundled in `assets/source-documents/`.

For an isolated build, run `RADAR_OUT=_site python3 _source/src/build.py` from the repository root. The builder creates the output directory and copies assets. Then run `python3 scripts/check_site.py _site` to check every page and local link. GitHub Actions uses these same commands before publishing `main` to Pages.
