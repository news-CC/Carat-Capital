// Just enough user-agent reading to say what readers hold: device, browser, OS.
// The tracker only runs where JavaScript runs, so most crawlers never report;
// this list catches the ones that render pages (search renderers, audit tools,
// headless browsers, previewers) and the scripted clients that post directly.

const BOT = new RegExp([
  'bot\\b', 'bot/', 'crawler', 'spider', 'slurp', 'headless', 'lighthouse', 'pagespeed',
  'gtmetrix', 'pingdom', 'uptime', 'phantomjs', 'selenium', 'puppeteer', 'playwright',
  'cypress', 'webdriver', 'python', 'curl/', 'wget', 'java/', 'go-http', 'okhttp', 'axios',
  'node-fetch', 'undici', 'httpclient', 'libwww', 'scrapy', 'facebookexternalhit',
  'whatsapp/', 'preview', 'google-inspectiontool', 'google-read-aloud', 'mediapartners',
  'adsbot', 'feedfetcher', 'bytespider', 'ccbot', 'chatgpt-user', 'oai-searchbot', 'gptbot',
  'claude-user', 'claude-web', 'perplexity', 'amazonbot', 'applebot', 'baiduspider',
  'semrush', 'ahrefs', 'archive\\.org', 'ia_archiver',
].join('|'), 'i');

export function isBot(ua) {
  return !ua || (BOT.test(ua) && !/cubot/i.test(ua)); // Cubot is a phone maker, not a crawler
}

/**
 * @param {string} ua
 * @param {number} touch navigator.maxTouchPoints, which unmasks iPads posing as Macs
 */
export function parseUA(ua, touch = 0) {
  let os = 'Other', device = 'Desktop';
  if (/iPhone|iPod/.test(ua)) { os = 'iOS'; device = 'Mobile'; }
  else if (/iPad/.test(ua)) { os = 'iPadOS'; device = 'Tablet'; }
  else if (/Android/.test(ua)) { os = 'Android'; device = /Mobile/.test(ua) ? 'Mobile' : 'Tablet'; }
  else if (/Windows Phone/.test(ua)) { os = 'Windows Phone'; device = 'Mobile'; }
  else if (/Windows NT/.test(ua)) os = 'Windows';
  else if (/CrOS/.test(ua)) os = 'ChromeOS';
  else if (/Macintosh|Mac OS X/.test(ua)) {
    if (touch > 1) { os = 'iPadOS'; device = 'Tablet'; } else os = 'macOS';
  }
  else if (/Linux/.test(ua)) os = 'Linux';

  // In-app browsers first: they are how social readers arrive.
  let browser = 'Other';
  if (/Instagram/.test(ua)) browser = 'Instagram app';
  else if (/FBAN|FBAV|FB_IAB|FBIOS/.test(ua)) browser = 'Facebook app';
  else if (/LinkedInApp/.test(ua)) browser = 'LinkedIn app';
  else if (/musical_ly|BytedanceWebview|TikTok|trill_/.test(ua)) browser = 'TikTok app';
  else if (/Twitter|TwitterAndroid/.test(ua)) browser = 'X app';
  else if (/Snapchat/.test(ua)) browser = 'Snapchat app';
  else if (/Pinterest/.test(ua)) browser = 'Pinterest app';
  else if (/MicroMessenger/.test(ua)) browser = 'WeChat';
  else if (/\bLine\//.test(ua)) browser = 'LINE app';
  else if (/\bGSA\//.test(ua)) browser = 'Google app';
  else if (/Edg(e|A|iOS)?\//.test(ua)) browser = 'Edge';
  else if (/OPR\/|Opera/.test(ua)) browser = 'Opera';
  else if (/SamsungBrowser/.test(ua)) browser = 'Samsung Internet';
  else if (/YaBrowser/.test(ua)) browser = 'Yandex Browser';
  else if (/DuckDuckGo\//.test(ua)) browser = 'DuckDuckGo';
  else if (/Firefox\/|FxiOS/.test(ua)) browser = 'Firefox';
  else if (/Chrome\/|CriOS/.test(ua)) browser = 'Chrome';
  else if (/Version\/[\d.]+.*Safari\//.test(ua)) browser = 'Safari';
  else if (/AppleWebKit/.test(ua) && (os === 'iOS' || os === 'iPadOS')) browser = 'In-app browser';
  return { device, os, browser };
}
