from fastapi import FastAPI, Depends
from blog import schemas, database, models
from .database import engine, SessionLocal, get_db
app = FastAPI()

models.Base.metadata.create_all(engine)

from sqlalchemy.orm import Session


@app.get('/')
def hello_world():
    return {"message": "Hello world"}

@app.post('/blog')
def create(request: schemas.Blog, db:Session=Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog')
def all(db:Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}')
def get_blog_with_id(id:int, db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    return blog


# def get_all(db: Session):
#     blogs = db.query(models.Blog).all()
#     return blogs 
