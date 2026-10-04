"""Train stage: fit the model on the prepared training data.

Usage (from anywhere):
    python src/train.py

Reads data/processed/train.csv and writes models/model.pkl.
Model type and hyperparameters come from params.yaml.
"""

import pickle
import sys
from pathlib import Path

# Allow `python src/train.py` as well as `python -m src.train`
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd

from src.data import TRAIN_FILE
from src.features import TARGET
from src.model import build_model
from src.params import load_params, set_seed
from src.paths import MODEL_FILE, PROCESSED_DATA_DIR


def main():
    params = load_params()
    set_seed(params["seed"])

    train = pd.read_csv(PROCESSED_DATA_DIR / TRAIN_FILE)
    X, y = train.drop(columns=TARGET), train[TARGET]

    model = build_model(seed=params["seed"], **params["train"]).fit(X, y)

    MODEL_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MODEL_FILE, "wb") as f:
        pickle.dump(model, f)
    print("Train Shape:", X.shape)
    print("Model:", model)
    print(f"Model written to: {MODEL_FILE}")


if __name__ == "__main__":
    main()
