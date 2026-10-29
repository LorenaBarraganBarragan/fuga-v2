from passlib.context import CryptContext
import re

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

COMMON_PASSWORDS = {
    "password123456", "123456789012", "qwertyuiop123", "administrator",
    "password12345", "123456789abc", "abcdefghijk1", "Password123456",
    "welcome123456", "letmein123456", "admin12345678"
}

def validate_password_strength(password: str) -> tuple[bool, str]:
    """Validate password meets D-09 requirements"""
    if len(password) < 12:
        return False, "Password must be at least 12 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    if password.lower() in [p.lower() for p in COMMON_PASSWORDS]:
        return False, "Password is too common"
    return True, "Valid"

def hash_password(password: str) -> str:
    """Hash password with bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)
