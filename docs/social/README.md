# Social posters

Four 1200x1500 (2x: 2400x3000) field-note posters about the kernel, generated from HTML/SVG
with a headless Chromium and checked by an in-page validator for text overlaps, edge
crossings, edges through boxes and clipped text.

```bash
cd docs/social && python3 poster1.py && python3 poster2.py
node render.mjs poster1.html seven-stage-cell.png        # needs playwright-core and a Chromium
node render.mjs poster2.html one-graph-four-harnesses.png
node render.mjs poster3.html manager-metro-map.png
node render.mjs poster4.html kernel-clock.png
```

Fonts (Playfair Display, Caveat, IBM Plex Mono, Inter, Syne, JetBrains Mono, Space Grotesk) are fetched from google/fonts into
`fonts/` and are not committed. Post copy with Unicode bold lives in `POSTS.md`.
