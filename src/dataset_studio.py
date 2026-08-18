import io

import pandas as pd

ALLOWED_FEATURES = ["mismatches", "pam_correct", "in_exon", "conservation_score", "gc_content"]


def profile_csv(raw: bytes) -> dict:
    frame = pd.read_csv(io.BytesIO(raw))
    numeric = frame.select_dtypes(include="number")
    missing = frame.isna().sum()
    return {
        "rows": int(len(frame)),
        "columns": int(len(frame.columns)),
        "column_names": frame.columns.tolist(),
        "missing_values": {k: int(v) for k, v in missing.items() if int(v) > 0},
        "numeric_summary": numeric.describe().round(4).fillna(0).to_dict(),
        "supported_features": [c for c in ALLOWED_FEATURES if c in frame.columns],
        "unsupported_features": [c for c in frame.columns if c not in ALLOWED_FEATURES],
        "data_type": "user-provided educational dataset; not stored by this endpoint",
    }
