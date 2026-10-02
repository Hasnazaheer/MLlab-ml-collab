"""Model definition, validation and final fitting."""

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def build_model():
    """Standard-scaled logistic regression."""
    return make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))


def evaluate(X, y, test_size=0.2, random_state=42):
    """Fit on a train split and score the held-out split.

    Returns a dict with the classification report text and ROC-AUC.
    """
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    model = build_model().fit(X_train, y_train)
    return {
        "report": classification_report(y_val, model.predict(X_val)),
        "roc_auc": roc_auc_score(y_val, model.predict_proba(X_val)[:, 1]),
    }


def fit_full(X, y):
    """Fit the model on all labelled data."""
    return build_model().fit(X, y)
