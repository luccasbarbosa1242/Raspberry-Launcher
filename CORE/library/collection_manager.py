from CORE.library.collection_repository import (
    CollectionRepository
)


class CollectionManager:

    def __init__(self):

        self.repository = (
            CollectionRepository()
        )

    def all_collections(self):

        return (
            self.repository
            .all()
        )

    def games_from_collection(
        self,
        collection_id
    ):

        return (
            self.repository
            .games_from_collection(
                collection_id
            )
        )