-- The Circulation Desk: Carat Capital's readership ledger.
--
-- Nothing here identifies a reader. There are no cookies and no IP addresses.
-- `visitor` is a hash of (the day's random salt, IP address, browser) and the
-- salt is deleted after two days, so a reader counts once per day and cannot
-- be followed from one day to the next.

-- One row per pageview. `id` is the random pageview number the tracker picks,
-- so the reading-time update that follows can find its row by primary key.
CREATE TABLE IF NOT EXISTS hits (
  id           INTEGER PRIMARY KEY,
  ts           INTEGER NOT NULL,            -- unix seconds, UTC
  day          TEXT    NOT NULL,            -- YYYY-MM-DD in the paper's timezone
  hour         INTEGER NOT NULL,            -- 0-23 in the paper's timezone
  path         TEXT    NOT NULL,            -- /a-some-story, /, /diamonds ...
  title        TEXT,
  desk         TEXT,                        -- desk slug, articles only
  published    TEXT,                        -- YYYY-MM-DD, articles only
  visitor      TEXT    NOT NULL,            -- daily-salted hash, see above
  entry        INTEGER NOT NULL DEFAULT 0,  -- 1 = this pageview starts a visit
  channel      TEXT    NOT NULL,            -- Search, Social, AI, Email, Paid, Referral, Direct, Internal
  ref          TEXT,                        -- referring site (or campaign source)
  utm_campaign TEXT,
  country      TEXT,                        -- ISO 3166 alpha-2
  city         TEXT,
  device       TEXT,                        -- Desktop, Mobile, Tablet
  browser      TEXT,
  os           TEXT,
  engaged      INTEGER NOT NULL DEFAULT 0,  -- seconds of active reading
  depth        INTEGER NOT NULL DEFAULT 0   -- furthest point reached in the article, percent
);
CREATE INDEX IF NOT EXISTS hits_ts   ON hits (ts);
CREATE INDEX IF NOT EXISTS hits_path ON hits (path, ts);

-- Daily totals by dimension, rebuilt from `hits` by the hourly roll-up.
-- The dashboard reads these, so a year of figures costs a few thousand rows.
CREATE TABLE IF NOT EXISTS daily (
  dim       TEXT    NOT NULL,   -- total, hour, path, desk, channel, ref, campaign, country, city, device, browser, os
  day       TEXT    NOT NULL,
  key       TEXT    NOT NULL,
  views     INTEGER NOT NULL,
  readers   INTEGER NOT NULL,   -- distinct visitors that day
  visits    INTEGER NOT NULL,   -- pageviews that started a visit
  engaged   INTEGER NOT NULL,   -- total seconds of active reading
  engaged_n INTEGER NOT NULL,   -- pageviews that reported reading time
  reads     INTEGER NOT NULL,   -- article pageviews that reached the end
  articles  INTEGER NOT NULL,   -- article pageviews that reported how far they got
  PRIMARY KEY (dim, day, key)
) WITHOUT ROWID;

-- The latest title, desk and publication date seen for each page.
CREATE TABLE IF NOT EXISTS pages (
  path      TEXT PRIMARY KEY,
  title     TEXT,
  desk      TEXT,
  published TEXT,
  last_seen INTEGER
) WITHOUT ROWID;

-- One random salt per day; deleted after two days.
CREATE TABLE IF NOT EXISTS salts (
  day  TEXT PRIMARY KEY,
  salt TEXT NOT NULL
) WITHOUT ROWID;

-- Small settings: the session-signing salt and roll-up timestamps.
CREATE TABLE IF NOT EXISTS meta (
  k TEXT PRIMARY KEY,
  v TEXT NOT NULL
) WITHOUT ROWID;
