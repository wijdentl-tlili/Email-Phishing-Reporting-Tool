from app.models.report import Report
from app.models.indicator import Indicator


def save_report(
    db,
    parsed_email,
    risk,
    analyzed_urls,
    raw_email
):

    report = Report(
        sender=parsed_email["sender"],
        subject=parsed_email["subject"],
        risk_score=risk["score"],
        verdict=risk["verdict"],
        raw_email=raw_email.decode(errors="ignore")
    )

    db.add(report)

    db.commit()

    db.refresh(report)

    # Save URL indicators
    for url_result in analyzed_urls:

        indicator = Indicator(
            report_id=report.id,
            indicator_type="url",
            value=url_result["url"],
            malicious=url_result["suspicious"]
        )

        db.add(indicator)

    db.commit()

    return report