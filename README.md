
# PROJECT 12 - ƯỚC LƯỢNG CƯỜNG ĐỘ NÉN BÊ TÔNG

## 1. Giới thiệu đề tài

Đồ án Machine Learning xây dựng hệ thống ước lượng cường độ
chịu nén của bê tông (Concrete Compressive Strength) dựa trên
thành phần cấp phối và tuổi bảo dưỡng.

Hệ thống sử dụng các phương pháp hồi quy:

- Mean Baseline
- Linear Regression
- SGDRegressor

Các mô hình được đánh giá bằng MAE, RMSE và R².

Mô hình cuối cùng được tích hợp vào ứng dụng web sử dụng
FastAPI, HTML, CSS và JavaScript.

**Đầu ra:** Cường độ nén bê tông, đơn vị MPa.

> Đây là dự án học thuật. Kết quả không thay thế thí nghiệm
> cường độ nén bê tông hoặc phê duyệt kết cấu công trình.


## 2. Mục tiêu

- Phân tích bộ dữ liệu cường độ nén bê tông.
- Kiểm tra chất lượng dữ liệu và dữ liệu trùng lặp.
- Chia dữ liệu thành Train, Validation và Test.
- Hạn chế data leakage khi chia dữ liệu.
- Xây dựng mô hình Mean Baseline.
- Huấn luyện Linear Regression.
- Thử nghiệm SGDRegressor với nhiều learning rate.
- So sánh các mô hình trên tập Validation.
- Lựa chọn mô hình bằng Validation RMSE.
- Đánh giá mô hình cuối trên tập Test.
- Phân tích residual và các trường hợp sai số lớn.
- Xây dựng ứng dụng web dự đoán.
- Kiểm tra dữ liệu đầu vào ngoài miền Train.
- Hiển thị Dashboard đánh giá mô hình.
- Phân tích độ nhạy (Sensitivity Analysis).
- Kiểm thử các chức năng API.


## 3. Nguồn dữ liệu

Bộ dữ liệu:

**Concrete Compressive Strength Dataset**

Nguồn:
UCI Machine Learning Repository

https://archive.ics.uci.edu/dataset/165/concrete+compressive+strength

Tổng số quan sát: **1.030 mẫu**

Số biến đầu vào: **8**

Số biến đầu ra: **1**

Dữ liệu được lưu trong:

`data/raw/Concrete_Data.xls`

Các thông tin về dữ liệu được trình bày thêm tại:

- `data/README.md`
- `data/data_dictionary.csv`


## 4. Các biến đầu vào

| Tên biến | Ý nghĩa | Đơn vị |
|---|---|---|
| cement | Xi măng | kg/m³ |
| slag | Xỉ lò cao | kg/m³ |
| fly_ash | Tro bay | kg/m³ |
| water | Nước | kg/m³ |
| superplasticizer | Phụ gia siêu dẻo | kg/m³ |
| coarse_aggregate | Cốt liệu thô | kg/m³ |
| fine_aggregate | Cốt liệu mịn | kg/m³ |
| age | Tuổi bê tông | ngày |

**Biến mục tiêu:**

`strength` - Cường độ chịu nén của bê tông (MPa).


## 5. Cấu trúc thư mục

```text
BTL_MachineLearning/
|
|-- app/
|   |-- main.py
|   |-- templates/
|       |-- index.html
|       |-- predict.html
|       |-- dashboard.html
|
|-- config/
|   |-- final_model.json
|
|-- data/
|   |-- raw/
|   |-- processed/
|   |   |-- train.csv
|   |   |-- validation.csv
|   |   |-- test.csv
|   |-- data_dictionary.csv
|   |-- README.md
|
|-- models/
|   |-- candidates/
|       |-- linear_regression.joblib
|       |-- sgd_best.joblib
|
|-- reports/
|   |-- figures/
|   |-- tables/
|   |-- data_quality.md
|   |-- eda_report.md
|   |-- split_report.md
|   |-- model_experiments.md
|   |-- residual_analysis.md
|   |-- model_card.md
|
|-- src/
|   |-- data.py
|   |-- prepare_data.py
|   |-- split_data.py
|   |-- eda.py
|   |-- baseline.py
|   |-- train_linear.py
|   |-- experiment_sgd.py
|   |-- compare_models.py
|   |-- evaluate_final.py
|
|-- tests/
|   |-- test_api.py
|
|-- requirements.txt
|-- README.md
```

Bộ kiểm thử tự động được lưu tại `tests/test_api.py`.

Chạy kiểm thử bằng lệnh:

```powershell
python -m pytest tests/test_api.py -v
```


## 6. Cài đặt môi trường

### 6.1. Tải mã nguồn

```powershell
git clone https://github.com/NgoThiMinhQuang/BTL_MachineLearning.git

cd BTL_MachineLearning
```

Nếu đã tải project về máy, chỉ cần mở thư mục project
trong VS Code.

### 6.2. Tạo môi trường ảo Python

Trên Windows:

```powershell
python -m venv .venv
```

Kích hoạt môi trường bằng PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Nếu sử dụng CMD:

```cmd
.venv\Scripts\activate.bat
```

Khi kích hoạt thành công, Terminal thường hiển thị:

```text
(.venv)
```

### 6.3. Cài đặt thư viện

```powershell
python -m pip install -r requirements.txt
```

Các thư viện chính:

- pandas
- numpy
- scikit-learn
- matplotlib
- joblib
- FastAPI
- Uvicorn
- Pydantic

Để chạy bộ kiểm thử, cài thêm:

```powershell
python -m pip install pytest httpx
```

Lưu ý: Nên sử dụng môi trường Python tương thích với
các phiên bản thư viện trong `requirements.txt`.


## 7. Chạy ứng dụng web

### 7.1. Khởi động FastAPI

Mở Terminal ở thư mục gốc của project.

Chạy:

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Nếu thành công, Terminal hiển thị:

```text
Uvicorn running on http://127.0.0.1:8000
```

Giữ Terminal hoạt động trong khi sử dụng website.

### 7.2. Mở website

**Trang chủ:**

http://127.0.0.1:8000/

**Trang dự đoán:**

http://127.0.0.1:8000/predict

**Dashboard đánh giá mô hình:**

http://127.0.0.1:8000/dashboard

**Swagger API Documentation:**

http://127.0.0.1:8000/docs

Với cách chạy này, FastAPI phục vụ cả giao diện và API.

Không cần bật Go Live.


## 8. Chạy giao diện bằng Go Live

Project cũng hỗ trợ mở các trang HTML bằng extension
Live Server của VS Code.

Thực hiện:

1. Khởi động FastAPI ở cổng 8000.
2. Giữ Terminal FastAPI đang chạy.
3. Mở `app/templates/index.html` trong VS Code.
4. Chọn "Open with Live Server" hoặc nhấn Go Live.
5. Sử dụng thanh menu để chuyển trang.

Khi mở bằng Go Live:

- Go Live hiển thị HTML, CSS và JavaScript.
- FastAPI cung cấp API và chạy mô hình Machine Learning.
- JavaScript gửi yêu cầu sang FastAPI ở cổng 8000.
- FastAPI phải bật CORS cho cổng Go Live đang sử dụng.

**Quan trọng:**

Chỉ bật Go Live mà không khởi động FastAPI thì các trang HTML
có thể hiển thị, nhưng chức năng dự đoán và các API khác
sẽ không hoạt động.


## 9. Các màn hình của website

### 9.1. Trang chủ

File:

`app/templates/index.html`

Chức năng:

- Giới thiệu đề tài.
- Trình bày nguồn dữ liệu.
- Hiển thị 8 biến đầu vào.
- Giới thiệu các phương pháp Machine Learning.
- Điều hướng tới trang dự đoán và Dashboard.

### 9.2. Trang dự đoán

File:

`app/templates/predict.html`

Chức năng:

- Nhập 8 thông số cấp phối và tuổi bê tông.
- Hiển thị khoảng min-max của tập Train.
- Kiểm tra dữ liệu đầu vào.
- Gọi API dự đoán.
- Hiển thị cường độ nén dự đoán bằng MPa.
- Thông báo lỗi bằng tiếng Việt.
- Phân tích độ nhạy khi thay đổi một biến.

### 9.3. Dashboard

File:

`app/templates/dashboard.html`

Chức năng:

- Hiển thị MAE, RMSE và R² trên Test.
- So sánh ba phương pháp trên Validation.
- Hiển thị bảng thử nghiệm learning rate.
- Hiển thị Actual vs Predicted.
- Hiển thị Residual vs Age.
- Hiển thị Residual vs Actual Strength.
- Hiển thị SGD Loss theo Learning Rate.
- Hiển thị thông tin Model Card.


## 10. Quy trình Machine Learning

### 10.1. Kiểm tra dữ liệu

Script:

`src/prepare_data.py`

Script sử dụng dữ liệu gốc, chuẩn hóa tên cột
và xuất báo cáo các dòng trùng lặp.

### 10.2. Chia dữ liệu

Script:

`src/split_data.py`

Dữ liệu được chia bằng GroupShuffleSplit với
`random_state = 42`.

Các mẫu có cùng 8 biến đầu vào được đưa vào cùng một group
nhằm hạn chế trùng lặp giữa các tập.

Kết quả hiện tại:

| Tập | Số mẫu |
|---|---:|
| Train | 721 |
| Validation | 156 |
| Test | 153 |
| Tổng | 1030 |

### 10.3. Phân tích EDA

Script:

`src/eda.py`

Các phân tích bao gồm:

- Phân bố cường độ nén.
- Tương quan giữa các biến.
- Quan hệ giữa tuổi và cường độ.
- Quan hệ giữa xi măng và cường độ.
- Quan hệ giữa nước và cường độ.
- Tổng hợp các giá trị ngoại lai theo IQR.

Các hình được lưu tại:

`reports/figures/`

### 10.4. Mean Baseline

Script:

`src/baseline.py`

Mean Baseline dự đoán mọi mẫu Validation
bằng cường độ nén trung bình của tập Train.

Đây là mô hình tham chiếu để đánh giá
lợi ích của các mô hình Machine Learning.

### 10.5. Linear Regression

Script:

`src/train_linear.py`

Pipeline bao gồm:

```text
StandardScaler
      |
      v
LinearRegression
      |
      v
Predicted Strength
```

StandardScaler được fit trên Train.

Dữ liệu Validation chỉ được transform bằng
scaler đã học từ Train.

### 10.6. SGDRegressor

Script:

`src/experiment_sgd.py`

Các learning rate đã thử:

- 0.0001
- 0.001
- 0.01

Số epoch: 200.

Kết quả được đánh giá trên tập Validation.

Biểu đồ Training MSE theo epoch:

`reports/figures/sgd_learning_rate_loss.png`

### 10.7. So sánh mô hình

Script:

`src/compare_models.py`

Mô hình cuối được chọn theo RMSE trên Validation.

Tập Test không được dùng để lựa chọn mô hình
hay điều chỉnh learning rate.


## 11. Kết quả trên tập Validation

| Mô hình | MAE (MPa) | RMSE (MPa) | R² |
|---|---:|---:|---:|
| Linear Regression | 7.7045 | 9.7288 | 0.6925 |
| SGDRegressor | 7.7284 | 9.7647 | 0.6903 |
| Mean Baseline | 14.4212 | 17.6209 | -0.0086 |

SGDRegressor tốt nhất sử dụng learning rate = 0.001.

Linear Regression được chọn làm mô hình cuối cùng
vì đạt RMSE Validation thấp nhất trong ba phương pháp.

Cấu hình mô hình cuối:

`config/final_model.json`

Model đã lưu:

`models/candidates/linear_regression.joblib`


## 12. Kết quả trên tập Test

Sau khi lựa chọn mô hình trên Validation,
Linear Regression được đánh giá trên Test.

| Chỉ số | Kết quả |
|---|---:|
| MAE | 7.4896 MPa |
| RMSE | 9.3517 MPa |
| R² | 0.5696 |

Diễn giải:

- MAE khoảng 7.49 MPa: sai lệch tuyệt đối trung bình.
- RMSE khoảng 9.35 MPa: nhạy hơn với sai số lớn.
- R² khoảng 0.57: mô hình giải thích được khoảng
  57% biến thiên của strength trên tập Test.

R² không có nghĩa độ chính xác dự đoán là 57%.

Kết quả gốc được lưu tại:

`reports/tables/final_test_metrics.csv`


## 13. Phân tích sai số Residual

Residual được tính theo công thức:

```text
Residual = Actual Strength - Predicted Strength
```

- Residual dương: mô hình dự đoán thấp hơn thực tế.
- Residual âm: mô hình dự đoán cao hơn thực tế.
- Residual gần 0: dự đoán gần giá trị thực tế.

Các biểu đồ chính:

- `actual_vs_predicted.png`
- `residual_vs_age.png`
- `residual_vs_actual_strength.png`

Các bảng phân tích:

- `test_predictions.csv`
- `top_10_residuals.csv`
- `train_domain_ranges.csv`

Thư mục chứa bảng:

`reports/tables/`

Nhận xét:

Linear Regression chưa mô tả đầy đủ quan hệ
phi tuyến giữa tuổi bê tông và cường độ nén.

Một số mẫu có sai số lớn ngay cả khi từng biến
vẫn nằm trong khoảng min-max của Train.

Báo cáo chi tiết:

`reports/residual_analysis.md`


## 14. Các API chính

### GET /api/health

Kiểm tra trạng thái hoạt động của server.

### GET /api/domain

Trả về miền giá trị Train của 8 biến đầu vào.

### POST /api/strength

Dự đoán cường độ nén bê tông.

Ví dụ dữ liệu gửi lên:

```json
{
  "cement": 300,
  "slag": 60,
  "fly_ash": 80,
  "water": 180,
  "superplasticizer": 7,
  "coarse_aggregate": 1000,
  "fine_aggregate": 800,
  "age": 28
}
```

Kết quả dự đoán của mô hình hiện tại:

```json
{
  "predicted_strength_mpa": 38.02,
  "model": "Linear Regression",
  "warning": "Chỉ sử dụng cho mục đích học tập và khảo sát."
}
```

Đối tượng trên minh họa các trường chính;
nội dung `warning` thực tế có thể dài hơn.

Nếu đầu vào vượt miền Train, API trả HTTP 422.

### GET /api/dashboard/summary

Trả về các chỉ số Test, bảng so sánh Validation,
learning rate và thông tin chia dữ liệu.

### GET /api/dashboard/chart/{filename}

Trả về các biểu đồ PNG được cho phép.

### POST /api/sensitivity

Phân tích độ nhạy bằng cách thay đổi một biến
và giữ cố định bảy biến còn lại.

API sử dụng chính mô hình đã huấn luyện
để tính các điểm của biểu đồ.

Các API có thể được xem và thử tại:

http://127.0.0.1:8000/docs


## 15. Kiểm thử tự động

Bộ kiểm thử nằm tại:

`tests/test_api.py`

Cài thư viện:

```powershell
python -m pip install pytest httpx
```

Chạy kiểm thử:

```powershell
python -m pytest tests/test_api.py -v
```

Bộ kiểm thử bao gồm:

- Kiểm tra các route web.
- Kiểm tra API health.
- Kiểm tra miền dữ liệu Train.
- Kiểm tra dự đoán hợp lệ.
- Kiểm tra dữ liệu âm, thiếu, sai kiểu.
- Kiểm tra dữ liệu ngoài miền Train.
- Kiểm tra kết quả Dashboard.
- Kiểm tra các biểu đồ.
- Kiểm tra phân tích độ nhạy.
- Kiểm tra CORS cho Go Live.

Kết quả kiểm thử gần nhất trên môi trường phát triển:

```text
24 passed, 1 warning
```

Các bài kiểm thử đã chạy thành công.
Cảnh báo hiện tại liên quan đến thư viện Starlette TestClient
và không làm bài kiểm thử thất bại.

Kết quả trên môi trường khác cần được chạy lại để xác nhận.


## 16. Tái tạo quy trình thí nghiệm

Project đã lưu sẵn dữ liệu chia tập, mô hình và kết quả
đánh giá nên không cần huấn luyện lại chỉ để chạy website.

Nếu cần chạy lại quy trình Machine Learning,
thực hiện tại thư mục gốc theo thứ tự:

```powershell
python src/prepare_data.py

python src/split_data.py

python src/eda.py

python src/baseline.py

python src/train_linear.py

python src/experiment_sgd.py

python src/compare_models.py

python src/evaluate_final.py
```

Lưu ý:

- Các lệnh có thể ghi đè kết quả trong `reports/`,
  `models/` và `data/processed/`.
- Nên commit hoặc sao lưu kết quả hiện tại trước khi chạy lại.
- Nếu kết quả khác, kiểm tra phiên bản thư viện,
  dữ liệu nguồn và cấu hình random_state.
- Không dùng tập Test để lựa chọn hoặc tinh chỉnh mô hình.


## 17. Giới hạn của hệ thống

- Linear Regression chỉ biểu diễn quan hệ tuyến tính.
- Một số ảnh hưởng của thành phần bê tông có thể phi tuyến.
- Kiểm tra min-max không bảo đảm cấp phối nằm trong
  vùng dữ liệu quen thuộc của mô hình.
- Biểu đồ Sensitivity mô tả phản ứng của mô hình,
  không chứng minh quan hệ nhân quả.
- Kết quả không thay thế các thí nghiệm và
  tiêu chuẩn kiểm định vật liệu.
- Mô hình chỉ được sử dụng cho học tập và khảo sát.


## 18. Các tài liệu kết quả

Các báo cáo có sẵn:

- `reports/data_quality.md`
- `reports/eda_report.md`
- `reports/split_report.md`
- `reports/model_experiments.md`
- `reports/residual_analysis.md`
- `reports/model_card.md`

Bảng kết quả:

`reports/tables/`

Biểu đồ:

`reports/figures/`


## 19. Công nghệ sử dụng

**Machine Learning:**

- Python
- pandas
- numpy
- scikit-learn
- matplotlib
- joblib

**Backend:**

- FastAPI
- Pydantic
- Uvicorn

**Frontend:**

- HTML
- CSS
- JavaScript

**Testing:**

- pytest
- HTTPX
- FastAPI TestClient


## 20. Kết luận

Project đã triển khai quy trình từ chuẩn bị dữ liệu,
huấn luyện, so sánh mô hình đến đánh giá và xây dựng
ứng dụng web.

Linear Regression được chọn do có RMSE thấp nhất
trên tập Validation trong các phương pháp đã thử.

Kết quả Test cho thấy mô hình cung cấp
một mức dự đoán tham khảo, nhưng vẫn tồn tại
những sai số đáng kể và giới hạn phi tuyến.

Hệ thống được xây dựng cho mục đích học tập,
nghiên cứu và khảo sát dữ liệu bê tông.
