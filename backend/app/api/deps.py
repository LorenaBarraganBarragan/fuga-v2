from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security.tokens import verify_token
from app.core.database import db
from bson import ObjectId
from bson.errors import InvalidId

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    jti = payload.get("jti")
    if not user_id or not jti:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    try:
        user_obj_id = ObjectId(user_id)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = await db.db.usuarios.find_one({"_id": user_obj_id})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if user.get("estado") != "activo":
        raise HTTPException(status_code=403, detail="Account inactive")
    
    session = await db.db.sesiones.find_one({"jti": jti, "usuarioId": user_obj_id})
    if not session or session.get("estado") != "activa":
        raise HTTPException(status_code=401, detail="Session revoked")
    
    return {"user_id": str(user["_id"]), "email": user["correo"], "rol": user.get("rol", "usuario"), "jti": jti}
