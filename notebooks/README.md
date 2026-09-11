# Research workflow

The repository separates reusable analytics from exploratory work.

| Notebook | Purpose |
|---|---|
| `01_data_quality` | data layout, missingness, seasoning and loan-level assembly |
| `02_pd_model` | default definition, logistic PD, scorecard and calibration |
| `03_lgd_model` | realised loss, economic LGD and severity modelling |
| `04_ead_and_staging` | exposure at default and IFRS 9 staging |
| `05_expected_credit_loss` | Stage 1/2/3 ECL aggregation |
| `06_stress_testing` | historical and macro-driven stress scenarios |
| `07_validation` | discrimination, calibration, stability and out-of-time checks |
| `08_portfolio_dashboard` | management-level portfolio risk summary |

Notebooks are the research and presentation layer. Core calculations belong in `src/credit_risk/` so that they can be tested and reused independently of notebook state.
