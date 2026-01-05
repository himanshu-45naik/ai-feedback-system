from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes import reviews

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI-Feedback-System")

#CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reviews.router)

@app.get("/health")
def health():
    return {"status": "ok"}