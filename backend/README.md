# FUGA+ Backend

FastAPI backend for FUGA+ application. 
- Python + FastAPI
- MongoDB Atlas
- JWT authentication with session management
- Deterministic expense processing (no external AI)
- Explainable leak detection
- Strict user data isolation

## Setup

1. Create virtual environment: `python -m venv venv`
2. Activate: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and configure
5. Run: `uvicorn app.main:app --reload`

## Structure

See plan maestro for full structure. Implements Must Have features first.
