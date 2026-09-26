// Where a reader came from: the referring site, folded to one name per
// network, and the channel it belongs to.

export const CHANNELS = ['Search', 'Social', 'AI', 'Email', 'Paid', 'Referral', 'Direct', 'Internal'];

const SEARCH = new Set([
  'google.com', 'news.google.com', 'discover.google.com', 'bing.com', 'duckduckgo.com',
  'yahoo.com', 'yandex.com', 'baidu.com', 'ecosia.org', 'search.brave.com', 'startpage.com',
  'qwant.com', 'naver.com', 'seznam.cz', 'kagi.com', 'sogou.com', 'so.com',
]);
const AI = new Set([
  'chatgpt.com', 'perplexity.ai', 'claude.ai', 'gemini.google.com', 'copilot.microsoft.com',
  'you.com', 'phind.com', 'chat.deepseek.com', 'meta.ai', 'grok.com', 'chat.mistral.ai',
  'poe.com', 'kimi.com',
]);
const SOCIAL = new Set([
  'instagram.com', 'facebook.com', 'x.com', 'linkedin.com', 'tiktok.com', 'pinterest.com',
  'reddit.com', 'youtube.com', 'threads.net', 'bsky.app', 'whatsapp.com', 'telegram.org',
  'snapchat.com', 'weibo.com', 'xiaohongshu.com', 'douyin.com', 'vk.com',
  'news.ycombinator.com', 'quora.com', 'mastodon.social', 'discord.com', 'line.me', 'tumblr.com',
]);
const EMAIL = new Set([
  'mail.google.com', 'outlook.live.com', 'outlook.office.com', 'outlook.office365.com',
  'mail.yahoo.com', 'mail.proton.me', 'mail.aol.com', 'mail.zoho.com', 'gmail.com',
]);

// Android apps that open links report themselves as android-app://<package>.
const APPS = {
  'com.google.android.googlequicksearchbox': 'discover.google.com',
  'com.google.android.gm': 'mail.google.com',
  'com.linkedin.android': 'linkedin.com',
  'com.instagram.android': 'instagram.com',
  'com.facebook.katana': 'facebook.com',
  'com.twitter.android': 'x.com',
  'com.reddit.frontpage': 'reddit.com',
  'com.zhiliaoapp.musically': 'tiktok.com',
  'com.whatsapp': 'whatsapp.com',
  'org.telegram.messenger': 'telegram.org',
  'com.openai.chatgpt': 'chatgpt.com',
};

/** One canonical host per network: l.instagram.com → instagram.com, t.co → x.com. */
export function normalizeHost(host) {
  let h = String(host || '').toLowerCase().replace(/\.$/, '');
  if (!h) return '';
  if (h === 'news.google.com' || h === 'gemini.google.com') return h;
  if (h === 'bard.google.com') return 'gemini.google.com';
  if (h === 'chat.openai.com') return 'chatgpt.com';
  h = h.replace(/^(www\d?|m|l|lm|mobile|amp|out|touch)\./, '');
  if (/(^|\.)google\.[a-z.]{2,7}$/.test(h)) return 'google.com';
  if (/(^|\.)bing\.com$/.test(h)) return 'bing.com';
  if (/(^|\.)yahoo\.[a-z.]{2,7}$/.test(h)) return 'yahoo.com';
  if (/(^|\.)yandex\.[a-z.]{2,7}$/.test(h)) return 'yandex.com';
  if (h === 't.co' || h === 'twitter.com' || h === 'x.com') return 'x.com';
  if (h === 'lnkd.in' || /(^|\.)linkedin\.com$/.test(h)) return 'linkedin.com';
  if (h === 'fb.me' || h === 'fb.com' || /(^|\.)facebook\.com$/.test(h)) return 'facebook.com';
  if (/(^|\.)instagram\.com$/.test(h)) return 'instagram.com';
  if (h === 'youtu.be' || /(^|\.)youtube\.com$/.test(h)) return 'youtube.com';
  if (h === 'pin.it' || /(^|\.)pinterest\.[a-z.]{2,7}$/.test(h)) return 'pinterest.com';
  if (/(^|\.)reddit\.com$/.test(h)) return 'reddit.com';
  if (/(^|\.)tiktok\.com$/.test(h)) return 'tiktok.com';
  if (/^threads\.(net|com)$/.test(h)) return 'threads.net';
  if (h === 'wa.me' || /(^|\.)whatsapp\.com$/.test(h)) return 'whatsapp.com';
  if (h === 't.me' || /(^|\.)telegram\.org$/.test(h)) return 'telegram.org';
  return h;
}

// utm_source values people actually type, mapped to the same canonical hosts.
const SOURCE_ALIASES = {
  ig: 'instagram.com', instagram: 'instagram.com', fb: 'facebook.com', facebook: 'facebook.com',
  tiktok: 'tiktok.com', tt: 'tiktok.com', linkedin: 'linkedin.com', li: 'linkedin.com',
  x: 'x.com', twitter: 'x.com', threads: 'threads.net', pinterest: 'pinterest.com',
  youtube: 'youtube.com', yt: 'youtube.com', reddit: 'reddit.com', whatsapp: 'whatsapp.com',
  wa: 'whatsapp.com', telegram: 'telegram.org', chatgpt: 'chatgpt.com', openai: 'chatgpt.com',
  perplexity: 'perplexity.ai', google: 'google.com', bing: 'bing.com', gemini: 'gemini.google.com',
};

export function normalizeSource(source) {
  const s = String(source || '').trim().toLowerCase().slice(0, 80);
  if (!s) return '';
  if (SOURCE_ALIASES[s]) return SOURCE_ALIASES[s];
  return /\./.test(s) ? normalizeHost(s) : s;
}

/** The referring host from document.referrer, including Android app referrers. */
export function referrerHost(referrer) {
  const r = String(referrer || '');
  if (!r) return '';
  const app = /^android-app:\/\/([\w.]+)/.exec(r);
  if (app) return APPS[app[1]] || app[1];
  try {
    const u = new URL(r);
    return /^https?:$/.test(u.protocol) ? u.hostname : '';
  } catch {
    return '';
  }
}

/**
 * @param {{host: string, internal: boolean, medium?: string, source?: string}} s
 * @returns {string} one of CHANNELS
 */
export function channelOf({ host, internal, medium = '', source = '' }) {
  const m = medium.toLowerCase();
  if (/^(cpc|ppc|paid|paid[_-]?social|display|banner|cpm|ads?)$/.test(m)) return 'Paid';
  if (/e-?mail|newsletter/.test(m) || /newsletter|brief|mailchimp|substack|beehiiv|convertkit|klaviyo|buttondown/.test(source)) return 'Email';
  if (/social/.test(m)) return 'Social';
  if (source) {
    if (AI.has(source)) return 'AI';
    if (SOCIAL.has(source)) return 'Social';
    if (SEARCH.has(source)) return 'Search';
  }
  if (internal) return 'Internal';
  if (!host) return source ? 'Referral' : 'Direct';
  if (AI.has(host)) return 'AI';
  if (SEARCH.has(host)) return 'Search';
  if (SOCIAL.has(host)) return 'Social';
  if (EMAIL.has(host)) return 'Email';
  return 'Referral';
}
