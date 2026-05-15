from app.services.parsers.email_parser import parse_eml

from app.services.analyzers.url_analyzer import analyze_url
from app.services.analyzers.header_analyzer import analyze_headers
from app.services.analyzers.html_analyzer import analyze_html
from app.services.analyzers.spoofing_analyzer import analyze_spoofing
from app.services.analyzers.attachment_analyzer import analyze_attachments
from app.services.analyzers.nlp_analyzer import analyze_nlp
from app.services.analyzers.domain_analyzer import analyze_domain
from app.services.analyzers.received_analyzer import analyze_received
from app.services.orchestration.risk_engine import calculate_risk
from app.services.orchestration.explanation_engine import build_explanation


def analyze_email(contents):

    parsed_email = parse_eml(contents)

    # URL analysis
    analyzed_urls = []

    for url in parsed_email["urls"]:

        analyzed_urls.append(
            analyze_url(url)
        )

    # Header analysis
    header_analysis = analyze_headers(
        parsed_email,
        contents
    )

    # HTML analysis
    html_analysis = analyze_html(
        parsed_email["html_body"]
    )

    # Spoofing analysis
    spoofing_analysis = analyze_spoofing(parsed_email)

    # Attachment analysis
    attachment_analysis = analyze_attachments(
        parsed_email.get("attachments", [])
    )

    # NLP analysis
    nlp_analysis = analyze_nlp(parsed_email.get("body", ""))

    # Domain analysis
    domain_analysis = analyze_domain(parsed_email.get("sender", ""))

    # Received analysis
    received_analysis = analyze_received(contents.decode(errors="ignore"))

    # Risk calculation
    risk = calculate_risk(
        parsed_email,
        analyzed_urls,
        header_analysis,
        html_analysis,
        spoofing_analysis,
        attachment_analysis,
        nlp_analysis,
        domain_analysis,
        received_analysis
    )
    explanation = build_explanation(
        indicators={
            "headers": header_analysis,
            "html": html_analysis,
            "spoofing": spoofing_analysis,
            "attachments": attachment_analysis,
            "nlp": nlp_analysis,
            "domain": domain_analysis,
            "received": received_analysis,
            "urls": analyzed_urls
        },
        risk_score=risk["score"]
    )

    return {
    "risk_assessment": risk,
    "indicators": {
        "headers": header_analysis,
        "html": html_analysis,
        "spoofing": spoofing_analysis,
        "attachments": attachment_analysis,
        "nlp": nlp_analysis,
        "domain": domain_analysis,
        "received": received_analysis,
        "urls": analyzed_urls
    },
    "parsed_email": parsed_email,
    "explanation": explanation,
}