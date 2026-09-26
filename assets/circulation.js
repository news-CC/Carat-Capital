/* The Circulation Desk: Carat Capital's own readership counter.
 *
 * No cookies and nothing stored on the reader's device. For each page it
 * reports the address, the title, where the reader came from, and then how
 * long they actively read and how far down the story they got. The collector
 * keeps no IP addresses.
 *
 * Staff can stop counting their own reading on a browser by visiting
 * https://caratcapital.org/?circulation=ignore (and ?circulation=count to undo).
 */
(function () {
  'use strict';
  var script = document.currentScript;
  var endpoint = script && script.getAttribute('data-endpoint');
  if (!endpoint || !navigator.sendBeacon || !window.crypto || navigator.webdriver) return;

  try {
    var opt = new URLSearchParams(location.search).get('circulation');
    if (opt === 'ignore') localStorage.setItem('circulation-ignore', '1');
    if (opt === 'count') localStorage.removeItem('circulation-ignore');
    if (localStorage.getItem('circulation-ignore')) return;
  } catch (e) { /* storage blocked: count as usual */ }

  var url = endpoint.replace(/\/+$/, '') + '/c';
  var id, active, lastTick, lastInput, depth, sentSeconds, sentDepth, framed;

  function meta(property) {
    var m = document.querySelector('meta[property="' + property + '"]');
    return m ? m.getAttribute('content') : '';
  }

  // On a story, depth is measured through the story itself; elsewhere, the page.
  var article = meta('article:published_time') ? document.querySelector('article') : null;

  function send(beacon) {
    try { navigator.sendBeacon(url, JSON.stringify(beacon)); } catch (e) { /* never break the page */ }
  }

  function newId() {
    var a = new Uint32Array(2);
    crypto.getRandomValues(a);
    return (a[0] & 0x1fffff) * 4294967296 + a[1] || 1;
  }

  // How far down the story the reader has seen, in percent.
  function measure() {
    var seen, total;
    if (article) {
      var box = article.getBoundingClientRect();
      seen = innerHeight - box.top;
      total = box.height;
    } else {
      seen = scrollY + innerHeight;
      total = document.documentElement.scrollHeight;
    }
    var pct = total > 0 ? Math.round(Math.max(0, Math.min(1, seen / total)) * 100) : 100;
    if (pct > depth) depth = pct;
  }

  // Reading time: seconds on screen with the reader active in the last 45
  // seconds, so a long paragraph read without touching anything still counts.
  function tick() {
    var now = Date.now();
    if (document.visibilityState === 'visible' && now - lastInput < 45000) {
      active += Math.min(now - lastTick, 15000);
    }
    lastTick = now;
  }

  function flush() {
    tick();
    measure();
    var seconds = Math.round(active / 1000);
    if (seconds > sentSeconds || depth > sentDepth) {
      send({ t: 'e', id: id, s: seconds, d: depth });
      sentSeconds = seconds;
      sentDepth = depth;
    }
  }

  function view(nav) {
    id = newId();
    active = 0; depth = 0; sentSeconds = 0; sentDepth = 0;
    lastTick = lastInput = Date.now();
    send({
      t: 'v', id: id, n: nav,
      u: location.href,
      r: document.referrer,
      ti: meta('og:title') || document.title,
      se: meta('article:section'),
      pu: meta('article:published_time'),
      w: screen.width,
      tp: navigator.maxTouchPoints || 0
    });
    measure();
  }

  function start() {
    var nav = 'navigate';
    try { nav = performance.getEntriesByType('navigation')[0].type || nav; } catch (e) { /* older browsers */ }
    view(nav);
    setInterval(tick, 5000);
    ['scroll', 'wheel', 'keydown', 'pointerdown', 'pointermove', 'touchstart'].forEach(function (type) {
      addEventListener(type, function () { lastInput = Date.now(); }, { passive: true, capture: true });
    });
    addEventListener('scroll', function () {
      if (framed) return;
      framed = true;
      requestAnimationFrame(function () { framed = false; measure(); });
    }, { passive: true });
    document.addEventListener('visibilitychange', function () {
      if (document.visibilityState === 'hidden') flush();
      else lastTick = lastInput = Date.now();
    });
    addEventListener('pagehide', flush);
    // A page restored from the back/forward cache is a fresh view.
    addEventListener('pageshow', function (e) { if (e.persisted) view('back_forward'); });
  }

  // Prerendered pages count only once someone actually opens them.
  if (document.prerendering) document.addEventListener('prerenderingchange', start, { once: true });
  else start();
})();
