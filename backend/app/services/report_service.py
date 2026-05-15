from app.models.report import Report
from app.models.indicator import Indicator


def save_report(
    db,
    analysis,
    raw_email
):

    parsed_email = analysis["parsed_email"]

    risk = analysis["risk_assessment"]

    indicators = analysis["indicators"]

    report = Report(

        sender=parsed_email.get("sender"),

        subject=parsed_email.get("subject"),

        risk_score=risk.get("score"),

        verdict=risk.get("verdict"),

        raw_email=raw_email.decode(errors="ignore"),

        # FULL ANALYSIS STORED
        analysis_data=analysis
    )

    db.add(report)

    db.commit()

    db.refresh(report)

    # Save indicators separately too
    for indicator_type, values in indicators.items():

        if isinstance(values, list):

            for item in values:

                value = ""

                malicious = False

                if isinstance(item, dict):

                    value = str(item)

                    malicious = item.get(
                        "suspicious",
                        False
                    )

                else:
                    value = str(item)

                db_indicator = Indicator(
                    report_id=report.id,
                    indicator_type=indicator_type,
                    value=value,
                    malicious=malicious
                )

                db.add(db_indicator)

    db.commit()

    return report