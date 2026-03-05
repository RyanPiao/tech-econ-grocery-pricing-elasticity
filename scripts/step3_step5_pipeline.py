#!/usr/bin/env python3
"""Generate Step 3-5 outputs from synthetic grocery pricing panel."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

DATA_PATH = Path("data/synthetic_session_panel.csv")
OUT_DIR = Path("outputs")


def cluster_fit(formula: str, df: pd.DataFrame, group_col: str = "market_id"):
    return smf.ols(formula=formula, data=df).fit(
        cov_type="cluster", cov_kwds={"groups": df[group_col]}
    )


def day3_outputs(df: pd.DataFrame) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    key_cols = ["effective_price", "conversion", "market_id", "stage", "eta_minutes", "stockout_rate"]
    missingness = (
        df[key_cols]
        .isna()
        .mean()
        .rename("missing_rate")
        .reset_index()
        .rename(columns={"index": "variable"})
    )
    missingness.to_csv(OUT_DIR / "day3_missingness_table.csv", index=False)

    summary_market = (
        df.groupby("market_id", as_index=False)
        .agg(
            sessions=("session_id", "count"),
            conversion_rate=("conversion", "mean"),
            mean_effective_price=("effective_price", "mean"),
            contaminated_rate=("contaminated", "mean"),
        )
        .sort_values("market_id")
    )
    summary_market.to_csv(OUT_DIR / "day3_market_summary.csv", index=False)

    dec = df.copy()
    dec["price_decile"] = pd.qcut(dec["effective_price"], q=10, labels=False, duplicates="drop") + 1
    decile_tab = (
        dec.groupby("price_decile", as_index=False)
        .agg(
            conversion_rate=("conversion", "mean"),
            mean_effective_price=("effective_price", "mean"),
            n=("session_id", "count"),
        )
        .sort_values("price_decile")
    )
    decile_tab.to_csv(OUT_DIR / "day3_conversion_by_price_decile.csv", index=False)

    plt.figure(figsize=(7, 4))
    plt.plot(decile_tab["mean_effective_price"], decile_tab["conversion_rate"], marker="o")
    plt.title("Step 3: Conversion vs Effective Price Deciles")
    plt.xlabel("Mean effective price (USD, pre-tax)")
    plt.ylabel("Conversion rate")
    plt.grid(alpha=0.2)
    plt.tight_layout()
    plt.savefig(OUT_DIR / "day3_conversion_vs_price.png", dpi=160)
    plt.close()

    corr = (
        df[["conversion", "effective_price", "eta_minutes", "stockout_rate", "rain_index", "order_value"]]
        .corr()
        .reset_index()
        .rename(columns={"index": "variable"})
    )
    corr.to_csv(OUT_DIR / "day3_correlation_matrix.csv", index=False)


def day4_outputs(df_clean: pd.DataFrame) -> pd.DataFrame:
    fs = cluster_fit(
        "ln_effective_price ~ did_treat_post + eta_minutes + stockout_rate + rain_index + C(market_id) + C(stage) + C(hour_local)",
        df_clean,
    )
    rf = cluster_fit(
        "conversion ~ did_treat_post + eta_minutes + stockout_rate + rain_index + C(market_id) + C(stage) + C(hour_local)",
        df_clean,
    )
    fe = cluster_fit(
        "conversion ~ ln_effective_price + eta_minutes + stockout_rate + rain_index + C(market_id) + C(stage) + C(hour_local)",
        df_clean,
    )

    fs_b = fs.params.get("did_treat_post", np.nan)
    rf_b = rf.params.get("did_treat_post", np.nan)
    implied = rf_b / fs_b if pd.notna(fs_b) and abs(fs_b) > 1e-8 else np.nan

    rows = [
        {
            "model": "first_stage_price",
            "target": "did_treat_post",
            "coef": fs_b,
            "std_err": fs.bse.get("did_treat_post", np.nan),
            "p_value": fs.pvalues.get("did_treat_post", np.nan),
            "n_obs": int(fs.nobs),
        },
        {
            "model": "reduced_form_conversion",
            "target": "did_treat_post",
            "coef": rf_b,
            "std_err": rf.bse.get("did_treat_post", np.nan),
            "p_value": rf.pvalues.get("did_treat_post", np.nan),
            "n_obs": int(rf.nobs),
        },
        {
            "model": "implied_elasticity_rf_over_fs",
            "target": "conversion wrt ln_effective_price",
            "coef": implied,
            "std_err": np.nan,
            "p_value": np.nan,
            "n_obs": int(rf.nobs),
        },
        {
            "model": "fe_descriptive",
            "target": "ln_effective_price",
            "coef": fe.params.get("ln_effective_price", np.nan),
            "std_err": fe.bse.get("ln_effective_price", np.nan),
            "p_value": fe.pvalues.get("ln_effective_price", np.nan),
            "n_obs": int(fe.nobs),
        },
    ]

    out = pd.DataFrame(rows)
    out.to_csv(OUT_DIR / "day4_baseline_model_results.csv", index=False)
    return out


def day5_outputs(df: pd.DataFrame) -> pd.DataFrame:
    specs: list[tuple[str, pd.DataFrame, str]] = []

    specs.append(
        (
            "baseline_exclude_contaminated",
            df[df["contaminated"] == 0].copy(),
            "conversion ~ ln_effective_price + eta_minutes + stockout_rate + rain_index + C(market_id) + C(stage) + C(hour_local)",
        )
    )

    specs.append(
        (
            "include_contamination_controls",
            df.copy(),
            "conversion ~ ln_effective_price + major_campaign_window + other_price_experiment + eta_minutes + stockout_rate + rain_index + C(market_id) + C(stage) + C(hour_local)",
        )
    )

    alt = df[df["contaminated"] == 0].copy()
    alt["ln_total_paid"] = np.log(alt["total_paid"])
    specs.append(
        (
            "alt_price_total_paid",
            alt,
            "conversion ~ ln_total_paid + eta_minutes + stockout_rate + rain_index + C(market_id) + C(stage) + C(hour_local)",
        )
    )

    win = df[df["contaminated"] == 0].copy()
    lo, hi = np.percentile(win["effective_price"], [1, 99])
    win["effective_price_w"] = win["effective_price"].clip(lo, hi)
    win["ln_effective_price_w"] = np.log(win["effective_price_w"])
    specs.append(
        (
            "winsorized_price_1_99",
            win,
            "conversion ~ ln_effective_price_w + eta_minutes + stockout_rate + rain_index + C(market_id) + C(stage) + C(hour_local)",
        )
    )

    placebo = df[df["quote_ts_local"] < "2025-02-01"].copy()
    placebo["fake_post"] = (placebo["quote_ts_local"] >= "2025-01-20").astype(int)
    placebo["placebo_treat"] = placebo["treated_market"] * placebo["fake_post"]
    specs.append(
        (
            "placebo_preperiod_rollout",
            placebo,
            "conversion ~ placebo_treat + eta_minutes + stockout_rate + rain_index + C(market_id) + C(stage) + C(hour_local)",
        )
    )

    rows = []
    for name, sdf, formula in specs:
        model = cluster_fit(formula, sdf)
        if "ln_effective_price_w" in formula:
            target = "ln_effective_price_w"
        elif "ln_total_paid" in formula:
            target = "ln_total_paid"
        elif "placebo_treat" in formula:
            target = "placebo_treat"
        else:
            target = "ln_effective_price"

        rows.append(
            {
                "spec": name,
                "target": target,
                "coef": model.params.get(target, np.nan),
                "std_err": model.bse.get(target, np.nan),
                "p_value": model.pvalues.get(target, np.nan),
                "n_obs": int(model.nobs),
            }
        )

    out = pd.DataFrame(rows)
    out.to_csv(OUT_DIR / "day5_robustness_checks.csv", index=False)
    return out


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"{DATA_PATH} not found. Run scripts/day2_generate_synthetic_data.py first."
        )

    df = pd.read_csv(DATA_PATH, parse_dates=["quote_ts_utc", "quote_ts_local", "date"])

    day3_outputs(df)
    clean = df[df["contaminated"] == 0].copy()
    day4_outputs(clean)
    day5_outputs(df)

    print("Generated outputs:")
    for p in sorted(OUT_DIR.glob("step*.csv")):
        print(" -", p)
    for p in sorted(OUT_DIR.glob("step*.png")):
        print(" -", p)


if __name__ == "__main__":
    main()
