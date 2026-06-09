import sqlite3
import pickle
import numpy as np

from feature_extractor import extract_feature

DB_PATH = "animals.db"

def search_image(query_image, top_k=5):

    query_vec = extract_feature(query_image)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT file_name, feature_vector
        FROM images
    """)

    results = []

    for row in cursor.fetchall():

        file_name = row[0]
        db_vec = pickle.loads(row[1])

        score = np.dot(query_vec, db_vec)

        results.append(
            (file_name, score)
        )

    conn.close()

    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return results[:top_k]