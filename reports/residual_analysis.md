# PHÂN TÍCH RESIDUAL VÀ SAI SỐ MÔ HÌNH

## 1. Mục tiêu

Phần này phân tích sai số của mô hình cuối cùng trên tập Test.

Mô hình đã được lựa chọn trước đó dựa trên tập Validation.
Tập Test chỉ được sử dụng cho đánh giá cuối cùng.

## 2. Định nghĩa Residual

Residual được tính theo công thức:

`residual = actual strength - predicted strength`

Residual dương nghĩa là mô hình dự đoán thấp hơn thực tế.

Residual âm nghĩa là mô hình dự đoán cao hơn thực tế.

Residual càng gần 0 thì dự đoán càng gần giá trị thực tế.

## 3. Kết quả trên tập Test

Mô hình cuối cùng:

`Linear Regression`

MAE:

`ĐIỀN KẾT QUẢ`

RMSE:

`ĐIỀN KẾT QUẢ`

R²:

`ĐIỀN KẾT QUẢ`

Kết quả chi tiết:

`reports/tables/final_test_metrics.csv`

## 4. Residual theo tuổi bê tông

Biểu đồ:

`reports/figures/residual_vs_age.png`

Nhận xét:

`CHƯA ĐIỀN - XEM BIỂU ĐỒ THỰC TẾ TRƯỚC`

## 5. Residual theo cường độ thực tế

Biểu đồ:

`reports/figures/residual_vs_actual_strength.png`

Nhận xét:

`CHƯA ĐIỀN - XEM BIỂU ĐỒ THỰC TẾ TRƯỚC`

## 6. Mười residual lớn nhất

Mười mẫu có absolute residual lớn nhất được lưu tại:

`reports/tables/top_10_residuals.csv`

Nhóm kiểm tra các mẫu này dựa trên:

- cường độ thực tế
- cường độ dự đoán
- residual
- tuổi bê tông
- thành phần cấp phối
- miền dữ liệu Train

## 7. Miền dữ liệu Train

Khoảng min-max của các feature trong tập Train được lưu tại:

`reports/tables/train_domain_ranges.csv`

Các giá trị nằm ngoài miền Train cần được xem xét thận trọng
vì mô hình chưa được huấn luyện đầy đủ trên vùng dữ liệu đó.

## 8. Giới hạn

Mô hình được xây dựng cho mục đích học thuật và khảo sát.

Kết quả dự đoán không thay thế thí nghiệm cường độ nén
theo tiêu chuẩn hoặc quyết định kỹ thuật kết cấu.