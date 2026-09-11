"""Canonical definitions used by the analytical workflow."""

import numpy as np
import pandas as pd


def realised_loss(ead, accrued_interest=0.0, costs=0.0, recoveries=0.0):
    """Calculate realised loss from EAD, accrued amounts, costs and recoveries."""
    return np.asarray(ead) + np.asarray(accrued_interest) + np.asarray(costs) - np.asarray(recoveries)


def lgd_from_loss(loss, ead, lower=0.0, upper=1.10):
    """Convert loss to LGD and bound extreme observations for modelling."""
    ead = np.asarray(ead, dtype=float)
    lgd = np.divide(loss, ead, out=np.full_like(ead, np.nan), where=ead != 0)
    return np.clip(lgd, lower, upper)


def ead_at_default(balance):
    """Return outstanding balance at default as EAD for a term mortgage."""
    return pd.to_numeric(balance, errors="coerce")
