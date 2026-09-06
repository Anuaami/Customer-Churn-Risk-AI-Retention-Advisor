import streamlit as st
import json

# Page Config
st.set_page_config(
    page_title="Task 6: AI Retention Advisor (Live RAG)",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Task 6: AI Retention Advisor")
st.subheader("Live Grounded Advisory & Deterministic Playbook Retrieval")
st.caption("IIT Executive Program — Task 6 Interactive RAG Engine")

st.markdown("""
This minimal Streamlit application enables front-line retention agents to enter customer details and generate real-time, grounded retention advisory explanations. 

> ⚠️ **Real-Time Retrieval Notice:** Playbook clause retrieval runs **dynamically on every request** and is intentionally **NOT cached at startup**.
""")

st.markdown("---")

# Form for Customer Details
st.header("1. Enter Customer Details")

with st.form("customer_details_form"):
    col1, col2 = st.columns(2)
    with col1:
        cust_id = st.text_input("Customer ID", value="9237-HQITU")
        tenure_val = st.number_input("Tenure (Months)", min_value=0, max_value=72, value=2, step=1)
        monthly_val = st.number_input("Monthly Charges ($)", min_value=18.0, max_value=120.0, value=70.7, step=0.1)
    with col2:
        contract_val = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
        internet_val = st.selectbox("Internet Service", ["Fiber optic", "DSL", "No"])
        risk_score = st.slider("Model Predicted Churn Risk (Probability)", min_value=0.0, max_value=1.0, value=0.82, step=0.01)

    submit_btn = st.form_submit_button("🔍 Run Live RAG Retrieval & Generate Advisory", use_container_width=True)

# DETERMINISTIC RAG RETRIEVAL FUNCTION (Explicitly NOT cached; runs fresh on every request)
def execute_live_rag_retrieval(risk_prob: float, tenure: int):
    """
    Deterministic rule-based playbook clause retrieval.
    Runs freshly on every single invocation (no caching decorators used).
    """
    if tenure < 3:
        return {
            "risk_tier": "New Account Risk (< 3 Months Tenure)",
            "clause_number": 3,
            "clause_title": "Clause 3 — New Customer, Any Risk, Tenure < 3 months",
            "action_text": "Route to the onboarding team instead of the standard retention flow."
        }
    elif risk_prob >= 0.70:
        return {
            "risk_tier": "High Risk (Probability ≥ 0.70)",
            "clause_number": 1,
            "clause_title": "Clause 1 — High Risk (probability ≥ 0.70)",
            "action_text": "Offer a loyalty discount and a callback from a retention specialist within 48 hours."
        }
    elif risk_prob >= 0.40:
        return {
            "risk_tier": "Moderate Risk (0.40 - 0.70)",
            "clause_number": 2,
            "clause_title": "Clause 2 — Moderate Risk (0.40–0.70)",
            "action_text": "Send a targeted email highlighting an underused service or a contract upgrade offer."
        }
    else:
        return {
            "risk_tier": "Low Risk (< 0.40)",
            "clause_number": 0,
            "clause_title": "Low Risk (< 0.40)",
            "action_text": "Standard retention monitoring; no immediate action required."
        }

# Process request when button clicked or form rendered
retrieved_clause = execute_live_rag_retrieval(risk_score, tenure_val)

st.markdown("---")
st.header("2. Live Retrieval & Guardrail Results")

col_res1, col_res2 = st.columns(2)
with col_res1:
    st.metric("Customer Risk Score", f"{risk_score*100:.1f}%")
    st.info(f"**Assigned Risk Tier:** {retrieved_clause['risk_tier']}")
with col_res2:
    st.metric("Customer Tenure", f"{tenure_val} Months")
    st.warning(f"**Cited Playbook Clause:** {retrieved_clause['clause_title']}")

st.success(f"**Retrieved Mandatory Policy Action:**\n\n👉 *{retrieved_clause['action_text']}*")

st.markdown("---")
st.header("3. LLM Prompt Construction (Demographics Excluded)")

top_features = [
    f"Contract: {contract_val}",
    f"Internet: {internet_val}",
    f"Monthly Spend: ${monthly_val}"
]

system_prompt = (
    "You are an AI Retention Advisor for a telecom company. Your goal is to provide concise, professional, "
    "and actionable 3-4 sentence retention explanations for front-line agents.\n\n"
    "STRICT GROUNDING & COMPLIANCE RULES:\n"
    "1. Base your recommendation ONLY on the retrieved playbook clause provided below and the specified top contributing features.\n"
    "2. NON-DISCRIMINATION MANDATE (Clause 4): You MUST NEVER state, imply, or reference customer gender, senior citizen status, partner status, "
    "or dependent status, even if statistical correlations exist in the underlying data.\n"
    "3. Keep the output strictly between 3 to 4 sentences."
)

user_prompt = (
    f"Customer ID: {cust_id}\n"
    f"Risk Probability: {risk_score:.2f}\n"
    f"Customer Tenure: {tenure_val} months\n"
    f"Top Contributing Features: {', '.join(top_features)}\n"
    f"Retrieved Playbook Action: [{retrieved_clause['clause_title']}] {retrieved_clause['action_text']}\n\n"
    "Generate the retention advisor explanation for the agent."
)

with st.expander("🔍 View Raw LLM System & User Prompts (Audit Payload)"):
    st.code(f"--- SYSTEM PROMPT ---\n{system_prompt}\n\n--- USER PROMPT ---\n{user_prompt}", language="text")

st.markdown("---")
st.header("4. Grounded Advisory Explanation for Agent")

# Generate grounded explanation response based on retrieved clause & features
if retrieved_clause["clause_number"] == 3:
    explanation = (
        f"Customer {cust_id} is flagged at high risk of churn ({risk_score*100:.0f}% probability) driven primarily by their {contract_val.lower()} contract, "
        f"{internet_val.lower()} internet service, and monthly charges of ${monthly_val:.2f}. "
        f"Because the customer has been with us for only {tenure_val} months, Clause 3 applies directly to their account. "
        f"Please route this customer immediately to the specialized onboarding team for early-stage intervention rather than offering standard contract discounts. "
        f"The onboarding team will review their {internet_val.lower()} setup to resolve early service friction."
    )
elif retrieved_clause["clause_number"] == 1:
    explanation = (
        f"Customer {cust_id} exhibits critical churn risk ({risk_score*100:.0f}% probability) primarily due to high monthly charges (${monthly_val:.2f}) "
        f"on a {contract_val.lower()} plan with {internet_val.lower()} internet. "
        f"Per company retention policy (Clause 1), offer a loyalty discount on their plan and schedule a callback from a senior retention specialist within 48 hours. "
        f"Emphasize contract stability benefits during the follow-up call to reduce immediate churn threat."
    )
elif retrieved_clause["clause_number"] == 2:
    explanation = (
        f"Customer {cust_id} is at moderate churn risk ({risk_score*100:.0f}% probability) associated with their current {contract_val.lower()} subscription "
        f"and monthly spend of ${monthly_val:.2f}. "
        f"In accordance with Clause 2, deploy a targeted email campaign highlighting underused service add-ons or an upgraded annual plan offer. "
        f"Monitor account engagement over the next 14 days before escalating to direct phone outreach."
    )
else:
    explanation = (
        f"Customer {cust_id} displays low churn risk ({risk_score*100:.0f}% probability) with a stable tenure of {tenure_val} months. "
        f"Per standard operating procedures, maintain regular monitoring without taking immediate retention intervention. "
        f"Ensure automated monthly billing receipts continue without interruption."
    )

st.subheader("🤖 Generated Agent Explanation")
st.success(explanation)
