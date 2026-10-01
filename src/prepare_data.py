from pathlib import Path
from data import load_data, rename_columns


REPORT_DIR = Path("reports/tables")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    # 1. Doc du lieu goc
    df = load_data()
    df = rename_columns(df)

    # 2. Tim tat ca cac dong nam trong nhom trung lap
    duplicate_rows = df[df.duplicated(keep=False)]

    print("===== TONG SO DONG =====")
    print(len(df))

    print("\n===== SO DONG TRUNG LAP =====")
    print(df.duplicated().sum())

    print("\n===== CAC DONG THUOC NHOM TRUNG LAP =====")
    print(duplicate_rows.to_string())

    # 3. Luu danh sach duplicate de lam minh chung
    duplicate_rows.to_csv(
        REPORT_DIR / "duplicate_rows.csv",
        index=True
    )

    print(
        "\nDa luu bao cao duplicate tai:"
        " reports/tables/duplicate_rows.csv"
    )


if __name__ == "__main__":
    main()