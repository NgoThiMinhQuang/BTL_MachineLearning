
from pathlib import Path

import pandas as pd
from ucimlrepo import fetch_ucirepo

from data import rename_columns, validate_schema


# =====================================
# 1. DUONG DAN PROJECT
# =====================================

ROOT_DIR = Path(__file__).resolve().parents[1]

RAW_DIR = ROOT_DIR / "data" / "raw"

OUTPUT_PATH = (
    RAW_DIR / "Concrete_Data_downloaded.csv"
)

RAW_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =====================================
# 2. TAI VA KIEM TRA DU LIEU UCI
# =====================================

def main():

    print(
        "Dang tai Concrete Compressive Strength Dataset..."
    )

    # Dataset UCI ID = 165
    dataset = fetch_ucirepo(id=165)

    # Lay 8 bien dau vao
    X = dataset.data.features.copy()

    # Lay bien muc tieu
    y = dataset.data.targets.copy()

    # Ghep du lieu
    df = pd.concat(
        [X, y],
        axis=1
    )

    print("\n===== DU LIEU GOC =====")

    print("So dong:", len(df))
    print("So cot:", df.shape[1])

    print("\nTen cot goc:")
    print(df.columns.tolist())

    # =====================================
    # 3. KIEM TRA KICH THUOC
    # =====================================

    if len(df) != 1030:
        raise ValueError(
            f"So dong khong mong doi: {len(df)}"
        )

    if df.shape[1] != 9:
        raise ValueError(
            f"So cot khong mong doi: {df.shape[1]}"
        )

    # =====================================
    # 4. KIEM TRA TEN VA THU TU COT
    # =====================================

    # Khong doi ten cot theo vi tri mot cach
    # truc tiep khi chua kiem tra cot nguon.

    df = rename_columns(df)

    # =====================================
    # 5. KIEM TRA SCHEMA
    # =====================================

    df = validate_schema(df)

    print("\n===== SCHEMA VALIDATION =====")

    print("So dong hop le:", len(df))
    print("So cot hop le:", df.shape[1])

    print("\nTen cot sau chuan hoa:")
    print(df.columns.tolist())

    # =====================================
    # 6. LUU FILE CSV
    # =====================================

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print("\n===== DOWNLOAD SUCCESS =====")

    print("So dong:", len(df))
    print("So cot:", df.shape[1])

    print("\nFile da luu:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()
