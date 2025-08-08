from sqlalchemy import Column, String, Integer, TIMESTAMP, text
from app.database import Base


class ScanEvent(Base):
    __tablename__ = "scan_events"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))
