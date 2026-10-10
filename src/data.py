from pathlib import Path

import pandas as pd


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

    df = df.copy()

    if df.shape[1] != len(
        COLUMN_NAMES
    ):

        raise ValueError(
            (
                "Dataset phai co 9 cot, "
                f"nhung hien co {df.shape[1]} cot."
            )
        )

    df.columns = COLUMN_NAMES

    return df


# ==========================================
# GET DATA
# ==========================================

def get_data():

    df = load_data()

    df = rename_columns(
        df
    )

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