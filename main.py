import sqlite3
import os

db = "animals.db"

print(os.path.abspath(db))

conn = sqlite3.connect(db)

cursor = conn.cursor()

cursor.execute(
    "SELECT COUNT(*) FROM images"
)

print(cursor.fetchone())

conn.close()