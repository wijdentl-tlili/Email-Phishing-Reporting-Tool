import re

URGENCY_KEYWORDS = [
    "urgent",
    "immediately",
    "within 24 hours",
    "your account will be closed",
    "action required",
    "as soon as possible"
]

FEAR_KEYWORDS = [
    "suspended",
    "unauthorized",
    "security alert",
    "login attempt",
    "breach",
    "compromised"
]

CREDENTIAL_KEYWORDS = [
    "password",
    "verify your account",
    "login details",
    "confirm your identity",
    "update payment",
    "credit card"
]

REWARD_KEYWORDS = [
    "won",
    "prize",
    "lottery",
    "gift",
    "free",
    "claim now"
]


def analyze_nlp(text):

    if not text:
        return {
            "urgency": False,
            "fear": False,
            "credential_harvesting": False,
            "reward_bait": False,
            "reasons": []
        }

    text_lower = text.lower()

    results = {
        "urgency": False,
        "fear": False,
        "credential_harvesting": False,
        "reward_bait": False,
        "reasons": []
    }

    # -------------------------
    # URGENCY DETECTION
    # -------------------------
    for word in URGENCY_KEYWORDS:

        if word in text_lower:

            results["urgency"] = True

            results["reasons"].append(
                f"Urgency manipulation detected: '{word}'"
            )

    # -------------------------
    # FEAR DETECTION
    # -------------------------
    for word in FEAR_KEYWORDS:

        if word in text_lower:

            results["fear"] = True

            results["reasons"].append(
                f"Fear-based manipulation detected: '{word}'"
            )

    # -------------------------
    # CREDENTIAL HARVESTING
    # -------------------------
    for word in CREDENTIAL_KEYWORDS:

        if word in text_lower:

            results["credential_harvesting"] = True

            results["reasons"].append(
                f"Credential harvesting attempt detected: '{word}'"
            )

    # -------------------------
    # REWARD / BAIT
    # -------------------------
    for word in REWARD_KEYWORDS:

        if word in text_lower:

            results["reward_bait"] = True

            results["reasons"].append(
                f"Social engineering reward bait detected: '{word}'"
            )

    return results