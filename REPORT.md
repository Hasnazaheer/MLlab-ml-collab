# MLLab ML Collaboration — Final Report

Repository: https://github.com/Hasnazaheer/MLlab-ml-collab
DVC remote (DagsHub): https://dagshub.com/hasnazaheer861/MLlab-ml-collab
Release tag: `model-v1.0`

## 1. Team members and roles

| Member | GitHub | Role | Main responsibilities |
|---|---|---|---|
| Hasna Zaheer | `Hasnazaheer` | Data Owner | Repository setup, DVC and DagsHub, dataset versions, EDA, CI |
| Muhammad Tayyab | `tyb01` | Model Owner | Code refactor, environment, model pipeline, parameters, experiments, release tag |

## 2. Dataset and source

- **Dataset:** Titanic passenger survival (binary classification, target `Survived`).
- **Source:** Kaggle "Titanic - Machine Learning from Disaster",
  https://www.kaggle.com/c/titanic/data
- **Storage:** the CSV files are tracked with DVC and stored on DagsHub. Git holds
  only the pointer files `data/raw/train.csv.dvc` and `data/raw/test.csv.dvc`.

| Version | Rows | Change |
|---|---|---|
| v1 | 891 | Original Kaggle `train.csv` |
| v2 (released) | 889 | 2 rows with missing `Embarked` removed |

`data/raw/test.csv` (418 rows) is the unlabelled Kaggle test file. It is tracked but
not used by the pipeline, because it has no target to score against.

## 3. Pipeline

Defined in `dvc.yaml` and run with `uv run dvc repro`.

| Stage | Script | Input | Output |
|---|---|---|---|
| prepare | `src/prepare.py` | `data/raw/train.csv` | `data/processed/train.csv` (711 rows), `data/processed/test.csv` (178 rows) |
| train | `src/train.py` | `data/processed/train.csv` | `models/model.pkl` |
| evaluate | `src/evaluate.py` | model, `data/processed/test.csv` | `outputs/predictions.csv`, `metrics.json` |

- **Parameters:** all in `params.yaml` (`seed`, `split.test_size`, `train.model`,
  `train.n_estimators`, `train.max_depth`).
- **Seeds:** seed 42 is used for the stratified train/test split, the model's
  `random_state`, and Python's and NumPy's global generators in every stage.
- **Leakage prevention:** the data is split first. The Fare outlier cap, the Age and
  Fare medians and the Embarked mode are computed on the training split only and then
  applied to both splits. One-hot columns are taken from the training split.
- **Traceability:** `metrics.json` records the Git commit the run was made from.

## 4. Released model and final metrics

| Setting | Value |
|---|---|
| Model | Random Forest |
| `n_estimators` | 50 |
| `max_depth` | 10 |
| `seed` | 42 |
| `split.test_size` | 0.2 (stratified) |
| Dataset | v2 |

`metrics.json` on `main`:

| Metric | Value |
|---|---|
| accuracy | 0.7921348314606742 |
| precision | 0.7313432835820896 |
| recall | 0.7205882352941176 |
| f1 | 0.725925925925926 |
| roc_auc | 0.8064839572192513 |

## 5. Reproducibility table

The released configuration was run by both members. All metric values match exactly.

| Run | By | accuracy | precision | recall | f1 | roc_auc |
|---|---|---|---|---|---|---|
| Model Owner's run | Tayyab | 0.7921348314606742 | 0.7313432835820896 | 0.7205882352941176 | 0.725925925925926 | 0.8064839572192513 |
| Fresh clone of `staging` | Hasna | 0.7921348314606742 | 0.7313432835820896 | 0.7205882352941176 | 0.725925925925926 | 0.8064839572192513 |
| Released on `main` | — | 0.7921348314606742 | 0.7313432835820896 | 0.7205882352941176 | 0.725925925925926 | 0.8064839572192513 |

Steps used for the fresh reproduction:

```bash
git clone https://github.com/Hasnazaheer/MLlab-ml-collab.git
cd MLlab-ml-collab
git checkout staging
uv sync
uv run dvc pull
uv run dvc repro
```

## 6. Experiment comparison

### 6.1 `n_estimators` (Tayyab)

Run with `dvc exp run --set-param train.n_estimators=<n>`. Dataset v1, `max_depth` 6,
seed 42.

| Experiment | n_estimators | accuracy | precision | recall | f1 | roc_auc | Outcome |
|---|---|---|---|---|---|---|---|
| baseline | 100 | 0.8324 | 0.8197 | 0.7246 | 0.7692 | 0.8524 | Replaced |
| `tayyab-n-est-50` | 50 | 0.8324 | 0.8095 | 0.7391 | 0.7727 | 0.8514 | **Winner** (PR #10) |
| `tayyab-n-est-200` | 200 | 0.8324 | 0.8305 | 0.7101 | 0.7656 | 0.8504 | Abandoned |
| `tayyab-n-est-300` | 300 | 0.8324 | 0.8305 | 0.7101 | 0.7656 | 0.8478 | Abandoned |

### 6.2 `max_depth` (Hasna and Tayyab)

| max_depth | By | PR |
|---|---|---|
| 6 | baseline | #9 |
| 8 | Hasna | #13 |
| 10 (released) | Tayyab | #12 |

### 6.3 Pipeline runs recorded in the repository

| PR | Dataset | n_estimators | max_depth | accuracy | precision | recall | f1 | roc_auc |
|---|---|---|---|---|---|---|---|---|
| #9 | v1 | 100 | 6 | 0.8324 | 0.8197 | 0.7246 | 0.7692 | 0.8524 |
| #10 | v1 | 50 | 6 | 0.8324 | 0.8095 | 0.7391 | 0.7727 | 0.8514 |
| #11 | v2 | 100 | 6 | 0.8146 | 0.7966 | 0.6912 | 0.7402 | 0.8381 |
| #18 | v2 | 50 | 10 | 0.7921 | 0.7313 | 0.7206 | 0.7259 | 0.8065 |

## 7. Why the winner was selected

**`n_estimators` = 50.** All four settings reached the same accuracy (0.8324). 50 trees
gave the best F1 (0.7727) and the best recall (0.7391), with ROC-AUC within 0.001 of the
baseline, and it is the smallest and fastest model. Finding survivors (recall) matters
more than a slightly higher precision, so 50 was merged in PR #10.

**`max_depth` = 10.** This was the last `max_depth` change merged into `dev`, after
`max_depth` 8. The released configuration (`n_estimators` 50, `max_depth` 10) scores
lower on dataset v2 than the earlier run with `n_estimators` 100 and `max_depth` 6
(accuracy 0.7921 against 0.8146). We discuss this in the retrospective.

## 8. Required PR links

### Data-update PR

- PR #11, `data/update-dataset` → `dev`:
  https://github.com/Hasnazaheer/MLlab-ml-collab/pull/11
- Removed the 2 rows with missing `Embarked`; `train.csv` went from 891 to 889 rows.

### Conflict PR

- PR #11: https://github.com/Hasnazaheer/MLlab-ml-collab/pull/11
- The data branch and the `n_estimators` experiment (PR #10) both changed `dvc.lock`
  and `metrics.json`. Hasna merged `dev` into the data branch and resolved the conflict
  there.

Other PRs with conflicts:
[#8](https://github.com/Hasnazaheer/MLlab-ml-collab/pull/8)
(`.gitignore`, `pyproject.toml`, `uv.lock`) and
[#4](https://github.com/Hasnazaheer/MLlab-ml-collab/pull/4)
(`pyproject.toml`, `uv.lock`).

### Changes-requested review

- PR #16, `fix/gitignore` → `dev`:
  https://github.com/Hasnazaheer/MLlab-ml-collab/pull/16
- Opened by Tayyab and reviewed by Hasna, who requested changes. Tayyab pushed the
  requested fix and Hasna then approved and merged it.

### Release PRs

| PR | Direction | Link |
|---|---|---|
| #20 | `dev` → `staging` | https://github.com/Hasnazaheer/MLlab-ml-collab/pull/20 |
| #21 | `staging` → `main` | https://github.com/Hasnazaheer/MLlab-ml-collab/pull/21 |

Tag `model-v1.0` ("First production model") was created on `main` after PR #21.

## 9. Abandoned experiment

`tayyab-n-est-200` and `tayyab-n-est-300` were run and then abandoned.

- Both gave the same accuracy as the baseline (0.8324) with lower recall (0.7101 against
  0.7246) and lower F1 (0.7656 against 0.7692).
- ROC-AUC fell as trees were added: 0.8524 (100), 0.8504 (200), 0.8478 (300).
- More trees cost more training time and a larger model for no gain, so neither was
  merged.

## 10. CI

Workflow: `.github/workflows/ci.yml`. It runs on every pull request into `dev`,
`staging` and `main`:

1. Install dependencies with `uv sync --dev`
2. `ruff check .`
3. `ruff format --check .`
4. `pytest tests/`
5. `dvc pull`
6. Data check: `data/raw/train.csv` and `data/raw/test.csv` exist
7. Smoke training: `dvc repro`

### CI failure

![CI failure](docs/img/ci-failure.png)

### CI success

![CI success](docs/img/ci-success.png)

## 11. Each member's contribution

### Hasna Zaheer — Data Owner

- **Repository setup:** I created the project structure and the first pre-commit
  configuration (PR #1).
- **DVC and data:** I initialised DVC, connected the DagsHub remote and tracked
  `train.csv` and `test.csv` (PR #6).
- **EDA:** I wrote `notebooks/01-eda.ipynb`. It covers the dataset structure, missing
  values, the target, passenger class, sex, age, fare and family features, with
  visualisations and conclusions (PR #8).
- **Dataset update:** I created dataset v2 by removing the rows with missing
  `Embarked`, re-ran the pipeline, and resolved the conflict in `dvc.lock` and
  `metrics.json` (PR #11).
- **CI:** I wrote the GitHub Actions workflow with lint, format check, tests, DVC pull,
  data checks and smoke training. I broke a test on purpose to show a failing run, then
  fixed it, and added DagsHub authentication through GitHub secrets (PR #18).
- **Experiments:** I set `max_depth` to 8 (PR #13) and added experiment results
  (PR #14).
- **Reproduction:** I cloned the repository into a fresh folder, checked out `staging`,
  ran `dvc pull` and `dvc repro`, and confirmed the metrics match Tayyab's exactly.
- **Reviews:** I reviewed and merged PRs #2, #4, #9, #16, #19, #20 and #21, and
  requested changes on PR #16. I also documented our review workflow (PR #17).

### Muhammad Tayyab — Model Owner

- **Code refactor:** I moved the starter notebook code into reusable modules in `src/`
  and removed hardcoded paths, so the code runs on any machine (PR #2).
- **Environment:** I set up uv with `pyproject.toml` and `uv.lock`, and documented the
  setup in the README and `CONTRIBUTING.md` (PR #2).
- **Model pipeline:** I built the three DVC stages `prepare`, `train` and `evaluate`
  in `dvc.yaml` (PR #9).
- **Parameters:** I moved the seed, split ratio and hyperparameters into `params.yaml`
  (PR #9).
- **Training:** I train a Random Forest whose type and hyperparameters are read from
  `params.yaml`, with the seed applied to the split and the model (PR #9).
- **Leakage fix:** I changed imputation so the Age and Fare medians come from the
  training split only, and added a test that guards it (PR #9).
- **Metrics:** I made the evaluate stage write `metrics.json` with accuracy, precision,
  recall, F1, ROC-AUC and the Git commit of the run (PR #9).
- **Experiments:** I ran three `n_estimators` experiments (50, 200, 300) against the
  baseline of 100 and merged the winner (PR #10). I also set `max_depth` to 10 (PR #12).
- **Tests:** I wrote `tests/test_preprocessing.py` (PR #8) and the pipeline tests in
  `tests/test_pipeline.py` (PR #9).
- **Release:** I refreshed `dvc.lock` and fixed a lint failure before release (PR #19),
  opened the release PRs #20 and #21, and created the tag `model-v1.0`.
- **Reviews:** I reviewed and merged PRs #1, #6, #8, #11, #13, #14, #17 and #18.

## 12. Retrospective

### What went well

- **Reproducibility worked.** Both of us ran the released configuration and got the
  same metric values to every digit.
- **Splitting data and code.** DVC with DagsHub kept the CSV files out of Git while
  every commit still pins the exact data version.
- **Branch protection and PRs.** No change reached `dev`, `staging` or `main` without
  a pull request.
- **CI caught a real problem.** The lint step failed on a line-length error before the
  release, and we fixed it in PR #19.

### What went wrong

- **Parameters changed without re-running the pipeline.** PRs #12 and #13 changed
  `max_depth` in `params.yaml` without running `dvc repro`, so `dvc.lock` and
  `metrics.json` no longer matched the parameters. We only saw the effect when the
  pipeline was re-run in PR #18, and the released model scores lower than an earlier
  configuration.
- **A conflict resolution left the lock file inconsistent.** After the PR #11 conflict,
  `params.yaml` and `dvc.lock` did not describe the same run.
- **DagsHub was not connected to GitHub at first.** `dvc push` succeeded but the
  DagsHub page was empty, because the DagsHub repository had no Git history. We
  recreated it as a repository connected to GitHub.

### What we would do differently

- Make every experiment PR include the re-run `dvc.lock` and `metrics.json`, and add a
  CI step that fails when the pipeline is out of date.
- After resolving a conflict in `dvc.lock` or `metrics.json`, always run `dvc repro`
  instead of choosing one side by hand.
- Change one parameter at a time on a fixed dataset version, so results are comparable.
- Push experiments with `dvc exp push`, so both of us can see them in `dvc exp show`.
