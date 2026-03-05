# Step 6 Technical Note

## Objective
This repository provides a reproducible, academically styled weekly workflow for estimating demand sensitivity to algorithmic delivered-price variation in grocery delivery.

## Method summary

- **Primary identification lock:** staggered DiD around fee-algorithm rollout.
- **Fallback:** descriptive fixed-effects elasticity model.
- **Primary price metric:** pre-tax effective delivered price.
- **Unit of analysis:** session-level quote exposure (including non-converters).

## Directory design

- `docs/`: assumptions, locks, interpretation, limits, recap
- `scripts/`: synthetic data generator and analysis pipeline
- `notebooks/`: Step 2–5 analysis notebooks
- `outputs/`: generated tables/charts for Step 3–5
- `data/`: reproducible synthetic panel output

## Reproducibility instructions

### 1) Environment

```bash
cd /path/to/tech-econ-grocery-pricing-elasticity
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Generate synthetic dataset (Step 2)

```bash
python scripts/day2_generate_synthetic_data.py --n-sessions 60000 --seed 20260303
```

### 3) Build Step 3–5 outputs

```bash
python scripts/day3_day5_pipeline.py
```

### 4) Optional notebook workflow

Open and run notebooks in order:
1. `notebooks/day2_ingestion.ipynb`
2. `notebooks/day3_eda.ipynb`
3. `notebooks/day4_baseline_model.ipynb`
4. `notebooks/day5_robustness_sensitivity.ipynb`

## Expected outputs

- Step 3: summary tables + conversion/price chart
- Step 4: baseline econometric result table
- Step 5: robustness check table

## Guardrails

- No raw private data is committed.
- Causal claims must satisfy pre-defined credibility gates in `docs/day2_preanalysis_lock.md`.
