# Healthcare Pipeline Runbook

## 1) Setup
- Create and activate a virtual environment
- Install dependencies:
  - `pip install -r requirements.txt`

## 2) Optional encryption key
- Set a Fernet-compatible key:
  - `HEALTHCARE_PIPELINE_KEY=<base64_32byte_key>`
- If not set, pipeline uses a local dev key.

## 3) Input data
- Place source CSV at `data/raw/patients.csv`.
- Expected columns include:
  - `patient_id`, `patient_name`, `email`, `phone`, `address`, `ssn`, `gender`, `date_of_birth`

## 4) Run the pipeline
- `python -m src.pipeline`

## 5) Outputs
- Curated data: `data/processed/patients_curated.parquet`
- Iceberg-style demo table artifact: `data/iceberg/patients_table.parquet`
- FHIR resources: `artifacts/fhir_patients.json`

## 6) Data quality checks
- Soda checks defined in `soda/checks.yml`.
- Integrate with CI or run in your preferred Soda workflow.
