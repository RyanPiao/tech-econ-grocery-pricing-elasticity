#!/usr/bin/env python3
"""Stage 2 Step 6: medium-run retention/frequency elasticity outcomes."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

DATA_IN = Path("data/week2_day2_production_session_panel.csv")
OUT_DIR = Path("outputs")


def build_user_week_panel(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    d["week_start"] = d["quote_ts_local"].dt.to_period("W-SUN").dt.start_time

    agg = (
        d.groupby(["user_id", "market_id", "week_start"], as_index=False)
        .agg(
            sessions=("session_id", "count"),
            orders=("conversion", "sum"),
            avg_ln_effective_price=("ln_effective_price", "mean"),
            avg_eta_minutes=("eta_minutes", "mean"),
            avg_stockout_rate=("stockout_rate", "mean"),
        )
        .sort_values(["user_id", "week_start"])
    )

    def add_future(g: pd.DataFrame) -> pd.DataFrame:
        g = g.sort_values("week_start").copy()
        orders_vals = g["orders"].to_numpy()
        sessions_vals = g["sessions"].to_numpy()

        next4_orders = np.full(len(g), np.nan)
        next4_sessions = np.full(len(g), np.nan)
        for i in range(len(g)):
            if i + 4 < len(g):
                next4_orders[i] = orders_vals[i + 1 : i + 5].sum()
                next4_sessions[i] = sessions_vals[i + 1 : i + 5].sum()

        g["orders_next4w"] = next4_orders
        g["sessions_next4w"] = next4_sessions
        g["active_next4w"] = (g["orders_next4w"] > 0).astype(float)
        return g

    parts = [add_future(g) for _, g in agg.groupby("user_id", sort=False)]
    return pd.concat(parts, ignore_index=True)


def fit_models(panel: pd.DataFrame) -> pd.DataFrame:
    base = panel.dropna(subset=["orders_next4w", "sessions_next4w"]).copy()
    base["week_label"] = base["week_start"].astype(str)

    formulas = {
        "orders_next4w": (
            "orders_next4w ~ avg_ln_effective_price + orders + sessions + avg_eta_minutes + avg_stockout_rate "
            "+ C(market_id) + C(week_label)"
        ),
        "active_next4w": (
            "active_next4w ~ avg_ln_effective_price + orders + sessions + avg_eta_minutes + avg_stockout_rate "
            "+ C(market_id) + C(week_label)"
        ),
        "sessions_next4w": (
            "sessions_next4w ~ avg_ln_effective_price + orders + sessions + avg_eta_minutes + avg_stockout_rate "
            "+ C(market_id) + C(week_label)"
        ),
    }

    rows = []
    for outcome, formula in formulas.items():
        fit = smf.ols(formula=formula, data=base).fit(
            cov_type="cluster", cov_kwds={"groups": base["market_id"]}
        )
        target = "avg_ln_effective_price"
        rows.append(
            {
                "outcome": outcome,
                "target": target,
                "coef": fit.params.get(target, np.nan),
                "std_err": fit.bse.get(target, np.nan),
                "p_value": fit.pvalues.get(target, np.nan),
                "n_obs": int(fit.nobs),
            }
        )

    return pd.DataFrame(rows), base


def plot_response_curve(base: pd.DataFrame) -> None:
    d = base.copy()
    d["price_bin"] = pd.qcut(d["avg_ln_effective_price"], q=10, labels=False, duplicates="drop") + 1

    curve = (
        d.groupby("price_bin", as_index=False)
        .agg(
            avg_ln_effective_price=("avg_ln_effective_price", "mean"),
            mean_orders_next4w=("orders_next4w", "mean"),
            mean_active_next4w=("active_next4w", "mean"),
        )
        .sort_values("price_bin")
    )

    fig, ax1 = plt.subplots(figsize=(8.6, 4.8))
    ax1.plot(curve["avg_ln_effective_price"], curve["mean_orders_next4w"], marker="o", color="#1f77b4")
    ax1.set_xlabel("Average ln effective price (current stage)")
    ax1.set_ylabel("Mean orders in next 4 weeks", color="#1f77b4")
    ax1.tick_params(axis="y", labelcolor="#1f77b4")

    ax2 = ax1.twinx()
    ax2.plot(curve["avg_ln_effective_price"], curve["mean_active_next4w"], marker="s", color="#ff7f0e")
    ax2.set_ylabel("Pr(active in next 4 weeks)", color="#ff7f0e")
    ax2.tick_params(axis="y", labelcolor="#ff7f0e")

    plt.title("Stage 2 Step 6: Medium-Run Retention/Frequency Response")
    fig.tight_layout()
    plt.savefig(OUT_DIR / "week2_day6_medium_run_response_curve.png", dpi=170)
    plt.close()


def main() -> None:
    if not DATA_IN.exists():
        raise FileNotFoundError(
            f"{DATA_IN} missing. Run scripts/week2_day2_production_extraction.py first."
        )

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_IN, parse_dates=["quote_ts_local", "quote_ts_utc", "date"])
    df = df[df["contaminated"] == 0].copy()

    panel = build_user_week_panel(df)
    models, base = fit_models(panel)

    models.to_csv(OUT_DIR / "week2_day6_retention_frequency_models.csv", index=False)
    panel.head(1000).to_csv(OUT_DIR / "week2_day6_user_week_panel_sample.csv", index=False)

    plot_response_curve(base)

    print("Stage2 Step6 outputs generated:")
    for path in [
        OUT_DIR / "week2_day6_retention_frequency_models.csv",
        OUT_DIR / "week2_day6_user_week_panel_sample.csv",
        OUT_DIR / "week2_day6_medium_run_response_curve.png",
    ]:
        print(" -", path)


if __name__ == "__main__":
    main()
