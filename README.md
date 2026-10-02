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
data/raw/          Titanic train.csv and test.csv (not committed; see Setup)
notebooks/         Exploration notebook (imports code from src/)
src/
  paths.py         Project-relative paths
  data.py          Data loading and inspection
  features.py      Cleaning, imputation, feature engineering, encoding
  model.py         Model definition, validation, final fit
  train.py         Command-line training entry point
outputs/           Generated submission files (not committed)
```

## Setup

1. Create an environment and install dependencies with [uv](https://docs.astral.sh/uv/):

   ```bash
   uv venv
   uv pip install -r requirements.txt
   ```

2. Download the [Kaggle Titanic dataset](https://www.kaggle.com/c/titanic/data) and place
   `train.csv` and `test.csv` in `data/raw/`.

## Train

```bash
uv run python src/train.py
```

This prints validation metrics and writes `outputs/submission.csv`.
Run `python src/train.py --help` for options (`--data-dir`, `--output`, `--test-size`, `--random-state`).
