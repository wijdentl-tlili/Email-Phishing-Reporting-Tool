from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal

from app.models.report import Report
from app.models.indicator import Indicator

from app.services.email_parser import parse_eml
from app.services.url_analyzer import analyze_url
from app.services.risk_engine import calculate_risk
from app.services.report_service import save_report

router = APIRouter()


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/analyze-email")
async def analyze_email(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    contents = await file.read()

    parsed_email = parse_eml(contents)

    analyzed_urls = []

    for url in parsed_email["urls"]:

        result = analyze_url(url)

        analyzed_urls.append(result)

    risk = calculate_risk(
        parsed_email,
        analyzed_urls
    )

    report = save_report(
        db,
        parsed_email,
        risk,
        analyzed_urls,
        contents
    )

    return {
        "status": "success",

        "report_id": report.id,

        "email_analysis": parsed_email,

        "url_analysis": analyzed_urls,

        "risk_assessment": risk
    }


@router.get("/reports")
def get_reports(db: Session = Depends(get_db)):

    reports = db.query(Report).all()

    return reports


@router.get("/reports/{report_id}")
def get_report(
    report_id: int,
    db: Session = Depends(get_db)
):

    report = db.query(Report).filter(
        Report.id == report_id
    ).first()

    indicators = db.query(Indicator).filter(
        Indicator.report_id == report_id
    ).all()

    return {
        "report": report,
        "indicators": indicators
    }