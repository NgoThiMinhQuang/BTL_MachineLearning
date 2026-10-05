# MÔ TẢ BỘ DỮ LIỆU

## 1. Tên bộ dữ liệu

Concrete Compressive Strength

## 2. Nguồn dữ liệu

UCI Machine Learning Repository.
Bộ dữ liệu được lấy từ UCI Machine Learning Repository.

Nguồn:
https://archive.ics.uci.edu/dataset/165/concrete+compressive+strength

DOI:
https://doi.org/10.24432/C5PK67

## 3. Mục đích sử dụng

Bộ dữ liệu được sử dụng để xây dựng mô hình hồi quy dự đoán
cường độ nén của bê tông dựa trên thành phần cấp phối và tuổi bê tông.
## 4. Quy mô dữ liệu

- Số mẫu: 1030
- Số biến đầu vào: 8
- Số biến đầu ra: 1
- Tổng số cột : 9
## 4. Biến đầu ra

Biến cần dự đoán:

strength

Ý nghĩa:

Cường độ nén của bê tông.

Đơn vị:

MPa.

## 5. Các biến đầu vào

1. cement - hàm lượng xi măng
2. slag - hàm lượng xỉ lò cao
3. fly_ash - hàm lượng tro bay
4. water - hàm lượng nước
5. superplasticizer - phụ gia siêu dẻo
6. coarse_aggregate - cốt liệu thô
7. fine_aggregate - cốt liệu mịn
8. age - tuổi bê tông

## 6. Chất lượng dữ liệu ban đầu

- Không có giá trị thiếu.
- Phát hiện 25 lần xuất hiện trùng lặp.
- Tất cả các biến đều là dữ liệu số.
- Dữ liệu gốc được giữ nguyên, không chỉnh sửa trực tiếp.

## 9. Dữ liệu trùng lặp

Phát hiện 25 lần xuất hiện trùng lặp bằng:

df.duplicated().sum()

Danh sách tất cả các dòng thuộc nhóm trùng lặp được lưu tại:

reports/tables/duplicate_rows.csv

Các dòng này chưa bị loại bỏ tùy tiện.
Việc chia train/validation/test sẽ bảo đảm các mẫu có cùng
đầu vào không xuất hiện ở nhiều tập khác nhau.

## 10. Giấy phép

Theo thông tin của UCI Machine Learning Repository,
bộ dữ liệu được phân phối theo giấy phép CC BY 4.0.

## 11. Ngày truy cập

01/10/2026

## 7. Vị trí dữ liệu gốc

data/raw/Concrete_Data.xls