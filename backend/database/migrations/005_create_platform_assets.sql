CREATE TABLE  IF NOT EXISTS platform_assets (

    id TEXT PRIMARY KEY,

    platform_id TEXT NOT NULL,

    type TEXT NOT NULL,

    remote_url TEXT,

    local_path TEXT,

    downloaded INTEGER DEFAULT 0
);

