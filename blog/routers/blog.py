from typing import List
from fastapi import APIRouter
from blog import schemas, database
from fastapi import Depends, status
from sqlalchemy.orm import Session
from blog.repository import blog

router = APIRouter(
    tags=['blogs'],
    prefix='/blog'
)

@router.get('/fetch_all', status_code=200, response_model=List[schemas.ShowBlog])
def get_resp_model(db:Session=Depends(database.get_db)):
    return blog.fetch_all_logic(db)

@router.post('/create', status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db:Session=Depends(database.get_db)):
    return blog.create_blog_logic(db, request)

@router.get('/fetch_with_id/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_blog_with_id(id:int, db:Session=Depends(database.get_db)):
    return blog.fetch_blog_with_id_logic(db, id)

@router.delete('/delete/{id}')
def delete_blog(id: int, db: Session=Depends(database.get_db)):
    return blog.delete_blog_logic(db, id)


@router.put('/update/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id:int, request_obj: schemas.Blog,db:Session=Depends(database.get_db)):
    return blog.update_blog_logic(db, id, request_obj)