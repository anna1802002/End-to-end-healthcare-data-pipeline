import pandas as pd
import pytest

from src.data_contracts import validate_patient_contract


def test_data_contract_passes_minimum_columns() -> None:
    df = pd.DataFrame(
        [{"patient_id": "p1", "gender": "female", "date_of_birth": "1990-01-01"}]
    )
    validated = validate_patient_contract(df)
    assert not validated.empty


def test_data_contract_fails_without_patient_id() -> None:
    df = pd.DataFrame([{"gender": "female", "date_of_birth": "1990-01-01"}])
    with pytest.raises(Exception):
        validate_patient_contract(df)
