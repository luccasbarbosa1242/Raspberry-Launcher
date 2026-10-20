CREATE TABLE IF NOT EXISTS platforms (

    id TEXT PRIMARY KEY,

    name TEXT NOT NULL,

    type TEXT NOT NULL,

    plugin_id TEXT,

    emulator_id TEXT
);