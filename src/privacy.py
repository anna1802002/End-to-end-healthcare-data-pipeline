from __future__ import annotations

import base64
import hashlib
import os

from cryptography.fernet import Fernet


def _fernet_from_env() -> Fernet:
    key = os.getenv("HEALTHCARE_PIPELINE_KEY")
    if not key:
        # deterministic fallback for local demo only
        key = base64.urlsafe_b64encode(hashlib.sha256(b"local-dev-key").digest()).decode()
    return Fernet(key.encode())


def mask_value(value: object) -> str:
    text = str(value or "")
    if not text:
        return ""
    if len(text) <= 4:
        return "*" * len(text)
    return text[:2] + ("*" * (len(text) - 4)) + text[-2:]


def encrypt_value(value: object) -> str:
    fernet = _fernet_from_env()
    return fernet.encrypt(str(value or "").encode()).decode()
