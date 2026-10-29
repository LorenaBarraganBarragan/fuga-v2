"""
FUGA+ Backend API
FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import router as api_router
from app.core.database import connect_to_mongo, close_mongo_connection

app = FastAPI(
    title="FUGA+ API",
    description="API for FUGA+ expense tracking app",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    try:
        if not settings.is_jwt_config_valid() and settings.APP_ENV != "development":
            raise ValueError("Invalid JWT configuration")
        await connect_to_mongo()
    except Exception as e:
        print(f"Startup error: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "fuga-api"}

app.include_router(api_router, prefix=settings.API_V1_PREFIX)
