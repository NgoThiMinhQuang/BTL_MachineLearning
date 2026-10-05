from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.linear_model import SGDRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
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

FIGURE_DIR = (
    ROOT_DIR
    / "reports"
    / "figures"
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

FIGURE_DIR.mkdir(
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

RANDOM_STATE = 42

EPOCHS = 200

LEARNING_RATES = [
    0.0001,
    0.001,
    0.01,
]


def main():

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
    ].to_numpy()

    X_validation = validation[
        FEATURES
    ]

    y_validation = validation[
        TARGET
    ]

    # ==========================
    # CHUAN HOA
    # ==========================

    scaler = StandardScaler()

    X_train_scaled = (
        scaler.fit_transform(
            X_train
        )
    )

    X_validation_scaled = (
        scaler.transform(
            X_validation
        )
    )

    results = []

    loss_rows = []

    best_model = None

    best_rmse = float("inf")

    best_learning_rate = None

    # ==========================
    # THU 3 LEARNING RATE
    # ==========================

    for learning_rate in (
        LEARNING_RATES
    ):

        print(
            "\nLearning rate:",
            learning_rate
        )

        model = SGDRegressor(
            loss="squared_error",
            penalty=None,
            learning_rate="constant",
            eta0=learning_rate,
            max_iter=1,
            tol=None,
            shuffle=False,
            random_state=RANDOM_STATE,
        )

        rng = np.random.default_rng(
            RANDOM_STATE
        )

        # 200 epoch
        for epoch in range(
            1,
            EPOCHS + 1
        ):

            order = rng.permutation(
                len(X_train_scaled)
            )

            X_epoch = (
                X_train_scaled[
                    order
                ]
            )

            y_epoch = (
                y_train[
                    order
                ]
            )

            model.partial_fit(
                X_epoch,
                y_epoch
            )

            train_predictions = (
                model.predict(
                    X_train_scaled
                )
            )

            train_mse = (
                mean_squared_error(
                    y_train,
                    train_predictions
                )
            )

            loss_rows.append(
                {
                    "learning_rate":
                        learning_rate,
                    "epoch":
                        epoch,
                    "train_mse":
                        train_mse,
                }
            )

        # ======================
        # DANH GIA VALIDATION
        # ======================

        predictions = (
            model.predict(
                X_validation_scaled
            )
        )

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
            f"MAE: {mae:.4f}"
        )

        print(
            f"RMSE: {rmse:.4f}"
        )

        print(
            f"R2: {r2:.4f}"
        )

        results.append(
            {
                "learning_rate":
                    learning_rate,
                "MAE": mae,
                "RMSE": rmse,
                "R2": r2,
            }
        )

        if rmse < best_rmse:

            best_rmse = rmse

            best_model = model

            best_learning_rate = (
                learning_rate
            )

    # ==========================
    # LUU KET QUA
    # ==========================

    result_df = pd.DataFrame(
        results
    )

    result_df.to_csv(
        TABLE_DIR
        / "sgd_learning_rate_results.csv",
        index=False
    )

    loss_df = pd.DataFrame(
        loss_rows
    )

    loss_df.to_csv(
        TABLE_DIR
        / "sgd_loss_history.csv",
        index=False
    )

    # ==========================
    # VE LOSS
    # ==========================

    plt.figure(
        figsize=(9, 6)
    )

    for learning_rate in (
        LEARNING_RATES
    ):

        current = loss_df[
            loss_df[
                "learning_rate"
            ]
            == learning_rate
        ]

        plt.plot(
            current["epoch"],
            current["train_mse"],
            label=(
                f"eta0={learning_rate}"
            )
        )

    plt.xlabel(
        "Epoch"
    )

    plt.ylabel(
        "Training MSE"
    )

    plt.title(
        "SGD Loss by Learning Rate"
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR
        / "sgd_learning_rate_loss.png",
        dpi=300
    )

    plt.close()

    # ==========================
    # LUU MODEL SGD TOT NHAT
    # ==========================

    joblib.dump(
        {
            "scaler": scaler,
            "model": best_model,
            "learning_rate":
                best_learning_rate,
        },
        MODEL_DIR
        / "sgd_best.joblib"
    )

    print(
        "\n===== BEST SGD ====="
    )

    print(
        "Learning rate:",
        best_learning_rate
    )

    print(
        "Validation RMSE:",
        best_rmse
    )


if __name__ == "__main__":
    main()