-- Retain browser history and foreign identifiers while removing it from runtime.
ALTER TABLE games ADD COLUMN archived INTEGER NOT NULL DEFAULT 0;
ALTER TABLE games ADD COLUMN archive_reason TEXT;
ALTER TABLE game_versions ADD COLUMN archived INTEGER NOT NULL DEFAULT 0;
ALTER TABLE game_versions ADD COLUMN archive_reason TEXT;

UPDATE game_versions SET archived = 1, archive_reason = 'unsupported_browser_game'
WHERE lower(trim(coalesce(launch_type, ''))) IN ('html', 'html5', 'web', 'browser', 'url')
   OR lower(trim(coalesce(platform, ''))) IN ('html', 'html5', 'web', 'browser', 'url')
   OR lower(trim(coalesce(path, ''))) LIKE 'http://%'
   OR lower(trim(coalesce(path, ''))) LIKE 'https://%'
   OR lower(trim(coalesce(path, ''))) LIKE '%.htm'
   OR lower(trim(coalesce(path, ''))) LIKE '%.html'
   OR lower(trim(coalesce(path, ''))) LIKE '%.xhtml'
   OR lower(trim(coalesce(path, ''))) LIKE '%.htm?%'
   OR lower(trim(coalesce(path, ''))) LIKE '%.htm#%'
   OR lower(trim(coalesce(path, ''))) LIKE '%.html?%'
   OR lower(trim(coalesce(path, ''))) LIKE '%.html#%'
   OR lower(trim(coalesce(path, ''))) LIKE '%.xhtml?%'
   OR lower(trim(coalesce(path, ''))) LIKE '%.xhtml#%';

-- An HTML primary does not make a separate native version unsupported. Pick a
-- retained version deterministically, preferring an existing local installation.
CREATE TEMP TABLE phase1_supported_primaries AS
SELECT g.id AS game_id,
       (SELECT v.id FROM game_versions v
        WHERE v.game_id = g.id AND v.archived = 0
        ORDER BY v.installed DESC, v.platform, v.id LIMIT 1) AS version_id
FROM games g
WHERE lower(trim(coalesce(g.type, ''))) IN ('html', 'html5', 'web', 'browser', 'url')
   OR lower(trim(coalesce(g.launch_type, ''))) IN ('html', 'html5', 'web', 'browser', 'url')
   OR lower(trim(coalesce(g.platform, ''))) IN ('html', 'html5', 'web', 'browser', 'url')
   OR lower(trim(coalesce(g.path, ''))) LIKE 'http://%'
   OR lower(trim(coalesce(g.path, ''))) LIKE 'https://%'
   OR lower(trim(coalesce(g.path, ''))) LIKE '%.htm'
   OR lower(trim(coalesce(g.path, ''))) LIKE '%.html'
   OR lower(trim(coalesce(g.path, ''))) LIKE '%.xhtml'
   OR lower(trim(coalesce(g.path, ''))) LIKE '%.htm?%'
   OR lower(trim(coalesce(g.path, ''))) LIKE '%.htm#%'
   OR lower(trim(coalesce(g.path, ''))) LIKE '%.html?%'
   OR lower(trim(coalesce(g.path, ''))) LIKE '%.html#%'
   OR lower(trim(coalesce(g.path, ''))) LIKE '%.xhtml?%'
   OR lower(trim(coalesce(g.path, ''))) LIKE '%.xhtml#%';

UPDATE games SET
    type = CASE WHEN lower(trim(type)) = 'rom' THEN 'rom' ELSE 'native' END,
    (platform, path, launch_type, download_url, archive_name, archive_type,
     executable, strip_root_folder, score_enabled, installed) =
    (SELECT platform, path, launch_type, download_url, archive_name, archive_type,
            executable, strip_root_folder, score_enabled, installed
     FROM game_versions WHERE id =
       (SELECT version_id FROM phase1_supported_primaries p WHERE p.game_id = games.id))
WHERE id IN (SELECT game_id FROM phase1_supported_primaries WHERE version_id IS NOT NULL);

UPDATE game_installations SET
    version_id = (SELECT version_id FROM phase1_supported_primaries p WHERE p.game_id = game_installations.game_id),
    executable_path = (SELECT path FROM games WHERE id = game_installations.game_id),
    installed = (SELECT installed FROM games WHERE id = game_installations.game_id)
WHERE game_id IN (SELECT game_id FROM phase1_supported_primaries WHERE version_id IS NOT NULL);

UPDATE games SET archived = 1, archive_reason = 'unsupported_browser_game'
WHERE lower(trim(coalesce(type, ''))) IN ('html', 'html5', 'web', 'browser', 'url')
   OR lower(trim(coalesce(launch_type, ''))) IN ('html', 'html5', 'web', 'browser', 'url')
   OR lower(trim(coalesce(platform, ''))) IN ('html', 'html5', 'web', 'browser', 'url')
   OR lower(trim(coalesce(path, ''))) LIKE 'http://%'
   OR lower(trim(coalesce(path, ''))) LIKE 'https://%'
   OR lower(trim(coalesce(path, ''))) LIKE '%.htm'
   OR lower(trim(coalesce(path, ''))) LIKE '%.html'
   OR lower(trim(coalesce(path, ''))) LIKE '%.xhtml'
   OR lower(trim(coalesce(path, ''))) LIKE '%.htm?%'
   OR lower(trim(coalesce(path, ''))) LIKE '%.htm#%'
   OR lower(trim(coalesce(path, ''))) LIKE '%.html?%'
   OR lower(trim(coalesce(path, ''))) LIKE '%.html#%'
   OR lower(trim(coalesce(path, ''))) LIKE '%.xhtml?%'
   OR lower(trim(coalesce(path, ''))) LIKE '%.xhtml#%';

UPDATE game_versions SET archived = 1, archive_reason = 'unsupported_browser_game'
WHERE game_id IN (SELECT id FROM games WHERE archived = 1);

DROP TABLE phase1_supported_primaries;

CREATE INDEX IF NOT EXISTS idx_games_active ON games(archived, title);
CREATE INDEX IF NOT EXISTS idx_game_versions_active ON game_versions(game_id, archived);
