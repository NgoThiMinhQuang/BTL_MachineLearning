# MODEL CARD

## 1. Tên mô hình

Concrete Compressive Strength Regression

## 2. Mục đích

Ước lượng cường độ chịu nén của bê tông dựa trên
thành phần cấp phối và tuổi bê tông.

## 3. Đầu vào

- cement
- slag
- fly_ash
- water
- superplasticizer
- coarse_aggregate
- fine_aggregate
- age

## 4. Đầu ra

strength

Đơn vị: MPa

## 5. Dữ liệu

Concrete Compressive Strength Dataset - UCI.

Tổng số mẫu:

1030

## 6. Chia dữ liệu

Train: 721

Validation: 156

Test: 153

Các dòng có cùng bộ 8 feature được giữ trong cùng một group
để hạn chế leakage.

## 7. Mô hình cuối cùng

Linear Regression

Mô hình được lựa chọn bằng Validation RMSE.

## 8. Validation

MAE:

`7.7045 MPa`

RMSE:

`9.7288 MPa`

R²:

`0.6925`

## 9. Test

MAE:

`7.4896 MPa`

RMSE:

`9.3517 MPa`

R²:

`0.5696`

## 10. Phương pháp lựa chọn mô hình

Ba phương pháp được so sánh trên cùng tập Validation:

| Mô hình | MAE | RMSE | R² |
|---|---:|---:|---:|
| Mean Baseline | 14.4212 | 17.6209 | -0.0086 |
| Linear Regression | 7.7045 | 9.7288 | 0.6925 |
| SGDRegressor | 7.7284 | 9.7647 | 0.6903 |

SGDRegressor tốt nhất sử dụng learning rate = 0.001.

Linear Regression được chọn làm mô hình cuối vì có RMSE
trên Validation thấp nhất.

Tập Test không được sử dụng trong quá trình lựa chọn mô hình.
## 11. Giới hạn

Mô hình có thể cho kết quả kém tin cậy hơn đối với các cấp phối
hoặc tuổi bê tông nằm ngoài miền dữ liệu huấn luyện.

Các hệ số hoặc tương quan không chứng minh quan hệ nhân quả.

## 12. Cảnh báo sử dụng

Mô hình được xây dựng cho mục đích học tập và hỗ trợ khảo sát.

Kết quả dự đoán không thay thế thí nghiệm cường độ nén
theo tiêu chuẩn hoặc phê duyệt kỹ thuật kết cấu.