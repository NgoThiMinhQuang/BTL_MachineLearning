from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


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

TABLE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

TARGET = "strength"


def main():

    # Doc tap Train
    train = pd.read_csv(
        TRAIN_PATH
    )

    # Doc tap Validation
    validation = pd.read_csv(
        VALIDATION_PATH
    )

    # Tinh trung binh strength cua Train
    train_mean = train[TARGET].mean()

    # Tat ca mau Validation deu duoc du doan
    # bang gia tri trung binh cua Train
    predictions = np.full(
        len(validation),
        train_mean
    )

    # MAE
    mae = mean_absolute_error(
        validation[TARGET],
        predictions
    )

    # MSE
    mse = mean_squared_error(
        validation[TARGET],
        predictions
    )

    # RMSE
    rmse = np.sqrt(mse)

    # R2
    r2 = r2_score(
        validation[TARGET],
        predictions
    )

    print("===== MEAN BASELINE =====")

    print(
        f"Train mean: {train_mean:.4f}"
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

    # Luu ket qua
    result = pd.DataFrame(
        {
            "model": [
                "Mean Baseline"
            ],
            "MAE": [mae],
            "RMSE": [rmse],
            "R2": [r2],
        }
    )

    result.to_csv(
        TABLE_DIR
        / "baseline_validation.csv",
        index=False
    )


if __name__ == "__main__":
    main()