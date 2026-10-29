from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class Database:
    client: AsyncIOMotorClient = None
    db = None

db = Database()

async def connect_to_mongo():
    try:
        if not settings.MONGODB_URI:
            raise ValueError("MONGODB_URI not configured")
        db.client = AsyncIOMotorClient(settings.MONGODB_URI)
        db.db = db.client[settings.MONGODB_DB]
        await db.client.admin.command('ping')
        print("Connected to MongoDB")
        await create_indexes()
    except Exception as e:
        print(f"Failed to connect to MongoDB: {type(e).__name__}")
        raise

async def close_mongo_connection():
    if db.client:
        try:
            db.client.close()
        except Exception:
            pass

async def create_indexes():
    if db.db is None:
        return
    await db.db.usuarios.create_index("correo", unique=True)
    await db.db.sesiones.create_index("jti")
    await db.db.sesiones.create_index("usuarioId")
    await db.db.sesiones.create_index("estado")
    await db.db.sesiones.create_index("refreshTokenHash")
    await db.db.login_attempts.create_index([("email", 1), ("ip", 1)])
    await db.db.login_attempts.create_index("timestamp")
    await db.db.login_attempts.create_index([("timestamp", 1)], expireAfterSeconds=3600)  # Cleanup after 1 hour
