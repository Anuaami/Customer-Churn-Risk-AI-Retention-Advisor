import json

def get_playbook_clause(risk_prob: float, tenure: int) -> dict:
    """
    Deterministic rule-based retrieval based on Playbook clauses:
    Clause 1 — High Risk (probability >= 0.70): Offer a loyalty discount and a callback from a retention specialist within 48 hours.
    Clause 2 — Moderate Risk (0.40 - 0.70): Send a targeted email highlighting an underused service or a contract upgrade offer.
    Clause 3 — New Customer, Any Risk, Tenure < 3 months: Route to the onboarding team instead of the standard retention flow.
    Clause 4 — Non-Discrimination Rule: Retention explanations must never state or imply that gender, senior-citizen status, or family/partner status contributed to a customer's risk score...
    """
    if tenure < 3:
        return {
            "clause_number": 3,
            "clause_title": "Clause 3 — New Customer, Any Risk, Tenure < 3 months",
            "text": "Route to the onboarding team instead of the standard retention flow."
        }
    elif risk_prob >= 0.70:
        return {
            "clause_number": 1,
            "clause_title": "Clause 1 — High Risk (probability >= 0.70)",
            "text": "Offer a loyalty discount and a callback from a retention specialist within 48 hours."
        }
    elif risk_prob >= 0.40:
        return {
            "clause_number": 2,
            "clause_title": "Clause 2 — Moderate Risk (0.40–0.70)",
            "text": "Send a targeted email highlighting an underused service or a contract upgrade offer."
        }
    else:
        return {
            "clause_number": 0,
            "clause_title": "Low Risk (< 0.40)",
            "text": "Standard retention monitoring; no immediate action required."
        }

def build_llm_prompt(customer_id: str, risk_prob: float, top_features: list, tenure: int, retrieved_clause: dict) -> dict:
    """
    Build system prompt and user prompt for Task 6.
    Strictly filters out demographic columns (gender, SeniorCitizen, Partner, Dependents).
    """
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
        f"Customer ID: {customer_id}\n"
        f"Risk Probability: {risk_prob:.2f}\n"
        f"Customer Tenure: {tenure} months\n"
        f"Top 3 Contributing Features: {', '.join(top_features)}\n"
        f"Retrieved Playbook Action: [{retrieved_clause['clause_title']}] {retrieved_clause['text']}\n\n"
        "Generate the retention advisor explanation for the agent."
    )
    
    return {
        "system_prompt": system_prompt,
        "user_prompt": user_prompt
    }

# Demonstration execution for Task 6 sample customer
if __name__ == "__main__":
    # Flagged high-risk customer sample
    sample_customer = {
        "customerID": "9237-HQITU",
        "risk_prob": 0.82,
        "tenure": 2, # Note: Tenure < 3 triggers Clause 3 per playbook rules!
        "top_features": ["Month-to-month contract", "Fiber optic internet service", "Payment method: Electronic check"]
    }
    
    clause_new = get_playbook_clause(sample_customer["risk_prob"], sample_customer["tenure"])
    prompt_new = build_llm_prompt(
        sample_customer["customerID"],
        sample_customer["risk_prob"],
        sample_customer["top_features"],
        sample_customer["tenure"],
        clause_new
    )
    
    print("--- TASK 6 GROUNDED ADVISORY TEST ---")
    print("Sample Customer:", sample_customer["customerID"])
    print("Retrieved Clause:", clause_new["clause_title"])
    print("\n[System Prompt]:\n", prompt_new["system_prompt"])
    print("\n[User Prompt]:\n", prompt_new["user_prompt"])
    
    # Sample high risk customer with tenure >= 3
    sample_customer_high_risk = {
        "customerID": "7892-POOKP",
        "risk_prob": 0.78,
        "tenure": 28,
        "top_features": ["Month-to-month contract", "Fiber optic internet service", "Payment method: Electronic check"]
    }
    clause_high = get_playbook_clause(sample_customer_high_risk["risk_prob"], sample_customer_high_risk["tenure"])
    prompt_high = build_llm_prompt(
        sample_customer_high_risk["customerID"],
        sample_customer_high_risk["risk_prob"],
        sample_customer_high_risk["top_features"],
        sample_customer_high_risk["tenure"],
        clause_high
    )
    print("\n--- SAMPLE HIGH RISK (TENURE >= 3) ---")
    print("Retrieved Clause:", clause_high["clause_title"])
    print("\n[Generated Prompt Output]:\n", prompt_high["user_prompt"])
