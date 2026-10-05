# BTL Machine Learning - Concrete Compressive Strength

## 1. Giới thiệu

Đề tài xây dựng mô hình hồi quy để ước lượng cường độ
chịu nén của bê tông (MPa) dựa trên thành phần cấp phối
và tuổi bê tông.

Dataset sử dụng:
Concrete Compressive Strength - UCI Machine Learning Repository.

## 2. Biến đầu vào

Mô hình sử dụng 8 biến:

- cement
- slag
- fly_ash
- water
- superplasticizer
- coarse_aggregate
- fine_aggregate
- age

Biến cần dự đoán:

- strength (MPa)

## 3. Cấu trúc project

- `data/`: chứa dữ liệu
- `src/`: chứa code Python
- `reports/`: chứa báo cáo, bảng và hình
- `models/`: chứa mô hình đã lưu
- `app/`: sẽ chứa ứng dụng web

## 4. Cài đặt

Tạo môi trường:

```cmd
python -m venv .venv