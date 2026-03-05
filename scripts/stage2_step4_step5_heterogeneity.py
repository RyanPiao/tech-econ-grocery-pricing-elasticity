#!/usr/bin/env python3
"""Stage 2 Step 4-5: heterogeneity expansions.

Focus expansions:
- new vs loyal users
- high-urgency windows
- market segments
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

DATA_IN = Path("data/week2_day2_production_session_panel.csv")
OUT_DIR = Path("outputs")


def add_user_states(df: pd.DataFrame) -> pd.DataFrame:
    first_date = df.groupby("user_id")["date"].min().rename("user_first_date")
    out = df.merge(first_date, on="user_id", how="left")
    out["user_tenure_days"] = (out["date"] - out["user_first_date"]).dt.days

    out["is_new_user"] = (out["user_tenure_days"] <= 14).astype(int)
    out["is_loyal_user"] = (out["user_tenure_days"] >= 56).astype(int)

    p75_eta = out["eta_minutes"].quantile(0.75)
    out["high_urgency_window"] = (
        (out["eta_minutes"] >= p75_eta)
        | (out["hour_local"].between(17, 20))
        | (out["surge_fee"] >= out["surge_fee"].quantile(0.7))
    ).astype(int)

    return out


def run_model(sdf: pd.DataFrame):
    formula = (
        "conversion ~ ln_effective_price + eta_minutes + stockout_rate + rain_index "
        "+ C(market_id) + C(stage) + C(hour_local)"
    )
    return smf.ols(formula=formula, data=sdf).fit(
        cov_type="cluster", cov_kwds={"groups": sdf["market_id"]}
    )


def collect_result(group_type: str, group_name: str, sdf: pd.DataFrame) -> dict:
    if len(sdf) < 200:
        return {
            "group_type": group_type,
            "group_name": group_name,
            "n_obs": int(len(sdf)),
            "coef_ln_effective_price": np.nan,
            "std_err": np.nan,
            "p_value": np.nan,
            "mean_conversion": float(sdf["conversion"].mean()) if len(sdf) else np.nan,
            "mean_effective_price": float(sdf["effective_price"].mean()) if len(sdf) else np.nan,
        }

    fit = run_model(sdf)
    return {
        "group_type": group_type,
        "group_name": group_name,
        "n_obs": int(fit.nobs),
        "coef_ln_effective_price": fit.params.get("ln_effective_price", np.nan),
        "std_err": fit.bse.get("ln_effective_price", np.nan),
        "p_value": fit.pvalues.get("ln_effective_price", np.nan),
        "mean_conversion": float(sdf["conversion"].mean()),
        "mean_effective_price": float(sdf["effective_price"].mean()),
    }


def plot_results(out: pd.DataFrame) -> None:
    p = out.dropna(subset=["coef_ln_effective_price", "std_err"]).copy()
    p = p.sort_values("coef_ln_effective_price")

    labels = [f"{gt}: {gn}" for gt, gn in zip(p["group_type"], p["group_name"])]

    plt.figure(figsize=(9.4, 5.6))
    y = np.arange(len(p))
    plt.errorbar(
        p["coef_ln_effective_price"],
        y,
        xerr=1.96 * p["std_err"],
        fmt="o",
        capsize=3,
    )
    plt.axvline(0, color="black", linewidth=1)
    plt.yticks(y, labels)
    plt.xlabel("Elasticity proxy coefficient on ln_effective_price")
    plt.title("Stage 2 Step 4-5: Heterogeneity in Price Response")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "week2_day4_day5_heterogeneity_plot.png", dpi=170)
    plt.close()


def main() -> None:
    if not DATA_IN.exists():
        raise FileNotFoundError(
            f"{DATA_IN} missing. Run scripts/week2_day2_production_extraction.py first."
        )

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_IN, parse_dates=["quote_ts_local", "quote_ts_utc", "date"], low_memory=False)
    df = df[df["contaminated"] == 0].copy()
    df = add_user_states(df)

    rows = []

    rows.append(collect_result("user_lifecycle", "new_users", df[df["is_new_user"] == 1]))
    rows.append(collect_result("user_lifecycle", "loyal_users", df[df["is_loyal_user"] == 1]))
    rows.append(collect_result("user_lifecycle", "mid_tenure_users", df[(df["is_new_user"] == 0) & (df["is_loyal_user"] == 0)]))

    rows.append(collect_result("urgency", "high_urgency_window", df[df["high_urgency_window"] == 1]))
    rows.append(collect_result("urgency", "non_high_urgency_window", df[df["high_urgency_window"] == 0]))

    for seg, sdf in df.groupby("market_segment"):
        rows.append(collect_result("market_segment", str(seg), sdf))

    out = pd.DataFrame(rows)
    out.to_csv(OUT_DIR / "week2_day4_day5_heterogeneity_elasticity.csv", index=False)

    counts = (
        pd.DataFrame(
            {
                "new_users": [int(df["is_new_user"].sum())],
                "loyal_users": [int(df["is_loyal_user"].sum())],
                "high_urgency_sessions": [int(df["high_urgency_window"].sum())],
                "total_sessions": [int(len(df))],
            }
        )
    )
    counts.to_csv(OUT_DIR / "week2_day4_day5_segment_counts.csv", index=False)

    plot_results(out)

    print("Stage2 Step4-5 outputs generated:")
    for path in [
        OUT_DIR / "week2_day4_day5_heterogeneity_elasticity.csv",
        OUT_DIR / "week2_day4_day5_segment_counts.csv",
        OUT_DIR / "week2_day4_day5_heterogeneity_plot.png",
    ]:
        print(" -", path)


if __name__ == "__main__":
    main()
