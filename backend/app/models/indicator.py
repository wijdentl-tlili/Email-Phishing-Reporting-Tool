from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Indicator(Base):

    __tablename__ = "indicators"

    id = Column(Integer, primary_key=True, index=True)

    report_id = Column(
        Integer,
        ForeignKey("reports.id"),
        nullable=False,
        index=True
    )

    indicator_type = Column(
        String(50),
        index=True,
        nullable=False
    )

    value = Column(String(1000), nullable=True)

    malicious = Column(Boolean, default=False)

    severity = Column(String(20), default="low")  # low | medium | high | critical

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    # Relationship back to Report
    report = relationship(
        "Report",
        back_populates="indicators"
    )