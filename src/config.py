from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = ROOT_DIR / "data" / "raw" / "patients.csv"
PROCESSED_DATA_PATH = ROOT_DIR / "data" / "processed" / "patients_curated.parquet"
ICEBERG_SIM_PATH = ROOT_DIR / "data" / "iceberg" / "patients_table.parquet"
ARTIFACTS_DIR = ROOT_DIR / "artifacts"

PHI_COLUMNS = ["patient_name", "email", "phone", "address", "ssn"]
