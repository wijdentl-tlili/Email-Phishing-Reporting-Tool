from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import JSON

from app.database import Base


class Report(Base):

    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        index=True
    )

    sender = Column(String(255), nullable=False)

    subject = Column(Text, nullable=True)

    risk_score = Column(Integer, default=0)

    verdict = Column(String(50), default="Unknown")

    raw_email = Column(Text, nullable=False)

    # FULL SOC REPORT JSON
    analysis_data = Column(JSON, nullable=True)

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    indicators = relationship(
        "Indicator",
        back_populates="report",
        cascade="all, delete-orphan"
    )