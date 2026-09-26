// The Circulation Desk: the dashboard client. Plain DOM and SVG, no framework.
//
// Titles, referrers and campaign names arrive from public beacons, so they are
// untrusted: they only ever reach the page through textContent, never markup.

const $ = (sel, root = document) => root.querySelector(sel);
const NS = 'http://www.w3.org/2000/svg';

function el(tag, attrs = {}, ...kids) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) if (v != null && v !== false) node.setAttribute(k, v === true ? '' : v);
  for (const kid of kids.flat()) if (kid != null && kid !== false) node.append(kid instanceof Node ? kid : String(kid));
  return node;
}

function svg(tag, attrs = {}, ...kids) {
  const node = document.createElementNS(NS, tag);
  for (const [k, v] of Object.entries(attrs)) if (v != null) node.setAttribute(k, v);
  for (const kid of kids.flat()) if (kid != null) node.append(kid instanceof Node ? kid : String(kid));
  return node;
}

const store = {
  get(k, fallback) { try { return localStorage.getItem(k) ?? fallback; } catch { return fallback; } },
  set(k, v) { try { localStorage.setItem(k, v); } catch { /* private mode */ } },
};

// ── Vocabulary ───────────────────────────────────────────

const RANGES = ['today', '7d', '30d', '90d', '12m'];
const SPAN = { today: 'so far today', '7d': 'over seven days', '30d': 'over 30 days', '90d': 'over 90 days', '12m': 'over 12 months' };
const VERSUS = { today: 'vs this time yesterday', '7d': 'vs previous 7 days', '30d': 'vs previous 30 days', '90d': 'vs previous 90 days', '12m': 'vs previous 12 months' };

const DESKS = {
  diamonds: { no: '01', name: 'Diamonds' },
  'gold-metals': { no: '02', name: 'Gold & Metals' },
  gemstones: { no: '03', name: 'Colored Gemstones' },
  watches: { no: '04', name: 'Watches' },
  auctions: { no: '05', name: 'Auctions & Estates' },
  'retail-tech': { no: '06', name: 'Retail & Technology' },
};
const deskName = (slug) => DESKS[slug]?.name || slug || 'No desk';
const deskCode = (slug) => (DESKS[slug] ? `D-${DESKS[slug].no}` : '');

const CHANNELS = {
  Search: 'Search', Social: 'Social', AI: 'AI assistants', Email: 'Newsletter & email',
  Paid: 'Paid', Referral: 'Other sites', Direct: 'Direct & bookmarks',
};
const CHANNEL_PHRASE = {
  Search: 'search', Social: 'social networks', AI: 'AI assistants', Email: 'newsletters and email',
  Paid: 'paid links', Referral: 'other sites', Direct: 'direct visits and bookmarks',
};

const SOURCES = {
  'google.com': 'Google', 'news.google.com': 'Google News', 'discover.google.com': 'Google Discover',
  'bing.com': 'Bing', 'duckduckgo.com': 'DuckDuckGo', 'yahoo.com': 'Yahoo', 'yandex.com': 'Yandex',
  'baidu.com': 'Baidu', 'ecosia.org': 'Ecosia', 'search.brave.com': 'Brave Search', 'naver.com': 'Naver',
  'chatgpt.com': 'ChatGPT', 'perplexity.ai': 'Perplexity', 'claude.ai': 'Claude', 'gemini.google.com': 'Gemini',
  'copilot.microsoft.com': 'Copilot', 'instagram.com': 'Instagram', 'facebook.com': 'Facebook', 'x.com': 'X',
  'linkedin.com': 'LinkedIn', 'tiktok.com': 'TikTok', 'pinterest.com': 'Pinterest', 'reddit.com': 'Reddit',
  'youtube.com': 'YouTube', 'threads.net': 'Threads', 'bsky.app': 'Bluesky', 'whatsapp.com': 'WhatsApp',
  'telegram.org': 'Telegram', 'mail.google.com': 'Gmail', 'outlook.live.com': 'Outlook',
  'news.ycombinator.com': 'Hacker News', 'feedly.com': 'Feedly', 'flipboard.com': 'Flipboard',
  'inoreader.com': 'Inoreader', newsletter: 'Newsletter',
};
const sourceName = (host) => SOURCES[host] || host;

const PAGES = {
  '/': 'Front page', '/diamonds': 'Diamonds desk', '/gold-metals': 'Gold & Metals desk',
  '/gemstones': 'Colored Gemstones desk', '/watches': 'Watches desk', '/auctions': 'Auctions & Estates desk',
  '/retail-tech': 'Retail & Technology desk', '/indices': 'The Carat indices',
  '/natural-diamond-prices': 'Natural diamond prices', '/lab-grown-diamond-prices': 'Lab-grown diamond prices',
  '/the-record': 'The Record', '/almanac': 'The Almanac', '/field-guide': 'The Field Guide',
  '/magazine': 'The Magazine', '/about': 'About the paper', '/privacy': 'Privacy', '/terms': 'Terms',
};

const regions = (() => { try { return new Intl.DisplayNames(['en'], { type: 'region' }); } catch { return null; } })();
function countryName(code) {
  if (!code || code === 'XX') return 'Unknown';
  if (code === 'T1') return 'Tor network';
  try { return regions?.of(code) || code; } catch { return code; }
}

// ── Numbers and dates ────────────────────────────────────

const whole = new Intl.NumberFormat('en-US', { maximumFractionDigits: 0 });
const compact = new Intl.NumberFormat('en-US', { notation: 'compact', maximumFractionDigits: 1 });
const fmtInt = (n) => whole.format(Math.round(n || 0));
const fmtBig = (n) => (n >= 100000 ? compact.format(n) : fmtInt(n));
const fmtPct = (f, digits = 0) => (f == null || !Number.isFinite(f) ? '—' : `${(f * 100).toFixed(digits)}%`);
function fmtDur(s) {
  if (s == null || !Number.isFinite(s)) return '—';
  s = Math.round(s);
  if (s < 60) return `${s}s`;
  const m = Math.floor(s / 60);
  if (m < 60) return `${m}m ${String(s % 60).padStart(2, '0')}s`;
  return `${Math.floor(m / 60)}h ${String(m % 60).padStart(2, '0')}m`;
}
const plural = (n, word) => `${word}${Math.round(n) === 1 ? '' : 's'}`;
const WORDS = ['no', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'];
/** A count in the paper's prose style: one to nine in words, larger numbers in figures. */
const say = (n, word, cap = false) => {
  const r = Math.round(n);
  const figure = r >= 0 && r < 10 ? WORDS[r] : fmtInt(r);
  return `${cap ? figure[0].toUpperCase() + figure.slice(1) : figure} ${plural(r, word)}`;
};

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const MONTHS_LONG = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
const DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
const DAYS_LONG = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const asDate = (d) => { const [y, m, dd] = d.split('-').map(Number); return new Date(Date.UTC(y, m - 1, dd)); };
const fmtDay = (d, year = false) => { const t = asDate(d); return `${t.getUTCDate()} ${MONTHS[t.getUTCMonth()]}${year ? ` ${t.getUTCFullYear()}` : ''}`; };
const fmtDayShort = (d) => { const t = asDate(d); return `${DAYS[t.getUTCDay()]} ${t.getUTCDate()} ${MONTHS[t.getUTCMonth()]}`; };
const fmtDayLong = (d) => { const t = asDate(d); return `${DAYS_LONG[t.getUTCDay()]} ${t.getUTCDate()} ${MONTHS_LONG[t.getUTCMonth()]} ${t.getUTCFullYear()}`; };
const fmtHour = (h) => `${String(h).padStart(2, '0')}:00`;

function clockIn(tz, ms) {
  const parts = new Intl.DateTimeFormat('en-GB', { timeZone: tz, hour: '2-digit', minute: '2-digit', hourCycle: 'h23' }).formatToParts(new Date(ms));
  const get = (t) => Number(parts.find((p) => p.type === t)?.value);
  return { h: get('hour'), m: get('minute') };
}

function spanLabel(d) {
  if (d.range === 'today') return fmtDayLong(d.today);
  const sameYear = d.from.slice(0, 4) === d.to.slice(0, 4);
  return `${fmtDay(d.from, !sameYear)} – ${fmtDay(d.to, true)}`;
}

// ── Metrics ──────────────────────────────────────────────

const SUMS = ['views', 'readers', 'visits', 'engaged', 'engaged_n', 'reads', 'articles'];
const METRICS = {
  readers: { label: 'Readers', kind: 'count', of: (s) => s.readers, fmt: fmtBig },
  views: { label: 'Pageviews', kind: 'count', of: (s) => s.views, fmt: fmtBig },
  visits: { label: 'Visits', kind: 'count', of: (s) => s.visits, fmt: fmtBig },
  time: { label: 'Reading time', kind: 'duration', of: (s) => (s.engaged_n ? s.engaged / s.engaged_n : null), fmt: fmtDur, note: 'per pageview' },
  read: { label: 'Read-through', kind: 'ratio', of: (s) => (s.articles ? s.reads / s.articles : null), fmt: (v) => fmtPct(v), note: 'of story views' },
};

function change(cur, prev, kind) {
  if (cur == null || prev == null || !Number.isFinite(cur) || !Number.isFinite(prev)) return null;
  if (kind === 'ratio') {
    const pts = (cur - prev) * 100;
    return { dir: Math.abs(pts) < 0.05 ? 'flat' : pts > 0 ? 'up' : 'down', text: `${Math.abs(pts).toFixed(1)} pts` };
  }
  if (!prev) return null;
  const pct = ((cur - prev) / prev) * 100;
  const size = Math.abs(pct);
  return { dir: size < 0.05 ? 'flat' : pct > 0 ? 'up' : 'down', text: `${size >= 10 ? Math.round(size) : size.toFixed(1)}%`, pct };
}

function deltaChip(c) {
  const glyph = c.dir === 'up' ? '▲' : c.dir === 'down' ? '▼' : '■';
  const words = c.dir === 'up' ? 'up' : c.dir === 'down' ? 'down' : 'level,';
  return el('span', { class: `delta ${c.dir}` }, el('span', { 'aria-hidden': 'true' }, `${glyph} `), el('span', { class: 'sr' }, `${words} `), c.text);
}

/** Seven-day buckets ending on the last day; rates are recomputed from the sums. */
function weekly(series) {
  const out = [];
  for (let end = series.length; end >= 7; end -= 7) {
    const chunk = series.slice(end - 7, end);
    const sum = { key: chunk[0].key, week: true };
    for (const k of SUMS) sum[k] = chunk.reduce((a, s) => a + (s[k] || 0), 0);
    out.unshift(sum);
  }
  return out;
}
const bucket = (series, range) => (range === '12m' ? weekly(series) : series);

// ── State and API ────────────────────────────────────────

const state = {
  range: RANGES.includes(store.get('circulation-range')) ? store.get('circulation-range') : '30d',
  metric: METRICS[store.get('circulation-metric')] ? store.get('circulation-metric') : 'readers',
  data: null,
  tz: 'America/New_York',
  showAllStories: false,
  firstLoad: true,
  timers: [],
  redraws: new Map(),
};

class ApiError extends Error {
  constructor(code, status) { super(code); this.code = code; this.status = status; }
}

async function api(path, options = {}) {
  const res = await fetch(path, { credentials: 'same-origin', headers: { Accept: 'application/json' }, ...options });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw new ApiError(body.error || 'server-error', res.status);
  return body;
}

function notice(text) {
  $('#notice').hidden = !text;
  $('#notice-text').textContent = text || '';
}

function explain(e) {
  if (e.code === 'daily-limit') return 'Cloudflare’s free database allowance for today is used up, so the desk pauses until midnight UTC (8 pm in New York). New visits are not recorded until then.';
  return 'The desk could not fetch the figures just now. It will try again shortly.';
}

// ── Sign-in ──────────────────────────────────────────────

function showGate(code) {
  stopTimers();
  $('#desk').hidden = true;
  $('#gate').hidden = false;
  const form = $('#gate-form');
  const configured = code !== 'not-configured';
  $('#gate-note').textContent = configured
    ? 'Readership figures for caratcapital.org. Staff only.'
    : 'This desk has no password yet. Set the DASHBOARD_PASSWORD secret on the Worker (see the README), then reload.';
  for (const f of form.elements) f.disabled = !configured;
  if (configured) $('#gate-password').focus();
}

$('#gate-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const button = $('#gate-submit');
  const error = $('#gate-error');
  const password = $('#gate-password').value;
  if (!password) { error.textContent = 'Enter the desk password.'; return; }
  button.disabled = true;
  error.textContent = '';
  try {
    await api('/api/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ password }) });
    $('#gate-password').value = '';
    $('#gate').hidden = true;
    await boot();
  } catch (e) {
    error.textContent = e.code === 'wrong-password' ? 'That password did not open the desk.'
      : e.code === 'slow-down' ? 'Too many tries. Wait a minute, then try again.'
        : e.code === 'not-configured' ? 'The desk has no password set yet.'
          : 'The desk did not answer. Try again in a moment.';
    $('#gate-password').select();
  } finally {
    button.disabled = false;
  }
});

$('#sign-out').addEventListener('click', async () => {
  try { await api('/api/logout', { method: 'POST' }); } catch { /* signed out either way */ }
  showGate('signed-out');
});

// ── Editions (themes) ────────────────────────────────────

function edition() {
  return document.documentElement.dataset.theme || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
}
function labelEdition() {
  const next = edition() === 'dark' ? 'Paper' : 'Carbon';
  const button = $('#theme-toggle');
  button.textContent = next;
  button.setAttribute('aria-label', `Switch to the ${next} edition`);
}
$('#theme-toggle').addEventListener('click', () => {
  const next = edition() === 'dark' ? 'light' : 'dark';
  document.documentElement.dataset.theme = next;
  store.set('circulation-theme', next);
  labelEdition();
});
matchMedia('(prefers-color-scheme: dark)').addEventListener?.('change', labelEdition);

// ── Tooltip ──────────────────────────────────────────────

const tip = $('#tip');

function showTip(title, rows, x, y) {
  tip.replaceChildren(el('div', { class: 'tip-title' }, title));
  for (const r of rows) {
    tip.append(el('div', { class: 'tip-row' },
      r.key ? el('span', { class: `key${r.key === 'ctx' ? ' ctx' : ''}` }) : null,
      el('strong', {}, r.value), r.label ? el('span', {}, r.label) : null));
  }
  tip.hidden = false;
  const w = tip.offsetWidth, h = tip.offsetHeight;
  let left = x + 14, top = y - h - 12;
  if (left + w > innerWidth - 8) left = x - w - 14;
  if (left < 8) left = 8;
  if (top < 8) top = y + 16;
  tip.style.left = `${Math.round(left)}px`;
  tip.style.top = `${Math.round(top)}px`;
}
const hideTip = () => { tip.hidden = true; };
addEventListener('scroll', hideTip, { passive: true });

// ── Charts ───────────────────────────────────────────────

function niceScale(max, kind) {
  if (!(max > 0)) return { top: kind === 'ratio' ? 1 : kind === 'duration' ? 60 : 4, step: kind === 'ratio' ? 0.25 : kind === 'duration' ? 15 : 1 };
  const raw = max / 4;
  const mag = 10 ** Math.floor(Math.log10(raw));
  const n = raw / mag;
  let step = (n <= 1 ? 1 : n <= 2 ? 2 : n <= 2.5 ? 2.5 : n <= 5 ? 5 : 10) * mag;
  if (kind === 'count') step = Math.max(1, Math.round(step));
  if (kind === 'duration' && step >= 30) step = Math.ceil(step / 30) * 30;
  return { top: Math.ceil(max / step - 1e-9) * step, step };
}

function tickText(v, kind) {
  if (kind === 'ratio') return `${Math.round(v * 100)}%`;
  if (kind === 'duration') return v >= 60 ? `${Math.floor(v / 60)}m${v % 60 ? ` ${Math.round(v % 60)}s` : ''}` : `${Math.round(v)}s`;
  return v >= 10000 ? compact.format(v) : fmtInt(v);
}

function roundedTop(x, y, w, h, r) {
  if (h <= 0 || w <= 0) return '';
  r = Math.min(r, w / 2, h);
  return `M${x},${y + h}V${y + r}A${r},${r} 0 0 1 ${x + r},${y}H${x + w - r}A${r},${r} 0 0 1 ${x + w},${y + r}V${y + h}Z`;
}

function linePath(points) {
  let d = '';
  let pen = false;
  for (const p of points) {
    if (p == null) { pen = false; continue; }
    d += `${pen ? 'L' : 'M'}${p[0].toFixed(1)},${p[1].toFixed(1)}`;
    pen = true;
  }
  return d;
}

function areaPath(points, base) {
  let d = '';
  let run = [];
  const close = () => {
    if (run.length > 1) d += `M${run[0][0]},${base}L${run.map((p) => `${p[0].toFixed(1)},${p[1].toFixed(1)}`).join('L')}L${run[run.length - 1][0]},${base}Z`;
    run = [];
  };
  for (const p of points) { if (p == null) close(); else run.push(p); }
  close();
  return d;
}

/** Hover and arrow-key reading for a chart indexed along x. */
function readable(root, count, xAt, show, hide) {
  let current = -1;
  const pick = (i, clientX, clientY) => { current = Math.max(0, Math.min(count - 1, i)); show(current, clientX, clientY); };
  root.addEventListener('pointermove', (e) => {
    const box = root.getBoundingClientRect();
    const x = e.clientX - box.left;
    let best = 0;
    let bestGap = Infinity;
    for (let i = 0; i < count; i++) {
      const gap = Math.abs(xAt(i) - x);
      if (gap < bestGap) { best = i; bestGap = gap; }
    }
    pick(best, e.clientX, e.clientY);
  });
  root.addEventListener('pointerleave', () => { current = -1; hide(); });
  root.addEventListener('blur', () => { current = -1; hide(); });
  root.addEventListener('keydown', (e) => {
    if (!['ArrowLeft', 'ArrowRight', 'Home', 'End', 'Escape'].includes(e.key)) return;
    e.preventDefault();
    if (e.key === 'Escape') { current = -1; hide(); return; }
    const next = e.key === 'Home' ? 0 : e.key === 'End' ? count - 1
      : current < 0 ? count - 1 : current + (e.key === 'ArrowRight' ? 1 : -1);
    const box = root.getBoundingClientRect();
    pick(next, box.left + xAt(Math.max(0, Math.min(count - 1, next))), box.top + 40);
  });
}

/**
 * A line for the chosen metric over the period, with the previous period as a
 * gray context line on the same axis (same unit, so one scale is honest).
 */
function trendChart(host, { labels, current, context, contextLabels, kind, name, contextName }) {
  const W = Math.max(280, host.clientWidth);
  const H = 292;
  const values = [...current, ...context].filter((v) => v != null);
  const { top: maxV, step } = niceScale(Math.max(0, ...values), kind);
  const ticks = [];
  for (let v = 0; v <= maxV + step / 2; v += step) ticks.push(v);
  const tickW = Math.max(...ticks.map((t) => tickText(t, kind).length)) * 6.6 + 10;
  const lastIdx = current.reduce((acc, v, i) => (v != null ? i : acc), -1);
  const endText = lastIdx >= 0 ? METRIC_FMT(kind)(current[lastIdx]) : '';
  const m = { l: tickW, r: Math.max(18, endText.length * 7.2 + 16), t: 14, b: 30 };
  const pw = W - m.l - m.r;
  const ph = H - m.t - m.b;
  const n = labels.length;
  const x = (i) => m.l + (n === 1 ? pw / 2 : (i * pw) / (n - 1));
  const y = (v) => m.t + ph * (1 - v / maxV);

  const root = svg('svg', {
    viewBox: `0 0 ${W} ${H}`, width: W, height: H, tabindex: '0', role: 'img',
    'aria-label': `${name}: ${labels.length} points. Use the arrow keys to read values.`,
  });
  for (const t of ticks) {
    root.append(svg('line', { class: t === 0 ? 'baseline' : 'gridline', x1: m.l, x2: W - m.r, y1: y(t), y2: y(t) }));
    root.append(svg('text', { class: 'tick', x: m.l - 10, y: y(t) + 4, 'text-anchor': 'end' }, tickText(t, kind)));
  }
  const every = Math.max(1, Math.ceil(n / Math.max(2, Math.floor(pw / 86))));
  for (let i = 0; i < n; i += every) {
    root.append(svg('text', { class: 'tick', x: x(i), y: H - 8, 'text-anchor': i === 0 && n > 1 ? 'start' : 'middle' }, labels[i]));
  }
  const pts = (arr) => arr.map((v, i) => (v == null ? null : [x(i), y(v)]));
  const ctxPts = pts(context);
  const curPts = pts(current);
  root.append(svg('path', { class: 'series-ctx', d: linePath(ctxPts) }));
  root.append(svg('path', { class: 'wash', d: areaPath(curPts, y(0)) }));
  root.append(svg('path', { class: 'series', d: linePath(curPts) }));
  if (lastIdx >= 0) {
    root.append(svg('circle', { class: 'mark', cx: x(lastIdx), cy: y(current[lastIdx]), r: 4.5 }));
    root.append(svg('text', { class: 'end-label', x: x(lastIdx) + 9, y: y(current[lastIdx]) + 4 }, endText));
  }
  const cross = svg('line', { class: 'crosshair', y1: m.t, y2: m.t + ph, visibility: 'hidden' });
  const dotCtx = svg('circle', { class: 'mark-ctx', r: 4.5, visibility: 'hidden' });
  const dotCur = svg('circle', { class: 'mark', r: 4.5, visibility: 'hidden' });
  root.append(cross, dotCtx, dotCur, svg('rect', { class: 'hit', x: m.l, y: m.t, width: pw, height: ph }));
  const f = METRIC_FMT(kind);
  readable(root, n, x, (i, cx, cy) => {
    cross.setAttribute('x1', x(i)); cross.setAttribute('x2', x(i)); cross.setAttribute('visibility', 'visible');
    for (const [dot, v] of [[dotCur, current[i]], [dotCtx, context[i]]]) {
      if (v == null) { dot.setAttribute('visibility', 'hidden'); continue; }
      dot.setAttribute('cx', x(i)); dot.setAttribute('cy', y(v)); dot.setAttribute('visibility', 'visible');
    }
    const rows = [{ key: 'cur', value: current[i] == null ? '—' : f(current[i]), label: name }];
    if (context.length) rows.push({ key: 'ctx', value: context[i] == null ? '—' : f(context[i]), label: `${contextName}${contextLabels?.[i] ? ` · ${contextLabels[i]}` : ''}` });
    showTip(labels.full?.[i] || labels[i], rows, cx, cy);
  }, () => {
    cross.setAttribute('visibility', 'hidden'); dotCur.setAttribute('visibility', 'hidden'); dotCtx.setAttribute('visibility', 'hidden');
    hideTip();
  });
  host.replaceChildren(root);
}

function METRIC_FMT(kind) {
  return kind === 'ratio' ? (v) => fmtPct(v) : kind === 'duration' ? fmtDur : fmtInt;
}

/** Columns for a single series; each column is its own hover target. */
function columnChart(host, { labels, full, values, name, height = 190, marker }) {
  const W = Math.max(240, host.clientWidth);
  const H = height;
  const { top: maxV, step } = niceScale(Math.max(0, ...values), 'count');
  const ticks = [];
  for (let v = 0; v <= maxV + step / 2; v += step) ticks.push(v);
  const tickW = Math.max(...ticks.map((t) => tickText(t, 'count').length)) * 6.6 + 10;
  const m = { l: tickW, r: 6, t: marker ? 22 : 10, b: 26 };
  const pw = W - m.l - m.r;
  const ph = H - m.t - m.b;
  const n = values.length;
  const slot = pw / n;
  const bw = Math.max(2, Math.min(24, slot - 2));
  const x = (i) => m.l + i * slot + (slot - bw) / 2;
  const cx = (i) => x(i) + bw / 2;
  const y = (v) => m.t + ph * (1 - v / maxV);
  const root = svg('svg', { viewBox: `0 0 ${W} ${H}`, width: W, height: H, tabindex: '0', role: 'img', 'aria-label': `${name}. Use the arrow keys to read values.` });
  for (const t of ticks) {
    root.append(svg('line', { class: t === 0 ? 'baseline' : 'gridline', x1: m.l, x2: W - m.r, y1: y(t), y2: y(t) }));
    root.append(svg('text', { class: 'tick', x: m.l - 8, y: y(t) + 4, 'text-anchor': 'end' }, tickText(t, 'count')));
  }
  const every = Math.max(1, Math.ceil(n / Math.max(2, Math.floor(pw / 46))));
  for (let i = 0; i < n; i += every) root.append(svg('text', { class: 'tick', x: cx(i), y: H - 8, 'text-anchor': 'middle' }, labels[i]));
  if (marker != null && marker < n) {
    root.append(svg('line', { class: 'edition-mark', x1: cx(marker), x2: cx(marker), y1: m.t - 6, y2: m.t + ph }));
    root.append(svg('text', { class: 'edition-label', x: cx(marker) + 5, y: m.t - 10 }, 'Edition 06:00'));
  }
  const bars = values.map((v, i) => {
    const bar = svg('path', { class: 'bar', d: roundedTop(x(i), y(v), bw, y(0) - y(v), 4) });
    root.append(bar);
    return bar;
  });
  root.append(svg('rect', { class: 'hit', x: m.l, y: m.t, width: pw, height: ph }));
  let hot = null;
  readable(root, n, cx, (i, px, py) => {
    hot?.classList.remove('is-hot');
    hot = bars[i];
    hot.classList.add('is-hot');
    showTip(full?.[i] || labels[i], [{ value: fmtInt(values[i]), label: name }], px, py);
  }, () => { hot?.classList.remove('is-hot'); hot = null; hideTip(); });
  host.replaceChildren(root);
}

function sparkline(values) {
  const W = 160, H = 30;
  const root = svg('svg', { class: 'spark', viewBox: `0 0 ${W} ${H}`, preserveAspectRatio: 'none', 'aria-hidden': 'true' });
  const present = values.filter((v) => v != null);
  if (present.length < 2) return root;
  const max = Math.max(...present);
  const min = Math.min(0, ...present);
  const n = values.length;
  const pts = values.map((v, i) => (v == null ? null : [(i / (n - 1)) * (W - 6) + 3, H - 4 - ((v - min) / (max - min || 1)) * (H - 8)]));
  // The period in the de-emphasis gray, the latest point in the accent.
  root.append(svg('path', { class: 'spark-line', d: linePath(pts), 'vector-effect': 'non-scaling-stroke' }));
  const last = pts.reduce((a, p) => p || a, null);
  if (last) root.append(svg('path', { class: 'spark-end', d: `M${last[0]},${last[1]}h0`, 'vector-effect': 'non-scaling-stroke' }));
  return root;
}

/** Horizontal bars for one series; the numbers stay visible, so the list is its own table. */
function barList(host, rows, { value = (r) => r.views, name, sub, code, total, limit = 8, noun = 'pageviews', empty = 'No figures for this period.' } = {}) {
  const shown = rows.filter((r) => value(r) > 0).slice(0, limit);
  if (!shown.length) { host.replaceChildren(el('p', { class: 'empty' }, empty)); return; }
  const max = Math.max(...shown.map(value));
  const sum = total ?? rows.reduce((a, r) => a + value(r), 0);
  const list = el('ul', { class: 'bars' });
  for (const r of shown) {
    const v = value(r);
    const fill = el('span', { class: 'fill' });
    fill.style.width = `${Math.max(0.6, (v / max) * 100)}%`;
    const label = name(r);
    const li = el('li', {},
      el('span', { class: 'name' }, code?.(r) ? el('span', { class: 'code' }, code(r)) : null, label, sub?.(r) ? el('span', { class: 'sub' }, sub(r)) : null),
      el('span', { class: 'val' }, fmtInt(v), el('span', { class: 'share' }, fmtPct(sum ? v / sum : 0, 0))),
      el('span', { class: 'track', 'aria-hidden': 'true' }, fill));
    // Every number is printed in the row; the tooltip only adds the exact share.
    li.addEventListener('pointermove', (e) => showTip(label, [{ value: fmtInt(v), label: noun }, { value: fmtPct(sum ? v / sum : 0, 1), label: 'of the total' }], e.clientX, e.clientY));
    li.addEventListener('pointerleave', hideTip);
    list.append(li);
  }
  host.replaceChildren(list);
}

function dataTable(head, rows) {
  return el('table', { class: 'data-table' },
    el('thead', {}, el('tr', {}, head.map((h, i) => el('th', { class: i ? 'num' : null, scope: 'col' }, h)))),
    el('tbody', {}, rows.map((r) => el('tr', {}, r.map((c, i) => el(i ? 'td' : 'th', { class: i ? 'num' : null, scope: i ? null : 'row' }, c))))));
}

function redrawOnResize(key, fn) {
  state.redraws.set(key, fn);
  fn();
}
let resizeFrame = 0;
let lastWidth = innerWidth;
addEventListener('resize', () => {
  if (innerWidth === lastWidth) return;
  lastWidth = innerWidth;
  cancelAnimationFrame(resizeFrame);
  resizeFrame = requestAnimationFrame(() => { for (const fn of state.redraws.values()) fn(); });
});

for (const fig of document.querySelectorAll('.fig')) {
  fig.addEventListener('click', (e) => {
    const b = e.target.closest('.view-toggle button');
    if (!b) return;
    const table = b.dataset.view === 'table';
    for (const x of fig.querySelectorAll('.view-toggle button')) x.setAttribute('aria-pressed', String(x === b));
    fig.querySelector('.chart').hidden = table;
    fig.querySelector('.table-view').hidden = !table;
    const legend = fig.querySelector('.legend');
    if (legend) legend.hidden = table;
  });
}

// ── The lead: a headline written from the figures ───────

function writeLead(d) {
  $('#lead-kicker').textContent = `Circulation report · ${spanLabel(d)}${d.range === 'today' ? ' · so far' : ''}`;
  const head = $('#lead-head');
  const dek = $('#lead-dek');
  const t = d.totals;
  const p = d.previous;
  if (!d.since) {
    head.textContent = 'No readers counted yet';
    dek.textContent = 'The tracker has not reported from caratcapital.org. Once the site carries it, the first visit shows up on the wire within a minute.';
    return;
  }
  if (!t.views) {
    head.textContent = d.range === 'today' ? 'No readers yet today' : 'No readers counted in this period';
    dek.textContent = `The desk has been counting since ${fmtDayLong(d.since)}.`;
    return;
  }
  const readers = change(t.readers, p.readers, 'count');
  let line;
  if (d.range === 'today') {
    line = `${say(t.readers, 'reader', true)} so far today`;
    if (readers && p.readers >= 25 && readers.dir !== 'flat') line += `, ${readers.dir} ${readers.text} on yesterday`;
  } else if (readers && p.readers >= 25 && readers.dir !== 'flat') {
    line = `Readers ${readers.dir} ${readers.text} to ${fmtInt(t.readers)}`;
  } else {
    line = `${say(t.readers, 'reader', true)} ${SPAN[d.range]}`;
  }
  if (d.desks.length > 1) line += `; ${deskName(d.desks[0].name)} leads the desks`;
  head.textContent = line;

  const parts = [];
  const views = change(t.views, p.views, 'count');
  parts.push(views && p.views >= 25 && views.dir !== 'flat'
    ? `Pageviews ${views.dir === 'up' ? 'rose' : 'fell'} ${views.text} to ${fmtInt(t.views)}.`
    : `${say(t.views, 'pageview', true)}.`);
  const nodes = [parts.join(' '), ' '];
  const top = d.stories[0];
  if (top) {
    nodes.push('The most-read story, ', el('q', {}, top.title || top.path), `, drew ${say(top.readers, 'reader')}. `);
  }
  const visits = d.channels.reduce((a, c) => a + c.visits, 0);
  const lead = d.channels[0];
  if (lead && visits >= 10) {
    const share = Math.round((lead.visits / visits) * 100);
    nodes.push(lead.name === 'Direct'
      ? `${share}% of visits were direct or from bookmarks.`
      : `${share}% of visits came from ${CHANNEL_PHRASE[lead.name] || lead.name}.`);
  }
  dek.replaceChildren(...nodes);
}

// ── Sections ─────────────────────────────────────────────

function writeMeta(d) {
  const clock = clockIn(d.tz, d.generated);
  $('#filters-meta').textContent = `${spanLabel(d)} · New York time · updated ${String(clock.h).padStart(2, '0')}:${String(clock.m).padStart(2, '0')}`;
  for (const b of document.querySelectorAll('#ranges button')) b.setAttribute('aria-checked', String(b.dataset.range === d.range));
}

function seriesFor(d) {
  const cur = bucket(d.series, d.range);
  const prev = bucket(d.previousSeries, d.range);
  if (d.range === 'today') {
    const now = clockIn(d.tz, d.generated).h;
    return { cur: cur.map((s, i) => (i <= now ? s : null)), prev };
  }
  return { cur, prev };
}

function renderKpis(d) {
  const host = $('#kpis');
  const { cur } = seriesFor(d);
  host.replaceChildren(...Object.entries(METRICS).map(([key, m]) => {
    const value = m.of(d.totals);
    const delta = change(value, m.of(d.previous), m.kind);
    const button = el('button', { type: 'button', class: 'kpi', 'aria-pressed': String(state.metric === key) },
      el('span', { class: 'kpi-label' }, m.label),
      el('span', { class: 'kpi-value' }, value == null ? '—' : m.fmt(value)),
      el('span', { class: 'kpi-foot' }, delta ? [deltaChip(delta), el('span', {}, VERSUS[d.range])] : el('span', {}, 'No earlier figures to compare')),
      sparkline(cur.map((s) => (s ? m.of(s) : null))));
    button.addEventListener('click', () => {
      state.metric = key;
      store.set('circulation-metric', key);
      for (const b of host.children) b.setAttribute('aria-pressed', String(b === button));
      renderTrend(d);
    });
    return button;
  }));
}

function renderTrend(d) {
  const m = METRICS[state.metric];
  const today = d.range === 'today';
  const { cur, prev } = seriesFor(d);
  const keys = today ? d.series : cur; // cur is null after the current hour today
  const labels = keys.map((s) => (today ? `${s.key}:00` : fmtDay(s.key)));
  labels.full = keys.map((s, i) => (today ? `${fmtDayShort(d.today)} · ${fmtHour(i)}` : s.week ? `Week of ${fmtDay(s.key, true)}` : fmtDayShort(s.key)));
  const current = cur.map((s) => (s ? m.of(s) : null));
  const context = prev.map((s) => m.of(s));
  const contextLabels = prev.map((s) => (today ? fmtDayShort(d.prevFrom) : s.week ? `week of ${fmtDay(s.key)}` : fmtDayShort(s.key)));
  const contextName = today ? 'Yesterday' : 'Previous period';
  $('#trend-title').textContent = `${m.label}, ${today ? 'by hour' : d.range === '12m' ? 'by week' : 'by day'}`;
  $('#trend-note').textContent = `${m.note ? `${m.label} ${m.note}. ` : ''}${today ? 'Today against yesterday, New York time.' : `This period against the ${d.range === '12m' ? '12 months' : `${d.series.length} days`} before it.`}`;
  $('#trend-legend').replaceChildren(
    el('span', {}, el('span', { class: 'key' }), today ? 'Today' : 'This period'),
    el('span', {}, el('span', { class: 'key ctx' }), contextName));
  redrawOnResize('trend', () => trendChart($('#trend-chart'), { labels, current, context, contextLabels, kind: m.kind, name: m.label, contextName }));
  const f = METRIC_FMT(m.kind);
  $('#trend-table').replaceChildren(dataTable(
    [today ? 'Hour' : d.range === '12m' ? 'Week of' : 'Day', today ? 'Today' : 'This period', contextName],
    labels.map((l, i) => [labels.full[i], current[i] == null ? '—' : f(current[i]), context[i] == null ? '—' : `${f(context[i])} (${contextLabels[i]})`])));
}

function openStoryUrl(path) {
  try {
    const url = new URL(path, 'https://caratcapital.org');
    return url.hostname === 'caratcapital.org' ? url.href : 'https://caratcapital.org/';
  } catch { return 'https://caratcapital.org/'; }
}

function renderStories(d) {
  const host = $('#stories');
  const rows = state.showAllStories ? d.stories : d.stories.slice(0, 10);
  const more = $('#stories-more');
  more.hidden = d.stories.length <= 10;
  more.textContent = state.showAllStories ? 'Show the top ten' : `Show all ${d.stories.length}`;
  if (!rows.length) { host.replaceChildren(el('p', { class: 'empty' }, 'No story was read in this period.')); return; }
  const body = el('tbody');
  rows.forEach((s, i) => {
    const read = s.articles ? s.reads / s.articles : null;
    const fill = el('span', { class: 'meter-fill' });
    fill.style.width = `${Math.round((read || 0) * 100)}%`;
    const title = el('button', { type: 'button', class: 'story-btn' }, s.title || s.path);
    const meta = el('span', { class: 'story-meta' },
      s.desk ? el('span', { class: 'desk-code' }, `${deskCode(s.desk)} `) : null,
      s.desk ? deskName(s.desk) : 'Story',
      s.published ? ` · Filed ${fmtDay(s.published)}` : '');
    const row = el('tr', {},
      el('td', { class: 'rank' }, String(i + 1).padStart(2, '0')),
      el('td', { class: 'title-cell' }, title, meta),
      el('td', { class: 'num', 'data-label': plural(s.readers, 'reader') }, fmtInt(s.readers)),
      el('td', { class: 'num', 'data-label': plural(s.views, 'view') }, fmtInt(s.views)),
      el('td', { class: 'num', 'data-label': 'read' }, fmtDur(s.engaged_n ? s.engaged / s.engaged_n : null)),
      el('td', { class: 'num', 'data-label': 'finish' },
        el('span', { class: 'meter' }, el('span', { class: 'meter-track', 'aria-hidden': 'true' }, fill), fmtPct(read))));
    row.addEventListener('click', () => openStory(s.path, title));
    body.append(row);
  });
  host.replaceChildren(el('table', { class: 'stories' },
    el('thead', {}, el('tr', {},
      el('th', { scope: 'col' }, el('span', { class: 'sr' }, 'Rank')),
      el('th', { scope: 'col', class: 'story-h' }, 'Story'),
      el('th', { scope: 'col' }, 'Readers'),
      el('th', { scope: 'col' }, 'Views'),
      el('th', { scope: 'col' }, 'Reading time'),
      el('th', { scope: 'col' }, 'Read-through'))),
    body));
}

$('#stories-more').addEventListener('click', () => {
  state.showAllStories = !state.showAllStories;
  renderStories(state.data);
});

function csvCell(v) {
  let s = String(v ?? '');
  if (/^[=+\-@\t\r]/.test(s)) s = `'${s}`; // never hand a spreadsheet a formula
  return /[",\n\r]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}

$('#stories-csv').addEventListener('click', () => {
  const d = state.data;
  if (!d) return;
  const head = ['rank', 'title', 'url', 'desk', 'filed', 'readers', 'pageviews', 'visits', 'avg_reading_seconds', 'read_through_pct'];
  const lines = [head.join(',')];
  d.stories.forEach((s, i) => lines.push([
    i + 1, s.title || '', openStoryUrl(s.path), deskName(s.desk), s.published || '', s.readers, s.views, s.visits,
    s.engaged_n ? Math.round(s.engaged / s.engaged_n) : '', s.articles ? ((s.reads / s.articles) * 100).toFixed(1) : '',
  ].map(csvCell).join(',')));
  const blob = new Blob([`${lines.join('\r\n')}\r\n`], { type: 'text/csv;charset=utf-8' });
  const a = el('a', { href: URL.createObjectURL(blob), download: `carat-capital-stories-${d.from}-to-${d.to}.csv` });
  document.body.append(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
});

function renderDesks(d) {
  barList($('#desks'), d.desks, {
    name: (r) => deskName(r.name),
    code: (r) => deskCode(r.name),
    sub: (r) => `${fmtDur(r.engaged_n ? r.engaged / r.engaged_n : null)} · ${fmtPct(r.articles ? r.reads / r.articles : null)} read`,
    noun: 'story pageviews',
    limit: 6,
    empty: 'No story pageviews in this period.',
  });
}

function renderSources(d) {
  const visits = (r) => r.visits;
  barList($('#channels'), d.channels, { value: visits, name: (r) => CHANNELS[r.name] || r.name, noun: 'visits', empty: 'No visits in this period.' });
  barList($('#refs'), d.refs, { value: visits, name: (r) => sourceName(r.name), sub: (r) => CHANNELS[r.channel] || '', noun: 'visits', empty: 'No referring sites in this period.' });
  barList($('#campaigns'), d.campaigns, { value: visits, name: (r) => r.name, noun: 'visits', empty: 'No tagged links were used. Add ?utm_campaign=… to links you share.' });
}

function renderPlaces(d) {
  barList($('#countries'), d.countries, { name: (r) => countryName(r.name) });
  barList($('#cities'), d.cities, { name: (r) => r.name, sub: (r) => countryName(r.country), total: d.totals.views });
}

function renderHours(d) {
  const values = d.hours.map((h) => h.views);
  const labels = d.hours.map((h) => h.key);
  const full = d.hours.map((h) => `${fmtHour(Number(h.key))}–${fmtHour((Number(h.key) + 1) % 24)} New York`);
  $('#hours-note').textContent = d.range === 'today' ? 'Pageviews by hour today, New York time.' : 'Pageviews by hour of day across the period, New York time.';
  redrawOnResize('hours', () => columnChart($('#hours-chart'), { labels, full, values, name: 'Pageviews by hour', marker: 6 }));
  const total = values.reduce((a, v) => a + v, 0);
  $('#hours-table').replaceChildren(dataTable(['Hour', 'Pageviews', 'Share'], d.hours.map((h, i) => [full[i], fmtInt(values[i]), fmtPct(total ? values[i] / total : 0, 1)])));
}

function renderKit(d) {
  barList($('#devices'), d.devices, { name: (r) => r.name });
  barList($('#browsers'), d.browsers, { name: (r) => r.name });
  barList($('#systems'), d.os, { name: (r) => r.name });
}

function renderPages(d) {
  barList($('#pages'), d.pages, { name: (r) => PAGES[r.path] || r.title || r.path, sub: (r) => r.path, limit: 12, total: d.totals.views, empty: 'No other pages were read in this period.' });
}

function render(d) {
  state.data = d;
  $('#demo-banner').hidden = !d.demo;
  writeMeta(d);
  writeLead(d);
  renderKpis(d);
  renderTrend(d);
  renderStories(d);
  renderDesks(d);
  renderSources(d);
  renderPlaces(d);
  renderHours(d);
  renderKit(d);
  renderPages(d);
}

// ── The wire (live) ──────────────────────────────────────

function renderLive(live) {
  const host = $('#live');
  const pill = $('#live-pill-text');
  pill.textContent = live.readers ? `${fmtInt(live.readers)} live` : 'Live';
  const bars = svg('svg', { class: 'live-spark', viewBox: '0 0 300 44', preserveAspectRatio: 'none', 'aria-hidden': 'true' });
  const max = Math.max(1, ...live.perMinute);
  live.perMinute.forEach((v, i) => {
    const h = v ? Math.max(2, (v / max) * 42) : 0;
    if (h) bars.append(svg('rect', { x: i * 10 + 1, y: 44 - h, width: 8, height: h, rx: 1.5 }));
  });
  const list = el('ul', { class: 'live-list' }, live.pages.map((p) => el('li', {},
    el('span', {}, PAGES[p.path] || p.title || p.path),
    el('span', {}, `${fmtInt(p.readers)} ${plural(p.readers, 'reader')}`))));
  host.replaceChildren(
    el('p', { class: 'live-figure' }, el('strong', {}, fmtInt(live.readers)), el('span', {}, `${plural(live.readers, 'reader')} · ${fmtInt(live.views)} ${plural(live.views, 'pageview')}`)),
    bars,
    el('div', { class: 'live-axis', 'aria-hidden': 'true' }, el('span', {}, '30 min ago'), el('span', {}, 'now')),
    live.pages.length ? list : el('p', { class: 'empty' }, 'Quiet on the wire. Nobody has opened a page in the last half hour.'));
}

async function refreshLive() {
  if (document.hidden) return;
  try {
    renderLive(await api('/api/live'));
  } catch (e) {
    if (e.status === 401) showGate(e.code);
  }
}

$('#live-pill').addEventListener('click', () => $('#live-panel').scrollIntoView({ behavior: 'smooth', block: 'center' }));

// ── Story drawer ─────────────────────────────────────────

let drawerOpener = null;

function closeStory() {
  $('#drawer').hidden = true;
  $('#scrim').hidden = true;
  document.body.style.overflow = '';
  state.redraws.delete('story');
  hideTip();
  drawerOpener?.focus();
}

$('#scrim').addEventListener('click', closeStory);
document.addEventListener('keydown', (e) => {
  if ($('#drawer').hidden) return;
  if (e.key === 'Escape') { closeStory(); return; }
  if (e.key !== 'Tab') return;
  const focusable = [...$('#drawer').querySelectorAll('button, a[href], [tabindex="0"]')].filter((n) => !n.closest('[hidden]'));
  if (!focusable.length) return;
  const first = focusable[0];
  const last = focusable[focusable.length - 1];
  if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
  else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
});

async function openStory(path, opener) {
  drawerOpener = opener;
  const body = $('#drawer-body');
  const close = el('button', { type: 'button', class: 'tool', 'aria-label': 'Close story' }, 'Close ✕');
  close.addEventListener('click', closeStory);
  body.replaceChildren(el('div', { class: 'drawer-top' }, el('p', { class: 'fig-no' }, 'Story file'), close), el('h2', { id: 'drawer-title', class: 'story-title' }, 'Pulling the file…'));
  $('#scrim').hidden = false;
  $('#drawer').hidden = false;
  document.body.style.overflow = 'hidden';
  close.focus();
  let s;
  try {
    s = await api(`/api/story?path=${encodeURIComponent(path)}&range=${state.range}`);
  } catch (e) {
    if (e.status === 401) { closeStory(); showGate(e.code); return; }
    body.append(el('p', { class: 'empty' }, explain(e)));
    return;
  }
  const t = s.totals;
  const read = t.articles ? t.reads / t.articles : null;
  const kicker = el('p', { class: 'fig-no' },
    s.desk ? `${deskCode(s.desk)} · ${deskName(s.desk)}` : 'Page',
    s.published ? ` · Filed ${fmtDay(s.published, true)}` : '');
  const link = el('a', { class: 'open-link', href: openStoryUrl(path), target: '_blank', rel: 'noopener' }, 'Read it on caratcapital.org ↗');
  const days = el('section', { class: 'panel fig' },
    el('header', { class: 'panel-head' }, el('div', {}, el('p', { class: 'fig-no' }, 'Readers'), el('h2', {}, state.range === 'today' ? 'By hour today' : 'By day'))),
    el('div', { class: 'chart chart-short', id: 'story-chart' }));
  const depthHost = el('div');
  const sourcesHost = el('div');
  const refsHost = el('div');
  const placesHost = el('div');
  const devicesHost = el('div');
  body.replaceChildren(
    el('div', { class: 'drawer-top' }, kicker, close),
    el('h2', { id: 'drawer-title', class: 'story-title' }, s.title || path),
    link,
    el('div', { class: 'mini-kpis' },
      el('div', {}, el('span', { class: 'kpi-label' }, 'Readers'), el('b', {}, fmtInt(t.readers))),
      el('div', {}, el('span', { class: 'kpi-label' }, 'Pageviews'), el('b', {}, fmtInt(t.views))),
      el('div', {}, el('span', { class: 'kpi-label' }, 'Reading time'), el('b', {}, fmtDur(t.engaged_n ? t.engaged / t.engaged_n : null))),
      el('div', {}, el('span', { class: 'kpi-label' }, 'Read-through'), el('b', {}, fmtPct(read)))),
    days,
    el('section', { class: 'panel' }, el('header', { class: 'panel-head' }, el('div', {}, el('p', { class: 'fig-no' }, 'Depth'), el('h2', {}, 'How far readers got'),
      el('p', { class: 'panel-note' }, `Share of the ${fmtInt(s.depth.reported)} ${plural(s.depth.reported, 'view')} that reported how far they read.`))), depthHost),
    el('section', { class: 'panel' }, el('header', { class: 'panel-head' }, el('div', {}, el('p', { class: 'fig-no' }, 'Sources'), el('h2', {}, 'Where they came from'),
      el('p', { class: 'panel-note' }, s.fromOtherPages ? `Plus ${fmtInt(s.fromOtherPages)} ${plural(s.fromOtherPages, 'view')} from other Carat Capital pages.` : 'Visits from outside the paper.'))), sourcesHost, refsHost),
    el('div', { class: 'grid grid-2-drawer' },
      el('section', { class: 'panel' }, el('header', { class: 'panel-head' }, el('div', {}, el('p', { class: 'fig-no' }, 'Places'), el('h2', {}, 'Countries'))), placesHost),
      el('section', { class: 'panel' }, el('header', { class: 'panel-head' }, el('div', {}, el('p', { class: 'fig-no' }, 'Devices'), el('h2', {}, 'Held on'))), devicesHost)));

  // Start the chart on the day the story was filed, not weeks of empty days before it.
  const filed = state.range !== 'today' && s.published ? s.series.findIndex((r) => r.key >= s.published) : 0;
  const life = filed > 0 ? s.series.slice(filed) : s.series;
  const byWeek = life.length > 45;
  const series = byWeek ? weekly(life) : life;
  days.querySelector('h2').textContent = state.range === 'today' ? 'By hour today' : byWeek ? 'By week' : 'By day';
  const labels = series.map((r) => (state.range === 'today' ? r.key : fmtDay(r.key)));
  const full = series.map((r) => (state.range === 'today' ? `${fmtHour(Number(r.key))} New York` : byWeek ? `Week of ${fmtDay(r.key, true)}` : fmtDayShort(r.key)));
  redrawOnResize('story', () => columnChart($('#story-chart'), { labels, full, values: series.map((r) => r.readers), name: 'Readers' }));
  const steps = { 25: 'A quarter of the way', 50: 'Halfway', 75: 'Three quarters', 90: 'The end' };
  barList(depthHost, s.depth.steps.map((st) => ({ ...st, name: steps[st.at] })), {
    value: (r) => r.views, name: (r) => r.name, total: s.depth.reported, noun: 'views', limit: 4, empty: 'No reading reports yet.',
  });
  barList(sourcesHost, s.channels, { value: (r) => r.visits, name: (r) => CHANNELS[r.name] || r.name, noun: 'visits', empty: 'No outside visits in this period.' });
  if (s.refs.length) barList(refsHost, s.refs, { value: (r) => r.visits, name: (r) => sourceName(r.name), sub: (r) => CHANNELS[r.channel] || '', noun: 'visits', limit: 6 });
  barList(placesHost, s.countries, { name: (r) => countryName(r.name), limit: 6 });
  barList(devicesHost, s.devices, { name: (r) => r.name, limit: 3 });
}

// ── Loading ──────────────────────────────────────────────

function stopTimers() {
  for (const t of state.timers) clearInterval(t);
  state.timers = [];
}

async function load({ quiet = false } = {}) {
  const page = $('#page');
  if (!quiet) page.classList.add('is-loading');
  try {
    let d = await api(`/api/overview?range=${state.range}`);
    // On the first day of counting there are no whole days yet: open on today.
    if (state.firstLoad && d.range !== 'today' && d.since && d.since > d.to) {
      state.range = 'today';
      d = await api('/api/overview?range=today');
    }
    state.firstLoad = false;
    notice('');
    render(d);
  } catch (e) {
    if (e.status === 401) { showGate(e.code); return; }
    notice(explain(e));
  } finally {
    page.classList.remove('is-loading');
  }
}

$('#ranges').addEventListener('click', (e) => {
  const b = e.target.closest('button[data-range]');
  if (!b || b.dataset.range === state.range) return;
  state.range = b.dataset.range;
  state.showAllStories = false;
  store.set('circulation-range', state.range);
  for (const x of document.querySelectorAll('#ranges button')) x.setAttribute('aria-checked', String(x === b));
  load();
});
$('#ranges').addEventListener('keydown', (e) => {
  if (!['ArrowLeft', 'ArrowRight'].includes(e.key)) return;
  const buttons = [...document.querySelectorAll('#ranges button')];
  const i = buttons.indexOf(document.activeElement);
  const next = buttons[(i + (e.key === 'ArrowRight' ? 1 : -1) + buttons.length) % buttons.length];
  next.focus();
  next.click();
});

async function boot() {
  labelEdition();
  let session;
  try {
    session = await api('/api/session');
  } catch (e) {
    $('#desk').hidden = false;
    notice(explain(e));
    return;
  }
  if (!session.signedIn) { showGate(session.configured ? 'signed-out' : 'not-configured'); return; }
  state.tz = session.tz || state.tz;
  $('#gate').hidden = true;
  $('#desk').hidden = false;
  for (const b of document.querySelectorAll('#ranges button')) b.setAttribute('aria-checked', String(b.dataset.range === state.range));
  stopTimers();
  await Promise.all([load(), refreshLive()]);
  state.timers.push(setInterval(refreshLive, 30000));
  state.timers.push(setInterval(() => { if (!document.hidden) load({ quiet: true }); }, 5 * 60000));
}

document.addEventListener('visibilitychange', () => { if (!document.hidden && !$('#desk').hidden) refreshLive(); });

boot();
