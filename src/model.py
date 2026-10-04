"""Model definition and scoring."""

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def build_model(model="random_forest", seed=42, **hyperparams):
    """Return an unfitted classifier.

    ``model`` and ``hyperparams`` come from the ``train`` section of
    params.yaml; ``seed`` fixes the model's own randomness.
    """
    if model == "random_forest":
        return RandomForestClassifier(random_state=seed, **hyperparams)
    if model == "logistic_regression":
        return make_pipeline(
            StandardScaler(),
            LogisticRegression(random_state=seed, **hyperparams),
        )
    raise ValueError(
        f"Unknown model {model!r}; expected 'random_forest' or 'logistic_regression'"
    )


def score(y_true, y_pred, y_proba):
    """Return classification metrics as a plain dict of floats."""
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred)),
        "recall": float(recall_score(y_true, y_pred)),
        "f1": float(f1_score(y_true, y_pred)),
        "roc_auc": float(roc_auc_score(y_true, y_proba)),
    }
