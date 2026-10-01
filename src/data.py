import pandas as pd


DATA_PATH = "data/raw/Concrete_Data.xls"


def load_data():
    df = pd.read_excel(DATA_PATH)
    return df


def rename_columns(df):
    df = df.copy()

    df.columns = [
        "cement",
        "slag",
        "fly_ash",
        "water",
        "superplasticizer",
        "coarse_aggregate",
        "fine_aggregate",
        "age",
        "strength"
    ]

    return df


if __name__ == "__main__":
    df = load_data()
    df = rename_columns(df)

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