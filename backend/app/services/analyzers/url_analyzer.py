import math
import whois
import tldextract

from datetime import datetime
from urllib.parse import urlparse


SUSPICIOUS_TLDS = [
    "xyz",
    "top",
    "buzz",
    "click",
    "work",
    "country"
]


def calculate_entropy(text):

    prob = [float(text.count(c)) / len(text)
            for c in dict.fromkeys(list(text))]

    entropy = -sum([p * math.log(p) / math.log(2.0)
                    for p in prob])

    return entropy


def get_domain_age(domain):

    try:
        domain_info = whois.whois(domain)

        creation_date = domain_info.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if creation_date:

            age = (datetime.now() - creation_date).days

            return age

    except:
        return None


def analyze_url(url):

    parsed = urlparse(url)

    domain = parsed.netloc

    extracted = tldextract.extract(url)

    suffix = extracted.suffix

    entropy = calculate_entropy(domain)

    domain_age = get_domain_age(domain)

    suspicious = False

    reasons = []

    # Suspicious TLD
    if suffix in SUSPICIOUS_TLDS:
        suspicious = True
        reasons.append("Suspicious TLD")

    # High entropy
    if entropy > 4:
        suspicious = True
        reasons.append("High entropy domain")

    # Young domain
    if domain_age is not None and domain_age < 30:
        suspicious = True
        reasons.append("Recently created domain")

    # IP-based URL
    if domain.replace(".", "").isdigit():
        suspicious = True
        reasons.append("IP-based URL")

    return {
        "url": url,
        "domain": domain,
        "entropy": round(entropy, 2),
        "domain_age_days": domain_age,
        "suspicious": suspicious,
        "reasons": reasons
    }