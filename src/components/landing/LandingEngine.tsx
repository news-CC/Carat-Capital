"use client";

/**
 * The landing page's living layer: god-ray atmosphere, film grain, the
 * page-transition wipe, and one WebGL particle entity (~9k point sprites)
 * that morphs through the product's story as the visitor scrolls —
 * mist → the empty chair → a handset that becomes a live waveform while
 * the example call plays → ✕ → a particle wave → ascending bars → the
 * chair again. Hand-rolled WebGL: no runtime dependencies.
 *
 * The static markup lives in the server component (page.tsx); this
 * component renders only the fixed background stack and drives the DOM
 * by id/class. Everything is torn down on unmount, so React strict
 * mode's double-invoke in dev is safe.
 */

import { useEffect, useRef } from "react";
import { SAMPLE_CALL } from "@/lib/site";

export default function LandingEngine() {
  const glRef = useRef<HTMLCanvasElement | null>(null);
  const decoRef = useRef<HTMLCanvasElement | null>(null);
  const grainRef = useRef<HTMLDivElement | null>(null);
  const wipeRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const glCanvas = glRef.current;
    const deco = decoRef.current;
    const grainEl = grainRef.current;
    const wipeEl = wipeRef.current;
    if (!glCanvas || !deco || !grainEl || !wipeEl) return;

    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const isMobile = window.matchMedia("(max-width: 760px)").matches;

    let alive = true;
    const cleanups: Array<() => void> = [];
    const on = <K extends keyof WindowEventMap>(
      target: Window | Document,
      type: K | string,
      fn: EventListenerOrEventListenerObject,
      opts?: AddEventListenerOptions,
    ) => {
      target.addEventListener(type as string, fn, opts);
      cleanups.push(() => target.removeEventListener(type as string, fn, opts));
    };

    /* ================= WebGL particle entity ================= */
    const N = isMobile ? 4200 : 9000;
    const gl = glCanvas.getContext("webgl", { alpha: true, antialias: false, premultipliedAlpha: true });
    let W = 0;
    let H = 0;
    let DPR = 1;

    function resizeGL() {
      if (!glCanvas) return;
      DPR = Math.min(window.devicePixelRatio || 1, 2);
      W = window.innerWidth;
      H = window.innerHeight;
      glCanvas.width = Math.round(W * DPR);
      glCanvas.height = Math.round(H * DPR);
      if (gl) gl.viewport(0, 0, glCanvas.width, glCanvas.height);
    }
    resizeGL();

    let aPos = 0;
    let aTint = 0;
    let uPoint: WebGLUniformLocation | null = null;
    let uDim: WebGLUniformLocation | null = null;
    let posBuf: WebGLBuffer | null = null;
    let tintBuf: WebGLBuffer | null = null;

    const tint = new Float32Array(N * 2);
    if (gl) {
      const vsSrc =
        "attribute vec2 p; attribute vec2 t; uniform float dpr; varying vec2 vt;" +
        "void main(){ vt=t; gl_Position=vec4(p,0.,1.); gl_PointSize=t.x*dpr; }";
      const fsSrc =
        "precision mediump float; varying vec2 vt; uniform float dim;" +
        "void main(){ vec2 c=gl_PointCoord-0.5; float d=length(c);" +
        " float a=smoothstep(0.5,0.06,d); a*=a;" +
        " vec3 cold=vec3(0.96,0.97,1.0); vec3 warm=vec3(0.985,0.87,0.72); vec3 rose=vec3(0.94,0.74,0.82);" +
        " float k=vt.y; vec3 col= k<0.5 ? mix(cold,warm,k*2.0) : mix(warm,rose,(k-0.5)*2.0);" +
        " float core=smoothstep(0.16,0.0,d);" +
        " gl_FragColor=vec4(col*(a+core)*dim, a*dim); }";
      const sh = (type: number, src: string) => {
        const s = gl.createShader(type)!;
        gl.shaderSource(s, src);
        gl.compileShader(s);
        return s;
      };
      const prog = gl.createProgram()!;
      gl.attachShader(prog, sh(gl.VERTEX_SHADER, vsSrc));
      gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, fsSrc));
      gl.linkProgram(prog);
      gl.useProgram(prog);
      gl.enable(gl.BLEND);
      gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
      aPos = gl.getAttribLocation(prog, "p");
      aTint = gl.getAttribLocation(prog, "t");
      uPoint = gl.getUniformLocation(prog, "dpr");
      uDim = gl.getUniformLocation(prog, "dim");
      posBuf = gl.createBuffer();
      tintBuf = gl.createBuffer();
    }

    const pos = new Float32Array(N * 2);
    const tgt = new Float32Array(N * 2);
    const seed = new Float32Array(N * 4);
    const barIdx = new Int16Array(N);
    for (let i = 0; i < N; i++) {
      pos[i * 2] = (Math.random() * 2 - 1) * 1.4;
      pos[i * 2 + 1] = (Math.random() * 2 - 1) * 1.4;
      seed[i * 4] = Math.random() * Math.PI * 2;
      seed[i * 4 + 1] = Math.random() * Math.PI * 2;
      seed[i * 4 + 2] = 0.4 + Math.random() * 1.1;
      seed[i * 4 + 3] = Math.random();
      tint[i * 2] = 1.9 + Math.pow(Math.random(), 3.2) * 4.4;
      tint[i * 2 + 1] =
        Math.random() < 0.72 ? Math.random() * 0.3 : Math.random() < 0.75 ? 0.45 + Math.random() * 0.2 : 0.72 + Math.random() * 0.28;
    }
    if (gl && tintBuf) {
      gl.bindBuffer(gl.ARRAY_BUFFER, tintBuf);
      gl.bufferData(gl.ARRAY_BUFFER, tint, gl.STATIC_DRAW);
    }

    /* ---------- shape samplers ---------- */
    const SS = 400;
    const raster = document.createElement("canvas");
    raster.width = SS;
    raster.height = SS;
    const rc = raster.getContext("2d", { willReadFrequently: true })!;

    function samplesFromRaster(draw: (c: CanvasRenderingContext2D) => void): Array<[number, number]> {
      rc.clearRect(0, 0, SS, SS);
      rc.fillStyle = "#fff";
      rc.strokeStyle = "#fff";
      draw(rc);
      const img = rc.getImageData(0, 0, SS, SS).data;
      const pts: Array<[number, number]> = [];
      for (let y = 0; y < SS; y += 2) {
        for (let x = 0; x < SS; x += 2) {
          const a = img[(y * SS + x) * 4 + 3];
          if (a > 90 && Math.random() < a / 300) pts.push([(x / SS) * 2 - 1, 1 - (y / SS) * 2]);
        }
      }
      return pts.length ? pts : [[0, 0]];
    }

    function fillTargets(pts: Array<[number, number]>, cx: number, cy: number, s: number, jitter = 0.012): Float32Array {
      const aspect = W / H;
      const out = new Float32Array(N * 2);
      for (let i = 0; i < N; i++) {
        const p = pts[(i * 7919) % pts.length];
        out[i * 2] = cx + (p[0] * s) / aspect + (Math.random() - 0.5) * jitter;
        out[i * 2 + 1] = cy + p[1] * s + (Math.random() - 0.5) * jitter;
      }
      return out;
    }

    /* the empty salon chair — backrest, armrests, seat, stem, star base */
    function chairShape(cx: number, cy: number, s: number): Float32Array {
      return fillTargets(
        samplesFromRaster((c) => {
          c.lineWidth = 13;
          c.lineCap = "round";
          c.lineJoin = "round";
          c.beginPath();
          c.moveTo(150, 78);
          c.quadraticCurveTo(200, 62, 250, 78);
          c.lineTo(258, 170);
          c.quadraticCurveTo(200, 186, 142, 170);
          c.closePath();
          c.globalAlpha = 0.85;
          c.fill();
          c.globalAlpha = 1;
          c.stroke();
          c.beginPath();
          c.moveTo(118, 176);
          c.quadraticCurveTo(118, 152, 142, 152);
          c.stroke();
          c.beginPath();
          c.moveTo(282, 176);
          c.quadraticCurveTo(282, 152, 258, 152);
          c.stroke();
          c.beginPath();
          c.moveTo(112, 188);
          c.quadraticCurveTo(200, 214, 288, 188);
          c.lineTo(280, 222);
          c.quadraticCurveTo(200, 244, 120, 222);
          c.closePath();
          c.globalAlpha = 0.9;
          c.fill();
          c.globalAlpha = 1;
          c.stroke();
          c.beginPath();
          c.moveTo(200, 244);
          c.lineTo(200, 306);
          c.stroke();
          c.lineWidth = 8;
          ([[122, 344], [278, 344], [166, 352], [234, 352]] as Array<[number, number]>).forEach((w) => {
            c.beginPath();
            c.moveTo(200, 306);
            c.lineTo(w[0], w[1]);
            c.stroke();
            c.beginPath();
            c.arc(w[0], w[1] + 8, 7, 0, Math.PI * 2);
            c.fill();
          });
        }),
        cx,
        cy,
        s,
        0.016,
      );
    }

    function handsetShape(cx: number, cy: number, s: number): Float32Array {
      return fillTargets(
        samplesFromRaster((c) => {
          c.save();
          c.translate(SS / 2, SS / 2);
          c.rotate(-0.62);
          c.translate(-SS / 2, -SS / 2);
          c.lineWidth = 30;
          c.lineCap = "round";
          c.beginPath();
          c.arc(200, 235, 108, Math.PI * 1.02, Math.PI * 1.98);
          c.stroke();
          c.beginPath();
          c.ellipse(92, 240, 40, 52, -0.35, 0, Math.PI * 2);
          c.fill();
          c.beginPath();
          c.ellipse(308, 240, 40, 52, 0.35, 0, Math.PI * 2);
          c.fill();
          c.restore();
        }),
        cx,
        cy,
        s,
        0.014,
      );
    }

    function xShape(cx: number, cy: number, s: number): Float32Array {
      return fillTargets(
        samplesFromRaster((c) => {
          c.lineWidth = 44;
          c.lineCap = "round";
          c.beginPath();
          c.moveTo(96, 96);
          c.lineTo(304, 304);
          c.stroke();
          c.beginPath();
          c.moveTo(304, 96);
          c.lineTo(96, 304);
          c.stroke();
        }),
        cx,
        cy,
        s,
        0.02,
      );
    }

    function mistTargets(): Float32Array {
      const out = new Float32Array(N * 2);
      for (let i = 0; i < N; i++) {
        const a = Math.random() * Math.PI * 2;
        const r = Math.pow(Math.random(), 0.5);
        out[i * 2] = Math.cos(a) * r * 0.55;
        out[i * 2 + 1] = Math.sin(a) * r * 0.42 + 0.05;
      }
      return out;
    }

    function waveTargets(): Float32Array {
      const out = new Float32Array(N * 2);
      for (let i = 0; i < N; i++) {
        const x = Math.random() * 2.4 - 1.2;
        const crest = Math.sin(x * 2.1 + 0.8) * 0.22 + Math.sin(x * 4.7) * 0.08;
        const depth = Math.pow(Math.random(), 2.2);
        out[i * 2] = x;
        out[i * 2 + 1] = -0.28 + crest - depth * 0.5 + Math.random() * 0.05;
      }
      return out;
    }

    function barsTargets(): Float32Array {
      const out = new Float32Array(N * 2);
      const aspect = W / H;
      const bars = [0.16, 0.28, 0.44, 0.62, 0.84];
      const bw = 0.075;
      const cx = isMobile ? 0 : 0.58;
      const base = isMobile ? -1.08 : -0.92;
      for (let i = 0; i < N; i++) {
        const b = i % bars.length;
        out[i * 2] = cx + ((b - 2) * (bw * 2.3)) / aspect + ((Math.random() - 0.5) * (bw * 1.1)) / aspect;
        out[i * 2 + 1] = base + Math.pow(Math.random(), 1.3) * bars[b];
      }
      return out;
    }

    const WAVE_BARS = 42;
    function waveformTargets(): Float32Array {
      const out = new Float32Array(N * 2);
      const aspect = W / H;
      const cx = isMobile ? 0 : -0.4;
      const cy = isMobile ? -0.05 : 0.42;
      const span = isMobile ? 0.8 : 0.5;
      for (let i = 0; i < N; i++) {
        const b = i % WAVE_BARS;
        barIdx[i] = b;
        out[i * 2] = cx + (((b / (WAVE_BARS - 1)) * 2 - 1) * span) / aspect + (Math.random() - 0.5) * 0.008;
        out[i * 2 + 1] = cy + (Math.random() * 2 - 1) * 0.02;
      }
      return out;
    }

    const shapes: Record<string, Float32Array> = {};
    function buildShapes() {
      shapes.hero = chairShape(0, isMobile ? -0.2 : -0.02, isMobile ? 0.42 : 0.62);
      shapes.call = handsetShape(isMobile ? 0 : -0.42, isMobile ? -0.05 : 0.34, isMobile ? 0.38 : 0.44);
      shapes.vow = xShape(0, 0.04, isMobile ? 0.5 : 0.55);
      shapes.how = waveTargets();
      shapes.math = barsTargets();
      shapes.safe = mistTargets();
      shapes.pricing = waveTargets();
      shapes.faq = mistTargets();
      shapes.closing = chairShape(0, isMobile ? 0.2 : 0.12, isMobile ? 0.3 : 0.46);
    }
    buildShapes();

    /* per-scene glow so the entity never fights the reading layer */
    const DIMS: Record<string, number> = { hero: 1, call: 0.95, vow: 1, how: 0.8, math: isMobile ? 0.32 : 0.55, safe: 0.32, pricing: 0.5, faq: 0.3, closing: 1 };
    let dimNow = 1;
    let dimTarget = 1;

    let current = "hero";
    let waveformOn = false;
    let wavePulse = 0;
    let burst = 0;
    tgt.set(shapes.hero);

    function setScene(name: string) {
      if (name === current || !shapes[name]) return;
      current = name;
      waveformOn = name === "call";
      if (waveformOn) shapes.call = waveformTargets();
      burst = 1;
      dimTarget = DIMS[name] !== undefined ? DIMS[name] : 1;
      tgt.set(shapes[name]);
    }

    /* mouse + scroll energy */
    let mx = 0;
    let my = 0;
    let mOn = false;
    on(
      window,
      "pointermove",
      ((e: PointerEvent) => {
        mx = (e.clientX / W) * 2 - 1;
        my = 1 - (e.clientY / H) * 2;
        mOn = true;
      }) as EventListener,
      { passive: true },
    );

    let scrollV = 0;
    let lastY = window.scrollY;
    on(
      window,
      "scroll",
      (() => {
        const y = window.scrollY;
        scrollV += Math.min(Math.abs(y - lastY) / 900, 0.5);
        lastY = y;
      }) as EventListener,
      { passive: true },
    );

    /* ---------- deco layer: wireframe box + dust ---------- */
    const dc = deco.getContext("2d")!;
    let boxAlpha = 0;
    let boxAlphaTarget = 1;
    function resizeDeco() {
      if (!deco) return;
      deco.width = Math.round(W * DPR);
      deco.height = Math.round(H * DPR);
      dc.setTransform(DPR, 0, 0, DPR, 0, 0);
    }
    resizeDeco();

    const dust: Array<{ x: number; y: number; r: number; s: number; ph: number }> = [];
    for (let d = 0; d < (isMobile ? 26 : 60); d++) {
      dust.push({ x: Math.random(), y: Math.random(), r: 0.6 + Math.random() * 1.6, s: 0.004 + Math.random() * 0.012, ph: Math.random() * Math.PI * 2 });
    }

    function drawDeco(t: number) {
      dc.clearRect(0, 0, W, H);
      boxAlpha += (boxAlphaTarget - boxAlpha) * 0.04;
      if (boxAlpha > 0.01) {
        const bw = Math.min(W * 0.34, 430);
        const bh = Math.min(H * 0.62, 520);
        const bx = W / 2 - bw / 2 + Math.sin(t * 0.24) * 6;
        const by = H / 2 - bh / 2 + Math.cos(t * 0.2) * 5;
        dc.save();
        dc.globalAlpha = 0.16 * boxAlpha;
        dc.strokeStyle = "#cdd6e4";
        dc.lineWidth = 1;
        const cols = 7;
        const rows = 9;
        for (let cxi = 0; cxi <= cols; cxi++) {
          const gx = bx + (bw / cols) * cxi;
          dc.beginPath();
          dc.moveTo(gx, by);
          dc.lineTo(gx, by + bh);
          dc.stroke();
        }
        for (let ryi = 0; ryi <= rows; ryi++) {
          const gy = by + (bh / rows) * ryi;
          dc.beginPath();
          dc.moveTo(bx, gy);
          dc.lineTo(bx + bw, gy);
          dc.stroke();
        }
        const grad = dc.createLinearGradient(0, by, 0, by + 46);
        grad.addColorStop(0, "rgba(178,150,220,0.5)");
        grad.addColorStop(1, "rgba(178,150,220,0)");
        dc.globalAlpha = 0.5 * boxAlpha;
        dc.fillStyle = grad;
        dc.fillRect(bx, by, bw, 46);
        dc.restore();
      }
      dc.save();
      for (const p of dust) {
        const px = (p.x + Math.sin(t * p.s * 8 + p.ph) * 0.012) * W;
        const py = ((((p.y - t * p.s * 0.6) % 1) + 1) % 1) * H;
        dc.globalAlpha = 0.12 + 0.1 * Math.sin(t * 1.4 + p.ph);
        dc.fillStyle = "#e8edf6";
        dc.beginPath();
        dc.arc(px, py, p.r, 0, Math.PI * 2);
        dc.fill();
      }
      dc.restore();
    }

    /* ---------- frame loop ---------- */
    let rafId = 0;
    const start = performance.now();
    function frame(now: number) {
      if (!alive) return;
      const t = (now - start) / 1000;
      scrollV *= 0.9;
      burst *= 0.94;
      if (waveformOn) wavePulse *= 0.95;
      const aspect = W / H;

      for (let i = 0; i < N; i++) {
        const ix = i * 2;
        const iy = ix + 1;
        let tx = tgt[ix];
        let ty = tgt[iy];

        const s0 = seed[i * 4];
        const s1 = seed[i * 4 + 1];
        const sp = seed[i * 4 + 2];
        const rv = seed[i * 4 + 3];
        const wan = 0.012 + burst * 0.5 + scrollV * 0.1;
        tx += Math.sin(t * sp + s0) * wan + Math.sin(t * 0.31 + s1 * 3.1) * 0.008;
        ty += Math.cos(t * sp * 0.9 + s1) * wan + Math.cos(t * 0.27 + s0 * 2.3) * 0.008;

        if (waveformOn) {
          const b = barIdx[i];
          const amp = 0.06 + 0.05 * Math.sin(t * 2.2 + b * 0.55) + wavePulse * 0.22 * Math.sin(b * 0.9 + t * 9);
          ty += (rv * 2 - 1) * Math.max(amp, 0.015);
        }

        if (burst > 0.02) {
          const dx0 = pos[ix];
          const dy0 = pos[iy];
          const dd = Math.sqrt(dx0 * dx0 + dy0 * dy0) + 0.001;
          tx += (dx0 / dd) * burst * 0.5 * rv;
          ty += (dy0 / dd) * burst * 0.5 * rv;
        }

        if (mOn) {
          const dxm = pos[ix] - mx;
          const dym = pos[iy] - my;
          const d2 = dxm * dxm * aspect * aspect + dym * dym;
          if (d2 < 0.03) {
            const f = (0.03 - d2) * 2.4;
            tx += dxm * f;
            ty += dym * f;
          }
        }

        const k = 0.045 + rv * 0.035;
        pos[ix] += (tx - pos[ix]) * k;
        pos[iy] += (ty - pos[iy]) * k;
      }

      if (gl && posBuf && tintBuf) {
        gl.clearColor(0, 0, 0, 0);
        gl.clear(gl.COLOR_BUFFER_BIT);
        gl.bindBuffer(gl.ARRAY_BUFFER, posBuf);
        gl.bufferData(gl.ARRAY_BUFFER, pos, gl.DYNAMIC_DRAW);
        gl.enableVertexAttribArray(aPos);
        gl.vertexAttribPointer(aPos, 2, gl.FLOAT, false, 0, 0);
        gl.bindBuffer(gl.ARRAY_BUFFER, tintBuf);
        gl.enableVertexAttribArray(aTint);
        gl.vertexAttribPointer(aTint, 2, gl.FLOAT, false, 0, 0);
        dimNow += (dimTarget - dimNow) * 0.03;
        gl.uniform1f(uPoint, DPR);
        gl.uniform1f(uDim, dimNow);
        gl.drawArrays(gl.POINTS, 0, N);
      }

      drawDeco(t);
      if (!document.hidden && !reduceMotion) rafId = requestAnimationFrame(frame);
    }

    const onResize = () => {
      resizeGL();
      resizeDeco();
      buildShapes();
      if (shapes[current]) tgt.set(shapes[current]);
    };
    on(window, "resize", onResize as EventListener);

    if (reduceMotion) {
      for (let r = 0; r < 220; r++) for (let i = 0; i < N * 2; i++) pos[i] += (tgt[i] - pos[i]) * 0.08;
      frame(performance.now());
    } else {
      rafId = requestAnimationFrame(frame);
    }
    on(document, "visibilitychange", (() => {
      if (!document.hidden && !reduceMotion && alive) rafId = requestAnimationFrame(frame);
    }) as EventListener);
    cleanups.push(() => cancelAnimationFrame(rafId));

    /* ---------- film grain ---------- */
    {
      const g = document.createElement("canvas");
      g.width = 160;
      g.height = 160;
      const gc = g.getContext("2d")!;
      const img = gc.createImageData(160, 160);
      for (let i = 0; i < img.data.length; i += 4) {
        const v = (Math.random() * 255) | 0;
        img.data[i] = v;
        img.data[i + 1] = v;
        img.data[i + 2] = v;
        img.data[i + 3] = 30;
      }
      gc.putImageData(img, 0, 0);
      grainEl.style.background = "url(" + g.toDataURL() + ")";
      if (!reduceMotion) {
        let step = 0;
        const grainTimer = window.setInterval(() => {
          step = (step + 1) % 3;
          grainEl.style.transform = "translate(" + step * 37 + "px," + ((step * 53) % 100) + "px)";
        }, 130);
        cleanups.push(() => window.clearInterval(grainTimer));
      }
    }

    /* ================= scroll orchestration ================= */
    let lastWipe = 0;
    const WIPE_SCENES: Record<string, 1> = { how: 1, closing: 1 };
    const sceneObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((en) => {
          if (!en.isIntersecting) return;
          const name = en.target.getAttribute("data-scene");
          if (name && name !== current) {
            const nowT = performance.now();
            if (!reduceMotion && WIPE_SCENES[name] && nowT - lastWipe > 2600) {
              lastWipe = nowT;
              wipeEl.classList.remove("sweep");
              void wipeEl.offsetWidth;
              wipeEl.classList.add("sweep");
              window.setTimeout(() => setScene(name), 240);
            } else {
              setScene(name);
            }
          }
          if (name) boxAlphaTarget = name === "hero" || name === "closing" ? 1 : 0;
        });
      },
      { threshold: 0.42 },
    );
    document.querySelectorAll("[data-scene]").forEach((s) => sceneObserver.observe(s));
    cleanups.push(() => sceneObserver.disconnect());

    /* reveal groups */
    const revealObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((en) => {
          if (en.isIntersecting) {
            en.target.classList.add("lon");
            revealObserver.unobserve(en.target);
          }
        });
      },
      { threshold: 0.16 },
    );
    document.querySelectorAll("[data-reveal]").forEach((el) => revealObserver.observe(el));
    cleanups.push(() => revealObserver.disconnect());

    /* closing title: per-letter blur reveal */
    const closingTitle = document.getElementById("closing-title");
    if (closingTitle && !closingTitle.dataset.split) {
      closingTitle.dataset.split = "1";
      const text = closingTitle.textContent || "";
      closingTitle.textContent = "";
      text.split("").forEach((ch, idx) => {
        const sp = document.createElement("span");
        if (ch === " ") sp.innerHTML = "&nbsp;";
        else sp.textContent = ch;
        sp.style.setProperty("--ld", idx * 0.045 + "s");
        closingTitle.appendChild(sp);
      });
    }
    if (closingTitle) {
      const io = new IntersectionObserver(
        (entries) => {
          entries.forEach((en) => {
            if (en.isIntersecting) {
              closingTitle.classList.add("lon");
              io.unobserve(closingTitle);
            }
          });
        },
        { threshold: 0.4 },
      );
      io.observe(closingTitle);
      cleanups.push(() => io.disconnect());
    }

    /* ================= the call — transcript playback ================= */
    const SCRIPT = SAMPLE_CALL.lines;
    const chat = document.getElementById("chat");
    const timerEl = document.getElementById("call-timer");
    let playToken = 0;
    const timeouts: number[] = [];
    const later = (fn: () => void, ms: number) => {
      const id = window.setTimeout(fn, ms);
      timeouts.push(id);
      return id;
    };
    cleanups.push(() => timeouts.forEach((id) => window.clearTimeout(id)));

    function renderAll() {
      if (!chat || !timerEl) return;
      chat.innerHTML = "";
      SCRIPT.forEach((line) => {
        const d = document.createElement("div");
        d.className = "msgl show " + (line.agent ? "msgl-agent" : "msgl-human");
        d.innerHTML = "<span class='who'>" + line.who + "</span>" + line.text;
        chat.appendChild(d);
      });
      chat.scrollTop = chat.scrollHeight;
      timerEl.textContent = "1:30";
    }

    function playScript() {
      if (!chat || !timerEl) return;
      const token = ++playToken;
      chat.innerHTML = "";
      const typing = document.createElement("div");
      typing.className = "typing";
      typing.innerHTML = "<i></i><i></i><i></i>";
      chat.appendChild(typing);
      let t0: number | null = null;
      const tick = () => {
        if (token !== playToken || !alive) return;
        if (t0 === null) t0 = Date.now();
        const s = Math.floor((Date.now() - t0) / 1000);
        timerEl.textContent = Math.floor(s / 60) + ":" + ("0" + (s % 60)).slice(-2);
        if (s < 95) later(tick, 1000);
      };
      tick();
      let i = 0;
      const next = () => {
        if (token !== playToken || !alive || !chat) return;
        if (i >= SCRIPT.length) {
          typing.remove();
          return;
        }
        const line = SCRIPT[i++];
        typing.classList.toggle("show", line.agent);
        chat.appendChild(typing);
        chat.scrollTop = chat.scrollHeight;
        later(() => {
          if (token !== playToken || !alive || !chat) return;
          typing.classList.remove("show");
          const d = document.createElement("div");
          d.className = "msgl " + (line.agent ? "msgl-agent" : "msgl-human");
          d.innerHTML = "<span class='who'>" + line.who + "</span>" + line.text;
          chat.insertBefore(d, typing);
          chat.scrollTop = chat.scrollHeight;
          requestAnimationFrame(() => requestAnimationFrame(() => d.classList.add("show")));
          later(() => chat.scrollTo({ top: chat.scrollHeight, behavior: "smooth" }), 60);
          if (line.agent) wavePulse = 1;
          later(next, 650 + Math.min(line.text.length * 14, 1500));
        }, line.agent ? 950 : 700);
      };
      next();
    }

    const transcript = document.getElementById("transcript");
    if (reduceMotion || !("IntersectionObserver" in window)) {
      renderAll();
    } else if (transcript) {
      const trIO = new IntersectionObserver(
        (entries) => {
          entries.forEach((en) => {
            if (en.isIntersecting) {
              playScript();
              trIO.unobserve(en.target);
            }
          });
        },
        { threshold: 0.35 },
      );
      trIO.observe(transcript);
      cleanups.push(() => trIO.disconnect());
    }
    const replayBtn = document.getElementById("replay");
    const onReplay = () => {
      if (reduceMotion) renderAll();
      else playScript();
    };
    replayBtn?.addEventListener("click", onReplay);
    cleanups.push(() => replayBtn?.removeEventListener("click", onReplay));

    /* ---------- funnel bars + count-up ---------- */
    const funnel = document.getElementById("funnel");
    const fmt = (n: number) => n.toLocaleString("en-US");
    function runFunnel() {
      if (!funnel) return;
      funnel.querySelectorAll<HTMLElement>(".bar").forEach((bar) => {
        bar.style.width = bar.getAttribute("data-w") + "%";
      });
      if (reduceMotion) return;
      funnel.querySelectorAll<HTMLElement>(".fn").forEach((el, idx) => {
        const target = parseInt(el.getAttribute("data-count") || "0", 10);
        let t0: number | null = null;
        const dur = 1100 + idx * 120;
        const stepCount = (ts: number) => {
          if (!alive) return;
          if (t0 === null) t0 = ts;
          const p = Math.min((ts - t0) / dur, 1);
          el.textContent = fmt(Math.round(target * (1 - Math.pow(1 - p, 3))));
          if (p < 1) requestAnimationFrame(stepCount);
        };
        requestAnimationFrame(stepCount);
      });
    }
    if (funnel) {
      if (reduceMotion) {
        runFunnel();
      } else {
        const fIO = new IntersectionObserver(
          (entries) => {
            entries.forEach((en) => {
              if (en.isIntersecting) {
                runFunnel();
                fIO.unobserve(funnel);
              }
            });
          },
          { threshold: 0.3 },
        );
        fIO.observe(funnel);
        cleanups.push(() => fIO.disconnect());
      }
    }

    /* ---------- contact strip → /start ---------- */
    const form = document.getElementById("contact-form") as HTMLFormElement | null;
    const onSubmit = (e: Event) => {
      e.preventDefault();
      const name = (document.getElementById("cf-name") as HTMLInputElement | null)?.value.trim() || "";
      const email = (document.getElementById("cf-email") as HTMLInputElement | null)?.value.trim() || "";
      const params = new URLSearchParams();
      if (name) params.set("name", name);
      if (email) params.set("email", email);
      const qs = params.toString();
      window.location.href = "/start" + (qs ? "?" + qs : "");
    };
    form?.addEventListener("submit", onSubmit);
    cleanups.push(() => form?.removeEventListener("submit", onSubmit));

    return () => {
      alive = false;
      cleanups.forEach((fn) => fn());
    };
  }, []);

  return (
    <>
      <div className="atmos" aria-hidden="true">
        <div className="beam beam-a" />
        <div className="beam beam-b" />
        <div className="beam beam-c" />
        <div className="beam beam-d" />
      </div>
      <canvas id="deco" ref={decoRef} aria-hidden="true" />
      <canvas id="gl" ref={glRef} aria-hidden="true" />
      <div id="grain" ref={grainRef} aria-hidden="true" />
      <div id="vignette" aria-hidden="true" />
      <div id="wipe" ref={wipeRef} aria-hidden="true" />
    </>
  );
}
