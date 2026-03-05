# Stage 2 Step 6 — Medium-Run Retention/Frequency Outcomes

## Objective
Estimate whether higher current-stage delivered prices predict weaker medium-run activity.

## Panel construction
- Build user-stage panel from contamination-excluded sessions
- Per user-stage metrics:
  - `sessions`
  - `orders`
  - `avg_ln_effective_price`
  - operations controls (ETA, stockout)
- Forward outcomes:
  - `orders_next4w`
  - `sessions_next4w`
  - `active_next4w` (any order in next 4 weeks)

## Models
For each outcome (`orders_next4w`, `sessions_next4w`, `active_next4w`):
- Main regressor: `avg_ln_effective_price`
- Controls: current stage orders/sessions + ops controls
- Fixed effects: market + stage
- Inference: market-clustered SE

## Repro
```bash
python scripts/week2_day6_retention_frequency.py
```

## Outputs
- `outputs/week2_day6_retention_frequency_models.csv`
- `outputs/week2_day6_user_week_panel_sample.csv`
- `outputs/week2_day6_medium_run_response_curve.png`
