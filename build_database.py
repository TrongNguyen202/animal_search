import sqlite3
import pickle
import os

from feature_extractor import extract_feature

conn = sqlite3.connect("animals.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS images(
id INTEGER PRIMARY KEY AUTOINCREMENT,
file_name TEXT,
animal_type TEXT,
feature_vector BLOB
)
""")

DATASET = "dataset"

for animal in os.listdir(DATASET):

    folder = os.path.join(DATASET, animal)

    for file in os.listdir(folder):

        path = os.path.join(folder, file)

        vec = extract_feature(path)

        cursor.execute(
            """
            INSERT INTO images
            (file_name, animal_type, feature_vector)
            VALUES(?,?,?)
            """,
            (
                path,
                animal,
                pickle.dumps(vec)
            )
        )

conn.commit()
conn.close()

print("Database created.")