# BÁO CÁO THÍ NGHIỆM MÔ HÌNH

## 1. Mục tiêu

Nhóm so sánh ba phương pháp:

1. Mean Baseline
2. Linear Regression
3. SGDRegressor

Các mô hình sử dụng cùng Train/Validation split và cùng
các metric MAE, RMSE và R².

Tập Test không được sử dụng trong quá trình lựa chọn mô hình.

## 2. Mean Baseline

Mean Baseline dự đoán tất cả các mẫu bằng trung bình
strength của tập Train.

Trung bình strength của Train:

`36.5966 MPa`

Kết quả Validation:

- MAE: 14.4212 MPa
- RMSE: 17.6209 MPa
- R²: -0.0086

Baseline được sử dụng làm mốc để đánh giá liệu mô hình học
máy có thực sự học được thông tin từ các feature hay không.

## 3. Linear Regression

Linear Regression sử dụng 8 feature.

StandardScaler được fit chỉ trên Train và được đặt trong
Pipeline cùng LinearRegression.

Kết quả Validation:

- MAE: 7.7045 MPa
- RMSE: 9.7288 MPa
- R²: 0.6925

Linear Regression cải thiện đáng kể so với Mean Baseline.

## 4. SGDRegressor

SGDRegressor được thử nghiệm với ba learning rate:

- 0.0001
- 0.001
- 0.01

Kết quả:

| Learning rate | MAE | RMSE | R² |
|---:|---:|---:|---:|
| 0.0001 | 7.8990 | 9.8945 | 0.6820 |
| 0.001 | 7.7284 | 9.7647 | 0.6903 |
| 0.01 | 7.7982 | 9.9540 | 0.6781 |

Learning rate 0.001 cho RMSE Validation nhỏ nhất trong ba
giá trị được thử nghiệm.

Biểu đồ loss theo epoch được lưu tại:

`reports/figures/sgd_learning_rate_loss.png`

## 5. So sánh mô hình

| Mô hình | MAE | RMSE | R² |
|---|---:|---:|---:|
| Mean Baseline | 14.4212 | 17.6209 | -0.0086 |
| Linear Regression | 7.7045 | 9.7288 | 0.6925 |
| SGDRegressor | 7.7284 | 9.7647 | 0.6903 |

Linear Regression có RMSE Validation nhỏ nhất nên được
lựa chọn làm mô hình cuối cùng.

## 6. Hệ số sau chuẩn hóa

Các hệ số được lưu tại:

`reports/tables/linear_coefficients.csv`

Do các feature đã được StandardScaler chuẩn hóa, độ lớn
của các hệ số có thể được so sánh dễ hơn.

Tuy nhiên, các hệ số chỉ mô tả mối liên hệ trong mô hình
và không được diễn giải như quan hệ nhân quả.

## 7. Mô hình cuối cùng

Mô hình cuối:

`Linear Regression`

Tiêu chí lựa chọn:

`Validation RMSE`

Cấu hình được lưu tại:

`config/final_model.json`