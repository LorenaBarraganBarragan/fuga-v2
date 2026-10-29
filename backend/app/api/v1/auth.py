from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.schemas.auth import UserRegister, UserLogin, TokenResponse, RefreshTokenRequest, MessageResponse
from app.core.security.passwords import hash_password, verify_password, validate_password_strength
from app.core.security.tokens import create_access_token, create_refresh_token, hash_refresh_token
from app.core.database import db
from app.core.config import settings
from app.api.deps import get_current_user
from datetime import datetime, timedelta
from bson import ObjectId
from bson.errors import InvalidId
import secrets

router = APIRouter()
security = HTTPBearer()

@router.post("/register", response_model=MessageResponse)
async def register(user_data: UserRegister):
    valid, msg = validate_password_strength(user_data.password)
    if not valid:
        raise HTTPException(status_code=400, detail=msg)
    
    existing = await db.db.usuarios.find_one({"correo": user_data.email.lower()})
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    
    user = {
        "correo": user_data.email.lower(),
        "contrasenaHash": hash_password(user_data.password),
        "nombre": user_data.nombre,
        "rol": "usuario",
        "estado": "activo",
        "fechaCreacion": datetime.utcnow()
    }
    try:
        await db.db.usuarios.insert_one(user)
    except Exception:
        raise HTTPException(status_code=409, detail="Email already registered")
    
    return {"message": "User registered successfully"}

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, request: Request):
    client_ip = request.client.host if request.client else "unknown"
    email = credentials.email.lower()
    
    now = datetime.utcnow()
    window_start = now - timedelta(minutes=settings.LOGIN_ATTEMPT_WINDOW_MINUTES)
    
    attempts = await db.db.login_attempts.count_documents({
        "email": email,
        "ip": client_ip,
        "timestamp": {"$gte": window_start},
        "success": False
    })
    
    if attempts >= settings.MAX_LOGIN_ATTEMPTS:
        raise HTTPException(status_code=429, detail="Too many login attempts")
    
    user = await db.db.usuarios.find_one({"correo": email})
    if not user or not verify_password(credentials.password, user["contrasenaHash"]):
        await db.db.login_attempts.insert_one({
            "email": email,
            "ip": client_ip,
            "timestamp": now,
            "success": False
        })
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if user.get("estado") != "activo":
        await db.db.login_attempts.insert_one({
            "email": email,
            "ip": client_ip,
            "timestamp": now,
            "success": False
        })
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    await db.db.login_attempts.insert_one({
        "email": email,
        "ip": client_ip,
        "timestamp": now,
        "success": True
    })
    
    jti = secrets.token_urlsafe(32)
    access_token = create_access_token({"sub": str(user["_id"]), "jti": jti})
    refresh_token = create_refresh_token()
    refresh_token_hash = hash_refresh_token(refresh_token)
    
    session = {
        "usuarioId": user["_id"],
        "jti": jti,
        "refreshTokenHash": refresh_token_hash,
        "refreshTokenFamily": secrets.token_urlsafe(16),
        "estado": "activa",
        "expRefresh": datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        "creadoEn": datetime.utcnow(),
        "ultimoUso": datetime.utcnow(),
        "rotatedAt": None
    }
    await db.db.sesiones.insert_one(session)
    
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh", response_model=TokenResponse)
async def refresh_tokens(token_req: RefreshTokenRequest):
    refresh_token_hash = hash_refresh_token(token_req.refresh_token)
    session = await db.db.sesiones.find_one({"refreshTokenHash": refresh_token_hash})
    
    if not session:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    if session.get("estado") != "activa":
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    if datetime.utcnow() > session["expRefresh"]:
        await db.db.sesiones.update_one({"_id": session["_id"]}, {"$set": {"estado": "revocada", "revocadoEn": datetime.utcnow()}})
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    user = await db.db.usuarios.find_one({"_id": session["usuarioId"]})
    if not user or user.get("estado") != "activo":
        await db.db.sesiones.update_one({"_id": session["_id"]}, {"$set": {"estado": "revocada", "revocadoEn": datetime.utcnow()}})
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    new_refresh_token = create_refresh_token()
    new_refresh_token_hash = hash_refresh_token(new_refresh_token)
    
    # Atomic rotation - if already rotated or modified concurrently, detect reuse
    result = await db.db.sesiones.update_one(
        {"_id": session["_id"], "estado": "activa", "refreshTokenHash": refresh_token_hash},
        {"$set": {"refreshTokenHash": new_refresh_token_hash, "ultimoUso": datetime.utcnow(), "rotatedAt": datetime.utcnow()}}
    )
    
    if result.modified_count == 0:
        # Token reuse detected - revoke this session
        await db.db.sesiones.update_one({"_id": session["_id"]}, {"$set": {"estado": "revocada", "revocadoEn": datetime.utcnow()}})
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    access_token = create_access_token({"sub": str(user["_id"]), "jti": session["jti"]})
    
    return {"access_token": access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}

@router.post("/logout", response_model=MessageResponse)
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security), current_user: dict = Depends(get_current_user)):
    jti = current_user.get("jti")
    user_id = current_user.get("user_id")
    if not jti or not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    try:
        user_obj_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    result = await db.db.sesiones.update_one(
        {"jti": jti, "usuarioId": user_obj_id, "estado": "activa"},
        {"$set": {"estado": "revocada", "revocadoEn": datetime.utcnow()}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=401, detail="Session already revoked")
    
    return {"message": "Logged out successfully"}

@router.get("/me")
async def me(current_user: dict = Depends(get_current_user)):
    return {"user_id": current_user["user_id"], "email": current_user["email"], "rol": current_user["rol"]}
