#!/usr/bin/env python3
"""Step 2 synthetic data generator for grocery pricing elasticity workflow.

Creates a reproducible mock session-level panel with:
- staggered pricing-rollout treatment
- decomposed price components
- contamination flags
- conversion and order outcomes
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def generate_panel(n_sessions: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    markets = ["MKT_A", "MKT_B", "MKT_C", "MKT_D", "MKT_E", "MKT_F", "MKT_G", "MKT_H"]
    treated_markets = set(markets[:5])
    rollout_dates = {
        "MKT_A": pd.Timestamp("2025-02-01"),
        "MKT_B": pd.Timestamp("2025-02-08"),
        "MKT_C": pd.Timestamp("2025-02-15"),
        "MKT_D": pd.Timestamp("2025-02-22"),
        "MKT_E": pd.Timestamp("2025-03-01"),
    }

    start = np.datetime64("2025-01-01")
    end = np.datetime64("2025-03-31")
    horizon_days = int((end - start).astype("timedelta64[D]").astype(int))

    market_id = rng.choice(markets, size=n_sessions, replace=True)
    date_offset = rng.integers(0, horizon_days + 1, size=n_sessions)
    date = pd.to_datetime(start + date_offset.astype("timedelta64[D]"))
    hour_local = rng.integers(7, 23, size=n_sessions)
    minute = rng.integers(0, 60, size=n_sessions)

    quote_ts_local = date + pd.to_timedelta(hour_local, unit="h") + pd.to_timedelta(minute, unit="m")
    quote_ts_utc = quote_ts_local + pd.to_timedelta(5, unit="h")

    user_id = [f"U{u:06d}" for u in rng.integers(0, 14000, size=n_sessions)]
    zone_id = [f"Z{z:03d}" for z in rng.integers(0, 140, size=n_sessions)]
    store_id = [f"S{s:04d}" for s in rng.integers(0, 600, size=n_sessions)]
    session_id = [f"SES{i:08d}" for i in range(n_sessions)]

    treated_market = np.array([1 if m in treated_markets else 0 for m in market_id])
    post_rollout = np.array(
        [1 if (m in rollout_dates and t >= rollout_dates[m]) else 0 for m, t in zip(market_id, quote_ts_local)]
    )
    did_treat_post = treated_market * post_rollout

    is_weekend = (pd.Series(quote_ts_local).dt.dayofweek >= 5).astype(int).to_numpy()

    market_base = {
        "MKT_A": 1.2,
        "MKT_B": 1.0,
        "MKT_C": 0.8,
        "MKT_D": 1.5,
        "MKT_E": 1.1,
        "MKT_F": 0.9,
        "MKT_G": 1.4,
        "MKT_H": 1.0,
    }

    market_fee_shift = np.array([market_base[m] for m in market_id])

    item_subtotal = np.clip(rng.normal(42.0, 11.5, size=n_sessions), 12.0, None)
    delivery_fee = np.clip(
        2.2 + market_fee_shift + 1.1 * did_treat_post + 0.55 * is_weekend + rng.normal(0, 0.6, size=n_sessions),
        0.49,
        None,
    )
    service_fee = np.clip(1.8 + 0.055 * item_subtotal + rng.normal(0, 0.28, size=n_sessions), 0.25, None)
    surge_fee = np.clip(
        0.3 + 0.4 * ((hour_local >= 17) & (hour_local <= 20)).astype(int) + rng.normal(0, 0.35, size=n_sessions),
        0,
        None,
    )

    major_campaign_window = (
        ((quote_ts_local >= "2025-02-12") & (quote_ts_local <= "2025-02-16"))
        | ((quote_ts_local >= "2025-03-10") & (quote_ts_local <= "2025-03-13"))
    ).astype(int)

    other_price_experiment = (
        (rng.random(n_sessions) < 0.05)
        * ((quote_ts_local >= "2025-02-01") & (quote_ts_local <= "2025-03-20"))
    ).astype(int)

    discount_total = np.clip(
        rng.gamma(shape=1.8, scale=1.2, size=n_sessions)
        + 0.9 * major_campaign_window
        + 0.6 * other_price_experiment,
        0,
        8.0,
    )

    taxes = np.clip(0.072 * (item_subtotal + delivery_fee + service_fee + surge_fee - discount_total), 0, None)

    effective_price = item_subtotal + delivery_fee + service_fee + surge_fee - discount_total
    total_paid = effective_price + taxes

    eta_minutes = np.clip(rng.normal(31, 8, size=n_sessions) + 2.5 * did_treat_post + 1.2 * is_weekend, 8, 70)
    stockout_rate = np.clip(rng.beta(2.4, 8.5, size=n_sessions) + 0.03 * is_weekend, 0, 0.95)
    rain_index = np.clip(rng.normal(0.2, 0.35, size=n_sessions), 0, 1)

    ln_effective_price = np.log(np.clip(effective_price, 1e-6, None))

    market_demand = {
        "MKT_A": 0.08,
        "MKT_B": 0.03,
        "MKT_C": 0.06,
        "MKT_D": -0.02,
        "MKT_E": 0.01,
        "MKT_F": 0.04,
        "MKT_G": -0.01,
        "MKT_H": 0.00,
    }
    market_term = np.array([market_demand[m] for m in market_id])

    latent = (
        1.35
        - 0.92 * ln_effective_price
        - 0.028 * eta_minutes
        - 0.55 * stockout_rate
        + 0.07 * is_weekend
        + 0.04 * rain_index
        + market_term
        + rng.normal(0, 0.22, size=n_sessions)
    )

    conversion_prob = sigmoid(latent)
    conversion = (rng.random(n_sessions) < conversion_prob).astype(int)

    order_value = conversion * np.clip(effective_price * (0.92 + rng.normal(0.08, 0.12, size=n_sessions)), 0, None)
    items_count = conversion * np.clip(np.round(rng.normal(9.5, 3.1, size=n_sessions)), 1, None)

    df = pd.DataFrame(
        {
            "session_id": session_id,
            "user_id": user_id,
            "market_id": market_id,
            "zone_id": zone_id,
            "store_id": store_id,
            "quote_ts_utc": quote_ts_utc,
            "quote_ts_local": quote_ts_local,
            "date": pd.to_datetime(quote_ts_local).normalize(),
            "stage": pd.to_datetime(quote_ts_local).isocalendar().stage.astype(int),
            "hour_local": hour_local,
            "is_weekend": is_weekend,
            "treated_market": treated_market,
            "post_rollout": post_rollout,
            "did_treat_post": did_treat_post,
            "item_subtotal": item_subtotal,
            "delivery_fee": delivery_fee,
            "service_fee": service_fee,
            "surge_fee": surge_fee,
            "discount_total": discount_total,
            "taxes": taxes,
            "effective_price": effective_price,
            "total_paid": total_paid,
            "eta_minutes": eta_minutes,
            "stockout_rate": stockout_rate,
            "rain_index": rain_index,
            "conversion": conversion,
            "order_value": order_value,
            "items_count": items_count.astype(int),
            "major_campaign_window": major_campaign_window,
            "other_price_experiment": other_price_experiment,
        }
    )

    df["contaminated"] = ((df["major_campaign_window"] == 1) | (df["other_price_experiment"] == 1)).astype(int)
    df["ln_effective_price"] = np.log(df["effective_price"])

    return df


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260303)
    parser.add_argument("--n-sessions", type=int, default=50000)
    parser.add_argument("--out", type=Path, default=Path("data/synthetic_session_panel.csv"))
    args = parser.parse_args()

    df = generate_panel(args.n_sessions, args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out, index=False)

    qa = {
        "rows": len(df),
        "conversion_rate": float(df["conversion"].mean()),
        "contaminated_rate": float(df["contaminated"].mean()),
        "treated_share": float(df["treated_market"].mean()),
    }
    print("Synthetic panel generated:")
    for k, v in qa.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
