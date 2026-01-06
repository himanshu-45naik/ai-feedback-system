from pydantic import BaseModel, Field
from typing import Optional

class ReviewCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    review_text: Optional[str] = ""

class ReviewResponse(BaseModel):
    id: int
    rating: int
    review_text: str
    ai_user_response: str
    ai_conclusion: str
    ai_summary: str
    ai_actions: str 
