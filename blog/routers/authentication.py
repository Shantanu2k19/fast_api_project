from fastapi import APIRouter
from blog import schemas, database, models
from fastapi import Depends, status
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from .. hashing import Hash 
from blog.repository import authentication
from datetime import timedelta
import os
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

router = APIRouter(
    tags = ['auth']
)

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email==request.username).first()
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"mssg":"user not found"})
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"mssg":"incorrect password"})
    
    #generate a jwt token 
    access_token_expiry = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = authentication.create_access_token(
        data={"sub":user.email}, expires_delta=access_token_expiry
    )
    return schemas.Token(access_token=access_token, token_type="bearer")



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception

def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_token(data, credentials_exception)