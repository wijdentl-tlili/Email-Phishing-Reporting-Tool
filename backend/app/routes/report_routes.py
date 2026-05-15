from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal

from app.models.report import Report
from app.models.indicator import Indicator

from app.services.orchestration.analysis_orchestrator import analyze_email
from app.services.report_service import save_report


router = APIRouter()


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/analyze-email")
async def analyze_email_route(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    contents = await file.read()

    analysis = analyze_email(contents)

    report = save_report(
        db,
        analysis,
        contents
    )

    return {
        "status": "success",
        "report_id": report.id,
        "risk_assessment": analysis["risk_assessment"],
        "indicators": analysis["indicators"],
        "explanation": analysis["explanation"]
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

    if not report:

        return {
            "error": "Report not found"
        }

    return report.analysis_data