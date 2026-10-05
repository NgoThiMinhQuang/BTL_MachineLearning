# BÁO CÁO CHẤT LƯỢNG DỮ LIỆU

## 1. Kích thước bộ dữ liệu

Bộ dữ liệu ban đầu gồm:

- 1030 dòng
- 9 cột
- 8 biến đầu vào
- 1 biến đầu ra

Biến đầu ra là:

strength

## 2. Kiểu dữ liệu

Tất cả các biến đều là dữ liệu số.

- age có kiểu số nguyên
- các biến còn lại có kiểu số thực

## 3. Giá trị thiếu

Kết quả kiểm tra cho thấy không có giá trị thiếu trong toàn bộ 9 biến.

Do đó, nhóm không cần thực hiện phương pháp điền giá trị thiếu.

## 4. Dữ liệu trùng lặp

Kết quả kiểm tra bằng hàm duplicated() của pandas cho thấy
25 bản ghi được đánh dấu là trùng lặp so với các bản ghi xuất hiện trước đó.

Khi lấy toàn bộ các dòng thuộc những nhóm trùng lặp bằng
duplicated(keep=False), có 36 dòng thuộc 11 nhóm trùng lặp hoàn toàn.

Các dòng thuộc nhóm trùng lặp đã được lưu tại:

reports/tables/duplicate_rows.csv

Các dòng trùng lặp chưa được xóa ngay.

Nhóm sử dụng cơ chế chia theo nhóm dựa trên 8 biến đầu vào
để các mẫu có cùng bộ giá trị đầu vào không bị phân tán
giữa Train, Validation và Test, qua đó hạn chế một nguồn
rò rỉ thông tin giữa các tập dữ liệu.

## 5. Biến mục tiêu

Biến mục tiêu:

strength

Đơn vị:

MPa

Giá trị nhỏ nhất quan sát được:

khoảng 2,33 MPa

Giá trị lớn nhất quan sát được:

khoảng 82,60 MPa

## 6. Tuổi bê tông

Tuổi nhỏ nhất:

1 ngày

Tuổi lớn nhất:

365 ngày

## 7. Giá trị ngoại lệ

Trong bước kiểm tra ban đầu, nhóm chưa tự động loại bỏ các giá trị
cực trị trong dữ liệu.

Các giá trị lớn hoặc nhỏ bất thường có thể là các cấp phối bê tông
thực tế và việc loại bỏ tùy tiện có thể làm thay đổi phân bố dữ liệu.

Do đó, các điểm cực trị sẽ được quan sát trong EDA và đặc biệt được
phân tích lại thông qua residual sau khi xây dựng mô hình.

Chỉ loại bỏ một mẫu khi có bằng chứng rõ ràng cho thấy đó là dữ liệu lỗi.