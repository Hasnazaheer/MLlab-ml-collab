# MLLab ML Collaboration

## Team
- Member 1 — Data Owner
- Member 2 — Model Owner

## Dataset
Titanic Dataset

## Task
Binary Classification
### Review Notes

This section documents the review workflow used during Phase 7.
## Project
Git-based collaboration and reproducible machine learning pipeline using Git, DVC, and CI.

## Project Layout

```
pyproject.toml     Project metadata and dependencies
uv.lock            Exact locked versions of all dependencies
.python-version    Python version used by uv
params.yaml        Seed, split ratio and model hyperparameters
dvc.yaml           Pipeline definition: prepare -> train -> evaluate
dvc.lock           Exact hashes of the data, code and params of the last run
metrics.json       Metrics from the last run of the evaluate stage
data/raw/          Titanic train.csv and test.csv (tracked by DVC; see Setup)
data/processed/    Output of the prepare stage (tracked by DVC)
models/            Output of the train stage (tracked by DVC)
outputs/           Predictions from the evaluate stage (tracked by DVC)
notebooks/         Exploratory analysis
src/
  paths.py         Project-relative paths
  params.py        Loads params.yaml and sets random seeds
  data.py          Data loading and inspection
  features.py      Cleaning, imputation, feature engineering, encoding
  model.py         Model definition and scoring
  prepare.py       Stage 1: split, clean and encode the raw data
  train.py         Stage 2: fit the model
  evaluate.py      Stage 3: write predictions and metrics.json
tests/             Unit tests (run with `uv run pytest`)
```

## Setup

1. Install [uv](https://docs.astral.sh/uv/), then create the environment from the lock file:

   ```bash
   uv sync
   ```

   This creates `.venv/` with the Python version from `.python-version` and the exact
   package versions from `uv.lock`.

2. Add your own DagsHub credentials (stored locally, never committed) and download the data:

   ```bash
   uv run dvc remote modify origin --local auth basic
   uv run dvc remote modify origin --local user <your-dagshub-username>
   uv run dvc remote modify origin --local password <your-dagshub-token>
   uv run dvc pull
   ```

## Pipeline

```
prepare  ->  train  ->  evaluate
```

| Stage | Script | Reads | Writes |
|---|---|---|---|
| prepare | `src/prepare.py` | `data/raw/train.csv` | `data/processed/train.csv`, `data/processed/test.csv` |
| train | `src/train.py` | `data/processed/train.csv` | `models/model.pkl` |
| evaluate | `src/evaluate.py` | `models/model.pkl`, `data/processed/test.csv` | `outputs/predictions.csv`, `metrics.json` |

Run the whole pipeline:

```bash
uv run dvc repro
```

DVC only re-runs the stages whose code, data or parameters changed.

All hyperparameters, the split ratio and the seed live in `params.yaml`. To try a
different setting, edit that file and run `uv run dvc repro` again, then compare:

```bash
uv run dvc metrics show
uv run dvc params diff
uv run dvc metrics diff
```

The same seed is used for the train/test split, shuffling and model initialisation,
so everyone gets the same `metrics.json` from the same commit.

After a run, commit `dvc.lock` and `metrics.json`, and upload the outputs:

```bash
uv run dvc push
```
