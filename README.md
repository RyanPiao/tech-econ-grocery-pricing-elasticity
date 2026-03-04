# Tech-Econ Research Lab: Algorithmic Pricing and Demand Elasticity in App-Based Grocery Delivery

This repository documents a 7-day applied-econometrics workflow focused on demand response to algorithmic pricing in grocery delivery platforms.

## Research question
How does customer demand respond to changes in **effective delivered price** (delivery/service/surge fees and discounts) in the short run?

## Day 1 status (already completed)
- Problem framing memo (`DAY1_problem_framing.md`)
- Critical review and conditional approval (`DAY1_review.md`)
- Initial plan (`PLAN.md`)

## Day 2–7 execution artifacts

### Day 2 — Design locks + data foundation
- `docs/day2_preanalysis_lock.md`
- `docs/day2_data_extraction_spec.md`
- `scripts/day2_generate_synthetic_data.py`
- `notebooks/day2_ingestion.ipynb`

### Day 3 — EDA
- `notebooks/day3_eda.ipynb`
- `outputs/day3_missingness_table.csv`
- `outputs/day3_market_summary.csv`
- `outputs/day3_conversion_by_price_decile.csv`
- `outputs/day3_correlation_matrix.csv`
- `outputs/day3_conversion_vs_price.png`

### Day 4 — Baseline econometric model
- `notebooks/day4_baseline_model.ipynb`
- `outputs/day4_baseline_model_results.csv`
- `docs/day4_interpretation_notes.md`

### Day 5 — Robustness and sensitivity
- `notebooks/day5_robustness_sensitivity.ipynb`
- `outputs/day5_robustness_checks.csv`
- `docs/day5_limitations.md`

### Day 6 — Documentation and reproducibility polish
- `docs/day6_technical_note.md`
- `requirements.txt`

### Day 7 — Weekly recap
- `docs/day7_weekly_recap.md`

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

python scripts/day2_generate_synthetic_data.py --n-sessions 60000 --seed 20260303
python scripts/day3_day5_pipeline.py
```

## Interpretation boundary

This run uses a synthetic, reproducible mock panel for workflow validation. Coefficients in this repository should be treated as methodological artifacts, not production business estimates.

Causal claims require the credibility-gate checks defined in `docs/day2_preanalysis_lock.md` to pass on real data.
