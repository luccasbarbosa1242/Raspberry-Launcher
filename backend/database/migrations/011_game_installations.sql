-- The old installed/path columns remain a write-compatible interface for tools.
-- Runtime reads use the local installation records rather than catalog state.
INSERT INTO game_version_installations(version_id, game_id, executable_path, installed)
SELECT id, game_id, path, CASE WHEN installed = 1 THEN 1 ELSE 0 END
FROM game_versions;

INSERT INTO game_installations(game_id, version_id, executable_path, installed)
SELECT g.id,
       (SELECT v.id FROM game_versions v
        WHERE v.game_id = g.id AND v.installed = 1 AND v.archived = 0
        ORDER BY v.id LIMIT 1),
       g.path, CASE WHEN g.installed = 1 THEN 1 ELSE 0 END
FROM games g;

CREATE TRIGGER game_installation_insert AFTER INSERT ON games
BEGIN
    INSERT INTO game_installations(game_id, executable_path, installed)
    VALUES(NEW.id, NEW.path, CASE WHEN NEW.installed = 1 THEN 1 ELSE 0 END)
    ON CONFLICT(game_id) DO UPDATE SET
        executable_path = excluded.executable_path, installed = excluded.installed;
END;

CREATE TRIGGER game_installation_update AFTER UPDATE OF path, installed ON games
WHEN NEW.path IS NOT OLD.path OR NEW.installed IS NOT OLD.installed
BEGIN
    INSERT INTO game_installations(game_id, version_id, executable_path, installed)
    VALUES(NEW.id,
        (SELECT id FROM game_versions WHERE game_id = NEW.id AND installed = 1
         AND archived = 0 ORDER BY id LIMIT 1),
        NEW.path, CASE WHEN NEW.installed = 1 THEN 1 ELSE 0 END)
    ON CONFLICT(game_id) DO UPDATE SET version_id = excluded.version_id,
        executable_path = excluded.executable_path, installed = excluded.installed;
END;

CREATE TRIGGER game_installation_delete AFTER DELETE ON games
BEGIN
    DELETE FROM game_installations WHERE game_id = OLD.id;
    DELETE FROM game_version_installations WHERE game_id = OLD.id;
END;

CREATE TRIGGER version_installation_insert AFTER INSERT ON game_versions
BEGIN
    INSERT INTO game_version_installations(version_id, game_id, executable_path, installed)
    VALUES(NEW.id, NEW.game_id, NEW.path, CASE WHEN NEW.installed = 1 THEN 1 ELSE 0 END)
    ON CONFLICT(version_id) DO UPDATE SET game_id = excluded.game_id,
        executable_path = excluded.executable_path, installed = excluded.installed;
    UPDATE game_installations SET version_id =
        (SELECT id FROM game_versions WHERE game_id = NEW.game_id AND installed = 1
         AND archived = 0 ORDER BY id LIMIT 1)
    WHERE game_id = NEW.game_id;
END;

CREATE TRIGGER version_installation_update AFTER UPDATE OF path, installed ON game_versions
WHEN NEW.path IS NOT OLD.path OR NEW.installed IS NOT OLD.installed
BEGIN
    INSERT INTO game_version_installations(version_id, game_id, executable_path, installed)
    VALUES(NEW.id, NEW.game_id, NEW.path, CASE WHEN NEW.installed = 1 THEN 1 ELSE 0 END)
    ON CONFLICT(version_id) DO UPDATE SET game_id = excluded.game_id,
        executable_path = excluded.executable_path, installed = excluded.installed;
    UPDATE game_installations SET version_id =
        (SELECT id FROM game_versions WHERE game_id = NEW.game_id AND installed = 1
         AND archived = 0 ORDER BY id LIMIT 1)
    WHERE game_id = NEW.game_id;
END;

CREATE TRIGGER version_installation_delete AFTER DELETE ON game_versions
BEGIN
    DELETE FROM game_version_installations WHERE version_id = OLD.id;
    UPDATE game_installations SET version_id = NULL WHERE version_id = OLD.id;
END;

CREATE VIEW runtime_games AS
SELECT g.id, g.title, g.type, g.platform,
       COALESCE(i.executable_path, g.path) AS path,
       g.launch_type, g.download_url, g.archive_name, g.archive_type, g.executable,
       g.strip_root_folder, g.score_enabled, COALESCE(i.installed, 0) AS installed,
       g.favorite, g.play_time, g.last_played, g.cover_url, g.banner_url, g.logo_url,
       g.archived, g.archive_reason
FROM games g LEFT JOIN game_installations i ON i.game_id = g.id;

CREATE VIEW runtime_game_versions AS
SELECT v.id, v.game_id, v.platform,
       COALESCE(i.executable_path, v.path) AS path,
       v.launch_type, v.download_url, v.archive_name, v.archive_type, v.executable,
       v.strip_root_folder, v.score_enabled, COALESCE(i.installed, 0) AS installed,
       v.architecture, v.archived, v.archive_reason
FROM game_versions v LEFT JOIN game_version_installations i ON i.version_id = v.id;
