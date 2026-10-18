from pathlib import Path

import pandas as pd
import json

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
    
    # Tu dong chon mo hinh theo Validation RMSE
    best_model_name = comparison.iloc[0]["model"]

    model_mapping = {
        "Linear Regression": {
            "model_type": "linear",
            "model_path": "models/candidates/linear_regression.joblib"
        },
        "SGDRegressor": {
            "model_type": "sgd",
            "model_path": "models/candidates/sgd_best.joblib"
        }
    }

    # Baseline khong phai model trien khai
    if best_model_name not in model_mapping:
        raise RuntimeError(
            "Mean Baseline dang tot nhat. "
            "Can phan tich ket qua truoc khi "
            "chon mo hinh de trien khai."
        )

    selected = model_mapping[best_model_name]

    model_path = ROOT_DIR / selected["model_path"]

    if not model_path.is_file():
        raise FileNotFoundError(
            f"Chua co model da huan luyen: {model_path}"
        )

    config = {
        **selected,
        "selection_metric": "RMSE",
        "selected_on": "validation",
        "random_state": 42
    }

    config_path = ROOT_DIR / "config" / "final_model.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print("\n===== FINAL MODEL SELECTED =====")
    print("Model:", best_model_name)
    print("Validation RMSE:", comparison.iloc[0]["RMSE"])
    print("Config:", config_path)


if __name__ == "__main__":
    main()