"""Cleaning, imputation and feature engineering."""

import numpy as np
import pandas as pd

TARGET = "Survived"
COMMON_TITLES = ["Mr", "Miss", "Mrs", "Master"]
DROP_COLS = ["Name", "Ticket", "PassengerId"]


def clean(train, test):
    """Cap Fare outliers, impute missing values and drop Cabin.

    Returns new DataFrames; the inputs are not modified.
    """
    train, test = train.copy(), test.copy()

    # Cap Fare outliers using the IQR rule computed on train
    q1, q3 = train["Fare"].quantile([0.25, 0.75])
    upper_limit = q3 + 1.5 * (q3 - q1)
    train["Fare"] = np.where(train["Fare"] > upper_limit, upper_limit, train["Fare"])
    test["Fare"] = np.where(test["Fare"] > upper_limit, upper_limit, test["Fare"])

    # Assign rather than fillna(inplace=True): inplace on a column is a
    # no-op under pandas 3 copy-on-write
    train["Age"] = train["Age"].fillna(train["Age"].median())
    test["Age"] = test["Age"].fillna(test["Age"].median())
    train["Embarked"] = train["Embarked"].fillna(train["Embarked"].mode()[0])
    test["Fare"] = test["Fare"].fillna(test["Fare"].median())

    return train.drop(columns="Cabin"), test.drop(columns="Cabin")


def add_features(df):
    """Add FamilySize, IsAlone and Title columns."""
    df = df.copy()
    df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
    df["IsAlone"] = (df["FamilySize"] == 1).astype(int)
    title = df["Name"].apply(lambda x: x.split(",")[1].split(".")[0].strip())
    df["Title"] = title.where(title.isin(COMMON_TITLES), "Other")
    return df


def encode(train, test):
    """One-hot encode and align test columns to train's feature set.

    Returns (X, y, X_test, test_ids).
    """
    test_ids = test["PassengerId"]
    train = pd.get_dummies(train.drop(columns=DROP_COLS), drop_first=True)
    test = pd.get_dummies(test.drop(columns=DROP_COLS), drop_first=True)

    X = train.drop(columns=TARGET)
    y = train[TARGET]
    X_test = test.reindex(columns=X.columns, fill_value=0)
    return X, y, X_test, test_ids


def preprocess(train, test):
    """Full pipeline from raw DataFrames to model-ready matrices."""
    train, test = clean(train, test)
    return encode(add_features(train), add_features(test))
