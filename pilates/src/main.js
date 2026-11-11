import Lenis from 'lenis';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { SplitText } from 'gsap/SplitText';
import { createFilm } from './film.js';

gsap.registerPlugin(ScrollTrigger, SplitText);

const html = document.documentElement;
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const INSTANT = location.search.includes('shot');
const finePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;
const FRAMES = 169;
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const smooth = (a, b, v) => { const t = clamp((v - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); };
if (reduce) html.classList.add('reduced');

// ---------- the film: frames from the 3D studio, made photoreal and upscaled with Higgsfield ----------
const stage = $('#stage'), breath = $('#breath'), canvas = $('#scene'), filmEl = $('#film');
const caps = $$('.cap'), stops = $$('.rail .stop'), tag = $('#yours-tag'), heroWord = $('#hero-word');
const railFill = $('.rail .fill'), car = $('.rail .car'), rail = $('.rail');
const film = createFilm(canvas, { count: FRAMES });
const size = () => film.resize(stage.clientWidth, stage.clientHeight);
size();
let lastW = innerWidth, lastH = innerHeight, railW = rail.clientWidth;
addEventListener('resize', () => {
  railW = rail.clientWidth;
  // ignore the phone URL bar showing and hiding; react to rotation and real resizes
  if (innerWidth !== lastW || Math.abs(innerHeight - lastH) > 160) { lastW = innerWidth; lastH = innerHeight; size(); }
});

// ---------- one clock: Lenis and every visual run on GSAP's ticker ----------
const lenis = reduce ? null : new Lenis({ lerp: 0.09, wheelMultiplier: 0.9 });
if (lenis) {
  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add((t) => lenis.raf(t * 1000));
  gsap.ticker.lagSmoothing(0);
}

let target = reduce ? 1 : 0, p = target, lastInput = performance.now();
ScrollTrigger.create({
  trigger: filmEl, start: 'top top', end: 'bottom bottom', invalidateOnRefresh: true,
  onUpdate: (s) => { if (!reduce) target = s.progress; lastInput = performance.now(); },
});
const seg = (v, a, b, f = 0.045) => Math.min(clamp((v - a) / f, 0, 1), clamp((b - v) / f, 0, 1));

// the driver: one progress value moves the film, the captions, the carriage, the stops and the hero word
gsap.ticker.add((time) => {
  p += (target - p) * (INSTANT ? 1 : 0.085);
  if (Math.abs(target - p) < 0.0001) p = target;
  const filmBottom = filmEl.offsetTop + filmEl.offsetHeight;
  const visible = reduce || scrollY < filmBottom;
  stage.classList.toggle('gone', !visible);
  html.classList.toggle('past', scrollY > filmBottom - innerHeight - 80);
  if (!visible) return;
  film.render(p);
  if (reduce) return;
  caps.forEach((c, i) => {
    const o = i === 0 ? 1 - smooth(0.02, +c.dataset.out, p) : seg(p, +c.dataset.in, +c.dataset.out);
    c.style.opacity = o.toFixed(3);
    c.style.translate = `0 ${((1 - o) * 26).toFixed(1)}px`;
    c.toggleAttribute('inert', o < 0.5);
  });
  // the hero word is the spring being drawn: it compresses as you start to scroll
  heroWord.style.fontStretch = `${(125 - 50 * smooth(0, 0.08, p)).toFixed(1)}%`;
  railFill.style.transform = `scaleX(${p.toFixed(4)})`;
  car.style.transform = `translateX(${(p * railW).toFixed(1)}px)`;
  stops.forEach((s) => s.classList.toggle('on', p >= +s.dataset.at - 0.002));
  tag.style.opacity = smooth(0.87, 0.93, p).toFixed(2);
  // at rest the room breathes: in for four counts, out for four
  const idle = smooth(1.4, 3, (performance.now() - lastInput) / 1000);
  const b = 1 + 0.014 * idle * (0.5 - 0.5 * Math.cos((time * Math.PI * 2) / 8));
  breath.style.transform = `scale(${b.toFixed(4)})`;
});

// ---------- bands ----------
if (!reduce) {
  // headings draw out on their width axis and settle, like a carriage returning
  $$('[data-stretch]').forEach((el) => {
    gsap.fromTo(el, { fontStretch: '62%', opacity: 0.35 }, { fontStretch: '112%', opacity: 1, ease: 'none',
      scrollTrigger: { trigger: el, start: 'top 95%', end: 'top 55%', scrub: 0.6 } });
  });
  gsap.fromTo('#foot-word', { fontStretch: '62%' }, { fontStretch: '125%', ease: 'none',
    scrollTrigger: { trigger: 'footer', start: 'top 85%', end: 'bottom bottom', scrub: 0.6 } });
  // statement: lines come up from under a mask
  const big = $('.statement .big');
  SplitText.create(big, { type: 'lines', mask: 'lines', autoSplit: true, onSplit: (self) =>
    gsap.from(self.lines, { yPercent: 105, duration: 1.1, ease: 'power3.out', stagger: 0.07, scrollTrigger: { trigger: big, start: 'top 78%' } }) });
  // the room photograph opens like a door being drawn
  gsap.fromTo('.room figure', { clipPath: 'inset(14% 0% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', ease: 'none',
    scrollTrigger: { trigger: '.room figure', start: 'top 92%', end: 'top 35%', scrub: 0.6 } });
  gsap.fromTo('.room figure img', { scale: 1.14 }, { scale: 1, ease: 'none',
    scrollTrigger: { trigger: '.room figure', start: 'top bottom', end: 'bottom top', scrub: 0.6 } });
  gsap.from('.facts div', { y: 40, opacity: 0, duration: 0.9, ease: 'power3.out', stagger: 0.08, scrollTrigger: { trigger: '.facts', start: 'top 80%' } });
}

// class index: a photograph rides with the pointer on desktop
if (finePointer && !reduce) {
  const peek = $('.peek'), imgs = $$('.peek img');
  const px = gsap.quickTo(peek, 'x', { duration: 0.6, ease: 'power3.out' });
  const py = gsap.quickTo(peek, 'y', { duration: 0.6, ease: 'power3.out' });
  const rot = gsap.quickTo(peek, 'rotation', { duration: 0.8, ease: 'power3.out' });
  let lx = 0;
  $('.index').addEventListener('pointermove', (e) => { px(innerWidth - peek.offsetWidth - Math.max(24, innerWidth * 0.06)); py(e.clientY - peek.offsetHeight / 2); rot(clamp((e.clientX - lx) * 0.25, -6, 6)); lx = e.clientX; });
  $$('.index a').forEach((a) => a.addEventListener('pointerenter', () => {
    imgs.forEach((im) => im.classList.toggle('on', im.dataset.k === a.dataset.img));
    gsap.to(peek, { autoAlpha: 1, scale: 1, duration: 0.5, ease: 'power3.out' });
  }));
  $('.index').addEventListener('pointerleave', () => gsap.to(peek, { autoAlpha: 0, scale: 0.92, duration: 0.4, ease: 'power3.out' }));
  gsap.set(peek, { scale: 0.92 });
}

// phone menu: a full-screen sheet drawn down over the page
const menuBtn = $('#menu-btn');
const setMenu = (open) => {
  html.classList.toggle('menu-open', open);
  menuBtn.setAttribute('aria-expanded', String(open));
  menuBtn.firstElementChild.textContent = open ? 'Close' : 'Menu';
  if (lenis) { if (open) lenis.stop(); else lenis.start(); }
};
menuBtn.addEventListener('click', () => setMenu(!html.classList.contains('menu-open')));
addEventListener('keydown', (e) => { if (e.key === 'Escape' && html.classList.contains('menu-open')) { setMenu(false); menuBtn.focus(); } });
$$('#main-nav a').forEach((l) => l.addEventListener('click', () => setMenu(false)));

// nav shows where you are
$$('.top nav a').forEach((a) => {
  ScrollTrigger.create({ trigger: a.getAttribute('href'), start: 'top 50%', end: 'bottom 50%',
    onToggle: (s) => a.setAttribute('aria-current', s.isActive ? 'true' : 'false') });
});

// in-page links glide through Lenis so the film scrubs on the way
$$('a[href^="#"]').forEach((a) => a.addEventListener('click', (e) => {
  const id = a.getAttribute('href');
  const el = id === '#top' ? null : $(id);
  if (id !== '#top' && !el) return;
  e.preventDefault();
  if (lenis) lenis.scrollTo(el || 0, { duration: 1.8 });
  else if (el) el.scrollIntoView(); else scrollTo(0, 0);
  if (el && id === '#main') el.focus({ preventScroll: true });
}));

// ---------- booking ----------
const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
const PLAN = {
  Mon: [['07:00', 'Foundations', 'Josie'], ['12:30', 'Flow', 'Amara'], ['18:15', 'Sculpt', 'Kit'], ['19:30', 'Flow', 'Josie']],
  Tue: [['07:00', 'Sculpt', 'Kit'], ['08:15', 'Flow', 'Amara'], ['18:15', 'Foundations', 'Josie'], ['19:30', 'Sculpt', 'Kit']],
  Wed: [['07:00', 'Flow', 'Josie'], ['12:30', 'Foundations', 'Amara'], ['18:15', 'Flow', 'Kit'], ['19:30', 'Sculpt', 'Amara']],
  Thu: [['07:30', 'Flow', 'Amara'], ['12:30', 'Sculpt', 'Kit'], ['18:15', 'Foundations', 'Josie'], ['19:30', 'Flow', 'Kit']],
  Fri: [['07:00', 'Sculpt', 'Amara'], ['12:30', 'Flow', 'Josie'], ['17:30', 'Flow', 'Kit']],
  Sat: [['09:00', 'Foundations', 'Josie'], ['10:15', 'Flow', 'Amara'], ['11:30', 'Sculpt', 'Kit']],
  Sun: [['10:00', 'Flow', 'Josie'], ['11:15', 'Foundations', 'Amara']],
};
const LEN = { Foundations: 50, Flow: 50, Sculpt: 45 };
// deterministic "taken" reformers per class
function taken(day, time) {
  let h = 0; for (const ch of day + time) h = (h * 31 + ch.charCodeAt(0)) >>> 0;
  const set = new Set(); const n = 3 + (h % 4);
  for (let i = 0; set.size < n && i < 40; i++) { h = (h * 1103515245 + 12345) >>> 0; const r = 1 + (h % 8); if (!(day === 'Thu' && time === '07:30' && r === 3)) set.add(r); }
  return set;
}
const state = { day: 'Thu', time: '07:30', reformer: 3 };
const dayBar = $('#days'), list = $('#sessions'), plan = $('#plan'), conf = $('#confirm'), hold = $('#hold');
function renderDays() {
  dayBar.innerHTML = DAYS.map((d) => `<button type="button" role="tab" id="day-${d}" aria-selected="${d === state.day}">${d}</button>`).join('');
}
function renderSessions() {
  list.innerHTML = PLAN[state.day].map(([time, cls, who]) => {
    const left = 8 - taken(state.day, time).size, on = time === state.time;
    return `<li><button type="button" id="s-${state.day}-${time.replace(':', '')}" class="sess${on ? ' on' : ''}" data-time="${time}" aria-pressed="${on}">
      <span class="t">${time}</span><span class="c">${cls}<small>${LEN[cls]} min with ${who}</small></span><span class="l">${left} of 8 free</span></button></li>`;
  }).join('');
}
function renderPlan() {
  const tk = taken(state.day, state.time);
  if (tk.has(state.reformer)) state.reformer = [1, 2, 3, 4, 5, 6, 7, 8].find((n) => !tk.has(n)) || null;
  // rows from the back wall (top) to the door (bottom): left column 5 to 8, right column 4 to 1
  const rows = [[5, 4], [6, 3], [7, 2], [8, 1]];
  plan.innerHTML = `<div class="wall">Windows and olive tree</div>` + rows.map(([l, r]) =>
    [l, r].map((n) => `<button type="button" id="ref-${n}" class="ref${tk.has(n) ? ' taken' : ''}${n === state.reformer ? ' mine' : ''}" ${tk.has(n) ? 'disabled' : ''} aria-pressed="${n === state.reformer}" aria-label="Reformer ${n}${tk.has(n) ? ', taken' : ''}">${n}</button>`).join('<span></span>')
  ).join('') + `<div class="door">Door</div><div class="mirrorwall" aria-hidden="true">Mirrors</div>`;
  const s = PLAN[state.day].find((x) => x[0] === state.time);
  $('#pick').textContent = state.reformer ? `Reformer ${state.reformer}, ${state.day} ${state.time}, ${s[1]} with ${s[2]}` : 'This class is full';
  hold.disabled = !state.reformer;
  conf.hidden = true;
}
function all() { renderDays(); renderSessions(); renderPlan(); }
dayBar.addEventListener('click', (e) => { const b = e.target.closest('button'); if (!b) return; state.day = b.textContent; state.time = PLAN[state.day][0][0]; all(); });
list.addEventListener('click', (e) => { const b = e.target.closest('.sess'); if (!b) return; state.time = b.dataset.time; renderSessions(); renderPlan(); });
plan.addEventListener('click', (e) => { const b = e.target.closest('.ref'); if (!b || b.disabled) return; state.reformer = +b.textContent; renderPlan(); });
$('#book-form').addEventListener('submit', (e) => {
  e.preventDefault();
  const s = PLAN[state.day].find((x) => x[0] === state.time);
  conf.innerHTML = `<strong>Reformer ${state.reformer} is held for you.</strong> ${state.day} ${state.time}, ${s[1]} with ${s[2]}. Arrive ten minutes early so we can set your springs. <em>Demo booking only.</em>`;
  conf.hidden = false;
  if (!reduce) gsap.from(conf, { x: -24, opacity: 0, duration: 0.6, ease: 'power3.out' });
});
all();
$('#year').textContent = new Date().getFullYear();
