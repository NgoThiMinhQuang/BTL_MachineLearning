
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT / "data" / "processed"

MODEL_PATH = (
    ROOT / "models" / "candidates"
    / "linear_regression.joblib"
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


def load_splits():
    train = pd.read_csv(DATA_DIR / "train.csv")
    validation = pd.read_csv(
        DATA_DIR / "validation.csv"
    )
    test = pd.read_csv(DATA_DIR / "test.csv")

    return train, validation, test


# ==========================================
# TEST 1: KHONG TRUNG NHOM GIUA CAC TAP
# ==========================================

def test_no_group_overlap():

    train, validation, test = load_splits()

    def group_ids(df):
        return set(
            pd.util.hash_pandas_object(
                df[FEATURES],
                index=False
            )
        )

    train_groups = group_ids(train)
    val_groups = group_ids(validation)
    test_groups = group_ids(test)

    assert train_groups.isdisjoint(val_groups)
    assert train_groups.isdisjoint(test_groups)
    assert val_groups.isdisjoint(test_groups)

    assert len(train) + len(validation) + len(test) == 1030


# ==========================================
# TEST 2: SCALER FIT TREN TRAIN
# ==========================================

def test_scaler_fitted_on_train():

    train, _, _ = load_splits()

    pipeline = joblib.load(MODEL_PATH)

    assert isinstance(pipeline, Pipeline)

    scaler = pipeline.named_steps["scaler"]
    model = pipeline.named_steps["model"]

    assert isinstance(scaler, StandardScaler)
    assert isinstance(model, LinearRegression)

    assert scaler.n_samples_seen_ == len(train)

    expected_mean = train[FEATURES].mean().to_numpy()

    np.testing.assert_allclose(
        scaler.mean_,
        expected_mean,
        rtol=1e-10,
        atol=1e-8
    )


# ==========================================
# TEST 3: TAI HUAN LUYEN CHO CUNG DU DOAN
# ==========================================

def test_linear_model_reproducibility():

    train, validation, _ = load_splits()

    X_train = train[FEATURES]
    y_train = train[TARGET]

    X_validation = validation[FEATURES]

    saved_pipeline = joblib.load(MODEL_PATH)

    new_pipeline = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("model", LinearRegression())
        ]
    )

    new_pipeline.fit(X_train, y_train)

    saved_predictions = saved_pipeline.predict(
        X_validation
    )

    new_predictions = new_pipeline.predict(
        X_validation
    )

    np.testing.assert_allclose(
        saved_predictions,
        new_predictions,
        rtol=1e-10,
        atol=1e-8
    )
