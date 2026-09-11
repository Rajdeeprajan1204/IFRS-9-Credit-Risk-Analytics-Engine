"""Scenario-based credit stress testing."""

import pandas as pd

from .expected_loss import expected_loss


def apply_multipliers(
    portfolio: pd.DataFrame,
    pd_multiplier: float = 1.0,
    lgd_multiplier: float = 1.0,
) -> pd.DataFrame:
    """Apply transparent PD/LGD scenario multipliers without changing EAD."""
    if pd_multiplier < 0 or lgd_multiplier < 0:
        raise ValueError("scenario multipliers must be non-negative")
    out = portfolio.copy()
    out["stressed_pd"] = (out["pd"] * pd_multiplier).clip(upper=1.0)
    out["stressed_lgd"] = (out["lgd"] * lgd_multiplier).clip(lower=0.0, upper=1.0)
    out["stressed_el"] = expected_loss(out["stressed_pd"], out["stressed_lgd"], out["ead"])
    return out


def scenario_summary(portfolio: pd.DataFrame) -> pd.Series:
    """Summarise stressed exposure and expected loss."""
    return pd.Series({
        "exposure": portfolio["ead"].sum(),
        "expected_loss": portfolio["stressed_el"].sum(),
        "expected_loss_bps": portfolio["stressed_el"].sum() / portfolio["ead"].sum() * 10_000,
    })
