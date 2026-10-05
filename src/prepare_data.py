from pathlib import Path

from data import load_data, rename_columns


ROOT_DIR = Path(__file__).resolve().parents[1]

REPORT_DIR = (
    ROOT_DIR
    / "reports"
    / "tables"
)

REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def main():

    df = load_data()

    df = rename_columns(df)

    # Tim tat ca cac dong nam trong nhom duplicate hoan toan
    duplicate_rows = df[
        df.duplicated(
            keep=False
        )
    ]

    duplicate_count = (
        df.duplicated().sum()
    )

    print(
        "===== TONG SO DONG ====="
    )

    print(len(df))

    print(
        "\n===== SO BAN GHI DUPLICATE ====="
    )

    print(duplicate_count)

    print(
        "\n===== SO DONG THUOC CAC NHOM DUPLICATE ====="
    )

    print(len(duplicate_rows))

    print(
        "\n===== CAC DONG DUPLICATE ====="
    )

    print(
        duplicate_rows.to_string()
    )

    duplicate_rows.to_csv(
        REPORT_DIR
        / "duplicate_rows.csv",
        index=True,
        index_label="original_index"
    )

    print(
        "\nDa luu tai:"
    )

    print(
        REPORT_DIR
        / "duplicate_rows.csv"
    )


if __name__ == "__main__":
    main()