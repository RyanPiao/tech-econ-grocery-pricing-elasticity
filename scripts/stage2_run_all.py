#!/usr/bin/env python3
"""Run Stage 2 Step2-Step7 continuation end-to-end."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=ROOT)


def main() -> None:
    # Ensure base panel exists and is reproducible for this run.
    run([sys.executable, "scripts/step2_generate_synthetic_data.py", "--n-sessions", "60000", "--seed", "20260303"])

    run([sys.executable, "scripts/stage2_step2_production_extraction.py"])
    run([sys.executable, "scripts/stage2_step3_event_study.py"])
    run([sys.executable, "scripts/stage2_step4_step5_heterogeneity.py"])
    run([sys.executable, "scripts/stage2_step6_retention_frequency.py"])
    run([sys.executable, "scripts/stage2_step7_generate_recap.py"])

    print("Stage 2 continuation complete.")


if __name__ == "__main__":
    main()
