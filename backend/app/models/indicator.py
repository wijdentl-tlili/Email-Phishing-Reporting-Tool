from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from app.database import Base


class Indicator(Base):

    __tablename__ = "indicators"

    id = Column(Integer, primary_key=True, index=True)

    report_id = Column(
        Integer,
        ForeignKey("reports.id")
    )

    indicator_type = Column(String(50))

    value = Column(String(1000))

    malicious = Column(Boolean, default=False)