
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.model_selection import GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


ROOT = Path(__file__).resolve().parents[1]

TRAIN_PATH = ROOT / "data" / "processed" / "train.csv"

OUTPUT_DIR = ROOT / "reports" / "tables"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


FEATURES_7 = [
    "cement",
    "slag",
    "fly_ash",
    "water",
    "superplasticizer",
    "coarse_aggregate",
    "fine_aggregate",
]

FEATURES_8 = FEATURES_7 + ["age"]

TARGET = "strength"

SEEDS = [11, 42, 2026]
N_FOLDS = 5


def main():

    # 1. Chi su dung Train
    df = pd.read_csv(TRAIN_PATH)

    X = df[FEATURES_8]
    y = df[TARGET]

    # 2. Nhom theo 7 thanh phan, KHONG gom age
    groups = pd.util.hash_pandas_object(
        df[FEATURES_7],
        index=False
    )

    print("===== GROUP CROSS-VALIDATION =====")
    print("So mau Train:", len(df))
    print("So cap phoi rieng biet:", groups.nunique())

    results = []

    # 3. Chay 3 seed x 5 fold
    for seed in SEEDS:

        splitter = GroupKFold(
            n_splits=N_FOLDS,
            shuffle=True,
            random_state=seed
        )

        for fold, (train_idx, val_idx) in enumerate(
            splitter.split(X, y, groups),
            start=1
        ):

            X_train = X.iloc[train_idx]
            y_train = y.iloc[train_idx]

            X_val = X.iloc[val_idx]
            y_val = y.iloc[val_idx]

            # Kiem tra cac cap phoi khong trung nhau
            train_groups = set(groups.iloc[train_idx])
            val_groups = set(groups.iloc[val_idx])

            assert train_groups.isdisjoint(val_groups)

            # Moi fold co Pipeline rieng
            pipeline = Pipeline([
                ("scaler", StandardScaler()),
                ("model", LinearRegression()),
            ])

            # Fit scaler va model chi tren train fold
            pipeline.fit(X_train, y_train)

            predictions = pipeline.predict(X_val)

            mae = mean_absolute_error(
                y_val, predictions
            )

            rmse = np.sqrt(
                mean_squared_error(y_val, predictions)
            )

            r2 = r2_score(y_val, predictions)

            results.append({
                "seed": seed,
                "fold": fold,
                "train_size": len(train_idx),
                "validation_size": len(val_idx),
                "MAE": mae,
                "RMSE": rmse,
                "R2": r2,
            })

            print(
                f"Seed={seed}, Fold={fold}: "
                f"MAE={mae:.4f}, "
                f"RMSE={rmse:.4f}, "
                f"R2={r2:.4f}"
            )

    # 4. Luu ket qua chi tiet
    result_df = pd.DataFrame(results)

    result_df.to_csv(
        OUTPUT_DIR / "linear_stability_group7_cv.csv",
        index=False
    )

    # 5. Tong hop theo seed
    summary = result_df.groupby("seed")[
        ["MAE", "RMSE", "R2"]
    ].agg(["mean", "std"])

    print("\n===== KET QUA THEO SEED =====")
    print(summary.round(4).to_string())

    # 6. Tong hop 15 luot
    print("\n===== TONG HOP 15 LUOT =====")

    for metric in ["MAE", "RMSE", "R2"]:
        print(
            f"{metric}: "
            f"mean={result_df[metric].mean():.4f}, "
            f"std={result_df[metric].std():.4f}"
        )

    print("\nDA LUU KET QUA TAI:")
    print(
        OUTPUT_DIR / "linear_stability_group7_cv.csv"
    )


if __name__ == "__main__":
    main()
