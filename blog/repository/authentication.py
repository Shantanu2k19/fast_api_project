import os 
import jwt 
from datetime import datetime, timezone, timedelta

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    key = os.getenv("SECRET_KEY")
    algo = os.getenv("ALGORITHM")
    # print(f"key:{key}, algo:{algo}")
    if not key or not algo:
        print("missing")
        return ""
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key, algorithm=algo)
    return encoded_jwt
