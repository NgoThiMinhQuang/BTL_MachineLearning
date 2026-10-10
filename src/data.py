from pathlib import Path

import pandas as pd
import numpy as np

# ==========================================
# DUONG DAN PROJECT
# ==========================================

ROOT_DIR = Path(__file__).resolve().parents[1]

XLS_PATH = (
    ROOT_DIR
    / "data"
    / "raw"
    / "Concrete_Data.xls"
)

DOWNLOADED_CSV_PATH = (
    ROOT_DIR
    / "data"
    / "raw"
    / "Concrete_Data_downloaded.csv"
)


# ==========================================
# TEN COT CHUAN CUA PROJECT
# ==========================================

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


# ==========================================
# LOAD DATA
# ==========================================

def load_data():

    # Truong hop 1:
    # File XLS goc dang ton tai
    if XLS_PATH.exists():

        print(
            "Dang doc du lieu tu Concrete_Data.xls"
        )

        return pd.read_excel(
            XLS_PATH
        )

    # Truong hop 2:
    # Khong co XLS nhung da chay download_data.py
    if DOWNLOADED_CSV_PATH.exists():

        print(
            "Dang doc du lieu tu Concrete_Data_downloaded.csv"
        )

        return pd.read_csv(
            DOWNLOADED_CSV_PATH
        )

    # Khong tim thay du lieu
    raise FileNotFoundError(
        "\nKhong tim thay file du lieu.\n"
        "Hay chay lenh:\n"
        "python src/download_data.py"
    )


# ==========================================
# DOI TEN COT
# ==========================================


def rename_columns(df):
    import re

    df = df.copy()

    if df.shape[1] != len(COLUMN_NAMES):
        raise ValueError(
            f"Dataset phai co 9 cot, "
            f"nhung hien co {df.shape[1]} cot."
        )

    # Cac ten cot nguon duoc chap nhan theo dung thu tu.
    # Ho tro ten cot goc UCI va ten chuan cua project.
    expected_prefixes = [
        ("cement",),
        ("blast furnace slag", "slag"),
        ("fly ash",),
        ("water",),
        ("superplasticizer",),
        ("coarse aggregate",),
        ("fine aggregate",),
        ("age",),
        ("concrete compressive strength", "strength"),
    ]

    for index, (original, prefixes) in enumerate(
        zip(df.columns, expected_prefixes)
    ):
        name = re.sub(
            r"\s+", " ", str(original)
        ).strip().lower().replace("_", " ")

        valid = any(
            name == prefix
            or name.startswith(prefix + " ")
            or name.startswith(prefix + "(")
            for prefix in prefixes
        )

        if not valid:
            raise ValueError(
                f"Sai ten hoac thu tu cot {index + 1}: "
                f"{original!r}. "
                f"Can kiem tra lai schema du lieu nguon."
            )

    df.columns = COLUMN_NAMES

    return df


# ==========================================
# KIEM TRA SCHEMA DU LIEU
# ==========================================

def validate_schema(df):

    if list(df.columns) != COLUMN_NAMES:
        raise ValueError(
            "Schema khong dung danh sach cot yeu cau."
        )

    if df.empty:
        raise ValueError("Dataset khong duoc rong.")

    # Kiem tra kieu du lieu
    for column in COLUMN_NAMES:
        if not pd.api.types.is_numeric_dtype(df[column]):
            raise ValueError(
                f"Cot {column} phai la du lieu so."
            )

    # Kiem tra gia tri thieu
    if df[COLUMN_NAMES].isna().any().any():
        raise ValueError(
            "Dataset chua gia tri thieu."
        )

    # Kiem tra NaN, Infinity
    if not np.isfinite(
        df[COLUMN_NAMES].to_numpy(dtype=float)
    ).all():
        raise ValueError(
            "Dataset chua gia tri khong huu han."
        )

    # Kiem tra 8 feature khong am
    features = COLUMN_NAMES[:-1]

    if (df[features] < 0).any().any():
        raise ValueError(
            "Feature khong duoc mang gia tri am."
        )

    # Tuoi be tong phai la so nguyen duong
    if (
        (df["age"] <= 0).any()
        or (df["age"] % 1 != 0).any()
    ):
        raise ValueError(
            "Age phai la so nguyen duong."
        )

    # Cuong do nen phai duong
    if (df["strength"] <= 0).any():
        raise ValueError(
            "Strength phai lon hon 0."
        )

    return df

# ==========================================
# GET DATA
# ==========================================

def get_data():

    df = load_data()

    df = rename_columns(df)

    df = validate_schema(df)

    return df
# ==========================================
# CHAY TRUC TIEP
# ==========================================

def main():

    df = get_data()

    print(
        "\n===== 5 DONG DAU ====="
    )

    print(
        df.head()
    )

    print(
        "\n===== KICH THUOC ====="
    )

    print(
        df.shape
    )

    print(
        "\n===== TEN COT ====="
    )

    print(
        df.columns.tolist()
    )

    print(
        "\n===== MISSING VALUES ====="
    )

    print(
        df.isnull().sum()
    )

    print(
        "\n===== DUPLICATE ====="
    )

    print(
        df.duplicated().sum()
    )


if __name__ == "__main__":
    main()