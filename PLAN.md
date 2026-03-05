# PLAN.md

## Project
**Topic:** Algorithmic pricing and demand elasticity in app-based grocery delivery  
**Owner:** Richeng (Tech Economist)  
**Stage:** Step 1 framing → Step 5 first empirical readout

---

## 1) Stage Objective
This stage, I want to produce a **credible first estimate of short-run demand elasticity** with respect to customer-facing delivered price in app-based grocery delivery.

By end of stage, I should have:
- A clean analysis-ready panel at the session/order level.
- A baseline elasticity estimate with transparent assumptions.
- At least one quasi-experimental specification (event-study/DiD or threshold design).
- A short note on where identification is strong vs weak, and what data gaps remain.

---

## 2) Core Research Question
How sensitive is demand for app-based grocery delivery to algorithmically adjusted prices (delivery fees, service fees, surge multipliers, and targeted promotions)?

### Operational version
When the effective delivered price increases by 1%, by how much do:
1. Session-to-order conversion,
2. Order frequency,
3. Basket size / GMV,
change in the short run?

---

## 3) Working Hypotheses

### H1 (own-price elasticity)
Demand is price-elastic in the short run (elasticity < 0), with stronger sensitivity for low-frequency and price-sensitive users.

### H2 (component salience)
Elasticity is larger for highly salient fees (delivery/service fee shown at checkout) than for less salient item-level markups.

### H3 (state dependence / timing)
Elasticity varies by urgency context (e.g., peak dinner hours, bad weather, weekend stock-up behavior).

### H4 (heterogeneity)
Elasticity differs by geography, user tenure, and basket mission (top-up vs stock-up).

---

## 4) Data Plan

## Unit of analysis (priority order)
1. **Session-level panel** (preferred): app open / browsing session with exposure to a delivered price quote.
2. **Order-level panel**: completed checkouts with full pricing decomposition.
3. **User-step panel**: frequency and spending outcomes for retention effects.

## Required fields
- **Identifiers:** user_id (hashed), market/zone_id, store_id, timestamp (local + UTC).
- **Price components:** item subtotal, delivery fee, service fee, surge/dynamic multiplier, promo/discount, taxes, total delivered price.
- **Exposure logs:** quote shown before checkout, fee schedule version, ranking/sorting context.
- **Demand outcomes:** conversion (0/1), order placed, basket value, items count, category mix.
- **Controls:** wait time ETA, stockout proxies, courier supply indicators, weather, holiday/calendar flags, local competition proxy if available.

## Minimum data quality checks
- Missingness by key fields and by market/time.
- Pricing consistency (sum of components = charged total).
- Outlier filters/winsorization policy documented.
- Time-zone normalization and duplicate handling.

---

## 5) Identification Strategy Options
I will treat this as an identification menu and select 1 primary + 1 fallback this stage.

### Option A: Event-study / DiD around pricing policy changes (preferred if available)
Use market-time variation in fee algorithm updates or pricing rule deployments.
- **Design:** compare treated vs not-yet-treated markets before/after rollout.
- **Strength:** transparent and interpretable.
- **Risk:** rollout may coincide with other interventions.

### Option B: Threshold/RDD around rule discontinuities
Exploit deterministic cutoffs (e.g., free-delivery threshold, surge trigger, basket minimum).
- **Design:** local comparison around cutoff.
- **Strength:** strong local identification when manipulation is limited.
- **Risk:** local effect only; manipulation/checks required.

### Option C: Instrumental-variables using cost-side shifters
Use exogenous supply/cost shocks (e.g., sudden courier scarcity or weather-driven cost variation) as instruments for delivered price.
- **Strength:** addresses simultaneity between demand and price.
- **Risk:** exclusion restriction may be fragile; requires careful validation.

### Option D: User fixed-effects panel (descriptive baseline)
Estimate within-user sensitivity to delivered price changes with rich FE controls.
- **Strength:** fast baseline; useful sanity check.
- **Risk:** still vulnerable to endogenous pricing and time-varying confounders.

---

## 6) Risks and Mitigations

1. **Endogenous pricing (core risk)**  
   Mitigation: prioritize quasi-experimental variation; explicitly separate causal vs descriptive estimates.

2. **Concurrent experiments/promotions**  
   Mitigation: incorporate experiment flags and promo controls; run exclusion windows around major campaigns.

3. **Measurement error in exposure**  
   Mitigation: require quote-level exposure logs; avoid using only realized order prices.

4. **Selection bias from only observed purchasers**  
   Mitigation: include non-purchase sessions where possible; model conversion explicitly.

5. **Limited external validity**  
   Mitigation: report heterogeneity by market/user segment; avoid overgeneralization.

6. **Data access/privacy constraints**  
   Mitigation: use hashed IDs, aggregate reporting, and reproducible scripts with no raw data leakage.

---

## 7) Step 1–Step 5 Execution Plan

### Step 1 (today): framing + design lock
- Finalize estimand definitions and outcome metrics.
- Decide primary identification path based on available logs.
- Draft data dictionary and extraction spec.

### Step 2: data extraction + QA
- Build first analysis dataset.
- Complete missingness, consistency, and event-timing checks.

### Step 3: baseline estimation
- Run FE baseline + simple elasticity model.
- Produce first segment-level heterogeneity tables.

### Step 4: causal specification
- Run primary quasi-experimental model (DiD/RDD/IV).
- Conduct diagnostics (pre-trends, bandwidth sensitivity, placebo checks).

### Step 5: synthesis
- Summarize findings, assumptions, and caveats.
- Write recommendation memo and next-step experiment plan.

---

## 8) Reproducibility Commitments
- Keep all assumptions in markdown (no hidden logic).
- Version analysis scripts and model outputs.
- Separate raw, intermediate, and analysis-ready datasets.
- Log every inclusion/exclusion rule.
- Provide one-command rerun for core tables/figures once data paths are configured.
