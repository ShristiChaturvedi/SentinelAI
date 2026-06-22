import pandas as pd
from sklearn.ensemble import IsolationForest

# Load logs
df = pd.read_csv("logs.csv")

# Features for anomaly detection
X = df[["hour", "failed_logins", "data_downloaded"]]

# Train model
model = IsolationForest(
    contamination=0.25,
    random_state=42
)

# df["anomaly"] = model.fit_predict(X)
df["anomaly"] = model.fit_predict(X)

def risk_level(x):
    if x == -1:
        return "HIGH"
    return "LOW"

df["risk"] = df["anomaly"].apply(risk_level)

print(df)