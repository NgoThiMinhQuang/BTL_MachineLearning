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

Kết quả kiểm tra bằng hàm duplicated() của pandas phát hiện 25 lần xuất hiện trùng lặp.

Các dòng thuộc nhóm trùng lặp đã được lưu tại:

reports/tables/duplicate_rows.csv

Các dòng trùng lặp chưa được xóa ngay.

Nhóm tiếp tục kiểm tra và xử lý sao cho các mẫu có cùng đầu vào không xuất hiện đồng thời ở tập huấn luyện và tập kiểm thử, nhằm hạn chế rò rỉ thông tin giữa các tập dữ liệu.

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