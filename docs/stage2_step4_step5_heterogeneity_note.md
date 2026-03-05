# Stage 2 Step 4-5 — Heterogeneity Expansions

## Objective
Expand elasticity analysis across user lifecycle, urgency, and market segment dimensions.

## Segments
1. **User lifecycle**
   - New users: tenure <= 14 days
   - Loyal users: tenure >= 56 days
   - Mid-tenure users: otherwise
2. **Urgency windows**
   - High-urgency sessions (ETA p75+, evening peak, or high surge)
   - Non-high-urgency sessions
3. **Market segments**
   - Dense urban
   - Suburban
   - Mixed regional

## Estimation
Within each subgroup:
- Outcome: `conversion`
- Regressor of interest: `ln_effective_price`
- Controls: ETA, stockout, rain, market/stage/hour fixed effects
- Inference: market-clustered SE

## Repro
```bash
python scripts/week2_day4_day5_heterogeneity.py
```

## Outputs
- `outputs/week2_day4_day5_heterogeneity_elasticity.csv`
- `outputs/week2_day4_day5_segment_counts.csv`
- `outputs/week2_day4_day5_heterogeneity_plot.png`
