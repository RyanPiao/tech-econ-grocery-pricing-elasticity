#!/usr/bin/env python3
"""Stage 2 Step 2: production-style extraction with immutable fee-version timestamps.

Inputs
------
- data/synthetic_session_panel.csv

Outputs
-------
- data/week2_day2_production_session_panel.csv
- outputs/week2_day2_fee_version_catalog.csv
- outputs/week2_day2_extraction_quality_checks.csv
- outputs/week2_day2_fee_version_market_share.csv
- outputs/week2_day2_fee_versions_over_time.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DATA_IN = Path("data/synthetic_session_panel.csv")
DATA_OUT = Path("data/week2_day2_production_session_panel.csv")
OUT_DIR = Path("outputs")

MARKET_SEGMENT = {
    "MKT_A": "dense_urban",
    "MKT_B": "dense_urban",
    "MKT_C": "suburban",
    "MKT_D": "dense_urban",
    "MKT_E": "suburban",
    "MKT_F": "suburban",
    "MKT_G": "mixed_regional",
    "MKT_H": "mixed_regional",
}


def build_fee_catalog() -> pd.DataFrame:
    """Immutable fee-version catalog (simulated production dimension table)."""

    rows = [
        # MKT_A
        ("MKT_A", "A_v1", "2024-12-01 00:00:00+00:00", 2.8, 0.50, 0.30, "2024-12-01 00:00:00+00:00"),
        ("MKT_A", "A_v2", "2025-02-01 00:00:00+00:00", 3.4, 0.55, 0.32, "2025-02-01 00:00:00+00:00"),
        ("MKT_A", "A_v3", "2025-03-08 00:00:00+00:00", 3.6, 0.60, 0.35, "2025-03-08 00:00:00+00:00"),
        # MKT_B
        ("MKT_B", "B_v1", "2024-12-01 00:00:00+00:00", 2.6, 0.45, 0.28, "2024-12-01 00:00:00+00:00"),
        ("MKT_B", "B_v2", "2025-02-08 00:00:00+00:00", 3.2, 0.50, 0.30, "2025-02-08 00:00:00+00:00"),
        ("MKT_B", "B_v3", "2025-03-12 00:00:00+00:00", 3.3, 0.52, 0.32, "2025-03-12 00:00:00+00:00"),
        # MKT_C
        ("MKT_C", "C_v1", "2024-12-01 00:00:00+00:00", 2.4, 0.40, 0.26, "2024-12-01 00:00:00+00:00"),
        ("MKT_C", "C_v2", "2025-02-15 00:00:00+00:00", 3.0, 0.45, 0.28, "2025-02-15 00:00:00+00:00"),
        ("MKT_C", "C_v3", "2025-03-16 00:00:00+00:00", 3.2, 0.48, 0.30, "2025-03-16 00:00:00+00:00"),
        # MKT_D
        ("MKT_D", "D_v1", "2024-12-01 00:00:00+00:00", 3.0, 0.55, 0.34, "2024-12-01 00:00:00+00:00"),
        ("MKT_D", "D_v2", "2025-02-22 00:00:00+00:00", 3.7, 0.60, 0.36, "2025-02-22 00:00:00+00:00"),
        # MKT_E
        ("MKT_E", "E_v1", "2024-12-01 00:00:00+00:00", 2.7, 0.48, 0.30, "2024-12-01 00:00:00+00:00"),
        ("MKT_E", "E_v2", "2025-03-01 00:00:00+00:00", 3.3, 0.52, 0.33, "2025-03-01 00:00:00+00:00"),
        # MKT_F
        ("MKT_F", "F_v1", "2024-12-01 00:00:00+00:00", 2.5, 0.42, 0.27, "2024-12-01 00:00:00+00:00"),
        ("MKT_F", "F_v2", "2025-03-05 00:00:00+00:00", 2.6, 0.44, 0.28, "2025-03-05 00:00:00+00:00"),
        # MKT_G
        ("MKT_G", "G_v1", "2024-12-01 00:00:00+00:00", 2.9, 0.55, 0.33, "2024-12-01 00:00:00+00:00"),
        ("MKT_G", "G_v2", "2025-03-10 00:00:00+00:00", 3.0, 0.57, 0.34, "2025-03-10 00:00:00+00:00"),
        # MKT_H
        ("MKT_H", "H_v1", "2024-12-01 00:00:00+00:00", 2.7, 0.47, 0.30, "2024-12-01 00:00:00+00:00"),
        ("MKT_H", "H_v2", "2025-03-14 00:00:00+00:00", 2.8, 0.50, 0.31, "2025-03-14 00:00:00+00:00"),
    ]

    catalog = pd.DataFrame(
        rows,
        columns=[
            "market_id",
            "fee_version_id",
            "fee_version_effective_ts_utc",
            "base_delivery_fee",
            "weekend_addon",
            "peak_hour_addon",
            "fee_version_created_ts_utc",
        ],
    )
    catalog["fee_version_effective_ts_utc"] = pd.to_datetime(catalog["fee_version_effective_ts_utc"], utc=True)
    catalog["fee_version_created_ts_utc"] = pd.to_datetime(catalog["fee_version_created_ts_utc"], utc=True)
    return catalog.sort_values(["market_id", "fee_version_effective_ts_utc"]).reset_index(drop=True)


def assign_versions(df: pd.DataFrame, catalog: pd.DataFrame) -> pd.DataFrame:
    merged = []
    for market, sdf in df.groupby("market_id", sort=False):
        cdf = catalog[catalog["market_id"] == market].sort_values("fee_version_effective_ts_utc")
        right = cdf[[
            "fee_version_id",
            "fee_version_effective_ts_utc",
            "fee_version_created_ts_utc",
            "base_delivery_fee",
            "weekend_addon",
            "peak_hour_addon",
        ]].copy()

        tmp = sdf.sort_values("quote_ts_utc").copy()
        tmp = pd.merge_asof(
            tmp,
            right,
            left_on="quote_ts_utc",
            right_on="fee_version_effective_ts_utc",
            direction="backward",
        )
        merged.append(tmp)

    out = pd.concat(merged, ignore_index=True)

    peak_window = out["hour_local"].between(17, 20).astype(int)
    out["delivery_fee_reconstructed"] = (
        out["base_delivery_fee"]
        + out["weekend_addon"] * out["is_weekend"]
        + out["peak_hour_addon"] * peak_window
    )
    out["delivery_fee_residual"] = out["delivery_fee"] - out["delivery_fee_reconstructed"]

    out["market_segment"] = out["market_id"].map(MARKET_SEGMENT)
    out["fee_version_is_locked"] = 1
    out["extraction_run_ts_utc"] = pd.Timestamp("2026-03-03 23:00:00+00:00")

    return out


def build_quality_checks(df: pd.DataFrame, catalog: pd.DataFrame) -> pd.DataFrame:
    checks = []

    checks.append(("rows_extracted", float(len(df)), 1.0, "rows"))
    checks.append(("missing_fee_version_id_rate", float(df["fee_version_id"].isna().mean()), 0.0, "share"))
    checks.append(
        (
            "non_immutable_version_timestamp_rate",
            float((df["fee_version_created_ts_utc"] > df["quote_ts_utc"]).mean()),
            0.0,
            "share",
        )
    )

    monotonic_violations = 0
    for market, cdf in catalog.groupby("market_id"):
        if not cdf["fee_version_effective_ts_utc"].is_monotonic_increasing:
            monotonic_violations += 1
    checks.append(("catalog_monotonic_markets_violation_count", float(monotonic_violations), 0.0, "count"))

    checks.append(
        (
            "mean_abs_delivery_fee_reconstruction_error",
            float(df["delivery_fee_residual"].abs().mean()),
            np.nan,
            "usd",
        )
    )

    return pd.DataFrame(checks, columns=["check", "value", "target", "unit"])


def plot_fee_version_trend(df: pd.DataFrame) -> None:
    trend = (
        df.groupby([pd.Grouper(key="quote_ts_local", freq="W"), "fee_version_id"], as_index=False)
        .agg(sessions=("session_id", "count"))
        .sort_values("quote_ts_local")
    )

    pivot = trend.pivot(index="quote_ts_local", columns="fee_version_id", values="sessions").fillna(0)
    top_cols = pivot.sum().sort_values(ascending=False).head(6).index
    pivot = pivot[top_cols]

    plt.figure(figsize=(9, 4.8))
    pivot.plot(kind="area", stacked=True, alpha=0.85, ax=plt.gca())
    plt.title("Stage 2 Step 2: Fee-Version Usage Over Time")
    plt.ylabel("Sessions")
    plt.xlabel("Stage")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "week2_day2_fee_versions_over_time.png", dpi=170)
    plt.close()


def main() -> None:
    if not DATA_IN.exists():
        raise FileNotFoundError(f"{DATA_IN} not found. Run scripts/day2_generate_synthetic_data.py first.")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_IN, parse_dates=["quote_ts_utc", "quote_ts_local", "date"])
    df["quote_ts_utc"] = pd.to_datetime(df["quote_ts_utc"], utc=True)

    catalog = build_fee_catalog()
    extracted = assign_versions(df, catalog)

    DATA_OUT.parent.mkdir(parents=True, exist_ok=True)
    extracted.to_csv(DATA_OUT, index=False)

    catalog.to_csv(OUT_DIR / "week2_day2_fee_version_catalog.csv", index=False)

    checks = build_quality_checks(extracted, catalog)
    checks.to_csv(OUT_DIR / "week2_day2_extraction_quality_checks.csv", index=False)

    share = (
        extracted.groupby(["market_id", "fee_version_id"], as_index=False)
        .agg(sessions=("session_id", "count"))
        .sort_values(["market_id", "sessions"], ascending=[True, False])
    )
    share["session_share_market"] = share["sessions"] / share.groupby("market_id")["sessions"].transform("sum")
    share.to_csv(OUT_DIR / "week2_day2_fee_version_market_share.csv", index=False)

    plot_fee_version_trend(extracted)

    print("Stage2 Step2 outputs generated:")
    for path in [
        DATA_OUT,
        OUT_DIR / "week2_day2_fee_version_catalog.csv",
        OUT_DIR / "week2_day2_extraction_quality_checks.csv",
        OUT_DIR / "week2_day2_fee_version_market_share.csv",
        OUT_DIR / "week2_day2_fee_versions_over_time.png",
    ]:
        print(" -", path)


if __name__ == "__main__":
    main()
