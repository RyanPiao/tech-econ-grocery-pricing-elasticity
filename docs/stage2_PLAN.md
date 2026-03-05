# Stage 2 Plan — Production Extraction and Causal-Readiness Extensions

## Context
Stage 1 delivered a reproducible synthetic pipeline and a baseline econometric workflow. The immediate Stage 2 goal is to migrate the design to production-grade inputs and close the highest-priority evidence gaps documented in `docs/day7_weekly_recap.md` and `docs/day5_limitations.md`.

## Stage 2 objective
Upgrade the project from a workflow-validating baseline to a **decision-ready empirical package** with:
1. production extraction tied to immutable fee-version timestamps,
2. explicit event-study lead/lag and pre-trend outputs,
3. predefined heterogeneity expansions, and
4. medium-run retention/frequency outcomes.

## Workstreams and deliverables

### 1) Production extraction with immutable fee-version timestamps
**Goal:** Ensure each quote exposure is linked to the exact pricing-rule version active at quote time.

**Step 1–2 tasks**
- Finalize the production extraction contract (fields, grain, and join keys).
- Add immutable version-time fields (e.g., fee schedule/version ID + valid-from timestamp).
- Define deterministic backfill and tie-break rules when version history overlaps.
- Add QA checks for version coverage, one-to-one quote-version mapping, and timestamp integrity.

**Planned outputs**
- Updated extraction spec addendum in `docs/`
- Data QA table for version-link coverage and integrity in `outputs/`

---

### 2) Event-study lead/lag + pre-trend outputs
**Goal:** Move from provisional causal framing to explicit dynamic-treatment diagnostics.

**Step 2–3 tasks**
- Implement event-time construction around rollout/fee-version change events.
- Estimate lead/lag coefficients with pre-specified omitted reference period.
- Produce joint pre-trend tests and lead-coefficient summary table.
- Export event-study plot and machine-readable coefficient table.

**Planned outputs**
- Event-study coefficient table (CSV)
- Pre-trend joint test summary (CSV/markdown)
- Event-study figure (PNG)

---

### 3) Heterogeneity expansions
**Goal:** Quantify where elasticity differs most across user state and market context.

**Step 3–4 tasks**
- Lock segment definitions:
  - **new vs loyal users**,
  - **high-urgency windows** (time/context definition),
  - **market segments** (size/maturity/operational class).
- Run interaction/spec-split analyses using the same core model structure.
- Report sample sizes and uncertainty alongside point estimates.

**Planned outputs**
- Heterogeneity result table by segment (CSV)
- Short interpretation memo in `docs/`

---

### 4) Retention/frequency medium-run outcomes
**Goal:** Extend beyond immediate conversion to medium-run behavioral response.

**Step 4–5 tasks**
- Build user-step (or user-stage) outcome panel linked to treatment exposure.
- Define medium-run outcomes (repeat ordering and order frequency windows).
- Estimate reduced-form and price-linked responses for retention/frequency outcomes.
- Document interpretation limits where horizon censoring or exposure history is incomplete.

**Planned outputs**
- Retention/frequency outcome table(s) in `outputs/`
- Methods note for horizon definitions and censoring treatment in `docs/`

## Step 1 focus (this handoff)
Step 1 of Stage 2 is a framing and lock step. Immediate objective is to finalize:
- production extraction contract with immutable fee-version logic,
- event-study design choices (window, reference period, inference),
- heterogeneity segment definitions,
- medium-run outcome definitions and minimum data requirements.

Detailed Step 1 framing memo: `docs/week2_DAY1_problem_framing.md`.

## Success criteria for Stage 2 completion
- Production extraction can reproduce a clean analysis-ready panel with version-time lineage.
- Event-study outputs include lead/lag table, plot, and explicit pre-trend diagnostics.
- Heterogeneity results cover all three planned segmentation axes with transparent sample accounting.
- Retention/frequency outcomes are estimated with clearly stated horizon and identification limits.

## Boundary conditions
- No causal overstatement if pre-trend/identification diagnostics are weak.
- Keep model interpretation aligned with credibility-gate logic from `docs/day2_preanalysis_lock.md`.
- Preserve reproducibility discipline: locked definitions, explicit QA, and exportable outputs.
