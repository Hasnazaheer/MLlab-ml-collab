"""Project paths, resolved relative to the repository root.

Nothing here depends on the current working directory or on any one
machine's layout, so the same code works on every teammate's computer.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = PROJECT_ROOT / "models"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

PARAMS_FILE = PROJECT_ROOT / "params.yaml"
MODEL_FILE = MODELS_DIR / "model.pkl"
PREDICTIONS_FILE = OUTPUT_DIR / "predictions.csv"
METRICS_FILE = PROJECT_ROOT / "metrics.json"
