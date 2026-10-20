from backend.database.database import Database


class CollectionRepository:
    def __init__(self):

        self.db = Database()

    def all(self):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT *
            FROM collections
            ORDER BY name ASC
            """
        )

        return cursor.fetchall()

    def games_from_collection(self, collection_id):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT g.*
            FROM games g
            INNER JOIN game_collections gc
                ON gc.game_id = g.id
            WHERE gc.collection_id = ?
            ORDER BY g.title ASC
            """,
            (collection_id,),
        )

        return cursor.fetchall()
