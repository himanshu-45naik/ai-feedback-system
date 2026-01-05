# AI Feedback System

This repository contains a **production-style AI feedback system**

The system demonstrates:
- Prompt-driven LLM usage
- Backend-first API design
- Persistent storage
- Real web dashboards 
- End-to-end deployment readiness

---

## 📌 Project Overview

The application consists of **two dashboards** backed by a shared FastAPI backend and PostgreSQL database:

### 1. User Dashboard (Public)
- Users select a star rating (1–5)
- Write a short review
- Submit feedback
- Receive an **AI-generated response** in real time

### 2. Admin Dashboard (Internal)
- View all submitted reviews
- See:
  - User rating
  - User review
  - AI-generated summary
  - AI-recommended actions
- Data persists across refreshes

All AI logic is handled **server-side** using an LLM (Gemini).

---

## 🧱 Tech Stack

### Backend
- **FastAPI**
- **PostgreSQL** (Render)
- **SQLAlchemy**
- **Pydantic**
- **Gemini API** (LLM)

### Frontend
- HTML
- CSS
- JavaScript


### Deployment
- Backend: Render
- Frontend: Vercel 

---

## 📁 Project Structure

```
ai-feedback-system/
│
├── backend/
│   ├── main.py 
│   ├── routes
│   │    ├── reviews.py          
│   ├── models.py               
|   ├── schemas.py
│   ├── database.py            
│   ├── llm_service.py          
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── user/
│   │   ├── index.html
│   │   ├── style.css
│   │   └── script.js
│   │
│   └── admin/
│       ├── index.html
│       ├── style.css
│       └── script.js
│
└── README.md
```

# ⚙️ Running the Project Locally
## 🔹 Backend Setup (FastAPI)

### 1. Navigate to backend
```bash
cd backend
```
### 2. Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Create .env file
### 5. Run the backend
```bash
uvicorn main:app --reload
```

## 🔹 Frontend Setup (User & Admin Dashboards)
### 1. Run User Dashboard
```
cd frontend/user
python3 -m http.server 5500
```

### 2. Run Admin Dashboard 
```bash
cd frontend/admin
python3 -m http.server 5501
```

### 🔄 End-to-End Flow (Local)

- Open User Dashboard

- Submit rating + review

- AI-generated response appears

- Open Admin Dashboard

- Submitted review appears with AI summary & actions

- Refresh pages → data persists

