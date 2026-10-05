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
## 5. Biến đầu ra

Biến cần dự đoán:

strength

Ý nghĩa:

Cường độ nén của bê tông.

Đơn vị:

MPa.

## 6. Các biến đầu vào

1. cement - hàm lượng xi măng
2. slag - hàm lượng xỉ lò cao
3. fly_ash - hàm lượng tro bay
4. water - hàm lượng nước
5. superplasticizer - phụ gia siêu dẻo
6. coarse_aggregate - cốt liệu thô
7. fine_aggregate - cốt liệu mịn
8. age - tuổi bê tông

## 7. Chất lượng dữ liệu ban đầu

- Không có giá trị thiếu.
- Có 25 bản ghi được pandas đánh dấu là duplicate
so với bản ghi xuất hiện trước đó.

Có tổng cộng 36 dòng thuộc 11 nhóm duplicate hoàn toàn.
- Tất cả các biến đều là dữ liệu số.
- Dữ liệu gốc được giữ nguyên, không chỉnh sửa trực tiếp.

## 8. Dữ liệu trùng lặp

Kết quả kiểm tra bằng `df.duplicated().sum()` cho thấy
25 bản ghi được đánh dấu là trùng lặp so với bản ghi
xuất hiện trước đó.

Khi sử dụng `duplicated(keep=False)`, có tổng cộng
36 dòng thuộc 11 nhóm trùng lặp hoàn toàn.

Danh sách các dòng thuộc nhóm trùng lặp được lưu tại:

`reports/tables/duplicate_rows.csv`

Nhóm không tự động xóa các dòng này.

Khi chia dữ liệu, các mẫu có cùng bộ giá trị của 8 biến
đầu vào được giữ trong cùng một tập để hạn chế rò rỉ
thông tin giữa Train, Validation và Test.

Danh sách tất cả các dòng thuộc nhóm trùng lặp được lưu tại:

reports/tables/duplicate_rows.csv

Các dòng này chưa bị loại bỏ tùy tiện.
Việc chia train/validation/test sẽ bảo đảm các mẫu có cùng
đầu vào không xuất hiện ở nhiều tập khác nhau.

## 9. Giấy phép

Theo thông tin của UCI Machine Learning Repository,
bộ dữ liệu được phân phối theo giấy phép CC BY 4.0.

## 10. Ngày truy cập

01/10/2026

## 11. Vị trí dữ liệu gốc

data/raw/Concrete_Data.xls

## 12. Checksum

SHA256 của file dữ liệu gốc `Concrete_Data.xls`:
86ea0e3750a58857e81028075ab9cacae81dcc0a6e302b8214b639ad141238a0