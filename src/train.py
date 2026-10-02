"""Train the Titanic survival model and write a submission CSV.

Usage (from anywhere):
    python src/train.py [--data-dir DIR] [--output PATH]
"""

import argparse
import sys
from pathlib import Path

# Allow `python src/train.py` as well as `python -m src.train`
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd

from src.data import load_raw, missing_summary
from src.features import preprocess
from src.model import evaluate, fit_full
from src.paths import OUTPUT_DIR, RAW_DATA_DIR


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=RAW_DATA_DIR,
        help="Directory containing train.csv and test.csv (default: data/raw)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_DIR / "submission.csv",
        help="Submission CSV path (default: outputs/submission.csv)",
    )
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--random-state", type=int, default=42)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    train, test = load_raw(args.data_dir)
    print("Train Shape:", train.shape)
    print("Test Shape:", test.shape)
    print("\nMissing Analysis:\n", missing_summary(train))

    X, y, X_test, test_ids = preprocess(train, test)

    scores = evaluate(X, y, args.test_size, args.random_state)
    print(scores["report"])
    print("ROC-AUC:", scores["roc_auc"])

    model = fit_full(X, y)
    submission = pd.DataFrame(
        {
            "PassengerId": test_ids,
            "Survived": model.predict(X_test).astype(int),
        }
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    submission.to_csv(args.output, index=False)
    print(f"Submission file created: {args.output}")


if __name__ == "__main__":
    main()
