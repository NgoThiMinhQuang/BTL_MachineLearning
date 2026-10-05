from pathlib import Path
import json

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


# ==========================================
# DUONG DAN
# ==========================================

ROOT_DIR = Path(__file__).resolve().parents[1]

TRAIN_PATH = (
    ROOT_DIR
    / "data"
    / "processed"
    / "train.csv"
)

TEST_PATH = (
    ROOT_DIR
    / "data"
    / "processed"
    / "test.csv"
)

CONFIG_PATH = (
    ROOT_DIR
    / "config"
    / "final_model.json"
)

TABLE_DIR = (
    ROOT_DIR
    / "reports"
    / "tables"
)

FIGURE_DIR = (
    ROOT_DIR
    / "reports"
    / "figures"
)

TABLE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

FIGURE_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================
# CAC BIEN DAU VAO
# ==========================================

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


# ==========================================
# LOAD MODEL CUOI
# ==========================================

def load_final_model():

    with open(
        CONFIG_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        config = json.load(
            file
        )

    model_path = (
        ROOT_DIR
        / config["model_path"]
    )

    saved_object = joblib.load(
        model_path
    )

    return config, saved_object


# ==========================================
# DU DOAN
# ==========================================

def predict_with_model(
    config,
    saved_object,
    X
):

    # Neu model cuoi la Linear Regression
    if (
        config["model_type"]
        == "linear"
    ):

        return saved_object.predict(
            X
        )

    # Neu model cuoi la SGDRegressor
    elif (
        config["model_type"]
        == "sgd"
    ):

        scaler = (
            saved_object[
                "scaler"
            ]
        )

        model = (
            saved_object[
                "model"
            ]
        )

        X_scaled = (
            scaler.transform(
                X
            )
        )

        return model.predict(
            X_scaled
        )

    else:

        raise ValueError(
            "model_type khong hop le"
        )


# ==========================================
# MAIN
# ==========================================

def main():

    # --------------------------------------
    # 1. DOC TRAIN VA TEST
    # --------------------------------------

    train = pd.read_csv(
        TRAIN_PATH
    )

    test = pd.read_csv(
        TEST_PATH
    )

    X_test = test[
        FEATURES
    ]

    y_test = test[
        TARGET
    ]

    # --------------------------------------
    # 2. LOAD MODEL DA CHON
    # --------------------------------------

    config, saved_object = (
        load_final_model()
    )

    print(
        "===== FINAL MODEL ====="
    )

    print(
        "Model:",
        config["model_type"]
    )

    print(
        "Selected on:",
        config["selected_on"]
    )

    print(
        "Selection metric:",
        config["selection_metric"]
    )

    # --------------------------------------
    # 3. DU DOAN TEST
    # --------------------------------------

    predictions = (
        predict_with_model(
            config,
            saved_object,
            X_test
        )
    )

    # --------------------------------------
    # 4. TINH METRIC TEST
    # --------------------------------------

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    mse = mean_squared_error(
        y_test,
        predictions
    )

    rmse = np.sqrt(
        mse
    )

    r2 = r2_score(
        y_test,
        predictions
    )

    print(
        "\n===== FINAL TEST RESULTS ====="
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

    # --------------------------------------
    # 5. LUU METRIC
    # --------------------------------------

    metrics = pd.DataFrame(
        {
            "model": [
                config["model_type"]
            ],
            "MAE": [mae],
            "RMSE": [rmse],
            "R2": [r2],
        }
    )

    metrics.to_csv(
        TABLE_DIR
        / "final_test_metrics.csv",
        index=False
    )

    # --------------------------------------
    # 6. TAO BANG DU DOAN + RESIDUAL
    # --------------------------------------

    result = test.copy()

    result[
        "predicted_strength"
    ] = predictions

    result[
        "residual"
    ] = (
        result[TARGET]
        - result[
            "predicted_strength"
        ]
    )

    result[
        "absolute_residual"
    ] = (
        result[
            "residual"
        ].abs()
    )

    result.to_csv(
        TABLE_DIR
        / "test_predictions.csv",
        index=False
    )

    # --------------------------------------
    # 7. TIM 10 RESIDUAL LON NHAT
    # --------------------------------------

    top_10 = (
        result
        .sort_values(
            "absolute_residual",
            ascending=False
        )
        .head(10)
        .copy()
    )

    # --------------------------------------
    # 8. TAO MIEN TRAIN
    # --------------------------------------

    domain_rows = []

    for feature in FEATURES:

        minimum = (
            train[
                feature
            ].min()
        )

        maximum = (
            train[
                feature
            ].max()
        )

        domain_rows.append(
            {
                "feature":
                    feature,
                "train_min":
                    minimum,
                "train_max":
                    maximum,
            }
        )

    domain_df = pd.DataFrame(
        domain_rows
    )

    domain_df.to_csv(
        TABLE_DIR
        / "train_domain_ranges.csv",
        index=False
    )

    # --------------------------------------
    # 9. KIEM TRA 10 MAU CO NGOAI MIEN TRAIN
    # --------------------------------------

    outside_messages = []

    for _, row in (
        top_10.iterrows()
    ):

        outside_features = []

        for feature in FEATURES:

            train_min = (
                train[
                    feature
                ].min()
            )

            train_max = (
                train[
                    feature
                ].max()
            )

            if (
                row[feature]
                < train_min
                or
                row[feature]
                > train_max
            ):

                outside_features.append(
                    feature
                )

        if (
            len(
                outside_features
            )
            == 0
        ):

            outside_messages.append(
                "No"
            )

        else:

            outside_messages.append(
                ", ".join(
                    outside_features
                )
            )

    top_10[
        "outside_train_range"
    ] = outside_messages

    top_10.to_csv(
        TABLE_DIR
        / "top_10_residuals.csv",
        index=False
    )

    print(
        "\n===== TOP 10 RESIDUALS ====="
    )

    print(
        top_10[
            [
                "strength",
                "predicted_strength",
                "residual",
                "absolute_residual",
                "age",
                "outside_train_range",
            ]
        ].to_string(
            index=False
        )
    )

    # --------------------------------------
    # 10. RESIDUAL VS AGE
    # --------------------------------------

    plt.figure(
        figsize=(8, 5)
    )

    plt.scatter(
        result["age"],
        result["residual"],
        alpha=0.7
    )

    plt.axhline(
        y=0,
        linewidth=1
    )

    plt.xlabel(
        "Age (days)"
    )

    plt.ylabel(
        "Residual (MPa)"
    )

    plt.title(
        "Residual vs Age - Test Set"
    )

    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR
        / "residual_vs_age.png",
        dpi=300
    )

    plt.close()

    # --------------------------------------
    # 11. RESIDUAL VS STRENGTH
    # --------------------------------------

    plt.figure(
        figsize=(8, 5)
    )

    plt.scatter(
        result["strength"],
        result["residual"],
        alpha=0.7
    )

    plt.axhline(
        y=0,
        linewidth=1
    )

    plt.xlabel(
        "Actual Strength (MPa)"
    )

    plt.ylabel(
        "Residual (MPa)"
    )

    plt.title(
        "Residual vs Actual Strength"
    )

    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR
        / "residual_vs_actual_strength.png",
        dpi=300
    )

    plt.close()

    # --------------------------------------
    # 12. ACTUAL VS PREDICTED
    # --------------------------------------

    plt.figure(
        figsize=(8, 5)
    )

    plt.scatter(
        y_test,
        predictions,
        alpha=0.7
    )

    minimum = min(
        y_test.min(),
        predictions.min()
    )

    maximum = max(
        y_test.max(),
        predictions.max()
    )

    plt.plot(
        [minimum, maximum],
        [minimum, maximum]
    )

    plt.xlabel(
        "Actual Strength (MPa)"
    )

    plt.ylabel(
        "Predicted Strength (MPa)"
    )

    plt.title(
        "Actual vs Predicted Strength"
    )

    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR
        / "actual_vs_predicted.png",
        dpi=300
    )

    plt.close()

    print(
        "\nDa luu xong ket qua final evaluation."
    )


if __name__ == "__main__":
    main()