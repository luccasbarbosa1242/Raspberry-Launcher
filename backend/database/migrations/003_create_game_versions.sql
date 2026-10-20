CREATE TABLE IF NOT EXISTS game_versions (

    id TEXT PRIMARY KEY,

    game_id TEXT NOT NULL,

    platform TEXT NOT NULL,

    path TEXT NOT NULL,

    launch_type TEXT,

    download_url TEXT,

    archive_name TEXT,

    archive_type TEXT,

    executable TEXT,

    strip_root_folder INTEGER DEFAULT 0,

    score_enabled INTEGER DEFAULT 0,

    installed INTEGER DEFAULT 0,

    UNIQUE(game_id, platform)
);