# Algorithm & Methods Documentation

## K-Means Clustering (Unsupervised Learning)

### Purpose
Discover natural groupings in genetic data without predefined labels.

### Algorithm Flow
```
1. Data Input (100 genetic targets)
   ↓
2. Feature Scaling (StandardScaler)
   ├─ Conservation Score
   ├─ CRISPR Off-Target Sites
   └─ Expression Level
   ↓
3. Optimal K Selection (Elbow Method + Silhouette)
   ├─ Test K = 2,3,4,5,6,7
   ├─ Calculate Inertia
   ├─ Calculate Silhouette Score
   └─ Select K = 3 (optimal)
   ↓
4. K-Means Fitting
   ├─ Initialize 3 centroids
   ├─ Assign points to nearest centroid
   ├─ Update centroids
   └─ Repeat until convergence
   ↓
5. Cluster Analysis & Visualization
   ├─ 3D scatter plot
   ├─ Cluster characteristics
   └─ Risk assessment per cluster
```

### Expected Results
- **Cluster 0:** Low-risk targets (high conservation, low off-targets)
- **Cluster 1:** Moderate-risk targets (mixed characteristics)
- **Cluster 2:** High-risk targets (low conservation, high off-targets)

---

## Random Forest Classification (Supervised Learning)

### Purpose
Predict genetic risks: off-target effects and unauthorized gene drives.

### Algorithm Flow
```
1. Data Generation (8000 CRISPR targets)
   ├─ Random DNA sequences
   ├─ Features: mismatches, PAM, exon status
   └─ Labels: off-target risk, gene drive component
   ↓
2. Feature Engineering
   ├─ Conservation Score
   ├─ GC Content
   ├─ Mismatch Count
   ├─ PAM Correctness (boolean)
   └─ In-Exon Status (boolean)
   ↓
3. Train-Test Split (70-30)
   ├─ X_train, X_test
   ├─ y_off_target (train, test)
   └─ y_eco_risk (train, test)
   ↓
4. Random Forest Training
   ├─ Number of trees: Multiple
   ├─ Max depth: Auto
   ├─ Train Model 1: Off-target prediction
   └─ Train Model 2: Gene drive detection
   ↓
5. Model Evaluation
   ├─ ROC-AUC Score
   ├─ Confusion Matrix
   ├─ Precision, Recall, F1-Score
   └─ Feature Importance
   ↓
6. Predictions & Risk Assessment
   ├─ Classify new genetic targets
   ├─ Generate risk scores
   └─ Regulatory compliance check
```

### Model Performance
- **Off-Target Risk Model**
  - Detects high-risk off-target CRISPR effects
  - Important features: mismatches, conservation score, PAM correctness
  
- **Gene Drive Detection Model**
  - Identifies unauthorized gene drive components
  - Important features: genetic construct markers, sequence patterns

---

## Feature Importance

### K-Means Features
| Feature | Role |
|---------|------|
| Conservation Score | Measures genetic evolution preservation |
| Off-Target Sites | Count of unintended cut sites |
| Expression Level | Gene activity level |

### Random Forest Features
| Feature | Impact | Role |
|---------|--------|------|
| Mismatches | HIGH | Determines specificity |
| PAM Correctness | HIGH | CRISPR binding validation |
| In-Exon | MEDIUM | Coding region detection |
| Conservation Score | MEDIUM | Evolutionary significance |
| GC Content | LOW | Sequencing stability |

---

## Regulatory Applications

### 1. Off-Target Risk Assessment
```
High Mismatches + Low Conservation
        ↓
  Random Forest Prediction
        ↓
  ⚠️ HIGH RISK: Block genetic modification
```

### 2. Gene Drive Detection
```
Unauthorized Construct Detected
        ↓
  Random Forest Classification
        ↓
  🚫 CRITICAL: Quarantine & Report
```

### 3. Pattern Discovery
```
K-Means Clustering
        ↓
  Identify Risk Clusters
        ↓
  ✅ Regulatory Guidelines: Safe vs Unsafe Zones
```

---

## Challenges Addressed

1. **Genetic Safety:** Predicting off-target CRISPR effects
2. **Ecological Risk:** Detecting gene drive components
3. **Data Regulation:** Automated classification for compliance
4. **Pattern Recognition:** Unsupervised discovery of genetic groupings

---

*This documentation supports academic AIML curriculum.*
