# IFRS 9 Credit Risk Analytics Engine

An interpretable **mortgage credit-risk framework** covering Probability of Default (PD), Loss Given Default (LGD), Exposure at Default (EAD), Expected Credit Loss (ECL), IFRS 9 staging and portfolio stress testing.

The project is designed around an institutional risk workflow: **data quality → risk estimation → calibration → portfolio loss → stress testing → validation**.

## Why this matters

Credit-risk models are not just prediction problems. A useful risk framework has to answer:

- What constitutes a default?
- Which borrower and loan characteristics explain default risk?
- What is the economic loss after recoveries and workout costs?
- How much exposure is outstanding when default occurs?
- How does risk migrate from Stage 1 to Stage 2 and Stage 3?
- How sensitive is expected loss to a deterioration in the credit cycle?
- Does the model remain useful outside the period on which it was estimated?

This repository focuses on those questions while keeping the statistical methods transparent enough to inspect and challenge.

## Framework at a glance

```text
                         MARKET / LOAN DATA
                                │
                                ▼
                     Data quality & assembly
                                │
                 ┌──────────────┼──────────────┐
                 ▼              ▼              ▼
                PD             LGD            EAD
                 │              │              │
                 └──────────────┼──────────────┘
                                ▼
                         IFRS 9 STAGING
                    Stage 1 / Stage 2 / Stage 3
                                │
                                ▼
                   Expected Credit Loss (ECL)
                         PD × LGD × EAD
                                │
                 ┌──────────────┴──────────────┐
                 ▼                             ▼
          Portfolio analytics             Stress testing
                 │                             │
                 └──────────────┬──────────────┘
                                ▼
                    Validation & monitoring
```

## Core components

| Component | Approach | Main output |
|---|---|---|
| **PD** | Interpretable logistic regression + rating calibration | 12-month default probability |
| **LGD** | Realised workout loss + two-part severity framework | Expected loss severity |
| **EAD** | Outstanding balance at default | Exposure at default |
| **Staging** | SICR / credit-impaired indicators | Stage 1 / 2 / 3 |
| **ECL** | PD × LGD × EAD | Loan- and portfolio-level expected loss |
| **Stress** | Transparent PD/LGD scenario shocks and macro satellite framework | Stressed ECL |
| **Validation** | AUC/Gini/KS, calibration, PSI, out-of-time analysis | Model performance & stability |

## Data

The empirical analysis uses the **Freddie Mac Single-Family Loan-Level Dataset**, a public dataset of US residential mortgages containing origination characteristics and monthly servicing/performance information.

The modelling workflow works from the raw loan and performance histories to a **loan-level analytical table** containing default, balance-at-default, workout outcomes and engineered risk variables.

Raw source data is intentionally not redistributed in this repository. The dataset should be obtained directly from Freddie Mac under its applicable terms.

## PD framework

The PD model estimates the probability that a mortgage defaults within a defined 12-month observation window using information available at origination.

A baseline logistic specification is:

`logit(PD_i) = α + β'X_i`

Typical drivers include credit score, LTV/CLTV, DTI, interest rate, term and selected categorical characteristics.

The project treats **discrimination and calibration as separate questions**. A model can rank borrowers effectively while still systematically under- or over-estimating absolute default probabilities.

The score can therefore be mapped into rating grades and calibrated against long-run observed default experience. This makes the output easier to interpret as a credit-risk scale rather than just a machine-learning probability.

### PD validation

The validation framework includes:

- AUC / Gini / KS discrimination metrics
- predicted-versus-observed calibration
- grade-level calibration checks
- confusion-matrix diagnostics at policy-relevant thresholds
- out-of-time testing
- forward / out-of-regime holdouts
- population stability analysis (PSI)

## LGD framework

LGD is based on **observed workout economics**, rather than an assumed severity parameter.

For a disposed default, the loss calculation considers the balance at default, accrued amounts, sale proceeds, insurance recoveries and other recoveries/costs. The implementation distinguishes between:

1. **Nominal realised loss** — the observed dollar shortfall.
2. **Economic loss** — recovery cash flows discounted back to the default date to reflect the timing of the workout.

Where the realised-loss distribution contains a substantial zero-loss mass, a two-part model is more interpretable than a single regression:

`LGD = P(material loss) × E[severity | material loss]`

This separates the question **"will the workout generate a material loss?"** from **"how large will the loss be if it does?"**

Downturn analysis is also kept separate from the baseline estimate so that cyclical severity can be assessed explicitly.

## EAD and IFRS 9 staging

For a fully amortising mortgage, EAD is principally the outstanding balance at default. The framework does not introduce a revolving credit-conversion factor where no undrawn commitment exists.

Staging is deliberately separated from the statistical models:

- **Stage 1:** 12-month ECL
- **Stage 2:** lifetime ECL after a significant increase in credit risk
- **Stage 3:** lifetime ECL for credit-impaired exposures

The staging engine accepts SICR and credit-impairment indicators as inputs. This keeps the accounting-policy decision separate from the PD/LGD estimation layer and makes the policy assumptions explicit.

## Expected Credit Loss

At loan level:

`ECL = PD × LGD × EAD`

At portfolio level, individual ECLs are aggregated and can be expressed as both a dollar amount and an exposure-normalised loss rate.

This allows portfolio questions such as:

- Which risk grades contribute most to expected loss?
- How concentrated is credit exposure?
- How much of ECL is driven by PD versus LGD assumptions?
- How does lifetime ECL compare with the 12-month view?

## Stress testing

The stress layer is designed to distinguish **scenario assumptions** from the underlying risk model.

### Historical / scenario shocks

Observed adverse regimes can be translated into transparent multipliers on PD and LGD. This makes it easy to understand exactly why stressed ECL changes.

### Macro satellite framework

A more structural extension links aggregate credit outcomes to macroeconomic conditions. Stressed macro variables are passed through default-rate and LGD satellite relationships before being propagated into portfolio ECL.

The important output is the impact on **portfolio loss**, not merely a stressed model coefficient.

## Validation philosophy

Model validation is treated as part of the model, not as an afterthought.

Key areas include:

- data-layout and missing-value controls
- target-definition checks
- loss-field reconciliation
- discrimination
- calibration
- out-of-time performance
- out-of-regime stability
- population stability
- segment-level diagnostics
- sensitivity to estimation windows and modelling choices

A particularly important distinction is between **model performance** and **model stability**. A strong in-sample or random holdout result does not establish that the model will behave similarly in a different credit regime.

## Repository structure

```text
IFRS-9-Credit-Risk-Analytics-Engine/
│
├── README.md
├── requirements.txt
├── LICENSE
│
├── src/
│   └── credit_risk/
│       ├── __init__.py
│       ├── data.py
│       ├── expected_loss.py
│       ├── portfolio.py
│       ├── risk_metrics.py
│       ├── staging.py
│       └── stress.py
│
├── notebooks/
│   └── README.md
│
├── docs/
│   └── methodology.md
│
├── tests/
│   └── test_credit_risk.py
│
├── build_notebooks.py
└── run_notebooks.py
```

The separation is intentional:

- `src/credit_risk/` contains reusable analytical functions.
- `notebooks/` is the research and presentation layer.
- `docs/` contains methodology and modelling assumptions.
- `tests/` protects the core financial calculations.
- `build_notebooks.py` and `run_notebooks.py` orchestrate the research workflow.

## Selected empirical findings

Using the public mortgage panel, the analysis identifies materially higher default and realised-loss behaviour in the 2007–09 financial crisis than in the subsequent expansion. The completed analysis reports held-out PD discrimination around **AUC 0.83**, while the realised loss calculation closely reconciles with the dataset's reported loss field.

The stress framework also demonstrates the non-linearity of credit losses: a severe downturn can increase expected loss by multiples of the baseline because **PD and LGD deteriorate together**.

These figures are empirical results from the research sample, not claims about the performance of a production banking model.

## What this project demonstrates

**Credit / finance:** PD, LGD, EAD, ECL, SICR, staging, downturn risk, calibration and portfolio stress testing.

**Quantitative:** logistic regression, severity modelling, covariance / aggregation logic, validation metrics and out-of-time testing.

**Engineering:** modular Python, data validation, reproducible research workflows, separation of computation from notebooks and unit-tested financial calculations.

## Important limitations

This is a research implementation using public data. It is **not** a production IFRS 9 engine and does not reproduce any institution's proprietary model, governance framework or accounting policy.

Important limitations include public-data coverage, definition sensitivity, incomplete recent workouts, estimation-window dependence, regime changes, potential sample-selection effects and the need for institution-specific macroeconomic scenarios and SICR policy.

## Reproducibility

1. Obtain the permitted Freddie Mac loan-level data separately.
2. Place raw data under the expected local data directory.
3. Install dependencies from `requirements.txt`.
4. Run the data assembly and research workflow.
5. Inspect generated tables and validation outputs before interpreting portfolio results.

The analytical code is intentionally transparent: a reviewer should be able to trace a portfolio loss number back through **ECL → PD/LGD/EAD → model assumptions → underlying loan data**.
