"""Credit-model monitoring and validation metrics."""

import numpy as np
import pandas as pd


def population_stability_index(expected: pd.Series, actual: pd.Series, bins=10) -> float:
    """Calculate PSI for two numeric populations using shared quantile bins."""
    expected = pd.Series(expected).dropna().astype(float)
    actual = pd.Series(actual).dropna().astype(float)
    if expected.empty or actual.empty:
        raise ValueError("both populations must contain observations")

    edges = np.unique(np.quantile(expected, np.linspace(0, 1, bins + 1)))
    if len(edges) < 3:
        return 0.0
    expected_pct = pd.cut(expected, edges, include_lowest=True).value_counts(normalize=True, sort=False)
    actual_pct = pd.cut(actual, edges, include_lowest=True).value_counts(normalize=True, sort=False)
    e = expected_pct.clip(lower=1e-6)
    a = actual_pct.clip(lower=1e-6)
    return float(((a - e) * np.log(a / e)).sum())


def gini_from_auc(auc: float) -> float:
    """Convert AUC to Gini discrimination statistic."""
    if not 0 <= auc <= 1:
        raise ValueError("AUC must lie between 0 and 1")
    return 2 * auc - 1
