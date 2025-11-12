from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from database.base import Base

class Scan(Base):
     __tablename__ = "scans"
     id = Column(Integer, primary_key=True, index=True)
     video_name = Column(String, nullable=False)
     result = Column(String, nullable=False)
     confidence = Column(Float, nullable = False)
     user_email = Column(String, ForeignKey("users.email"), nullable=False)
     created_at = Column(DateTime(timezone=True), server_default=func.now())
     lime_image = Column(String, nullable = True)


