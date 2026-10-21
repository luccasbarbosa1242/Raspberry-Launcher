-- T02: preserve existing personal data, including archived games.
-- Installation and catalog records remain shared between local profiles.
INSERT OR IGNORE INTO profiles(id, name) VALUES ('default', 'Padrão');

CREATE TABLE IF NOT EXISTS profile_preferences (
    profile_id TEXT PRIMARY KEY REFERENCES profiles(id),
    theme TEXT NOT NULL DEFAULT 'dark'
        CHECK(theme IN ('dark','light','system')),
    music_volume INTEGER NOT NULL DEFAULT 50
        CHECK(music_volume BETWEEN 0 AND 100)
);

CREATE TABLE IF NOT EXISTS profile_collections (
    profile_id TEXT NOT NULL REFERENCES profiles(id),
    collection_id TEXT NOT NULL REFERENCES collections(id),
    PRIMARY KEY(profile_id, collection_id)
);

-- This snapshot is deliberately INSERT OR IGNORE, not UPDATE: repeated startup
-- must never replace subsequent profile usage with the legacy game columns.
INSERT OR IGNORE INTO profile_game_state(
    profile_id, game_id, favorite, play_time, last_played
)
SELECT 'default', id, COALESCE(favorite, 0),
       MAX(0, COALESCE(play_time, 0)), last_played
FROM games;

INSERT OR IGNORE INTO profile_preferences(profile_id)
SELECT id FROM profiles;

INSERT OR IGNORE INTO settings(key, value)
VALUES ('active_profile_id', 'default');

-- Old importers may still create games by SQL; new rows inherit their legacy
-- personal fields only for the default profile. Existing records are untouched.
CREATE TRIGGER IF NOT EXISTS profile_default_game_insert
AFTER INSERT ON games
BEGIN
    INSERT OR IGNORE INTO profile_game_state(
        profile_id, game_id, favorite, play_time, last_played
    ) VALUES(
        'default', NEW.id, COALESCE(NEW.favorite, 0),
        MAX(0, COALESCE(NEW.play_time, 0)), NEW.last_played
    );
END;

CREATE INDEX IF NOT EXISTS idx_profile_recent
ON profile_game_state(profile_id, last_played);
