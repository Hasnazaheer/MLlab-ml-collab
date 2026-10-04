"""Prepare stage: load raw data, split, clean and encode it.

Usage (from anywhere):
    python src/prepare.py

Reads data/raw/train.csv and writes data/processed/{train,test}.csv.
"""

import sys
from pathlib import Path

# Allow `python src/prepare.py` as well as `python -m src.prepare`
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sklearn.model_selection import train_test_split

from src.data import TEST_FILE, TRAIN_FILE, load_train
from src.features import TARGET, add_features, clean, encode
from src.params import load_params, set_seed
from src.paths import PROCESSED_DATA_DIR


def split_and_process(raw, test_size, seed):
    """Split labelled data, then clean and encode both parts.

    Splitting first means imputation and outlier limits are learned from
    the training part only. Returns (train, test) DataFrames that each
    hold the features plus the target column.
    """
    train_part, test_part = train_test_split(
        raw,
        test_size=test_size,
        random_state=seed,
        shuffle=True,
        stratify=raw[TARGET],
    )
    y_test = test_part[TARGET]

    train_part, test_part = clean(train_part, test_part)
    X_train, y_train, X_test, _ = encode(
        add_features(train_part), add_features(test_part)
    )
    return (
        X_train.assign(**{TARGET: y_train}),
        X_test.assign(**{TARGET: y_test}),
    )


def main():
    params = load_params()
    set_seed(params["seed"])

    raw = load_train()
    train, test = split_and_process(raw, params["split"]["test_size"], params["seed"])

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    train.to_csv(PROCESSED_DATA_DIR / TRAIN_FILE, index=False)
    test.to_csv(PROCESSED_DATA_DIR / TEST_FILE, index=False)
    print("Raw Shape:", raw.shape)
    print("Train Shape:", train.shape)
    print("Test Shape:", test.shape)
    print(f"Processed data written to: {PROCESSED_DATA_DIR}")


if __name__ == "__main__":
    main()
