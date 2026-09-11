"""Expected credit loss calculations."""

import numpy as np
import pandas as pd


def expected_loss(pd_value, lgd, ead):
    """Calculate expected loss as PD × LGD × EAD."""
    return np.asarray(pd_value) * np.asarray(lgd) * np.asarray(ead)


def stage_expected_loss(pd_value, lgd, ead, stage):
    """Calculate ECL under a simple IFRS 9 staging convention.

    Stage 1 uses a 12-month PD; Stage 2 and Stage 3 are supplied with the
    lifetime PD / loss assumptions appropriate to the implementation.
    """
    stage = pd.Series(stage).astype(int)
    valid = stage.isin([1, 2, 3])
    if not valid.all():
        raise ValueError("stage must contain only 1, 2 or 3")
    return pd.Series(expected_loss(pd_value, lgd, ead), index=stage.index)


def portfolio_expected_loss(pd_values, lgd_values, ead_values):
    """Aggregate loan-level expected loss to portfolio level."""
    return float(np.nansum(expected_loss(pd_values, lgd_values, ead_values)))
