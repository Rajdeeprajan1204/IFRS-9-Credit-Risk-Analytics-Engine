"""Transparent IFRS 9 staging rules."""

import pandas as pd


def assign_stage(
    significant_increase: pd.Series,
    credit_impaired: pd.Series,
) -> pd.Series:
    """Assign Stage 1/2/3 from SICR and credit-impairment indicators.

    Stage 3 takes precedence over Stage 2; Stage 2 takes precedence over Stage 1.
    The inputs represent upstream policy decisions and can therefore be replaced
    by a bank's approved SICR and default definitions.
    """
    sicr = pd.Series(significant_increase, index=significant_increase.index).fillna(False).astype(bool)
    impaired = pd.Series(credit_impaired, index=credit_impaired.index).fillna(False).astype(bool)
    stage = pd.Series(1, index=sicr.index, dtype="int64")
    stage.loc[sicr] = 2
    stage.loc[impaired] = 3
    return stage
