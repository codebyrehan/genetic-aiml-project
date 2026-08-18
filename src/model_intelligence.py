from functools import lru_cache

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix

FEATURES = ["mismatches", "pam_correct", "in_exon", "conservation_score", "gc_content"]


def synthetic_frame(seed: int = 42, n: int = 8000) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    frame = pd.DataFrame({
        "mismatches": rng.integers(0, 7, n),
        "pam_correct": rng.choice([True, False], n, p=[0.8, 0.2]),
        "in_exon": rng.choice([True, False], n, p=[0.65, 0.35]),
        "conservation_score": np.clip(rng.normal(0.7, 0.2, n), 0, 1),
        "gc_content": rng.uniform(0.3, 0.7, n),
    })
    frame["target"] = ((frame["mismatches"] <= 2) & frame["pam_correct"] & frame["in_exon"] & (frame["conservation_score"] > 0.6)).astype(int)
    return frame


@lru_cache(maxsize=1)
def model_metrics() -> dict:
    frame = synthetic_frame()
    split = int(len(frame) * 0.8)
    train, test = frame.iloc[:split], frame.iloc[split:]
    model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42, class_weight="balanced")
    model.fit(train[FEATURES], train["target"])
    pred = model.predict(test[FEATURES])
    cm = confusion_matrix(test["target"], pred, labels=[0, 1]).tolist()
    return {
        "dataset_size": len(frame),
        "train_size": len(train),
        "test_size": len(test),
        "split": "80/20 deterministic split",
        "metrics": {
            "accuracy": round(float(accuracy_score(test["target"], pred)) * 100, 2),
            "precision": round(float(precision_score(test["target"], pred, zero_division=0)) * 100, 2),
            "recall": round(float(recall_score(test["target"], pred, zero_division=0)) * 100, 2),
            "f1": round(float(f1_score(test["target"], pred, zero_division=0)) * 100, 2),
        },
        "confusion_matrix": cm,
        "features": FEATURES,
        "data_type": "synthetic educational",
    }
