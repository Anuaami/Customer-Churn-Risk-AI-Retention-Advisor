import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.figure(figsize=(10, 6))

with open('summary_stats.json', 'r') as f:
    data = json.load(f)

df_feat = pd.DataFrame(data['top_features'])
df_top10 = df_feat.head(10).sort_values('importance', ascending=True)

# Clean feature names for clean display
display_names = {
    'tenure': 'Tenure (Months)',
    'TotalCharges_Clean': 'Total Charges ($)',
    'MonthlyCharges': 'Monthly Charges ($)',
    'InternetService_Fiber optic': 'Internet: Fiber Optic',
    'PaymentMethod_Electronic check': 'Payment: Electronic Check',
    'Contract_Two year': 'Contract: Two Year',
    'Contract_One year': 'Contract: One Year',
    'OnlineSecurity_Yes': 'Add-on: Online Security',
    'TechSupport_Yes': 'Add-on: Tech Support',
    'PaperlessBilling_Yes': 'Billing: Paperless'
}

df_top10['display_name'] = df_top10['feature'].map(lambda x: display_names.get(x, x))

colors = ['#1f77b4' if i < 7 else '#2ca02c' for i in range(len(df_top10))]
# Highlight top 3 features in distinct navy/coral
bar_colors = []
for name in df_top10['feature']:
    if name in ['tenure', 'TotalCharges_Clean', 'MonthlyCharges', 'InternetService_Fiber optic', 'PaymentMethod_Electronic check']:
        bar_colors.append('#1A365D') # Deep Navy
    else:
        bar_colors.append('#4A5568') # Slate Gray

bars = plt.barh(df_top10['display_name'], df_top10['importance'], color=bar_colors, edgecolor='none', height=0.65)

plt.title('Top 10 Feature Importances — Random Forest Churn Model', fontsize=14, fontweight='bold', pad=15, color='#1A365D')
plt.xlabel('Gini Feature Importance', fontsize=11, fontweight='bold', color='#2D3748')
plt.ylabel('Feature', fontsize=11, fontweight='bold', color='#2D3748')

# Annotate bar values
for bar in bars:
    width = bar.get_width()
    plt.text(width + 0.003, bar.get_y() + bar.get_height()/2, f'{width:.4f} ({width*100:.1f}%)', 
             va='center', ha='left', fontsize=9, fontweight='bold', color='#2D3748')

plt.xlim(0, 0.26)
plt.tight_layout()
plt.savefig('feature_importance.png', dpi=300)
print("feature_importance.png saved successfully!")
