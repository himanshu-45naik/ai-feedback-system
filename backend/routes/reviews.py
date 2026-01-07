from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import ReviewCreate, ReviewResponse
from models import Review
from llm_service import analyze_review
from pydantic import ValidationError

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/submit-review", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def submit_review(data: ReviewCreate, db: Session = Depends(get_db)):
    """
    Submit a customer review with AI-powered analysis
    
    - **rating**: Integer between 1-5
    - **review_text**: Optional text (10-5000 characters if provided)
    """
    try:
        # Analyze review (handles empty reviews internally)
        analysis = analyze_review(data.rating, data.review_text or "")
        
        # Create review record
        review = Review(
            rating=data.rating,
            review_text=data.review_text or "",
            ai_user_response=analysis["user_response"],
            ai_conclusion=analysis["conclusion"],
            ai_summary=analysis["summary"],
            ai_actions=analysis["actions"],
        )
        
        db.add(review)
        db.commit()
        db.refresh(review)
        
        return review
    
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {str(e)}"
        )
    
    except Exception as e:
        db.rollback()
        print(f"ERROR in submit_review: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process review. Please try again later."
        )

@router.get("/admin/reviews")
def get_reviews(db: Session = Depends(get_db)):
    """
    Retrieve all reviews for admin dashboard
    
    Returns reviews ordered by most recent first
    """
    try:
        return db.query(Review).order_by(Review.created_at.desc()).all()
    except Exception as e:
        print(f"ERROR in get_reviews: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve reviews"
        )