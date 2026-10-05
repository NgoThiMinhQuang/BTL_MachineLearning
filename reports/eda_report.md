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

Phần này sẽ được bổ sung sau khi tạo
`correlation_matrix.png`.

## 7. Kiểm tra ngoại lệ

Nhóm sử dụng quy tắc IQR để hỗ trợ nhận diện các giá trị
nằm xa phần lớn dữ liệu.

Các điểm được phát hiện bởi IQR không tự động bị loại bỏ.

Do đây là dữ liệu thí nghiệm bê tông, một giá trị khác biệt
có thể vẫn là một cấp phối hợp lệ.

Chỉ loại dữ liệu khi có bằng chứng cho thấy đó là lỗi dữ liệu.

## 8. Kết luận EDA

EDA cho thấy các biến đầu vào có đơn vị và thang đo khác nhau.

Do SGDRegressor sử dụng Gradient Descent, nhóm sẽ sử dụng
StandardScaler trong Pipeline của mô hình SGD.

Một số quan hệ, đặc biệt là quan hệ giữa `age` và `strength`,
có dấu hiệu không hoàn toàn tuyến tính.

Vì vậy, sau khi xây dựng Linear Regression, nhóm sẽ tiếp tục
phân tích residual để đánh giá những cấu trúc mà mô hình tuyến
tính chưa mô tả tốt.