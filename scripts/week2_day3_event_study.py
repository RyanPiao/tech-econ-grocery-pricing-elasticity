#!/usr/bin/env python3
"""Week 2 Day 3: event-study lead/lag table + pre-trend tests."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

DATA_IN = Path("data/week2_day2_production_session_panel.csv")
OUT_DIR = Path("outputs")


def infer_rollout_week(df: pd.DataFrame) -> pd.DataFrame:
    treated = df[(df["treated_market"] == 1) & (df["post_rollout"] == 1)].copy()
    rollout = treated.groupby("market_id", as_index=False)["date"].min().rename(columns={"date": "rollout_date"})
    return rollout


def fit_event_study(es_df: pd.DataFrame, event_weeks: list[int]):
    baseline = -1
    keep_weeks = [w for w in event_weeks if w != baseline]

    for w in keep_weeks:
        col = f"ev_{'m' if w < 0 else 'p'}{abs(w)}"
        es_df[col] = (es_df["event_week"] == w).astype(int)

    ev_terms = [f"ev_{'m' if w < 0 else 'p'}{abs(w)}" for w in keep_weeks]
    formula = (
        "conversion ~ "
        + " + ".join(ev_terms)
        + " + eta_minutes + stockout_rate + rain_index + C(market_id) + C(week) + C(hour_local)"
    )

    model = smf.ols(formula=formula, data=es_df).fit(
        cov_type="cluster", cov_kwds={"groups": es_df["market_id"]}
    )
    return model, ev_terms


def build_lead_lag_table(model, event_weeks: list[int]) -> pd.DataFrame:
    rows = []
    for w in event_weeks:
        if w == -1:
            rows.append(
                {
                    "event_week": w,
                    "term": "baseline_omitted",
                    "coef": 0.0,
                    "std_err": np.nan,
                    "p_value": np.nan,
                    "ci_low": np.nan,
                    "ci_high": np.nan,
                }
            )
            continue

        term = f"ev_{'m' if w < 0 else 'p'}{abs(w)}"
        coef = model.params.get(term, np.nan)
        se = model.bse.get(term, np.nan)
        rows.append(
            {
                "event_week": w,
                "term": term,
                "coef": coef,
                "std_err": se,
                "p_value": model.pvalues.get(term, np.nan),
                "ci_low": coef - 1.96 * se if pd.notna(se) else np.nan,
                "ci_high": coef + 1.96 * se if pd.notna(se) else np.nan,
            }
        )

    return pd.DataFrame(rows).sort_values("event_week")


def run_pretrend_test(model, event_weeks: list[int]) -> pd.DataFrame:
    lead_terms = [f"ev_m{abs(w)}" for w in event_weeks if w <= -2]

    if not lead_terms:
        return pd.DataFrame(
            [
                {
                    "test": "joint_pretrend_leads_eq_zero",
                    "f_stat": np.nan,
                    "p_value": np.nan,
                    "df_num": np.nan,
                    "df_denom": np.nan,
                    "terms": "",
                }
            ]
        )

    hypothesis = " = 0, ".join(lead_terms) + " = 0"
    f_test = model.f_test(hypothesis)

    return pd.DataFrame(
        [
            {
                "test": "joint_pretrend_leads_eq_zero",
                "f_stat": float(np.asarray(f_test.fvalue).item()),
                "p_value": float(np.asarray(f_test.pvalue).item()),
                "df_num": float(getattr(f_test, "df_num", np.nan)),
                "df_denom": float(getattr(f_test, "df_denom", np.nan)),
                "terms": ", ".join(lead_terms),
            }
        ]
    )


def plot_event_study(table: pd.DataFrame) -> None:
    p = table.copy().sort_values("event_week")

    plt.figure(figsize=(8.5, 4.6))
    plt.axhline(0, color="black", linewidth=1, alpha=0.8)
    plt.axvline(-1, color="gray", linewidth=1, linestyle="--", alpha=0.8)

    non_base = p[p["term"] != "baseline_omitted"]
    plt.errorbar(
        non_base["event_week"],
        non_base["coef"],
        yerr=1.96 * non_base["std_err"],
        fmt="o-",
        capsize=3,
        linewidth=1.5,
    )
    plt.scatter([-1], [0], marker="x", s=60, color="gray", label="Baseline week (-1)")

    plt.title("Week 2 Day 3: Event-Study Lead/Lag Estimates (Conversion)")
    plt.xlabel("Event week relative to rollout")
    plt.ylabel("Coefficient on event-week dummy")
    plt.legend(loc="best")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "week2_day3_event_study_plot.png", dpi=170)
    plt.close()


def main() -> None:
    if not DATA_IN.exists():
        raise FileNotFoundError(
            f"{DATA_IN} missing. Run scripts/week2_day2_production_extraction.py first."
        )

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_IN, parse_dates=["quote_ts_local", "quote_ts_utc", "date"])
    df = df[df["contaminated"] == 0].copy()

    rollout = infer_rollout_week(df)
    es = df.merge(rollout, on="market_id", how="left")
    es = es[es["rollout_date"].notna()].copy()

    es["event_week"] = ((es["date"] - es["rollout_date"]).dt.days / 7.0).astype(float).apply(np.floor).astype(int)

    event_window = list(range(-5, 7))
    es = es[es["event_week"].between(min(event_window), max(event_window))].copy()

    model, _ = fit_event_study(es, event_window)
    table = build_lead_lag_table(model, event_window)
    pretrend = run_pretrend_test(model, event_window)

    table.to_csv(OUT_DIR / "week2_day3_event_study_lead_lag_table.csv", index=False)
    pretrend.to_csv(OUT_DIR / "week2_day3_pretrend_test.csv", index=False)

    sample = (
        es.groupby("event_week", as_index=False)
        .agg(sessions=("session_id", "count"), conversion_rate=("conversion", "mean"))
        .sort_values("event_week")
    )
    sample.to_csv(OUT_DIR / "week2_day3_event_study_sample_counts.csv", index=False)

    plot_event_study(table)

    print("Week2 Day3 outputs generated:")
    for path in [
        OUT_DIR / "week2_day3_event_study_lead_lag_table.csv",
        OUT_DIR / "week2_day3_pretrend_test.csv",
        OUT_DIR / "week2_day3_event_study_sample_counts.csv",
        OUT_DIR / "week2_day3_event_study_plot.png",
    ]:
        print(" -", path)


if __name__ == "__main__":
    main()
