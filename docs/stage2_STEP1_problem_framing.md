# Stage 2 Step 1 Problem Framing (Colleague Brief)

## Purpose
Stage 1 validated the workflow on synthetic data. Stage 2 starts by locking the production-facing design decisions needed to convert that workflow into a stronger causal evidence package.

Today’s Step 1 objective is to remove ambiguity in four areas before additional modeling:
1. immutable fee-version extraction,
2. event-study lead/lag and pre-trend outputs,
3. heterogeneity expansions,
4. medium-run retention/frequency outcomes.

## What we are trying to learn in Stage 2
Beyond the baseline short-run conversion response, we need to establish:
- whether rollout-linked price changes pass explicit pre-trend diagnostics,
- where elasticity differs (user tenure, urgency context, market segment), and
- whether pricing effects propagate into medium-run ordering behavior.

## Step 1 decisions to lock

### 1) Production extraction and version lineage
- Confirm quote-level panel grain remains one row per quote exposure.
- Require fee-rule linkage fields that identify **which fee version** was active at quote time.
- Freeze timestamp precedence rules (quote timestamp, version valid-from timestamp, timezone normalization).
- Define QA checks for missing or ambiguous version mappings.

### 2) Event-study specification
- Lock event-time definition and lead/lag window.
- Lock omitted reference period and clustering strategy.
- Commit to published outputs: coefficient table, pre-trend joint test, and event-study chart.
- Maintain conservative interpretation if lead tests fail.

### 3) Heterogeneity expansion definitions
- Freeze segmentation logic for:
  - new vs loyal users,
  - high-urgency windows,
  - market segments.
- Require sample-size reporting for each subgroup estimate.
- Keep model form aligned with core baseline to preserve comparability.

### 4) Medium-run retention/frequency outcomes
- Lock outcome windows for repeat behavior analysis (user-step/user-stage panel).
- Define retention/frequency outcomes in a way that is computable from available logs.
- Document horizon censoring and incomplete-history constraints before interpretation.

## Why this framing matters
Without these Step 1 locks, Stage 2 risks producing non-comparable estimates and post-hoc specification drift. Locking extraction lineage, dynamic diagnostics, segment definitions, and horizon outcomes up front protects credibility and speeds downstream execution.

## Step 1 deliverables
- `docs/week2_PLAN.md` (execution plan and success criteria)
- `docs/week2_DAY1_problem_framing.md` (this memo)
- README update adding a dedicated **Stage 2 focus** section

## Inputs needed from collaborators
- Production data dictionary entries for fee versioning and rollout/version history.
- Confirmation of timezone conventions in quote and fee-version logs.
- Final segment taxonomy for market grouping (if operational taxonomy exists).
- Any known experiment/campaign windows likely to contaminate event-time estimates.
