-- Online accounts are optional. Existing local profiles, installs and game data remain intact.
-- Account identifiers are auth provider UUIDs; sessions/credentials never enter SQLite.
CREATE TABLE IF NOT EXISTS online_outbox (
    id TEXT PRIMARY KEY,
    profile_id TEXT NOT NULL REFERENCES profiles(id),
    kind TEXT NOT NULL CHECK(kind IN ('favorite', 'played', 'started', 'preferences')),
    game_id TEXT,
    payload_json TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_online_outbox_owner
    ON online_outbox(profile_id, created_at, id);
CREATE TABLE IF NOT EXISTS online_imports (
    profile_id TEXT NOT NULL REFERENCES profiles(id),
    source_profile_id TEXT NOT NULL REFERENCES profiles(id),
    imported_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(profile_id, source_profile_id)
);
