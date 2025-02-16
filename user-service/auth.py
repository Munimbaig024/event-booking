from datetime import datetime, timedelta
from fastapi import HTTPException
from passlib.context import CryptContext
import jwt
import config
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Generate JWT token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)

def verify_token(authorization: str):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization token")

    try:
        token = authorization.split("Bearer ")[1]  # Extract token from "Bearer <TOKEN>"
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
        return payload  # Return decoded payload with user data

    except IndexError:
        raise HTTPException(status_code=401, detail="Invalid token format")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")