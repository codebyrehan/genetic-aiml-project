# ========================================================
# AIML Project: Genetic Risk Prediction in Mammals (Supervised)
# Random Forest for Off-Target + Gene Drive Detection
# ========================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve

plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# --------------------- Realistic Dataset ---------------------
np.random.seed(42)
n_samples = 8000

def random_dna(length=23):
    return ''.join(np.random.choice(['A', 'T', 'C', 'G'], length))

data = {
    'guide_sequence': [random_dna() for _ in range(n_samples)],
    'mismatches': np.random.randint(0, 7, n_samples),
    'pam_correct': np.random.choice([True, False], n_samples, p=[0.8, 0.2]),
    'in_exon': np.random.choice([True, False], n_samples, p=[0.65, 0.35]),
    'conservation_score': np.clip(np.random.normal(0.7, 0.2, n_samples), 0, 1),
    'gc_content': np.random.uniform(0.3, 0.7, n_samples),
    'is_gene_drive_component': np.random.choice([1, 0], n_samples, p=[0.04, 0.96])
}

df = pd.DataFrame(data)

# Labels
df['off_target_risk'] = ((df['mismatches'] <= 2) & df['pam_correct'] & df['in_exon'] & (df['conservation_score'] > 0.6)).astype(int)
df['ecological_risk'] = df['is_gene_drive_component']

print(f"Dataset: {n_samples} CRISPR targets | High off-target: {df['off_target_risk'].sum()} | Gene drives: {df['ecological_risk'].sum()}\n")

# Features
features = ['mismatches', 'pam_correct', 'in_exon', 'conservation_score', 'gc_content']
X = df[features]
y_off = df['off_target_risk']
y_eco = df['ecological_risk']

# Split & Train
X_train, X_test, y_off_train, y_off_test = train_test_split(X, y_off, test_size=0.3, random_state=42, stratify=y_off)
X_train_e, X_test_e, y_eco_train, y_eco_test = train_test_split(X, y_eco, test_size=0.3, random_state=42, stratify=y_eco)

clf_off = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42, class_weight='balanced')
clf_off.fit(X_train, y_off_train)

clf_eco = RandomForestClassifier(n_estimators=500, random_state=42, class_weight='balanced')
clf_eco.fit(X_train_e, y_eco_train)

# Predictions
pred_off = clf_off.predict(X_test)
pred_eco = clf_eco.predict(X_test_e)

# Results
print("="*60)
print("1. CRISPR OFF-TARGET RISK PREDICTION")
print(classification_report(y_off_test, pred_off, target_names=["Safe", "High Risk"]))
print(f"ROC-AUC: {roc_auc_score(y_off_test, clf_off.predict_proba(X_test)[:,1]):.4f}\n")

print("="*60)
print("2. GENE DRIVE / ECOLOGICAL RISK DETECTION")
print(classification_report(y_eco_test, pred_eco, target_names=["Normal", "Gene Drive"], zero_division=0))

# Plots
fig = plt.figure(figsize=(16, 10))

plt.subplot(2, 3, 1)
sns.heatmap(confusion_matrix(y_off_test, pred_off), annot=True, fmt='d', cmap='Blues',
            xticklabels=['Safe', 'High Risk'], yticklabels=['Safe', 'High Risk'])
plt.title('Off-Target Risk Confusion Matrix')

plt.subplot(2, 3, 2)
imp = pd.Series(clf_off.feature_importances_, index=features).sort_values(ascending=True)
imp.plot(kind='barh', color='skyblue', edgecolor='black')
plt.title('Feature Importance (Off-Target)')

plt.subplot(2, 3, 3)
fpr, tpr, _ = roc_curve(y_off_test, clf_off.predict_proba(X_test)[:,1])
plt.plot(fpr, tpr, label=f'AUC = {roc_auc_score(y_off_test, clf_off.predict_proba(X_test)[:,1]):.3f}')
plt.plot([0,1],[0,1],'k--')
plt.title('ROC Curve - Off-Target')
plt.xlabel('FPR'); plt.ylabel('TPR'); plt.legend()

plt.subplot(2, 3, 4)
sns.heatmap(confusion_matrix(y_eco_test, pred_eco), annot=True, fmt='d', cmap='Reds',
            xticklabels=['Normal', 'Gene Drive'], yticklabels=['Normal', 'Gene Drive'])
plt.title('Gene Drive Detection Confusion Matrix')

plt.subplot(2, 3, 5)
imp2 = pd.Series(clf_eco.feature_importances_, index=features).sort_values(ascending=True)
imp2.plot(kind='barh', color='salmon', edgecolor='black')
plt.title('Feature Importance (Gene Drive)')

plt.suptitle('AI-Powered Genetic Risk Regulation System in Mammals (Supervised Learning)', fontsize=18, fontweight='bold')
plt.tight_layout()
plt.show()

print("\nSupervised Model Demo Complete – Ready for Regulation!")