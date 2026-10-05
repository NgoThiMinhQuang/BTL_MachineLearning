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

`ĐIỀN`

RMSE:

`ĐIỀN`

R²:

`ĐIỀN`

## 9. Test

MAE:

`ĐIỀN`

RMSE:

`ĐIỀN`

R²:

`ĐIỀN`

## 10. Giới hạn

Mô hình có thể cho kết quả kém tin cậy hơn đối với các cấp phối
hoặc tuổi bê tông nằm ngoài miền dữ liệu huấn luyện.

Các hệ số hoặc tương quan không chứng minh quan hệ nhân quả.

## 11. Cảnh báo sử dụng

Mô hình được xây dựng cho mục đích học tập và hỗ trợ khảo sát.

Kết quả dự đoán không thay thế thí nghiệm cường độ nén
theo tiêu chuẩn hoặc phê duyệt kỹ thuật kết cấu.