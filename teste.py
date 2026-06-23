from CORE.database.database import Database

db = Database()
cursor = db.cursor()

cursor.execute("SELECT * FROM assets")

for row in cursor.fetchall():
    print(dict(row))

db.close()