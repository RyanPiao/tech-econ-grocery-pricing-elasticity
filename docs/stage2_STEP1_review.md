# Stage 2 Step 1 Review

## Scope reviewed
- `docs/week2_PLAN.md`
- `docs/week2_DAY1_problem_framing.md`
- `README.md` (Stage 2 focus section)

## Strengths
- **Clear Stage 1 → Stage 2 progression.** The plan correctly pivots from synthetic workflow validation to production-grade causal evidence.
- **Good prioritization of credibility-critical work.** The four streams (version lineage, event-study diagnostics, heterogeneity, medium-run outcomes) are the right next bottlenecks.
- **Execution framing is concrete.** Step-by-step tasking and planned outputs are specific enough to guide implementation.
- **Conservative interpretation posture is explicit.** Boundary conditions correctly state that weak diagnostics should limit causal claims.
- **Documentation alignment improved.** README now includes a dedicated Stage 2 section and points to the planning artifacts.

## Risks / gaps
- **Estimands are still not fully operationalized.** The docs describe goals, but do not yet lock exact mathematical definitions (treatment unit, elasticity scale/log form, outcome windows, denominator conventions).
- **Event-study specification remains partially underspecified.** Need explicit handling for staggered/multi-adoption settings, anticipation window policy, and exact inference design.
- **Contamination controls are not yet rule-based.** Known campaign/experiment overlaps are acknowledged, but exclusion/deconfounding rules are not locked.
- **QA thresholds are described, not gated.** Version-link QA is planned, but pass/fail cutoffs are not yet documented as hard gates.
- **Heterogeneity and medium-run expansion risk multiplicity/drift.** Segment definitions are named but not formally codified with minimum cell-size and reporting requirements.
- **README structure block is stale.** The repo tree still omits Stage 2 artifacts, which can create confusion for collaborators.

## Must-fix before execution
1. **Lock estimand spec table** in one place (treatment definition, exact outcomes, horizon windows, functional form, interpretation unit).
2. **Finalize event-study protocol**: estimator choice for staggered timing, lead/lag window, omitted period, clustering level, and pre-trend failure action.
3. **Freeze contamination policy** for concurrent promos/experiments (exclude, control, or stratify) with explicit date-window rules.
4. **Convert extraction QA into hard gates** with numeric thresholds (e.g., max unresolved version mappings, timestamp conflict tolerance).
5. **Codify heterogeneity and medium-run definitions** with deterministic segment logic, minimum sample thresholds, and censoring treatment.
6. **Update README repository structure** to include Stage 2 docs for discoverability and handoff clarity.

## Recommendation
**CONDITIONAL APPROVE**

The framing quality is strong and directionally correct. Proceed once the six must-fix items above are explicitly documented and treated as Step 2 entry criteria.