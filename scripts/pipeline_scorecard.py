from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.config import ARTIFACTS_DIR, PROCESSED_DATA_PATH


OUT = ARTIFACTS_DIR / "pipeline_scorecard.json"


def main() -> None:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    scorecard = {"status": "no_data", "checks": {}, "score_out_of_100": 0}
    if PROCESSED_DATA_PATH.exists():
        df = pd.read_parquet(PROCESSED_DATA_PATH)
        checks = {
            "has_rows": len(df) > 0,
            "has_patient_id": "patient_id" in df.columns,
            "phi_columns_removed": not any(c in df.columns for c in ["patient_name", "email", "phone", "address", "ssn"]),
        }
        score = 0
        score += 35 if checks["has_rows"] else 0
        score += 35 if checks["has_patient_id"] else 0
        score += 30 if checks["phi_columns_removed"] else 0
        scorecard = {"status": "ok", "checks": checks, "score_out_of_100": score}

    OUT.write_text(json.dumps(scorecard, indent=2), encoding="utf-8")
    print(f"Saved {OUT}")


if __name__ == "__main__":
    main()
