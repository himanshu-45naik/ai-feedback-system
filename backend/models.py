from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=False)
    review_text = Column(Text, nullable=True)
    ai_user_response = Column(Text) 
    ai_summary = Column(Text)
    ai_actions = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

