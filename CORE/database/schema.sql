CREATE TABLE IF NOT EXISTS games (

    id TEXT PRIMARY KEY,

    title TEXT NOT NULL,

    type TEXT NOT NULL,

    platform TEXT,

    path TEXT NOT NULL,

    launch_type TEXT,

    download_url TEXT,

    archive_name TEXT,

    archive_type TEXT,

    executable TEXT,

    strip_root_folder INTEGER DEFAULT 0,

    score_enabled INTEGER DEFAULT 0,

    installed INTEGER DEFAULT 0,

    favorite INTEGER DEFAULT 0,

    play_time INTEGER DEFAULT 0,

    last_played TEXT,

    cover_url TEXT,

    banner_url TEXT,

    logo_url TEXT
);

CREATE TABLE IF NOT EXISTS emulators (

    id TEXT PRIMARY KEY,

    name TEXT NOT NULL,

    version TEXT,

    install_path TEXT,

    executable_path TEXT,

    installed INTEGER DEFAULT 0,

    plugin_id TEXT
);

CREATE TABLE IF NOT EXISTS platforms (

    id TEXT PRIMARY KEY,

    name TEXT NOT NULL,

    plugin_id TEXT
);

CREATE TABLE IF NOT EXISTS downloads (

    id TEXT PRIMARY KEY,

    game_id TEXT,

    status TEXT,

    progress REAL,

    downloaded_bytes INTEGER,

    total_bytes INTEGER
);

CREATE TABLE IF NOT EXISTS settings (

    key TEXT PRIMARY KEY,

    value TEXT
);

CREATE TABLE IF NOT EXISTS emulator_packages (

    id TEXT PRIMARY KEY,

    name TEXT,

    version TEXT,

    download_url TEXT,

    executable TEXT
);

CREATE TABLE IF NOT EXISTS assets (

    id TEXT PRIMARY KEY,

    game_id TEXT,

    type TEXT NOT NULL,

    remote_url TEXT NOT NULL,

    local_path TEXT,

    downloaded INTEGER DEFAULT 0
);