def analyze_threat(user, failed_logins, downloads, hour):

    return f"""
Threat Assessment

User: {user}

Risk Indicators:
• Failed Logins: {failed_logins}
• Downloads: {downloads} MB
• Login Hour: {hour}

MITRE ATT&CK:
T1110 - Brute Force

Threat Severity:
HIGH

Recommended Actions:
• Lock Account
• Reset Credentials
• Review Endpoint Logs
• Monitor Lateral Movement
"""


def ask_security_question(question):

    question = question.lower()

    if "t1110" in question:
        return "T1110 is the MITRE ATT&CK technique for Brute Force attacks."

    elif "mitre" in question:
        return "MITRE ATT&CK is a knowledge base of adversary tactics and techniques used by cyber attackers."

    elif "soc" in question:
        return "A SOC analyst should investigate logs, isolate compromised assets, and perform incident response."

    else:
        return "Threat Intelligence Agent is running in offline mode."