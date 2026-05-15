import re

PRIVATE_IPS = [
    "10.",
    "172.",
    "192.168."
]


def analyze_received(headers_text):

    results = {
        "hop_count": 0,
        "has_private_ips": False,
        "suspicious_chain": False,
        "reasons": []
    }

    if not headers_text:

        return results

    # -------------------------
    # Count hops
    # -------------------------
    received_headers = re.findall(
        r"Received:",
        headers_text,
        re.IGNORECASE
    )

    results["hop_count"] = len(received_headers)

    if len(received_headers) > 8:

        results["suspicious_chain"] = True

        results["reasons"].append(
            "Excessive email relay hops detected"
        )

    # -------------------------
    # Private IP detection
    # -------------------------
    for ip_prefix in PRIVATE_IPS:

        if ip_prefix in headers_text:

            results["has_private_ips"] = True

            results["reasons"].append(
                "Private IP detected in email routing"
            )

    return results