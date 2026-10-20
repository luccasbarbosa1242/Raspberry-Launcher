-- Catalog metadata is independent from packages and local installations.
ALTER TABLE game_versions ADD COLUMN architecture TEXT NOT NULL DEFAULT 'any';
ALTER TABLE platforms ADD COLUMN examples_json TEXT NOT NULL DEFAULT '[]';

ALTER TABLE emulator_packages ADD COLUMN emulator_id TEXT REFERENCES emulators(id);
ALTER TABLE emulator_packages ADD COLUMN system TEXT;
ALTER TABLE emulator_packages ADD COLUMN architecture TEXT NOT NULL DEFAULT 'any';
ALTER TABLE emulator_packages ADD COLUMN archive_type TEXT;
CREATE UNIQUE INDEX IF NOT EXISTS emulator_package_target
    ON emulator_packages(emulator_id, system, architecture, version);

CREATE TABLE IF NOT EXISTS emulator_installations (
    emulator_id TEXT PRIMARY KEY REFERENCES emulators(id),
    package_id TEXT REFERENCES emulator_packages(id),
    version TEXT,
    install_path TEXT,
    executable_path TEXT,
    installed INTEGER NOT NULL DEFAULT 0 CHECK(installed IN (0,1))
);
INSERT OR IGNORE INTO emulator_installations(
    emulator_id,version,install_path,executable_path,installed
) SELECT id,version,install_path,executable_path,COALESCE(installed,0) FROM emulators;

-- Legacy tools may still write installation columns on emulators.
-- Runtime reads the independent installation table exclusively.
CREATE TRIGGER IF NOT EXISTS emulator_legacy_insert AFTER INSERT ON emulators
BEGIN
    INSERT INTO emulator_installations(emulator_id,version,install_path,executable_path,installed)
    VALUES(NEW.id,NEW.version,NEW.install_path,NEW.executable_path,COALESCE(NEW.installed,0))
    ON CONFLICT(emulator_id) DO UPDATE SET version=excluded.version,
        install_path=excluded.install_path,executable_path=excluded.executable_path,
        installed=excluded.installed;
END;
CREATE TRIGGER IF NOT EXISTS emulator_legacy_update
AFTER UPDATE OF version,install_path,executable_path,installed ON emulators
BEGIN
    INSERT INTO emulator_installations(emulator_id,version,install_path,executable_path,installed)
    VALUES(NEW.id,NEW.version,NEW.install_path,NEW.executable_path,COALESCE(NEW.installed,0))
    ON CONFLICT(emulator_id) DO UPDATE SET version=excluded.version,
        install_path=excluded.install_path,executable_path=excluded.executable_path,
        installed=excluded.installed;
END;

CREATE TABLE IF NOT EXISTS game_installations (
    game_id TEXT PRIMARY KEY REFERENCES games(id),
    version_id TEXT REFERENCES game_versions(id),
    executable_path TEXT,
    installed INTEGER NOT NULL DEFAULT 0 CHECK(installed IN (0,1))
);
CREATE TABLE IF NOT EXISTS game_version_installations (
    version_id TEXT PRIMARY KEY REFERENCES game_versions(id),
    game_id TEXT NOT NULL REFERENCES games(id),
    executable_path TEXT,
    installed INTEGER NOT NULL DEFAULT 0 CHECK(installed IN (0,1))
);

-- Models reserved for later phases. No profile selection or source sync yet.
-- Current favorites and play time continue using the existing game fields.
CREATE TABLE IF NOT EXISTS profiles (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS profile_game_state (
    profile_id TEXT NOT NULL REFERENCES profiles(id),
    game_id TEXT NOT NULL REFERENCES games(id),
    favorite INTEGER NOT NULL DEFAULT 0,
    play_time INTEGER NOT NULL DEFAULT 0,
    last_played TEXT,
    PRIMARY KEY(profile_id,game_id)
);
CREATE TABLE IF NOT EXISTS catalog_sources (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    base_url TEXT
);
CREATE TABLE IF NOT EXISTS external_game_ids (
    source_id TEXT NOT NULL REFERENCES catalog_sources(id),
    external_id TEXT NOT NULL,
    game_id TEXT NOT NULL REFERENCES games(id),
    PRIMARY KEY(source_id,external_id),
    UNIQUE(source_id,game_id)
);
