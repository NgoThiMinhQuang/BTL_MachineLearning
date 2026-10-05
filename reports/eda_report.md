# BÁO CÁO KHÁM PHÁ DỮ LIỆU - EDA

## 1. Phạm vi phân tích

EDA chỉ được thực hiện trên tập Train gồm 721 mẫu.

Tập Validation và Test không được sử dụng để đưa ra
các quyết định trong quá trình khám phá dữ liệu.

Điều này giúp giữ tập Test độc lập cho quá trình
đánh giá mô hình cuối cùng.

## 2. Phân bố cường độ chịu nén

Biến `strength` biểu diễn cường độ chịu nén của bê tông,
đơn vị MPa.

Quan sát biểu đồ `strength_distribution.png` cho thấy
phần lớn các mẫu tập trung ở vùng cường độ trung bình.

Số lượng mẫu có cường độ rất cao ít hơn.

Phân bố không hoàn toàn đối xứng và có xu hướng kéo dài
về phía các giá trị cường độ cao.

## 3. Quan hệ giữa age và strength

Quan sát biểu đồ `age_vs_strength.png` cho thấy cường độ
chịu nén nhìn chung có xu hướng tăng khi tuổi bê tông tăng.

Tuy nhiên, quan hệ giữa `age` và `strength` không hoàn toàn
tuyến tính.

Ở các giai đoạn tuổi nhỏ, cường độ có xu hướng thay đổi
mạnh hơn, trong khi ở tuổi lớn mức tăng không còn giống
giai đoạn đầu.

Điều này cho thấy mô hình hồi quy tuyến tính có thể chưa
mô tả hoàn toàn ảnh hưởng của tuổi bê tông.

Sau khi huấn luyện mô hình, nhóm sẽ tiếp tục kiểm tra điều
này thông qua phân tích residual.

## 4. Quan hệ giữa cement và strength

Quan sát biểu đồ `cement_vs_strength.png` cho thấy `cement`
có xu hướng đồng biến với `strength`.

Các mẫu có hàm lượng xi măng cao thường có khả năng xuất
hiện ở vùng cường độ cao hơn.

Tuy nhiên, tại cùng một mức xi măng vẫn tồn tại nhiều giá
trị cường độ khác nhau.

Điều này cho thấy cường độ bê tông còn phụ thuộc vào tuổi
và các thành phần cấp phối khác.

## 5. Quan hệ giữa water và strength

Quan sát biểu đồ `water_vs_strength.png` cho thấy `water`
có xu hướng nghịch biến với `strength`.

Các mẫu có lượng nước lớn thường xuất hiện nhiều hơn ở
vùng cường độ thấp và trung bình.

Tuy nhiên, dữ liệu vẫn có độ phân tán lớn nên không thể
kết luận cường độ chỉ phụ thuộc vào lượng nước.

## 6. Ma trận tương quan

Ma trận tương quan được sử dụng để khảo sát mức độ liên hệ
tuyến tính giữa các biến đầu vào và biến `strength`.

Giá trị correlation chỉ thể hiện mức độ liên hệ thống kê,
không chứng minh quan hệ nhân quả.

Ma trận tương quan được tính chỉ trên tập Train.

Một số hệ số tương quan đáng chú ý với biến `strength`:

- cement: khoảng 0.507
- age: khoảng 0.333
- superplasticizer: khoảng 0.329
- water: khoảng -0.303

Trong đó, `cement` có tương quan tuyến tính dương lớn nhất
với `strength` trong tập Train.

`water` có tương quan tuyến tính âm với `strength`.

Các biến còn lại có mức tương quan tuyến tính riêng lẻ thấp hơn.

Tuy nhiên, hệ số tương quan chỉ thể hiện mức độ liên hệ
tuyến tính và không chứng minh quan hệ nhân quả.

Ma trận tương quan được lưu tại:

`reports/figures/correlation_matrix.png`

## 7. Kiểm tra ngoại lệ

Nhóm sử dụng quy tắc IQR trên tập Train để hỗ trợ
nhận diện các quan sát nằm xa phần lớn dữ liệu.

Kết quả:

- cement: 0
- slag: 0
- fly_ash: 0
- water: 6
- superplasticizer: 7
- coarse_aggregate: 0
- fine_aggregate: 4
- age: 41
- strength: 2

Các điểm được quy tắc IQR đánh dấu không được tự động
coi là dữ liệu sai.

Đặc biệt, biến `age` có 41 quan sát nằm ngoài ngưỡng IQR,
nhưng những tuổi bê tông lớn vẫn có thể là dữ liệu thực tế
hợp lệ.

Vì vậy, nhóm giữ lại các quan sát này và sẽ tiếp tục xem xét
chúng trong bước phân tích residual sau khi xây dựng mô hình.

Kết quả chi tiết được lưu tại:

`reports/tables/iqr_outlier_summary.csv`

## 8. Kết luận EDA

EDA cho thấy các biến đầu vào có đơn vị và thang đo khác nhau.

Do SGDRegressor sử dụng Gradient Descent, nhóm sẽ sử dụng
StandardScaler trong Pipeline của mô hình SGD.

Một số quan hệ, đặc biệt là quan hệ giữa `age` và `strength`,
có dấu hiệu không hoàn toàn tuyến tính.

Vì vậy, sau khi xây dựng Linear Regression, nhóm sẽ tiếp tục
phân tích residual để đánh giá những cấu trúc mà mô hình tuyến
tính chưa mô tả tốt.