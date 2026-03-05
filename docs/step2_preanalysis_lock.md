# Step 2 Pre-Analysis Lock

**Topic (locked):** Algorithmic pricing and demand elasticity in app-based grocery delivery

This memo closes the five Step 1 review conditions before any Step 2 extraction or estimation work.

---

## 1) Primary identification strategy (locked)

### Primary design: staggered Difference-in-Differences (DiD) on pricing-rule rollout

We treat the introduction of a revised fee algorithm as the treatment, with market-level staggered adoption dates.

- **Treated units:** markets receiving the new fee schedule
- **Controls:** not-yet-treated markets in the same calendar windows
- **Time granularity:** session-level observations with step/stage controls
- **Interpretation:** average causal effect of the rollout-induced price shift on conversion behavior, conditional on assumptions

### Fallback design (pre-committed)

If staggered rollout timing is not sufficiently clean (see credibility gates), fallback is a **user-by-time fixed-effects descriptive elasticity model** (non-causal framing).

### Activation criteria for fallback

Fallback is activated if **any** of the following fail:
1. No credible rollout timestamp mapping for >=80% of treated sessions
2. Pre-trend test fails (p < 0.10 on joint leads)
3. Severe contamination overlap (>20% treated sessions in exclusion windows)

---

## 2) Estimands and price definitions (frozen)

### Primary causal estimand (rollout-based)

\[
\theta = \frac{\Delta E[\text{Conversion}_{imt} \mid \text{Rollout}_{mt}]}{\Delta E[\ln(\text{EffectivePrice}_{imt}) \mid \text{Rollout}_{mt}]}
\]

Where \(i\) indexes sessions, \(m\) market, \(t\) time. This is a local elasticity-style estimand implied by reduced-form over first-stage effects of rollout.

### Secondary descriptive estimand

Coefficient on \(\ln(\text{EffectivePrice}_{imt})\) from FE panel model:
- outcome: session conversion (0/1)
- interpretation: semi-elasticity (pp change in conversion per 1% price change), descriptive unless identification gates pass.

### Frozen price variable definitions

- **EffectivePrice (pre-tax, customer-facing):**
  - `item_subtotal + delivery_fee + service_fee + surge_fee - discount_total`
- **TotalPaid (post-tax):**
  - `EffectivePrice + taxes`
- **Primary price regressor:** `ln_effective_price = ln(EffectivePrice)`
- **Outcomes:**
  1. `conversion` (session-level binary)
  2. `order_value` (conditional on conversion, pre-tax)
  3. `items_count` (conditional on conversion)

### Explicit exclusions from primary regressor

- Taxes (included only in robustness)
- Tips
- Subscription fees not surfaced at session quote

---

## 3) Extraction specification (final)

Final extraction schema and joins are documented in:
- `docs/day2_data_extraction_spec.md`

Locked extraction grain:
- **One row per session quote exposure** (including non-converting sessions)

Required joins:
1. Quote events (price components)
2. Session outcomes (conversion/order)
3. Market rollout calendar
4. Context controls (ETA, stockout, weather proxies)

---

## 4) Contamination rules (defined)

A session is excluded from primary causal estimation if any of:

1. **Major promo campaign overlap:** within +/- 3 days of a major campaign launch in market
2. **Concurrent pricing experiment overlap:** session flagged as belonging to separate fee experiment
3. **Platform outage/incident windows:** marked operational anomaly window
4. **Ambiguous pricing snapshot:** missing or inconsistent component sums

Contamination windows are encoded and reported as exclusion rates by market/stage.

---

## 5) Credibility gates (go/no-go)

Primary causal interpretation is allowed only if all gates pass:

1. **Coverage gate:** >=95% non-missing on `EffectivePrice`, `conversion`, market-time keys
2. **Consistency gate:** >=99% component add-up integrity (`components -> EffectivePrice/TotalPaid`)
3. **Pre-trend gate:** event-study lead coefficients jointly not different from zero (p >= 0.10)
4. **First-stage relevance gate:** rollout -> `ln_effective_price` F-stat >= 10
5. **Inference gate:** clustered SE at market-stage (or market when sparse)
6. **Sensitivity gate:** sign and order of magnitude robust across predefined alternate specs

If any gate fails, all elasticity statements are explicitly labeled **descriptive/non-causal**.

---

## Lock timestamp

- Locked on: 2026-03-03 (America/New_York)
- Applies to Step 2–Step 7 workflow unless superseded by a documented amendment.
