/* Téléphone 3D du diagnostic — High Tech Clinic
   API : P3D.mount(el) · P3D.focus(testId) · P3D.results(map) · P3D.shake() · P3D.tilt(x, y) */
(function () {
  var P3D = { ok: false, mount: noop, focus: noop, results: noop, shake: noop, tilt: noop };
  window.P3D = P3D;
  function noop() {}
  if (!window.THREE) return;
  var T = window.THREE;
  try {
    var test = document.createElement('canvas');
    if (!(test.getContext('webgl') || test.getContext('experimental-webgl'))) return;
  } catch (e) { return; }

  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var BLUE = new T.Color('#4F8CFF'), GREEN = new T.Color('#3DDC97'), RED = new T.Color('#FF6B5E'), GREY = new T.Color('#3A434E');

  var renderer = new T.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  if (renderer.outputEncoding !== undefined) renderer.outputEncoding = T.sRGBEncoding;
  var canvas = renderer.domElement;
  canvas.style.cssText = 'display:block;width:100%;height:100%;touch-action:pan-y;cursor:grab';
  canvas.setAttribute('aria-hidden', 'true');

  var scene = new T.Scene();
  var camera = new T.PerspectiveCamera(30, 1, 0.1, 50);
  camera.position.set(0, 0, 4.6);

  scene.add(new T.AmbientLight(0xffffff, 0.55));
  var key = new T.DirectionalLight(0xffffff, 0.9); key.position.set(2, 3, 4); scene.add(key);
  var rim = new T.PointLight(0x4f8cff, 1.4, 12); rim.position.set(-3, -1, -2); scene.add(rim);
  var fill = new T.PointLight(0x4f8cff, 0.6, 10); fill.position.set(2.5, -2, 3); scene.add(fill);

  function rrect(w, h, r) {
    var s = new T.Shape(), x = -w / 2, y = -h / 2;
    s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r);
    s.lineTo(x + w, y + h - r); s.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    s.lineTo(x + r, y + h); s.quadraticCurveTo(x, y + h, x, y + h - r);
    s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y);
    return s;
  }
  function mat(color, metal, rough, extra) {
    var m = new T.MeshStandardMaterial({ color: color, metalness: metal, roughness: rough, emissive: 0x000000 });
    if (extra) for (var k in extra) m[k] = extra[k];
    return m;
  }

  var phone = new T.Group(); scene.add(phone);
  var W = 0.76, H = 1.56, D = 0.075, BEV = 0.022;
  var FRONT = D / 2 + BEV, BACK = -(D / 2 + BEV);

  // Coque
  var bodyGeo = new T.ExtrudeGeometry(rrect(W, H, 0.13), { depth: D, bevelEnabled: true, bevelThickness: BEV, bevelSize: BEV, bevelSegments: 4, curveSegments: 18 });
  bodyGeo.translate(0, 0, -D / 2);
  var body = new T.Mesh(bodyGeo, mat('#2A323C', 0.75, 0.32)); phone.add(body);

  // Écran
  var screenMat = mat('#05070A', 0.1, 0.25);
  var screen = new T.Mesh(new T.ShapeGeometry(rrect(W - 0.05, H - 0.05, 0.11), 18), screenMat);
  screen.position.z = FRONT + 0.002; phone.add(screen);

  // Caméra avant (pastille)
  var pillMat = mat('#000000', 0.2, 0.4);
  var pill = new T.Mesh(new T.ShapeGeometry(rrect(0.2, 0.055, 0.0275), 10), pillMat);
  pill.position.set(0, H / 2 - 0.09, FRONT + 0.004); phone.add(pill);
  var lensF = new T.Mesh(new T.CircleGeometry(0.016, 20), mat('#0B1830', 0.6, 0.15));
  lensF.position.set(0.055, H / 2 - 0.09, FRONT + 0.005); phone.add(lensF);

  // Écouteur (haut-parleur du haut)
  var earMat = mat('#11161C', 0.4, 0.5);
  var ear = new T.Mesh(new T.BoxGeometry(0.14, 0.012, 0.01), earMat);
  ear.position.set(0, H / 2 - 0.035, FRONT - 0.002); phone.add(ear);

  // Bloc photo arrière
  var bumpMat = mat('#20262E', 0.6, 0.3);
  var bumpGeo = new T.ExtrudeGeometry(rrect(0.34, 0.34, 0.08), { depth: 0.02, bevelEnabled: true, bevelThickness: 0.006, bevelSize: 0.006, bevelSegments: 2 });
  var bump = new T.Mesh(bumpGeo, bumpMat);
  bump.rotation.y = Math.PI; bump.position.set(W / 2 - 0.22, H / 2 - 0.22, BACK); phone.add(bump);
  var lensMat = mat('#0A0F18', 0.9, 0.08);
  var ringMat = mat('#3A434E', 0.9, 0.25);
  var lensGroup = new T.Group(); phone.add(lensGroup);
  [[-0.07, 0.07], [-0.07, -0.07], [0.075, 0]].forEach(function (p) {
    var ring = new T.Mesh(new T.CylinderGeometry(0.058, 0.058, 0.03, 28), ringMat);
    ring.rotation.x = Math.PI / 2; ring.position.set(W / 2 - 0.22 - p[0], H / 2 - 0.22 + p[1], BACK - 0.035);
    var glass = new T.Mesh(new T.CircleGeometry(0.042, 28), lensMat);
    glass.rotation.y = Math.PI; glass.position.set(ring.position.x, ring.position.y, BACK - 0.051);
    lensGroup.add(ring); lensGroup.add(glass);
  });
  var flash = new T.Mesh(new T.CircleGeometry(0.018, 16), mat('#D8D2B8', 0.2, 0.4));
  flash.rotation.y = Math.PI; flash.position.set(W / 2 - 0.22 - 0.075, H / 2 - 0.22 + 0.11, BACK - 0.03); lensGroup.add(flash);

  // Bord du bas : port, haut-parleur, micro
  var portMat = mat('#05070A', 0.3, 0.5);
  var port = new T.Mesh(new T.BoxGeometry(0.12, 0.02, 0.035), portMat);
  port.position.set(0, -H / 2 - BEV + 0.008, 0); phone.add(port);
  var spkMat = mat('#05070A', 0.3, 0.5), micMat = mat('#05070A', 0.3, 0.5);
  var spk = new T.Group(), mic = new T.Group(); phone.add(spk); phone.add(mic);
  for (var i = 0; i < 6; i++) {
    var h1 = new T.Mesh(new T.CylinderGeometry(0.009, 0.009, 0.02, 10), spkMat);
    h1.position.set(0.11 + i * 0.03, -H / 2 - BEV + 0.008, 0); spk.add(h1);
  }
  for (var j = 0; j < 2; j++) {
    var h2 = new T.Mesh(new T.CylinderGeometry(0.009, 0.009, 0.02, 10), micMat);
    h2.position.set(-0.13 - j * 0.03, -H / 2 - BEV + 0.008, 0); mic.add(h2);
  }

  // Boutons latéraux
  var btnMat = mat('#323B46', 0.8, 0.3);
  [[0.38, 0.14], [0.16, 0.1], [0.02, 0.1]].forEach(function (b, k) {
    var bt = new T.Mesh(new T.BoxGeometry(0.014, b[1], 0.04), btnMat);
    bt.position.set(k === 0 ? W / 2 + BEV + 0.004 : -W / 2 - BEV - 0.004, b[0], 0); phone.add(bt);
  });

  // Halos lumineux
  var haloTex = (function () {
    var c = document.createElement('canvas'); c.width = c.height = 128;
    var g = c.getContext('2d'), gr = g.createRadialGradient(64, 64, 0, 64, 64, 64);
    gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.25, 'rgba(255,255,255,.55)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
    g.fillStyle = gr; g.fillRect(0, 0, 128, 128);
    return new T.CanvasTexture(c);
  })();
  var halos = [];
  function halo(pos, color, size) {
    var sp = new T.Sprite(new T.SpriteMaterial({ map: haloTex, color: color, transparent: true, depthWrite: false, blending: T.AdditiveBlending }));
    sp.position.copy(pos); sp.scale.set(size, size, 1); sp.renderOrder = 10; sp.userData.base = size;
    phone.add(sp); halos.push(sp); return sp;
  }
  function clearHalos() { halos.forEach(function (h) { phone.remove(h); h.material.dispose(); }); halos = []; }
  var V = function (x, y, z) { return new T.Vector3(x, y, z); };

  // Pièces par test
  var PARTS = {
    screen: { mats: [screenMat], view: { x: 0.12, y: -0.35 }, at: [] },
    ear: { mats: [earMat, spkMat], view: { x: -0.95, y: 0.25 }, at: [V(0.185, -H / 2 - BEV, 0.02)] },
    mic: { mats: [micMat], view: { x: -1.05, y: -0.2 }, at: [V(-0.145, -H / 2 - BEV, 0.02)] },
    back: { mats: [bumpMat, ringMat], view: { x: 0.15, y: Math.PI - 0.45 }, at: [V(W / 2 - 0.22, H / 2 - 0.22, BACK - 0.06)] },
    front: { mats: [pillMat], view: { x: 0.35, y: -0.2 }, at: [V(0.055, H / 2 - 0.09, FRONT + 0.02)] },
    body: { mats: [body.material], view: { x: 0.2, y: -0.7 }, at: [] },
    port: { mats: [portMat], view: { x: -1.05, y: 0.1 }, at: [V(0, -H / 2 - BEV, 0.02)] }
  };
  var TEST_PART = { touch: 'screen', pixels: 'screen', speaker: 'ear', mic: 'mic', camback: 'back', camfront: 'front', sensors: 'body', vib: 'body', charge: 'port' };

  // État d'animation
  var target = { x: 0.12, y: -0.35 }, rot = { x: 0.12, y: -0.35 };
  var drag = null, dragOff = { x: 0, y: 0 }, tiltV = { x: 0, y: 0 }, shakeT = 0;
  var pulse = [], statusColors = [], autoSpin = false, screenCycle = false;

  function clearFx() {
    Object.keys(PARTS).forEach(function (k) { PARTS[k].mats.forEach(function (m) { m.emissive.setHex(0x000000); m.emissiveIntensity = 1; }); });
    pulse = []; statusColors = []; screenCycle = false; clearHalos();
  }

  P3D.ok = true;
  P3D.mount = function (el) {
    if (!el) return;
    if (canvas.parentNode !== el) el.appendChild(canvas);
    P3D._observe(el);
    resize();
    requestAnimationFrame(resize);
  };
  P3D.focus = function (testId) {
    clearFx(); autoSpin = false; dragOff = { x: 0, y: 0 }; tiltV = { x: 0, y: 0 };
    var p = PARTS[TEST_PART[testId]]; if (!p) return;
    target = { x: p.view.x, y: p.view.y };
    pulse = p.mats.slice();
    p.at.forEach(function (pos) { halo(pos, BLUE, 0.42); });
    if (testId === 'pixels') screenCycle = true;
  };
  P3D.results = function (map) {
    clearFx(); autoSpin = !reduce; dragOff = { x: 0, y: 0 };
    var state = {};
    Object.keys(map).forEach(function (testId) {
      var part = TEST_PART[testId]; if (!part) return;
      var st = map[testId].status;
      if (st === 'ko' || !state[part]) state[part] = st;
      else if (st === 'ok' && state[part] === 'skip') state[part] = 'ok';
    });
    var firstKo = null;
    Object.keys(state).forEach(function (part) {
      var c = state[part] === 'ko' ? RED : state[part] === 'ok' ? GREEN : GREY;
      PARTS[part].mats.forEach(function (m) { statusColors.push({ m: m, c: c, ko: state[part] === 'ko' }); });
      if (state[part] === 'ko') { if (!firstKo) firstKo = part; PARTS[part].at.forEach(function (pos) { halo(pos, RED, 0.42); }); }
    });
    target = firstKo ? { x: PARTS[firstKo].view.x, y: PARTS[firstKo].view.y } : { x: 0.12, y: -0.35 };
  };
  P3D.shake = function () { shakeT = 1.6; };
  P3D.tilt = function (x, y) { tiltV.x = y * 0.6; tiltV.y = x * 0.8; };

  // Rotation au doigt / à la souris
  canvas.addEventListener('pointerdown', function (e) { drag = { x: e.clientX, y: e.clientY, ox: dragOff.x, oy: dragOff.y }; canvas.style.cursor = 'grabbing'; autoSpin = false; });
  window.addEventListener('pointermove', function (e) { if (!drag) return; dragOff.y = drag.oy + (e.clientX - drag.x) * 0.012; dragOff.x = Math.max(-1.2, Math.min(1.2, drag.ox + (e.clientY - drag.y) * 0.008)); });
  window.addEventListener('pointerup', function () { drag = null; canvas.style.cursor = 'grab'; });

  function resize() {
    var p = canvas.parentNode; if (!p) return;
    var w = p.clientWidth || 300, h = p.clientHeight || 260;
    renderer.setSize(w, h, false); camera.aspect = w / h;
    camera.position.z = w / h < 0.9 ? 4.8 : 3.9;
    camera.updateProjectionMatrix();
  }
  window.addEventListener('resize', resize);
  if (window.ResizeObserver) { var ro = new ResizeObserver(function () { resize(); }); P3D._observe = function (el) { ro.disconnect(); ro.observe(el); }; } else { P3D._observe = noop; }

  var clock = new T.Clock(), cycleCols = [new T.Color('#FF2020'), new T.Color('#20FF40'), new T.Color('#2060FF'), new T.Color('#FFFFFF')];
  function frame() {
    requestAnimationFrame(frame);
    if (!canvas.parentNode || !canvas.offsetParent) return;
    var dt = Math.min(clock.getDelta(), 0.05), t = clock.elapsedTime;
    if (autoSpin) target.y += dt * 0.4;
    var gx = target.x + dragOff.x + tiltV.x, gy = target.y + dragOff.y + tiltV.y;
    var k = reduce ? 1 : 1 - Math.pow(0.0025, dt);
    rot.x += (gx - rot.x) * k; rot.y += (gy - rot.y) * k;
    var sway = reduce || autoSpin ? 0 : Math.sin(t * 0.8) * 0.06;
    phone.rotation.set(rot.x, rot.y + sway, 0);
    phone.position.set(0, reduce ? 0 : Math.sin(t * 1.1) * 0.03, 0);
    if (shakeT > 0) { shakeT -= dt; phone.position.x = Math.sin(t * 90) * 0.025 * Math.min(1, shakeT); }
    var pl = 0.55 + 0.45 * Math.sin(t * 4);
    pulse.forEach(function (m) { m.emissive.copy(BLUE); m.emissiveIntensity = reduce ? 0.8 : pl; });
    if (screenCycle) { screenMat.emissive.copy(cycleCols[Math.floor(t / 0.9) % 4]); screenMat.emissiveIntensity = 0.7; }
    halos.forEach(function (h) { var sc = h.userData.base * (reduce ? 1 : 0.8 + 0.35 * Math.sin(t * 4)); h.scale.set(sc, sc, 1); });
    statusColors.forEach(function (s) { s.m.emissive.copy(s.c); s.m.emissiveIntensity = s.ko && !reduce ? pl : 0.7; });
    renderer.render(scene, camera);
  }
  frame();
})();
