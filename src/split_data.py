from pathlib import Path

import pandas as pd
from sklearn.model_selection import GroupShuffleSplit

from data import get_data


# =============================
# CAC DUONG DAN
# =============================

ROOT_DIR = Path(__file__).resolve().parents[1]

OUTPUT_DIR = ROOT_DIR / "data" / "processed"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =============================
# CAC BIEN DAU VAO
# =============================

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


# =============================
# TAO GROUP
# =============================

def create_group_id(df):
    """
    Tao ID nhom dua tren 8 bien dau vao.

    Nhung dong co cung 8 bien dau vao
    se duoc xem la cung mot nhom.

    Viec nay giup tranh mot mau giong nhau
    xuat hien o ca train va test.
    """

    group_id = pd.util.hash_pandas_object(
        df[FEATURES],
        index=False
    )

    return group_id.astype(str)


# =============================
# CHIA DU LIEU
# =============================

def split_data(df):

    df = df.copy()

    groups = create_group_id(df)

    # ---------------------------------
    # Lan 1:
    #
    # 85% -> train + validation
    # 15% -> test
    # ---------------------------------

    split_test = GroupShuffleSplit(
        n_splits=1,
        test_size=0.15,
        random_state=RANDOM_STATE
    )

    train_val_index, test_index = next(
        split_test.split(
            df,
            groups=groups
        )
    )

    train_val = df.iloc[
        train_val_index
    ].copy()

    test = df.iloc[
        test_index
    ].copy()

    train_val_groups = groups.iloc[
        train_val_index
    ].reset_index(drop=True)

    train_val = train_val.reset_index(
        drop=True
    )

    test = test.reset_index(
        drop=True
    )

    # ---------------------------------
    # Lan 2:
    #
    # Tach validation khoi train_val
    #
    # 15 / 85 = 0.1765
    # ---------------------------------

    split_validation = GroupShuffleSplit(
        n_splits=1,
        test_size=0.1765,
        random_state=RANDOM_STATE
    )

    train_index, validation_index = next(
        split_validation.split(
            train_val,
            groups=train_val_groups
        )
    )

    train = train_val.iloc[
        train_index
    ].copy()

    validation = train_val.iloc[
        validation_index
    ].copy()

    train = train.reset_index(
        drop=True
    )

    validation = validation.reset_index(
        drop=True
    )

    return train, validation, test


# =============================
# KIEM TRA LEAKAGE
# =============================

def check_leakage(train, validation, test):

    train_groups = set(
        create_group_id(train)
    )

    validation_groups = set(
        create_group_id(validation)
    )

    test_groups = set(
        create_group_id(test)
    )

    train_validation_overlap = (
        train_groups.intersection(
            validation_groups
        )
    )

    train_test_overlap = (
        train_groups.intersection(
            test_groups
        )
    )

    validation_test_overlap = (
        validation_groups.intersection(
            test_groups
        )
    )

    print("\n===== KIEM TRA LEAKAGE =====")

    print(
        "Train - Validation overlap:",
        len(train_validation_overlap)
    )

    print(
        "Train - Test overlap:",
        len(train_test_overlap)
    )

    print(
        "Validation - Test overlap:",
        len(validation_test_overlap)
    )

    if (
        len(train_validation_overlap) == 0
        and len(train_test_overlap) == 0
        and len(validation_test_overlap) == 0
    ):

        print(
            "\nKHONG PHAT HIEN LEAKAGE "
            "GIUA CAC TAP."
        )

    else:

        print(
            "\nCAN KIEM TRA LAI "
            "CACH CHIA DU LIEU."
        )


# =============================
# MAIN
# =============================

def main():

    df = get_data()

    train, validation, test = split_data(df)

    print(
        "===== KICH THUOC CAC TAP ====="
    )

    print(
        "Tong du lieu:",
        len(df)
    )

    print(
        "Train:",
        len(train)
    )

    print(
        "Validation:",
        len(validation)
    )

    print(
        "Test:",
        len(test)
    )

    print(
        "\nTong sau khi chia:",
        len(train)
        + len(validation)
        + len(test)
    )

    check_leakage(
        train,
        validation,
        test
    )

    # Luu file

    train.to_csv(
        OUTPUT_DIR / "train.csv",
        index=False
    )

    validation.to_csv(
        OUTPUT_DIR / "validation.csv",
        index=False
    )

    test.to_csv(
        OUTPUT_DIR / "test.csv",
        index=False
    )

    print(
        "\n===== DA LUU DU LIEU ====="
    )

    print(
        OUTPUT_DIR / "train.csv"
    )

    print(
        OUTPUT_DIR / "validation.csv"
    )

    print(
        OUTPUT_DIR / "test.csv"
    )


if __name__ == "__main__":
    main()