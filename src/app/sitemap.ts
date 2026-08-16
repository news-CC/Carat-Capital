import type { MetadataRoute } from 'next';

import { publicEnv } from '@/lib/env';

/**
 * Only the pages a stranger should land on. /admin and /login are operator surface, /start/thanks is
 * a post-submit confirmation that means nothing cold, and /api returns JSON — indexing any of them
 * spends crawl budget on pages that can never rank and puts a login form in search results.
 */
const PUBLIC_ROUTES: { path: string; priority: number; changeFrequency: MetadataRoute.Sitemap[number]['changeFrequency'] }[] = [
  { path: '/', priority: 1, changeFrequency: 'weekly' },
  { path: '/start', priority: 0.9, changeFrequency: 'monthly' },
  { path: '/terms', priority: 0.3, changeFrequency: 'yearly' },
  { path: '/privacy', priority: 0.3, changeFrequency: 'yearly' },
];

export default function sitemap(): MetadataRoute.Sitemap {
  const base = publicEnv.appUrl.replace(/\/+$/, '');
  const lastModified = new Date();

  return PUBLIC_ROUTES.map((route) => ({
    url: `${base}${route.path}`,
    lastModified,
    changeFrequency: route.changeFrequency,
    priority: route.priority,
  }));
}
