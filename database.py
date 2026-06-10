import sqlite3

DB_NAME = "animals.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    DROP TABLE IF EXISTS images
    """)

    cursor.execute("""
    CREATE TABLE images(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        file_name TEXT NOT NULL,

        animal_type TEXT NOT NULL,

        hsv_feature BLOB,

        color_feature BLOB,

        lbp_feature BLOB,

        glcm_feature BLOB,

        hog_feature BLOB,

        hu_feature BLOB
    )
    """)

    conn.commit()
    conn.close()


def count_images():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM images
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


if __name__ == "__main__":

    create_database()

    print("Database created.")