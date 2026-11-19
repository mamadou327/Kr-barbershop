// Scroll-scrubbed photoreal film: draws pre-rendered frames to a canvas (cover fit).
// Portrait screens use frames/p, wider screens use frames/l.
export function createFilm(canvas, { count, onProgress, onReady }) {
  const ctx = canvas.getContext('2d', { alpha: false });
  const sets = {};
  let set = null, W = 1, H = 1, last = -1, dpr = Math.min(window.devicePixelRatio || 1, 2);

  function load(kind) {
    if (sets[kind]) return sets[kind];
    const imgs = new Array(count), done = new Uint8Array(count);
    const s = sets[kind] = { imgs, done, n: 0 };
    // load a coarse pass first so scrubbing works early, then fill the gaps
    const order = [];
    for (const step of [16, 8, 4, 2, 1]) for (let i = 0; i < count; i += step) if (!order.includes(i)) order.push(i);
    let next = 0, active = 0;
    const pump = () => {
      while (active < 6 && next < order.length) {
        const i = order[next++]; active++;
        const im = new Image(); im.decoding = 'async';
        im.onload = () => (im.decode ? im.decode().catch(() => {}) : Promise.resolve()).then(() => { done[i] = 1; s.n++; active--; if (set === s) { onProgress && onProgress(s.n / count); if (i === 0) { onReady && onReady(); } last = -1; } pump(); });
        im.onerror = () => { active--; pump(); };
        im.src = `frames/${kind}/${String(i).padStart(3, '0')}.webp`;
        imgs[i] = im;
      }
    };
    pump();
    return s;
  }

  function resize(w, h) {
    W = w; H = h;
    canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
    set = load(w / h < 0.9 ? 'p' : 'l'); last = -1;
  }

  function nearest(i) {
    if (set.done[i]) return i;
    for (let d = 1; d < count; d++) { if (i - d >= 0 && set.done[i - d]) return i - d; if (i + d < count && set.done[i + d]) return i + d; }
    return -1;
  }

  function render(p) {
    if (!set) return;
    const i = nearest(Math.round(p * (count - 1)));
    if (i < 0 || i === last) return;
    last = i;
    const im = set.imgs[i], iw = im.naturalWidth, ih = im.naturalHeight;
    const s = Math.max(canvas.width / iw, canvas.height / ih), dw = iw * s, dh = ih * s;
    ctx.drawImage(im, (canvas.width - dw) / 2, (canvas.height - dh) / 2, dw, dh);
  }

  return { resize, render };
}
