# Day 5 Limitations and Scope Boundaries

## Data limitations

1. **Synthetic panel, not production telemetry**
   - Outputs are workflow-validating artifacts, not business-ground truth.
2. **Constructed contamination flags**
   - Real campaign and experiment overlap can be more complex and partially observed.
3. **Simplified user behavior process**
   - No persistent user habit dynamics, latent demand shocks, or strategic app usage patterns.

## Identification limitations

1. **Rollout exogeneity remains an assumption**
   - Staggered rollout may still correlate with market-specific operations or strategy decisions.
2. **No full event-study pre-trend table in Day 4 baseline**
   - Parallel trend evidence is incomplete until explicit lead estimates are shown.
3. **Cluster count is limited in synthetic setup**
   - Inference with small number of clusters can be fragile.

## Measurement limitations

1. **Price salience may vary by UI context**
   - Session-level quoted components may not map one-to-one to what users cognitively weight.
2. **Outcome timing is short-run**
   - No retention/churn horizon in this weekly baseline.
3. **Potential omitted controls**
   - Competition intensity and inventory quality are proxied, not fully observed.

## External validity limits

- Results should not be generalized to all markets, cohorts, or categories without heterogeneity analysis on real logs.

## What would materially improve confidence

1. Production-grade quote exposure logs with immutable fee versioning.
2. Full event-study diagnostics (lead tests, dynamic effects).
3. Market-week clustered (or multiway) inference with larger treated/control count.
4. User-day retention outcomes for medium-run elasticity and welfare tradeoffs.
