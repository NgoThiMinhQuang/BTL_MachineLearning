from pathlib import Path

import pandas as pd
from ucimlrepo import fetch_ucirepo


ROOT_DIR = Path(__file__).resolve().parents[1]

RAW_DIR = (
    ROOT_DIR
    / "data"
    / "raw"
)

OUTPUT_PATH = (
    RAW_DIR
    / "Concrete_Data_downloaded.csv"
)

RAW_DIR.mkdir(
    parents=True,
    exist_ok=True
)


COLUMN_NAMES = [
    "cement",
    "slag",
    "fly_ash",
    "water",
    "superplasticizer",
    "coarse_aggregate",
    "fine_aggregate",
    "age",
    "strength",
]


def main():

    print(
        "Dang tai Concrete Compressive Strength Dataset..."
    )

    # Dataset Concrete Compressive Strength
    # tren UCI co ID = 165
    dataset = fetch_ucirepo(
        id=165
    )

    # 8 feature
    X = (
        dataset
        .data
        .features
        .copy()
    )

    # Target strength
    y = (
        dataset
        .data
        .targets
        .copy()
    )

    # Ghep feature va target
    df = pd.concat(
        [
            X,
            y
        ],
        axis=1
    )

    # Kiem tra so dong
    if len(df) != 1030:

        raise ValueError(
            f"So dong khong mong doi: {len(df)}"
        )

    # Kiem tra so cot
    if df.shape[1] != 9:

        raise ValueError(
            f"So cot khong mong doi: {df.shape[1]}"
        )

    # Dat ten cot thong nhat voi project
    df.columns = COLUMN_NAMES

    # Luu file
    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(
        "\n===== DOWNLOAD SUCCESS ====="
    )

    print(
        "So dong:",
        len(df)
    )

    print(
        "So cot:",
        df.shape[1]
    )

    print(
        "File:"
    )

    print(
        OUTPUT_PATH
    )


if __name__ == "__main__":
    main()