from pathlib import Path
import pandas as pd


# Thu muc goc cua project
ROOT_DIR = Path(__file__).resolve().parents[1]

# Duong dan den file du lieu goc
DATA_PATH = ROOT_DIR / "data" / "raw" / "Concrete_Data.xls"


# Ten cac cot su dung trong toan bo project
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


def load_data():
    """
    Doc bo du lieu goc Concrete Compressive Strength.
    """
    df = pd.read_excel(DATA_PATH)
    return df


def rename_columns(df):
    """
    Doi ten cot goc thanh ten ngan gon de su dung trong code.
    """
    df = df.copy()

    df.columns = COLUMN_NAMES

    return df


def get_data():
    """
    Tra ve bo du lieu da duoc doi ten cot.
    """
    df = load_data()

    df = rename_columns(df)

    return df


if __name__ == "__main__":

    df = get_data()

    print("===== 5 DONG DAU TIEN =====")
    print(df.head())

    print("\n===== KICH THUOC DU LIEU =====")
    print(df.shape)

    print("\n===== TEN CAC COT =====")
    print(df.columns.tolist())

    print("\n===== THONG TIN DU LIEU =====")
    df.info()

    print("\n===== THONG KE MO TA =====")
    print(df.describe())

    print("\n===== GIA TRI THIEU =====")
    print(df.isnull().sum())

    print("\n===== SO DONG TRUNG LAP =====")
    print(df.duplicated().sum())