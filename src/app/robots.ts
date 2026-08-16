import type { MetadataRoute } from 'next';

import { publicEnv } from '@/lib/env';

export default function robots(): MetadataRoute.Robots {
  const base = publicEnv.appUrl.replace(/\/+$/, '');

  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        // The operator console, the login form, the JSON API, and the post-submit
        // confirmation. None of these can rank, and a crawled login page in search
        // results is a liability rather than a miss.
        disallow: ['/admin', '/admin/', '/login', '/api/', '/start/thanks'],
      },
    ],
    sitemap: `${base}/sitemap.xml`,
    host: base,
  };
}
