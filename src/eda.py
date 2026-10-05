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

    print(
        "\nDA TAO XONG CAC BIEU DO EDA."
    )

    print(
        "Thu muc:",
        FIGURE_DIR
    )


if __name__ == "__main__":
    main()