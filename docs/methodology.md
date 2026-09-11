# Methodology

## Credit risk framework

The project is organised around four linked questions:

1. **How likely is default?** — estimate 12-month PD from origination characteristics.
2. **How much is lost if default occurs?** — estimate LGD from observed workout outcomes.
3. **How much is exposed?** — measure EAD at the point of default.
4. **What is the portfolio loss under accounting and stress assumptions?** — combine PD, LGD and EAD and test adverse regimes.

## PD

The baseline model uses interpretable logistic regression. For a loan `i`:

`logit(PD_i) = alpha + beta' X_i`

Origination-only variables keep the scorecard usable as a through-the-door risk measure and avoid contaminating the target with post-origination information.

Model outputs are evaluated on discrimination, calibration, rank ordering and stability across time. A rating-grade master scale can then map continuous model output into policy-relevant risk buckets.

## LGD

Mortgage recoveries are realised over a workout period rather than instantaneously. The framework therefore distinguishes nominal realised loss from an economic loss view where recoveries are discounted to the default date.

A two-part severity approach is useful where the realised-LGD distribution has a substantial zero-loss mass:

`LGD = P(material loss) × E[severity | material loss]`

This keeps the probability of a loss event separate from the size of the loss conditional on that event.

## EAD

For a fully amortising term mortgage, EAD is primarily the outstanding balance at default. There is no undrawn revolving commitment requiring a credit-conversion factor in the basic specification.

## IFRS 9 staging and ECL

The simplified implementation distinguishes:

- **Stage 1:** 12-month expected credit loss;
- **Stage 2:** lifetime expected credit loss following a significant increase in credit risk;
- **Stage 3:** lifetime expected credit loss for credit-impaired exposures.

At loan level:

`ECL = PD × LGD × EAD`

The staging engine deliberately separates the accounting policy decision (SICR/default classification) from the statistical estimation of PD and LGD.

## Stress testing

Two complementary approaches are supported conceptually:

- **Historical/scenario multipliers:** translate observed adverse regimes into transparent PD and LGD shocks.
- **Macro satellite models:** link portfolio default rates and loss severity to macroeconomic conditions, then propagate those stressed assumptions into ECL.

The key output is not merely stressed PD. It is the resulting change in **portfolio expected loss and loss rate per unit of exposure**.

## Validation and model risk

Important controls include out-of-time validation, out-of-regime testing, calibration, discrimination, PSI, loss reconciliation, segment analysis and sensitivity to estimation windows.

The public dataset is rich enough to demonstrate the framework but is not a substitute for a bank's internal risk data, approved definitions, macroeconomic forecasts, governance process or production model-validation framework.
