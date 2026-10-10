
from pathlib import Path
import json

import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, ConfigDict, Field
from fastapi.middleware.cors import CORSMiddleware

# =====================================
# 1. ĐƯỜNG DẪN VÀ CẤU HÌNH
# =====================================

ROOT = Path(__file__).resolve().parents[1]

TEMPLATE_DIR = ROOT / "app" / "templates"

FEATURES = [
    "cement",
    "slag",
    "fly_ash",
    "water",
    "superplasticizer",
    "coarse_aggregate",
    "fine_aggregate",
    "age"
]

FEATURE_NAMES = {
    "cement": "Xi măng",
    "slag": "Xỉ lò cao",
    "fly_ash": "Tro bay",
    "water": "Nước",
    "superplasticizer": "Phụ gia siêu dẻo",
    "coarse_aggregate": "Cốt liệu thô",
    "fine_aggregate": "Cốt liệu mịn",
    "age": "Tuổi bê tông"
}


# =====================================
# 2. ĐỌC CẤU HÌNH MODEL
# =====================================

CONFIG_PATH = ROOT / "config" / "final_model.json"

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

if config["model_type"] != "linear":
    raise RuntimeError(
        "API hiện chỉ hỗ trợ mô hình Linear Regression"
    )


# =====================================
# 3. NẠP MODEL ĐÃ HUẤN LUYỆN
# =====================================

MODEL_PATH = ROOT / config["model_path"]

# Chỉ nạp model do chính nhóm tạo và tin cậy.
# Model chỉ được tải một lần khi khởi động server.
model = joblib.load(MODEL_PATH)


# =====================================
# 4. ĐỌC MIỀN DỮ LIỆU TRAIN
# =====================================

RANGE_PATH = (
    ROOT / "reports" / "tables" / "train_domain_ranges.csv"
)

ranges = pd.read_csv(RANGE_PATH)

DOMAIN = {
    row["feature"]: (
        float(row["train_min"]),
        float(row["train_max"])
    )
    for _, row in ranges.iterrows()
}


# =====================================
# 5. KHỞI TẠO FASTAPI
# =====================================

app = FastAPI(
    title="Concrete Strength Prediction",
    description="API dự đoán cường độ nén bê tông",
    version="1.0"
)


# Cho phép Go Live kết nối với FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5501",
        "http://localhost:5501"
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"]
)

# =====================================
# 6. SCHEMA DỮ LIỆU ĐẦU VÀO
# =====================================

class ConcreteInput(BaseModel):

    model_config = ConfigDict(
        extra="forbid",
        allow_inf_nan=False
    )

    cement: float = Field(ge=0)
    slag: float = Field(ge=0)
    fly_ash: float = Field(ge=0)
    water: float = Field(ge=0)
    superplasticizer: float = Field(ge=0)
    coarse_aggregate: float = Field(ge=0)
    fine_aggregate: float = Field(ge=0)
    age: int = Field(gt=0)


# =====================================
# 7. XỬ LÝ LỖI VALIDATION TIẾNG VIỆT
# =====================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):

    errors = []

    for error in exc.errors():

        location = error.get("loc", [])
        error_type = error.get("type", "")

        field = next(
            (
                item for item in reversed(location)
                if isinstance(item, str)
                and item not in ("body", "query", "path")
            ),
            "Dữ liệu"
        )

        field_name = FEATURE_NAMES.get(field, field)

        # Dịch thông báo lỗi sang tiếng Việt
        if error_type == "missing":
            message = "Không được bỏ trống"

        elif error_type == "greater_than_equal":
            message = "Phải lớn hơn hoặc bằng 0"

        elif error_type == "greater_than":
            message = "Phải lớn hơn 0"

        elif error_type in (
            "int_parsing",
            "int_from_float",
            "int_type"
        ):
            message = "Phải là số nguyên hợp lệ"

        elif error_type in (
            "float_parsing",
            "float_type"
        ):
            message = "Phải là số hợp lệ"

        elif error_type == "finite_number":
            message = "Giá trị phải là số hữu hạn"

        elif error_type == "extra_forbidden":
            message = "Trường dữ liệu không được hỗ trợ"

        else:
            message = "Giá trị không hợp lệ"

        errors.append({
            "loc": list(location),
            "type": error_type,
            "field": field_name,
            "msg": message
        })

    return JSONResponse(
        status_code=422,
        content={
            "detail": errors
        }
    )


# =====================================
# 8. TRANG CHỦ GIỚI THIỆU PROJECT 12
# =====================================

@app.get("/", include_in_schema=False)
def home():

    return FileResponse(
        TEMPLATE_DIR / "index.html",
        media_type="text/html",
        headers={
            "Cache-Control": "no-store, max-age=0"
        }
    )


# =====================================
# 9. API KIỂM TRA TRẠNG THÁI
# =====================================

@app.get("/api/health")
def health_check():

    return {
        "status": "ok",
        "message": "API đang hoạt động",
        "model": "Linear Regression",
        "version": "1.0"
    }


# =====================================
# 10. API DỰ ĐOÁN CƯỜNG ĐỘ
# =====================================

@app.post("/api/strength")
def predict_strength(request: ConcreteInput):

    values = request.model_dump()

    outside = []

    # Kiểm tra miền giá trị của tập Train
    for feature in FEATURES:

        low, high = DOMAIN[feature]
        value = values[feature]

        if not (low <= value <= high):

            outside.append({
                "feature": feature,
                "name": FEATURE_NAMES[feature],
                "value": value,
                "min": low,
                "max": high
            })

    # Nếu đầu vào vượt miền Train
    if outside:

        raise HTTPException(
            status_code=422,
            detail={
                "message": (
                    "Dữ liệu nằm ngoài miền huấn luyện"
                ),
                "fields": outside
            }
        )

    # Tạo DataFrame theo đúng thứ tự feature
    X = pd.DataFrame(
        [values],
        columns=FEATURES
    )

    # Dự đoán từ Pipeline đã huấn luyện
    prediction = float(
        model.predict(X)[0]
    )

    return {
        "predicted_strength_mpa": round(
            prediction, 2
        ),
        "model": "Linear Regression",
        "warning": (
            "Chỉ sử dụng cho mục đích học tập và khảo sát. "
            "Không thay thế thí nghiệm cường độ nén "
            "bê tông hoặc phê duyệt kỹ thuật kết cấu."
        )
    }


# =====================================
# 11. API MIỀN DỮ LIỆU TRAIN
# =====================================

@app.get("/api/domain")
def get_feature_domain():

    return {
        "features": {
            feature: {
                "name": FEATURE_NAMES[feature],
                "min": low,
                "max": high,
                "unit": (
                    "ngày"
                    if feature == "age"
                    else "kg/m³"
                )
            }
            for feature, (low, high) in DOMAIN.items()
        }
    }


# =====================================
# 12. TRANG WEB DỰ ĐOÁN
# =====================================

@app.get("/predict", include_in_schema=False)
def prediction_page():

    return FileResponse(
        TEMPLATE_DIR / "predict.html",
        media_type="text/html",
        headers={
            "Cache-Control": "no-store, max-age=0"
        }
    )
