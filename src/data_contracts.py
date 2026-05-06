from __future__ import annotations

import pandera as pa
from pandera import Column, DataFrameSchema


PATIENT_SCHEMA = DataFrameSchema(
    {
        "patient_id": Column(str, nullable=False),
        "gender": Column(str, nullable=True),
        "date_of_birth": Column(str, nullable=True),
    },
    strict=False,
    coerce=True,
)


def validate_patient_contract(df):
    """Validate incoming dataframe against minimum data contract."""
    return PATIENT_SCHEMA.validate(df, lazy=True)
