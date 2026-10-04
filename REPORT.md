# MLLab ML Collaboration — Final Report

Repository: https://github.com/Hasnazaheer/MLlab-ml-collab
DVC remote (DagsHub): https://dagshub.com/hasnazaheer861/MLlab-ml-collab
Release tag: `model-v1.0` (commit `e899b6d` on `main`)

Items marked **TODO** need a screenshot or a detail that is only visible on GitHub or
on a teammate's machine.

## 1. Team members and roles

| Member | GitHub | Role | Main responsibilities |
|---|---|---|---|
| Hasna Zaheer | `Hasnazaheer` | Data Owner | Repository setup, DVC and DagsHub, dataset versions, EDA, CI |
| Muhammad Tayyab | `tyb01` | Model Owner | Code refactor, environment, model pipeline, parameters, experiments, release tag |

Commits on `main` (excluding merges): Tayyab 18, Hasna 17.
Of the 21 pull requests, Tayyab merged 13 and Hasna merged 8.

## 2. Dataset and source

- **Dataset:** Titanic passenger survival (binary classification, target `Survived`).
- **Source:** Kaggle "Titanic - Machine Learning from Disaster",
  https://www.kaggle.com/c/titanic/data
- **Storage:** the CSV files are tracked with DVC and stored on DagsHub. Git holds
  only the pointer files `data/raw/train.csv.dvc` and `data/raw/test.csv.dvc`.

| Version | Commit | Rows | DVC md5 | Change |
|---|---|---|---|---|
| v1 | `be7ba68` | 891 | `2309cc5f` | Original Kaggle `train.csv` |
| v2 (released) | `00f5d84` | 889 | `60f1e059` | 2 rows with missing `Embarked` removed |

`data/raw/test.csv` (418 rows, md5 `7533b82e`) is the unlabelled Kaggle test file. It
is tracked but not used by the pipeline, because it has no target to score against.

In v2, 177 rows are missing `Age` and 687 are missing `Cabin`. The survival rate is
38.25%.

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
- **Traceability:** `metrics.json` records the Git commit SHA the run was made from.
- **Features (14):** `Pclass`, `Age`, `SibSp`, `Parch`, `Fare`, `FamilySize`,
  `IsAlone`, `Sex_male`, `Embarked_Q`, `Embarked_S`, `Title_Miss`, `Title_Mr`,
  `Title_Mrs`, `Title_Other`.

## 4. Released model and final metrics

| Setting | Value |
|---|---|
| Model | Random Forest |
| `n_estimators` | 50 |
| `max_depth` | 10 |
| `seed` | 42 |
| `split.test_size` | 0.2 (stratified) |
| Dataset | v2, md5 `60f1e059` |

`metrics.json` on `main` at `model-v1.0`:

| Metric | Value |
|---|---|
| accuracy | 0.7921348314606742 |
| precision | 0.7313432835820896 |
| recall | 0.7205882352941176 |
| f1 | 0.725925925925926 |
| roc_auc | 0.8064839572192513 |
| commit_sha | `bd407020b178213a7b8ddc1a8d3dc4426fe941df` |

## 5. Reproducibility table

The same configuration (dataset v2, `n_estimators` 50, `max_depth` 10, seed 42) was
run independently by both members. The five metric values match to every digit.

| Run | By | Commit | accuracy | precision | recall | f1 | roc_auc |
|---|---|---|---|---|---|---|---|
| Pipeline run in CI PR #18 | Hasna | `7bd04c0` | 0.7921348314606742 | 0.7313432835820896 | 0.7205882352941176 | 0.725925925925926 | 0.8064839572192513 |
| Re-run before release, PR #19 | Tayyab | `1b0b3e6` | 0.7921348314606742 | 0.7313432835820896 | 0.7205882352941176 | 0.725925925925926 | 0.8064839572192513 |
| Released on `main` | — | `e899b6d` | 0.7921348314606742 | 0.7313432835820896 | 0.7205882352941176 | 0.725925925925926 | 0.8064839572192513 |
| Fresh clone of `staging` | Hasna | **TODO** | **TODO** | **TODO** | **TODO** | **TODO** | **TODO** |

> **TODO (Hasna):** fill the last row from the fresh-clone run
> (`git clone`, `git checkout staging`, `uv sync`, `uv run dvc pull`, `uv run dvc repro`).

Notes:

- On one machine, a forced full re-run (`dvc repro --force`) produced a byte-identical
  `dvc.lock`: same processed data, same model file, same metrics.
- Between the two machines the metric values are identical, but the file hashes of the
  processed CSVs and `model.pkl` differ (for example `data/processed/train.csv` is
  `e588bf0e` in Hasna's run and `23cc1f11` in Tayyab's). The results are reproducible;
  the files are not byte-identical across machines.
- `commit_sha` differs between runs by design, because it records the commit each run
  was made from.

Steps to reproduce:

```bash
git clone https://github.com/Hasnazaheer/MLlab-ml-collab.git
cd MLlab-ml-collab
git checkout model-v1.0
uv sync
uv run dvc remote modify origin --local auth basic
uv run dvc remote modify origin --local user <dagshub-username>
uv run dvc remote modify origin --local password <dagshub-token>
uv run dvc pull
uv run dvc repro
```

## 6. Experiment comparison

### 6.1 Tayyab: `n_estimators`

Run with `dvc exp run --set-param train.n_estimators=<n>` on branch
`exp/tayyab-n-estimators`, from commit `963f416`. Dataset v1, `max_depth` 6, seed 42.

| Experiment | n_estimators | accuracy | precision | recall | f1 | roc_auc | Outcome |
|---|---|---|---|---|---|---|---|
| baseline | 100 | 0.8324 | 0.8197 | 0.7246 | 0.7692 | 0.8524 | Replaced |
| `tayyab-n-est-50` | 50 | 0.8324 | 0.8095 | 0.7391 | 0.7727 | 0.8514 | **Winner**, merged in PR #10 |
| `tayyab-n-est-200` | 200 | 0.8324 | 0.8305 | 0.7101 | 0.7656 | 0.8504 | Abandoned |
| `tayyab-n-est-300` | 300 | 0.8324 | 0.8305 | 0.7101 | 0.7656 | 0.8478 | Abandoned |

### 6.2 Hasna: experiments

> **TODO (Hasna):** add your 3 experiments. Run `uv run dvc exp show --only-changed --md`
> and paste the table here. They were not pushed to GitHub, so they are only on your
> machine.

| Experiment | Parameter changed | accuracy | precision | recall | f1 | roc_auc | Outcome |
|---|---|---|---|---|---|---|---|
| **TODO** | | | | | | | |
| **TODO** | | | | | | | |
| **TODO** | | | | | | | |

### 6.3 Pipeline runs committed to the repository

| Commit | PR | Dataset | n_estimators | max_depth | accuracy | precision | recall | f1 | roc_auc |
|---|---|---|---|---|---|---|---|---|---|
| `cb3165b` | #9 | v1 | 100 | 6 | 0.8324 | 0.8197 | 0.7246 | 0.7692 | 0.8524 |
| `d0b7d66` | #10 | v1 | 50 | 6 | 0.8324 | 0.8095 | 0.7391 | 0.7727 | 0.8514 |
| `00f5d84` | #11 | v2 | 100 | 6 | 0.8146 | 0.7966 | 0.6912 | 0.7402 | 0.8381 |
| `7bd04c0` | #18 | v2 | 50 | 10 | 0.7921 | 0.7313 | 0.7206 | 0.7259 | 0.8065 |

`max_depth` 8 (PR #13) and `max_depth` 10 (PR #12) were merged as changes to
`params.yaml` only, without re-running the pipeline. `max_depth` 8 was never measured.
`max_depth` 10 was first measured when the pipeline was re-run in PR #18.

## 7. Why the winner was selected

**`n_estimators` = 50.** All four settings reached the same accuracy (0.8324). 50 trees
gave the best F1 (0.7727) and the best recall (0.7391), with ROC-AUC within 0.001 of the
baseline, and it is the smallest and fastest model. Finding survivors (recall) matters
more than a slightly higher precision, so 50 was merged in PR #10.

**`max_depth` = 10.** This was the last `max_depth` change merged into `dev` (PR #12,
after PR #13 set it to 8). It was not selected from measured results; see the
retrospective.

**Honest assessment of the released model.** The released configuration scores lower
than the earlier committed run on the same dataset v2:

| Configuration on dataset v2 | accuracy | f1 | roc_auc |
|---|---|---|---|
| `n_estimators` 100, `max_depth` 6 (`00f5d84`) | 0.8146 | 0.7402 | 0.8381 |
| `n_estimators` 50, `max_depth` 10 (released) | 0.7921 | 0.7259 | 0.8065 |

Two parameters differ between these rows, so the drop cannot be attributed to
`max_depth` alone. `n_estimators` 50 with `max_depth` 6 was not run on dataset v2.

## 8. Required PR links

### Data-update PR

- **PR #11** `data/update-dataset` → `dev`, by Hasna:
  https://github.com/Hasnazaheer/MLlab-ml-collab/pull/11
- Removed the 2 rows with missing `Embarked`; `train.csv` went from 891 to 889 rows and
  its DVC md5 from `2309cc5f` to `60f1e059`.
- Earlier, **PR #6** `data/initial-dataset` → `dev` first put the dataset under DVC:
  https://github.com/Hasnazaheer/MLlab-ml-collab/pull/6

### Conflict PR

| PR | Branch | Conflicting files | Resolved by | Resolution commit |
|---|---|---|---|---|
| [#11](https://github.com/Hasnazaheer/MLlab-ml-collab/pull/11) | `data/update-dataset` | `dvc.lock`, `metrics.json` | Hasna | `2b5ee4c` |
| [#8](https://github.com/Hasnazaheer/MLlab-ml-collab/pull/8) | `feat/eda-notebook` | `.gitignore`, `pyproject.toml`, `uv.lock` | Hasna | `efa13cd`, `735269e` |
| [#4](https://github.com/Hasnazaheer/MLlab-ml-collab/pull/4) | `feat/pre-commit` | `pyproject.toml`, `uv.lock` | Tayyab | `431ea67` |

PR #11 is the main example: the data branch and the `n_estimators` experiment (PR #10)
both changed `dvc.lock` and `metrics.json`.

### Changes-requested review

- **PR #16** `fix/gitignore` → `dev`, by Tayyab, reviewed by Hasna:
  https://github.com/Hasnazaheer/MLlab-ml-collab/pull/16
- First commit `7ae224e` ("fixed dvc files") added a comment line to `.gitignore`.
  After the review, commit `39da1bd` ("fixed requested changes") reworded it, and Hasna
  merged the PR.
- The review workflow is also noted in the README (PR #17).

> **TODO:** add a screenshot of the "Changes requested" review on PR #16.

### Release PRs

| PR | Direction | Merged by | Link |
|---|---|---|---|
| #20 | `dev` → `staging` | Hasna | https://github.com/Hasnazaheer/MLlab-ml-collab/pull/20 |
| #21 | `staging` → `main` | Hasna | https://github.com/Hasnazaheer/MLlab-ml-collab/pull/21 |

Tag `model-v1.0` ("First production model") was created by Tayyab on the merge commit
of PR #21 (`e899b6d`).

An earlier promotion used the same route: PR #5 (`dev` → `staging`) and PR #7
(`staging` → `main`).

## 9. Abandoned experiment

`tayyab-n-est-200` and `tayyab-n-est-300` were run and then abandoned.

- Both gave the same accuracy as the baseline (0.8324) with lower recall (0.7101 against
  0.7246) and lower F1 (0.7656 against 0.7692).
- ROC-AUC fell as trees were added: 0.8524 (100), 0.8504 (200), 0.8478 (300).
- More trees cost more training time and a larger model for no gain, so neither was
  applied or merged. They remain as DVC experiments on `exp/tayyab-n-estimators`.

> **TODO:** if the assignment expects a closed, unmerged PR as the abandoned
> experiment, add its link here.

## 10. CI

Workflow: `.github/workflows/ci.yml`, added by Hasna in PR #18. It runs on every pull
request into `dev`, `staging` and `main`:

1. Install dependencies with `uv sync --dev`
2. `ruff check .`
3. `ruff format --check .`
4. `pytest tests/` (8 tests)
5. `dvc pull`, using DagsHub credentials stored as GitHub secrets
6. Data check: `data/raw/train.csv` and `data/raw/test.csv` exist
7. Smoke training: `dvc repro`

### CI failure

- **Intentional failure, PR #18:** commit `ef77643` changed a test assertion to
  `assert model.n_estimators == 999`, so `pytest` failed. Commit `36da3d8` restored it.
- **Real failure, PR #19:** `ruff check` failed with `E501 Line too long (97 > 88)` on
  a docstring in `src/data.py`. Fixed in commit `f647746`.

> **TODO:** add the CI failure screenshot, e.g. `![CI failure](docs/img/ci-failure.png)`

### CI success

> **TODO:** add the CI success screenshot, e.g. `![CI success](docs/img/ci-success.png)`

## 11. All pull requests

| PR | Branch | Author | Merged by | Summary |
|---|---|---|---|---|
| #1 | `feat/pre-commit` → `main` | Hasna | Tayyab | Pre-commit hooks |
| #2 | `feat/starter-code-refactor` → `dev` | Tayyab | Hasna | Notebook code moved into `src/`, uv environment |
| #3 | `feat/pre-commit` → `dev` | Tayyab | Tayyab | Branch-protection test |
| #4 | `feat/pre-commit` → `dev` | Tayyab | Hasna | Pre-commit setup, conflict resolved |
| #5 | `dev` → `staging` | — | Tayyab | First promotion |
| #6 | `data/initial-dataset` → `dev` | Hasna | Tayyab | Dataset tracked with DVC |
| #7 | `staging` → `main` | — | Hasna | First promotion |
| #8 | `feat/eda-notebook` → `dev` | Hasna, Tayyab | Tayyab | EDA notebook, first unit test |
| #9 | `feat/dvc-pipeline` → `dev` | Tayyab | Hasna | 3-stage pipeline, `params.yaml`, seeds, leakage fix |
| #10 | `feat/tayyab-n-estimators-50` → `dev` | Tayyab | Tayyab | Experiment winner: `n_estimators` 50 |
| #11 | `data/update-dataset` → `dev` | Hasna | Tayyab | Dataset v2 |
| #12 | `feat/tayyab-max-depth-10` → `dev` | Tayyab | Tayyab | `max_depth` 10 |
| #13 | `feat/hasna-max-depth-8` → `dev` | Hasna | Tayyab | `max_depth` 8 |
| #14 | `feat/exp` → `dev` | Hasna | Tayyab | Experiment results; no net file change |
| #15 | `fix/require_funciton_changed` → `dev` | Tayyab | Tayyab | Docstring for `_require` |
| #16 | `fix/gitignore` → `dev` | Tayyab | Hasna | `.gitignore` fix, changes requested |
| #17 | `docs/review-pr-practice` → `dev` | Hasna | Tayyab | Review workflow notes |
| #18 | `feat/ci` → `dev` | Hasna | Tayyab | GitHub Actions CI |
| #19 | `fix/refresh-dvc-lock` → `dev` | Tayyab | Hasna | Refreshed `dvc.lock`, lint fix |
| #20 | `dev` → `staging` | Tayyab | Hasna | Release v1.0 |
| #21 | `staging` → `main` | Tayyab | Hasna | Release v1.0 |

## 12. Each member's contribution

### Hasna Zaheer — Data Owner

> **TODO (Hasna):** this section is written from the Git history. Check it and add
> anything it misses.

- **Repository setup:** created the project structure (`6f89d63`) and the first
  pre-commit configuration (`50b3230`, PR #1).
- **DVC and data:** initialised DVC, connected the DagsHub remote and tracked
  `train.csv` and `test.csv` (`be7ba68`, `3014617`, PR #6).
- **EDA:** wrote `notebooks/01-eda.ipynb`, covering dataset structure, missing values,
  the target, passenger class, sex, age, fare and family features, with visualisations
  and conclusions (PR #8).
- **Dataset update:** produced dataset v2 by removing the rows with missing `Embarked`,
  re-ran the pipeline and resolved the resulting conflict in `dvc.lock` and
  `metrics.json` (PR #11).
- **CI:** wrote the GitHub Actions workflow with lint, format, tests, DVC pull, data
  checks and smoke training; demonstrated a failing and a passing run; added DagsHub
  authentication through GitHub secrets (PR #18).
- **Experiments:** `max_depth` 8 (PR #13) and experiment results (PR #14).
- **Documentation:** review workflow notes (PR #17).
- **Reviews and merges:** merged PRs #2, #4, #7, #9, #16, #19, #20 and #21; requested
  changes on PR #16.

### Muhammad Tayyab — Model Owner

- **Code refactor:** moved the starter notebook code into reusable modules in `src/`
  and removed hardcoded paths, so the code runs from any machine (PR #2).
- **Environment:** set up uv with `pyproject.toml` and `uv.lock`, and documented the
  setup in the README and `CONTRIBUTING.md` (PR #2).
- **Model pipeline:** built the three DVC stages `prepare`, `train` and `evaluate`
  with `dvc.yaml` (PR #9).
- **Parameters:** moved the seed, split ratio and hyperparameters into `params.yaml`
  (PR #9).
- **Training:** Random Forest, with the model type and hyperparameters read from
  `params.yaml` and the seed applied to the split and the model (PR #9).
- **Leakage fix:** changed imputation so the Age and Fare medians come from the
  training split only, with a test that guards it (`b5a4465`, PR #9).
- **Metrics:** `metrics.json` with accuracy, precision, recall, F1, ROC-AUC and the
  Git commit SHA (`cb3165b`, PR #9).
- **Experiments:** three `n_estimators` experiments (50, 200, 300) against the
  baseline of 100; merged the winner (PR #10); `max_depth` 10 (PR #12).
- **Tests:** `tests/test_preprocessing.py` (PR #8) and seven pipeline tests in
  `tests/test_pipeline.py` (PR #9).
- **Release:** refreshed `dvc.lock` and fixed the lint failure before release (PR #19),
  opened the release PRs #20 and #21, and created the tag `model-v1.0`.
- **Reviews and merges:** merged PRs #1, #5, #6, #8, #11, #13, #14, #17 and #18.

## 13. Retrospective

### What went well

- **Reproducibility worked.** Both members ran the released configuration
  independently and got the same five metric values to every digit.
- **Splitting data and code.** DVC with DagsHub kept the CSV files out of Git while
  every commit still pins the exact data version by hash.
- **Branch protection and PRs.** No change reached `dev`, `staging` or `main` without
  a pull request; a direct push to `dev` was rejected by the repository rules.
- **CI caught a real problem.** The lint step failed on a line-length error in PR #19
  that had already been merged into `dev` unnoticed.

### What went wrong

- **Parameters changed without re-running the pipeline.** PRs #12 and #13 changed
  `max_depth` in `params.yaml` but did not run `dvc repro`, so `dvc.lock` and
  `metrics.json` no longer matched the parameters. The effect was only seen when CI
  re-ran the pipeline in PR #18, and the released model scores lower than an earlier
  configuration.
- **A conflict resolution left the lock file inconsistent.** After the PR #11 conflict,
  `params.yaml` said `n_estimators` 50 while `dvc.lock` and `metrics.json` still held
  the results of the 100-tree run.
- **DagsHub was not connected to GitHub at first.** `dvc push` succeeded but the DagsHub
  page was empty, because the pointer files were on GitHub and the DagsHub repository
  had no Git history. The repository was recreated as a connected mirror.
- **Wrong Git identity.** The first three commits on `feat/starter-code-refactor` were
  made with another account's Git configuration and had to be rewritten.
- **A lint rule arrived after the code it rejects.** The line-length rule was added to
  the ruff configuration in PR #18. PR #15 had been written before that, passed its
  local hooks, and was merged with a 97-character line that CI then rejected in PR #19.
  The pre-commit hook also pins ruff `v0.9.10` while CI installs `ruff>=0.16.10`.

### What we would do differently

- Make every experiment PR include the re-run `dvc.lock` and `metrics.json`, and add a
  CI step that fails when `dvc status` reports the pipeline is out of date.
- After resolving a conflict in `dvc.lock` or `metrics.json`, always run `dvc repro`
  instead of choosing one side by hand.
- Change one parameter at a time on a fixed dataset version, so results are comparable.
- Push experiments with `dvc exp push`, so both members can see them in `dvc exp show`.
- Use the same ruff version in the pre-commit hook and in CI, and re-run CI on open
  branches when lint rules change.
- Set each member's Git identity and DagsHub token on the first day.
