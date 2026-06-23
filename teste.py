from CORE.database.database import Database

db = Database()
cursor = db.cursor()

cursor.execute("SELECT * FROM assets")

rows = cursor.fetchall()

for row in rows:
    print(dict(row))

db.close()