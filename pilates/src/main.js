import Lenis from 'lenis';
import { createFilm } from './film.js';

const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const INSTANT = location.search.includes('shot');
const FRAMES = 169;
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));

// ---------- photoreal film: frames rendered from the 3D studio, made photoreal with Higgsfield ----------
const stage = $('#stage'), canvas = $('#scene'), film = $('#film');
const chapters = $$('.chap'), ticks = $$('.rail li'), tag = $('#yours-tag'), loader = $('#loader');
const studio = createFilm(canvas, {
  count: FRAMES,
  onProgress: (f) => loader.style.setProperty('--f', f.toFixed(3)),
  onReady: () => document.documentElement.classList.add('ready'),
});
const size = () => studio.resize(stage.clientWidth, stage.clientHeight);
size();
let lastW = innerWidth, lastH = innerHeight;
addEventListener('resize', () => {
  // ignore the phone URL bar showing and hiding; react to rotation and real resizes
  if (innerWidth !== lastW || Math.abs(innerHeight - lastH) > 160) { lastW = innerWidth; lastH = innerHeight; size(); }
});

const lenis = reduce ? null : new Lenis({ lerp: 0.085, wheelMultiplier: 0.9 });
let target = 0, p = 0, visible = true;

function progress() {
  const top = film.offsetTop, span = film.offsetHeight - innerHeight;
  return clamp((scrollY - top) / span, 0, 1);
}
function seg(v, a, b, f = 0.05) { return Math.min(clamp((v - a) / f, 0, 1), clamp((b - v) / f, 0, 1)); }

function frame(t) {
  if (lenis) lenis.raf(t);
  target = progress();
  p += (target - p) * (reduce || INSTANT ? 1 : 0.075);
  if (Math.abs(target - p) < 0.0002) p = target;
  const filmBottom = film.offsetTop + film.offsetHeight;
  visible = scrollY < filmBottom && !document.hidden;
  stage.classList.toggle('gone', !visible);
  document.documentElement.classList.toggle('past', scrollY > filmBottom - innerHeight - 70);
  if (visible) {
    chapters.forEach((c) => {
      const o = seg(p, +c.dataset.in, +c.dataset.out);
      c.style.opacity = o.toFixed(3);
      c.style.transform = `translate3d(0, ${((1 - o) * 18).toFixed(1)}px, 0)`;
      c.toggleAttribute('inert', o < 0.5);
    });
    ticks.forEach((li) => li.classList.toggle('on', p >= +li.dataset.at - 0.001));
    studio.render(p);
    tag.style.opacity = clamp((p - 0.88) / 0.06, 0, 1).toFixed(2);
  }
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);

// in-page links go through Lenis so the film scrubs smoothly
$$('a[href^="#"]').forEach((a) => a.addEventListener('click', (e) => {
  const id = a.getAttribute('href');
  const el = id === '#top' ? document.body : $(id);
  if (!el) return;
  e.preventDefault();
  if (lenis) lenis.scrollTo(id === '#top' ? 0 : el, { duration: 1.6 }); else (id === '#top' ? scrollTo(0, 0) : el.scrollIntoView());
}));

// ---------- booking ----------
const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
const TEACH = { Amara: 'Amara', Josie: 'Josie', Kit: 'Kit' };
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
    const left = 8 - taken(state.day, time).size;
    const on = time === state.time;
    return `<li><button type="button" id="s-${state.day}-${time.replace(':', '')}" class="sess${on ? ' on' : ''}" data-time="${time}" aria-pressed="${on}">
      <span class="t">${time}</span><span class="c">${cls}<small>${LEN[cls]} min · ${TEACH[who]}</small></span><span class="l">${left} of 8 free</span></button></li>`;
  }).join('');
}
function renderPlan() {
  const tk = taken(state.day, state.time);
  if (tk.has(state.reformer)) state.reformer = [1, 2, 3, 4, 5, 6, 7, 8].find((n) => !tk.has(n)) || null;
  // rows from the back wall (top) to the door (bottom): left column 5–8, right column 4–1
  const rows = [[5, 4], [6, 3], [7, 2], [8, 1]];
  plan.innerHTML = `<div class="wall">Windows · olive tree</div>` + rows.map(([l, r]) =>
    [l, r].map((n) => `<button type="button" id="ref-${n}" class="ref${tk.has(n) ? ' taken' : ''}${n === state.reformer ? ' mine' : ''}" ${tk.has(n) ? 'disabled' : ''} aria-pressed="${n === state.reformer}" aria-label="Reformer ${n}${tk.has(n) ? ', taken' : ''}">${n}</button>`).join('<span class="aisle"></span>')
  ).join('') + `<div class="door">Door</div><div class="mirrorwall" aria-hidden="true">Mirrors</div>`;
  const s = PLAN[state.day].find((x) => x[0] === state.time);
  $('#pick').textContent = state.reformer ? `Reformer ${state.reformer} · ${state.day} ${state.time} · ${s[1]} with ${s[2]}` : 'This class is full';
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
});
all();
$('#year').textContent = new Date().getFullYear();
