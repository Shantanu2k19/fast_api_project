from fastapi import APIRouter, Depends
from blog import schemas, database
from sqlalchemy.orm import Session
from blog.repository import user

router = APIRouter(
    tags=['users'],
    prefix='/user'
)

@router.post('/create', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db:Session=Depends(database.get_db)):
    return user.create_user_logic(request, db)

@router.get('/fetch/{id}', response_model=schemas.ShowUser)
def get_user(id:int, db:Session=Depends(database.get_db)):
    return user.fetch_user_logic(id, db)
