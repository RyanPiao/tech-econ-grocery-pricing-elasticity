#!/usr/bin/env python3
"""Run Stage 2 Step2-Step7 continuation end-to-end."""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=ROOT)


def main() -> None:
    # Ensure base panel exists and is reproducible for this run.
    run(["python", "scripts/day2_generate_synthetic_data.py", "--n-sessions", "60000", "--seed", "20260303"])

    run(["python", "scripts/week2_day2_production_extraction.py"])
    run(["python", "scripts/week2_day3_event_study.py"])
    run(["python", "scripts/week2_day4_day5_heterogeneity.py"])
    run(["python", "scripts/week2_day6_retention_frequency.py"])
    run(["python", "scripts/week2_day7_generate_recap.py"])

    print("Stage 2 continuation complete.")


if __name__ == "__main__":
    main()
