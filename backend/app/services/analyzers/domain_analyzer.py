import whois
import re
from datetime import datetime

import dns.resolver


SUSPICIOUS_TLDS = [
    ".xyz", ".top", ".click", ".work",
    ".biz", ".info", ".live"
]


def extract_domain(email):

    match = re.search(r"@([a-zA-Z0-9.-]+)", email or "")

    if match:
        return match.group(1).lower()

    return None


def check_mx_records(domain):

    try:

        dns.resolver.resolve(domain, "MX")

        return True

    except Exception:

        return False


def analyze_domain(email):

    domain = extract_domain(email)

    results = {
        "domain": domain,
        "age_days": None,
        "is_new_domain": False,
        "suspicious_tld": False,
        "has_mx_records": True,
        "reasons": []
    }

    if not domain:

        return results

    # -------------------------
    # Suspicious TLD check
    # -------------------------
    for tld in SUSPICIOUS_TLDS:

        if domain.endswith(tld):

            results["suspicious_tld"] = True

            results["reasons"].append(
                f"Suspicious TLD detected: {tld}"
            )

    # -------------------------
    # MX records check
    # -------------------------
    has_mx = check_mx_records(domain)

    results["has_mx_records"] = has_mx

    if not has_mx:

        results["reasons"].append(
            "Domain has no MX records (suspicious)"
        )

    # -------------------------
    # WHOIS lookup
    # -------------------------
    try:

        w = whois.whois(domain)

        creation_date = w.creation_date

        if isinstance(creation_date, list):

            creation_date = creation_date[0]

        if creation_date:

            age_days = (datetime.utcnow() - creation_date).days

            results["age_days"] = age_days

            # New domain detection
            if age_days < 30:

                results["is_new_domain"] = True

                results["reasons"].append(
                    f"Domain is very new ({age_days} days old)"
                )

    except Exception:

        results["reasons"].append(
            "WHOIS lookup failed or blocked"
        )

    return results