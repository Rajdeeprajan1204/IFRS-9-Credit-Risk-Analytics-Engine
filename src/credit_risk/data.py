"""Data preparation and validation helpers."""

import pandas as pd


def validate_loan_table(df: pd.DataFrame) -> pd.DataFrame:
    """Validate the minimum fields required by the analytics layer."""
    required = {"ead"}
    missing = required.difference(df.columns)
    if missing:
        raise KeyError(f"Missing required columns: {sorted(missing)}")
    if df.empty:
        raise ValueError("loan table cannot be empty")
    out = df.copy()
    out["ead"] = pd.to_numeric(out["ead"], errors="coerce")
    if (out["ead"].dropna() < 0).any():
        raise ValueError("EAD cannot be negative")
    return out


def missingness_report(df: pd.DataFrame) -> pd.DataFrame:
    """Return column-level missing counts and percentages."""
    return pd.DataFrame({
        "missing_count": df.isna().sum(),
        "missing_pct": df.isna().mean(),
        "dtype": df.dtypes.astype(str),
    }).sort_values("missing_pct", ascending=False)
