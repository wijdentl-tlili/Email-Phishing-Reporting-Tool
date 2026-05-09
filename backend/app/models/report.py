from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class Report(Base):

    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    sender = Column(String(255))

    subject = Column(Text)

    risk_score = Column(Integer, default=0)

    verdict = Column(String(50))

    raw_email = Column(Text)

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )