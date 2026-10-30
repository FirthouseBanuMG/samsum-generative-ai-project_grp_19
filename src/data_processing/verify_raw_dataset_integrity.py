"""Compare raw SAMSum CSV hashes with the project's recorded local baseline.

Run with ``python -m data_processing.verify_raw_dataset_integrity`` before preprocessing.
"""

import hashlib

from project_paths import RAW_DATA_DIR

EXPECTED_SHA256 = {
    "samsum-train.csv": (
        "03CA44B69042741F82603FA4C1FD66E919519637DCE7219D327F22947DB25B42"
    ),
    "samsum-validation.csv": (
        "29A36F37B530AFF1616E6BAA0B146253F47FF6D02E2653FAA2FC3A8EBDB590F7"
    ),
    "samsum-test.csv": (
        "7104369C1CF0658B0D42FF759B3D4E23A1762B5B67DE56E3E556CD5FA63C8AF3"
    ),
}

for filename, expected_hash in EXPECTED_SHA256.items():
    path = RAW_DATA_DIR / filename
    if not path.is_file():
        raise FileNotFoundError(f"Raw dataset file not found: {path}")

    digest = hashlib.sha256(path.read_bytes()).hexdigest().upper()
    if digest != expected_hash:
        raise ValueError(
            f"Raw dataset integrity check failed for {filename}: "
            "its SHA-256 differs from the baseline recorded on 2026-10-16."
        )
    print(f"{filename}: PASS (matches 2026-10-16 SHA-256 baseline)")

print(
    "Raw dataset integrity check passed. "
    "This verifies only against the recorded local baseline."
)
