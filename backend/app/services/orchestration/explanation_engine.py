def build_explanation(indicators, risk_score):

    reasons = []

    # Collect all reasons safely
    for key in indicators:

        data = indicators[key]

        if isinstance(data, dict):

            reasons.extend(data.get("reasons", []))

    # Sort + clean duplicates
    unique_reasons = list(set(reasons))

    # Priority summary
    summary = []

    if risk_score >= 80:
        summary.append("🚨 High confidence phishing email detected")

    elif risk_score >= 50:
        summary.append("⚠️ Suspicious email with multiple risk signals")

    else:
        summary.append("✅ Low risk email")

    return {
        "summary": summary,
        "reasons": unique_reasons[:10] 
    }