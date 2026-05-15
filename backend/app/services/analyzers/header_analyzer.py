import re
from email.utils import parseaddr


def extract_domain(email_address):

    if not email_address:
        return None

    parsed = parseaddr(email_address)[1]

    if "@" not in parsed:
        return None

    return parsed.split("@")[1].lower()


def analyze_headers(parsed_email, raw_email):

    results = {
        "spf": "unknown",
        "dkim": "unknown",
        "dmarc": "unknown",
        "from_return_path_match": True,
        "from_reply_to_match": True,
        "suspicious_received_chain": False,
        "reasons": []
    }

    headers = raw_email.decode(errors="ignore")

    from_header = parsed_email.get("from")

    return_path = parsed_email.get("return_path")

    reply_to = parsed_email.get("reply_to")

    # Domain extraction
    from_domain = extract_domain(from_header)

    return_path_domain = extract_domain(return_path)

    reply_to_domain = extract_domain(reply_to)

    # SPF
    spf_match = re.search(
        r"spf=(pass|fail|softfail|neutral)",
        headers,
        re.IGNORECASE
    )

    if spf_match:

        results["spf"] = spf_match.group(1).lower()

        if results["spf"] != "pass":

            results["reasons"].append(
                f"SPF failed: {results['spf']}"
            )

    # DKIM
    dkim_match = re.search(
        r"dkim=(pass|fail|neutral)",
        headers,
        re.IGNORECASE
    )

    if dkim_match:

        results["dkim"] = dkim_match.group(1).lower()

        if results["dkim"] != "pass":

            results["reasons"].append(
                f"DKIM failed: {results['dkim']}"
            )

    # DMARC
    dmarc_match = re.search(
        r"dmarc=(pass|fail|bestguesspass)",
        headers,
        re.IGNORECASE
    )

    if dmarc_match:

        results["dmarc"] = dmarc_match.group(1).lower()

        if results["dmarc"] != "pass":

            results["reasons"].append(
                f"DMARC failed: {results['dmarc']}"
            )

    # From vs Return-Path
    if from_domain and return_path_domain:

        if from_domain != return_path_domain:

            results["from_return_path_match"] = False

            results["reasons"].append(
                "From domain does not match Return-Path"
            )

    # From vs Reply-To
    if from_domain and reply_to_domain:

        if from_domain != reply_to_domain:

            results["from_reply_to_match"] = False

            results["reasons"].append(
                "From domain does not match Reply-To"
            )

    # Received chain analysis
    received_count = headers.lower().count("received:")

    if received_count > 10:

        results["suspicious_received_chain"] = True

        results["reasons"].append(
            "Suspicious number of mail relays"
        )

    return results