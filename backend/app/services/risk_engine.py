PHISHING_KEYWORDS = [
    "verify",
    "urgent",
    "password",
    "bank",
    "login",
    "suspended",
    "confirm"
]


def calculate_risk(parsed_email, analyzed_urls):

    score = 0

    reasons = []

    body = parsed_email["body"].lower()

    subject = parsed_email["subject"].lower()

    # Keyword analysis
    for keyword in PHISHING_KEYWORDS:

        if keyword in body or keyword in subject:

            score += 10

            reasons.append(
                f"Suspicious keyword detected: {keyword}"
            )

    # URL analysis
    for result in analyzed_urls:

        if result["suspicious"]:

            score += 25

            reasons.extend(result["reasons"])

    # Attachments
    if parsed_email["attachments"]:

        score += 10

        reasons.append("Email contains attachments")

    # Normalize
    if score > 100:
        score = 100

    # Verdict
    if score <= 30:
        verdict = "Safe"

    elif score <= 60:
        verdict = "Suspicious"

    else:
        verdict = "Phishing"

    return {
        "score": score,
        "verdict": verdict,
        "reasons": list(set(reasons))
    }