# Week 2 Day 3 — Event-Study and Pre-Trend Diagnostics

## Objective
Estimate lead/lag treatment dynamics around rollout and produce formal pre-trend evidence.

## Design
- Sample: contamination-excluded panel from Week 2 Day 2 extract
- Event time: week difference between session date and market-specific rollout date
- Window: `[-5, +6]` event weeks; baseline omitted week `-1`
- Outcome: `conversion`
- Controls: ETA, stockout, rain, market FE, week FE, hour FE
- Inference: market-clustered SEs

## Pre-trend test
Joint F-test for all lead coefficients (`event_week <= -2`) equal to zero.

## Repro
```bash
python scripts/week2_day3_event_study.py
```

## Outputs
- `outputs/week2_day3_event_study_lead_lag_table.csv`
- `outputs/week2_day3_pretrend_test.csv`
- `outputs/week2_day3_event_study_sample_counts.csv`
- `outputs/week2_day3_event_study_plot.png`
