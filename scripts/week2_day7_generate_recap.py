#!/usr/bin/env python3
"""Week 2 Day 7: compile recap markdown from generated outputs."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

OUT_DIR = Path("outputs")
DOC_OUT = Path("docs/week2_day7_weekly_recap.md")


def fmt(v: float, digits: int = 4) -> str:
    if pd.isna(v):
        return "NA"
    return f"{v:.{digits}f}"


def main() -> None:
    day2 = pd.read_csv(OUT_DIR / "week2_day2_extraction_quality_checks.csv")
    day3 = pd.read_csv(OUT_DIR / "week2_day3_pretrend_test.csv")
    day4 = pd.read_csv(OUT_DIR / "week2_day4_day5_heterogeneity_elasticity.csv")
    day6 = pd.read_csv(OUT_DIR / "week2_day6_retention_frequency_models.csv")

    missing_fee = day2.loc[day2["check"] == "missing_fee_version_id_rate", "value"].squeeze()
    immutable_violation = day2.loc[day2["check"] == "non_immutable_version_timestamp_rate", "value"].squeeze()

    pretrend_p = day3.loc[day3["test"] == "joint_pretrend_leads_eq_zero", "p_value"].squeeze()

    new_coef = day4.loc[
        (day4["group_type"] == "user_lifecycle") & (day4["group_name"] == "new_users"),
        "coef_ln_effective_price",
    ].squeeze()
    loyal_coef = day4.loc[
        (day4["group_type"] == "user_lifecycle") & (day4["group_name"] == "loyal_users"),
        "coef_ln_effective_price",
    ].squeeze()

    retention_coef = day6.loc[day6["outcome"] == "active_next4w", "coef"].squeeze()
    freq_coef = day6.loc[day6["outcome"] == "orders_next4w", "coef"].squeeze()

    text = f"""# Week 2 Day 7 Recap — Production Continuation

## Scope completed
This Week 2 continuation implemented the four requested focus areas end-to-end with reproducible scripts, notebooks, and output artifacts.

1. **Production-style extraction with immutable fee-version timestamps**
2. **Event-study lead/lag tables with pre-trend test outputs**
3. **Heterogeneity expansions (new vs loyal users, urgency windows, market segments)**
4. **Medium-run retention/frequency elasticity outcomes**

## Key empirical highlights (synthetic panel)
- Day 2 extraction completeness: missing `fee_version_id` rate = **{fmt(missing_fee)}**
- Immutable timestamp violation rate = **{fmt(immutable_violation)}**
- Day 3 joint pre-trend p-value = **{fmt(pretrend_p)}**
- Day 4-5 elasticity proxy: new users = **{fmt(new_coef)}**, loyal users = **{fmt(loyal_coef)}**
- Day 6 medium-run outcomes: `orders_next4w` coef = **{fmt(freq_coef)}**, `active_next4w` coef = **{fmt(retention_coef)}**

## Output index
- Day 2:
  - `outputs/week2_day2_fee_version_catalog.csv`
  - `outputs/week2_day2_extraction_quality_checks.csv`
  - `outputs/week2_day2_fee_versions_over_time.png`
- Day 3:
  - `outputs/week2_day3_event_study_lead_lag_table.csv`
  - `outputs/week2_day3_pretrend_test.csv`
  - `outputs/week2_day3_event_study_plot.png`
- Day 4-5:
  - `outputs/week2_day4_day5_heterogeneity_elasticity.csv`
  - `outputs/week2_day4_day5_heterogeneity_plot.png`
- Day 6:
  - `outputs/week2_day6_retention_frequency_models.csv`
  - `outputs/week2_day6_medium_run_response_curve.png`

## Reproducibility
```bash
python scripts/week2_run_all.py
```
"""

    DOC_OUT.parent.mkdir(parents=True, exist_ok=True)
    DOC_OUT.write_text(text)
    print(f"Wrote {DOC_OUT}")


if __name__ == "__main__":
    main()
