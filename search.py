import pickle
import numpy as np

from database import get_connection
from feature_extractor import extract_feature


# ======================================
# COSINE SIMILARITY
# ======================================

def cosine_similarity(a, b):

    a_norm = np.linalg.norm(a)
    b_norm = np.linalg.norm(b)

    if a_norm == 0 or b_norm == 0:
        return 0

    return np.dot(a, b) / (
        a_norm * b_norm
    )


# ======================================
# SEARCH
# ======================================

def search_image(
        image_path,
        top_k=5,

        w_hsv=0.25,
        w_color=0.20,
        w_lbp=0.15,
        w_glcm=0.10,
        w_hog=0.15,
        w_hu=0.15
):

    query = extract_feature(
        image_path
    )

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        file_name,
        animal_type,

        hsv_feature,
        color_feature,
        lbp_feature,
        glcm_feature,
        hog_feature,
        hu_feature

    FROM images
    """)

    results = []

    rows = cursor.fetchall()

    for row in rows:

        file_name = row[0]
        animal_type = row[1]

        hsv_db = pickle.loads(
            row[2]
        )

        color_db = pickle.loads(
            row[3]
        )

        lbp_db = pickle.loads(
            row[4]
        )

        glcm_db = pickle.loads(
            row[5]
        )

        hog_db = pickle.loads(
            row[6]
        )

        hu_db = pickle.loads(
            row[7]
        )

        # ==========================
        # Individual Scores
        # ==========================

        hsv_score = cosine_similarity(
            query["hsv"],
            hsv_db
        )

        color_score = cosine_similarity(
            query["color"],
            color_db
        )

        lbp_score = cosine_similarity(
            query["lbp"],
            lbp_db
        )

        glcm_score = cosine_similarity(
            query["glcm"],
            glcm_db
        )

        hog_score = cosine_similarity(
            query["hog"],
            hog_db
        )

        hu_score = cosine_similarity(
            query["hu"],
            hu_db
        )

        # ==========================
        # Weighted Fusion
        # ==========================

        final_score = (

            w_hsv * hsv_score +

            w_color * color_score +

            w_lbp * lbp_score +

            w_glcm * glcm_score +

            w_hog * hog_score +

            w_hu * hu_score
        )

        results.append({

            "file": file_name,

            "animal": animal_type,

            "score": float(
                final_score
            ),

            "hsv": float(
                hsv_score
            ),

            "color": float(
                color_score
            ),

            "lbp": float(
                lbp_score
            ),

            "glcm": float(
                glcm_score
            ),

            "hog": float(
                hog_score
            ),

            "hu": float(
                hu_score
            )
        })

    conn.close()

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]