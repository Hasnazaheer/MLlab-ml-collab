"""Pipeline parameters (params.yaml) and seeding."""

import random

import numpy as np
import yaml

from src.paths import PARAMS_FILE


def load_params(path=PARAMS_FILE):
    """Return the contents of params.yaml as a dict."""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def set_seed(seed):
    """Seed Python's and NumPy's global random number generators.

    scikit-learn calls also get the seed explicitly via ``random_state``;
    this covers any shuffling or sampling that falls back to global state.
    """
    random.seed(seed)
    np.random.seed(seed)
