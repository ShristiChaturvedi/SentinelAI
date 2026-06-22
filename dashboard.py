from threat_agent import (
    analyze_threat,
    ask_security_question
)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="SentinelAI",
    page_icon="🛡️",
    layout="wide"
)
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

h1 {
    color: #00C8FF;
    text-align: center;
}

h2, h3 {
    color: white;
}

div[data-testid="metric-container"] {
    background-color: #1E1E1E;
    border: 1px solid #2D3748;
    padding: 15px;
    border-radius: 10px;
}

.stAlert {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv("logs.csv")

# ==========================================
# ANOMALY DETECTION ENGINE
# ==========================================

X = df[["hour", "failed_logins", "data_downloaded"]]

model = IsolationForest(
    contamination=0.25,
    random_state=42
)

df["anomaly"] = model.fit_predict(X)

# ==========================================
# RISK SCORING ENGINE
# ==========================================

df["risk_score"] = (
    df["failed_logins"] * 10
    + df["data_downloaded"] * 0.2
)

df["risk_score"] = df["risk_score"].clip(upper=100)

# Increase score if anomaly detected
df.loc[df["anomaly"] == -1, "risk_score"] += 20

df["risk_score"] = df["risk_score"].clip(upper=100)

# ==========================================
# RISK CLASSIFICATION
# ==========================================

def risk_level(score):

    if score >= 70:
        return "HIGH"

    elif score >= 40:
        return "MEDIUM"

    return "LOW"


df["risk"] = df["risk_score"].apply(risk_level)

# ==========================================
# DASHBOARD HEADER
# ==========================================

st.title("🛡️ SentinelAI")
st.info("""
AI-powered cyber resilience platform for critical infrastructure.
Detects anomalies, maps threats to MITRE ATT&CK,
predicts attacker progression, and recommends response actions.
""")
st.subheader("AI-Powered Cyber Resilience Platform")

# ==========================================
# KPI METRICS
# ==========================================

total_users = len(df)
threats = len(df[df["risk"] == "HIGH"])
safe = len(df[df["risk"] == "LOW"])

col1, col2, col3 = st.columns(3)

col1.metric("Total Assets Monitored", total_users)
col2.metric("Threats Detected", threats)
col3.metric("Safe Assets", safe)

# ==========================================
# RISK DISTRIBUTION
# ==========================================
st.divider()
st.subheader("Risk Distribution")

risk_counts = df["risk"].value_counts()

fig, ax = plt.subplots(figsize=(2, 1))

risk_counts.plot(
    kind="bar",
    ax=ax
)

ax.set_ylabel("Count")
ax.set_xlabel("Risk Level")
st.pyplot(fig)

# ==========================================
# HIGH RISK USERS
# ==========================================
st.divider()
st.subheader("High Risk Users")

high_risk = df[df["risk"] == "HIGH"]

st.dataframe(high_risk)

# ==========================================
# MITRE ATT&CK MAPPING
# ==========================================
st.divider()
st.subheader("MITRE ATT&CK Mapping")

mitre_data = []

for _, row in high_risk.iterrows():

    if row["failed_logins"] >= 5:
        technique = "T1110 - Brute Force"

    elif row["data_downloaded"] > 150:
        technique = "T1041 - Data Exfiltration"

    else:
        technique = "T1078 - Valid Accounts"

    mitre_data.append(
        {
            "User": row["user"],
            "Technique": technique
        }
    )

mitre_df = pd.DataFrame(mitre_data)

st.dataframe(mitre_df)

# ==========================================
# AI THREAT ANALYSIS
# ==========================================
st.divider()
st.subheader("AI Threat Analysis")

for _, row in high_risk.iterrows():

    analysis = analyze_threat(
        row["user"],
        row["failed_logins"],
        row["data_downloaded"],
        row["hour"]
    )

    st.warning(analysis)

# ==========================================
# ATTACK PREDICTION AGENT
# ==========================================
st.divider()
st.subheader("Attack Progression Prediction")

for _, row in high_risk.iterrows():

    if row["failed_logins"] >= 5:

        next_stage = "Credential Compromise"

    elif row["data_downloaded"] > 150:

        next_stage = "Data Exfiltration"

    else:

        next_stage = "Lateral Movement"

    st.info(
        f"""
User: {row['user']}

Predicted Next Attack Stage:
{next_stage}
"""
    )

# ==========================================
# RESPONSE ORCHESTRATOR
# ==========================================
st.divider()
st.subheader("Automated Response")

for _, row in high_risk.iterrows():

    if row["risk_score"] >= 90:

        st.error(
            f"""
User: {row['user']}

Actions Executed:
• Account Locked
• IP Blocked
• Security Team Notified
• Incident Ticket Created
"""
        )

st.subheader("Threat Intelligence Assistant")

question = st.text_input(
    "Ask a cybersecurity question",
    key="security_chat"
)

if question:
    answer = ask_security_question(question)
    st.success(answer)


# ==========================================
# COMPLETE SECURITY LOGS
# ==========================================
st.divider()
st.subheader("Complete Security Logs")

st.dataframe(df)
st.markdown("---")
st.caption(
    "SentinelAI | AI-Driven Cyber Resilience Platform"
)