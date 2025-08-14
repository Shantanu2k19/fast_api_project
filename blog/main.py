from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from blog import schemas, database, models
from .database import engine, SessionLocal, get_db
app = FastAPI()

models.Base.metadata.create_all(engine)
#Base.metadata is a container of table definitions for all models registered with that Base
#create_all(engine) Sends CREATE TABLE IF NOT EXISTS ... SQL commands to the database via the engine
from sqlalchemy.orm import Session


@app.get('/', tags=['init'])
def hello_world():
    return {"message": "Hello world"}

@app.post('/create_blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create_blog(request: schemas.Blog, db:Session=Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit() #saves the data to db from memory/session
    db.refresh(new_blog)  #reloads object from db with latest data
    return new_blog

@app.get('/all_blog', tags=['blogs'])
def all_blogs(db:Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog_withId/{id}', status_code=status.HTTP_200_OK, tags=['blogs'])
def get_blog_with_id(id:int, response_obj: Response, db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "messg": "blog not found"
        })
        # response_obj.status_code = status.HTTP_404_NOT_FOUND
        # return {
        #     "Message": "Blog not found"
        # }
    return blog

@app.delete('/blog_del/{id}', tags=['blogs'])
def delete_blog(id: int, response_obj: Response, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"mssg":"Blog not found"})
    
    db.delete(blog)
    db.commit()
    return {"mssg": "Delete success"}


@app.put('/blog_update/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update_blog(id:int, request_obj: schemas.Blog,db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    # blog = db.query(models.Blog).filter(models.Blog.id==id).update({'title':'Updated title'})
    #  db.query(models.Blog).filter(models.Blog.id==id).update(request_obj)
    if blog:
        blog.title = 'Updated title'
        db.commit()
        return {"mssg": "updated"} 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"mssg": "Not found"})


### RESPONSE MODEL 
#validates and shapes data into schema before returning 
#here the response will return in form of ShowBlog
@app.get('/blog_resp/{id}', status_code=200, response_model=schemas.ShowBlog, tags=['response'])
def get_resp_model(id:int, db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "messg": "blog not found"
        })
    return blog

@app.get('/blog_all', status_code=200, response_model=List[schemas.ShowBlog], tags=['response'])
def get_resp_model(id:int, db:Session=Depends(get_db)):
    return db.query(models.Blog).all()


######## USER
@app.post('/user_create', tags=['user'])
def create_user(request: schemas.User, db:Session=Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=request.password)
    # new_user = models.User(**request.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 