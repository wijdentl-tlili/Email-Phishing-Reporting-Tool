PHISHING_KEYWORDS = [
    "verify",
    "urgent",
    "password",
    "bank",
    "login",
    "suspended",
    "confirm"
]


def calculate_risk(parsed_email,
                    analyzed_urls,
                    header_analysis,
                    html_analysis, 
                    spoofing_analysis, 
                    attachment_analysis, 
                    nlp_analysis, 
                    domain_analysis, 
                    received_analysis):

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
    # SPF
    if header_analysis["spf"] != "pass":

        score += 20

    # DKIM
    if header_analysis["dkim"] != "pass":

        score += 20

    # DMARC
    if header_analysis["dmarc"] != "pass":

        score += 20

    # Return-Path mismatch
    if not header_analysis["from_return_path_match"]:

        score += 15

    # Reply-To mismatch
    if not header_analysis["from_reply_to_match"]:

        score += 15

    # Suspicious relays
    if header_analysis["suspicious_received_chain"]:

        score += 10

    reasons.extend(header_analysis["reasons"])

    # HTML phishing tricks
    if html_analysis["has_forms"]:

        score += 30

    if html_analysis["has_javascript"]:

        score += 20

    if html_analysis["mismatched_links"]:

        score += 35

    if html_analysis["hidden_elements"]:

        score += 15

    if html_analysis["has_base64_images"]:

        score += 10

    reasons.extend(
        html_analysis["reasons"]
    )
    

    # Spoofing attacks 
    if spoofing_analysis["brand_impersonation"]:

        score += 40

    if spoofing_analysis["typosquatting"]:

        score += 35

    if spoofing_analysis["homoglyph_attack"]:

        score += 30

    if spoofing_analysis["display_name_spoofing"]:

        score += 25

    reasons.extend(
        spoofing_analysis["reasons"]
    )

    # Attachment-based threats 

    if attachment_analysis["suspicious_files"]:

        score += 40

    if attachment_analysis["macro_files"]:

        score += 35

    if attachment_analysis["double_extensions"]:

        score += 45

    if attachment_analysis["archives"]:

        score += 15

    reasons.extend(
        attachment_analysis["reasons"]
    )


    # NLP social engineering signals 

    if nlp_analysis["urgency"]:

        score += 20

    if nlp_analysis["fear"]:

        score += 25

    if nlp_analysis["credential_harvesting"]:

        score += 40

    if nlp_analysis["reward_bait"]:

        score += 15

    reasons.extend(
        nlp_analysis["reasons"]
    )

    # Domain intelligence (VERY STRONG SIGNAL)

    if domain_analysis["is_new_domain"]:

        score += 35

    if domain_analysis["suspicious_tld"]:

        score += 20

    if not domain_analysis["has_mx_records"]:

        score += 30

    reasons.extend(
        domain_analysis["reasons"]
    )

    # Received Analysis
    if received_analysis["suspicious_chain"]:
        score += 25

    if received_analysis["has_private_ips"]:
        score += 20

    reasons.extend(received_analysis["reasons"])
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