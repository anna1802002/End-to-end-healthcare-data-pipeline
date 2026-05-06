from __future__ import annotations

from typing import Any

import pandas as pd
from jsonschema import validate


FHIR_PATIENT_SCHEMA = {
    "type": "object",
    "required": ["resourceType", "id", "meta"],
    "properties": {
        "resourceType": {"const": "Patient"},
        "id": {"type": "string"},
        "gender": {"type": "string"},
        "birthDate": {"type": "string"},
        "meta": {"type": "object"},
    },
}


def to_fhir_patient_rows(df: pd.DataFrame) -> list[dict[str, Any]]:
    """Map tabular patient rows into lightweight FHIR-like Patient resources."""
    resources: list[dict[str, Any]] = []
    for _, row in df.iterrows():
        resource = {
            "resourceType": "Patient",
            "id": str(row.get("patient_id", "")),
            "gender": str(row.get("gender", "unknown")).lower(),
            "birthDate": str(row.get("date_of_birth", "")),
            "meta": {"profile": ["http://hl7.org/fhir/StructureDefinition/Patient"]},
        }
        validate(resource, FHIR_PATIENT_SCHEMA)
        resources.append(resource)
    return resources
