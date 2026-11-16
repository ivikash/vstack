"""Regenerate the vstack logo SVGs. Wordmark glyphs are converted to paths, so the files need no font.

    python3 -m venv .venv && .venv/bin/pip install fonttools && .venv/bin/python make.py

Requires URW Gothic Book (urw-base35, shipped with Ghostscript on most Linux distributions).
"""
import pathlib
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = pathlib.Path(__file__).parent
FONT = "/usr/share/fonts/urw-base35/URWGothic-Book.otf"
INK, IVORY = "#141414", "#F5F2EC"
TRACK = 0.34  # letter spacing in em


def text_path(text, size):
    f = TTFont(FONT)
    gs, cmap = f.getGlyphSet(), f.getBestCmap()
    scale = size / f["head"].unitsPerEm
    d, cx = [], 0.0
    for i, ch in enumerate(text):
        g = gs[cmap[ord(ch)]]
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}")
        g.draw(TransformPen(pen, (scale, 0, 0, -scale, cx, 0)))
        d.append(pen.getCommands())
        cx += g.width * scale + (TRACK * size if i < len(text) - 1 else 0)
    return " ".join(d), cx


def svg(w, h, body, bg=None):
    rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{rect}{body}</svg>'


def chevrons(ink, sw, x, y, s):
    """Three nested hairline chevrons: a V, and a stack of three layers."""
    lines = "".join(f'<polyline points="20,{16 + i * 15.5} 50,{52 + i * 15.5} 80,{16 + i * 15.5}"/>' for i in range(3))
    return (f'<g transform="translate({x},{y}) scale({s / 100})" fill="none" stroke="{ink}" '
            f'stroke-width="{sw}" stroke-linejoin="miter" stroke-linecap="butt">{lines}</g>')


def horizontal(name, ink, bg=None, size=120):
    W, H = 1400, 480
    d, adv = text_path("VSTACK", size)
    cap = size * 0.72
    mark, gap = cap * 1.55, size * 0.55
    x0, cy = (W - (mark + gap + adv)) / 2, H / 2
    body = chevrons(ink, 2.6, x0, cy - mark / 2, mark) + \
        f'<path d="{d}" fill="{ink}" transform="translate({x0 + mark + gap},{cy + cap / 2})"/>'
    (HERE / f"{name}.svg").write_text(svg(W, H, body, bg))


def stacked(name, ink, bg=None, size=96):
    W, H = 900, 700
    d, adv = text_path("VSTACK", size)
    cap, mark, gap = size * 0.72, 240, 80
    y0 = (H - (mark + gap + cap)) / 2
    body = chevrons(ink, 2.4, (W - mark) / 2, y0, mark) + \
        f'<path d="{d}" fill="{ink}" transform="translate({(W - adv) / 2},{y0 + mark + gap + cap})"/>'
    (HERE / f"{name}.svg").write_text(svg(W, H, body, bg))


def mark(name, ink, bg=None):
    (HERE / f"{name}.svg").write_text(svg(512, 512, chevrons(ink, 2.6, 0, 0, 512), bg))


if __name__ == "__main__":
    horizontal("vstack-logo", INK)            # light backgrounds
    horizontal("vstack-logo-dark", IVORY)     # dark backgrounds
    stacked("vstack-logo-stacked", INK, IVORY)
    stacked("vstack-logo-stacked-ink", IVORY, INK)
    mark("vstack-mark", INK)
    mark("vstack-mark-ink", IVORY, INK)
