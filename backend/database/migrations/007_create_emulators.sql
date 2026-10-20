CREATE TABLE IF NOT EXISTS emulators (

    id TEXT PRIMARY KEY,

    name TEXT NOT NULL,

    version TEXT,

    install_path TEXT,

    executable_path TEXT,

    installed INTEGER DEFAULT 0,

    plugin_id TEXT
);