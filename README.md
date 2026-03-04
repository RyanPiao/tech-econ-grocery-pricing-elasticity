# Tech-Econ Research Lab: Algorithmic Pricing and Demand Elasticity in App-Based Grocery Delivery

This repository documents a reproducible applied-econometrics workflow for studying demand response to delivered-price changes in app-based grocery delivery.

## Start here (primary single-page overview)
- **Executive summary:** [`docs/weekX_executive_summary.md`](docs/weekX_executive_summary.md)
- Website abstract source: [`docs/weekX_website_abstract.md`](docs/weekX_website_abstract.md)

## Research question
How does customer demand respond to changes in **effective delivered price** (delivery/service/surge fees and discounts) in the short run and medium run?

## Week 1 (completed baseline)
- Day 1 framing + review: `DAY1_problem_framing.md`, `DAY1_review.md`
- Day 2-7 baseline artifacts (identification lock, synthetic panel, EDA, baseline model, robustness, recap)

## Week 2 continuation (Day 2-Day 7, production-style extension)

### Executive summary
- `docs/weekX_executive_summary.md`

### Week2 Day2 — Production extraction with immutable fee-version timestamps
- Script: `scripts/week2_day2_production_extraction.py`
- Notebook: `notebooks/week2_day2_production_extraction.ipynb`
- Doc: `docs/week2_day2_production_extraction_spec.md`
- Outputs:
  - `data/week2_day2_production_session_panel.csv`
  - `outputs/week2_day2_fee_version_catalog.csv`
  - `outputs/week2_day2_extraction_quality_checks.csv`
  - `outputs/week2_day2_fee_version_market_share.csv`
  - `outputs/week2_day2_fee_versions_over_time.png`

### Week2 Day3 — Event-study lead/lag + pre-trend tests
- Script: `scripts/week2_day3_event_study.py`
- Notebook: `notebooks/week2_day3_event_study.ipynb`
- Doc: `docs/week2_day3_event_study_note.md`
- Outputs:
  - `outputs/week2_day3_event_study_lead_lag_table.csv`
  - `outputs/week2_day3_pretrend_test.csv`
  - `outputs/week2_day3_event_study_sample_counts.csv`
  - `outputs/week2_day3_event_study_plot.png`

### Week2 Day4-Day5 — Heterogeneity expansions
- Script: `scripts/week2_day4_day5_heterogeneity.py`
- Notebook: `notebooks/week2_day4_day5_heterogeneity.ipynb`
- Doc: `docs/week2_day4_day5_heterogeneity_note.md`
- Outputs:
  - `outputs/week2_day4_day5_heterogeneity_elasticity.csv`
  - `outputs/week2_day4_day5_segment_counts.csv`
  - `outputs/week2_day4_day5_heterogeneity_plot.png`

### Week2 Day6 — Retention/frequency medium-run outcomes
- Script: `scripts/week2_day6_retention_frequency.py`
- Notebook: `notebooks/week2_day6_retention_frequency.ipynb`
- Doc: `docs/week2_day6_retention_frequency_note.md`
- Outputs:
  - `outputs/week2_day6_retention_frequency_models.csv`
  - `outputs/week2_day6_user_week_panel_sample.csv`
  - `outputs/week2_day6_medium_run_response_curve.png`

### Week2 Day7 — Weekly continuation recap
- Script: `scripts/week2_day7_generate_recap.py`
- Output doc: `docs/week2_day7_weekly_recap.md`

---

## Repository structure

```text
.
├── README.md
├── docs/
├── notebooks/
├── outputs/
├── scripts/
├── data/
├── PLAN.md
├── DAY1_problem_framing.md
└── DAY1_review.md
```

## Reproducibility

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Week 1 baseline panel + outputs
python scripts/day2_generate_synthetic_data.py --n-sessions 60000 --seed 20260303
python scripts/day3_day5_pipeline.py

# Week 2 continuation end-to-end
python scripts/week2_run_all.py
```

## Interpretation boundary

This run uses a synthetic, reproducible mock panel for workflow validation. Coefficients in this repository should be treated as methodological artifacts, not production business estimates.

Causal claims require the credibility-gate checks defined in `docs/day2_preanalysis_lock.md` to pass on real data.
