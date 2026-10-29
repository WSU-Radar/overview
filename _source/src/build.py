"""Assemble the RADAR documentation site from content fragments + figures."""
import os, re, sys, html, urllib.parse, shutil
sys.path.insert(0, os.path.dirname(__file__))
from docs import DOCS, TRACKS, AUD, EDGES, READING_PATHS, by_n
from figures import FIGS
import figures2  # noqa
import figures3  # noqa

B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = f"{B}/src/content"
OUT = os.path.abspath(os.environ.get("RADAR_OUT", f"{B}/site"))
VERSION = "Draft v0.1"
DATE = "29 October 2026"

SOURCES = [
    ("INV-110654 Investment Document (proposal)", "assets/source-documents/INV110654_2026_WSU Kenya_Proposal_Investment_Document_WSUCleared (1).pdf"),
    ("Proposed Milestone-Based Stage Gates", "assets/source-documents/RADAR_Stage_Gates_Proposed_WSURevClean.pdf"),
    ("RADAR slide deck", "assets/source-documents/PowerPoint Presentation.pdf"),
]

esc = html.escape


def slugify(t):
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"[^a-zA-Z0-9]+", "-", t.lower()).strip("-")
    return t[:60]


def figure_html(name):
    fn, cap, wide = FIGS[name]
    cls = "fig wide" if wide else "fig"
    return f'<figure class="{cls}" id="fig-{name}">\n{fn().svg()}\n<figcaption>{cap}</figcaption>\n</figure>'


def parse_fragment(text):
    parts = re.split(r"<!--\s*(inshort|why|body|sources)\s*-->", text)
    out = {}
    for i in range(1, len(parts), 2):
        out[parts[i]] = parts[i + 1].strip()
    return out


def number_sections(body):
    toc = []
    n = 0

    def rep(m):
        nonlocal n
        attrs, inner = m.group(1) or "", m.group(2)
        n += 1
        sid = slugify(inner)
        toc.append((sid, re.sub(r"<[^>]+>", "", inner)))
        return f'<h2 id="{sid}"{attrs}><span class="sec">{n}</span>{inner}</h2>'

    body = re.sub(r"<h2([^>]*)>(.*?)</h2>", rep, body)
    return body, toc


def nav_html(cur):
    groups = []
    for tk, (tname, col, _) in TRACKS.items():
        items = [d for d in DOCS if d["track"] == tk]
        cur_attr = ' aria-current="page"'
        lis = "".join(
            f'<li><a href="{d["slug"]}.html"{cur_attr if d["n"] == cur else ""}><span class="n">{d["n"]}</span><span>{esc(d["short"])}</span></a></li>'
            for d in items)
        groups.append(f'<div class="navgroup"><h4><i style="background:{col}"></i>{esc(tname)}</h4><ul>{lis}</ul></div>')
    return ('<nav class="sidenav" aria-label="All documents"><details open><summary>All documents</summary>'
            f'<div class="navgroups">{"".join(groups)}</div></details></nav>')


def connections_html(n):
    ins = [(a, why) for a, b, why in EDGES if b == n and a != "18"]
    outs = [(b, why) for a, b, why in EDGES if a == n]
    def item(m, why):
        d = by_n(m)
        return f'<a class="conn" href="{d["slug"]}.html"><span class="t">{d["n"]} · {esc(d["short"])}</span><span class="r">{esc(why)}</span></a>'
    if ins:
        left = "".join(item(m, w) for m, w in ins)
    else:
        left = "".join(f'<a class="conn" href="{urllib.parse.quote(f)}"><span class="t">{esc(t)}</span><span class="r">Source document in the _docs folder</span></a>' for t, f in SOURCES)
    if n == "18":
        right = '<span class="conn"><span class="t">Every document</span><span class="r">Shared vocabulary and the full source list.</span></span>'
    elif outs:
        right = "".join(item(m, w) for m, w in outs)
    else:
        right = '<span class="conn"><span class="r">—</span></span>'
    return ('<section class="connections" aria-label="How this document connects"><h3>How this document connects</h3>'
            f'<div class="conn-grid"><div class="conn-col"><h4>← Builds on</h4>{left}</div>'
            f'<div class="conn-col"><h4>Informs →</h4>{right}</div></div></section>')


def shell(d, title, main_html, description):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="stylesheet" href="assets/radar.css">
</head>
<body>
<header class="topbar">
  <div class="topbar-inner">
    <a class="brand" href="index.html"><span class="inst">Washington State University · Global Health – Kenya</span><span class="prog">RADAR Documentation</span></a>
    <div class="meta"><strong>INV-110654</strong> · {VERSION} · {DATE}</div>
  </div>
</header>
<div class="layout">
{nav_html(d["n"])}
<main id="main">
<article class="doc">
{main_html}
<footer class="foot"><span>RADAR — Real-Time AI-Driven Alert &amp; Response System · WSU Global Health – Kenya with KNPHI and partners</span><span>{VERSION} · prepared {DATE} · internal working document</span></footer>
</article>
</main>
</div>
<script>if (window.matchMedia("(max-width: 980px)").matches) {{ var d = document.querySelector(".sidenav details"); if (d) d.open = false; }}</script>
</body>
</html>
'''


def pager(d):
    i = DOCS.index(d)
    prev_ = DOCS[i - 1] if i > 0 else None
    next_ = DOCS[i + 1] if i < len(DOCS) - 1 else None
    s = '<nav class="pager" aria-label="Previous and next document">'
    if prev_:
        s += f'<a class="prev" href="{prev_["slug"]}.html"><span class="d">← Previous</span><br><span class="t">{prev_["n"]} · {esc(prev_["short"])}</span></a>'
    if next_:
        s += f'<a class="next" href="{next_["slug"]}.html"><span class="d">Next →</span><br><span class="t">{next_["n"]} · {esc(next_["short"])}</span></a>'
    return s + "</nav>"


def header_html(d):
    tname, col, _ = TRACKS[d["track"]]
    chips = "".join(f'<span class="chip">{esc(AUD[a])}</span>' for a in d["aud"])
    return (f'<div class="eyebrow"><span class="num">Doc {d["n"]}</span><span>·</span>'
            f'<span class="track"><i style="background:{col}"></i>{esc(tname)}</span></div>'
            f'<h1>{esc(d["title"])}</h1><p class="lede">{esc(d["summary"])}</p>'
            f'<div class="docmeta"><span><b>For:</b> {chips}</span><span><b>Status:</b> {VERSION}</span><span><b>Updated:</b> {DATE}</span></div>')


LEGEND = ('<p class="legend-tags">Labels used in this document: <span class="tag prop">Proposal</span> stated in the funded proposal, '
          'stage-gate paper or deck · <span class="tag res">Research</span> external evidence (see Sources) · '
          '<span class="tag rec">Recommended</span> proposed design choice, to be confirmed · '
          '<span class="tag open">Open</span> decision still needed</p>')


def build_doc(d):
    path = f"{SRC}/{d['slug']}.html"
    frag = parse_fragment(open(path, encoding="utf-8").read())
    body = frag.get("body", "")
    body = re.sub(r"<!--fig:([a-z0-9-]+)-->", lambda m: figure_html(m.group(1)), body)
    body, toc = number_sections(body)
    srcs = frag.get("sources", "")
    toc_html = "".join(f'<li><a href="#{sid}">{esc(t)}</a></li>' for sid, t in toc)
    if srcs:
        toc_html += '<li><a href="#sources">Sources</a></li>'
    main = header_html(d)
    main += ('<div class="summary">'
             f'<div class="box inshort"><h3>In short</h3>{frag.get("inshort", "")}</div>'
             f'<div class="box why"><h3>Why it matters</h3>{frag.get("why", "")}</div></div>')
    main += connections_html(d["n"])
    main += f'<nav class="toc" aria-label="On this page"><b>On this page</b><ol>{toc_html}</ol></nav>'
    main += LEGEND
    main += body
    if srcs:
        main += f'<h2 id="sources">Sources</h2><div class="sources">{srcs}</div>'
    main += pager(d)
    title = f'{d["n"]} · {d["title"]} — RADAR'
    return shell(d, title, main, d["summary"])


def build_hub():
    d = by_n("00")
    frag = parse_fragment(open(f"{SRC}/00-start-here.html", encoding="utf-8").read())
    body = frag.get("body", "")
    body = re.sub(r"<!--fig:([a-z0-9-]+)-->", lambda m: figure_html(m.group(1)), body)
    # track cards
    cards = []
    for tk, (tname, col, blurb) in TRACKS.items():
        items = [x for x in DOCS if x["track"] == tk and x["n"] != "00"]
        if not items:
            continue
        links = "".join(f'<a class="doclink" href="{x["slug"]}.html"><span class="n">{x["n"]}</span><span><span class="t">{esc(x["title"])}</span><span class="s">{esc(x["summary"])}</span></span></a>' for x in items)
        cards.append(f'<div class="trackcard" style="border-top-color:{col}"><h3>{esc(tname)}</h3><p>{esc(blurb)}</p>{links}</div>')
    body = body.replace("<!--trackcards-->", f'<div class="hub-tracks">{"".join(cards)}</div>')
    paths = []
    for name, blurb, seq in READING_PATHS:
        links = "".join(f'<a href="{by_n(n)["slug"]}.html" title="{esc(by_n(n)["title"])}">{n}</a>' for n in seq)
        names = " → ".join(by_n(n)["short"] for n in seq)
        paths.append(f'<div class="path"><h4>{esc(name)}</h4><p>{esc(blurb)}</p><div class="seq">{links}</div><p style="margin-top:6px">{esc(names)}</p></div>')
    body = body.replace("<!--paths-->", f'<div class="paths">{"".join(paths)}</div>')
    srcs = "".join(f'<li><a href="{urllib.parse.quote(f)}">{esc(t)}</a></li>' for t, f in SOURCES)
    body = body.replace("<!--sourcefiles-->", f"<ul>{srcs}</ul>")
    # relationship matrix
    rows = []
    for x in DOCS:
        if x["n"] == "00":
            continue
        outs = [b for a, b, _ in EDGES if a == x["n"]]
        ins = [a for a, b, _ in EDGES if b == x["n"] and a != "18"]
        fmt = lambda L: ", ".join(f'<a href="{by_n(m)["slug"]}.html">{m}</a>' for m in L) or "—"
        rows.append(f'<tr><td><a href="{x["slug"]}.html"><b>{x["n"]}</b> {esc(x["short"])}</a></td><td>{fmt(ins)}</td><td>{fmt(outs)}</td></tr>')
    body = body.replace("<!--matrix-->", '<div class="table-wrap"><table><thead><tr><th>Document</th><th>Builds on</th><th>Informs</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table></div>")
    body, toc = number_sections(body)
    toc_html = "".join(f'<li><a href="#{sid}">{esc(t)}</a></li>' for sid, t in toc)
    main = header_html(d)
    main += ('<div class="summary">'
             f'<div class="box inshort"><h3>In short</h3>{frag.get("inshort", "")}</div>'
             f'<div class="box why"><h3>Why it matters</h3>{frag.get("why", "")}</div></div>')
    main += f'<nav class="toc" aria-label="On this page"><b>On this page</b><ol>{toc_html}</ol></nav>'
    main += body + pager(d)
    return shell(d, "RADAR Documentation — Start Here", main, d["summary"])


def main():
    os.makedirs(OUT, exist_ok=True)
    assets = os.path.join(os.path.dirname(B), "assets")
    destination = os.path.join(OUT, "assets")
    if os.path.realpath(assets) != os.path.realpath(destination):
        shutil.copytree(assets, destination, dirs_exist_ok=True)
    only = sys.argv[1:]
    built = []
    for d in DOCS:
        if only and d["n"] not in only:
            continue
        p = f"{SRC}/{d.get('src', d['slug'])}.html"
        if not os.path.exists(p):
            raise FileNotFoundError(p)
        out = build_hub() if d["n"] == "00" else build_doc(d)
        with open(f"{OUT}/{d['slug']}.html", "w", encoding="utf-8") as f:
            f.write(out)
        built.append(d["n"])
    print("built", built)


if __name__ == "__main__":
    main()
