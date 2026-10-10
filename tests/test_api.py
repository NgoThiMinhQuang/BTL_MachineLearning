
"""
KIỂM THỬ TỰ ĐỘNG - PROJECT 12
Ước lượng cường độ nén bê tông

Kiểm thử:
- Trang web
- API sức khỏe hệ thống
- Miền dữ liệu Train
- API dự đoán
- Kiểm tra dữ liệu đầu vào
- Dashboard
- Phân tích độ nhạy
- CORS cho Go Live
"""

import pytest

from fastapi.testclient import TestClient
from app.main import app


# =====================================
# 1. KHỞI TẠO TEST CLIENT
# =====================================

# TestClient cho phép kiểm thử FastAPI
# mà không cần bật server bằng uvicorn.

client = TestClient(app)


# =====================================
# 2. DỮ LIỆU MẪU
# =====================================

SAMPLE = {
    "cement": 300,
    "slag": 60,
    "fly_ash": 80,
    "water": 180,
    "superplasticizer": 7,
    "coarse_aggregate": 1000,
    "fine_aggregate": 800,
    "age": 28,
}

FEATURES = set(SAMPLE)


# =====================================
# 3. KIỂM THỬ CÁC TRANG WEB
# =====================================

@pytest.mark.parametrize(
    "path",
    [
        "/",
        "/predict",
        "/dashboard",
    ]
)
def test_web_pages_load(path):

    response = client.get(path)

    assert response.status_code == 200

    assert "text/html" in (
        response.headers["content-type"]
    )


# =====================================
# 4. KIỂM THỬ API HEALTH
# =====================================

def test_health_api():

    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


# =====================================
# 5. KIỂM THỬ MIỀN TRAIN
# =====================================

def test_domain_api():

    response = client.get("/api/domain")

    assert response.status_code == 200

    data = response.json()

    features = data["features"]

    # Phải có đủ 8 thông số
    assert set(features) == FEATURES

    # Miền xi măng trong Train
    assert features["cement"]["min"] == pytest.approx(
        102
    )

    assert features["cement"]["max"] == pytest.approx(
        540
    )

    # Miền tuổi bê tông trong Train
    assert features["age"]["min"] == pytest.approx(
        3
    )

    assert features["age"]["max"] == pytest.approx(
        365
    )

    # Miền min-max phải hợp lệ
    assert all(
        item["min"] <= item["max"]
        for item in features.values()
    )


# =====================================
# 6. KIỂM THỬ DỰ ĐOÁN HỢP LỆ
# =====================================

def test_valid_prediction():

    response = client.post(
        "/api/strength",
        json=SAMPLE
    )

    assert response.status_code == 200

    result = response.json()

    assert result["model"] == (
        "Linear Regression"
    )

    # Bộ dữ liệu mẫu đã kiểm tra trên web:
    # Kết quả khoảng 38.02 MPa
    assert result[
        "predicted_strength_mpa"
    ] == pytest.approx(
        38.02,
        abs=0.05
    )


# =====================================
# 7. KIỂM THỬ VƯỢT MIỀN TRAIN
# =====================================

def test_outside_train_range():

    payload = {
        **SAMPLE,
        "cement": 600
    }

    response = client.post(
        "/api/strength",
        json=payload
    )

    assert response.status_code == 422

    detail = response.json()["detail"]

    assert detail["message"] == (
        "Dữ liệu nằm ngoài miền huấn luyện"
    )

    assert any(
        item["feature"] == "cement"
        for item in detail["fields"]
    )


# =====================================
# 8. KIỂM THỬ NHIỀU BIẾN VƯỢT MIỀN
# =====================================

def test_multiple_outside_train_ranges():

    payload = {
        **SAMPLE,
        "cement": 600,
        "age": 400
    }

    response = client.post(
        "/api/strength",
        json=payload
    )

    assert response.status_code == 422

    fields = {
        item["feature"]
        for item in response.json()[
            "detail"
        ]["fields"]
    }

    assert {
        "cement",
        "age"
    }.issubset(fields)


# =====================================
# 9. KIỂM THỬ GIÁ TRỊ KHÔNG HỢP LỆ
# =====================================

@pytest.mark.parametrize(
    "changes,field",
    [
        ({"cement": -1}, "cement"),
        ({"age": 0}, "age"),
        ({"age": 28.5}, "age"),
    ]
)
def test_invalid_values(changes, field):

    payload = {
        **SAMPLE,
        **changes
    }

    response = client.post(
        "/api/strength",
        json=payload
    )

    assert response.status_code == 422

    errors = response.json()["detail"]

    assert isinstance(errors, list)

    # Phải xác định được trường nhập sai
    assert any(
        error["loc"][-1] == field
        for error in errors
    )

    # Phải có thông báo lỗi
    assert all(
        error["msg"]
        for error in errors
    )


# =====================================
# 10. KIỂM THỬ THIẾU THÔNG SỐ
# =====================================

def test_missing_field():

    payload = dict(SAMPLE)

    # Cố tình không gửi biến water
    payload.pop("water")

    response = client.post(
        "/api/strength",
        json=payload
    )

    assert response.status_code == 422

    errors = response.json()["detail"]

    assert any(
        error["loc"][-1] == "water"
        for error in errors
    )


# =====================================
# 11. KIỂM THỬ THÔNG SỐ KHÔNG TỒN TẠI
# =====================================

def test_unknown_field_rejected():

    payload = {
        **SAMPLE,
        "unknown": 123
    }

    response = client.post(
        "/api/strength",
        json=payload
    )

    assert response.status_code == 422

    errors = response.json()["detail"]

    assert any(
        error["type"] == "extra_forbidden"
        for error in errors
    )


# =====================================
# 12. KIỂM THỬ DASHBOARD
# =====================================

def test_dashboard_summary():

    response = client.get(
        "/api/dashboard/summary"
    )

    assert response.status_code == 200

    result = response.json()

    assert result["selected_model"] == (
        "Linear Regression"
    )

    # Kiểm tra số mẫu
    assert result["split"] == {
        "train": 721,
        "validation": 156,
        "test": 153
    }

    # Kiểm tra số liệu Test
    assert result["test"]["MAE"] == (
        pytest.approx(7.4896, abs=0.01)
    )

    assert result["test"]["RMSE"] == (
        pytest.approx(9.3517, abs=0.01)
    )

    assert result["test"]["R2"] == (
        pytest.approx(0.5696, abs=0.01)
    )

    # Đủ 3 mô hình so sánh
    assert len(result["validation"]) == 3

    # Đủ 3 thí nghiệm SGD
    assert len(result["sgd"]) == 3


# =====================================
# 13. KIỂM THỬ 4 BIỂU ĐỒ DASHBOARD
# =====================================

@pytest.mark.parametrize(
    "filename",
    [
        "actual_vs_predicted.png",
        "residual_vs_age.png",
        "residual_vs_actual_strength.png",
        "sgd_learning_rate_loss.png",
    ]
)
def test_dashboard_chart(filename):

    response = client.get(
        f"/api/dashboard/chart/{filename}"
    )

    assert response.status_code == 200

    assert response.headers[
        "content-type"
    ].startswith("image/png")

    # File phải có dữ liệu ảnh
    assert len(response.content) > 100


# =====================================
# 14. KIỂM THỬ BIỂU ĐỒ KHÔNG TỒN TẠI
# =====================================

def test_unknown_chart_rejected():

    response = client.get(
        "/api/dashboard/chart/unknown.png"
    )

    assert response.status_code == 404


# =====================================
# 15. KIỂM THỬ SENSITIVITY - XI MĂNG
# =====================================

def test_sensitivity_cement():

    payload = {
        **SAMPLE,
        "feature": "cement"
    }

    response = client.post(
        "/api/sensitivity",
        json=payload
    )

    assert response.status_code == 200

    result = response.json()

    assert result["feature"] == "cement"

    assert result["name"] == "Xi măng"

    # Điểm đang khảo sát
    assert result["baseline"]["value"] == (
        pytest.approx(300)
    )

    # Kết quả tại cấp phối gốc
    assert result[
        "baseline"
    ]["strength_mpa"] == pytest.approx(
        38.02,
        abs=0.05
    )

    points = result["points"]

    # Biểu đồ cần đủ điểm khảo sát
    assert len(points) >= 30

    xs = [
        point["value"]
        for point in points
    ]

    # Giá trị khảo sát phải được sắp xếp
    assert xs == sorted(xs)

    # Không được vượt miền Train
    assert all(
        result["min"] <= value <= result["max"]
        for value in xs
    )

    # Phải có giá trị xi măng hiện tại
    assert 300 in xs

    # Các điểm phải có kết quả số
    assert all(
        isinstance(
            point["strength_mpa"],
            (int, float)
        )
        for point in points
    )


# =====================================
# 16. KIỂM THỬ SENSITIVITY - TUỔI
# =====================================

def test_sensitivity_age_values_are_integers():

    payload = {
        **SAMPLE,
        "feature": "age"
    }

    response = client.post(
        "/api/sensitivity",
        json=payload
    )

    assert response.status_code == 200

    result = response.json()

    assert result["feature"] == "age"

    assert result["baseline"]["value"] == (
        pytest.approx(28)
    )

    # Tuổi bê tông phải là số nguyên
    assert all(
        float(point["value"]).is_integer()
        for point in result["points"]
    )


# =====================================
# 17. KIỂM THỬ FEATURE KHÔNG HỢP LỆ
# =====================================

def test_sensitivity_invalid_feature():

    payload = {
        **SAMPLE,
        "feature": "strength"
    }

    response = client.post(
        "/api/sensitivity",
        json=payload
    )

    assert response.status_code == 422


# =====================================
# 18. KIỂM THỬ SENSITIVITY VƯỢT MIỀN
# =====================================

def test_sensitivity_outside_train_range():

    payload = {
        **SAMPLE,
        "feature": "cement",
        "cement": 600
    }

    response = client.post(
        "/api/sensitivity",
        json=payload
    )

    assert response.status_code == 422

    detail = response.json()["detail"]

    assert any(
        field["feature"] == "cement"
        for field in detail["fields"]
    )


# =====================================
# 19. KIỂM THỬ CORS CHO GO LIVE
# =====================================

def test_cors_for_go_live():

    response = client.get(
        "/api/domain",
        headers={
            "Origin": "http://127.0.0.1:5500"
        }
    )

    assert response.status_code == 200

    assert response.headers.get(
        "access-control-allow-origin"
    ) == "http://127.0.0.1:5500"


# =====================================
# 20. KIEM THU DU DOAN CUONG DO AM
# =====================================

def test_negative_strength_prediction_rejected():

    # Tat ca thong so nam trong mien Train
    # nhung to hop nay lam mo hinh du doan am.
    invalid_combination = {
        "cement": 102,
        "slag": 0,
        "fly_ash": 0,
        "water": 247,
        "superplasticizer": 0,
        "coarse_aggregate": 801,
        "fine_aggregate": 594,
        "age": 3,
    }

    response = client.post(
        "/api/strength",
        json=invalid_combination
    )

    # API phai tu choi du doan phi thuc te
    assert response.status_code == 422

    detail = response.json()["detail"]

    assert isinstance(detail, str)

    assert "không phù hợp về mặt vật lý" in detail
