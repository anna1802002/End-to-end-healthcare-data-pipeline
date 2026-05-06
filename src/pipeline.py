from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from prefect import flow, get_run_logger, task

from src.config import (
    ARTIFACTS_DIR,
    ICEBERG_SIM_PATH,
    PHI_COLUMNS,
    PROCESSED_DATA_PATH,
    RAW_DATA_PATH,
)
from src.data_contracts import validate_patient_contract
from src.fhir_mapping import to_fhir_patient_rows
from src.privacy import encrypt_value, mask_value


@task
def extract_data(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing input data file: {path}")
    return pd.read_csv(path)


@task
def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    transformed = df.copy()
    transformed.columns = [c.strip().lower() for c in transformed.columns]
    transformed = transformed.drop_duplicates()
    transformed = validate_patient_contract(transformed)
    return transformed


@task
def apply_phi_protection(df: pd.DataFrame) -> pd.DataFrame:
    secured = df.copy()
    for column in PHI_COLUMNS:
        if column in secured.columns:
            secured[f"{column}_masked"] = secured[column].map(mask_value)
            secured[f"{column}_encrypted"] = secured[column].map(encrypt_value)
            secured = secured.drop(columns=[column])
    return secured


@task
def quality_checks(df: pd.DataFrame) -> dict:
    checks = {
        "row_count": int(len(df)),
        "null_ratio": float(df.isna().mean().mean()),
        "has_patient_id": "patient_id" in df.columns,
    }
    if checks["row_count"] == 0:
        raise ValueError("Quality check failed: dataset is empty.")
    if checks["null_ratio"] > 0.30:
        raise ValueError("Quality check failed: too many null values.")
    return checks


@task
def save_outputs(df: pd.DataFrame) -> None:
    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    ICEBERG_SIM_PATH.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    df.to_parquet(PROCESSED_DATA_PATH, index=False)
    # Iceberg table simulation artifact for portfolio demo.
    df.to_parquet(ICEBERG_SIM_PATH, index=False)

    fhir_rows = to_fhir_patient_rows(df)
    (ARTIFACTS_DIR / "fhir_patients.json").write_text(json.dumps(fhir_rows, indent=2), encoding="utf-8")


@flow(name="healthcare-compliance-pipeline")
def run_pipeline() -> None:
    logger = get_run_logger()
    logger.info("Starting compliance-first healthcare pipeline run")

    raw_df = extract_data(RAW_DATA_PATH)
    transformed = transform_data(raw_df)
    secured = apply_phi_protection(transformed)
    checks = quality_checks(secured)
    logger.info(f"Quality checks passed: {checks}")
    save_outputs(secured)


if __name__ == "__main__":
    run_pipeline()
