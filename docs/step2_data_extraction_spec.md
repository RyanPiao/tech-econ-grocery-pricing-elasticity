# Day 2 Data Extraction Specification (Final)

## Scope
Build an analysis-ready session-level panel for estimating demand response to algorithmic delivered-price changes.

- **Panel grain:** `session_id` x quote exposure (one row per session quote)
- **Observation window (mock):** 2025-01-01 to 2025-03-31
- **Time zone handling:** store UTC and local timestamp fields

---

## Source tables (logical)

| Domain | Logical table | Grain | Purpose |
|---|---|---|---|
| Quote exposure | `quote_events` | quote/session | Price component decomposition shown to user |
| Orders/outcomes | `session_outcomes` | session | Conversion, order value, item count |
| Policy rollout | `pricing_rollout_calendar` | market-date | Treatment timing for DiD/event-study |
| Market context | `market_context_hourly` | market-hour | ETA, stockout, weather and ops proxies |
| Contamination tags | `campaign_and_experiment_flags` | market-date/session | Promo/experiment overlap exclusions |

---

## Key joins

1. `quote_events` LEFT JOIN `session_outcomes` ON `session_id`
2. JOIN `pricing_rollout_calendar` ON `market_id` with `event_ts >= rollout_ts`
3. JOIN `market_context_hourly` ON (`market_id`, `hour_bucket`)
4. LEFT JOIN contamination flags ON (`session_id`) and (`market_id`, `date`)

---

## Required fields (locked names)

### Identifiers and timing
- `session_id` (string)
- `user_id` (hashed string)
- `market_id` (string)
- `zone_id` (string)
- `store_id` (string)
- `quote_ts_utc` (timestamp)
- `quote_ts_local` (timestamp)
- `date` (date)
- `week` (ISO week index)

### Price components
- `item_subtotal` (float)
- `delivery_fee` (float)
- `service_fee` (float)
- `surge_fee` (float)
- `discount_total` (float)
- `taxes` (float)

### Constructed prices
- `effective_price` = `item_subtotal + delivery_fee + service_fee + surge_fee - discount_total`
- `total_paid` = `effective_price + taxes`
- `ln_effective_price` = `ln(effective_price)`

### Outcomes
- `conversion` (0/1)
- `order_value` (float; pre-tax, 0 if no order)
- `items_count` (int; 0 if no order)

### Controls
- `eta_minutes` (float)
- `stockout_rate` (float, 0-1)
- `rain_index` (float)
- `is_weekend` (0/1)
- `hour_local` (0-23)

### Treatment and contamination
- `treated_market` (0/1)
- `post_rollout` (0/1)
- `did_treat_post` (0/1)
- `major_campaign_window` (0/1)
- `other_price_experiment` (0/1)
- `contaminated` (0/1; OR of exclusion flags)

---

## Quality checks

1. **Missingness thresholds**
   - Critical fields (`effective_price`, `conversion`, `market_id`, `date`) <= 5% missing
2. **Price integrity**
   - `effective_price` must equal component sum within tolerance (1e-6)
   - `total_paid` must equal `effective_price + taxes`
3. **Range checks**
   - `effective_price > 0`
   - `conversion in {0,1}`
   - `stockout_rate in [0,1]`
4. **Duplicate checks**
   - `session_id` unique at panel grain

---

## Extraction output

- Primary output file: `data/synthetic_session_panel.csv` (mock reproducible analogue)
- Schema companion: this document + notebook checks in `notebooks/day2_ingestion.ipynb`

---

## Notes for real-data migration

To swap mock with production data, keep locked field names and formulas unchanged; only replace table references in extraction SQL/pipeline.
