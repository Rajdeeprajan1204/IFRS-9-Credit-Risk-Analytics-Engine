import numpy as np
import pandas as pd

from credit_risk.expected_loss import expected_loss
from credit_risk.portfolio import weighted_average
from credit_risk.staging import assign_stage
from credit_risk.stress import apply_multipliers
from credit_risk.risk_metrics import gini_from_auc


def test_expected_loss():
    assert np.isclose(expected_loss(0.02, 0.40, 100_000), 800.0)


def test_stage_precedence():
    index = pd.Index(["a", "b", "c"])
    result = assign_stage(pd.Series([False, True, True], index=index), pd.Series([False, False, True], index=index))
    assert result.tolist() == [1, 2, 3]


def test_weighted_average():
    values = pd.Series([0.10, 0.20])
    weights = pd.Series([100.0, 300.0])
    assert np.isclose(weighted_average(values, weights), 0.175)


def test_stress():
    portfolio = pd.DataFrame({"pd": [0.02], "lgd": [0.40], "ead": [100_000.0]})
    stressed = apply_multipliers(portfolio, 2.0, 1.5)
    assert np.isclose(stressed.loc[0, "stressed_el"], 2_400.0)


def test_gini():
    assert np.isclose(gini_from_auc(0.83), 0.66)
