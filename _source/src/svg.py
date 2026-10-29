"""Tiny inline-SVG diagram helper for the RADAR docs.

Hand-authored native shapes only (rect, line, polyline, polygon, circle, text).
Strokes/text use currentColor so diagrams inherit the page ink; crimson marks emphasis.
"""
import html
import math

CRIMSON = "#A60F2D"
GRAY = "#4D4D4D"
INK = "currentColor"
MUTED = "#5A5A5A"
LINE = "#9A9A9A"
SOFT = "#EBEBEB"
PANEL = "#F4F4F4"
WHITE = "#FFFFFF"
MIDNIGHT = "#002D61"
SKY = "#5BC3F5"
AUTUMN = "#E16727"
VINE = "#AADC24"
GOLD = "#F3E700"


def esc(s):
    return html.escape(str(s), quote=True)


def text_width(s, size, bold=False):
    # Montserrat is a wide geometric sans; these factors were tuned by eye.
    f = 0.64 if bold else 0.6
    w = 0
    for ch in str(s):
        if ch in "il.,:;'|!I ":
            w += 0.32
        elif ch in "mwMW":
            w += 0.9
        elif ch.isupper():
            w += 0.72 if bold else 0.68
        elif ch.isdigit():
            w += 0.62
        else:
            w += f
    return w * size


def wrap(s, max_px, size, bold=False):
    words = str(s).split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if not cur or text_width(trial, size, bold) <= max_px:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


class Box:
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

    @property
    def cx(self):
        return self.x + self.w / 2

    @property
    def cy(self):
        return self.y + self.h / 2

    def l(self, dy=0):
        return (self.x, self.cy + dy)

    def r(self, dy=0):
        return (self.x + self.w, self.cy + dy)

    def t(self, dx=0):
        return (self.cx + dx, self.y)

    def b(self, dx=0):
        return (self.cx + dx, self.y + self.h)


STYLES = {
    # fill, stroke, stroke-width, title color, sub color, dash
    "plain": (WHITE, LINE, 1.2, INK, MUTED, None),
    "soft": (PANEL, PANEL, 1, INK, MUTED, None),
    "accent": (WHITE, CRIMSON, 2, CRIMSON, MUTED, None),
    "solid": (CRIMSON, CRIMSON, 1, WHITE, "#F2D6DC", None),
    "dark": (GRAY, GRAY, 1, WHITE, "#E6E6E6", None),
    "midnight": (MIDNIGHT, MIDNIGHT, 1, WHITE, "#D5DEEA", None),
    "dashed": (WHITE, LINE, 1.2, INK, MUTED, "5 4"),
    "ghost": ("none", LINE, 1.2, MUTED, MUTED, "4 4"),
    "line": (WHITE, SOFT, 1, INK, MUTED, None),
}


class Diagram:
    def __init__(self, w, h, label):
        self.w, self.h, self.label = w, h, label
        self.back = []   # zones / lanes
        self.mid = []    # arrows
        self.front = []  # boxes & text

    # ---------- primitives ----------
    def rect(self, x, y, w, h, fill=WHITE, stroke=LINE, sw=1, rx=6, dash=None, layer="front", opacity=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' opacity="{opacity}"' if opacity is not None else ""
        el = f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{o}/>'
        getattr(self, layer).append(el)

    def text(self, x, y, s, size=12, weight=400, anchor="start", fill=INK, italic=False, layer="front", halo=False, ls=None):
        it = ' font-style="italic"' if italic else ""
        h = ' stroke="#FFFFFF" stroke-width="5" stroke-linejoin="round" paint-order="stroke"' if halo else ""
        l = f' letter-spacing="{ls}"' if ls else ""
        el = (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" '
              f'dominant-baseline="middle" fill="{fill}"{it}{h}{l}>{esc(s)}</text>')
        getattr(self, layer).append(el)

    def lines(self, x, y, rows, size=12, weight=400, anchor="start", fill=INK, lh=None, layer="front", italic=False):
        lh = lh or size * 1.35
        for i, r in enumerate(rows):
            self.text(x, y + i * lh, r, size, weight, anchor, fill, layer=layer, italic=italic)

    def line(self, x1, y1, x2, y2, stroke=LINE, sw=1, dash=None, layer="mid"):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        getattr(self, layer).append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def circle(self, cx, cy, r, fill=WHITE, stroke=LINE, sw=1.2, layer="front"):
        getattr(self, layer).append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def poly(self, pts, fill=WHITE, stroke=LINE, sw=1, layer="front"):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        getattr(self, layer).append(f'<polygon points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    # ---------- composites ----------
    def box(self, x, y, w, h, title=None, sub=None, style="plain", ts=13, ss=11.5, align="center",
            stripe=None, pad=12, rx=6, tw=700, badge=None, href=None):
        start = len(self.front)
        b = self._box(x, y, w, h, title, sub, style, ts, ss, align, stripe, pad, rx, tw, badge)
        if href:
            inner = "".join(self.front[start:])
            self.front[start:] = [f'<a href="{esc(href)}"><title>{esc((title or "") + " — open document")}</title>{inner}</a>']
        return b

    def _box(self, x, y, w, h, title, sub, style, ts, ss, align, stripe, pad, rx, tw, badge):
        fill, stroke, sw, tc, sc, dash = STYLES[style]
        self.rect(x, y, w, h, fill, stroke, sw, rx, dash)
        if stripe:
            self.front.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="5" height="{h:.1f}" rx="2" fill="{stripe}"/>')
        inner = w - 2 * pad - (6 if stripe else 0)
        tl = wrap(title, inner, ts, True) if title else []
        sl = wrap(sub, inner, ss) if sub else []
        th, sh = ts * 1.28, ss * 1.38
        total = len(tl) * th + (6 if tl and sl else 0) + len(sl) * sh
        cy0 = y + h / 2 - total / 2
        if align == "center":
            ax, anchor = x + w / 2 + (3 if stripe else 0), "middle"
        else:
            ax, anchor = x + pad + (6 if stripe else 0), "start"
        yy = cy0 + th / 2
        for r in tl:
            self.text(ax, yy, r, ts, tw, anchor, tc)
            yy += th
        if sl:
            yy += 6 - th / 2 + sh / 2
            for r in sl:
                self.text(ax, yy, r, ss, 400, anchor, sc)
                yy += sh
        if badge:
            bw = text_width(badge, 10, True) + 14
            self.rect(x + w - bw - 6, y - 9, bw, 18, CRIMSON, CRIMSON, 1, 9)
            self.text(x + w - bw / 2 - 6, y, badge, 10, 700, "middle", WHITE)
        return Box(x, y, w, h)

    def zone(self, x, y, w, h, label=None, fill=PANEL, stroke="none", dash=None, lsize=11, lcolor=MUTED, rx=8, label_pos="tl"):
        self.rect(x, y, w, h, fill, stroke if stroke != "none" else fill, 1, rx, dash, layer="back")
        if label:
            if label_pos == "tl":
                self.text(x + 12, y + 14, label.upper(), lsize, 700, "start", lcolor, layer="back", ls="0.08em")
            elif label_pos == "tc":
                self.text(x + w / 2, y + 14, label.upper(), lsize, 700, "middle", lcolor, layer="back", ls="0.08em")
        return Box(x, y, w, h)

    def arrow(self, pts, label=None, style="solid", head="end", lpos=None, lsize=10.5, lcolor=None, sw=1.4, loff=(0, 0), lanchor="middle"):
        color = {"solid": GRAY, "accent": CRIMSON, "muted": LINE, "dashed": GRAY, "dashacc": CRIMSON, "midnight": MIDNIGHT}[style]
        dash = ' stroke-dasharray="5 4"' if style in ("dashed", "dashacc") else ""
        w = 2 if style in ("accent", "dashacc") else sw
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.mid.append(f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="{w}"{dash} stroke-linejoin="round"/>')

        def headat(a, b):
            ang = math.atan2(b[1] - a[1], b[0] - a[0])
            L, W = 8, 4.5
            tip = b
            p1 = (b[0] - L * math.cos(ang) + W * math.sin(ang), b[1] - L * math.sin(ang) - W * math.cos(ang))
            p2 = (b[0] - L * math.cos(ang) - W * math.sin(ang), b[1] - L * math.sin(ang) + W * math.cos(ang))
            self.mid.append(f'<polygon points="{tip[0]:.1f},{tip[1]:.1f} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{color}"/>')

        if head in ("end", "both"):
            headat(pts[-2], pts[-1])
        if head in ("start", "both"):
            headat(pts[1], pts[0])
        if label:
            if lpos is None:
                # midpoint of longest segment
                best, bi = -1, 0
                for i in range(len(pts) - 1):
                    d = math.dist(pts[i], pts[i + 1])
                    if d > best:
                        best, bi = d, i
                a, b = pts[bi], pts[bi + 1]
                lx, ly = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            else:
                lx, ly = lpos
            lx += loff[0]
            ly += loff[1]
            rows = label.split("\n")
            for i, r in enumerate(rows):
                self.text(lx, ly + (i - (len(rows) - 1) / 2) * lsize * 1.3, r, lsize, 600, lanchor,
                          lcolor or (CRIMSON if style in ("accent", "dashacc") else MUTED), halo=True)

    def pill(self, x, y, s, fill=CRIMSON, color=WHITE, size=10.5, anchor="middle", padx=9, h=20):
        w = text_width(s, size, True) + 2 * padx
        x0 = x - w / 2 if anchor == "middle" else x
        self.rect(x0, y - h / 2, w, h, fill, fill, 1, h / 2)
        self.text(x0 + w / 2, y + 0.5, s, size, 700, "middle", color)
        return Box(x0, y - h / 2, w, h)

    def num(self, cx, cy, n, r=11, fill=CRIMSON, color=WHITE, size=11):
        self.circle(cx, cy, r, fill, fill, 1)
        self.text(cx, cy + 0.5, str(n), size, 700, "middle", color)

    def raw(self, el, layer="front"):
        getattr(self, layer).append(el)

    def vtext(self, x, y, s, size=11, weight=700, fill=MUTED, ls=None):
        l = f' letter-spacing="{ls}"' if ls else ""
        self.front.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" text-anchor="middle" '
                          f'dominant-baseline="middle" fill="{fill}" transform="rotate(-90 {x:.1f} {y:.1f})"{l}>{esc(s)}</text>')

    def svg(self):
        body = "\n".join(self.back + self.mid + self.front)
        return (f'<svg viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{esc(self.label)}" '
                f'xmlns="http://www.w3.org/2000/svg">\n{body}\n</svg>')
