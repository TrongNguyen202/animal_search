import os
import pickle

from database import (
    create_database,
    get_connection
)

from feature_extractor import (
    extract_feature
)


DATASET_PATH = "dataset"


def build_database():

    print(
        "Creating database..."
    )

    create_database()

    conn = get_connection()

    cursor = conn.cursor()

    inserted = 0

    animals = os.listdir(
        DATASET_PATH
    )

    for animal in animals:

        animal_folder = os.path.join(
            DATASET_PATH,
            animal
        )

        if not os.path.isdir(
            animal_folder
        ):
            continue

        print(
            f"\nProcessing: {animal}"
        )

        files = os.listdir(
            animal_folder
        )

        for file in files:

            if not file.lower().endswith(
                (
                    ".jpg",
                    ".jpeg",
                    ".png",
                    ".bmp"
                )
            ):
                continue

            image_path = os.path.join(
                animal_folder,
                file
            )

            try:

                feature = extract_feature(
                    image_path
                )

                cursor.execute("""
                INSERT INTO images(

                    file_name,
                    animal_type,

                    hsv_feature,
                    color_feature,
                    lbp_feature,
                    glcm_feature,
                    hog_feature,
                    hu_feature

                )
                VALUES(
                    ?, ?, ?, ?, ?, ?, ?, ?
                )
                """,
                (
                    image_path,
                    animal,

                    pickle.dumps(
                        feature["hsv"]
                    ),

                    pickle.dumps(
                        feature["color"]
                    ),

                    pickle.dumps(
                        feature["lbp"]
                    ),

                    pickle.dumps(
                        feature["glcm"]
                    ),

                    pickle.dumps(
                        feature["hog"]
                    ),

                    pickle.dumps(
                        feature["hu"]
                    )
                ))

                inserted += 1

                if inserted % 100 == 0:

                    print(
                        f"Inserted: {inserted}"
                    )

            except Exception as e:

                print(
                    f"Error: {image_path}"
                )

                print(e)

    conn.commit()

    conn.close()

    print(
        "\nFinished."
    )

    print(
        f"Total inserted: {inserted}"
    )


if __name__ == "__main__":

    build_database()