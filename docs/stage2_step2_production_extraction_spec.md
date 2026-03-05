# Stage 2 Step 2 — Production Extraction Extension

## Objective
Introduce a production-style extraction layer that attaches each session quote to an **immutable fee-version record** with UTC effective timestamps.

## What was added
- Fee policy/version catalog with per-market version IDs and effective timestamps
- As-of assignment from quote timestamp to fee version (`merge_asof` by market)
- Locked fields in extracted panel:
  - `fee_version_id`
  - `fee_version_effective_ts_utc`
  - `fee_version_created_ts_utc`
  - `fee_version_is_locked`
  - `extraction_run_ts_utc`
  - `market_segment`

## Key checks
- Missing fee-version assignment rate
- Version timestamp immutability violations (`created_ts > quote_ts`)
- Monotonic effective timestamp checks within market
- Delivery fee reconstruction residual summary

## Repro
```bash
python scripts/week2_day2_production_extraction.py
```

## Outputs
- `data/week2_day2_production_session_panel.csv`
- `outputs/week2_day2_fee_version_catalog.csv`
- `outputs/week2_day2_extraction_quality_checks.csv`
- `outputs/week2_day2_fee_version_market_share.csv`
- `outputs/week2_day2_fee_versions_over_time.png`
