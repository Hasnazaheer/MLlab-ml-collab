"""Loading and inspecting the raw Titanic dataset."""

from pathlib import Path

import pandas as pd

from src.paths import RAW_DATA_DIR

TRAIN_FILE = "train.csv"
TEST_FILE = "test.csv"


def load_raw(data_dir=RAW_DATA_DIR):
    """Return (train, test) DataFrames read from ``data_dir``."""
    data_dir = Path(data_dir)
    missing = [
        name for name in (TRAIN_FILE, TEST_FILE) if not (data_dir / name).is_file()
    ]
    if missing:
        raise FileNotFoundError(
            f"Missing {', '.join(missing)} in {data_dir}. "
            "Download the Titanic dataset (Kaggle: titanic) and place "
            f"{TRAIN_FILE} and {TEST_FILE} in data/raw/."
        )
    return pd.read_csv(data_dir / TRAIN_FILE), pd.read_csv(data_dir / TEST_FILE)


def missing_summary(df):
    """Count and percentage of missing values for columns that have any."""
    counts = df.isnull().sum()
    summary = pd.DataFrame(
        {
            "Missing_Count": counts,
            "Missing_%": counts / len(df) * 100,
        }
    )
    return summary[summary["Missing_Count"] > 0]
