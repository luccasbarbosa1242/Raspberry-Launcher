CREATE TABLE IF NOT EXISTS collections (

    id TEXT PRIMARY KEY,

    name TEXT NOT NULL,

    description TEXT
);

CREATE TABLE IF NOT EXISTS game_collections (

    game_id TEXT NOT NULL,

    collection_id TEXT NOT NULL,

    PRIMARY KEY (
        game_id,
        collection_id
    )
);