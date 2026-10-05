from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ROOT_DIR = Path(__file__).resolve().parents[1]

TRAIN_PATH = (
    ROOT_DIR
    / "data"
    / "processed"
    / "train.csv"
)

VALIDATION_PATH = (
    ROOT_DIR
    / "data"
    / "processed"
    / "validation.csv"
)

TABLE_DIR = (
    ROOT_DIR
    / "reports"
    / "tables"
)

MODEL_DIR = (
    ROOT_DIR
    / "models"
    / "candidates"
)

TABLE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)


FEATURES = [
    "cement",
    "slag",
    "fly_ash",
    "water",
    "superplasticizer",
    "coarse_aggregate",
    "fine_aggregate",
    "age",
]

TARGET = "strength"


def main():

    # ==========================
    # 1. DOC DU LIEU
    # ==========================

    train = pd.read_csv(
        TRAIN_PATH
    )

    validation = pd.read_csv(
        VALIDATION_PATH
    )

    X_train = train[
        FEATURES
    ]

    y_train = train[
        TARGET
    ]

    X_validation = validation[
        FEATURES
    ]

    y_validation = validation[
        TARGET
    ]

    # ==========================
    # 2. TAO MODEL
    # ==========================

    pipeline = Pipeline(
        steps=[
            (
                "scaler",
                StandardScaler()
            ),
            (
                "model",
                LinearRegression()
            ),
        ]
    )

    # CHI HOC TREN TRAIN
    pipeline.fit(
        X_train,
        y_train
    )

    # ==========================
    # 3. DU DOAN VALIDATION
    # ==========================

    predictions = pipeline.predict(
        X_validation
    )

    # ==========================
    # 4. TINH METRIC
    # ==========================

    mae = mean_absolute_error(
        y_validation,
        predictions
    )

    mse = mean_squared_error(
        y_validation,
        predictions
    )

    rmse = np.sqrt(
        mse
    )

    r2 = r2_score(
        y_validation,
        predictions
    )

    print(
        "===== LINEAR REGRESSION ====="
    )

    print(
        f"MAE: {mae:.4f}"
    )

    print(
        f"RMSE: {rmse:.4f}"
    )

    print(
        f"R2: {r2:.4f}"
    )

    # ==========================
    # 5. LUU METRIC
    # ==========================

    result = pd.DataFrame(
        {
            "model": [
                "Linear Regression"
            ],
            "MAE": [mae],
            "RMSE": [rmse],
            "R2": [r2],
        }
    )

    result.to_csv(
        TABLE_DIR
        / "linear_validation.csv",
        index=False
    )

    # ==========================
    # 6. LUU HE SO
    # ==========================

    model = (
        pipeline
        .named_steps["model"]
    )

    coefficients = pd.DataFrame(
        {
            "feature":
                FEATURES,
            "coefficient":
                model.coef_,
        }
    )

    coefficients[
        "abs_coefficient"
    ] = (
        coefficients[
            "coefficient"
        ].abs()
    )

    coefficients = (
        coefficients
        .sort_values(
            "abs_coefficient",
            ascending=False
        )
    )

    coefficients.to_csv(
        TABLE_DIR
        / "linear_coefficients.csv",
        index=False
    )

    print(
        "\n===== HE SO ====="
    )

    print(
        coefficients.to_string(
            index=False
        )
    )

    # ==========================
    # 7. LUU MODEL
    # ==========================

    joblib.dump(
        pipeline,
        MODEL_DIR
        / "linear_regression.joblib"
    )


if __name__ == "__main__":
    main()