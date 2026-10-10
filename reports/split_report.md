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

Quá trình kiểm tra bằng `df.duplicated().sum()` cho thấy
25 bản ghi được đánh dấu là trùng lặp so với các bản ghi
xuất hiện trước đó.

Khi sử dụng `duplicated(keep=False)`, có tổng cộng
36 dòng thuộc 11 nhóm trùng lặp hoàn toàn.

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

Cách chia theo group bảo đảm các dòng có cùng bộ giá trị
của 8 biến đầu vào được giữ trong cùng một tập, thay vì
bị phân tán giữa Train, Validation và Test.

## 5. Kiểm tra rò rỉ dữ liệu

Sau khi chia dữ liệu, nhóm kiểm tra sự giao nhau giữa
các group của Train, Validation và Test.

Kết quả:

- Train - Validation overlap: 0
- Train - Test overlap: 0
- Validation - Test overlap: 0

Không phát hiện group có cùng bộ giá trị đầu vào
xuất hiện đồng thời trong nhiều tập dữ liệu.

## 6. Phân tích bổ sung về cách tạo nhóm dữ liệu

### 6.1. Cách chia dữ liệu ban đầu

Trong quá trình xây dựng mô hình, nhóm sử dụng
GroupShuffleSplit với random_state = 42.

Group được tạo dựa trên 8 biến đầu vào:

- cement
- slag
- fly_ash
- water
- superplasticizer
- coarse_aggregate
- fine_aggregate
- age

Cách chia này bảo đảm những mẫu có cùng toàn bộ
8 giá trị đầu vào không xuất hiện đồng thời
trong Train, Validation và Test.

Tuy nhiên, những mẫu có cùng 7 thành phần vật liệu
nhưng khác tuổi bê tông vẫn có thể nằm ở các tập khác nhau.

### 6.2. Kiểm tra trùng cấp phối vật liệu

Nhóm thực hiện kiểm tra bổ sung bằng script:

`src/check_group_overlap.py`

Kết quả kiểm tra:

| Cặp dữ liệu | Trùng nhóm 8 biến | Trùng cấp phối 7 thành phần |
|---|---:|---:|
| Train - Validation | 0 | 83 |
| Train - Test | 0 | 89 |
| Validation - Test | 0 | 42 |

Kết quả cho thấy không có nhóm trùng đủ 8 biến
giữa các tập.

Tuy nhiên, vẫn tồn tại cấp phối vật liệu giống nhau
được quan sát ở những tuổi bê tông khác nhau.

Điều này không tự động chứng minh có target leakage,
nhưng là một giới hạn cần lưu ý khi diễn giải
khả năng tổng quát hóa của mô hình.

### 6.3. Phạm vi đánh giá của tập Test

Kết quả Test ban đầu được sử dụng để đánh giá
mô hình trên những mẫu có bộ 8 đặc trưng đầu vào
không trùng hoàn toàn với tập Train.

Tuy nhiên, kết quả này không đại diện cho một
phép đánh giá độc lập hoàn toàn theo cấp phối vật liệu.

Vì vậy, nhóm không khẳng định kết quả Test ban đầu
phản ánh đầy đủ khả năng dự đoán cấp phối
hoàn toàn mới.

### 6.4. Đánh giá bổ sung theo 7 thành phần

Để khảo sát khả năng tổng quát hóa đối với
các cấp phối mới, nhóm bổ sung thí nghiệm
Group Cross-Validation trên tập Train ban đầu.

Group được xây dựng từ 7 thành phần vật liệu,
không bao gồm age.

Age vẫn được sử dụng làm đặc trưng đầu vào
của mô hình hồi quy.

Nhóm sử dụng 5-fold GroupKFold với ba seed:
11, 42 và 2026.

Tổng cộng thực hiện 15 lượt đánh giá.

Trong mỗi lượt, các cấp phối thuộc phần validation
không xuất hiện trong phần train của cùng fold.

Kết quả trung bình:

- MAE: 8.6075 MPa
- RMSE: 10.8337 MPa
- R²: 0.5809

Kết quả chi tiết được lưu tại:

`reports/tables/linear_stability_group7_cv.csv`

Thí nghiệm này chỉ sử dụng tập Train gốc,
không sử dụng tập Test gốc.

Các kết quả được dùng để phân tích độ ổn định
và giới hạn tổng quát hóa, không dùng để điều chỉnh
mô hình cuối đã lựa chọn.

### 6.5. Kết luận

Cách chia theo 8 đặc trưng ban đầu giúp tránh
những mẫu có đầu vào hoàn toàn giống nhau
xuất hiện ở nhiều tập dữ liệu.

Đánh giá bổ sung theo 7 thành phần cung cấp
thêm thông tin về khả năng dự đoán đối với
cấp phối chưa xuất hiện trong phần huấn luyện.

Nhóm trình bày riêng hai phương pháp đánh giá
vì chúng đo lường những điều kiện tổng quát hóa
khác nhau.

Đây là một giới hạn của thiết kế đánh giá
được ghi nhận và công bố minh bạch trong báo cáo.
