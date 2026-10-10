# BÁO CÁO THÍ NGHIỆM MÔ HÌNH

## 1. Mục tiêu

Nhóm so sánh ba phương pháp:

1. Mean Baseline
2. Linear Regression
3. SGDRegressor

Các mô hình sử dụng cùng Train/Validation split và cùng
các metric MAE, RMSE và R².

Tập Test không được sử dụng trong quá trình lựa chọn mô hình.

## 1.1. Cơ sở lý thuyết và phương pháp

### 1.1.1. Bài toán hồi quy tuyến tính

Bài toán sử dụng 8 biến đầu vào gồm cement, slag, fly_ash,
water, superplasticizer, coarse_aggregate, fine_aggregate
và age để dự đoán cường độ nén bê tông (strength), đơn vị MPa.

Mô hình hồi quy tuyến tính đa biến có dạng:

$$
\hat{y} = b_0 + \sum_{j=1}^{8} b_j z_j
$$

Trong đó:

- $\hat{y}$: cường độ nén bê tông dự đoán (MPa).
- $b_0$: hệ số chặn (intercept).
- $b_j$: hệ số hồi quy của biến thứ j.
- $z_j$: giá trị đặc trưng thứ j sau chuẩn hóa.

Mô hình tìm các hệ số sao cho tổng bình phương sai số
giữa giá trị dự đoán và giá trị thực tế là nhỏ nhất.

### 1.1.2. Chuẩn hóa dữ liệu bằng StandardScaler

Các biến đầu vào có đơn vị và khoảng giá trị khác nhau.
Vì vậy, nhóm sử dụng StandardScaler để chuẩn hóa các
đặc trưng trước khi huấn luyện.

Công thức chuẩn hóa:

$$
z_j = \frac{x_j-\mu_j}{\sigma_j}
$$

Trong đó:

- $x_j$: giá trị ban đầu của đặc trưng.
- $\mu_j$: giá trị trung bình của đặc trưng trên tập Train.
- $\sigma_j$: độ lệch chuẩn của đặc trưng trên tập Train.
- $z_j$: giá trị sau chuẩn hóa.

StandardScaler chỉ được fit trên tập Train.

Validation và Test sử dụng các tham số chuẩn hóa
đã học từ Train thông qua transform.

Điều này giúp tránh rò rỉ thông tin từ Validation và Test.

### 1.1.3. Hàm mất mát Mean Squared Error

Mô hình được xây dựng theo nguyên tắc tối thiểu hóa
sai số bình phương.

Công thức MSE:

$$
MSE = \frac{1}{n}\sum_{i=1}^{n}(y_i-\hat{y}_i)^2
$$

Trong đó:

- $n$: số lượng mẫu.
- $y_i$: cường độ nén thực tế.
- $\hat{y}_i$: cường độ nén dự đoán.

MSE phạt các sai số lớn mạnh hơn do có phép bình phương.

### 1.1.4. Linear Regression

Nhóm sử dụng LinearRegression của scikit-learn để
tìm nghiệm bình phương tối thiểu (Ordinary Least Squares).

Mô hình được huấn luyện bằng dữ liệu Train và đánh giá
trên tập Validation.

Phương pháp này không sử dụng vòng lặp Gradient Descent
để cập nhật hệ số như SGDRegressor.

### 1.1.5. Stochastic Gradient Descent

SGD là phương pháp tối ưu cập nhật các tham số dựa
trên gradient của hàm mất mát ở từng mẫu huấn luyện.

Quy tắc cập nhật tổng quát:

$$
\theta_{t+1} = \theta_t-\eta\nabla L_i(\theta_t)
$$

Trong đó:

- $\theta_t$: các tham số mô hình ở bước t.
- $\eta$: learning rate, điều khiển độ lớn bước cập nhật.
- $\nabla L_i$: gradient của hàm mất mát ở mẫu i.

Với hàm mất mát của một mẫu:

$$
L_i = \frac{1}{2}(y_i-\hat{y}_i)^2
$$

Gradient theo hệ số của đặc trưng đã chuẩn hóa:

$$
\frac{\partial L_i}{\partial b_j}
= (\hat{y}_i-y_i)z_{ij}
$$

Trong thí nghiệm, nhóm sử dụng SGDRegressor với:

- loss = squared_error
- penalty = None
- learning_rate = constant
- 3 learning rate: 0.0001, 0.001 và 0.01
- 200 epoch
- random_state = 42

Nhóm gọi partial_fit để tiếp tục cập nhật mô hình
qua từng epoch, đồng thời xáo trộn thứ tự mẫu
bằng bộ sinh số ngẫu nhiên cố định.

Sau mỗi epoch, nhóm tính Training MSE để
theo dõi quá trình hội tụ.

Learning rate được lựa chọn dựa trên RMSE của Validation,
không sử dụng tập Test để điều chỉnh.

### 1.1.6. Các chỉ số đánh giá mô hình

Mean Absolute Error (MAE):

$$
MAE = \frac{1}{n}\sum_{i=1}^{n}|y_i-\hat{y}_i|
$$

Root Mean Squared Error (RMSE):

$$
RMSE = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i-\hat{y}_i)^2}
$$

Hệ số xác định R²:

$$
R^2 = 1-\frac{\sum_{i=1}^{n}(y_i-\hat{y}_i)^2}
{\sum_{i=1}^{n}(y_i-\bar{y})^2}
$$

Trong đó $\bar{y}$ là trung bình giá trị thực tế
của tập đang được đánh giá.

MAE và RMSE càng thấp càng tốt. RMSE nhạy hơn
với các trường hợp có sai số lớn.

R² thể hiện khả năng giải thích biến thiên của target
so với mô hình dự đoán bằng trung bình trên tập đánh giá.
R² có thể âm và không phải phần trăm độ chính xác.

### 1.1.7. Giả định và giới hạn của hồi quy tuyến tính

Hồi quy tuyến tính giả định kỳ vọng có điều kiện của
biến mục tiêu có quan hệ tuyến tính với các đặc trưng
theo biểu diễn được sử dụng.

Các vấn đề cần xem xét gồm:

- Quan hệ phi tuyến chưa được biểu diễn.
- Sai số có thể có phương sai thay đổi.
- Các đặc trưng có thể tương quan mạnh với nhau.
- Các quan sát có thể không hoàn toàn độc lập.
- Các mẫu cực trị có thể ảnh hưởng tới hệ số.

Chuẩn hóa đặc trưng giúp so sánh hệ số và hỗ trợ
quá trình tối ưu bằng SGD, nhưng không tự loại bỏ
quan hệ phi tuyến hoặc đa cộng tuyến.

Nhóm sử dụng biểu đồ residual để nhận diện những
cấu trúc sai số mà mô hình chưa mô tả được.

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


## 6. Phân tích và diễn giải hệ số hồi quy

### 6.1. Hệ số của mô hình Linear Regression

Sau khi huấn luyện Pipeline gồm StandardScaler và
LinearRegression, nhóm trích xuất các hệ số từ mô hình.

Kết quả được lưu trong:

`reports/tables/linear_coefficients.csv`

| Biến | Hệ số sau chuẩn hóa |
|---|---:|
| cement | +12.2612 |
| slag | +8.2998 |
| age | +7.3756 |
| fly_ash | +5.5152 |
| water | -4.2282 |
| fine_aggregate | +1.0070 |
| coarse_aggregate | +0.9837 |
| superplasticizer | +0.9619 |

### 6.2. Ý nghĩa các hệ số

Vì các đặc trưng đầu vào đã được chuẩn hóa bằng
StandardScaler, mỗi hệ số biểu diễn mức thay đổi
dự đoán khi biến tương ứng tăng một độ lệch chuẩn
của tập Train, trong điều kiện các biến khác không đổi.

- cement: Hệ số +12.2612 cho thấy khi lượng xi măng
  tăng một độ lệch chuẩn, mô hình dự đoán cường độ
  tăng khoảng 12.26 MPa nếu giữ nguyên các biến khác.

- slag: Hệ số +8.2998 thể hiện mối liên hệ dương
  giữa lượng xỉ lò cao và cường độ dự đoán.

- age: Hệ số +7.3756 cho thấy tuổi bê tông có
  mối liên hệ dương với cường độ dự đoán trong mô hình.

- fly_ash: Hệ số +5.5152 thể hiện mối liên hệ dương
  có điều kiện trong mô hình hồi quy.

- water: Hệ số -4.2282 thể hiện mối liên hệ âm.
  Khi lượng nước tăng một độ lệch chuẩn, dự đoán
  giảm khoảng 4.23 MPa nếu các biến khác giữ nguyên.

- fine_aggregate, coarse_aggregate và
  superplasticizer có hệ số dương với độ lớn
  tương đối nhỏ hơn trong mô hình hiện tại.

### 6.3. Nhận xét và giới hạn

Trong các hệ số chuẩn hóa, cement có độ lớn
tuyệt đối lớn nhất, tiếp theo là slag và age.

Tuy nhiên, không nên kết luận cement là yếu tố
có ảnh hưởng nhân quả lớn nhất đến cường độ bê tông.

Các biến cấp phối có thể tương quan với nhau.
Đa cộng tuyến có thể khiến hệ số hồi quy thay đổi
đáng kể khi dữ liệu hoặc tập đặc trưng thay đổi.

Các hệ số cũng chỉ phản ánh quan hệ tuyến tính
có điều kiện trong mô hình đã huấn luyện.

Đặc biệt, mặc dù age có hệ số dương, kết quả
phân tích residual cho thấy ảnh hưởng của tuổi
bê tông không hoàn toàn tuyến tính.

Do đó, việc giải thích các hệ số cần kết hợp
với EDA, phân tích residual và hiểu biết về
giới hạn của dữ liệu.
