from fastapi import APIRouter, Depends
from blog import schemas, database
from sqlalchemy.orm import Session
from blog.repository import user
from blog.routers import authentication

router = APIRouter(
    tags=['users'],
    prefix='/user'
)


@router.post('/create', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db:Session=Depends(database.get_db), current_user: schemas.User = Depends(authentication.get_current_user)):
    return user.create_user_logic(request, db)


@router.get('/fetch/{id}', response_model=schemas.ShowUser)
def get_user(id:int, db:Session=Depends(database.get_db), current_user: schemas.User = Depends(authentication.get_current_user)):
    return user.fetch_user_logic(id, db)
