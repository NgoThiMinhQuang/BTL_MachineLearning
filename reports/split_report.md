# BÁO CÁO CHIA DỮ LIỆU

## 1. Mục đích

Bộ dữ liệu Concrete Compressive Strength được chia
thành ba tập Train, Validation và Test.

Tập Train được sử dụng để huấn luyện mô hình.

Tập Validation được sử dụng để so sánh mô hình và
lựa chọn các tham số trong quá trình phát triển.

Tập Test được giữ độc lập và chỉ được sử dụng
để đánh giá mô hình cuối cùng.

## 2. Tỷ lệ chia dữ liệu
Bộ dữ liệu ban đầu gồm 1030 mẫu.

Sau khi chia:

- Train: 721 mẫu, chiếm khoảng 70.00%
- Validation: 156 mẫu, chiếm khoảng 15.15%
- Test: 153 mẫu, chiếm khoảng 14.85%

Tổng số mẫu sau khi chia vẫn là 1030 mẫu,
do đó không có mẫu nào bị mất trong quá trình chia.

Do dữ liệu được chia theo group để hạn chế rò rỉ dữ liệu,
số lượng thực tế có chênh lệch nhỏ so với tỷ lệ mục tiêu
70% - 15% - 15%.
Tỷ lệ mục tiêu:

- Train: khoảng 70%
- Validation: khoảng 15%
- Test: khoảng 15%

Do dữ liệu được chia theo nhóm nên số mẫu thực tế
có thể chênh lệch nhỏ so với tỷ lệ trên.

## 3. Khả năng tái lập

Nhóm sử dụng:

random_state = 42

Việc cố định random_state giúp quá trình chia dữ liệu
có thể được tái lập trong những lần chạy sau.

## 4. Xử lý các mẫu trùng lặp

Quá trình kiểm tra ban đầu phát hiện 25 lần xuất hiện
trùng lặp trong bộ dữ liệu.

Nhóm không xóa các mẫu này một cách tùy tiện.

Thay vào đó, nhóm tạo nhóm dựa trên 8 biến đầu vào:

- cement
- slag
- fly_ash
- water
- superplasticizer
- coarse_aggregate
- fine_aggregate
- age

Các mẫu có cùng giá trị của 8 biến đầu vào được giữ
trong cùng một tập.

Cách làm này giúp hạn chế việc cùng một mẫu xuất hiện
đồng thời trong tập huấn luyện và tập kiểm thử.

## 5. Kiểm tra rò rỉ dữ liệu

Sau khi chia dữ liệu, nhóm kiểm tra sự giao nhau giữa
các group của Train, Validation và Test.

Kết quả:

- Train - Validation overlap: 0
- Train - Test overlap: 0
- Validation - Test overlap: 0

Không phát hiện group có cùng bộ giá trị đầu vào
xuất hiện đồng thời trong nhiều tập dữ liệu.