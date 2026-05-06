# End-to-End Healthcare Data Pipeline

## **Overview**
This project implements an end-to-end data engineering pipeline using Python, MongoDB, and AWS S3. It automates the extraction, transformation, and loading (ETL) process for healthcare data and integrates best practices for data governance and compliance.

## **Features**
- **ETL Pipeline**: Extracts, transforms, and loads healthcare data.
- **Data Storage**:
  - Stores transformed data in MongoDB.
  - Uploads data to AWS S3 for scalable cloud storage.
- **Data Governance**:
  - Encrypts sensitive data for compliance.
  - Verifies file integrity using hashing.
- **Workflow Automation**: Automates tasks using the `schedule` library in Python.

## **Technologies Used**
- **Programming Language**: Python
- **Libraries/Tools**: Pandas, NumPy, Matplotlib, Cryptography, Boto3
- **Database**: MongoDB
- **Cloud Storage**: AWS S3

## **Portfolio Upgrade (Compliance-First v2)**
- **Orchestration**: Prefect flow in `src/pipeline.py`
- **PHI protection**: Masking + encryption in `src/privacy.py`
- **FHIR mapping**: Basic Patient resource mapping in `src/fhir_mapping.py`
- **Data contracts**: Pandera schema checks in `src/data_contracts.py`
- **Data quality**: Soda checks in `soda/checks.yml`
- **Table storage target**: Parquet outputs including an Iceberg-style table artifact
- **Pipeline scorecard**: `scripts/pipeline_scorecard.py` generates `artifacts/pipeline_scorecard.json`

## **How It Works (Short)**
1. Extract patient records from `data/raw/patients.csv`
2. Clean and normalize columns
3. Mask and encrypt PHI columns (`patient_name`, `email`, `phone`, `address`, `ssn`)
4. Run quality checks (row count, null ratio, patient id)
5. Save curated parquet + FHIR JSON artifacts

See `RUNBOOK.md` for exact setup and commands.

## **CI/CD**

- GitHub Actions workflow: `.github/workflows/ci.yml`
- Runs:
  - dependency install
  - compile checks
  - unit tests
  - scorecard generation
- CI dependency set: `requirements-ci.txt` (stable runner subset)

## **Pre-Push Verification**

```bash
python -m compileall src scripts tests
pytest -q
python -m src.pipeline
python scripts/pipeline_scorecard.py
```


