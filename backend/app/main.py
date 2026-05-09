from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base

from app.models.user import User
from app.models.report import Report
from app.models.indicator import Indicator

from app.routes.user_routes import router as user_router
from app.routes.report_routes import router as report_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PhishGuard API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(report_router)


@app.get("/")
def root():
    return {
        "message": "PhishGuard API Running"
    }