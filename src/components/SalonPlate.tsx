/**
 * The hero plate: an empty styling chair at a lit salon mirror.
 *
 * Inline SVG rather than a photograph, on purpose. It is the argument the headline makes — the
 * empty chair IS the buried money — and it costs no network request, stays sharp at any size, and
 * draws from the same palette tokens as everything else, so it cannot drift out of key.
 *
 * Two things carry the whole drawing, and both were wrong in the first pass:
 *  - The arch must be WIDE and shallow. A tall narrow arch with anything hanging inside it reads
 *    as a bell jar, not a mirror.
 *  - The chair must be filled opaque and overlap the counter, so it sits in FRONT. Outlined and
 *    non-overlapping, it floats somewhere behind the glass and the image stops being a room.
 *
 * To swap in a real photograph later, replace the <svg> with next/image and keep the frame div —
 * the aspect ratio, hairline border and card shadow are what make it read as an editorial plate.
 */
export default function SalonPlate({ className = '' }: { className?: string }) {
  return (
    <div
      className={`relative overflow-hidden rounded-[14px] border border-line bg-paper ${className}`}
      style={{ boxShadow: 'var(--shadow-card)' }}
    >
      <svg
        viewBox="0 0 480 600"
        className="block h-auto w-full"
        role="img"
        aria-labelledby="salon-plate-title salon-plate-desc"
      >
        <title id="salon-plate-title">An empty styling chair at a salon mirror</title>
        <desc id="salon-plate-desc">
          Line drawing of a vacant styling chair in front of a wide arched salon mirror flanked by
          two sconces — the empty chair a lapsed client used to fill.
        </desc>

        <defs>
          <linearGradient id="sp-wash" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="var(--color-cream)" />
            <stop offset="100%" stopColor="var(--color-shell)" />
          </linearGradient>
          <linearGradient id="sp-glass" x1="0.2" y1="0" x2="0.8" y2="1">
            <stop offset="0%" stopColor="var(--color-paper)" />
            <stop offset="55%" stopColor="var(--color-cream)" />
            <stop offset="100%" stopColor="var(--color-shell)" />
          </linearGradient>
          <radialGradient id="sp-glow" cx="0.5" cy="0.42" r="0.55">
            <stop offset="0%" stopColor="var(--color-paper)" stopOpacity="0.9" />
            <stop offset="100%" stopColor="var(--color-paper)" stopOpacity="0" />
          </radialGradient>
        </defs>

        <rect width="480" height="600" fill="url(#sp-wash)" />
        <rect width="480" height="600" fill="url(#sp-glow)" />

        {/* ---- the room, behind everything: wide shallow arch = mirror, not a jar ---- */}
        <g stroke="var(--color-ink)" fill="none" strokeLinecap="round" strokeLinejoin="round">
          <path
            d="M100 336 L100 214 A140 108 0 0 1 380 214 L380 336 Z"
            fill="url(#sp-glass)"
            strokeWidth="1.5"
            opacity="0.9"
          />
          <path
            d="M114 336 L114 216 A126 96 0 0 1 366 216 L366 336"
            strokeWidth="0.75"
            opacity="0.35"
          />
          {/* a single raking highlight across the glass */}
          <path d="M150 320 L250 176" strokeWidth="0.75" opacity="0.18" />
          <path d="M176 328 L286 170" strokeWidth="0.75" opacity="0.12" />

          {/* sconces, outside the arch — this is what the pendant should have been */}
          <g strokeWidth="1.25" opacity="0.6">
            <circle cx="66" cy="228" r="13" fill="var(--color-paper)" />
            <path d="M66 241 L66 258" />
            <circle cx="414" cy="228" r="13" fill="var(--color-paper)" />
            <path d="M414 241 L414 258" />
          </g>

          {/* vanity counter, with a front face so it has thickness */}
          <path d="M64 336 L416 336" strokeWidth="1.5" />
          <path d="M64 336 L64 350 L416 350 L416 336" strokeWidth="1.25" fill="var(--color-cream)" />
          <path d="M64 350 L416 350" strokeWidth="0.75" opacity="0.4" />
        </g>

        {/* ---- the chair: filled, and overlapping the counter, so it reads as foreground ---- */}
        <g
          stroke="var(--color-ink)"
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth="1.75"
          fill="var(--color-paper)"
        >
          {/* high back with a shoulder taper */}
          <path d="M178 300 L178 262 A30 30 0 0 1 208 232 L272 232 A30 30 0 0 1 302 262 L302 300 L292 436 L188 436 Z" />
          {/* inner seam */}
          <path
            d="M192 300 L192 268 A20 20 0 0 1 212 248 L268 248 A20 20 0 0 1 288 268 L288 300"
            fill="none"
            strokeWidth="0.75"
            opacity="0.4"
          />
          {/* seat cushion */}
          <path d="M158 436 L322 436 A14 14 0 0 1 322 470 L158 470 A14 14 0 0 1 158 436 Z" />
          <path d="M158 452 L322 452" fill="none" strokeWidth="0.75" opacity="0.3" />
          {/* armrest, near side only — keeps the silhouette readable */}
          <path
            d="M154 404 L154 428 A10 10 0 0 0 164 438"
            fill="none"
            strokeWidth="1.5"
            opacity="0.8"
          />
          {/* hydraulic column */}
          <path d="M226 470 L254 470 L252 528 L228 528 Z" />
          <path d="M231 492 L249 492" fill="none" strokeWidth="0.75" opacity="0.35" />
          {/* footrest ring in front of the column */}
          <path
            d="M204 508 A36 12 0 0 0 276 508"
            fill="none"
            strokeWidth="1.5"
            opacity="0.85"
          />
          {/* five-star base with castors */}
          <ellipse cx="240" cy="530" rx="18" ry="6" />
          <g fill="none" strokeWidth="1.5">
            <path d="M240 534 L170 556" />
            <path d="M240 534 L310 556" />
            <path d="M240 536 L206 562" />
            <path d="M240 536 L274 562" />
          </g>
          <g strokeWidth="1.25">
            <circle cx="167" cy="559" r="5" />
            <circle cx="313" cy="559" r="5" />
            <circle cx="203" cy="565" r="5" />
            <circle cx="277" cy="565" r="5" />
          </g>
        </g>

        {/* floor, then one brass hairline — the only warm mark in the drawing */}
        <path d="M36 578 L444 578" stroke="var(--color-ink)" strokeWidth="1" opacity="0.28" />
        <path d="M36 582 L444 582" stroke="var(--color-brass)" strokeWidth="1.5" opacity="0.8" />
      </svg>
    </div>
  );
}
