"""Loading and inspecting the raw Titanic dataset."""

from pathlib import Path

import pandas as pd

from src.paths import RAW_DATA_DIR

TRAIN_FILE = "train.csv"
TEST_FILE = "test.csv"


def _require(data_dir, names):
    """Raise FileNotFoundError if any of the files in ``names`` are missing from ``data_dir``."""

    missing = [name for name in names if not (data_dir / name).is_file()]
    if missing:
        raise FileNotFoundError(
            f"Missing {', '.join(missing)} in {data_dir}. "
            "Run `dvc pull` to download the Titanic dataset into data/raw/."
        )


def load_train(data_dir=RAW_DATA_DIR):
    """Return the labelled Titanic DataFrame read from ``data_dir``."""
    data_dir = Path(data_dir)
    _require(data_dir, [TRAIN_FILE])
    return pd.read_csv(data_dir / TRAIN_FILE)


def load_raw(data_dir=RAW_DATA_DIR):
    """Return (train, test) DataFrames read from ``data_dir``."""
    data_dir = Path(data_dir)
    _require(data_dir, [TRAIN_FILE, TEST_FILE])
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
