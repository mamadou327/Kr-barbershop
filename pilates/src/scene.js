// Olea Studio: the real-time 3D room.
// Room coordinates (metres): x 0 (left wall) → 8.4 (mirror wall), z 0 (back wall, windows + olive tree) → 10 (front wall, arched door), y up.
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

const RW = 8.4, RD = 10, H = 3.3, T = 0.18;
export const ROWS = [8.1, 6.6, 5.1, 3.6];
export const MIRRORS = [8.1, 6.6, 5.1, 3.6, 2.1];

const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const smooth = (a, b, v) => { const t = clamp((v - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); };
const lerp = (a, b, t) => a + (b - a) * t;

function canvasTex(w, h, draw, srgb = true) {
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  draw(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c);
  if (srgb) t.colorSpace = THREE.SRGBColorSpace;
  return t;
}

function archShape(path, cx, y0, w, rectH) {
  const r = w / 2;
  path.moveTo(cx - r, y0); path.lineTo(cx + r, y0); path.lineTo(cx + r, y0 + rectH);
  path.absarc(cx, y0 + rectH, r, 0, Math.PI, false); path.lineTo(cx - r, y0);
  return path;
}

function wallGeo(width, height, holes = []) {
  const s = new THREE.Shape();
  s.moveTo(0, 0); s.lineTo(width, 0); s.lineTo(width, height); s.lineTo(0, height); s.lineTo(0, 0);
  for (const h of holes) s.holes.push(archShape(new THREE.Path(), h.x, h.y, h.w, h.h));
  return new THREE.ExtrudeGeometry(s, { depth: T, bevelEnabled: false, curveSegments: 28 });
}

export function createStudio(canvas, { isMobile, onProgress, onReady }) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: !isMobile, powerPreference: 'high-performance' });
  const DPR = Math.min(window.devicePixelRatio || 1, isMobile ? 1.6 : 2);
  renderer.setPixelRatio(DPR);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 0.86;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(50, 1, 0.05, 80);
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(renderer), 0.04).texture;

  // ---------- textures ----------
  const manager = new THREE.LoadingManager();
  manager.onProgress = (_u, done, total) => onProgress && onProgress(done / total);
  manager.onLoad = () => { needsCube = true; onReady && onReady(); };
  const tl = new THREE.TextureLoader(manager);
  const aniso = renderer.capabilities.getMaxAnisotropy();
  const tex = (url, rx = 1, ry = 1) => {
    const t = tl.load(url); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping;
    t.repeat.set(rx, ry); t.anisotropy = aniso; return t;
  };
  const plasterT = tex('tex/plaster.jpg', 1 / 2.6, 1 / 2.6);
  const ceilT = tex('tex/plaster.jpg', 2.2, 2.6);
  const oakT = tex('tex/oak.jpg', RW / 1.7, RD / 1.7);
  const rugT = tex('tex/rug.jpg', 1, 3.6);
  const ashT = tex('tex/ash.jpg', 1, 1);
  const padT = tex('tex/leather.jpg', 1, 1);

  // ---------- materials ----------
  const env = 0.45;
  const M = {
    plaster: new THREE.MeshStandardMaterial({ map: plasterT, color: 0xf6efe6, roughness: 0.96, envMapIntensity: env }),
    ceiling: new THREE.MeshStandardMaterial({ map: ceilT, color: 0xfbf6ef, roughness: 1, envMapIntensity: env }),
    floor: new THREE.MeshStandardMaterial({ map: oakT, color: 0xe9d8c0, roughness: 0.5, envMapIntensity: 0.6 }),
    rug: new THREE.MeshStandardMaterial({ map: rugT, roughness: 1, envMapIntensity: 0.3, polygonOffset: true, polygonOffsetFactor: -2 }),
    wood: new THREE.MeshStandardMaterial({ map: ashT, color: 0xf6e7cf, roughness: 0.5, envMapIntensity: env }),
    oak: new THREE.MeshStandardMaterial({ map: oakT, color: 0xd9c2a0, roughness: 0.55, envMapIntensity: env }),
    pad: new THREE.MeshStandardMaterial({ map: padT, color: 0xf5ede1, roughness: 0.78, envMapIntensity: env }),
    steel: new THREE.MeshStandardMaterial({ color: 0xd4d6d8, metalness: 1, roughness: 0.26 }),
    rope: new THREE.MeshStandardMaterial({ color: 0x302a25, roughness: 0.9 }),
    red: new THREE.MeshStandardMaterial({ color: 0xb4432e, roughness: 0.45 }),
    blue: new THREE.MeshStandardMaterial({ color: 0x3c5d8c, roughness: 0.45 }),
    yellow: new THREE.MeshStandardMaterial({ color: 0xd8af3a, roughness: 0.45 }),
    green: new THREE.MeshStandardMaterial({ color: 0x5b7c48, roughness: 0.45 }),
    black: new THREE.MeshStandardMaterial({ color: 0x1d1b19, roughness: 0.55, metalness: 0.3 }),
    sage: new THREE.MeshStandardMaterial({ color: 0x8f9a7a, roughness: 0.9 }),
    clay: new THREE.MeshStandardMaterial({ color: 0xb8714d, roughness: 0.9 }),
    cream: new THREE.MeshStandardMaterial({ color: 0xe9dfcf, roughness: 0.9 }),
  };

  const world = new THREE.Group(); scene.add(world);
  const shadowAll = (o, cast = true, recv = true) => o.traverse(c => { if (c.isMesh) { c.castShadow = cast; c.receiveShadow = recv; } });

  // ---------- floor, ground ----------
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(RW, RD), M.floor);
  floor.rotation.x = -Math.PI / 2; floor.position.set(RW / 2, 0, RD / 2); floor.receiveShadow = true; world.add(floor);
  // floor slab edge, seen from above
  const slab = new THREE.Mesh(new THREE.BoxGeometry(RW + 2 * T, 0.22, RD + 2 * T), new THREE.MeshStandardMaterial({ color: 0xc9b9a3, roughness: 1 }));
  slab.position.set(RW / 2, -0.111, RD / 2); slab.receiveShadow = true; world.add(slab);
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), new THREE.ShadowMaterial({ opacity: 0.16 }));
  ground.rotation.x = -Math.PI / 2; ground.position.set(RW / 2, -0.23, RD / 2); ground.receiveShadow = true; scene.add(ground);

  // ---------- walls ----------
  const WIN = [{ x: 1.75 + T, y: 0.45, w: 1.3, h: 2.0 }, { x: 6.65 + T, y: 0.45, w: 1.3, h: 2.0 }];
  const back = new THREE.Mesh(wallGeo(RW + 2 * T, H, WIN), M.plaster);
  back.position.set(-T, 0, -T); world.add(back);
  const right = new THREE.Mesh(wallGeo(RD, H), M.plaster);
  right.rotation.y = -Math.PI / 2; right.position.set(RW + T, 0, 0); world.add(right);
  // cutaway walls (rise as the camera comes down)
  const cutFront = new THREE.Group(), cutLeft = new THREE.Group(); world.add(cutFront, cutLeft);
  const front = new THREE.Mesh(wallGeo(RW + 2 * T, H, [{ x: RW / 2 + T, y: 0, w: 1.05, h: 2.35 }]), M.plaster);
  front.position.set(-T, 0, RD); cutFront.add(front);
  const left = new THREE.Mesh(wallGeo(RD, H), M.plaster);
  left.rotation.y = Math.PI / 2; left.position.set(-T, 0, RD); cutLeft.add(left);
  // skirting
  const skirt = (len, x, z, ry, parent) => { const m = new THREE.Mesh(new THREE.BoxGeometry(len, 0.09, 0.018), M.oak); m.position.set(x, 0.045, z); m.rotation.y = ry; parent.add(m); };
  skirt(RW, RW / 2, 0.009, 0, world); skirt(RD, RW - 0.009, RD / 2, Math.PI / 2, world);
  skirt(RD, 0.009, RD / 2, Math.PI / 2, cutLeft);
  skirt(RW / 2 - 0.53, (RW / 2 - 0.53) / 2, RD - 0.009, 0, cutFront); skirt(RW / 2 - 0.53, RW - (RW / 2 - 0.53) / 2, RD - 0.009, 0, cutFront);

  // windows: bright frosted glass + oak frames
  const glassMat = new THREE.MeshBasicMaterial({ color: new THREE.Color(1.55, 1.45, 1.28), toneMapped: false });
  for (const w of WIN) {
    const cx = w.x - T;
    const g = new THREE.Mesh(new THREE.ShapeGeometry(archShape(new THREE.Shape(), 0, 0, w.w, w.h), 24), glassMat);
    g.position.set(cx, w.y, -T + 0.03); world.add(g);
    const bar = (bw, bh, x, y) => { const m = new THREE.Mesh(new THREE.BoxGeometry(bw, bh, 0.05), M.oak); m.position.set(x, y, -0.09); m.castShadow = true; world.add(m); };
    bar(0.045, w.h + w.w / 2, cx, w.y + (w.h + w.w / 2) / 2);
    bar(w.w, 0.045, cx, w.y + 0.75); bar(w.w, 0.045, cx, w.y + 1.5); bar(w.w, 0.04, cx, w.y + w.h);
    const sill = new THREE.Mesh(new THREE.BoxGeometry(w.w + 0.16, 0.04, 0.24), M.oak);
    sill.position.set(cx, w.y - 0.02, 0.03); sill.castShadow = sill.receiveShadow = true; world.add(sill);
  }
  // door: oak reveal + mat + plaque outside
  const doorMat = new THREE.Mesh(new THREE.PlaneGeometry(1.0, 0.6), new THREE.MeshStandardMaterial({ color: 0x5a4c3f, roughness: 1 }));
  doorMat.rotation.x = -Math.PI / 2; doorMat.position.set(RW / 2, 0.004, RD + 0.6); world.add(doorMat);
  const plaque = new THREE.Mesh(new THREE.PlaneGeometry(0.62, 0.3), new THREE.MeshStandardMaterial({
    roughness: 0.35, metalness: 0.6, map: canvasTex(512, 248, (c, w, h) => {
      c.fillStyle = '#b08d57'; c.fillRect(0, 0, w, h);
      c.fillStyle = '#3a2a19'; c.textAlign = 'center';
      c.font = '600 112px "Bricolage Grotesque Variable", sans-serif'; c.fillText('OLEA', w / 2, 128);
      c.font = '500 34px "Instrument Sans", sans-serif'; c.fillText('REFORMER PILATES', w / 2, 196);
    }),
  }));
  plaque.position.set(RW / 2 + 1.15, 1.55, RD + T + 0.006); cutFront.add(plaque);

  // ceiling (one-sided: invisible from above) + track lights
  const ceiling = new THREE.Mesh(new THREE.PlaneGeometry(RW, RD), M.ceiling);
  ceiling.rotation.x = Math.PI / 2; ceiling.position.set(RW / 2, H, RD / 2);
  ceiling.castShadow = true; M.ceiling.shadowSide = THREE.DoubleSide; world.add(ceiling);
  const inside = new THREE.Group(); world.add(inside);
  const SPOTS = [];
  for (const tx of [2.0, 6.4]) {
    const track = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.04, 8.2), M.black);
    track.position.set(tx, H - 0.02, 5.4); inside.add(track);
    for (const z of [2.2, 3.6, 5.1, 6.6, 8.1]) {
      const head = new THREE.Group();
      const can = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.055, 0.17, 16), M.black); can.position.y = -0.11;
      const lens = new THREE.Mesh(new THREE.CircleGeometry(0.042, 16), new THREE.MeshBasicMaterial({ color: new THREE.Color(1.6, 1.25, 0.85), toneMapped: false }));
      lens.rotation.x = Math.PI / 2; lens.position.y = -0.197;
      head.add(can, lens); head.position.set(tx, H - 0.04, z); head.rotation.z = tx < 4 ? 0.28 : -0.28; inside.add(head);
    }
    for (const z of [3.6, 6.6]) SPOTS.push([tx, z]);
  }
  const lightWarm = 0xffcf9a;
  for (const [x, z] of SPOTS) {
    const s = new THREE.SpotLight(lightWarm, 26, 0, 0.75, 0.9, 2);
    s.position.set(x, H - 0.2, z); s.target.position.set(x < 4 ? x - 0.4 : x + 0.4, 0, z - 0.6);
    world.add(s, s.target);
  }
  // the "yours" light over reformer 3
  const yourLight = new THREE.SpotLight(0xffc48a, 0, 0, 0.5, 0.85, 2);
  yourLight.position.set(5.7, H - 0.2, 5.1); yourLight.target.position.set(6.9, 0, 5.1); world.add(yourLight, yourLight.target);

  // ---------- lights ----------
  const hemi = new THREE.HemisphereLight(0xfff3e4, 0x9c8166, 0.62); scene.add(hemi);
  const sun = new THREE.DirectionalLight(0xffdcb0, 3.0);
  sun.position.set(RW / 2 - 2.5, 7.5, -7.5); sun.target.position.set(RW / 2, 0, 4); scene.add(sun, sun.target);
  sun.castShadow = true; sun.shadow.mapSize.set(isMobile ? 1024 : 2048, isMobile ? 1024 : 2048);
  Object.assign(sun.shadow.camera, { left: -9, right: 9, top: 9, bottom: -9, near: 1, far: 30 });
  sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.03; sun.shadow.radius = 4;
  // soft fill so the overview reads as a lit model
  const fill = new THREE.DirectionalLight(0xfff4e8, 0.45); fill.position.set(-6, 10, 14); scene.add(fill);

  // ---------- rug ----------
  const rug = new THREE.Mesh(new THREE.PlaneGeometry(1.1, 7.2), M.rug);
  rug.rotation.x = -Math.PI / 2; rug.position.set(RW / 2, 0.006, 5.85); rug.receiveShadow = true; world.add(rug);

  // ---------- reformers ----------
  const contactTex = canvasTex(256, 128, (c, w, h) => {
    const g = c.createRadialGradient(w / 2, h / 2, 4, w / 2, h / 2, w / 2);
    g.addColorStop(0, 'rgba(0,0,0,0.55)'); g.addColorStop(0.55, 'rgba(0,0,0,0.3)'); g.addColorStop(1, 'rgba(0,0,0,0)');
    c.save(); c.scale(1, 0.5); c.translate(0, h / 2); c.fillStyle = g; c.fillRect(0, -h / 2, w, h * 2); c.restore();
  }, false);
  const contactMat = new THREE.MeshBasicMaterial({ color: 0x000000, alphaMap: contactTex, transparent: true, opacity: 0.55, depthWrite: false });
  const reformerParts = buildReformerParts();
  const reformers = [];
  ROWS.forEach((z, i) => {
    for (const side of [1, -1]) {
      const g = new THREE.Group();
      for (const [key, geo] of reformerParts) { const m = new THREE.Mesh(geo, M[key]); m.castShadow = true; m.receiveShadow = true; g.add(m); }
      const cs = new THREE.Mesh(new THREE.PlaneGeometry(2.9, 1.25), contactMat); cs.rotation.x = -Math.PI / 2; cs.position.set(1.2, 0.008, 0); g.add(cs);
      if (side === 1) g.position.set(5.6, 0, z); else { g.rotation.y = Math.PI; g.position.set(2.8, 0, z); }
      world.add(g);
      reformers.push({ group: g, number: side === 1 ? i + 1 : 8 - i });
    }
  });
  // floor numbers at each reformer foot
  for (const r of reformers) {
    const right = r.group.position.x > 4;
    const t = canvasTex(128, 128, (c, w, h) => {
      c.strokeStyle = 'rgba(58,44,30,.55)'; c.lineWidth = 4; c.beginPath(); c.arc(w / 2, h / 2, 54, 0, Math.PI * 2); c.stroke();
      c.fillStyle = 'rgba(58,44,30,.7)'; c.font = '600 64px "Bricolage Grotesque Variable", sans-serif';
      c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(String(r.number), w / 2, h / 2 + 3);
    });
    const d = new THREE.Mesh(new THREE.PlaneGeometry(0.2, 0.2), new THREE.MeshStandardMaterial({ map: t, transparent: true, roughness: 0.9, polygonOffset: true, polygonOffsetFactor: -3 }));
    d.rotation.x = -Math.PI / 2; d.position.set(right ? 5.38 : 3.02, 0.007, r.group.position.z); d.receiveShadow = true; world.add(d);
  }
  // glow outline under reformer 3
  const ringTex = canvasTex(512, 256, (c, w, h) => {
    c.shadowColor = 'rgba(255,190,120,1)'; c.shadowBlur = 30; c.strokeStyle = 'rgba(255,214,160,1)'; c.lineWidth = 7;
    const r = 46, x = 34, y = 34, ww = w - 68, hh = h - 68;
    c.beginPath(); c.roundRect(x, y, ww, hh, r); c.stroke(); c.stroke();
  }, false);
  const ring = new THREE.Mesh(new THREE.PlaneGeometry(2.95, 1.35), new THREE.MeshBasicMaterial({ color: 0xffc58c, alphaMap: ringTex, transparent: true, opacity: 0, depthWrite: false, toneMapped: false, blending: THREE.AdditiveBlending }));
  ring.rotation.x = -Math.PI / 2; ring.position.set(6.8, 0.012, 5.1); world.add(ring);

  // ---------- mirrors with warm LED halo ----------
  const cubeRT = new THREE.WebGLCubeRenderTarget(isMobile ? 256 : 512, { type: THREE.UnsignedByteType });
  const cubeCam = new THREE.CubeCamera(0.05, 30, cubeRT); cubeCam.position.set(4.6, 1.45, 5.1); scene.add(cubeCam);
  const mirrorMat = new THREE.MeshBasicMaterial({ color: 0xe6e0d6, envMap: cubeRT.texture, reflectivity: 1 });
  const haloMat = new THREE.MeshBasicMaterial({ color: new THREE.Color(3.2, 1.9, 0.85), toneMapped: false });
  const washTex = canvasTex(128, 256, (c, w, h) => {
    const g = c.createRadialGradient(w / 2, h * 0.42, 6, w / 2, h * 0.42, h * 0.5);
    g.addColorStop(0, 'rgba(255,255,255,0.9)'); g.addColorStop(0.5, 'rgba(255,255,255,0.35)'); g.addColorStop(1, 'rgba(255,255,255,0)');
    c.fillStyle = g; c.fillRect(0, 0, w, h);
  }, false);
  const washMat = new THREE.MeshBasicMaterial({ color: 0xffb070, alphaMap: washTex, transparent: true, opacity: 0.6, depthWrite: false, blending: THREE.AdditiveBlending });
  const mirrors = [];
  const MW = 0.82, MR = 1.5, MY = 0.38;
  for (const z of MIRRORS) {
    const g = new THREE.Group(); g.rotation.y = -Math.PI / 2; g.position.set(RW, 0, z);
    const wash = new THREE.Mesh(new THREE.PlaneGeometry(1.7, 3.1), washMat); wash.position.set(0, MY + 1.05, 0.004); g.add(wash);
    const outer = archShape(new THREE.Shape(), 0, MY - 0.035, MW + 0.07, MR + 0.035);
    outer.holes.push(archShape(new THREE.Path(), 0, MY, MW, MR));
    const halo = new THREE.Mesh(new THREE.ShapeGeometry(outer, 40), haloMat); halo.position.z = 0.01; g.add(halo);
    const m = new THREE.Mesh(new THREE.ShapeGeometry(archShape(new THREE.Shape(), 0, MY, MW, MR), 40), mirrorMat); m.position.z = 0.018; g.add(m);
    mirrors.push(m); world.add(g);
  }
  // warm bounce from the halos
  const haloFill = new THREE.PointLight(0xffb27a, 3.5, 7, 2); haloFill.position.set(7.9, 1.6, 5.1); world.add(haloFill);

  // ---------- bench + mats by the door ----------
  const bench = new THREE.Group();
  const top = new THREE.Mesh(new THREE.BoxGeometry(2.0, 0.05, 0.4), M.oak); top.position.y = 0.45; bench.add(top);
  for (const x of [-0.9, 0.9]) { const leg = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.43, 0.36), M.oak); leg.position.set(x, 0.215, 0); bench.add(leg); }
  const matCols = [M.sage, M.cream, M.clay, M.sage, M.cream];
  matCols.forEach((mat, i) => { const mm = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.075, 0.38, 20), mat); mm.rotation.x = Math.PI / 2; mm.position.set(-0.75 + i * 0.17, 0.55, 0); bench.add(mm); });
  bench.position.set(1.5, 0, RD - 0.32); shadowAll(bench); world.add(bench);

  // ---------- olive trees (Higgsfield image → 3D model) ----------
  const treeSlots = [{ x: RW / 2, z: 1.0, h: 2.45, ry: 0.4 }, { x: RW - 0.6, z: RD - 0.6, h: 1.55, ry: 2.2 }];
  new GLTFLoader(manager).load('models/olive.json', (gltf) => {
    const src = gltf.scene;
    src.traverse(c => { if (c.isMesh) { c.castShadow = true; c.receiveShadow = true; if (c.material) { c.material.envMapIntensity = env; } } });
    const box = new THREE.Box3().setFromObject(src); const size = box.getSize(new THREE.Vector3()); const ctr = box.getCenter(new THREE.Vector3());
    for (const s of treeSlots) {
      const t = src.clone(); const k = s.h / size.y;
      const w = new THREE.Group(); t.position.set(-ctr.x, -box.min.y, -ctr.z); w.add(t);
      w.scale.setScalar(k); w.position.set(s.x, 0, s.z); w.rotation.y = s.ry; world.add(w);
      const cs = new THREE.Mesh(new THREE.PlaneGeometry(1.2 * s.h / 2.45, 1.2 * s.h / 2.45), contactMat); cs.rotation.x = -Math.PI / 2; cs.position.set(s.x, 0.009, s.z); world.add(cs);
    }
    needsCube = true;
  });

  // ---------- dust in the window light ----------
  const N = isMobile ? 160 : 320;
  const dpos = new Float32Array(N * 3), dseed = new Float32Array(N);
  for (let i = 0; i < N; i++) { dpos[i * 3] = 0.6 + Math.random() * 7.2; dpos[i * 3 + 1] = 0.2 + Math.random() * 2.9; dpos[i * 3 + 2] = 0.3 + Math.random() * 5.5; dseed[i] = Math.random() * 100; }
  const dgeo = new THREE.BufferGeometry(); dgeo.setAttribute('position', new THREE.BufferAttribute(dpos, 3));
  const dotTex = canvasTex(32, 32, (c) => { const g = c.createRadialGradient(16, 16, 0, 16, 16, 16); g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(1, 'rgba(255,255,255,0)'); c.fillStyle = g; c.fillRect(0, 0, 32, 32); }, false);
  const dust = new THREE.Points(dgeo, new THREE.PointsMaterial({ color: 0xfff1dc, size: 0.007, alphaMap: dotTex, transparent: true, opacity: 0.5, depthWrite: false, blending: THREE.AdditiveBlending }));
  inside.add(dust);
  const dbase = dpos.slice();

  // ---------- post ----------
  const composer = new EffectComposer(renderer);
  composer.addPass(new RenderPass(scene, camera));
  const bloom = new UnrealBloomPass(new THREE.Vector2(256, 256), 0.22, 0.45, 1.35);
  composer.addPass(bloom);
  if (location.search.includes('nobloom')) bloom.enabled = false;
  composer.addPass(new OutputPass());

  // ---------- camera path ----------
  // p is scroll progress 0..1 through the film. Keys: overview → swing to the front → outside the door → through the arch → down the aisle → turn to reformer 3.
  let keys, curvePos, curveTgt;
  function buildPath(portrait) {
    keys = portrait ? [
      { p: 0.00, pos: [-3.2, 17.5, 18.2], tgt: [4.2, 0.0, 5.0] },
      { p: 0.20, pos: [0.4, 7.4, 19.8], tgt: [4.2, 0.8, 6.0] },
      { p: 0.38, pos: [4.2, 1.6, 13.6], tgt: [4.2, 1.35, 7.0] },
      { p: 0.50, pos: [4.2, 1.5, 9.7], tgt: [4.2, 1.25, 4.0] },
      { p: 0.63, pos: [4.2, 1.5, 6.9], tgt: [4.35, 1.15, 1.6] },
      { p: 0.82, pos: [3.3, 2.05, 5.75], tgt: [7.0, 0.55, 5.05] },
      { p: 1.00, pos: [3.75, 1.85, 5.6], tgt: [7.2, 0.5, 5.1] },
    ] : [
      { p: 0.00, pos: [-5.6, 9.8, 15.4], tgt: [4.2, 0.2, 4.6] },
      { p: 0.20, pos: [0.8, 5.6, 17.2], tgt: [4.2, 1.0, 6.4] },
      { p: 0.38, pos: [4.2, 1.6, 14.4], tgt: [4.2, 1.4, 7.0] },
      { p: 0.50, pos: [4.2, 1.5, 9.7], tgt: [4.2, 1.3, 4.0] },
      { p: 0.63, pos: [4.2, 1.5, 6.9], tgt: [4.4, 1.2, 1.6] },
      { p: 0.82, pos: [3.2, 2.0, 6.1], tgt: [7.0, 0.6, 4.95] },
      { p: 1.00, pos: [3.65, 1.82, 5.85], tgt: [7.2, 0.55, 5.05] },
    ];
    curvePos = new THREE.CatmullRomCurve3(keys.map(k => new THREE.Vector3(...k.pos)), false, 'centripetal');
    curveTgt = new THREE.CatmullRomCurve3(keys.map(k => new THREE.Vector3(...k.tgt)), false, 'centripetal');
  }
  function pathU(p) {
    for (let i = 0; i < keys.length - 1; i++) {
      if (p <= keys[i + 1].p) { const f = (p - keys[i].p) / (keys[i + 1].p - keys[i].p); const e = f < 0.5 ? 2 * f * f : 1 - Math.pow(-2 * f + 2, 2) / 2; return (i + lerp(f, e, 0.55)) / (keys.length - 1); }
    }
    return 1;
  }

  // ---------- sizing ----------
  let W = 1, Hh = 1, portrait = false;
  function resize(w, h) {
    W = w; Hh = h; portrait = w / h < 0.9;
    renderer.setSize(w, h, false); composer.setSize(w, h); composer.setPixelRatio(DPR);
    bloom.resolution.set(w / 2, h / 2);
    camera.aspect = w / h; camera.fov = portrait ? 66 : (w / h > 1.9 ? 42 : 48); camera.updateProjectionMatrix();
    buildPath(portrait);
  }

  // ---------- frame ----------
  let needsCube = true;
  const tmpP = new THREE.Vector3(), tmpT = new THREE.Vector3(), right3 = new THREE.Vector3(), up3 = new THREE.Vector3();
  const pointer = { x: 0, y: 0, sx: 0, sy: 0 };
  const label3 = new THREE.Vector3(6.75, 1.05, 5.1);

  function captureMirrors() {
    mirrors.forEach(m => (m.visible = false)); inside.visible = false;
    cubeCam.update(renderer, scene);
    mirrors.forEach(m => (m.visible = true));
  }

  function render(p, t, motion = true) {
    if (needsCube) { captureMirrors(); needsCube = false; }
    const u = pathU(p);
    curvePos.getPoint(u, tmpP); curveTgt.getPoint(u, tmpT);
    // gentle pointer parallax
    pointer.sx += (pointer.x - pointer.sx) * 0.05; pointer.sy += (pointer.y - pointer.sy) * 0.05;
    camera.position.copy(tmpP); camera.lookAt(tmpT);
    if (motion) {
      const amt = lerp(0.35, 0.07, smooth(0.3, 0.5, p));
      right3.setFromMatrixColumn(camera.matrix, 0); up3.setFromMatrixColumn(camera.matrix, 1);
      camera.position.addScaledVector(right3, pointer.sx * amt).addScaledVector(up3, -pointer.sy * amt * 0.6);
      camera.position.y += Math.sin(t * 0.0009) * 0.012 * smooth(0.4, 0.55, p);
      camera.lookAt(tmpT);
    }
    // frame the dollhouse beside the hero text at the top
    const off = 1 - smooth(0.0, 0.2, p);
    if (off > 0.001) camera.setViewOffset(W, Hh, portrait ? 0 : -W * 0.13 * off, portrait ? -Hh * 0.13 * off : 0, W, Hh);
    else camera.clearViewOffset();

    // the room builds itself around you
    const k = smooth(0.1, 0.33, p);
    const s = lerp(0.24, 1, k); cutFront.scale.y = s; cutLeft.scale.y = s;
    plaque.visible = k > 0.6;
    inside.visible = camera.position.y < H - 0.05;

    // reformer 3 is yours
    const y = smooth(0.74, 0.86, p);
    ring.material.opacity = y * (0.85 + 0.15 * Math.sin(t * 0.003));
    yourLight.intensity = y * 15;

    // dust drift
    if (motion && inside.visible) {
      const a = dgeo.attributes.position.array;
      for (let i = 0; i < N; i++) { const sd = dseed[i]; a[i * 3] = dbase[i * 3] + Math.sin(t * 0.00021 + sd) * 0.25; a[i * 3 + 1] = dbase[i * 3 + 1] + Math.sin(t * 0.00017 + sd * 2) * 0.2; a[i * 3 + 2] = dbase[i * 3 + 2] + Math.cos(t * 0.00019 + sd) * 0.25; }
      dgeo.attributes.position.needsUpdate = true;
    }
    composer.render();

    // screen position of reformer 3's label
    const v = label3.clone().project(camera);
    return { label: { x: (v.x * 0.5 + 0.5) * W, y: (-v.y * 0.5 + 0.5) * Hh, on: y, behind: v.z > 1 } };
  }

  function setVoid(css) {
    const c = new THREE.Color(css.trim() || '#e6dccd'); c.convertSRGBToLinear();
    scene.background = c;
  }

  return { resize, render, pointer, setVoid, manager };
}

// One reformer, merged into a handful of meshes (one per material). Foot end at x=0, head end at x=2.4.
function buildReformerParts() {
  const parts = {};
  const o = new THREE.Object3D();
  const add = (geo, key, x, y, z, rx = 0, ry = 0, rz = 0) => {
    o.position.set(x, y, z); o.rotation.set(rx, ry, rz); o.scale.set(1, 1, 1); o.updateMatrix();
    let g = geo.index ? geo.toNonIndexed() : geo; g.applyMatrix4(o.matrix);
    (parts[key] = parts[key] || []).push(g);
  };
  const between = (a, b, r, key) => {
    const A = new THREE.Vector3(...a), B = new THREE.Vector3(...b), d = B.clone().sub(A), len = d.length();
    const g = new THREE.CylinderGeometry(r, r, len, 8).toNonIndexed();
    const q = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.normalize());
    const m = new THREE.Matrix4().compose(A.clone().add(B).multiplyScalar(0.5), q, new THREE.Vector3(1, 1, 1));
    g.applyMatrix4(m); (parts[key] = parts[key] || []).push(g);
  };
  const L = 2.4, Wd = 0.66;
  for (const x of [0.08, 1.2, 2.32]) for (const z of [-Wd / 2, Wd / 2]) add(new THREE.BoxGeometry(0.08, 0.14, 0.08), 'wood', x, 0.07, z);
  for (const z of [-Wd / 2, Wd / 2]) add(new THREE.BoxGeometry(L, 0.13, 0.07), 'wood', L / 2, 0.2, z);
  add(new THREE.BoxGeometry(0.07, 0.13, Wd + 0.07), 'wood', 0.035, 0.2, 0);
  add(new THREE.BoxGeometry(0.07, 0.13, Wd + 0.07), 'wood', L - 0.035, 0.2, 0);
  for (const z of [-0.21, 0.21]) add(new THREE.BoxGeometry(L - 0.3, 0.025, 0.04), 'steel', L / 2 + 0.05, 0.275, z);
  add(new THREE.BoxGeometry(0.9, 0.04, 0.56), 'wood', 1.72, 0.29, 0);
  add(new RoundedBoxGeometry(0.95, 0.09, 0.6, 3, 0.03), 'pad', 1.72, 0.355, 0);
  add(new RoundedBoxGeometry(0.3, 0.06, 0.48, 3, 0.025), 'pad', 2.13, 0.425, 0, 0, 0, 0.16);
  for (const z of [-0.17, 0.17]) add(new RoundedBoxGeometry(0.09, 0.17, 0.11, 3, 0.03), 'pad', 1.95, 0.48, z);
  add(new RoundedBoxGeometry(0.28, 0.06, 0.62, 3, 0.025), 'pad', 0.17, 0.3, 0);
  const cols = ['red', 'red', 'blue', 'yellow', 'green'];
  [-0.16, -0.08, 0, 0.08, 0.16].forEach((z, i) => {
    add(new THREE.CylinderGeometry(0.011, 0.011, 0.84, 8), 'steel', 0.85, 0.255, z, 0, 0, Math.PI / 2);
    add(new THREE.SphereGeometry(0.022, 10, 8), cols[i], 0.43, 0.255, z);
  });
  add(new THREE.BoxGeometry(0.04, 0.04, 0.5), 'steel', 0.4, 0.255, 0);
  for (const z of [-Wd / 2 + 0.02, Wd / 2 - 0.02]) add(new THREE.CylinderGeometry(0.018, 0.018, 0.55, 10), 'steel', 0.3, 0.5, z, 0, 0, -0.25);
  add(new THREE.CylinderGeometry(0.032, 0.032, Wd - 0.02, 16), 'pad', 0.37, 0.77, 0, Math.PI / 2, 0, 0);
  for (const z of [-Wd / 2, Wd / 2]) {
    add(new THREE.BoxGeometry(0.06, 0.64, 0.06), 'wood', L - 0.03, 0.5, z);
    const zi = z > 0 ? z - 0.05 : z + 0.05;
    add(new THREE.CylinderGeometry(0.035, 0.035, 0.03, 16), 'steel', L - 0.03, 0.8, zi, Math.PI / 2, 0, 0);
    between([L - 0.05, 0.8, zi], [2.0, 0.53, zi * 0.72], 0.006, 'rope');
    add(new THREE.TorusGeometry(0.05, 0.012, 8, 20), 'rope', 1.98, 0.57, zi * 0.72, Math.PI / 2, 0, 0);
  }
  return Object.entries(parts).map(([k, gs]) => [k, mergeGeometries(gs, false)]);
}
