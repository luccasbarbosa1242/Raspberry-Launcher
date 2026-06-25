from CORE.library.collection_manager import (
    CollectionManager
)


manager = CollectionManager()

collections = (
    manager
    .all_collections()
)

for collection in collections:

    print(
        collection["id"],
        collection["name"]
    )

    games = (
        manager
        .games_from_collection(
            collection["id"]
        )
    )

    for game in games:

        print(
            "-",
            game["title"]
        )