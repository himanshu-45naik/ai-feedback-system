from pydantic import BaseModel, Field, field_validator
from typing import Optional

class ReviewCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    review_text: Optional[str] = Field(default="", max_length=5000)
    
    @field_validator('review_text')
    @classmethod
    def validate_review_text(cls, v: str) -> str:
        if v is None:
            return ""
        
        v = v.strip()
        
        # Enforce minimum length if text is provided
        if v and len(v) < 10:
            raise ValueError("Review must be at least 10 characters if provided")
        
        # Enforce maximum length
        if len(v) > 5000:
            raise ValueError("Review cannot exceed 5000 characters")
        
        return v

class ReviewResponse(BaseModel):
    id: int
    rating: int
    review_text: str
    ai_user_response: str
    ai_conclusion: str
    ai_summary: str
    ai_actions: str