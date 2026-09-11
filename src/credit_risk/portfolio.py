"""Portfolio-level credit-risk analytics."""

import pandas as pd

from .expected_loss import expected_loss


def portfolio_expected_loss(portfolio: pd.DataFrame, pd_col="pd", lgd_col="lgd", ead_col="ead") -> float:
    """Aggregate loan-level ECL from a portfolio table."""
    required = {pd_col, lgd_col, ead_col}
    missing = required.difference(portfolio.columns)
    if missing:
        raise KeyError(f"Missing columns: {sorted(missing)}")
    return float(expected_loss(portfolio[pd_col], portfolio[lgd_col], portfolio[ead_col]).sum())


def weighted_average(values: pd.Series, weights: pd.Series) -> float:
    """Return an exposure-weighted average."""
    aligned = pd.concat([values, weights], axis=1).dropna()
    if aligned.empty or aligned.iloc[:, 1].sum() <= 0:
        raise ValueError("weights must contain positive total exposure")
    return float((aligned.iloc[:, 0] * aligned.iloc[:, 1]).sum() / aligned.iloc[:, 1].sum())
