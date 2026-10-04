import re

import pandas as pd
import pytest

from src.evaluate import current_commit_sha
from src.features import clean
from src.model import build_model
from src.params import load_params
from src.prepare import split_and_process


def _raw(n=40):
    return pd.DataFrame(
        {
            "PassengerId": range(1, n + 1),
            "Survived": [0, 1] * (n // 2),
            "Pclass": [1, 2, 3, 3] * (n // 4),
            "Name": ["Doe, Mr. John", "Doe, Mrs. Jane"] * (n // 2),
            "Sex": ["male", "female"] * (n // 2),
            "Age": [22.0, None, 35.0, 4.0] * (n // 4),
            "SibSp": [0, 1] * (n // 2),
            "Parch": [0, 0, 1, 2] * (n // 4),
            "Ticket": ["A1"] * n,
            "Fare": [7.25, 71.28, 8.05, 500.0] * (n // 4),
            "Cabin": [None] * n,
            "Embarked": ["S", "C", "Q", None] * (n // 4),
        }
    )


def test_params_has_seed_split_and_hyperparameters():
    params = load_params()

    assert isinstance(params["seed"], int)
    assert 0 < params["split"]["test_size"] < 1
    assert "model" in params["train"]


def test_split_is_reproducible_for_same_seed():
    first_train, first_test = split_and_process(_raw(), test_size=0.25, seed=42)
    second_train, second_test = split_and_process(_raw(), test_size=0.25, seed=42)

    pd.testing.assert_frame_equal(first_train, second_train)
    pd.testing.assert_frame_equal(first_test, second_test)


def test_split_has_no_missing_values_and_matching_columns():
    train, test = split_and_process(_raw(), test_size=0.25, seed=42)

    assert len(train) == 30
    assert len(test) == 10
    assert list(train.columns) == list(test.columns)
    assert not train.isnull().any().any()
    assert not test.isnull().any().any()


def test_build_model_uses_seed_and_hyperparameters():
    model = build_model(model="random_forest", seed=7, n_estimators=10, max_depth=3)

    assert model.random_state == 7
    assert model.n_estimators == 999
    assert model.max_depth == 3


def test_build_model_rejects_unknown_model():
    with pytest.raises(ValueError):
        build_model(model="unknown")


def test_clean_fits_imputation_on_train_only():
    train = _raw().assign(Age=[10.0, 20.0, 30.0, None] * 10)
    test = _raw(8).assign(Age=[None, 90.0] * 4, Fare=[None, 1.0] * 4)

    cleaned_train, cleaned_test = clean(train, test)

    # Filled with train's medians, not test's (which would be 90.0 and 1.0)
    assert (cleaned_test["Age"].iloc[::2] == 20.0).all()
    assert (cleaned_test["Fare"].iloc[::2] == cleaned_train["Fare"].median()).all()


def test_current_commit_sha_is_full_git_sha():
    assert re.fullmatch(r"[0-9a-f]{40}", current_commit_sha())
