from fastapi import FastAPI, Depends, status, Response, HTTPException
from blog import schemas, database, models
from .database import engine, SessionLocal, get_db
app = FastAPI()

models.Base.metadata.create_all(engine)

from sqlalchemy.orm import Session


@app.get('/')
def hello_world():
    return {"message": "Hello world"}

@app.post('/blog', status_code=status.HTTP_201_CREATED)
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

@app.get('/blog/{id}', status_code=status.HTTP_200_OK)
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

@app.delete('/blog/{id}')
def delete_blog(id: int, response_obj: Response, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"mssg":"Blog not found"})
    
    db.delete(blog)
    db.commit()
    return {"mssg": "Delete success"}


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id:int, request_obj: schemas.Blog,db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    # blog = db.query(models.Blog).filter(models.Blog.id==id).update({'title':'Updated title'})
    #  db.query(models.Blog).filter(models.Blog.id==id).update(request_obj)
    if blog:
        blog.title = 'Updated title'
        db.commit()
        return {"mssg": "updated"}  
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"mssg": "Not found"})


# def get_all(db: Session):
#     blogs = db.query(models.Blog).all()
#     return blogs 
