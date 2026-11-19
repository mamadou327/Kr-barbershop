// Render-only page: draws the 3D studio at a given path progress for video export.
import { createStudio } from './scene.js';
const canvas = document.getElementById('scene');
const studio = createStudio(canvas, { isMobile: false, exporting: true, onReady: () => document.documentElement.classList.add('ready') });
studio.setVoid('#e3d8c8');
studio.resize(innerWidth, innerHeight);
window.__frame = (p, t) => { studio.render(p, t, false); return canvas.toDataURL('image/jpeg', 0.92); };
