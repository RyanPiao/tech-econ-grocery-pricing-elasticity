# Day 4 Interpretation Notes

## Baseline model set

Using non-contaminated sessions (`contaminated == 0`), we estimated:

1. **First stage:** `ln_effective_price ~ did_treat_post + controls + FE`
2. **Reduced form:** `conversion ~ did_treat_post + controls + FE`
3. **Descriptive FE:** `conversion ~ ln_effective_price + controls + FE`

Clustered standard errors at market level.

## Key outputs (from `outputs/day4_baseline_model_results.csv`)

- First-stage rollout effect on log price: **0.0252** (SE 0.0041, p < 0.001)
  - Interpretation: rollout raised effective pre-tax price by about 2.5% on average.
- Reduced-form rollout effect on conversion: **0.00123** (SE 0.00258, p = 0.63)
  - Interpretation: no statistically clear direct conversion shift in this synthetic sample.
- Implied elasticity (RF / FS): **0.0488**
  - Not reliable for causal interpretation here due weak reduced-form precision.
- Descriptive FE semi-elasticity on `ln_effective_price`: **-0.0499** (SE 0.0033, p < 0.001)
  - Interpretation: 1% increase in effective price is associated with ~0.05 pp lower conversion, descriptively.

## Credibility gate readout

- **Coverage gate:** pass in synthetic panel.
- **Consistency gate:** pass (component add-up checks clean).
- **First-stage relevance gate:** pass (strong first stage).
- **Pre-trend gate:** not fully established in this baseline artifact (requires explicit event-study leads).
- **Inference gate:** pass (clustered SE applied).

## Causal interpretation status

Given reduced-form imprecision and absence of explicit lead-coefficient table in this run, **causal claims remain provisional**. Descriptive negative price-conversion relationship is stable and directionally consistent with the data-generating process.

## Immediate next empirical step

Implement full event-study lead/lag specification and report joint lead tests before upgrading claims from descriptive to causal.
