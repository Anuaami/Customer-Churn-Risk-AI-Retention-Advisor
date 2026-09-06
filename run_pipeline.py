import pandas as pd
import numpy as np
import json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.cluster import KMeans

# ---------------------------------------------------------
# TASK 1: Explore Data as a KPI Story
# ---------------------------------------------------------
df = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')

total_customers = len(df)
overall_churn_count = (df['Churn'] == 'Yes').sum()
overall_churn_rate = (df['Churn'] == 'Yes').mean() * 100

print(f"--- TASK 1: DATA KPI EXPLORATION ---")
print(f"Total Customers: {total_customers}")
print(f"Overall Churn Count: {overall_churn_count}")
print(f"Overall Churn Rate: {overall_churn_rate:.2f}%\n")

# Churn rate by Contract
churn_by_contract = df.groupby('Contract')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
count_by_contract = df.groupby('Contract')['Churn'].count()
churn_cnt_by_contract = df.groupby('Contract')['Churn'].apply(lambda x: (x == 'Yes').sum())

print("Churn Rate by Contract Type:")
for contract, rate in churn_by_contract.items():
    print(f"  {contract}: {rate:.2f}% ({churn_cnt_by_contract[contract]}/{count_by_contract[contract]})")

# Churn rate by InternetService
churn_by_internet = df.groupby('InternetService')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
count_by_internet = df.groupby('InternetService')['Churn'].count()
churn_cnt_by_internet = df.groupby('InternetService')['Churn'].apply(lambda x: (x == 'Yes').sum())

print("\nChurn Rate by Internet Service Type:")
for iservice, rate in churn_by_internet.items():
    print(f"  {iservice}: {rate:.2f}% ({churn_cnt_by_internet[iservice]}/{count_by_internet[iservice]})")

# Correlation between tenure and Churn
df['Churn_Numeric'] = df['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)
tenure_churn_corr = df['tenure'].corr(df['Churn_Numeric'])
print(f"\nCorrelation between tenure and Churn: {tenure_churn_corr:.4f}")

# ---------------------------------------------------------
# TASK 2: Clean & Preprocess
# ---------------------------------------------------------
print("\n--- TASK 2: CLEAN & PREPROCESS ---")
blank_total_charges = (df['TotalCharges'].str.strip() == '').sum()
print(f"Blank space values in TotalCharges: {blank_total_charges}")

df['TotalCharges_Clean'] = pd.to_numeric(df['TotalCharges'].str.strip(), errors='coerce')
df['TotalCharges_Clean'] = df['TotalCharges_Clean'].fillna(0.0)

missing_tc_tenure = df[df['TotalCharges'].str.strip() == '']['tenure'].tolist()
print(f"Tenures for customers with blank TotalCharges: {missing_tc_tenure}")

target_col = 'Churn_Numeric'
feature_cols = [c for c in df.columns if c not in ['customerID', 'Churn', 'Churn_Numeric', 'TotalCharges', 'TotalCharges_Clean']]
feature_cols.append('TotalCharges_Clean')

X = df[feature_cols].copy()
y = df[target_col].copy()

numeric_cols = ['tenure', 'MonthlyCharges', 'TotalCharges_Clean']
categorical_cols = [c for c in feature_cols if c not in numeric_cols]

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_cols),
        ('cat', OneHotEncoder(drop='first', sparse_output=False), categorical_cols)
    ]
)

X_train_raw, X_test_raw, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

X_train = preprocessor.fit_transform(X_train_raw)
X_test = preprocessor.transform(X_test_raw)

cat_encoder = preprocessor.named_transformers_['cat']
cat_feature_names = cat_encoder.get_feature_names_out(categorical_cols)
all_feature_names = numeric_cols + list(cat_feature_names)

# ---------------------------------------------------------
# TASK 3: Train, Evaluate, and Check Trust
# ---------------------------------------------------------
print("\n--- TASK 3: TRAIN & EVALUATE MODELS ---")

baseline_model = LogisticRegression(random_state=42, max_iter=1000)
baseline_model.fit(X_train, y_train)

y_pred_base = baseline_model.predict(X_test)
y_prob_base = baseline_model.predict_proba(X_test)[:, 1]

print("Baseline (Logistic Regression) Metrics on Test Set:")
print(f"  Accuracy:  {accuracy_score(y_test, y_pred_base)*100:.2f}%")
print(f"  Precision: {precision_score(y_test, y_pred_base)*100:.2f}%")
print(f"  Recall:    {recall_score(y_test, y_pred_base)*100:.2f}%")
print(f"  F1 Score:  {f1_score(y_test, y_pred_base)*100:.2f}%")
print(f"  ROC-AUC:   {roc_auc_score(y_test, y_prob_base):.4f}")

complex_model = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
complex_model.fit(X_train, y_train)

y_pred_complex_train = complex_model.predict(X_train)
y_pred_complex_test = complex_model.predict(X_test)
y_prob_complex_test = complex_model.predict_proba(X_test)[:, 1]

print("\nComplex Model (Random Forest) Metrics:")
print(f"  Training Set Accuracy: {accuracy_score(y_train, y_pred_complex_train)*100:.2f}%")
print(f"  Test Set Accuracy:     {accuracy_score(y_test, y_pred_complex_test)*100:.2f}%")
print(f"  Test Set Precision:    {precision_score(y_test, y_pred_complex_test)*100:.2f}%")
print(f"  Test Set Recall:       {recall_score(y_test, y_pred_complex_test)*100:.2f}%")
print(f"  Test Set F1 Score:     {f1_score(y_test, y_pred_complex_test)*100:.2f}%")
print(f"  Test Set ROC-AUC:      {roc_auc_score(y_test, y_prob_complex_test):.4f}")

# ---------------------------------------------------------
# TASK 4: Feature Importance for Strategy
# ---------------------------------------------------------
print("\n--- TASK 4: FEATURE IMPORTANCE ---")
importances = complex_model.feature_importances_
feat_imp = pd.DataFrame({'feature': all_feature_names, 'importance': importances})
feat_imp = feat_imp.sort_values('importance', ascending=False).reset_index(drop=True)

print("Top 10 Features:")
for idx, row in feat_imp.head(10).iterrows():
    print(f"  {idx+1}. {row['feature']}: {row['importance']:.4f}")

# ---------------------------------------------------------
# TASK 5: Segment Customers for Targeting
# ---------------------------------------------------------
print("\n--- TASK 5: CUSTOMER SEGMENTATION ---")

X_all = preprocessor.transform(X)
df['Predicted_Churn_Prob'] = complex_model.predict_proba(X_all)[:, 1]

cluster_features = df[['tenure', 'MonthlyCharges', 'Predicted_Churn_Prob']].copy()
scaler_cluster = StandardScaler()
cluster_scaled = scaler_cluster.fit_transform(cluster_features)

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(cluster_scaled)

segment_stats = df.groupby('Cluster').agg(
    Customer_Count=('customerID', 'count'),
    Avg_Tenure=('tenure', 'mean'),
    Avg_MonthlyCharges=('MonthlyCharges', 'mean'),
    Avg_TotalCharges=('TotalCharges_Clean', 'mean'),
    Avg_Churn_Prob=('Predicted_Churn_Prob', 'mean'),
    Actual_Churn_Rate=('Churn_Numeric', lambda x: x.mean() * 100),
    Total_Monthly_Revenue=('MonthlyCharges', 'sum')
).reset_index()

print("Cluster Statistics:")
print(segment_stats.to_string(index=False))

# Save output to json
summary_data = {
    'total_customers': total_customers,
    'overall_churn_rate': overall_churn_rate,
    'churn_by_contract': churn_by_contract.to_dict(),
    'churn_by_internet': churn_by_internet.to_dict(),
    'tenure_churn_corr': tenure_churn_corr,
    'blank_total_charges': int(blank_total_charges),
    'baseline_test_acc': accuracy_score(y_test, y_pred_base) * 100,
    'baseline_test_rec': recall_score(y_test, y_pred_base) * 100,
    'baseline_test_prec': precision_score(y_test, y_pred_base) * 100,
    'baseline_test_f1': f1_score(y_test, y_pred_base) * 100,
    'baseline_test_auc': roc_auc_score(y_test, y_prob_base),
    'complex_train_acc': accuracy_score(y_train, y_pred_complex_train) * 100,
    'complex_test_acc': accuracy_score(y_test, y_pred_complex_test) * 100,
    'complex_test_rec': recall_score(y_test, y_pred_complex_test) * 100,
    'complex_test_prec': precision_score(y_test, y_pred_complex_test) * 100,
    'complex_test_f1': f1_score(y_test, y_pred_complex_test) * 100,
    'complex_test_auc': roc_auc_score(y_test, y_prob_complex_test),
    'top_features': feat_imp.head(10).to_dict(orient='records'),
    'segment_stats': segment_stats.to_dict(orient='records')
}

with open('summary_stats.json', 'w') as f:
    json.dump(summary_data, f, indent=2)

print("\nSummary stats written to summary_stats.json successfully!")
