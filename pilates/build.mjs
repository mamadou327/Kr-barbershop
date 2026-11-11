// Builds pilates/index.html (full page) and dist/artifact.html (fragment for claude.ai artifacts).
// Usage: NODE_PATH=<dir with node_modules> node build.mjs
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { createRequire } from 'node:module';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const req = createRequire(join(process.env.NODE_PATH || here, 'x.js'));
const esbuild = req('esbuild');

const out = await esbuild.build({
  entryPoints: [join(here, 'src/main.js')], bundle: true, minify: true, format: 'iife', write: false,
  target: ['es2020', 'safari15'], nodePaths: [process.env.NODE_PATH || ''], legalComments: 'none',
});
const js = out.outputFiles[0].text.replace(/<\/script/gi, '<\\/script');

const font = (pkg, file) => readFileSync(join(dirname(req.resolve(`${pkg}/package.json`)), 'files', file)).toString('base64');
const fonts = `
@font-face{font-family:"Bricolage Grotesque Variable";font-style:normal;font-display:swap;font-weight:200 800;src:url(data:font/woff2;base64,${font('@fontsource-variable/bricolage-grotesque', 'bricolage-grotesque-latin-wght-normal.woff2')}) format("woff2-variations")}
@font-face{font-family:"Instrument Sans";font-style:normal;font-display:swap;font-weight:400;src:url(data:font/woff2;base64,${font('@fontsource/instrument-sans', 'instrument-sans-latin-400-normal.woff2')}) format("woff2")}
@font-face{font-family:"Instrument Sans";font-style:normal;font-display:swap;font-weight:500;src:url(data:font/woff2;base64,${font('@fontsource/instrument-sans', 'instrument-sans-latin-500-normal.woff2')}) format("woff2")}
@font-face{font-family:"Instrument Sans";font-style:normal;font-display:swap;font-weight:600;src:url(data:font/woff2;base64,${font('@fontsource/instrument-sans', 'instrument-sans-latin-600-normal.woff2')}) format("woff2")}`;

const body = readFileSync(join(here, 'src/template.html'), 'utf8')
  .replace('/*FONTS*/', () => fonts)
  .replace('<!--APP-->', () => `<script>${js}</script>`);

const full = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
${body.slice(0, body.indexOf('<header class="top">'))}</head>
<body>
${body.slice(body.indexOf('<header class="top">'))}
</body>
</html>
`;
writeFileSync(join(here, 'index.html'), full);
mkdirSync(join(here, 'dist'), { recursive: true });
writeFileSync(join(here, 'dist/artifact.html'), body);
console.log('built', (full.length / 1024).toFixed(0) + ' KB');
