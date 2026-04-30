# Project Architecture & Workflow

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│   GENETIC INFORMATION ANALYSIS FOR MAMMALIAN REGULATION     │
└─────────────────────────────────────────────────────────────┘

                    ┌──────────────────────┐
                    │   Genetic Database   │
                    │  (Mammalian Targets) │
                    └──────────┬───────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
         ┌──────▼─────────┐          ┌─────▼────────────┐
         │  Unsupervised  │          │   Supervised     │
         │   Learning     │          │   Learning       │
         └──────┬─────────┘          └─────┬────────────┘
                │                          │
        ┌───────▼────────┐         ┌───────▼──────────┐
        │  K-Means       │         │  Random Forest   │
        │  Clustering    │         │  Classifier      │
        └───────┬────────┘         └───────┬──────────┘
                │                          │
        ┌───────▼────────┐         ┌───────▼──────────┐
        │ Pattern        │         │ Risk Prediction  │
        │ Discovery      │         │ (Off-target &    │
        │ (3 Clusters)   │         │  Gene Drive)     │
        └────────────────┘         └──────────────────┘
```

## Data Pipeline

```
RAW GENETIC DATA
      │
      ├─ Conservation Score
      ├─ CRISPR Off-Target Sites
      ├─ Expression Level
      ├─ PAM Correctness
      ├─ GC Content
      └─ Gene Drive Component Flag
      │
      ▼
PREPROCESSING & SCALING
      │
      ├─ StandardScaler (for K-means)
      └─ Feature Normalization
      │
      ▼
MODEL TRAINING
      │
      ├─ K-Means (Optimal K=3)
      └─ Random Forest Classifier
      │
      ▼
OUTPUT & ANALYSIS
      │
      ├─ Cluster Identification
      ├─ Risk Classification
      ├─ Silhouette Scores
      └─ ROC/Confusion Matrices
```

## Project Components

### 1. K-Means Clustering Discovery
- **File:** `genetic_kmeans_discovery.py`
- **Algorithm:** K-Means Unsupervised Learning
- **Objective:** Discover natural groupings in genetic patterns
- **Features Used:** Conservation Score, Off-Target Sites, Expression Level
- **Optimal Clusters:** 3
- **Evaluation:** Silhouette Score, Inertia

### 2. Genetic Risk Predictor
- **File:** `genetic_risk_predictor_mammals.py`
- **Algorithm:** Random Forest Classification
- **Objective:** Predict off-target risks and gene drive components
- **Features:** Mismatches, PAM Correctness, In-Exon, Conservation Score, GC Content
- **Targets:**
  - Off-Target Risk (High/Low)
  - Gene Drive Component Detection
- **Evaluation:** ROC-AUC, Confusion Matrix, Classification Report

## Technologies

| Technology | Purpose |
|-----------|---------|
| **Python** | Core Language |
| **Scikit-Learn** | ML Algorithms (K-Means, Random Forest) |
| **Pandas** | Data Processing |
| **NumPy** | Numerical Computation |
| **Matplotlib** | Visualization |
| **Seaborn** | Statistical Visualization |

## Regulatory Challenge

The project addresses the challenge of regulating genetic information by:
1. **Identifying risky genetic patterns** through clustering
2. **Predicting off-target effects** that could affect non-target organisms
3. **Detecting unauthorized gene drives** that could spread uncontrollably
4. **Analyzing conservation scores** to understand ecosystem impact

---

*For detailed implementation, see the Python files in the repository.*
