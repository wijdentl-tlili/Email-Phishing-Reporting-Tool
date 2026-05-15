import re
from rapidfuzz import fuzz


# Known brands
KNOWN_BRANDS = [
    "paypal",
    "microsoft",
    "amazon",
    "google",
    "apple",
    "facebook",
    "instagram",
    "bank",
    "netflix"
]


def normalize(text):

    if not text:
        return ""

    return text.lower()


def detect_homoglyphs(domain):

    replacements = {
        "0": "o",
        "1": "l",
        "3": "e",
        "5": "s"
    }

    for k, v in replacements.items():

        domain = domain.replace(k, v)

    return domain


def extract_domain(email):

    match = re.search(r"@([a-zA-Z0-9.-]+)", email or "")

    if match:
        return match.group(1).lower()

    return ""


def analyze_spoofing(parsed_email):

    sender = parsed_email.get("sender", "")

    subject = parsed_email.get("subject", "")

    domain = extract_domain(sender)

    results = {
        "brand_impersonation": False,
        "typosquatting": False,
        "homoglyph_attack": False,
        "display_name_spoofing": False,
        "reasons": []
    }

    # -------------------------
    # 1. Extract display name
    # -------------------------
    if "<" in sender:

        display_name = sender.split("<")[0].strip()

        email_domain = domain

        # If display name is a brand but domain is unrelated
        for brand in KNOWN_BRANDS:

            if brand in normalize(display_name):

                if brand not in email_domain:

                    results["brand_impersonation"] = True

                    results["reasons"].append(
                        f"Brand impersonation detected: {brand}"
                    )

    # -------------------------
    # 2. Typosquatting detection
    # -------------------------
    for brand in KNOWN_BRANDS:

        similarity = fuzz.ratio(brand, domain)

        if 70 <= similarity < 95:

            results["typosquatting"] = True

            results["reasons"].append(
                f"Possible typosquatting: {domain} resembles {brand}"
            )

    # -------------------------
    # 3. Homoglyph detection
    # -------------------------
    cleaned_domain = detect_homoglyphs(domain)

    if cleaned_domain != domain:

        results["homoglyph_attack"] = True

        results["reasons"].append(
            "Possible homoglyph attack detected in domain"
        )

    # -------------------------
    # 4. Fake display name detection
    # -------------------------
    if sender.endswith("@gmail.com") or sender.endswith("@yahoo.com"):

        for brand in KNOWN_BRANDS:

            if brand in normalize(subject):

                results["display_name_spoofing"] = True

                results["reasons"].append(
                    "Free email provider used with brand context"
                )

    return results