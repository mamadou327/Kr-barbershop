# Olea Pilates (concept site)

A scroll-driven, real-time 3D walk-through of a fictional reformer Pilates studio:
overview from above → through the arched door → down the aisle → reformer 3 → book.

- `src/scene.js`: the Three.js room (built in code, so nothing morphs).
- `src/main.js`: scroll, chapters, booking widget.
- `src/template.html`: page, styles and copy.
- `tex/`: wall, floor, rug, wood and leather textures generated with Higgsfield.
- `models/olive.json`: olive tree, Higgsfield image → 3D model (compressed).
- `index.html`: the built page (open it from a web server, e.g. GitHub Pages).

Build: `npm i three@0.160.0 lenis@1.1.13 esbuild@0.24.0 @fontsource-variable/bricolage-grotesque@5.1.0 @fontsource/instrument-sans@5.1.0`
in any folder, then `NODE_PATH=<that folder>/node_modules node build.mjs`.
