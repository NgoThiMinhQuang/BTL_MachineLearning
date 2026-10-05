# PHÂN TÍCH RESIDUAL VÀ SAI SỐ MÔ HÌNH

## 1. Mục tiêu

Phần này phân tích sai số của mô hình Linear Regression
trên tập Test.

Mô hình đã được lựa chọn trước đó dựa trên RMSE của tập
Validation.

Tập Test chỉ được sử dụng cho đánh giá cuối cùng và không
được sử dụng để lựa chọn mô hình hoặc tham số.

## 2. Định nghĩa Residual

Residual được tính theo công thức:

`residual = actual strength - predicted strength`

Residual dương nghĩa là mô hình dự đoán thấp hơn giá trị
thực tế.

Residual âm nghĩa là mô hình dự đoán cao hơn giá trị
thực tế.

Residual càng gần 0 thì dự đoán càng gần giá trị thực tế.

## 3. Kết quả trên tập Test

Mô hình cuối cùng:

`Linear Regression`

Kết quả:

- MAE: 7.4896 MPa
- RMSE: 9.3517 MPa
- R²: 0.5696

MAE cho thấy dự đoán của mô hình lệch so với giá trị thực
tế trung bình khoảng 7.49 MPa.

RMSE cao hơn MAE, cho thấy vẫn tồn tại một số mẫu có sai số
tương đối lớn.

R² bằng khoảng 0.57 cho thấy mô hình tuyến tính giải thích
được khoảng 57% biến thiên của strength trên tập Test.

R² không được hiểu là độ chính xác 57%.

Kết quả chi tiết được lưu tại:

`reports/tables/final_test_metrics.csv`

## 4. Residual theo tuổi bê tông

Biểu đồ:

`reports/figures/residual_vs_age.png`

Residual không phân bố hoàn toàn ngẫu nhiên theo tuổi bê tông.

Ở nhóm tuổi rất nhỏ từ 1 đến 7 ngày, residual trung bình
khoảng -9.94 MPa, cho thấy mô hình có xu hướng dự đoán
cao hơn giá trị thực tế.

Ở nhóm 29 đến 90 ngày, residual trung bình khoảng
+6.00 MPa, cho thấy mô hình có xu hướng dự đoán thấp hơn
thực tế.

Ở các mẫu 365 ngày, residual trung bình khoảng -20.07 MPa,
cho thấy mô hình có thể dự đoán quá cao ở một số mẫu tuổi lớn.

Sự thay đổi có hệ thống của residual theo tuổi là bằng chứng
cho thấy quan hệ giữa `age` và `strength` không hoàn toàn
tuyến tính.

Linear Regression vì vậy chưa mô tả đầy đủ ảnh hưởng phi
tuyến của tuổi bê tông.

## 5. Residual theo cường độ thực tế

Biểu đồ:

`reports/figures/residual_vs_actual_strength.png`

Residual cũng thể hiện xu hướng theo cường độ thực tế.

Với các mẫu có strength dưới 20 MPa, residual trung bình
khoảng -8.79 MPa. Điều này cho thấy mô hình có xu hướng
dự đoán cao hơn thực tế ở vùng cường độ thấp.

Với strength từ 40 đến 60 MPa, residual trung bình khoảng
+5.60 MPa.

Với các mẫu strength từ 60 MPa trở lên, residual trung bình
khoảng +12.47 MPa.

Điều này cho thấy mô hình có xu hướng dự đoán thấp hơn thực
tế đối với một số mẫu cường độ cao.

Kết quả gợi ý mô hình tuyến tính có xu hướng kéo các dự đoán
về vùng trung bình và chưa mô tả đầy đủ các trường hợp ở hai
đầu của phân bố cường độ.

## 6. Mười residual lớn nhất

Mười mẫu có absolute residual lớn nhất được lưu tại:

`reports/tables/top_10_residuals.csv`

Sai số tuyệt đối lớn nhất khoảng 29.11 MPa.

Mẫu này có:

- age = 365 ngày
- strength thực tế ≈ 25.08 MPa
- strength dự đoán ≈ 54.19 MPa
- residual ≈ -29.11 MPa

Mẫu có sai số lớn thứ hai cũng có age = 365 ngày:

- strength thực tế ≈ 36.15 MPa
- strength dự đoán ≈ 61.41 MPa
- residual ≈ -25.26 MPa

Hai trường hợp này củng cố nhận xét rằng quan hệ giữa tuổi
và strength không hoàn toàn tuyến tính.

Trong 10 mẫu có residual lớn nhất, chỉ có một mẫu bị phát hiện
nằm ngoài miền min-max của Train theo kiểm tra đơn giản.

Mẫu đó có age = 1 ngày, trong khi age nhỏ nhất của Train là
3 ngày.

Chín mẫu còn lại vẫn nằm trong khoảng min-max của từng feature.

Do đó, sai số lớn không chỉ xuất hiện do đầu vào nằm ngoài
miền dữ liệu, mà còn có thể do giới hạn của mô hình tuyến tính
trong việc mô tả quan hệ phức tạp giữa các biến.

## 7. Miền dữ liệu Train

Khoảng min-max của các feature trong Train được lưu tại:

`reports/tables/train_domain_ranges.csv`

Miền quan sát gồm:

- cement: 102.0 – 540.0 kg/m3
- slag: 0.0 – 359.4 kg/m3
- fly_ash: 0.0 – 200.1 kg/m3
- water: 121.75 – 247.0 kg/m3
- superplasticizer: 0.0 – 32.2 kg/m3
- coarse_aggregate: 801.0 – 1145.0 kg/m3
- fine_aggregate: 594.0 – 992.6 kg/m3
- age: 3 – 365 ngày

Việc một mẫu nằm trong khoảng min-max không bảo đảm rằng
mẫu đó thuộc vùng dữ liệu quen thuộc của mô hình.

Kiểm tra min-max chỉ được sử dụng như một cảnh báo đơn giản
cho các trường hợp rõ ràng nằm ngoài miền đã quan sát.

## 8. Giới hạn

Linear Regression là mô hình tuyến tính nên không thể mô tả
đầy đủ các quan hệ phi tuyến giữa thành phần cấp phối,
tuổi bê tông và cường độ nén.

Residual cho thấy đặc biệt biến `age` có cấu trúc phi tuyến
mà mô hình chưa mô tả tốt.

Mô hình được xây dựng cho mục đích học thuật và hỗ trợ khảo sát.

Kết quả dự đoán không thay thế thí nghiệm cường độ nén theo
tiêu chuẩn hoặc quyết định/phê duyệt kỹ thuật kết cấu.