# MLLab ML Collaboration

## Team
- Member 1 — Data Owner
- Member 2 — Model Owner

## Dataset
Titanic Dataset

## Task
Binary Classification

## Project
Git-based collaboration and reproducible machine learning pipeline using Git, DVC, and CI.

## Project Layout

```
pyproject.toml     Project metadata and dependencies
uv.lock            Exact locked versions of all dependencies
.python-version    Python version used by uv
data/raw/          Titanic train.csv and test.csv (not committed; see Setup)
src/
  paths.py         Project-relative paths
  data.py          Data loading and inspection
  features.py      Cleaning, imputation, feature engineering, encoding
  model.py         Model definition, validation, final fit
  train.py         Command-line training entry point
outputs/           Generated submission files (not committed)
```

## Setup

1. Install [uv](https://docs.astral.sh/uv/), then create the environment from the lock file:

   ```bash
   uv sync
   ```

   This creates `.venv/` with the Python version from `.python-version` and the exact
   package versions from `uv.lock`.

2. Download the [Kaggle Titanic dataset](https://www.kaggle.com/c/titanic/data) and place
   `train.csv` and `test.csv` in `data/raw/`.

## Train

```bash
uv run python src/train.py
```

This prints validation metrics and writes `outputs/submission.csv`.
Run `uv run python src/train.py --help` for options (`--data-dir`, `--output`, `--test-size`, `--random-state`).
