# ANIMAL IMAGE RETRIEVAL SYSTEM

## 1. Giới thiệu

Animal Image Retrieval System là hệ thống tìm kiếm ảnh động vật bốn chân dựa trên nội dung ảnh (Content-Based Image Retrieval - CBIR).

Hệ thống cho phép người dùng đưa vào một ảnh truy vấn (query image), sau đó tìm kiếm trong cơ sở dữ liệu và trả về 5 ảnh có nội dung tương đồng nhất.

Hệ thống sử dụng các đặc trưng thị giác truyền thống:

* HSV Histogram
* Color Moments
* Local Binary Pattern (LBP)
* Gray Level Co-occurrence Matrix (GLCM)
* Histogram of Oriented Gradients (HOG)
* Hu Moments

Độ tương đồng được tính bằng Cosine Similarity và kết hợp theo trọng số do người dùng lựa chọn trên giao diện.

---

# 2. Mục tiêu

* Xây dựng cơ sở dữ liệu lưu trữ ảnh động vật bốn chân.
* Trích xuất và lưu trữ đặc trưng ảnh.
* Tìm kiếm ảnh tương đồng dựa trên nội dung.
* Hiển thị Top-K ảnh giống nhất.
* Cho phép điều chỉnh trọng số các đặc trưng để đánh giá hiệu quả tìm kiếm.

---

# 3. Cấu trúc thư mục

```text
animal_search/

│
├── dataset/
│   ├── horse/
│   ├── dog/
│   ├── cat/
│   ├── cow/
│   └── zebra/
│
├── app.py
├── search.py
├── database.py
├── feature_extractor.py
├── build_database.py
│
├── animals.db
│
└── README.md
```

---

# 4. Các đặc trưng sử dụng

## 4.1 HSV Histogram

Mô tả phân bố màu sắc của ảnh trong không gian màu HSV.

Ưu điểm:

* Phân biệt các loài có màu sắc khác nhau.
* Ít nhạy với thay đổi độ sáng hơn RGB.

---

## 4.2 Color Moments

Bao gồm:

* Mean
* Standard Deviation
* Skewness

Mô tả đặc trưng thống kê của từng kênh màu.

Ưu điểm:

* Kích thước vector nhỏ.
* Thể hiện đặc tính màu tổng quát.

---

## 4.3 Local Binary Pattern (LBP)

Mô tả kết cấu bề mặt (texture).

Ưu điểm:

* Nhận diện lông, da, vằn sọc.
* Hiệu quả với ảnh động vật.

---

## 4.4 GLCM

Gray Level Co-occurrence Matrix.

Bao gồm:

* Contrast
* Dissimilarity
* Homogeneity
* Energy
* Correlation
* ASM

Ưu điểm:

* Đánh giá kết cấu ảnh.
* Bổ sung thông tin cho LBP.

---

## 4.5 HOG

Histogram of Oriented Gradients.

Ưu điểm:

* Mô tả hình dạng đối tượng.
* Nhận diện tư thế và cấu trúc cơ thể.

---

## 4.6 Hu Moments

Mô tả hình dạng tổng thể.

Ưu điểm:

* Bất biến với:

  * Tịnh tiến
  * Phóng to thu nhỏ
  * Xoay

---

# 5. Công thức tính độ tương đồng

Cosine Similarity:

[
Similarity(A,B)=
\frac{A \cdot B}
{|A||B|}
]

Trong đó:

* A là vector đặc trưng ảnh truy vấn.
* B là vector đặc trưng ảnh trong cơ sở dữ liệu.

Giá trị nằm trong khoảng:

```text
0 → Không giống nhau
1 → Giống hoàn toàn
```

---

# 6. Công thức tính điểm cuối cùng

Điểm tương đồng tổng hợp:

```text
Final Score =

w_hsv × HSV_Score +

w_color × Color_Score +

w_lbp × LBP_Score +

w_glcm × GLCM_Score +

w_hog × HOG_Score +

w_hu × HU_Score
```

Ví dụ:

```text
HSV   = 0.25
Color = 0.20
LBP   = 0.15
GLCM  = 0.10
HOG   = 0.15
HU    = 0.15
```

Tổng trọng số bằng:

```text
1.00
```

---

# 7. Cơ sở dữ liệu

SQLite được sử dụng để lưu trữ đặc trưng ảnh.

Bảng:

```sql
CREATE TABLE images(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    file_name TEXT,

    animal_type TEXT,

    hsv_feature BLOB,

    color_feature BLOB,

    lbp_feature BLOB,

    glcm_feature BLOB,

    hog_feature BLOB,

    hu_feature BLOB
);
```

---

# 8. Quy trình hoạt động

```text
Input Image
      |
      V
Feature Extraction
      |
      V
HSV
Color Moments
LBP
GLCM
HOG
HU
      |
      V
Similarity Calculation
      |
      V
Weighted Fusion
      |
      V
Ranking
      |
      V
Top-5 Similar Images
```

---

# 9. Giao diện

Hệ thống hỗ trợ:

* Chọn ảnh truy vấn.
* Điều chỉnh trọng số.
* Tìm kiếm Top-K.
* Hiển thị ảnh kết quả.
* Xem chi tiết từng ảnh.
* Biểu đồ đóng góp của từng đặc trưng.

---

# 10. Cài đặt

Cài đặt thư viện:

```bash
pip install numpy
pip install scipy
pip install pillow
pip install opencv-python
pip install scikit-image
pip install matplotlib
pip install customtkinter
```

---

# 11. Tạo cơ sở dữ liệu

```bash
python build_database.py
```

Sau khi hoàn thành:

```text
animals.db
```

sẽ được tạo tự động.

---

# 12. Chạy chương trình

```bash
python app.py
```

---

# 13. Kết quả

Đầu vào:

```text
1 ảnh động vật bốn chân
```

Đầu ra:

```text
Top 5 ảnh tương đồng nhất
```

được sắp xếp giảm dần theo độ tương đồng.

---

# 14. Hướng phát triển

* Bổ sung nhiều loài động vật hơn.
* Tăng kích thước dataset.
* Tối ưu trọng số đặc trưng.
* Tự động phát hiện đối tượng trước khi trích đặc trưng.
* So sánh hiệu quả giữa các phương pháp đặc trưng khác nhau.

---

# 15. Tác giả

Animal Image Retrieval System

CBIR using HSV, Color Moments, LBP, GLCM, HOG and Hu Moments.
