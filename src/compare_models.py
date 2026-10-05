from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]

TABLE_DIR = (
    ROOT_DIR
    / "reports"
    / "tables"
)


def main():

    baseline = pd.read_csv(
        TABLE_DIR
        / "baseline_validation.csv"
    )

    linear = pd.read_csv(
        TABLE_DIR
        / "linear_validation.csv"
    )

    sgd_results = pd.read_csv(
        TABLE_DIR
        / "sgd_learning_rate_results.csv"
    )

    # Tim SGD co RMSE nho nhat
    best_sgd = (
        sgd_results
        .sort_values(
            "RMSE"
        )
        .iloc[0]
    )

    sgd = pd.DataFrame(
        {
            "model": [
                "SGDRegressor"
            ],
            "MAE": [
                best_sgd["MAE"]
            ],
            "RMSE": [
                best_sgd["RMSE"]
            ],
            "R2": [
                best_sgd["R2"]
            ],
        }
    )

    comparison = pd.concat(
        [
            baseline,
            linear,
            sgd,
        ],
        ignore_index=True
    )

    comparison = (
        comparison
        .sort_values(
            "RMSE"
        )
    )

    print(
        "===== MODEL COMPARISON ====="
    )

    print(
        comparison.to_string(
            index=False
        )
    )

    comparison.to_csv(
        TABLE_DIR
        / "model_comparison_validation.csv",
        index=False
    )


if __name__ == "__main__":
    main()