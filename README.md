# 🔮 Customer Churn Risk & AI Retention Advisor

An end-to-end enterprise machine learning and GenAI Retrieval-Augmented Generation (RAG) platform built for telecom customer churn analytics, predictive risk modeling, strategic customer segmentation, and compliant AI-driven retention advisory.

---

## 📌 Project Overview

Customer churn is a critical business challenge in the telecom industry. This repository delivers a production-ready solution that combines:
1. **Exploratory Data Analysis & KPI Insights:** Quantifying churn drivers across contract types and service tiers.
2. **Predictive Churn Modeling:** Comparing interpretable Baseline (Logistic Regression) vs. Complex (Random Forest) models.
3. **Machine Learning Customer Segmentation:** Identifying high-risk, high-value customer clusters using K-Means.
4. **Deterministic RAG Advisory Layer:** A compliant GenAI system providing grounded retention playbooks while enforcing a strict non-discrimination mandate.
5. **Interactive Web Application:** A feature-rich Streamlit dashboard for executives and retention agents.

---

## 📊 Key Highlights & Performance Summary

| Metric / Section | Finding / Value |
| :--- | :--- |
| **Total Dataset Size** | 7,043 Customers |
| **Overall Churn Rate** | **26.54%** (1,869 churned) |
| **Highest Churn Contract** | Month-to-month (**42.71%**) |
| **Highest Churn Service** | Fiber Optic Internet (**41.89%**) |
| **Baseline Model (Logistic Reg)** | Test Accuracy: **80.62%** \| Test Recall: **55.88%** \| Test ROC-AUC: **0.8422** |
| **Complex Model (Random Forest)** | Test Accuracy: **80.70%** \| Test Recall: **50.27%** \| Test ROC-AUC: **0.8426** |
| **Target Segment (Cluster 3)** | **1,960 Accounts** with **62.35% actual churn rate** ($153,464 monthly spend at risk) |

---

## 🏗️ Project Architecture & Directory Structure

```text
Customer-Churn-Risk-AI-Retention-Advisor/
│
├── WA_Fn-UseC_-Telco-Customer-Churn.csv   # Telco Churn Dataset
├── run_pipeline.py                         # End-to-end ML pipeline (Tasks 1-5)
├── app.py                                  # Streamlit Interactive Dashboard
├── summary_stats.json                      # Machine-readable output metrics
├── Executive_Memo_and_Board_Report.md      # One-Page CFO Board Memo & Technical Report
├── README.md                               # Project documentation
├── requirements.txt                        # Python dependencies
│
└── src/
    └── genai_advisor.py                    # Task 6 RAG retrieval & prompt guardrail engine
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+ installed on your system.

### 2. Installation
Clone the repository and set up a virtual environment:

```bash
# Clone the repository
git clone https://github.com/Anuaami/Customer-Churn-Risk-AI-Retention-Advisor.git
cd Customer-Churn-Risk-AI-Retention-Advisor

# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🏃 Execution Guide

### Step 1: Run the Complete ML Pipeline
Execute `run_pipeline.py` to run data cleaning, model training, evaluation, feature importance analysis, and customer segmentation:

```bash
python run_pipeline.py
```
*Outputs generated:* Prints all task evaluation metrics and updates `summary_stats.json`.

### Step 2: Test the GenAI Advisory Layer & Guardrails
Execute `src/genai_advisor.py` to test deterministic RAG clause retrieval and demographic sanitization:

```bash
python src/genai_advisor.py
```

### Step 3: Launch the Streamlit Web Application
Launch the interactive web dashboard:

```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🛡️ Governance & Non-Discrimination Guardrails (Clause 4)

To adhere to enterprise compliance rules:
- **Data Minimization:** Demographic variables (`gender`, `SeniorCitizen`, `Partner`, `Dependents`) are physically stripped out before prompt creation.
- **Deterministic RAG Retrieval:** Playbook actions (Clause 1–3) are assigned in code via deterministic rules rather than relying on ungrounded LLM inference, preventing citation hallucinations.
- **Audit-Ready Prompt Payload:** Every LLM prompt payload is constructed exclusively from non-demographic operational metrics (`tenure`, `MonthlyCharges`, `Contract`, `InternetService`, `PaymentMethod`, and `Predicted_Churn_Prob`).

---

## 📄 Documentation & Reports
- Detailed executive findings and CFO recommendation: See [`Executive_Memo_and_Board_Report.md`](file:///c:/Users/anupa/Customer-Churn-Risk-AI-Retention-Advisor/Executive_Memo_and_Board_Report.md).
- Pipeline summary metrics: See [`summary_stats.json`](file:///c:/Users/anupa/Customer-Churn-Risk-AI-Retention-Advisor/summary_stats.json).

---

## 📜 License
This project is open-source and licensed under the [MIT License](file:///c:/Users/anupa/Customer-Churn-Risk-AI-Retention-Advisor/LICENSE).
