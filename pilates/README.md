# Olea Pilates (concept site)

A scroll-scrubbed, photoreal walk-in of a fictional reformer Pilates studio:
outside the arch → through the door → down the aisle → slow turn to reformer 3 → book.

## How the film is made

1. `render.html` (built from `src/scene.js` + `src/render-entry.js`) is the studio modelled in Three.js.
   The room is real 3D, so the camera path is exact and nothing can morph.
   Textures in `tex/` and the olive tree in `models/` were generated with Higgsfield.
2. A headless browser renders the camera move to video (portrait 720×1280 and landscape 1280×720, 14 s).
3. Higgsfield **FLUX 3 Video Edit** turns each video photoreal while keeping the camera move.
4. `frames.sh` cuts the results into 169 WebP frames per orientation (`frames/p`, `frames/l`).
5. The page (`src/main.js` + `src/film.js`) draws the frame that matches the scroll position.

## Build

`npm i lenis@1.1.13 three@0.160.0 esbuild@0.24.0 @fontsource-variable/bricolage-grotesque@5.1.0 @fontsource/instrument-sans@5.1.0`
in any folder, then `NODE_PATH=<that folder>/node_modules node build.mjs`.
Serve the folder from a web server (e.g. GitHub Pages) and open `index.html`.
