import cv2
import numpy as np

from scipy.stats import skew

from skimage.feature import (
    local_binary_pattern,
    graycomatrix,
    graycoprops,
    hog
)


# ======================================
# Normalize
# ======================================

def normalize(vec):

    vec = np.array(
        vec,
        dtype=np.float32
    )

    norm = np.linalg.norm(vec)

    if norm > 0:
        vec /= norm

    return vec


# ======================================
# HSV HISTOGRAM
# ======================================

def extract_hsv_histogram(hsv):

    hist = cv2.calcHist(
        [hsv],
        [0, 1, 2],
        None,
        [8, 8, 8],
        [0, 180, 0, 256, 0, 256]
    )

    hist = hist.flatten()

    return normalize(hist)


# ======================================
# COLOR MOMENTS
# ======================================

def extract_color_moments(hsv):

    features = []

    for i in range(3):

        channel = hsv[:, :, i]

        mean = np.mean(channel)

        std = np.std(channel)

        skewness = skew(
            channel.flatten()
        )

        features.extend([
            mean,
            std,
            skewness
        ])

    return normalize(features)


# ======================================
# LBP
# ======================================

def extract_lbp(gray):

    radius = 3

    n_points = radius * 8

    lbp = local_binary_pattern(
        gray,
        n_points,
        radius,
        method="uniform"
    )

    hist, _ = np.histogram(
        lbp.ravel(),
        bins=np.arange(
            0,
            n_points + 3
        ),
        range=(
            0,
            n_points + 2
        )
    )

    return normalize(hist)


# ======================================
# GLCM
# ======================================

def extract_glcm(gray):

    glcm = graycomatrix(
        gray,
        distances=[1],
        angles=[0],
        levels=256,
        symmetric=True,
        normed=True
    )

    feature = [

        graycoprops(
            glcm,
            "contrast"
        )[0, 0],

        graycoprops(
            glcm,
            "dissimilarity"
        )[0, 0],

        graycoprops(
            glcm,
            "homogeneity"
        )[0, 0],

        graycoprops(
            glcm,
            "energy"
        )[0, 0],

        graycoprops(
            glcm,
            "correlation"
        )[0, 0],

        graycoprops(
            glcm,
            "ASM"
        )[0, 0]
    ]

    return normalize(feature)


# ======================================
# HOG
# ======================================

def extract_hog(gray):

    feature = hog(
        gray,
        orientations=9,
        pixels_per_cell=(8, 8),
        cells_per_block=(2, 2),
        block_norm="L2-Hys",
        feature_vector=True
    )

    return normalize(feature)


# ======================================
# HU MOMENTS
# ======================================

def extract_hu(gray):

    hu = cv2.HuMoments(
        cv2.moments(gray)
    ).flatten()

    hu = np.sign(hu) * np.log10(
        np.abs(hu) + 1e-10
    )

    return normalize(hu)


# ======================================
# MAIN
# ======================================

def extract_feature(image_path):

    img = cv2.imread(image_path)

    if img is None:

        raise ValueError(
            f"Cannot read image: {image_path}"
        )

    img = cv2.resize(
        img,
        (224, 224)
    )

    hsv = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2HSV
    )

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    features = {

        "hsv":
            extract_hsv_histogram(
                hsv
            ),

        "color":
            extract_color_moments(
                hsv
            ),

        "lbp":
            extract_lbp(
                gray
            ),

        "glcm":
            extract_glcm(
                gray
            ),

        "hog":
            extract_hog(
                gray
            ),

        "hu":
            extract_hu(
                gray
            )
    }

    return features


# ======================================
# TEST
# ======================================

if __name__ == "__main__":

    feat = extract_feature(
        "test.jpg"
    )

    print(
        "HSV:",
        feat["hsv"].shape
    )

    print(
        "Color:",
        feat["color"].shape
    )

    print(
        "LBP:",
        feat["lbp"].shape
    )

    print(
        "GLCM:",
        feat["glcm"].shape
    )

    print(
        "HOG:",
        feat["hog"].shape
    )

    print(
        "HU:",
        feat["hu"].shape
    )