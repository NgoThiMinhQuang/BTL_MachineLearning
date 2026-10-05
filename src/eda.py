from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# ==========================================
# DUONG DAN
# ==========================================

ROOT_DIR = Path(__file__).resolve().parents[1]

TRAIN_PATH = (
    ROOT_DIR
    / "data"
    / "processed"
    / "train.csv"
)

FIGURE_DIR = (
    ROOT_DIR
    / "reports"
    / "figures"
)

FIGURE_DIR.mkdir(
    parents=True,
    exist_ok=True
)
TABLE_DIR = (
    ROOT_DIR
    / "reports"
    / "tables"
)

TABLE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# ==========================================
# DOC TAP TRAIN
# ==========================================

def load_train_data():

    df = pd.read_csv(TRAIN_PATH)

    return df


# ==========================================
# BIEU DO PHAN BO STRENGTH
# ==========================================

def plot_strength_distribution(df):

    plt.figure(figsize=(8, 5))

    plt.hist(
        df["strength"],
        bins=30,
        edgecolor="black"
    )

    plt.xlabel(
        "Concrete compressive strength (MPa)"
    )

    plt.ylabel("Frequency")

    plt.title(
        "Distribution of Concrete Compressive Strength"
    )

    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR
        / "strength_distribution.png",
        dpi=300
    )

    plt.close()


# ==========================================
# AGE VA STRENGTH
# ==========================================

def plot_age_vs_strength(df):

    plt.figure(figsize=(8, 5))

    plt.scatter(
        df["age"],
        df["strength"],
        alpha=0.6
    )

    plt.xlabel("Age (days)")

    plt.ylabel(
        "Concrete compressive strength (MPa)"
    )

    plt.title(
        "Age vs Concrete Compressive Strength"
    )

    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR
        / "age_vs_strength.png",
        dpi=300
    )

    plt.close()


# ==========================================
# CEMENT VA STRENGTH
# ==========================================

def plot_cement_vs_strength(df):

    plt.figure(figsize=(8, 5))

    plt.scatter(
        df["cement"],
        df["strength"],
        alpha=0.6
    )

    plt.xlabel("Cement (kg/m3)")

    plt.ylabel(
        "Concrete compressive strength (MPa)"
    )

    plt.title(
        "Cement vs Concrete Compressive Strength"
    )

    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR
        / "cement_vs_strength.png",
        dpi=300
    )

    plt.close()


# ==========================================
# WATER VA STRENGTH
# ==========================================

def plot_water_vs_strength(df):

    plt.figure(figsize=(8, 5))

    plt.scatter(
        df["water"],
        df["strength"],
        alpha=0.6
    )

    plt.xlabel("Water (kg/m3)")

    plt.ylabel(
        "Concrete compressive strength (MPa)"
    )

    plt.title(
        "Water vs Concrete Compressive Strength"
    )

    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR
        / "water_vs_strength.png",
        dpi=300
    )

    plt.close()

def plot_correlation_matrix(df):

    correlation = df.corr(
        numeric_only=True
    )

    fig, ax = plt.subplots(
        figsize=(10, 8)
    )

    image = ax.imshow(
        correlation.values
    )

    columns = correlation.columns

    ax.set_xticks(
        range(len(columns))
    )

    ax.set_yticks(
        range(len(columns))
    )

    ax.set_xticklabels(
        columns,
        rotation=45,
        ha="right"
    )

    ax.set_yticklabels(
        columns
    )

    for i in range(
        len(columns)
    ):

        for j in range(
            len(columns)
        ):

            ax.text(
                j,
                i,
                f"{correlation.iloc[i, j]:.2f}",
                ha="center",
                va="center"
            )

    fig.colorbar(
        image,
        ax=ax
    )

    ax.set_title(
        "Correlation Matrix - Train Set"
    )

    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR
        / "correlation_matrix.png",
        dpi=300
    )

    plt.close()


def save_iqr_outlier_summary(df):

    results = []

    numeric_columns = (
        df.select_dtypes(
            include="number"
        ).columns
    )

    for column in numeric_columns:

        q1 = df[column].quantile(
            0.25
        )

        q3 = df[column].quantile(
            0.75
        )

        iqr = q3 - q1

        lower_bound = (
            q1 - 1.5 * iqr
        )

        upper_bound = (
            q3 + 1.5 * iqr
        )

        outlier_count = (
            (
                (df[column] < lower_bound)
                |
                (df[column] > upper_bound)
            )
            .sum()
        )

        results.append(
            {
                "variable": column,
                "Q1": q1,
                "Q3": q3,
                "IQR": iqr,
                "lower_bound":
                    lower_bound,
                "upper_bound":
                    upper_bound,
                "outlier_count":
                    outlier_count,
            }
        )

    result_df = pd.DataFrame(
        results
    )

    result_df.to_csv(
        TABLE_DIR
        / "iqr_outlier_summary.csv",
        index=False
    )

    return result_df
# ==========================================
# CHUONG TRINH CHINH
# ==========================================

def main():

    df = load_train_data()

    print(
        "===== KICH THUOC TAP TRAIN ====="
    )

    print(df.shape)

    print(
        "\n===== 5 DONG DAU TIEN ====="
    )

    print(df.head())

    print(
        "\n===== THONG KE MO TA ====="
    )

    print(df.describe())

    print(
        "\n===== TUONG QUAN VOI STRENGTH ====="
    )

    correlation = (
        df.corr(numeric_only=True)["strength"]
        .sort_values(ascending=False)
    )

    print(correlation)

    plot_strength_distribution(df)

    plot_age_vs_strength(df)

    plot_cement_vs_strength(df)

    plot_water_vs_strength(df)

    plot_correlation_matrix(df)

    iqr_summary = (
        save_iqr_outlier_summary(
        df
        )
    )

    print(
        "\n===== IQR OUTLIER SUMMARY ====="
    )

    print(
        iqr_summary.to_string(
            index=False
        )
    )

    print(
        "\nDA TAO XONG CAC BIEU DO EDA."
    )

    print(
        "Thu muc:",
        FIGURE_DIR
    )


if __name__ == "__main__":
    main()