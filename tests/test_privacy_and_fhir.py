from __future__ import annotations

import pandas as pd

from src.fhir_mapping import to_fhir_patient_rows
from src.privacy import encrypt_value, mask_value


def test_mask_value_basic() -> None:
    masked = mask_value("john.doe@example.com")
    assert masked.startswith("jo")
    assert masked.endswith("om")
    assert "*" in masked


def test_encrypt_value_non_empty() -> None:
    encrypted = encrypt_value("sensitive")
    assert encrypted
    assert encrypted != "sensitive"


def test_fhir_mapping_shape() -> None:
    df = pd.DataFrame(
        [
            {
                "patient_id": "p1",
                "gender": "female",
                "date_of_birth": "1990-01-01",
            }
        ]
    )
    rows = to_fhir_patient_rows(df)
    assert len(rows) == 1
    assert rows[0]["resourceType"] == "Patient"
    assert rows[0]["id"] == "p1"
