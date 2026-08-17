from functools import lru_cache
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

FEATURES = ["mismatches", "pam_correct", "in_exon", "conservation_score", "gc_content"]

@lru_cache(maxsize=1)
def get_model():
    rng = np.random.default_rng(42)
    n = 8000
    df = pd.DataFrame({
        "mismatches": rng.integers(0, 7, n),
        "pam_correct": rng.choice([True, False], n, p=[0.8, 0.2]),
        "in_exon": rng.choice([True, False], n, p=[0.65, 0.35]),
        "conservation_score": np.clip(rng.normal(0.7, 0.2, n), 0, 1),
        "gc_content": rng.uniform(0.3, 0.7, n),
    })
    y = ((df.mismatches <= 2) & df.pam_correct & df.in_exon & (df.conservation_score > 0.6)).astype(int)
    model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42, class_weight="balanced")
    model.fit(df[FEATURES], y)
    return model

def analyze(payload: dict) -> dict:
    row = {
        "mismatches": int(payload["mismatches"]),
        "pam_correct": bool(payload["pam_correct"]),
        "in_exon": bool(payload["in_exon"]),
        "conservation_score": float(payload["conservation_score"]),
        "gc_content": float(payload["gc_content"]),
    }
    if not 0 <= row["mismatches"] <= 6 or not 0 <= row["conservation_score"] <= 1 or not 0.3 <= row["gc_content"] <= 0.7:
        raise ValueError("One or more feature values are outside the supported educational range.")
    model = get_model()
    frame = pd.DataFrame([row], columns=FEATURES)
    probability = float(model.predict_proba(frame)[0, 1])
    label = "HIGH RISK" if probability >= 0.70 else "MODERATE RISK" if probability >= 0.35 else "LOWER RISK"
    importances = dict(zip(FEATURES, model.feature_importances_))
    return {
        "risk_score": round(probability * 100, 1),
        "label": label,
        "confidence": round(max(probability, 1 - probability) * 100, 1),
        "feature_importance": {k: round(float(v), 4) for k, v in importances.items()},
        "inputs": row,
        "model": "Random Forest",
        "data_type": "synthetic educational",
    }
