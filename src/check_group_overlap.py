
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "processed"

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


def get_groups(df, features):
    return set(
        df[features].itertuples(
            index=False,
            name=None
        )
    )


def main():
    train = pd.read_csv(DATA_DIR / "train.csv")
    validation = pd.read_csv(
        DATA_DIR / "validation.csv"
    )
    test = pd.read_csv(DATA_DIR / "test.csv")

    datasets = {
        "Train": train,
        "Validation": validation,
        "Test": test,
    }

    pairs = [
        ("Train", "Validation"),
        ("Train", "Test"),
        ("Validation", "Test"),
    ]

    for features, title in [
        (FEATURES_8, "NHOM THEO 8 BIEN"),
        (FEATURES_7, "NHOM THEO 7 THANH PHAN"),
    ]:
        print(f"\n===== {title} =====")

        for a, b in pairs:
            groups_a = get_groups(
                datasets[a], features
            )
            groups_b = get_groups(
                datasets[b], features
            )

            overlap = groups_a & groups_b

            print(
                f"{a} - {b}: "
                f"{len(overlap)} nhom trung"
            )


if __name__ == "__main__":
    main()
