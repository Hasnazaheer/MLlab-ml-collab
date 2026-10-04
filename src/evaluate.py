"""Evaluate stage: score the trained model on the held-out test split.

Usage (from anywhere):
    python src/evaluate.py

Reads models/model.pkl and data/processed/test.csv, and writes
outputs/predictions.csv and metrics.json.
"""

import json
import pickle
import sys
from pathlib import Path

# Allow `python src/evaluate.py` as well as `python -m src.evaluate`
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd

from src.data import TEST_FILE
from src.features import TARGET
from src.model import score
from src.params import load_params, set_seed
from src.paths import METRICS_FILE, MODEL_FILE, PREDICTIONS_FILE, PROCESSED_DATA_DIR


def main():
    params = load_params()
    set_seed(params["seed"])

    test = pd.read_csv(PROCESSED_DATA_DIR / TEST_FILE)
    X, y = test.drop(columns=TARGET), test[TARGET]
    with open(MODEL_FILE, "rb") as f:
        model = pickle.load(f)

    y_pred = model.predict(X)
    y_proba = model.predict_proba(X)[:, 1]

    predictions = pd.DataFrame(
        {
            TARGET: y,
            "Predicted": y_pred.astype(int),
            "Probability": y_proba,
        }
    )
    PREDICTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    predictions.to_csv(PREDICTIONS_FILE, index=False)

    metrics = score(y, y_pred, y_proba)
    with open(METRICS_FILE, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
        f.write("\n")

    for name, value in metrics.items():
        print(f"{name}: {value:.4f}")
    print(f"Predictions written to: {PREDICTIONS_FILE}")
    print(f"Metrics written to: {METRICS_FILE}")


if __name__ == "__main__":
    main()
