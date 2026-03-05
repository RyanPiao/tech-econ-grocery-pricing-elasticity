# DAY1_problem_framing.md

## Day 1 Problem Framing (Colleague Brief)

I’m starting a focused empirical workflow on **algorithmic pricing and demand elasticity in app-based grocery delivery**. My Day 1 goal is to lock the question, estimand, and identification path before touching model-heavy analysis.

## What I am trying to learn
I want a credible estimate of how customer demand responds to changes in **effective delivered price** (delivery fee + service fee + dynamic surcharge − discounts, plus item-level markup where observable).

In practical terms: if delivered price increases by 1%, how much do conversion and order frequency decline?

## Why this matters
Algorithmic pricing is now a core margin lever in grocery delivery. But without clean elasticity estimates, we risk:
- Overpricing and suppressing demand,
- Misreading promo ROI,
- Confusing short-run lift with long-run retention damage.

A rigorous elasticity estimate gives us a common language for product, growth, and marketplace decisions.

## Primary empirical challenge
Price is not randomly assigned. The algorithm often adjusts price when demand/supply conditions also shift, so naive regressions can badly bias elasticity.

My Day 1 framing therefore prioritizes **identification first**:
1. Quasi-experimental rollouts (event-study/DiD) when available,
2. Deterministic thresholds (RDD) when rule cutoffs exist,
3. Cost-side instruments only with strong exclusion diagnostics.

## Day 1 decisions I am locking
- **Estimand:** short-run own-price elasticity of demand.
- **Primary outcomes:** session conversion, order incidence, basket value.
- **Unit of analysis:** session-level panel (fallback: order-level/user-day).
- **Baseline controls:** ETA/wait-time, weather, stockout proxies, time-market fixed effects.
- **Credibility checks:** pre-trends, placebo windows, sensitivity to alternative price definitions.

## Data requirements for immediate extraction
- Quote/exposure logs (not only realized orders),
- Full price decomposition by component,
- Market-zone-time identifiers,
- Promo/experiment flags,
- Supply-side context (courier availability / operational load).

## Expected Day 1 output
By end of Day 1, I will deliver:
1. A locked analysis plan,
2. A data dictionary + extraction spec,
3. The shortlist of feasible identification strategies ranked by credibility.

## What I need from collaborators
- Confirmation of any historical pricing rule changes and rollout timestamps,
- Access to quote-level exposure events,
- A list of concurrent campaigns/experiments that could contaminate treatment periods.

If we align on these inputs today, I can move into Day 2 extraction and Day 3 baseline estimation with minimal rework.
