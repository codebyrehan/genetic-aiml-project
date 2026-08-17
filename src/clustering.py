from functools import lru_cache

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

FEATURES = ["conservation_score", "off_target_sites", "expression_level"]

@lru_cache(maxsize=1)
def build_clusters():
    rng = np.random.default_rng(42)
    n = 300
    data = np.column_stack([
        np.clip(rng.normal(0.70, 0.18, n), 0, 1),
        rng.poisson(3, n).astype(float),
        np.clip(rng.normal(0.55, 0.20, n), 0, 1),
    ])
    scaler = StandardScaler()
    scaled = scaler.fit_transform(data)
    scores = {}
    for k in range(2, 7):
        labels = KMeans(n_clusters=k, random_state=42, n_init=20).fit_predict(scaled)
        scores[k] = round(float(silhouette_score(scaled, labels)), 4)
    best_k = max(scores, key=scores.get)
    model = KMeans(n_clusters=best_k, random_state=42, n_init=20)
    labels = model.fit_predict(scaled)
    centers = scaler.inverse_transform(model.cluster_centers_)
    return data, labels, best_k, scores, centers

def summary():
    data, labels, best_k, scores, _ = build_clusters()
    clusters = []
    for idx in range(best_k):
        members = data[labels == idx]
        clusters.append({
            "cluster": idx + 1,
            "size": int(len(members)),
            "conservation": round(float(members[:, 0].mean()), 3),
            "off_target_sites": round(float(members[:, 1].mean()), 2),
            "expression": round(float(members[:, 2].mean()), 3),
        })
    return {"algorithm":"K-Means", "best_k":best_k, "silhouette_scores":scores, "clusters":clusters, "features":FEATURES, "data_type":"synthetic educational"}
