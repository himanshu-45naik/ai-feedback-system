from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import ReviewCreate, ReviewResponse
from models import Review
from llm_service import analyze_review

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/submit-review", response_model=ReviewResponse)
def submit_review(data: ReviewCreate, db: Session= Depends(get_db)):
    analysis = analyze_review(data.rating, data.review_text or "")

    review = Review(
        rating=data.rating,
        review_text=data.review_text,
        ai_user_response=analysis["user_response"],
        ai_conclusion=analysis["conclusion"],
        ai_summary=analysis["summary"],
        ai_actions=analysis["actions"],
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    return review

@router.get("/admin/reviews")
def get_reviews(db: Session = Depends(get_db)):
    return db.query(Review).order_by(Review.created_at.desc()).all()