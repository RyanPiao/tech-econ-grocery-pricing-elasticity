# DAY1_review.md

## Strengths
- Clear research objective and practical business relevance (elasticity tied to conversion, frequency, basket value).
- Good Step 1 framing discipline: starts from identification risk (endogenous pricing) rather than modeling first.
- Strong initial design menu (DiD/event-study, RDD, IV, FE baseline) with stated tradeoffs.
- Data needs are mostly on target (quote exposure logs, price decomposition, promo/experiment flags, supply context).
- Reproducibility intent is explicit (assumption logging, dataset separation, versioned outputs).

## Critical risks / gaps
- **Primary identification is not yet locked.** PLAN still presents options; Step 2 could drift without a pre-committed primary design + fallback trigger.
- **Estimands are still ambiguous.** “1% price change” is stated, but exact functional form/horizon is not fixed (e.g., session conversion elasticity vs user-step frequency elasticity).
- **Price variable definition needs hard specs.** Inclusion/exclusion of taxes, item markups, and promo treatment must be standardized or estimates will be non-comparable.
- **Data feasibility risk remains open.** Step 1 asks for quote-level logs and rollout timestamps, but there is no feasibility check outcome yet.
- **Inference plan is underspecified.** No explicit clustering level, minimum sample thresholds, or go/no-go criteria for causal claims.

## Must-fix before Step 2
1. **Lock one primary identification strategy** (plus one fallback) with explicit activation criteria.
2. **Freeze estimand definitions**: exact outcome windows, denominator definitions, and elasticity functional form.
3. **Finalize a concrete extraction spec** (field name, source table, key joins, expected grain) for session-level panel.
4. **Define treatment contamination rules** for concurrent promos/experiments and exclusion windows.
5. **Set credibility gates** for Step 3/4 outputs (pre-trend pass criteria, placebo expectations, cluster scheme).

## Recommendation
**Conditional approve** — framing quality is strong and directionally correct, but Step 2 should not start until the five must-fix items above are explicitly documented.